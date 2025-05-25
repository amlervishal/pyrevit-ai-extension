# -*- coding: utf-8 -*-
"""
AI client utilities for Revit Function Call - Windows Compatible Version
"""
import sys
import os
import json

# Handle Python 2/3 compatibility for pyRevit (typically IronPython 2.7 on Windows)
try:
    # Python 3
    import urllib.request as urllib_request
    import urllib.parse as urllib_parse
    import urllib.error as urllib_error
    PYTHON_VERSION = 3
except ImportError:
    # Python 2 / IronPython
    import urllib2 as urllib_request
    import urllib as urllib_parse
    import urllib2 as urllib_error
    PYTHON_VERSION = 2

from .config import load_config

def create_ssl_context():
    """Create SSL context with Windows compatibility"""
    try:
        import ssl
        if hasattr(ssl, 'create_default_context'):
            # Python 3 approach
            context = ssl.create_default_context()
            return context
        else:
            # Python 2 / IronPython - no SSL context
            return None
    except ImportError:
        # No SSL module available
        return None

def make_http_request(url, data, headers, method="POST"):
    """Make HTTP request with Windows/IronPython compatibility"""
    
    # Create request object
    if PYTHON_VERSION == 3:
        req = urllib_request.Request(url=url, data=data, headers=headers)
        req.get_method = lambda: method
    else:
        # Python 2 / IronPython
        req = urllib_request.Request(url, data, headers)
        req.get_method = lambda: method
    
    # Try to make request with SSL context
    try:
        context = create_ssl_context()
        if context:
            response = urllib_request.urlopen(req, context=context)
        else:
            # Fallback for IronPython/older Python
            response = urllib_request.urlopen(req)
            
        return response
        
    except Exception as e:
        # If SSL fails, provide helpful error message
        if "SSL" in str(e) or "certificate" in str(e).lower():
            raise Exception("SSL/Certificate error. This may be due to Windows certificate store issues. "
                          "Try running Revit as Administrator or contact your IT department. Original error: {}".format(str(e)))
        else:
            raise e

