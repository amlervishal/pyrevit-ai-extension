# -*- coding: utf-8 -*-
"""
Revit Function Call AI Assistant - FIXED VERSION
--------------------------------
Provides an interface to ask questions about Revit API and generate Python scripts
using AI models (Claude or Gemini).
"""
import os
import sys
import clr
from pyrevit import forms
from pyrevit import script

# Add our lib directory to path
lib_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
utils_path = os.path.join(lib_path, 'lib', 'utils')
sys.path.append(os.path.join(lib_path, 'lib'))

# Import our utility modules with error handling
try:
    from utils.ai_client import get_ai_response
    from utils.docs_lookup import find_relevant_docs
    from utils.config import load_config
except ImportError as e:
    # Fallback for pyRevit environment
    try:
        import imp
        ai_client_module = imp.load_source('ai_client', os.path.join(utils_path, 'ai_client.py'))
        docs_lookup_module = imp.load_source('docs_lookup', os.path.join(utils_path, 'docs_lookup.py'))
        config_module = imp.load_source('config', os.path.join(utils_path, 'config.py'))
        
        get_ai_response = ai_client_module.get_ai_response
        find_relevant_docs = docs_lookup_module.find_relevant_docs
        load_config = config_module.load_config
    except Exception as import_error:
        print("Failed to import utilities: {}".format(str(import_error)))
        raise

# Setup output window
output = script.get_output()
output.close_others()

class AssistantUI(forms.WPFWindow):
    """
    Main UI window for Revit Function Call Assistant
    """
    
    def __init__(self):
        # Load WPF form
        forms.WPFWindow.__init__(self, os.path.join(os.path.dirname(__file__), 'ui.xaml'))
        
        # Load configuration
        self.config = load_config()
        
        # Initialize UI elements
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI elements"""
        # Set window title
        self.Title = "Revit AI Assistant"
        
        # Set model selection based on config
        if hasattr(self, 'modelComboBox'):
            self.modelComboBox.Items.Clear()
            self.modelComboBox.Items.Add("Claude")
            self.modelComboBox.Items.Add("Gemini")
            self.modelComboBox.SelectedIndex = 0 if self.config.get('default_model') == 'claude' else 1
    
    def ask_button_click(self, sender, e):
        """Handle click on Ask button"""
        query = self.queryTextBox.Text
        
        if not query:
            forms.alert("Please enter a question or request.", title="Empty Query")
            return
        
        # Show processing indicator
        self.responseTextBox.Text = "Processing your request..."
        
        # Get selected model
        model = "claude" if self.modelComboBox.SelectedIndex == 0 else "gemini"
        
        try:
            # Find relevant documentation
            docs = find_relevant_docs(query)
            
            # Get AI response
            response = get_ai_response(query, docs, model)
            
            # Display response
            self.display_response(response)
        except Exception as ex:
            self.responseTextBox.Text = "Error: {}".format(str(ex))
    
    def display_response(self, response):
        """Display the AI response"""
        self.responseTextBox.Text = response
    
    def execute_button_click(self, sender, e):
        """Execute generated code in Revit"""
        code = self.responseTextBox.Text
        
        # Extract code block if it's within markdown code fences
        if "```python" in code and "```" in code.split("```python", 1)[1]:
            code_block = code.split("```python", 1)[1].split("```", 1)[0].strip()
        elif "```" in code and "```" in code.split("```", 1)[1]:
            code_block = code.split("```", 1)[1].split("```", 1)[0].strip()
        else:
            code_block = code
        
        # Execute the code in Revit
        try:
            # Import Revit API modules for the executed code
            clr.AddReference('RevitAPI')
            clr.AddReference('RevitAPIUI')
            from Autodesk.Revit.DB import *
            from Autodesk.Revit.UI import *
            
            # Get current document context
            doc = __revit__.ActiveUIDocument.Document
            uidoc = __revit__.ActiveUIDocument
            
            # Create a transaction for any model changes
            if 'Transaction' in code_block:
                # Code already handles transactions
                exec(code_block, globals(), locals())
            else:
                # Wrap in a transaction for safety
                with Transaction(doc, "AI Generated Script") as t:
                    t.Start()
                    try:
                        exec(code_block, globals(), locals())
                        t.Commit()
                    except:
                        t.RollBack()
                        raise
            
            forms.alert("Script executed successfully!", title="Success")
        except Exception as ex:
            forms.alert("Error executing script:\n{}".format(str(ex)), title="Error Executing Script")

# Run the UI
if __name__ == "__main__":
    try:
        AssistantUI().ShowDialog()
    except Exception as e:
        forms.alert("Failed to start Assistant UI:\n{}".format(str(e)), title="Startup Error")
