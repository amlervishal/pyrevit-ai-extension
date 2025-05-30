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

def load_syntax_reference():
    """Load the comprehensive syntax reference JSON file"""
    try:
        # Get the path to the syntax reference file
        current_dir = os.path.dirname(__file__)
        lib_dir = os.path.dirname(current_dir)
        syntax_file = os.path.join(lib_dir, 'revit_api_docs', 'complete_syntax_reference.json')
        
        if os.path.exists(syntax_file):
            with open(syntax_file, 'r') as f:
                data = json.load(f)
            
            # Format the syntax reference for inclusion in prompts
            reference = data.get('revit_python_syntax_reference', {})
            
            # Create a formatted string of the most important syntax patterns
            formatted_ref = "\n=== CRITICAL SYNTAX PATTERNS ===\n"
            
            # Basic setup
            if 'basic_setup' in reference:
                formatted_ref += "\nBASIC SETUP:\n"
                for imp in reference['basic_setup'].get('imports', []):
                    formatted_ref += "  {0}\n".format(imp)
                for doc in reference['basic_setup'].get('document_access', []):
                    formatted_ref += "  {0}\n".format(doc)
            
            # Transaction patterns
            if 'transactions' in reference:
                formatted_ref += "\nTRANSACTION PATTERNS:\n"
                for pattern in reference['transactions'].get('basic_transaction', []):
                    formatted_ref += "  {0}\n".format(pattern)
            
            # Element collection
            if 'element_collection' in reference:
                formatted_ref += "\nELEMENT COLLECTION:\n"
                formatted_ref += "  {0}\n".format(reference['element_collection'].get('all_elements_by_class', ''))
                formatted_ref += "  {0}\n".format(reference['element_collection'].get('all_elements_by_category', ''))
            
            # Parameter access
            if 'parameters' in reference:
                formatted_ref += "\nPARAMETER ACCESS:\n"
                formatted_ref += "  Get: {0}\n".format(reference['parameters'].get('get_parameter_by_name', ''))
                formatted_ref += "  Set: {0}\n".format(reference['parameters'].get('set_parameter_by_name', ''))
            
            # String formatting
            if 'python_ironpython_compatibility' in reference:
                formatted_ref += "\nSTRING FORMATTING (IronPython 2.7):\n"
                for fmt in reference['python_ironpython_compatibility'].get('string_formatting', []):
                    formatted_ref += "  {0}\n".format(fmt)
            
            return formatted_ref
            
        else:
            return "\n=== SYNTAX REFERENCE FILE NOT FOUND ===\n"
            
    except Exception as e:
        return "\n=== ERROR LOADING SYNTAX REFERENCE: {0} ===\n".format(str(e))

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
    
    # Create enhanced prompt with comprehensive syntax reference
    revit_var = "__revit__"  # Store in variable to avoid markdown issues
    prompt = """You are an expert Revit API assistant with access to comprehensive syntax references, working code examples, and detailed documentation.

You MUST generate code that works in IronPython 2.7 (Revit's Python environment). Follow these critical rules:

🔹 SYNTAX REQUIREMENTS:
- Use .format() instead of f-strings: "Hello {}".format(name) ✅ NOT f"Hello {name}" ❌
- Use __revit__ (double underscores) for Revit application access
- Always import: clr, clr.AddReference('RevitAPI'), clr.AddReference('RevitAPIUI')
- Use proper Transaction handling for any model modifications
- Import System.Collections.Generic.List for element collections

🔹 COMPLETE SYNTAX REFERENCE:
{}

🔹 CONTEXT PROVIDED:

REVIT API DOCUMENTATION:
{}

WORKING EXAMPLES:
{}

COMMON PATTERNS:
{}

USER QUERY:
{}

🔹 GENERATION INSTRUCTIONS:
1. Always start with proper imports and document access
2. Use the syntax reference above for correct API calls
3. If relevant working examples exist, adapt them to the user's needs
4. Ensure IronPython 2.7 compatibility (no f-strings, proper print functions)
5. Include proper error handling and transactions
6. Generate complete, executable code

🔹 CODE TEMPLATE:
```python
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

# Get current document
doc = {}.ActiveUIDocument.Document
uidoc = {}.ActiveUIDocument

# Your code here with proper transactions if needed
```

Generate working, tested-quality code that follows these patterns exactly.""".format(syntax_reference, docs_context, examples_context, patterns_context, query, revit_var, revit_var)
    
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
    """Get response from Gemini API with enhanced context and comprehensive syntax reference"""
    config = load_config()
    api_key = config.get('gemini_api_key', '')
    
    if not api_key:
        return "ERROR: Gemini API key not set. Please update the configuration file."
    
    # Load comprehensive syntax reference
    syntax_reference = load_syntax_reference()
    
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
    
    # Create enhanced prompt (same as Claude but adapted for Gemini)
    revit_var = "__revit__"
    prompt = """You are an expert Revit API assistant with access to comprehensive syntax references, working code examples, and detailed documentation.

You MUST generate code that works in IronPython 2.7 (Revit's Python environment). Follow these critical rules:

🔹 SYNTAX REQUIREMENTS:
- Use .format() instead of f-strings: "Hello {}".format(name) ✅ NOT f"Hello {name}" ❌
- Use __revit__ (double underscores) for Revit application access
- Always import: clr, clr.AddReference('RevitAPI'), clr.AddReference('RevitAPIUI')
- Use proper Transaction handling for any model modifications
- Import System.Collections.Generic.List for element collections

🔹 COMPLETE SYNTAX REFERENCE:
{}

🔹 CONTEXT PROVIDED:

REVIT API DOCUMENTATION:
{}

WORKING EXAMPLES:
{}

COMMON PATTERNS:
{}

USER QUERY:
{}

🔹 GENERATION INSTRUCTIONS:
1. Always start with proper imports and document access
2. Use the syntax reference above for correct API calls
3. If relevant working examples exist, adapt them to the user's needs
4. Ensure IronPython 2.7 compatibility (no f-strings, proper print functions)
5. Include proper error handling and transactions
6. Generate complete, executable code

🔹 CODE TEMPLATE:
```python
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

# Get current document
doc = {}.ActiveUIDocument.Document
uidoc = {}.ActiveUIDocument

# Your code here with proper transactions if needed
```

Generate working, tested-quality code that follows these patterns exactly.""".format(syntax_reference, docs_context, examples_context, patterns_context, query, revit_var, revit_var)
    
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
