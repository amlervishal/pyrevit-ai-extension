# -*- coding: utf-8 -*-
"""
Documentation lookup utilities for Revit Function Call - Enhanced with Examples
"""
import os
import re
from .config import load_config
from .example_manager import ExampleManager

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

def find_relevant_context(query):
    """Find comprehensive context including docs and examples"""
    keywords = extract_keywords(query)
    config = load_config()
    max_docs = config.get('max_docs', 5)
    
    # Initialize example manager
    examples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples')
    example_manager = ExampleManager(examples_dir)
    
    # Add analysis-specific keywords for better matching
    analysis_keywords = ['area', 'room', 'space', 'analysis', 'calculate', 'quantity', 'measurement', 'statistics']
    if any(keyword.lower() in query.lower() for keyword in analysis_keywords):
        keywords.extend(['area', 'analysis', 'boundary', 'calculation'])
    
    # Find relevant examples
    relevant_examples = example_manager.find_relevant_examples(query, max_examples=3)
    
    # Find API documentation
    all_matching_docs = []
    for keyword in keywords:
        matching_docs = find_docs_for_keyword(keyword)
        all_matching_docs.extend(matching_docs)
    
    # Remove duplicates and limit
    unique_docs = list(set(all_matching_docs))
    selected_docs = unique_docs[:max_docs]
    
    # Read content of selected docs
    docs_content = []
    for doc_path in selected_docs:
        content = read_doc_content(doc_path)
        if content:
            docs_content.append({
                'type': 'documentation',
                'path': doc_path,
                'content': content
            })
    
    # Add example content
    examples_content = []
    for example_path, metadata, score in relevant_examples:
        content = example_manager.get_example_content(example_path)
        if content:
            examples_content.append({
                'type': 'example',
                'path': example_path,
                'content': content,
                'metadata': metadata,
                'relevance_score': score
            })
    
    # Get common patterns
    patterns = example_manager.get_example_patterns(query)
    
    return {
        'documentation': docs_content,
        'examples': examples_content,
        'patterns': patterns
    }

def find_relevant_docs(query):
    """Legacy function for backward compatibility"""
    context = find_relevant_context(query)
    return context['documentation']
