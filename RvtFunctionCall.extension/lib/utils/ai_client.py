# -*- coding: utf-8 -*-
"""
AI client utilities for Revit Function Call - FIXED FOR INDEX ERRORS
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
    """Load syntax reference from your actual revit_api_docs files - SAFE VERSION"""
    try:
        current_dir = os.path.dirname(__file__)
        lib_dir = os.path.dirname(current_dir)
        docs_dir = os.path.join(lib_dir, 'revit_api_docs')
        
        if not os.path.exists(docs_dir):
            return get_fallback_reference("Documentation directory not found")
        
        # Start with a basic reference
        syntax_content = "\n=== REVIT API DOCUMENTATION REFERENCE ===\n"
        
        # Read files safely
        files_to_read = [
            ('quick_reference.py', 'QUICK REFERENCE'),
            ('core/document.py', 'DOCUMENT OPERATIONS'),
            ('transactions/basic_transactions.py', 'TRANSACTIONS'),
            ('builtin_elements.py', 'BUILTIN ELEMENTS')
        ]
        
        files_read = 0
        for file_path, section_name in files_to_read:
            full_path = os.path.join(docs_dir, file_path)
            if os.path.exists(full_path):
                try:
                    content = read_python_file_safe(full_path)
                    if content:
                        syntax_content += "\n--- {} ---\n".format(section_name)
                        syntax_content += content[:1000] + "\n"  # Limit content
                        files_read += 1
                except Exception as e:
                    syntax_content += "\n--- {} (Error) ---\n".format(section_name)
                    syntax_content += "Error reading file: {}\n".format(str(e))
        
        # Add essential patterns
        syntax_content += get_essential_patterns()
        
        if files_read > 0:
            return syntax_content
        else:
            return get_fallback_reference("No documentation files could be read")
        
    except Exception as e:
        return get_fallback_reference("Documentation loading failed: {}".format(str(e)))

def read_python_file_safe(file_path):
    """Safely read a Python file with error handling"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Return first 800 characters to keep it manageable
        if len(content) > 800:
            return content[:800] + "...(truncated for safety)"
        
        return content
        
    except Exception as e:
        return "Error reading file: {}".format(str(e))

def get_essential_patterns():
    """Get essential IronPython patterns"""
    return """\n--- ESSENTIAL IRONPYTHON PATTERNS ---
SETUP:
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
# your modifications here
transaction.Commit()

STRING FORMAT:
"Hello {}".format(name)  # Use this, NOT f-strings

SELECTION:
FilteredElementCollector(doc).OfClass(Wall).ToElements()
"""

def get_fallback_reference(error_msg):
    """Get minimal fallback reference when docs can't be loaded"""
    return """\n=== MINIMAL REVIT API REFERENCE ===
Error: {}

BASIC SETUP:
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

TRANSACTION PATTERN:
transaction = Transaction(doc, "Operation")
transaction.Start()
# your code here
transaction.Commit()

ELEMENT SELECTION:
elements = FilteredElementCollector(doc).OfClass(Wall).ToElements()

STRING FORMATTING:
"Value: {}".format(variable)  # IronPython 2.7 compatible
""".format(error_msg)

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

