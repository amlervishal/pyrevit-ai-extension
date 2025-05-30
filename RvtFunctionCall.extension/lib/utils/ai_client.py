# -*- coding: utf-8 -*-
"""
AI client utilities for Revit Function Call - FIXED TO USE YOUR REVIT_API_DOCS
Now reads from your actual documentation files - NO FALLBACKS!
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
    """Load syntax reference from your actual revit_api_docs files - NO FALLBACKS"""
    try:
        current_dir = os.path.dirname(__file__)
        lib_dir = os.path.dirname(current_dir)
        docs_dir = os.path.join(lib_dir, 'revit_api_docs')
        
        if not os.path.exists(docs_dir):
            raise Exception("revit_api_docs directory not found at: {}".format(docs_dir))
        
        # Read core files first
        syntax_content = "\n=== REVIT API DOCUMENTATION REFERENCE ===\n"
        
        # 1. Quick Reference (most important patterns)
        quick_ref_path = os.path.join(docs_dir, 'quick_reference.py')
        if os.path.exists(quick_ref_path):
            syntax_content += "\n--- QUICK REFERENCE PATTERNS ---\n"
            syntax_content += read_python_file_content(quick_ref_path, extract_key_patterns=True)
        
        # 2. Core Document Operations
        doc_path = os.path.join(docs_dir, 'core', 'document.py')
        if os.path.exists(doc_path):
            syntax_content += "\n--- DOCUMENT OPERATIONS ---\n"
            syntax_content += read_python_file_content(doc_path, extract_key_patterns=True)
        
        # 3. Transaction Patterns (critical for modifications)
        trans_path = os.path.join(docs_dir, 'transactions', 'basic_transactions.py')
        if os.path.exists(trans_path):
            syntax_content += "\n--- TRANSACTION PATTERNS ---\n"
            syntax_content += read_python_file_content(trans_path, extract_key_patterns=True)
        
        # 4. Element Creation Patterns
        creation_path = os.path.join(docs_dir, 'elements', 'creation.py')
        if os.path.exists(creation_path):
            syntax_content += "\n--- ELEMENT CREATION ---\n"
            syntax_content += read_python_file_content(creation_path, extract_key_patterns=True)
        
        # 5. Selection and Filtering
        selection_path = os.path.join(docs_dir, 'selection', 'selection.py')
        if os.path.exists(selection_path):
            syntax_content += "\n--- SELECTION & FILTERING ---\n"
            syntax_content += read_python_file_content(selection_path, extract_key_patterns=True)
        
        # 6. Built-in Elements and Parameters
        builtin_path = os.path.join(docs_dir, 'builtin_elements.py')
        if os.path.exists(builtin_path):
            syntax_content += "\n--- BUILTIN ELEMENTS & PARAMETERS ---\n"
            syntax_content += read_python_file_content(builtin_path, extract_key_patterns=True)
        
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
"""
        
        return syntax_content
        
    except Exception as e:
        # If anything fails, raise the error - no fallbacks!
        raise Exception("Failed to load revit_api_docs: {}. Please check that your documentation files exist and are readable.".format(str(e)))

