# -*- coding: utf-8 -*-
"""
Revit Function Call AI Assistant - ROBUST VERSION with Fallbacks
--------------------------------
Provides an interface to ask questions about Revit API and generate Python scripts
using AI models (Claude or Gemini).
Includes comprehensive error handling to ensure ribbon loading.
"""
import os
import sys
import traceback

# Essential imports that must work for ribbon to load
try:
    import clr
    from pyrevit import forms
    from pyrevit import script
    PYREVIT_AVAILABLE = True
except ImportError as e:
    print("PyRevit not available: {}".format(e))
    PYREVIT_AVAILABLE = False
    # Create fallback functions
    class FallbackForms:
        @staticmethod
        def alert(message, title="Alert"):
            print("ALERT [{}]: {}".format(title, message))
    forms = FallbackForms()

# Global variables for fallback handling
AI_FUNCTIONS_AVAILABLE = False
CONFIG_AVAILABLE = False
get_ai_response = None
find_relevant_context = None
load_config = None

def safe_import_utilities():
    """Safely import utility modules with comprehensive fallback handling"""
    global AI_FUNCTIONS_AVAILABLE, CONFIG_AVAILABLE, get_ai_response, find_relevant_context, load_config
    
    # Try to add lib directory to path
    try:
        current_dir = os.path.dirname(__file__)
        extension_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        lib_path = os.path.join(extension_dir, 'lib')
        utils_path = os.path.join(lib_path, 'utils')
        
        if lib_path not in sys.path:
            sys.path.append(lib_path)
            
        print("Added lib path: {}".format(lib_path))
    except Exception as e:
        print("Failed to add lib path: {}".format(e))
    
    # Try importing utilities with multiple fallback methods
    try:
        # Method 1: Standard import
        from utils.ai_client import get_ai_response as _get_ai_response
        from utils.docs_lookup import find_relevant_context as _find_relevant_context
        from utils.config import load_config as _load_config
        
        get_ai_response = _get_ai_response
        find_relevant_context = _find_relevant_context
        load_config = _load_config
        
        AI_FUNCTIONS_AVAILABLE = True
        CONFIG_AVAILABLE = True
        print("✅ Standard utility imports successful")
        
        return True
        
    except ImportError as e:
        print("Standard import failed: {}".format(e))
        
        # Method 2: Direct file loading
        try:
            import imp
            
            # Load modules directly
            config_module = imp.load_source('config', os.path.join(utils_path, 'config.py'))
            ai_client_module = imp.load_source('ai_client', os.path.join(utils_path, 'ai_client.py'))
            docs_lookup_module = imp.load_source('docs_lookup', os.path.join(utils_path, 'docs_lookup.py'))
            
            get_ai_response = ai_client_module.get_ai_response
            find_relevant_context = docs_lookup_module.find_relevant_context
            load_config = config_module.load_config
            
            AI_FUNCTIONS_AVAILABLE = True
            CONFIG_AVAILABLE = True
            print("✅ Direct file loading successful")
            
            return True
            
        except Exception as e2:
            print("Direct file loading failed: {}".format(e2))
            
            # Method 3: Create minimal fallback functions
            try:
                def fallback_load_config():
                    """Fallback config loader"""
                    return {
                        'default_model': 'claude',
                        'claude_api_key': '',
                        'gemini_api_key': '',
                        'max_docs': 5
                    }
                
                def fallback_get_ai_response(query, context, model="claude"):
                    """Fallback AI response"""
                    return "ERROR: AI client not available. Please check your configuration and utility modules."
                
                def fallback_find_relevant_context(query):
                    """Fallback context finder"""
                    return {"documentation": [], "examples": [], "patterns": {}}
                
                get_ai_response = fallback_get_ai_response
                find_relevant_context = fallback_find_relevant_context
                load_config = fallback_load_config
                
                CONFIG_AVAILABLE = True
                print("⚠️ Using fallback functions")
                
                return True
                
            except Exception as e3:
                print("Even fallback creation failed: {}".format(e3))
                return False

