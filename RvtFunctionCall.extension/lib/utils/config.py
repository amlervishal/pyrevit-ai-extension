# -*- coding: utf-8 -*-
"""
Configuration utilities for Revit Function Call
"""
import os
import json

# Default configuration
DEFAULT_CONFIG = {
    'default_model': 'claude',  # Options: 'claude', 'gemini'
    'claude_api_key': '',       # Your Claude API key
    'gemini_api_key': '',       # Your Gemini API key
    'max_docs': 5               # Maximum number of document sections to retrieve
}

def get_config_path():
    """Get the path to the configuration file"""
    # Config will be stored in the extension directory
    extension_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(extension_dir, 'config.json')

def load_config():
    """Load configuration from file or create default if it doesn't exist"""
    config_path = get_config_path()
    
    # If config file doesn't exist, create it with defaults
    if not os.path.exists(config_path):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    # Read and parse config file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception:
        # If there's an error reading the file, return defaults
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file"""
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
