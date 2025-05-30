# -*- coding: utf-8 -*-
"""
AI client utilities for Revit Function Call - ROOT CAUSE FIX
Simplified to remove complex dependencies and focus on core functionality
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
    """Load basic syntax reference from documentation files"""
    try:
        current_dir = os.path.dirname(__file__)
        lib_dir = os.path.dirname(current_dir)
        docs_dir = os.path.join(lib_dir, 'revit_api_docs')
        
        # Start with basic content
        content = "\n=== REVIT API PATTERNS ===\n"
        
        # Try to read quick_reference.py
        quick_ref_path = os.path.join(docs_dir, 'quick_reference.py')
        if os.path.exists(quick_ref_path):
            try:
                with open(quick_ref_path, 'r') as f:
                    ref_content = f.read()
                content += "\n--- QUICK REFERENCE ---\n" + ref_content[:2000] + "\n"
            except Exception:
                pass
        
        # Add essential patterns
        content += """\n--- ESSENTIAL PATTERNS ---
BASIC SETUP:
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

TRANSACTION:
transaction = Transaction(doc, "Description")
transaction.Start()
# your code here
transaction.Commit()

ELEMENT SELECTION:
elements = FilteredElementCollector(doc).OfClass(Wall).ToElements()
"""
        
        return content
        
    except Exception as e:
        # Return minimal patterns
        return """\n=== BASIC REVIT PATTERNS ===
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
doc = __revit__.ActiveUIDocument.Document

transaction = Transaction(doc, "Operation")
transaction.Start()
# your code here
transaction.Commit()
"""

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
    
    try:
        context = create_ssl_context()
        if context:
            response = urllib_request.urlopen(req, context=context)
        else:
            response = urllib_request.urlopen(req)
            
        return response
        
    except Exception as e:
        if "SSL" in str(e) or "certificate" in str(e).lower():
            raise Exception("SSL/Certificate error. Try running Revit as Administrator. Original error: {}".format(str(e)))
        else:
            raise e

def get_claude_response(query, context_data):
    """Get response from Claude API - SIMPLIFIED AND UNRESTRICTED"""
    config = load_config()
    api_key = config.get('claude_api_key', '')
    
    if not api_key:
        return "ERROR: Claude API key not set. Please update the configuration file."
    
    # Get basic syntax reference
    syntax_reference = load_syntax_reference()
    
    # Simple context extraction - handle any data structure safely
    context_text = ""
    try:
        if context_data:
            if isinstance(context_data, dict):
                if 'documentation' in context_data:
                    docs = context_data['documentation']
                    if isinstance(docs, list) and len(docs) > 0:
                        # Take first doc safely
                        doc = docs[0]
                        if isinstance(doc, dict) and 'content' in doc:
                            context_text = doc['content'][:1500]
            elif isinstance(context_data, list) and len(context_data) > 0:
                # Handle as list of docs
                doc = context_data[0]
                if isinstance(doc, dict) and 'content' in doc:
                    context_text = doc['content'][:1500]
    except Exception:
        context_text = "Context processing skipped due to data structure issues"
    
    # Create UNRESTRICTED prompt - let Claude use its full knowledge
    prompt = """You are an expert Revit API assistant. The user is working with Revit in a pyRevit/IronPython 2.7 environment.

Key technical requirements:
- Generate code for IronPython 2.7 (no f-strings, use .format())
- Use __revit__ to access the Revit application
- Import standard Revit references (clr.AddReference('RevitAPI'), etc.)
- Use transactions for model modifications

Reference patterns available:
{}

Additional context (if available):
{}

User request: {}

Please generate working Revit Python code. Use your full knowledge of the Revit API and best practices. Focus on creating functional, production-ready code.""".format(
        syntax_reference,
        context_text,
        query
    )
    
    # Create request data
    request_data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
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
        
        # Safe access to response content
        if 'content' in response_json and len(response_json['content']) > 0:
            if 'text' in response_json['content'][0]:
                response_text = response_json['content'][0]['text']
                
                # Fix common markdown issues
                response_text = response_text.replace('**revit**', '__revit__')
                response_text = response_text.replace('*revit*', '__revit__')
                
                return response_text
            else:
                return "ERROR: No text in Claude response"
        else:
            return "ERROR: Invalid Claude response structure"
            
    except Exception as e:
        error_message = "Failed to get response from Claude: {}".format(str(e))
        if "401" in str(e):
            error_message += "\nCheck your Claude API key in config.json"
        elif "SSL" in str(e):
            error_message += "\nSSL error - try running Revit as Administrator"
        return "ERROR: {}".format(error_message)

def get_gemini_response(query, context_data):
    """Get response from Gemini API - SIMPLIFIED AND UNRESTRICTED"""
    config = load_config()
    api_key = config.get('gemini_api_key', '')
    
    if not api_key:
        return "ERROR: Gemini API key not set. Please update the configuration file."
    
    # Get basic syntax reference
    syntax_reference = load_syntax_reference()
    
    # Simple context extraction (same as Claude)
    context_text = ""
    try:
        if context_data:
            if isinstance(context_data, dict):
                if 'documentation' in context_data:
                    docs = context_data['documentation']
                    if isinstance(docs, list) and len(docs) > 0:
                        doc = docs[0]
                        if isinstance(doc, dict) and 'content' in doc:
                            context_text = doc['content'][:1500]
            elif isinstance(context_data, list) and len(context_data) > 0:
                doc = context_data[0]
                if isinstance(doc, dict) and 'content' in doc:
                    context_text = doc['content'][:1500]
    except Exception:
        context_text = "Context processing skipped"
    
    # Create UNRESTRICTED prompt (same structure as Claude)
    prompt = """You are an expert Revit API assistant. The user is working with Revit in a pyRevit/IronPython 2.7 environment.

Key technical requirements:
- Generate code for IronPython 2.7 (no f-strings, use .format())
- Use __revit__ to access the Revit application
- Import standard Revit references (clr.AddReference('RevitAPI'), etc.)
- Use transactions for model modifications

Reference patterns available:
{}

Additional context (if available):
{}

User request: {}

Please generate working Revit Python code. Use your full knowledge of the Revit API and best practices. Focus on creating functional, production-ready code.""".format(
        syntax_reference,
        context_text,
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
            "maxOutputTokens": 4000,
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
        
        # Safe access to response content
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            candidate = response_json['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                if 'text' in candidate['content']['parts'][0]:
                    response_text = candidate['content']['parts'][0]['text']
                    
                    # Fix common markdown issues
                    response_text = response_text.replace('**revit**', '__revit__')
                    response_text = response_text.replace('*revit*', '__revit__')
                    
                    return response_text
                else:
                    return "ERROR: No text in Gemini response"
            else:
                return "ERROR: Invalid Gemini response structure"
        else:
            return "ERROR: No candidates in Gemini response"
            
    except Exception as e:
        error_message = "Failed to get response from Gemini: {}".format(str(e))
        if "401" in str(e) or "403" in str(e):
            error_message += "\nCheck your Gemini API key in config.json"
        elif "SSL" in str(e):
            error_message += "\nSSL error - try running Revit as Administrator"
        return "ERROR: {}".format(error_message)

def get_ai_response(query, context_data, model="claude"):
    """Get response from selected AI model - ROOT CAUSE FIXED"""
    try:
        if model.lower() == "claude":
            return get_claude_response(query, context_data)
        else:
            return get_gemini_response(query, context_data)
    except Exception as e:
        return "ERROR: AI response function failed: {}".format(str(e))