def safe_get_docs_context(context_data):
    """Safely extract documentation context with bounds checking"""
    docs_context = ""
    
    try:
        if context_data is None:
            return "No context data provided"
        
        if isinstance(context_data, dict):
            # Handle dict format
            if 'documentation' in context_data:
                docs_list = context_data['documentation']
                if isinstance(docs_list, list) and len(docs_list) > 0:
                    # Safe iteration with bounds checking
                    max_docs = min(len(docs_list), 3)  # Maximum 3 docs
                    for i in range(max_docs):
                        try:
                            doc = docs_list[i]
                            if isinstance(doc, dict) and 'path' in doc and 'content' in doc:
                                path_name = doc.get('path', 'unknown')
                                content = doc.get('content', '')
                                
                                # Safe basename extraction
                                try:
                                    basename = os.path.basename(path_name)
                                except:
                                    basename = str(path_name)
                                
                                docs_context += "\n--- {} ---\n".format(basename)
                                
                                # Limit content length
                                if len(content) > 1500:
                                    content = content[:1500] + "...(truncated)"
                                
                                docs_context += content + "\n"
                        except Exception as e:
                            docs_context += "\n--- Error processing doc {} ---\n".format(i)
                            docs_context += "Error: {}\n".format(str(e))
                else:
                    docs_context = "No documentation items found in context"
            else:
                docs_context = "No 'documentation' key in context data"
                
        elif isinstance(context_data, list):
            # Handle list format
            if len(context_data) > 0:
                max_docs = min(len(context_data), 3)  # Maximum 3 docs
                for i in range(max_docs):
                    try:
                        doc = context_data[i]
                        if isinstance(doc, dict) and 'path' in doc and 'content' in doc:
                            path_name = doc.get('path', 'unknown')
                            content = doc.get('content', '')
                            
                            # Safe basename extraction
                            try:
                                basename = os.path.basename(path_name)
                            except:
                                basename = str(path_name)
                            
                            docs_context += "\n--- {} ---\n".format(basename)
                            
                            # Limit content length
                            if len(content) > 1500:
                                content = content[:1500] + "...(truncated)"
                            
                            docs_context += content + "\n"
                    except Exception as e:
                        docs_context += "\n--- Error processing item {} ---\n".format(i)
                        docs_context += "Error: {}\n".format(str(e))
            else:
                docs_context = "Empty context list provided"
        else:
            docs_context = "Context data format not recognized: {}".format(type(context_data))
    
    except Exception as e:
        docs_context = "Error processing context: {}".format(str(e))
    
    return docs_context

def get_claude_response(query, context_data):
    """Get response from Claude API - SAFE VERSION WITH BOUNDS CHECKING"""
    config = load_config()
    api_key = config.get('claude_api_key', '')
    
    if not api_key:
        return "ERROR: Claude API key not set. Please update the configuration file."
    
    # Load syntax reference with error handling
    try:
        syntax_reference = load_syntax_reference()
    except Exception as e:
        syntax_reference = get_fallback_reference("Syntax loading failed: {}".format(str(e)))
    
    # Safely get documentation context
    docs_context = safe_get_docs_context(context_data)
    
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
        syntax_reference[:2500] if len(syntax_reference) > 2500 else syntax_reference,
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
        
        # Safe access to response content
        if 'content' in response_json and len(response_json['content']) > 0:
            if 'text' in response_json['content'][0]:
                response_text = response_json['content'][0]['text']
            else:
                return "ERROR: No text in response content"
        else:
            return "ERROR: No content in response"
        
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
    """Get response from Gemini API - SAFE VERSION WITH BOUNDS CHECKING"""
    config = load_config()
    api_key = config.get('gemini_api_key', '')
    
    if not api_key:
        return "ERROR: Gemini API key not set. Please update the configuration file."
    
    # Use same safe approach as Claude
    try:
        syntax_reference = load_syntax_reference()
    except Exception as e:
        syntax_reference = get_fallback_reference("Syntax loading failed: {}".format(str(e)))
    
    # Safely get documentation context (same as Claude)
    docs_context = safe_get_docs_context(context_data)
    
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
        syntax_reference[:2500] if len(syntax_reference) > 2500 else syntax_reference,
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
        
        # Safe access to response content
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            candidate = response_json['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                if 'text' in candidate['content']['parts'][0]:
                    response_text = candidate['content']['parts'][0]['text']
                else:
                    return "ERROR: No text in Gemini response"
            else:
                return "ERROR: Invalid Gemini response structure"
        else:
            return "ERROR: No candidates in Gemini response"
        
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
    """Get response from selected AI model - SAFE VERSION"""
    try:
        if model.lower() == "claude":
            return get_claude_response(query, context_data)
        else:
            return get_gemini_response(query, context_data)
    except Exception as e:
        return "ERROR: AI response function failed: {}".format(str(e))