class AssistantUI(forms.WPFWindow):
    """
    Main UI window for Revit Function Call Assistant with robust error handling
    """
    
    def __init__(self):
        global AI_FUNCTIONS_AVAILABLE, CONFIG_AVAILABLE, get_ai_response, find_relevant_context, load_config
        
        try:
            # Load WPF form with error handling
            xaml_path = os.path.join(os.path.dirname(__file__), 'ui.xaml')
            if not os.path.exists(xaml_path):
                raise Exception("UI XAML file not found: {}".format(xaml_path))
                
            forms.WPFWindow.__init__(self, xaml_path)
            
            # Store global state in instance variables
            self.ai_functions_available = AI_FUNCTIONS_AVAILABLE
            self.config_available = CONFIG_AVAILABLE
            self.get_ai_response = get_ai_response
            self.find_relevant_context = find_relevant_context
            self.load_config = load_config
            
            # Load configuration with fallback
            try:
                self.config = self.load_config() if self.load_config else {'default_model': 'claude'}
            except Exception as e:
                print("Config loading failed, using defaults: {}".format(e))
                self.config = {'default_model': 'claude'}
            
            # Initialize UI elements
            self.setup_ui()
            
        except Exception as e:
            print("UI initialization failed: {}".format(e))
            # Try to show error in simple form
            try:
                forms.alert("UI initialization failed: {}".format(str(e)), title="UI Error")
            except:
                print("Even error alert failed")
            raise
    
    def setup_ui(self):
        """Set up the UI elements with error handling"""
        try:
            # Set window title
            self.Title = "Revit AI Assistant"
            
            # Set model selection based on config
            if hasattr(self, 'modelComboBox'):
                try:
                    self.modelComboBox.Items.Clear()
                    self.modelComboBox.Items.Add("Claude")
                    self.modelComboBox.Items.Add("Gemini")
                    self.modelComboBox.SelectedIndex = 0 if self.config.get('default_model') == 'claude' else 1
                except Exception as e:
                    print("Model combobox setup failed: {}".format(e))
            
            # Initialize status
            if hasattr(self, 'statusText'):
                try:
                    status = "Ready" if self.ai_functions_available else "Limited Mode - Check Configuration"
                    self.statusText.Text = status
                except Exception as e:
                    print("Status text setup failed: {}".format(e))
            
            # Clear initial content
            if hasattr(self, 'artifactTextBox'):
                try:
                    self.artifactTextBox.Text = "No code generated yet. Ask a question to get started!"
                except Exception as e:
                    print("Artifact textbox setup failed: {}".format(e))
            
            if hasattr(self, 'summaryTextBox'):
                try:
                    summary = "Summaries will appear here."
                    if not self.ai_functions_available:
                        summary += "\n\nNOTE: AI functions not available - check API keys and configuration."
                    self.summaryTextBox.Text = summary
                except Exception as e:
                    print("Summary textbox setup failed: {}".format(e))
                    
        except Exception as e:
            print("UI setup failed: {}".format(e))
    
    def ask_button_click(self, sender, e):
        """Handle click on Ask button with comprehensive error handling"""
        try:
            if not hasattr(self, 'queryTextBox'):
                forms.alert("Query input not available", title="UI Error")
                return
                
            query = self.queryTextBox.Text
            
            if not query or not query.strip():
                forms.alert("Please enter a question or request.", title="Empty Query")
                return
            
            # Check if AI functions are available
            if not self.ai_functions_available:
                forms.alert("AI functions not available. Please check your configuration.", title="Configuration Error")
                return
            
            # Update status
            if hasattr(self, 'statusText'):
                self.statusText.Text = "Processing..."
            
            # Show processing indicator
            if hasattr(self, 'artifactTextBox'):
                self.artifactTextBox.Text = "Generating code..."
            if hasattr(self, 'summaryTextBox'):
                self.summaryTextBox.Text = "Processing your request..."
            
            # Get selected model
            try:
                model = "claude" if self.modelComboBox.SelectedIndex == 0 else "gemini"
            except:
                model = "claude"  # Default fallback
            
            try:
                # Find relevant context (docs + examples + patterns)
                context = self.find_relevant_context(query) if self.find_relevant_context else {}
                
                # Get AI response with enhanced context
                response = self.get_ai_response(query, context, model) if self.get_ai_response else "AI response not available"
                
                # Parse and display response
                self.parse_and_display_response(response)
                
                # Update status
                if hasattr(self, 'statusText'):
                    self.statusText.Text = "Ready"
                    
            except Exception as ex:
                error_msg = "Error: {}".format(str(ex))
                if hasattr(self, 'artifactTextBox'):
                    self.artifactTextBox.Text = "Error generating code."
                if hasattr(self, 'summaryTextBox'):
                    self.summaryTextBox.Text = error_msg
                if hasattr(self, 'statusText'):
                    self.statusText.Text = "Error"
                    
        except Exception as e:
            try:
                forms.alert("Ask button error: {}".format(str(e)), title="Button Error")
            except:
                print("Ask button error: {}".format(str(e)))
    
    def parse_and_display_response(self, response):
        """Parse AI response and separate code from summary with error handling"""
        try:
            import re
            
            # Extract code blocks
            code_block = self.extract_code_from_response(response)
            
            if code_block:
                # Display clean code in artifact area
                if hasattr(self, 'artifactTextBox'):
                    self.artifactTextBox.Text = code_block
                
                # Create simple summary (remove verbose explanations)
                summary = self.create_simple_summary(response, code_block)
                if hasattr(self, 'summaryTextBox'):
                    self.summaryTextBox.Text = summary
            else:
                # No code found, show explanation only
                if hasattr(self, 'artifactTextBox'):
                    self.artifactTextBox.Text = "No executable code generated."
                if hasattr(self, 'summaryTextBox'):
                    self.summaryTextBox.Text = response
                    
        except Exception as e:
            print("Response parsing error: {}".format(e))
            if hasattr(self, 'summaryTextBox'):
                self.summaryTextBox.Text = "Error parsing response: {}".format(str(e))
    
    def create_simple_summary(self, full_response, code_block):
        """Create a concise summary of what the script does"""
        try:
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
                
        except Exception as e:
            return "Summary generation failed: {}".format(str(e))
    
    def review_fix_button_click(self, sender, e):
        """Handle Review & Fix button click with error handling"""
        try:
            if not self.ai_functions_available:
                forms.alert("AI functions not available for review.", title="Feature Unavailable")
                return
                
            current_code = getattr(self, 'artifactTextBox', None)
            current_code = current_code.Text if current_code else ""
            
            original_query = getattr(self, 'queryTextBox', None)
            original_query = original_query.Text if original_query else ""
            
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
            if hasattr(self, 'summaryTextBox'):
                self.summaryTextBox.Text = "Reviewing and fixing code..."
            
            # Get selected model
            try:
                model = "claude" if self.modelComboBox.SelectedIndex == 0 else "gemini"
            except:
                model = "claude"
            
            try:
                # Create review prompt
                review_prompt = self.create_review_prompt(original_query, current_code)
                
                # Find relevant context
                context = self.find_relevant_context(original_query) if self.find_relevant_context else {}
                
                # Get AI response for review and fix
                response = self.get_ai_response(review_prompt, context, model) if self.get_ai_response else "Review not available"
                
                # Parse and display the fixed response
                self.parse_and_display_response(response)
                
                # Update status
                if hasattr(self, 'statusText'):
                    self.statusText.Text = "Fixed"
                    
            except Exception as ex:
                if hasattr(self, 'summaryTextBox'):
                    self.summaryTextBox.Text = "Error during review: {}".format(str(ex))
                if hasattr(self, 'statusText'):
                    self.statusText.Text = "Error"
                    
        except Exception as e:
            try:
                forms.alert("Review error: {}".format(str(e)), title="Review Error")
            except:
                print("Review error: {}".format(str(e)))
    
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
        """Execute generated code in Revit with bulletproof scope handling"""
        try:
            if not hasattr(self, 'artifactTextBox'):
                from pyrevit import forms as pyrevit_forms
                pyrevit_forms.alert("Code display not available", title="UI Error")
                return
                
            code = self.artifactTextBox.Text
            
            if not code or code.strip() == "" or code == "No code generated yet. Ask a question to get started!":
                from pyrevit import forms as pyrevit_forms
                pyrevit_forms.alert("No code to execute!", title="Empty Code")
                return
                
            # Use the code directly from artifact (already extracted)
            code_block = code.strip()
            
            if not code_block:
                from pyrevit import forms as pyrevit_forms
                pyrevit_forms.alert("No executable Python code found.", title="No Code Found")
                return
                
            # Show the code that will be executed for confirmation
            from pyrevit import forms as pyrevit_forms
            if not pyrevit_forms.alert("Execute this code?\n\n{}".format(code_block[:500] + "..." if len(code_block) > 500 else code_block), 
                              title="Confirm Code Execution", ok=True, cancel=True):
                return
            
            # Update status
            if hasattr(self, 'statusText'):
                self.statusText.Text = "Executing..."
            
            # Execute the code in Revit with bulletproof scope
            try:
                self._execute_code_safely(code_block)
                
                # Update status and summary
                if hasattr(self, 'statusText'):
                    self.statusText.Text = "Success"
                if hasattr(self, 'summaryTextBox'):
                    self.summaryTextBox.Text = "Script executed successfully!"
                
                from pyrevit import forms as pyrevit_forms
                pyrevit_forms.alert("Script executed successfully!", title="Success")
                
            except Exception as ex:
                # Update status
                if hasattr(self, 'statusText'):
                    self.statusText.Text = "Error"
                if hasattr(self, 'summaryTextBox'):
                    self.summaryTextBox.Text = "Execution error: {}".format(str(ex))
                
                from pyrevit import forms as pyrevit_forms
                pyrevit_forms.alert("Error executing script:\n{}".format(str(ex)), title="Error Executing Script")
                
        except Exception as e:
            try:
                from pyrevit import forms as pyrevit_forms
                pyrevit_forms.alert("Execute button error: {}".format(str(e)), title="Execution Error")
            except:
                print("Execute button error: {}".format(str(e)))
    
    def _execute_code_safely(self, code_block):
        """Execute code with comprehensive scope setup and proper Revit context validation"""
        # First, validate Revit context
        if not self._validate_revit_context():
            raise Exception("No active Revit document found. Please open a Revit project first.")
        
        # Sanitize the code for IronPython 2.7 compatibility
        code_block = self._sanitize_code_for_ironpython(code_block)
        
        # Import everything we need at module level first
        import clr
        import System
        from System.Collections.Generic import List
        
        # Add Revit references
        clr.AddReference('RevitAPI')
        clr.AddReference('RevitAPIUI')
        
        # Import all Revit classes
        from Autodesk.Revit.DB import *
        from Autodesk.Revit.UI import *
        import Autodesk.Revit.DB as DB
        import Autodesk.Revit.UI as UI
        
        # Get current document and UI document with validation
        revit_app = None
        try:
            # Try multiple ways to get __revit__
            if '__revit__' in globals():
                revit_app = globals()['__revit__']
            elif hasattr(__builtins__, '__revit__'):
                revit_app = getattr(__builtins__, '__revit__')
            else:
                # Try to get from pyrevit context
                try:
                    from pyrevit import HOST_APP
                    revit_app = HOST_APP
                except:
                    raise Exception("Cannot find Revit application context")
            
            uidoc = revit_app.ActiveUIDocument
            if not uidoc:
                raise Exception("No active UI document found")
            
            doc = uidoc.Document
            if not doc:
                raise Exception("No active document found")
                
            # Additional validation
            if doc.IsFamilyDocument:
                # Family documents have different transaction requirements
                pass  # We'll handle this below
            
        except Exception as e:
            raise Exception("Cannot access Revit document: {}. Please ensure you have an active Revit project open.".format(str(e)))
        
        # Create comprehensive execution namespace
        exec_namespace = {}
        
        # Add standard Python modules that might be needed
        import sys, os, math, json, re
        exec_namespace.update({
            # Standard modules
            'sys': sys,
            'os': os, 
            'math': math,
            'json': json,
            're': re,
            
            # .NET/CLR
            'clr': clr,
            'System': System,
            'List': List,
            
            # Revit context  
            '__revit__': revit_app,
            'doc': doc,
            'uidoc': uidoc,
        })
        
        # Add all Revit DB classes to namespace
        db_classes = [
            'Transaction', 'TransactionGroup', 'SubTransaction',
            'FilteredElementCollector', 'Element', 'ElementId', 'ElementType',
            'Level', 'Grid', 'Wall', 'Floor', 'Ceiling', 'Door', 'Window', 'Room',
            'FamilyInstance', 'FamilySymbol', 'Family', 'Category',
            'Parameter', 'ParameterValueProvider', 'ParameterSet',
            'View', 'View3D', 'ViewPlan', 'ViewSection', 'ViewSheet',
            'Line', 'Arc', 'Circle', 'Ellipse', 'NurbSpline', 'HermiteSpline',
            'XYZ', 'UV', 'Transform', 'Plane', 'BoundingBoxXYZ',
            'CurveLoop', 'CurveArray', 'GeometryObject', 'Solid', 'Face', 'Edge',
            'Material', 'MaterialElement', 'Appearance',
            'ElementCategoryFilter', 'ElementClassFilter', 'ElementLevelFilter',
            'ElementParameterFilter', 'LogicalAndFilter', 'LogicalOrFilter',
            'BoundingBoxIntersectsFilter', 'BoundingBoxIsInsideFilter',
            'BuiltInCategory', 'BuiltInParameter', 'UnitType', 'DisplayUnitType',
            'TaskDialog', 'TaskDialogCommonButtons', 'TaskDialogResult',
            'CopyPasteOptions', 'ElementTransformUtils',
            'Options', 'GeometryElement', 'GeometryInstance',
            'Reference', 'ReferenceArray', 'IntersectionResult',
            'Units', 'UnitUtils', 'UnitSystem'
        ]
        
        # Add classes that exist in the DB module
        for class_name in db_classes:
            if hasattr(DB, class_name):
                exec_namespace[class_name] = getattr(DB, class_name)
        
        # Add all UI classes
        ui_classes = [
            'UIApplication', 'UIDocument', 'Selection',
            'TaskDialog', 'TaskDialogCommonButtons', 'TaskDialogResult',
            'MessageBox', 'DialogResult'
        ]
        
        for class_name in ui_classes:
            if hasattr(UI, class_name):
                exec_namespace[class_name] = getattr(UI, class_name)
        
        # Execute with proper transaction handling
        self._execute_with_transaction(code_block, exec_namespace, doc)
    
    def _validate_revit_context(self):
        """Validate that we have a proper Revit context for transactions"""
        try:
            # Check if __revit__ is available in globals
            revit_app = None
            if '__revit__' in globals():
                revit_app = globals()['__revit__']
            elif hasattr(__builtins__, '__revit__'):
                revit_app = getattr(__builtins__, '__revit__')
            else:
                # Try to get from pyrevit context
                try:
                    from pyrevit import HOST_APP
                    revit_app = HOST_APP
                except:
                    pass
            
            if not revit_app:
                print("DEBUG: __revit__ not found in any context")
                return False
            
            # Check if we have an active UI document
            try:
                uidoc = revit_app.ActiveUIDocument
                if not uidoc:
                    print("DEBUG: No ActiveUIDocument")
                    return False
            except Exception as e:
                print("DEBUG: Error accessing ActiveUIDocument: {}".format(e))
                return False
            
            # Check if we have an active document
            try:
                doc = uidoc.Document
                if not doc:
                    print("DEBUG: No Document")
                    return False
            except Exception as e:
                print("DEBUG: Error accessing Document: {}".format(e))
                return False
            
            # Check if document is valid (not null/disposed)
            try:
                # Try to access a basic property
                title = doc.Title
                print("DEBUG: Document found - Title: {}".format(title))
                return True
            except Exception as e:
                print("DEBUG: Error accessing document properties: {}".format(e))
                return False
                
        except Exception as e:
            print("DEBUG: Exception in _validate_revit_context: {}".format(e))
            return False
    
    def _execute_with_transaction(self, code_block, exec_namespace, doc):
        """Execute code with appropriate transaction handling based on content"""
        # Check if code already handles transactions
        has_transaction = ('Transaction(' in code_block or 
                          'transaction' in code_block.lower() or
                          'TransactionGroup(' in code_block or
                          'SubTransaction(' in code_block)
        
        if has_transaction:
            # Code handles its own transactions - just execute
            try:
                exec(code_block, exec_namespace)
            except Exception as ex:
                # Re-raise with more context
                raise Exception("Error in user transaction code: {}".format(str(ex)))
        else:
            # Check if code needs a transaction (modifies the model)
            needs_transaction = self._code_needs_transaction(code_block)
            
            if needs_transaction:
                # Wrap in a transaction
                try:
                    # Use the document's transaction manager
                    transaction = Transaction(doc, "AI Generated Script")
                    exec_namespace['transaction'] = transaction
                    
                    # Start transaction with proper error handling
                    status = transaction.Start()
                    if status != TransactionStatus.Started:
                        raise Exception("Failed to start transaction. Status: {}".format(status))
                    
                    try:
                        exec(code_block, exec_namespace)
                        
                        # Commit transaction
                        commit_status = transaction.Commit()
                        if commit_status != TransactionStatus.Committed:
                            raise Exception("Failed to commit transaction. Status: {}".format(commit_status))
                            
                    except Exception as ex:
                        # Rollback on any error
                        if transaction.GetStatus() == TransactionStatus.Started:
                            transaction.RollBack()
                        raise Exception("Error during transaction: {}".format(str(ex)))
                        
                except Exception as ex:
                    # Handle transaction creation errors
                    if "API context" in str(ex) or "external application" in str(ex):
                        raise Exception("Cannot create transaction - no active Revit document or invalid API context. Please ensure you have a Revit project open and try again.")
                    else:
                        raise ex
            else:
                # No transaction needed - just execute (read-only operations)
                exec(code_block, exec_namespace)
    
    def _code_needs_transaction(self, code_block):
        """Determine if code needs a transaction by analyzing its content"""
        # Keywords that typically indicate model modification
        modification_keywords = [
            '.Create', '.NewWall', '.NewFloor', '.NewCeiling',
            '.Delete', '.Move', '.Copy', '.Rotate',
            '.SetParameterByName', '.set_Parameter',
            'SetValueString', 'SetValueDouble', 'SetValueInteger', 'Set(',
            'ElementTransformUtils', 'CopyElements', 'MoveElements',
            'doc.Regenerate', 'doc.Save',
            'NewFamilyInstance', 'PlaceComponent'
        ]
        
        # Check if any modification keywords are present
        code_lower = code_block.lower()
        for keyword in modification_keywords:
            if keyword.lower() in code_lower:
                return True
        
        # If we're not sure, default to using a transaction for safety
        # Exception: if code is clearly read-only (only contains collectors, gets, etc.)
        readonly_only_keywords = [
            'FilteredElementCollector', '.ToElements()', '.FirstElement()',
            'get_Parameter', 'GetParameterValueByName', '.Name', '.Id',
            'TaskDialog.Show', 'print(', 'MessageBox.Show'
        ]
        
        # If code only contains read-only operations, don't use transaction
        has_readonly_only = any(keyword.lower() in code_lower for keyword in readonly_only_keywords)
        has_no_modifications = not any(keyword.lower() in code_lower for keyword in modification_keywords)
        
        if has_readonly_only and has_no_modifications:
            return False
        
        # Default to using transaction for safety
        return True
    
    def _sanitize_code_for_ironpython(self, code):
        """Convert Python 3+ syntax to IronPython 2.7 compatible syntax"""
        import re
        
        # Fix f-strings - this is the most common issue
        # Pattern: f"text {variable}" -> "text {}".format(variable)
        # Pattern: f'text {variable}' -> 'text {}'.format(variable)
        
        def fix_fstring(match):
            quote = match.group(1)  # " or '
            content = match.group(2)  # everything between quotes
            
            # Find all {variable} patterns
            var_pattern = r'\{([^}]+)\}'
            variables = re.findall(var_pattern, content)
            
            # Replace {variable} with {} and collect variables
            fixed_content = re.sub(var_pattern, '{}', content)
            
            # Build the .format() call
            if variables:
                var_list = ', '.join(variables)
                return '{quote}{content}{quote}.format({vars})'.format(
                    quote=quote, content=fixed_content, vars=var_list)
            else:
                # No variables, just remove f prefix
                return '{quote}{content}{quote}'.format(quote=quote, content=content)
        
        # Fix f"..." patterns
        code = re.sub(r'f(["\'])([^"\']*)\1', fix_fstring, code)
        
        # Fix **revit** back to __revit__ (common AI mistake)
        code = code.replace('**revit**', '__revit__')
        code = code.replace('*revit*', '__revit__')
        
        # Fix other Python 3+ syntax issues
        # Fix print statements (though most should already be function calls)
        # Pattern: print "text" -> print("text")
        code = re.sub(r'\bprint\s+([^\n(][^\n]*)', r'print(\1)', code)
        
        # Fix integer division if needed
        # Pattern: a / b where we want integer division -> a // b
        # This is tricky to detect automatically, so we'll skip for now
        
        return code
    
    def extract_code_from_response(self, response):
        """Extract Python code from AI response with error handling"""
        try:
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
            
        except Exception as e:
            print("Code extraction error: {}".format(e))
            return ''

