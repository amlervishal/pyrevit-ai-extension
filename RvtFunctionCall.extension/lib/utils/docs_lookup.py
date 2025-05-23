# -*- coding: utf-8 -*-
"""
Documentation lookup utilities for Revit Function Call
"""
import os
import re
from .config import load_config

def get_docs_path():
    """Get the path to the documentation directory"""
    lib_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(lib_dir, 'revit_api_docs')

def extract_keywords(query):
    """Extract potential API-related keywords from the query"""
    # This is a simple implementation that can be improved
    # Remove common words and punctuation
    common_words = ['a', 'an', 'the', 'in', 'on', 'at', 'for', 'with', 'to', 'and', 'or', 'how']
    
    # Make lowercase and remove punctuation
    clean_query = re.sub(r'[^\w\s]', ' ', query.lower())
    
    # Split into words and filter out common words
    words = clean_query.split()
    keywords = [word for word in words if word not in common_words and len(word) > 2]
    
    # Look for potential Revit API classes and methods
    revit_api_patterns = [
        r'Element\w*',
        r'Document\w*',
        r'Transaction\w*',
        r'Parameter\w*',
        r'View\w*',
        r'Family\w*',
        r'Instance\w*',
        r'Type\w*',
        r'Filter\w*',
        r'Collector\w*',
        r'Wall\w*',
        r'Floor\w*',
        r'Ceiling\w*',
        r'Door\w*',
        r'Window\w*',
        r'Room\w*',
        r'Level\w*',
        r'Grid\w*',
        r'Material\w*'
    ]
    
    for pattern in revit_api_patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        keywords.extend(matches)
    
    # Remove duplicates and return
    return list(set(keywords))

def find_docs_for_keyword(keyword):
    """Find documentation files that match the keyword"""
    docs_path = get_docs_path()
    matching_docs = []
    
    # Check if the docs path exists
    if not os.path.exists(docs_path):
        return matching_docs
    
    # Search for files that contain the keyword in their name
    for root, _, files in os.walk(docs_path):
        for file in files:
            if keyword.lower() in file.lower():
                matching_docs.append(os.path.join(root, file))
    
    return matching_docs

def read_doc_content(doc_path):
    """Read the content of a documentation file"""
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

def find_relevant_docs(query):
    """Find documentation relevant to the query"""
    keywords = extract_keywords(query)
    config = load_config()
    max_docs = config.get('max_docs', 5)
    
    all_matching_docs = []
    
    # Find docs for each keyword
    for keyword in keywords:
        matching_docs = find_docs_for_keyword(keyword)
        all_matching_docs.extend(matching_docs)
    
    # Remove duplicates
    unique_docs = list(set(all_matching_docs))
    
    # Limit to max_docs
    selected_docs = unique_docs[:max_docs]
    
    # Read content of selected docs
    docs_content = []
    for doc_path in selected_docs:
        content = read_doc_content(doc_path)
        if content:
            docs_content.append({
                'path': doc_path,
                'content': content
            })
    
    return docs_content
