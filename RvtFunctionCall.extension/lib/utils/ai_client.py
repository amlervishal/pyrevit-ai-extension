# -*- coding: utf-8 -*-
"""
AI client utilities for Revit Function Call - FIXED FOR REGEX ISSUES
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
    """Load syntax reference from your actual revit_api_docs files - SIMPLIFIED VERSION"""
    try:
        current_dir = os.path.dirname(__file__)
        lib_dir = os.path.dirname(current_dir)
        docs_dir = os.path.join(lib_dir, 'revit_api_docs')
        
        if not os.path.exists(docs_dir):
            raise Exception("revit_api_docs directory not found at: {}".format(docs_dir))
        
        # Start with a basic reference
        syntax_content = "\n=== REVIT API DOCUMENTATION REFERENCE ===\n"
        
        # Read files with simple content extraction (no complex regex)
        files_to_read = [
            ('quick_reference.py', 'QUICK REFERENCE PATTERNS'),
            ('core/document.py', 'DOCUMENT OPERATIONS'),
            ('transactions/basic_transactions.py', 'TRANSACTION PATTERNS'),
            ('builtin_elements.py', 'BUILTIN ELEMENTS & PARAMETERS')
        ]
        
        for file_path, section_name in files_to_read:
            full_path = os.path.join(docs_dir, file_path)
            if os.path.exists(full_path):
                syntax_content += "\n--- {} ---\n".format(section_name)
                syntax_content += read_python_file_simple(full_path)
        
        # Add critical IronPython compatibility notes
        syntax_content += """\n--- IRONPYTHON 2.7 COMPATIBILITY REQUIREMENTS ---
CRITICAL: Use .format() instead of f-strings:
  ✅ "Hello {}".format(name)
  ❌ f"Hello {name}" 
  
CRITICAL: Use __revit__ for application access:
  doc = __revit__.ActiveUIDocument.Document
  uidoc = __revit__.ActiveUIDocument
  
CRITICAL: Always wrap modifications in transactions:
  transaction = Transaction(doc, "Description")
  transaction.Start()
  # modifications here
  transaction.Commit()

BASIC SETUP TEMPLATE:
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
"""
        
        return syntax_content
        
    except Exception as e:
        # Return a minimal reference if anything fails
        return """\n=== BASIC REVIT API REFERENCE ===
Failed to load full documentation: {}

BASIC SETUP:
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
doc = __revit__.ActiveUIDocument.Document

TRANSACTION PATTERN:
transaction = Transaction(doc, "Description")
transaction.Start()
# your code here
transaction.Commit()

STRING FORMATTING (IronPython):
"Hello {}".format(name)  # Use this
""".format(str(e))

def read_python_file_simple(file_path):
    """Simple file reader without complex regex patterns"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract just a reasonable sample - first 1500 characters
        if len(content) > 1500:
            content = content[:1500] + "\n... (content truncated for brevity)"
        
        return content
        
    except Exception as e:
        return "Error reading {}: {}".format(file_path, str(e))

def create_ssl_context():
    """Create SSL context with Windows compatibility"""
    try:
        import ssl
        if hasattr(ssl, 'create_default_context'):
            context = ssl.create_default_context()
            return context
        else:
            return None
    except ImportError:
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
    """Get response from Claude API - SIMPLIFIED VERSION"""
    config = load_config()
    api_key = config.get('claude_api_key', '')
    
    if not api_key:
        return "ERROR: Claude API key not set. Please update the configuration file."
    
    # Load syntax reference with error handling
    try:
        syntax_reference = load_syntax_reference()
    except Exception as e:
        syntax_reference = "Basic patterns available. Documentation loading error: {}".format(str(e))
    
    # Simplified context handling
    docs_context = ""
    examples_context = ""
    
    try:
        if isinstance(context_data, dict) and 'documentation' in context_data:
            for doc in context_data['documentation'][:3]:  # Limit to 3 docs
                docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
                # Limit doc content to prevent overwhelming the prompt
                content = doc['content']
                if len(content) > 2000:
                    content = content[:2000] + "...(truncated)"
                docs_context += content + "\n"
        elif isinstance(context_data, list):
            for doc in context_data[:3]:  # Limit to 3 docs
                docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
                content = doc['content']
                if len(content) > 2000:
                    content = content[:2000] + "...(truncated)"
                docs_context += content + "\n"
    except Exception as e:
        docs_context = "Context loading error: {}".format(str(e))
    
    # Create simplified prompt
    prompt = """You are a Revit API expert. Generate working IronPython 2.7 code for Revit.

CRITICAL RULES:
- Use .format() for strings: "Hello {}".format(name) ✅ NOT f-strings ❌
- Use __revit__ for app access: doc = __revit__.ActiveUIDocument.Document
- Always use Transaction for modifications
- Import: clr, clr.AddReference('RevitAPI'), clr.AddReference('RevitAPIUI')

SYNTAX REFERENCE:
{}

DOCUMENTATION CONTEXT:
{}

USER REQUEST: {}

Generate complete working code following these patterns exactly.""".format(
        syntax_reference[:3000] if len(syntax_reference) > 3000 else syntax_reference,
        docs_context[:2000] if len(docs_context) > 2000 else docs_context, 
        query
    )
    
    # Create request data
    request_data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 3000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    # Send request to Claude API
    try:
        if PYTHON_VERSION == 3:
            data = json.dumps(request_data).encode('utf-8')
        else:
            data = json.dumps(request_data)
            if isinstance(data, unicode):
                data = data.encode('utf-8')
        
        response = make_http_request(
            url="https://api.anthropic.com/v1/messages",
            data=data,
            headers=headers,
            method='POST'
        )
        
        response_body = response.read()
        if PYTHON_VERSION == 3:
            response_body = response_body.decode('utf-8')
        
        response_json = json.loads(response_body)
        response_text = response_json['content'][0]['text']
        
        # Fix common markdown issues
        response_text = response_text.replace('**revit**', '__revit__')
        response_text = response_text.replace('*revit*', '__revit__')
        
        return response_text
            
    except Exception as e:
        error_message = "Failed to get response from Claude: {}".format(str(e))
        if "401" in str(e):
            error_message += "\nCheck your Claude API key in config.json"
        elif "SSL" in str(e):
            error_message += "\nSSL error - try running Revit as Administrator"
        return "ERROR: {}".format(error_message)