def read_python_file_content(file_path, extract_key_patterns=False):
    """Read and extract key patterns from Python documentation files"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if extract_key_patterns:
            # Extract key patterns from the Python documentation
            extracted = ""
            
            # Look for dictionary definitions with patterns
            import re
            
            # Extract dictionary contents (like QUICK_REFERENCE, PATTERNS, etc.)
            dict_pattern = r'(\w+)\s*=\s*{([^}]+(?:{[^}]*}[^}]*)*)}'  
            matches = re.findall(dict_pattern, content, re.MULTILINE | re.DOTALL)
            
            for dict_name, dict_content in matches:
                if any(keyword in dict_name.upper() for keyword in ['REFERENCE', 'PATTERN', 'EXAMPLE', 'USAGE', 'QUICK']):
                    extracted += "\n{} patterns:\n".format(dict_name)
                    # Clean up the dictionary content for readability
                    lines = dict_content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#') and ':' in line:
                            extracted += "  {}\n".format(line.strip(' "\''))
            
            # Also extract usage examples if present
            if 'USAGE_EXAMPLES' in content:
                usage_start = content.find('USAGE_EXAMPLES = """')
                if usage_start != -1:
                    usage_end = content.find('"""', usage_start + 20)
                    if usage_end != -1:
                        usage_content = content[usage_start + 20:usage_end]
                        extracted += "\nUSAGE EXAMPLES:\n{}".format(usage_content)
            
            return extracted if extracted else content[:1000]  # Fallback to first 1000 chars
        
        return content
        
    except Exception as e:
        return "Error reading {}: {}".format(file_path, str(e))

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
    """Get response from Claude API using YOUR revit_api_docs - NO FALLBACKS"""
    config = load_config()
    api_key = config.get('claude_api_key', '')
    
    if not api_key:
        return "ERROR: Claude API key not set. Please update the configuration file."
    
    # Load syntax reference from YOUR documentation files
    try:
        syntax_reference = load_syntax_reference()
    except Exception as e:
        return "ERROR: Could not load revit_api_docs: {}".format(str(e))
    
    # Prepare enhanced context from your examples and docs
    docs_context = ""
    examples_context = ""
    patterns_context = ""
    
    if isinstance(context_data, dict) and 'documentation' in context_data:
        # Enhanced context format
        for doc in context_data['documentation']:
            docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
            docs_context += doc['content']
            docs_context += "\n\n"
        
        # Add examples from your library
        for example in context_data.get('examples', []):
            examples_context += "\n--- WORKING EXAMPLE: {} ---\n".format(example['path'])
            examples_context += "Description: {}\n".format(example['metadata']['description'])
            examples_context += "Use Cases: {}\n".format(", ".join(example['metadata']['use_cases']))
            examples_context += "Code:\n{}".format(example['content'])
            examples_context += "\n\n"
        
        # Add patterns from your docs
        patterns = context_data.get('patterns', {})
        if patterns:
            patterns_context += "\n--- COMMON PATTERNS FROM YOUR DOCS ---\n"
            patterns_context += "UI Components: {}\n".format(", ".join(patterns.get('ui_components', [])))
            patterns_context += "Revit Classes: {}\n".format(", ".join(patterns.get('revit_classes', [])))
            patterns_context += "\n"
    else:
        # Legacy format support
        for doc in context_data:
            docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
            docs_context += doc['content']
            docs_context += "\n\n"
    
    # Create enhanced prompt using YOUR documentation
    revit_var = "__revit__"
    prompt = """You are an expert Revit API assistant with access to a comprehensive, curated documentation library.

🔴 CRITICAL: Generate ONLY IronPython 2.7 compatible code for Revit's environment.

🔹 MANDATORY SYNTAX RULES:
- Use .format() for strings: "Value: {}".format(value) ✅ NOT f"Value: {value}" ❌
- Use __revit__ (double underscores) for Revit application access
- Always import: clr, clr.AddReference('RevitAPI'), clr.AddReference('RevitAPIUI')  
- Wrap ALL model modifications in Transaction objects
- Import System.Collections.Generic.List for collections

🔹 PRIMARY REFERENCE - YOUR REVIT API DOCUMENTATION:
{}

🔹 ADDITIONAL CONTEXT FROM YOUR LIBRARY:

DOCUMENTATION DETAILS:
{}

WORKING EXAMPLES FROM YOUR CODE:
{}

PATTERNS FROM YOUR DOCS:
{}

🔹 USER REQUEST:
{}

🔹 GENERATION REQUIREMENTS:
1. ONLY use patterns and syntax from the documentation above
2. Generate complete, working IronPython 2.7 code
3. Include proper imports, document access, and transactions
4. Follow the exact syntax patterns shown in your documentation
5. Use real Revit API classes and methods from your references
6. NO FALLBACKS - only use what's documented in your files

🔹 REQUIRED CODE STRUCTURE:
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

# Use Transaction for modifications
transaction = Transaction(doc, "Description")
transaction.Start()
try:
    # Your code here using patterns from documentation
    pass
    transaction.Commit()
except Exception as e:
    transaction.RollBack()
    TaskDialog.Show("Error", str(e))
```

Generate production-ready code using ONLY the documented patterns above.""".format(
        syntax_reference, docs_context, examples_context, patterns_context, query, revit_var, revit_var)
    
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
    """Get response from Gemini API using YOUR revit_api_docs"""
    config = load_config()
    api_key = config.get('gemini_api_key', '')
    
    if not api_key:
        return "ERROR: Gemini API key not set. Please update the configuration file."
    
    # Load syntax reference from YOUR documentation files
    try:
        syntax_reference = load_syntax_reference()
    except Exception as e:
        return "ERROR: Could not load revit_api_docs: {}".format(str(e))
    
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
    
    # Create enhanced prompt using YOUR documentation (same structure as Claude)
    revit_var = "__revit__"
    prompt = """You are an expert Revit API assistant with access to a comprehensive, curated documentation library.

🔴 CRITICAL: Generate ONLY IronPython 2.7 compatible code for Revit's environment.

🔹 MANDATORY SYNTAX RULES:
- Use .format() for strings: "Value: {}".format(value) ✅ NOT f"Value: {value}" ❌
- Use __revit__ (double underscores) for Revit application access
- Always import: clr, clr.AddReference('RevitAPI'), clr.AddReference('RevitAPIUI')  
- Wrap ALL model modifications in Transaction objects
- Import System.Collections.Generic.List for collections

🔹 PRIMARY REFERENCE - YOUR REVIT API DOCUMENTATION:
{}

🔹 ADDITIONAL CONTEXT FROM YOUR LIBRARY:

DOCUMENTATION DETAILS:
{}

WORKING EXAMPLES FROM YOUR CODE:
{}

PATTERNS FROM YOUR DOCS:
{}

🔹 USER REQUEST:
{}

🔹 GENERATION REQUIREMENTS:
1. ONLY use patterns and syntax from the documentation above
2. Generate complete, working IronPython 2.7 code
3. Include proper imports, document access, and transactions
4. Follow the exact syntax patterns shown in your documentation
5. Use real Revit API classes and methods from your references
6. NO FALLBACKS - only use what's documented in your files

🔹 REQUIRED CODE STRUCTURE:
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

# Use Transaction for modifications
transaction = Transaction(doc, "Description")
transaction.Start()
try:
    # Your code here using patterns from documentation
    pass
    transaction.Commit()
except Exception as e:
    transaction.RollBack()
    TaskDialog.Show("Error", str(e))
```

Generate production-ready code using ONLY the documented patterns above.""".format(
        syntax_reference, docs_context, examples_context, patterns_context, query, revit_var, revit_var)
    
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
    """Get response from selected AI model using YOUR documentation"""
    if model.lower() == "claude":
        return get_claude_response(query, context_data)
    else:
        return get_gemini_response(query, context_data)
