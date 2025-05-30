# -*- coding: utf-8 -*-
"""
Documentation lookup utilities for Revit Function Call - SIMPLIFIED TO AVOID INDEX ERRORS
"""
import os

def get_docs_path():
    """Get the path to the documentation directory"""
    lib_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(lib_dir, 'revit_api_docs')

def read_doc_content(doc_path):
    """Read the content of a documentation file safely"""
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Limit content size to prevent issues
        if len(content) > 3000:
            return content[:3000] + "...(truncated for safety)"
        return content
    except Exception:
        return ""

def find_relevant_context(query):
    """Find relevant context - SIMPLIFIED VERSION WITHOUT ExampleManager"""
    try:
        docs_path = get_docs_path()
        
        # Get basic documentation files
        doc_files = [
            'quick_reference.py',
            'core/document.py', 
            'transactions/basic_transactions.py',
            'builtin_elements.py'
        ]
        
        docs_content = []
        
        for file_path in doc_files:
            full_path = os.path.join(docs_path, file_path)
            if os.path.exists(full_path):
                content = read_doc_content(full_path)
                if content:
                    docs_content.append({
                        'type': 'documentation',
                        'path': file_path,
                        'content': content,
                        'relevance': 'high'
                    })
        
        # Return simplified structure that won't cause index errors
        return {
            'documentation': docs_content,
            'examples': [],  # Empty to avoid ExampleManager issues
            'patterns': {},  # Empty to avoid complex processing
            'keywords': [],
            'query_type': 'general'
        }
        
    except Exception as e:
        # Return safe fallback structure
        return {
            'documentation': [{
                'type': 'documentation', 
                'path': 'fallback',
                'content': 'Basic Revit API patterns available',
                'relevance': 'medium'
            }],
            'examples': [],
            'patterns': {},
            'keywords': [],
            'query_type': 'general'
        }

def find_relevant_docs(query):
    """Legacy function for backward compatibility"""
    context = find_relevant_context(query)
    return context['documentation']
