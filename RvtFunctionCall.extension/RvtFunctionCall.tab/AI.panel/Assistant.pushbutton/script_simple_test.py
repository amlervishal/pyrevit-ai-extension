# -*- coding: utf-8 -*-
"""
SIMPLE FALLBACK SCRIPT - Use this if main script fails
Just shows that the extension loads and provides basic diagnostics
"""
from pyrevit import forms
import os

def main():
    """Simple diagnostic function"""
    
    # Get extension info
    current_dir = os.path.dirname(__file__)
    extension_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    
    # Check critical files
    config_exists = os.path.exists(os.path.join(extension_dir, 'config.json'))
    lib_exists = os.path.exists(os.path.join(extension_dir, 'lib'))
    
    message = """🎉 PyRevit Extension Loading Success!

Extension Directory: {}

File Status:
- config.json: {}
- lib directory: {}
- script.py: ✅ (you're seeing this!)
- icon.png: ✅ (button appeared!)

Next Steps:
1. Replace this script with the main script.py
2. Update config.json with your API keys
3. Test the full AI functionality

The ribbon is working! 🚀""".format(
        extension_dir,
        "✅ Found" if config_exists else "❌ Missing",
        "✅ Found" if lib_exists else "❌ Missing"
    )
    
    forms.alert(message, title="Extension Test - SUCCESS!")

if __name__ == "__main__":
    main()
