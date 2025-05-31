# -*- coding: utf-8 -*-
"""
AI client for Revit Function Call with enhanced .NET import rules
"""
import json
import sys

try:
    import urllib.request as urllib_request
    import urllib.parse as urllib_parse
except ImportError:
    import urllib2 as urllib_request
    import urllib as urllib_parse

from .config import load_config

# Standard Revit API boilerplate that works reliably
REVIT_BOILERPLATE = """import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument"""

# Critical .NET import rules to prevent common errors
NET_IMPORT_RULES = """
CRITICAL .NET IMPORT RULES FOR IRONPYTHON 2.7:
- NEVER use clr.AddReference('System.Collections.Generic')
- USE: from System.Collections.Generic import List
- Standard assemblies: RevitAPI, RevitAPIUI only
- Common .NET types: List, Dictionary are available via direct import
- Transaction pattern: with Transaction(doc, 'Name') as t: t.Start(); code; t.Commit()
- Selection: uidoc.Selection.SetElementIds(List[ElementId](ids))
"""

def get_claude_response(query, context_data):
    """Get response from Claude API with enhanced .NET rules"""
    config = load_config()
    api_key = config.get('claude_api_key', '')
    
    if not api_key:
        raise Exception("Claude API key not configured")
    
    documentation_context = ""
    if context_data and isinstance(context_data, dict) and 'documentation' in context_data:
        docs = context_data['documentation']
        if docs and len(docs) > 0:
            doc_sections = []
            for doc in docs[:3]:
                if 'content' in doc and 'source' in doc:
                    source = doc['source']
                    content = doc['content'][:2000]
                    doc_sections.append("=== {} ===\n{}".format(source.upper(), content))
            
            if doc_sections:
                documentation_context = "\n\n".join(doc_sections)
    
    prompt = """You are an expert Revit API assistant. Generate IronPython 2.7 compatible code for pyRevit.

{}

STANDARD BOILERPLATE (always include):
{}

REVIT API DOCUMENTATION:
{}

USER REQUEST: {}

Generate working Revit Python code following the rules above. Use the standard boilerplate and ensure proper .NET imports.""".format(
        NET_IMPORT_RULES,
        REVIT_BOILERPLATE,
        documentation_context if documentation_context else "No specific documentation loaded", 
        query
    )
    
    request_data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    data = json.dumps(request_data).encode('utf-8')
    req = urllib_request.Request("https://api.anthropic.com/v1/messages", data, headers)
    
    response = urllib_request.urlopen(req)
    response_data = json.loads(response.read().decode('utf-8'))
    
    return response_data['content'][0]['text']

def get_gemini_response(query, context_data):
    """Get response from Gemini API with enhanced .NET rules"""
    config = load_config()
    api_key = config.get('gemini_api_key', '')
    
    if not api_key:
        raise Exception("Gemini API key not configured")
    
    documentation_context = ""
    if context_data and isinstance(context_data, dict) and 'documentation' in context_data:
        docs = context_data['documentation']
        if docs and len(docs) > 0:
            doc_sections = []
            for doc in docs[:3]:
                if 'content' in doc and 'source' in doc:
                    source = doc['source']
                    content = doc['content'][:2000]
                    doc_sections.append("=== {} ===\n{}".format(source.upper(), content))
            
            if doc_sections:
                documentation_context = "\n\n".join(doc_sections)
    
    prompt = """You are an expert Revit API assistant. Generate IronPython 2.7 compatible code for pyRevit.

{}

STANDARD BOILERPLATE (always include):
{}

REVIT API DOCUMENTATION:
{}

USER REQUEST: {}

Generate working Revit Python code following the rules above. Use the standard boilerplate and ensure proper .NET imports.""".format(
        NET_IMPORT_RULES,
        REVIT_BOILERPLATE,
        documentation_context if documentation_context else "No specific documentation loaded",
        query
    )
    
    request_data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 3000}
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(request_data).encode('utf-8')
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={}".format(api_key)
    req = urllib_request.Request(url, data, headers)
    
    response = urllib_request.urlopen(req)
    response_data = json.loads(response.read().decode('utf-8'))
    
    return response_data['candidates'][0]['content']['parts'][0]['text']

def get_ai_response(query, context_data, model="claude"):
    """Get response from selected AI model with enhanced .NET rules"""
    if model.lower() == "claude":
        return get_claude_response(query, context_data)
    else:
        return get_gemini_response(query, context_data)
