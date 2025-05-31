# -*- coding: utf-8 -*-
"""
Revit AI Assistant - Complete Agentic Workflow
"""
import os
import sys
import clr
from pyrevit import forms, script
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

current_dir = os.path.dirname(__file__)
extension_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
lib_path = os.path.join(extension_dir, 'lib')
sys.path.append(lib_path)

from utils.ai_client import get_ai_response
from utils.docs_lookup import find_relevant_context
from utils.config import load_config
from utils.task_agent import understand_and_formulate_tasks, formulate_enhanced_query

class AssistantUI(forms.WPFWindow):
    """Main UI window for Revit AI Assistant with complete agentic workflow"""
    
    def __init__(self):
        xaml_path = os.path.join(os.path.dirname(__file__), 'ui.xaml')
        forms.WPFWindow.__init__(self, xaml_path)
        
        self.config = load_config()
        self.last_error = None
        self.last_query = None
        self.last_context = None
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize UI elements"""
        self.Title = "Revit AI Assistant - Agentic Workflow"
        
        self.modelComboBox.Items.Clear()
        self.modelComboBox.Items.Add("Claude")
        self.modelComboBox.Items.Add("Gemini")
        self.modelComboBox.SelectedIndex = 0 if self.config.get('default_model') == 'claude' else 1
        
        self.statusText.Text = "Ready for agentic workflow"
        self.artifactTextBox.Text = "Generated code will appear here..."
        self.summaryTextBox.Text = "Task analysis and response summary will appear here..."
    
    def ask_button_click(self, sender, e):
        """Handle Ask button - Complete agentic workflow"""
        query = self.queryTextBox.Text.strip()
        if not query:
            forms.alert("Please enter a question.", title="Empty Query")
            return
        
        self.last_query = query
        self.last_error = None
        
        self.statusText.Text = "Agent analyzing task..."
        
        task_analysis = understand_and_formulate_tasks(query)
        enhanced_query = formulate_enhanced_query(query, task_analysis)
        
        analysis_summary = """AGENT TASK ANALYSIS:
Action: {}
Elements: {}
Complexity: {}
Needs Selection: {}
Needs Transaction: {}
Approach: {}

Processing...""".format(
            task_analysis["primary_action"] or "general",
            ", ".join(task_analysis["target_elements"]) if task_analysis["target_elements"] else "unspecified",
            task_analysis["complexity"],
            "Yes" if task_analysis["requires_selection"] else "No",
            "Yes" if task_analysis["requires_transaction"] else "No",
            task_analysis["suggested_approach"]
        )
        
        self.summaryTextBox.Text = analysis_summary
        self.statusText.Text = "Querying documentation database..."
        
        context = find_relevant_context(query)
        self.last_context = context
        
        self.statusText.Text = "Agent generating code..."
        self.artifactTextBox.Text = "Agent is generating code based on task analysis..."
        
        model = "claude" if self.modelComboBox.SelectedIndex == 0 else "gemini"
        response = get_ai_response(enhanced_query, context, model)
        
        self.parse_and_display_response(response, task_analysis)
        self.statusText.Text = "Ready - Code generated"
    
    def parse_and_display_response(self, response, task_analysis):
        """Extract code from response and display with task context"""
        import re
        
        code_pattern = r'```(?:python)?\s*\n([\s\S]*?)\n```'
        matches = re.findall(code_pattern, response)
        
        if matches:
            code = matches[0].strip()
            self.artifactTextBox.Text = code
            
            summary_parts = [
                "TASK COMPLETED:",
                "Action: {}".format(task_analysis["primary_action"] or "general"),
                "Elements: {}".format(", ".join(task_analysis["target_elements"]) if task_analysis["target_elements"] else "unspecified"),
                "",
                "AGENT RESPONSE:",
                re.sub(code_pattern, '[Code Generated - See Above]', response).strip()[:500]
            ]
            
            if len(response) > 500:
                summary_parts.append("... (response truncated)")
            
            self.summaryTextBox.Text = "\n".join(summary_parts)
        else:
            self.artifactTextBox.Text = "No code block found in response"
            self.summaryTextBox.Text = "AGENT RESPONSE (No Code):\n" + response
    
    def execute_button_click(self, sender, e):
        """Execute the generated code with error capture"""
        code = self.artifactTextBox.Text.strip()
        
        if not code or code == "Generated code will appear here...":
            forms.alert("No code to execute!", title="Empty Code")
            return
        
        if not forms.alert("Execute this code?", ok=True, cancel=True):
            return
        
        self.statusText.Text = "Executing code..."
        
        try:
            self.execute_code(code)
            
            self.statusText.Text = "Success - Script completed"
            self.summaryTextBox.Text += "\n\n✅ EXECUTION SUCCESSFUL: Script ran without errors!"
            self.last_error = None
            forms.alert("Script executed successfully!", title="Success")
            
        except Exception as e:
            error_message = str(e)
            self.last_error = error_message
            
            self.statusText.Text = "Error - See summary"
            error_summary = "\n\n❌ EXECUTION ERROR:\n{}".format(error_message)
            self.summaryTextBox.Text += error_summary
            
            forms.alert("Script execution failed. Use 'Fix Code' button to automatically correct the error.", title="Execution Error")
    
    def review_fix_button_click(self, sender, e):
        """Fix code based on error or general review"""
        if not self.last_query:
            forms.alert("No previous query to fix. Please generate code first.", title="No Query")
            return
        
        current_code = self.artifactTextBox.Text.strip()
        if not current_code or current_code == "Generated code will appear here...":
            forms.alert("No code to fix. Please generate code first.", title="No Code")
            return
        
        self.statusText.Text = "Agent fixing code..."
        
        if self.last_error:
            fix_prompt = """ORIGINAL TASK: {}