def get_claude_response(query, context_data):
    """Get response from Claude API with enhanced context"""
    config = load_config()
    api_key = config.get('claude_api_key', '')
    
    if not api_key:
        return "ERROR: Claude API key not set. Please update the configuration file."
    
    # Prepare enhanced context
    docs_context = ""
    examples_context = ""
    patterns_context = ""
    
    if isinstance(context_data, dict) and 'documentation' in context_data:
        # New enhanced context format
        for doc in context_data['documentation']:
            docs_context += "\n--- API DOCUMENTATION: {} ---\n".format(os.path.basename(doc['path']))
            docs_context += doc['content']
            docs_context += "\n\n"
        
        # Add examples context
        for example in context_data.get('examples', []):
            examples_context += "\n--- WORKING EXAMPLE: {} ---\n".format(example['path'])
            examples_context += "Description: {}\n".format(example['metadata']['description'])
            examples_context += "Use Cases: {}\n".format(", ".join(example['metadata']['use_cases']))
            examples_context += "Code:\n{}".format(example['content'])
            examples_context += "\n\n"
        
        # Add patterns context
        patterns = context_data.get('patterns', {})
        if patterns:
            patterns_context += "\n--- COMMON PATTERNS ---\n"
            patterns_context += "UI Components: {}\n".format(", ".join(patterns.get('ui_components', [])))
            patterns_context += "Revit Classes: {}\n".format(", ".join(patterns.get('revit_classes', [])))
            patterns_context += "\n"
    else:
        # Legacy format support
        for doc in context_data:
            docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
            docs_context += doc['content']
            docs_context += "\n\n"
    
    # Create enhanced prompt
    revit_var = "__revit__"  # Store in variable to avoid markdown issues
    prompt = """You are an expert Revit API assistant with access to working code examples and comprehensive documentation. 
You help users with Revit API questions and generate high-quality Python code for Revit.

You have access to:
1. API Documentation - Official Revit API class and method documentation
2. Working Examples - Proven, tested code examples that demonstrate best practices
3. Common Patterns - UI patterns, transaction handling, and coding conventions

When generating code:
- Use the working examples as templates when relevant
- Follow the established patterns for UI, transactions, and error handling
- Provide complete, executable code that follows best practices
- Include proper imports, error handling, and helpful comments

CONTEXT PROVIDED:

REVIT API DOCUMENTATION:
{}

WORKING EXAMPLES:
{}

COMMON PATTERNS:
{}

USER QUERY:
{}

INSTRUCTIONS:
1. If there are relevant working examples, USE THEM as templates
2. Adapt the examples to match the user's specific requirements
3. Maintain the same coding style and patterns from the examples
4. If no examples match, use the API documentation and common patterns
5. Always provide complete, working code that can be executed in Revit

IMPORTANT FORMATTING RULES:
- Wrap all code in triple backticks with python specified
- Use EXACTLY this format for Revit document access: {}
- Do NOT use asterisks (*) around the word revit
- Use double underscores: {}

Standard code template (when not using examples):
```python
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# Get current document
doc = {}.ActiveUIDocument.Document
uidoc = {}.ActiveUIDocument

# Your code here
```
""".format(docs_context, examples_context, patterns_context, query, revit_var, revit_var, revit_var, revit_var)
    
    # Create request data
    request_data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    # Set up the request
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    # Send request to Claude API
    try:
        # Convert request data to JSON
        if PYTHON_VERSION == 3:
            data = json.dumps(request_data).encode('utf-8')
        else:
            # Python 2 / IronPython
            data = json.dumps(request_data)
            if isinstance(data, unicode):
                data = data.encode('utf-8')
        
        # Make HTTP request with compatibility layer
        response = make_http_request(
            url="https://api.anthropic.com/v1/messages",
            data=data,
            headers=headers,
            method='POST'
        )
        
        # Read and parse response
        response_body = response.read()
        if PYTHON_VERSION == 3:
            response_body = response_body.decode('utf-8')
        
        response_json = json.loads(response_body)
        
        # Extract response text and fix common markdown issues
        response_text = response_json['content'][0]['text']
        
        # Fix markdown formatting issues
        response_text = response_text.replace('**revit**', '__revit__')
        response_text = response_text.replace('*revit*', '__revit__')
        
        return response_text
            
    except Exception as e:
        error_message = "Failed to get response from Claude: {}".format(str(e))
        if "401" in str(e):
            error_message += "\nPlease check your API key in the config.json file."
        elif "SSL" in str(e) or "certificate" in str(e).lower():
            error_message += "\nSSL/Certificate error. Try running Revit as Administrator or check your network connection."
        elif "HTTP Error 403" in str(e):
            error_message += "\nAccess forbidden. Check your API key permissions."
        return "ERROR: {}".format(error_message)