def get_gemini_response(query, context_data):
    """Get response from Gemini API - SIMPLIFIED VERSION"""
    config = load_config()
    api_key = config.get('gemini_api_key', '')
    
    if not api_key:
        return "ERROR: Gemini API key not set. Please update the configuration file."
    
    # Use same simplified approach as Claude
    try:
        syntax_reference = load_syntax_reference()
    except Exception as e:
        syntax_reference = "Basic patterns available. Documentation loading error: {}".format(str(e))
    
    # Simplified context (same as Claude)
    docs_context = ""
    try:
        if isinstance(context_data, dict) and 'documentation' in context_data:
            for doc in context_data['documentation'][:3]:
                docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
                content = doc['content']
                if len(content) > 2000:
                    content = content[:2000] + "...(truncated)"
                docs_context += content + "\n"
        elif isinstance(context_data, list):
            for doc in context_data[:3]:
                docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
                content = doc['content']
                if len(content) > 2000:
                    content = content[:2000] + "...(truncated)"
                docs_context += content + "\n"
    except Exception as e:
        docs_context = "Context loading error: {}".format(str(e))
    
    # Create simplified prompt (same structure as Claude)
    prompt = """You are a Revit API expert. Generate working IronPython 2.7 code for Revit.

CRITICAL RULES:
- Use .format() for strings: "Hello {}".format(name) ✅ NOT f-strings ❌
- Use __revit__ for app access: doc = __revit__.ActiveUIDocument.Document
- Always use Transaction for modifications
- Import: clr, clr.AddReference('RevitAPI'), clr.AddReference('RevitAPIUI')

SYNTAX REFERENCE:
{}

DOCUMENTATION CONTEXT:
{}

USER REQUEST: {}

Generate complete working code following these patterns exactly.""".format(
        syntax_reference[:3000] if len(syntax_reference) > 3000 else syntax_reference,
        docs_context[:2000] if len(docs_context) > 2000 else docs_context,
        query
    )
    
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
            "maxOutputTokens": 3000,
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        if PYTHON_VERSION == 3:
            data = json.dumps(request_data).encode('utf-8')
        else:
            data = json.dumps(request_data)
            if isinstance(data, unicode):
                data = data.encode('utf-8')
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={}".format(api_key)
        
        response = make_http_request(
            url=url,
            data=data,
            headers=headers,
            method='POST'
        )
        
        response_body = response.read()
        if PYTHON_VERSION == 3:
            response_body = response_body.decode('utf-8')
        
        response_json = json.loads(response_body)
        response_text = response_json['candidates'][0]['content']['parts'][0]['text']
        
        # Fix common markdown issues
        response_text = response_text.replace('**revit**', '__revit__')
        response_text = response_text.replace('*revit*', '__revit__')
        
        return response_text
            
    except Exception as e:
        error_message = "Failed to get response from Gemini: {}".format(str(e))
        if "401" in str(e) or "403" in str(e):
            error_message += "\nCheck your Gemini API key in config.json"
        elif "SSL" in str(e):
            error_message += "\nSSL error - try running Revit as Administrator"
        return "ERROR: {}".format(error_message)

def get_ai_response(query, context_data, model="claude"):
    """Get response from selected AI model"""
    if model.lower() == "claude":
        return get_claude_response(query, context_data)
    else:
        return get_gemini_response(query, context_data)