def show_status_dialog():
    """Show a status dialog for diagnostics"""
    try:
        message = """Revit AI Assistant - Status Report

Extension Loading: ✅ Success
PyRevit Integration: {}
AI Functions: {}
Configuration: {}

{} 

To use the full AI assistant:
1. Update API keys in config.json
2. Ensure all utility modules are present
3. Check PyRevit Console for detailed errors

Extension loaded successfully - ribbon should be visible!""".format(
            "✅ Available" if PYREVIT_AVAILABLE else "❌ Not Available",
            "✅ Available" if AI_FUNCTIONS_AVAILABLE else "❌ Not Available", 
            "✅ Available" if CONFIG_AVAILABLE else "❌ Not Available",
            "Ready for full functionality!" if (AI_FUNCTIONS_AVAILABLE and CONFIG_AVAILABLE) else "Limited functionality - check configuration."
        )
        
        forms.alert(message, title="AI Assistant Status")
        
    except Exception as e:
        print("Status dialog error: {}".format(e))

# Initialize utilities on module load
print("Loading Revit AI Assistant...")
safe_import_utilities()

# Main execution
if __name__ == "__main__":
    try:
        if not PYREVIT_AVAILABLE:
            print("PyRevit not available - cannot show UI")
        elif AI_FUNCTIONS_AVAILABLE and CONFIG_AVAILABLE:
            # Full functionality available
            try:
                ui = AssistantUI()
                ui.Show()  # Non-blocking modeless dialog - allows Revit interaction
            except Exception as e:
                print("UI creation failed: {}".format(e))
                show_status_dialog()
        else:
            # Limited functionality - show status
            show_status_dialog()
            
    except Exception as e:
        print("Main execution error: {}".format(e))
        try:
            forms.alert("Extension loaded with errors:\n{}".format(str(e)), title="Loading Warning")
        except:
            print("Even error reporting failed: {}".format(e))

# Ensure the script doesn't fail silently
print("Revit AI Assistant script loaded - Status: AI={}, Config={}, PyRevit={}".format(
    AI_FUNCTIONS_AVAILABLE, CONFIG_AVAILABLE, PYREVIT_AVAILABLE))