CURRENT CODE WITH ERROR:
```python
{}
```

ERROR MESSAGE: {}

TASK: Fix the code to resolve this error. The error occurred during execution in Revit. 
Generate corrected IronPython 2.7 code that addresses the specific error while maintaining the original functionality.""".format(
                self.last_query, current_code, self.last_error
            )
        else:
            fix_prompt = """ORIGINAL TASK: {}

CURRENT CODE FOR REVIEW:
```python
{}
```

TASK: Review and improve this code. Check for:
- IronPython 2.7 compatibility
- Proper error handling
- Revit API best practices
- Transaction handling
- Performance optimizations

Generate improved IronPython 2.7 code.""".format(self.last_query, current_code)
        
        model = "claude" if self.modelComboBox.SelectedIndex == 0 else "gemini"
        
        context = self.last_context if self.last_context else find_relevant_context(self.last_query)
        
        response = get_ai_response(fix_prompt, context, model)
        
        task_analysis = understand_and_formulate_tasks(self.last_query)
        self.parse_and_display_response(response, task_analysis)
        
        self.statusText.Text = "Code fixed - Ready to execute"
        fix_summary = "\n\n🔧 CODE FIXED: Agent has analyzed and corrected the code."
        if self.last_error:
            fix_summary += " Error addressed: {}".format(self.last_error[:100])
        self.summaryTextBox.Text += fix_summary
        
        self.last_error = None
    
    def execute_code(self, code):
        """Execute code in Revit context"""
        doc = __revit__.ActiveUIDocument.Document
        uidoc = __revit__.ActiveUIDocument
        
        exec_globals = {
            '__revit__': __revit__,
            'doc': doc,
            'uidoc': uidoc,
            'clr': clr,
            'Transaction': Transaction,
            'FilteredElementCollector': FilteredElementCollector,
            'TaskDialog': TaskDialog
        }
        
        for attr_name in dir(sys.modules[__name__]):
            attr = getattr(sys.modules[__name__], attr_name)
            if hasattr(attr, '__module__') and attr.__module__ == 'Autodesk.Revit.DB':
                exec_globals[attr_name] = attr
        
        exec(code, exec_globals)

if __name__ == "__main__":
    ui = AssistantUI()
    ui.ShowDialog()
