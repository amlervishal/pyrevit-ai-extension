# -*- coding: utf-8 -*-
"""
Documentation lookup utilities for Revit Function Call - Enhanced with Comprehensive API Docs
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
    # Remove common words and punctuation
    common_words = ['a', 'an', 'the', 'in', 'on', 'at', 'for', 'with', 'to', 'and', 'or', 'how', 'do', 'get', 'set', 'create', 'make']
    
    # Make lowercase and remove punctuation
    clean_query = re.sub(r'[^\w\s]', ' ', query.lower())
    
    # Split into words and filter out common words
    words = clean_query.split()
    keywords = [word for word in words if word not in common_words and len(word) > 2]
    
    # Look for potential Revit API classes and methods
    revit_api_patterns = [
        r'Element\w*', r'Document\w*', r'Transaction\w*', r'Parameter\w*', r'View\w*',
        r'Family\w*', r'Instance\w*', r'Type\w*', r'Filter\w*', r'Collector\w*',
        r'Wall\w*', r'Floor\w*', r'Ceiling\w*', r'Door\w*', r'Window\w*',
        r'Room\w*', r'Level\w*', r'Grid\w*', r'Material\w*', r'Schedule\w*',
        r'Sheet\w*', r'Viewport\w*', r'Area\w*', r'Space\w*', r'Analysis\w*'
    ]
    
    for pattern in revit_api_patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        keywords.extend(matches)
    
    # Add workflow-specific keywords
    workflow_keywords = {
        'analysis': ['area', 'volume', 'calculate', 'measure', 'quantity', 'spatial', 'boundary'],
        'creation': ['create', 'build', 'place', 'insert', 'add', 'new'],
        'selection': ['select', 'pick', 'filter', 'find', 'collect'],
        'schedule': ['schedule', 'takeoff', 'list', 'report', 'table'],
        'sheet': ['sheet', 'drawing', 'plot', 'print', 'viewport'],
        'modification': ['move', 'copy', 'rotate', 'mirror', 'modify', 'change', 'update'],
        'transaction': ['transaction', 'commit', 'rollback', 'start']
    }
    
    for workflow, related_words in workflow_keywords.items():
        if any(word in query.lower() for word in related_words):
            keywords.append(workflow)
    
    # Remove duplicates and return
    return list(set(keywords))

def get_relevant_files_by_keywords(keywords):
    """Get relevant documentation files based on keywords"""
    docs_path = get_docs_path()
    if not os.path.exists(docs_path):
        return []
    
    # Priority mapping for different types of queries
    file_priority = {
        # Core operations
        'document': ['core/document.py', 'quick_reference.py'],
        'selection': ['selection/selection.py', 'quick_reference.py'],
        'transaction': ['transactions/basic_transactions.py', 'transactions/advanced_transactions.py'],
        'create': ['elements/creation.py', 'examples/complete_workflows.py'],
        'creation': ['elements/creation.py', 'examples/complete_workflows.py'],
        
        # Analysis and spatial
        'room': ['analysis/spatial_analysis.py', 'builtin_elements.py'],
        'area': ['analysis/spatial_analysis.py', 'builtin_elements.py'],
        'space': ['analysis/spatial_analysis.py', 'builtin_elements.py'],
        'analysis': ['analysis/spatial_analysis.py', 'builtin_elements.py'],
        'spatial': ['analysis/spatial_analysis.py'],
        'boundary': ['analysis/spatial_analysis.py'],
        'calculate': ['analysis/spatial_analysis.py', 'quick_reference.py'],
        'volume': ['analysis/spatial_analysis.py', 'builtin_elements.py'],
        
        # Documentation
        'schedule': ['documentation/schedules_sheets.py', 'builtin_elements.py'],
        'sheet': ['documentation/schedules_sheets.py', 'examples/complete_workflows.py'],
        'viewport': ['documentation/schedules_sheets.py'],
        'takeoff': ['documentation/schedules_sheets.py'],
        
        # Elements
        'wall': ['elements/creation.py', 'selection/selection.py', 'builtin_elements.py'],
        'floor': ['elements/creation.py', 'selection/selection.py', 'builtin_elements.py'],
        'door': ['elements/creation.py', 'selection/selection.py', 'builtin_elements.py'],
        'window': ['elements/creation.py', 'selection/selection.py', 'builtin_elements.py'],
        'family': ['elements/creation.py', 'selection/selection.py'],
        'level': ['elements/creation.py', 'builtin_elements.py'],
        'grid': ['elements/creation.py', 'builtin_elements.py'],
        
        # Modifications
        'move': ['elements/creation.py', 'quick_reference.py'],
        'copy': ['elements/creation.py', 'examples/complete_workflows.py'],
        'modify': ['elements/creation.py', 'quick_reference.py'],
        'parameter': ['builtin_elements.py', 'quick_reference.py'],
        
        # General
        'filter': ['selection/selection.py', 'quick_reference.py'],
        'collector': ['selection/selection.py', 'quick_reference.py']
    }
    
    # Get files based on keyword priority
    relevant_files = []
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in file_priority:
            relevant_files.extend(file_priority[keyword_lower])
    
    # Always include essential files for comprehensive coverage
    essential_files = ['quick_reference.py', 'index.py']
    relevant_files.extend(essential_files)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for file in relevant_files:
        if file not in seen:
            seen.add(file)
            unique_files.append(file)
    
    return unique_files[:8]  # Limit to 8 most relevant files

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
    
    # Get relevant files based on keywords
    relevant_files = get_relevant_files_by_keywords(keywords)
    docs_path = get_docs_path()
    
    # Read content of relevant documentation files
    docs_content = []
    for file_path in relevant_files[:max_docs]:
        full_path = os.path.join(docs_path, file_path)
        if os.path.exists(full_path):
            content = read_doc_content(full_path)
            if content:
                docs_content.append({
                    'type': 'documentation',
                    'path': file_path,
                    'content': content,
                    'relevance': 'high' if file_path in relevant_files[:3] else 'medium'
                })
    
    # Find relevant examples
    try:
        relevant_examples = example_manager.find_relevant_examples(query, max_examples=3)
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
    except Exception:
        # Fallback if example manager fails
        examples_content = []
    
    # Get common patterns
    try:
        patterns = example_manager.get_example_patterns(query)
    except Exception:
        patterns = {}
    
    return {
        'documentation': docs_content,
        'examples': examples_content,
        'patterns': patterns,
        'keywords': keywords,
        'query_type': classify_query_type(query, keywords)
    }

def classify_query_type(query, keywords):
    """Classify the type of query to help with response generation"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['area', 'volume', 'calculate', 'measure', 'room', 'space']):
        return 'analysis'
    elif any(word in query_lower for word in ['schedule', 'takeoff', 'list', 'report']):
        return 'documentation'
    elif any(word in query_lower for word in ['sheet', 'drawing', 'viewport', 'plot']):
        return 'sheets'
    elif any(word in query_lower for word in ['create', 'build', 'place', 'add', 'new']):
        return 'creation'
    elif any(word in query_lower for word in ['select', 'pick', 'filter', 'find']):
        return 'selection'
    elif any(word in query_lower for word in ['move', 'copy', 'rotate', 'modify', 'change']):
        return 'modification'
    else:
        return 'general'

def find_relevant_docs(query):
    """Legacy function for backward compatibility"""
    context = find_relevant_context(query)
    return context['documentation']
