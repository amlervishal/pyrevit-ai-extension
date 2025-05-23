# -*- coding: utf-8 -*-
"""
AI client utilities for Revit Function Call - FIXED VERSION
"""
import sys
import os
import json

# For Python 2/3 compatibility in pyRevit
try:
    # Python 3
    import urllib.request as urllib_request
    import urllib.parse as urllib_parse
    import urllib.error as urllib_error
except ImportError:
    # Python 2
    import urllib2 as urllib_request
    import urllib as urllib_parse
    import urllib2 as urllib_error

from .config import load_config

def create_request_with_ssl_context(url, data, headers, method="POST"):
    """Create a request with proper SSL context for Windows"""
    import ssl
    
    # Create SSL context
    context = ssl.create_default_context()
    
    # Create request
    req = urllib_request.Request(url=url, data=data, headers=headers)
    req.get_method = lambda: method
    
    return req, context

def get_claude_response(query, docs):
    """Get response from Claude API"""
    config = load_config()
    api_key = config.get('claude_api_key', '')
    
    if not api_key:
        return "ERROR: Claude API key not set. Please update the configuration."
    
    # Prepare context from documentation
    docs_context = ""
    for doc in docs:
        docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
        docs_context += doc['content']
        docs_context += "\n\n"
    
    # Create prompt with proper escaping
    revit_var = "__revit__"  # Store in variable to avoid markdown issues
    prompt = """You are a Revit API assistant. You help users with Revit API questions and generate Python code for Revit.
Please answer the following question or request based on the Revit API documentation provided below.
If the query asks for a Python script, make sure to provide working code that can be run in Revit's Python environment.
Include necessary imports, error handling, and comments explaining the code.

REVIT API DOCUMENTATION:
{}

USER QUERY:
{}

IMPORTANT FORMATTING RULES:
- If you're generating code, wrap it in triple backticks with python specified
- Use EXACTLY this format for the Revit document access: {}
- Do NOT use asterisks (*) around the word revit
- Use double underscores before and after revit like this: {}

Standard code template to use:
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
""".format(docs_context, query, revit_var, revit_var, revit_var, revit_var)
    
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
        data = json.dumps(request_data).encode('utf-8')
        
        # Create request object
        req = urllib_request.Request(
            url="https://api.anthropic.com/v1/messages",
            data=data,
            headers=headers
        )
        req.get_method = lambda: 'POST'
        
        # Send request and get response
        response = urllib_request.urlopen(req)
        response_body = response.read().decode('utf-8')
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
            error_message += "\nPlease check your API key."
        elif "SSL" in str(e):
            error_message += "\nSSL/TLS connection issue. Check your internet connection."
        return "ERROR: {}".format(error_message)

def get_gemini_response(query, docs):
    """Get response from Gemini API"""
    config = load_config()
    api_key = config.get('gemini_api_key', '')
    
    if not api_key:
        return "ERROR: Gemini API key not set. Please update the configuration."
    
    # Prepare context from documentation
    docs_context = ""
    for doc in docs:
        docs_context += "\n--- {} ---\n".format(os.path.basename(doc['path']))
        docs_context += doc['content']
        docs_context += "\n\n"
    
    # Create prompt with proper escaping
    revit_var = "__revit__"
    prompt = """You are a Revit API assistant. You help users with Revit API questions and generate Python code for Revit.
Please answer the following question or request based on the Revit API documentation provided below.
If the query asks for a Python script, make sure to provide working code that can be run in Revit's Python environment.
Include necessary imports, error handling, and comments explaining the code.

REVIT API DOCUMENTATION:
{}

USER QUERY:
{}

IMPORTANT FORMATTING RULES:
- If you're generating code, wrap it in triple backticks with python specified
- Use EXACTLY this format for the Revit document access: {}
- Do NOT use asterisks (*) around the word revit
- Use double underscores before and after revit like this: {}

Standard code template to use:
```
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
""".format(docs_context, query, revit_var, revit_var, revit_var, revit_var)
    
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
        data = json.dumps(request_data).encode('utf-8')
        
        # Create request URL with API key
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={}".format(api_key)
        
        # Create request object
        req = urllib_request.Request(
            url=url,
            data=data,
            headers=headers
        )
        req.get_method = lambda: 'POST'
        
        # Send request and get response
        response = urllib_request.urlopen(req)
        response_body = response.read().decode('utf-8')
        response_json = json.loads(response_body)
        
        # Extract response text and fix common markdown issues
        response_text = response_json['candidates'][0]['content']['parts'][0]['text']
        
        # Fix markdown formatting issues
        response_text = response_text.replace('**revit**', '__revit__')
        response_text = response_text.replace('*revit*', '__revit__')
        
        return response_text
            
    except Exception as e:
        error_message = "Failed to get response from Gemini: {}".format(str(e))
        return "ERROR: {}".format(error_message)

def get_ai_response(query, docs, model="claude"):
    """Get response from selected AI model"""
    if model.lower() == "claude":
        return get_claude_response(query, docs)
    else:
        return get_gemini_response(query, docs)
