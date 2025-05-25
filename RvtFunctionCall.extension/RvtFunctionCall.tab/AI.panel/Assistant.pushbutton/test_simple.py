# -*- coding: utf-8 -*-
"""
Simple test script to verify extension loading
Replace script.py with this temporarily if main script fails
"""
from pyrevit import forms

def main():
    """Simple test function"""
    forms.alert("Extension loaded successfully!", title="Test Success")

if __name__ == "__main__":
    main()