def get_gemini_response(query, context_data):
    """Get response from Gemini API with enhanced context"""
    config = load_config()
    api_key = config.get('gemini_api_key', '')
    
    if not api_key:
        return "ERROR: Gemini API key not set. Please update the configuration file."
    
    # Prepare context (same logic as Claude)
    docs_context = ""
    examples_context = ""
    patterns_context = ""
    
    if isinstance(context_data, dict) and 'documentation' in context_data:
        # New enhanced context format
        for doc in context_data['documentation']:
            docs_context += "\n--- API DOCUMENTATION: {} ---\n".format(os.path.basename(doc['path']))
            docs_context += doc['content']
            docs_context += "\n\n"
        
        # Add examples context
        for example in context_data.get('examples', []):
            examples_context += "\n--- WORKING EXAMPLE: {} ---\n".format(example['path'])
            examples_context += "Description: {}\n".format(example['metadata']['description'])
            examples_context += "Use Cases: {}\n".format(", ".join(example['metadata']['use_cases']))
            examples_context += "Code:\n{}".format(example['content'])
            examples_context += "\n\n"
        
        # Add patterns context
        patterns = context_data.get('patterns', {})
        if patterns:
            patterns_context += "\n--- COMMON PATTERNS ---\n"
            patterns_context += "UI Components: {}\n".format(", ".join(patterns.get('ui_components', [])))
            patterns_context += "Revit Classes: {}\n".format(", ".join(patterns.get('revit_classes', [])))
            patterns_context += "\n"
    else:
        # Legacy format support
        for doc in context_data:
            docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
            docs_context += doc['content']
            docs_context += "\n\n"
    
    # Create enhanced prompt (same as Claude)
    revit_var = "__revit__"
    prompt = """You are an expert Revit API assistant with access to working code examples and comprehensive documentation. 
You help users with Revit API questions and generate high-quality Python code for Revit.

You have access to:
1. API Documentation - Official Revit API class and method documentation
2. Working Examples - Proven, tested code examples that demonstrate best practices
3. Common Patterns - UI patterns, transaction handling, and coding conventions

When generating code:
- Use the working examples as templates when relevant
- Follow the established patterns for UI, transactions, and error handling
- Provide complete, executable code that follows best practices
- Include proper imports, error handling, and helpful comments

CONTEXT PROVIDED:

REVIT API DOCUMENTATION:
{}

WORKING EXAMPLES:
{}

COMMON PATTERNS:
{}

USER QUERY:
{}

INSTRUCTIONS:
1. If there are relevant working examples, USE THEM as templates
2. Adapt the examples to match the user's specific requirements
3. Maintain the same coding style and patterns from the examples
4. If no examples match, use the API documentation and common patterns
5. Always provide complete, working code that can be executed in Revit

IMPORTANT FORMATTING RULES:
- Wrap all code in triple backticks with python specified
- Use EXACTLY this format for Revit document access: {}
- Do NOT use asterisks (*) around the word revit
- Use double underscores: {}

Standard code template (when not using examples):
```python
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# Get current document
doc = {}.ActiveUIDocument.Document
uidoc = {}.ActiveUIDocument

# Your code here
```
""".format(docs_context, examples_context, patterns_context, query, revit_var, revit_var, revit_var, revit_var)
    
    # Create request data
    request_data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 4000,
        }
    }
    
    # Set up the request
    headers = {
        "Content-Type": "application/json"
    }
    
    # Send request to Gemini API
    try:
        # Convert request data to JSON
        if PYTHON_VERSION == 3:
            data = json.dumps(request_data).encode('utf-8')
        else:
            # Python 2 / IronPython
            data = json.dumps(request_data)
            if isinstance(data, unicode):
                data = data.encode('utf-8')
        
        # Create request URL with API key
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={}".format(api_key)
        
        # Make HTTP request with compatibility layer
        response = make_http_request(
            url=url,
            data=data,
            headers=headers,
            method='POST'
        )
        
        # Read and parse response
        response_body = response.read()
        if PYTHON_VERSION == 3:
            response_body = response_body.decode('utf-8')
        
        response_json = json.loads(response_body)
        
        # Extract response text and fix common markdown issues
        response_text = response_json['candidates'][0]['content']['parts'][0]['text']
        
        # Fix markdown formatting issues
        response_text = response_text.replace('**revit**', '__revit__')
        response_text = response_text.replace('*revit*', '__revit__')
        
        return response_text
            
    except Exception as e:
        error_message = "Failed to get response from Gemini: {}".format(str(e))
        if "401" in str(e) or "403" in str(e):
            error_message += "\nPlease check your API key in the config.json file."
        elif "SSL" in str(e) or "certificate" in str(e).lower():
            error_message += "\nSSL/Certificate error. Try running Revit as Administrator or check your network connection."
        return "ERROR: {}".format(error_message)

def get_ai_response(query, context_data, model="claude"):
    """Get response from selected AI model with enhanced context"""
    if model.lower() == "claude":
        return get_claude_response(query, context_data)
    else:
        return get_gemini_response(query, context_data)
