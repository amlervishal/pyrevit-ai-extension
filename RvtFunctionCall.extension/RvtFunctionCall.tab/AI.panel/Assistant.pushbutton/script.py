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
    from utils.docs_lookup import find_relevant_context
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
        
        # Initialize status
        if hasattr(self, 'statusText'):
            self.statusText.Text = "Ready"
        
        # Clear initial content
        if hasattr(self, 'artifactTextBox'):
            self.artifactTextBox.Text = "No code generated yet. Ask a question to get started!"
        
        if hasattr(self, 'summaryTextBox'):
            self.summaryTextBox.Text = "Summaries will appear here."
    
    def ask_button_click(self, sender, e):
        """Handle click on Ask button"""
        query = self.queryTextBox.Text
        
        if not query:
            forms.alert("Please enter a question or request.", title="Empty Query")
            return
        
        # Update status
        if hasattr(self, 'statusText'):
            self.statusText.Text = "Processing..."
        
        # Show processing indicator
        self.artifactTextBox.Text = "Generating code..."
        self.summaryTextBox.Text = "Processing your request..."
        
        # Get selected model
        model = "claude" if self.modelComboBox.SelectedIndex == 0 else "gemini"
        
        try:
            # Find relevant context (docs + examples + patterns)
            context = find_relevant_context(query)
            
            # Get AI response with enhanced context
            response = get_ai_response(query, context, model)
            
            # Parse and display response
            self.parse_and_display_response(response)
            
            # Update status
            if hasattr(self, 'statusText'):
                self.statusText.Text = "Ready"
                
        except Exception as ex:
            self.artifactTextBox.Text = "Error generating code."
            self.summaryTextBox.Text = "Error: {}".format(str(ex))
            if hasattr(self, 'statusText'):
                self.statusText.Text = "Error"
    
    def parse_and_display_response(self, response):
        """Parse AI response and separate code from summary"""
        import re
        
        # Extract code blocks
        code_block = self.extract_code_from_response(response)
        
        if code_block:
            # Display clean code in artifact area
            self.artifactTextBox.Text = code_block
            
            # Create simple summary (remove verbose explanations)
            summary = self.create_simple_summary(response, code_block)
            self.summaryTextBox.Text = summary
        else:
            # No code found, show explanation only
            self.artifactTextBox.Text = "No executable code generated."
            self.summaryTextBox.Text = response
    
    def create_simple_summary(self, full_response, code_block):
        """Create a concise summary of what the script does"""
        # Remove the code block from response to get explanation
        import re
        
        # Remove code blocks from response
        clean_response = re.sub(r'```[\w]*\n[\s\S]*?\n```', '', full_response)
        
        # Split into sentences and take key points
        sentences = [s.strip() for s in clean_response.split('.') if s.strip()]
        
        # Filter for meaningful sentences (avoid verbose explanations)
        key_sentences = []
        skip_keywords = ['import', 'necessary', 'explanation', 'following', 'above', 'below']
        
        for sentence in sentences[:3]:  # Take first 3 sentences max
            if len(sentence) > 20 and not any(skip in sentence.lower() for skip in skip_keywords):
                key_sentences.append(sentence + '.')
        
        if key_sentences:
            return '\n'.join(key_sentences)
        else:
            return "This script performs the requested Revit operation."
    
    def review_fix_button_click(self, sender, e):
        """Handle Review & Fix button click"""
        current_code = self.artifactTextBox.Text
        original_query = self.queryTextBox.Text
        
        if not current_code or current_code == "No code generated yet. Ask a question to get started!":
            forms.alert("No code to review. Please generate code first.", title="No Code")
            return
        
        if not original_query:
            forms.alert("Original query not found. Please re-enter your request.", title="Missing Query")
            return
        
        # Update status
        if hasattr(self, 'statusText'):
            self.statusText.Text = "Reviewing..."
        
        # Show processing indicator
        self.summaryTextBox.Text = "Reviewing and fixing code..."
        
        # Get selected model
        model = "claude" if self.modelComboBox.SelectedIndex == 0 else "gemini"
        
        try:
            # Create review prompt
            review_prompt = self.create_review_prompt(original_query, current_code)
            
            # Find relevant context
            context = find_relevant_context(original_query)
            
            # Get AI response for review and fix
            response = get_ai_response(review_prompt, context, model)
            
            # Parse and display the fixed response
            self.parse_and_display_response(response)
            
            # Update status
            if hasattr(self, 'statusText'):
                self.statusText.Text = "Fixed"
                
        except Exception as ex:
            self.summaryTextBox.Text = "Error during review: {}".format(str(ex))
            if hasattr(self, 'statusText'):
                self.statusText.Text = "Error"
    
    def create_review_prompt(self, original_query, current_code):
        """Create a prompt for reviewing and fixing code"""
        return """Please review and fix this Revit Python code. The original request was: "{}"

Current code that may have issues:
```python
{}
```

Please:
1. Identify any potential issues or errors
2. Fix any problems found
3. Provide improved, working code
4. Keep the same functionality as requested
5. Ensure proper error handling and transactions

Provide the corrected code and a brief summary of what was fixed.""".format(original_query, current_code)
    
    def execute_button_click(self, sender, e):
        """Execute generated code in Revit"""
        code = self.artifactTextBox.Text
        
        if not code or code.strip() == "" or code == "No code generated yet. Ask a question to get started!":
            forms.alert("No code to execute!", title="Empty Code")
            return
            
        # Use the code directly from artifact (already extracted)
        code_block = code.strip()
        
        if not code_block:
            forms.alert("No executable Python code found.", title="No Code Found")
            return
            
        # Show the code that will be executed for confirmation
        if not forms.alert("Execute this code?\n\n{}".format(code_block[:500] + "..." if len(code_block) > 500 else code_block), 
                          title="Confirm Code Execution", ok=True, cancel=True):
            return
        
        # Update status
        if hasattr(self, 'statusText'):
            self.statusText.Text = "Executing..."
        
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
            
            # Update status and summary
            if hasattr(self, 'statusText'):
                self.statusText.Text = "Success"
            self.summaryTextBox.Text = "Script executed successfully!"
            
            forms.alert("Script executed successfully!", title="Success")
        except Exception as ex:
            # Update status
            if hasattr(self, 'statusText'):
                self.statusText.Text = "Error"
            self.summaryTextBox.Text = "Execution error: {}".format(str(ex))
            
            forms.alert("Error executing script:\n{}".format(str(ex)), title="Error Executing Script")
    
    def extract_code_from_response(self, response):
        """Extract Python code from AI response"""
        import re
        
        # Try to find code blocks in various formats
        
        # Method 1: Look for ```python code blocks
        python_pattern = r'```python\s*\n([\s\S]*?)\n```'
        matches = re.findall(python_pattern, response, re.MULTILINE)
        if matches:
            return '\n'.join(matches).strip()
        
        # Method 2: Look for generic ``` code blocks
        generic_pattern = r'```\s*\n([\s\S]*?)\n```'
        matches = re.findall(generic_pattern, response, re.MULTILINE)
        if matches:
            # Filter for Python-like code
            for match in matches:
                if any(keyword in match for keyword in ['import', 'def ', 'class ', 'from ', 'clr.', 'Transaction']):
                    return match.strip()
        
        # Method 3: Look for lines that start with import or other Python keywords
        lines = response.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            stripped = line.strip()
            if any(stripped.startswith(keyword) for keyword in ['import ', 'from ', 'clr.', 'def ', 'class ', 'with Transaction']):
                in_code = True
                code_lines.append(line)
            elif in_code and (stripped == '' or line.startswith('    ') or line.startswith('\t')):
                code_lines.append(line)
            elif in_code and not stripped.startswith('#') and stripped != '':
                # Might be end of code block
                if any(char in stripped for char in ['.', '(', ')', '=']):
                    code_lines.append(line)
                else:
                    break
        
        if code_lines:
            return '\n'.join(code_lines).strip()
        
        # Method 4: If no code blocks found, return empty
        return ''

# Run the UI
if __name__ == "__main__":
    try:
        ui = AssistantUI()
        ui.Show()  # Non-blocking modeless dialog - allows Revit interaction
    except Exception as e:
        forms.alert("Failed to start Assistant UI:\n{}".format(str(e)), title="Startup Error")
