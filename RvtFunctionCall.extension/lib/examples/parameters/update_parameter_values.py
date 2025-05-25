"""
Update Parameter Values
Update parameter values for selected elements with various filtering options.
"""
import clr
from Autodesk.Revit.DB import FilteredElementCollector, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, Level, Transaction, FamilyInstance, ElementId, ElementParameterFilter, ParameterValueProvider, FilterStringRule, BuiltInParameter, Parameter, StorageType, FilterNumericRuleEvaluator, FilterDoubleRule, FilterIntegerRule, FilterRule
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, Panel, TextBox, ComboBox, GroupBox, RadioButton, NumericUpDown, MessageBox

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

class ParameterUpdateForm(Form):
    def __init__(self):
        self.InitializeComponent()
        self.selected_elements = None
        self.family_names = []
        
    def InitializeComponent(self):
        self.Text = "Update Parameter Values"
        self.Width = 500
        self.Height = 650
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Create family type selection
        self.lblFamilyTypes = Label()
        self.lblFamilyTypes.Text = "Enter Family Names (one per line, optional):"
        self.lblFamilyTypes.Location = System.Drawing.Point(20, 20)
        self.lblFamilyTypes.AutoSize = True
        
        self.txtFamilyNames = TextBox()
        self.txtFamilyNames.Multiline = True
        self.txtFamilyNames.Location = System.Drawing.Point(20, 45)
        self.txtFamilyNames.Size = System.Drawing.Size(440, 120)
        self.txtFamilyNames.ScrollBars = System.Windows.Forms.ScrollBars.Vertical
        
        # Level selection
        self.lblLevel = Label()
        self.lblLevel.Text = "Filter by Level (optional):"
        self.lblLevel.Location = System.Drawing.Point(20, 175)
        self.lblLevel.AutoSize = True
        
        self.cboLevel = ComboBox()
        self.cboLevel.Location = System.Drawing.Point(20, 200)
        self.cboLevel.Size = System.Drawing.Size(200, 21)
        self.cboLevel.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        self.cboLevel.Items.Add("All Levels")
        for level in FilteredElementCollector(doc).OfClass(Level).ToElements():
            self.cboLevel.Items.Add(level.Name)
        self.cboLevel.SelectedIndex = 0
        
        # Parameter name
        self.lblParamName = Label()
        self.lblParamName.Text = "Parameter Name:"
        self.lblParamName.Location = System.Drawing.Point(20, 240)
        self.lblParamName.AutoSize = True
        
        self.txtParamName = TextBox()
        self.txtParamName.Location = System.Drawing.Point(20, 265)
        self.txtParamName.Size = System.Drawing.Size(440, 21)
        
        # Parameter value
        self.lblParamValue = Label()
        self.lblParamValue.Text = "New Parameter Value:"
        self.lblParamValue.Location = System.Drawing.Point(20, 300)
        self.lblParamValue.AutoSize = True
        
        self.txtParamValue = TextBox()
        self.txtParamValue.Location = System.Drawing.Point(20, 325)
        self.txtParamValue.Size = System.Drawing.Size(440, 21)
        
        # Preview checkbox
        self.chkPreview = System.Windows.Forms.CheckBox()
        self.chkPreview.Text = "Preview elements before updating"
        self.chkPreview.Location = System.Drawing.Point(20, 360)
        self.chkPreview.Size = System.Drawing.Size(250, 20)
        self.chkPreview.Checked = True
        
        # Use selection checkbox
        self.chkUseSelection = System.Windows.Forms.CheckBox()
        self.chkUseSelection.Text = "Use current selection (ignore family filter)"
        self.chkUseSelection.Location = System.Drawing.Point(20, 390)
        self.chkUseSelection.Size = System.Drawing.Size(300, 20)
        
        # Buttons
        self.btnUpdate = Button()
        self.btnUpdate.Text = "Update Parameters"
        self.btnUpdate.Location = System.Drawing.Point(20, 430)
        self.btnUpdate.Size = System.Drawing.Size(150, 30)
        self.btnUpdate.Click += self.UpdateParameters
        
        self.btnCancel = Button()
        self.btnCancel.Text = "Cancel"
        self.btnCancel.Location = System.Drawing.Point(180, 430)
        self.btnCancel.Size = System.Drawing.Size(150, 30)
        self.btnCancel.Click += self.CancelForm
        
        # Add controls to form
        self.Controls.Add(self.lblFamilyTypes)
        self.Controls.Add(self.txtFamilyNames)
        self.Controls.Add(self.lblLevel)
        self.Controls.Add(self.cboLevel)
        self.Controls.Add(self.lblParamName)
        self.Controls.Add(self.txtParamName)
        self.Controls.Add(self.lblParamValue)
        self.Controls.Add(self.txtParamValue)
        self.Controls.Add(self.chkPreview)
        self.Controls.Add(self.chkUseSelection)
        self.Controls.Add(self.btnUpdate)
        self.Controls.Add(self.btnCancel)
        
    def UpdateParameters(self, sender, e):
        parameter_name = self.txtParamName.Text.strip()
        parameter_value = self.txtParamValue.Text.strip()
        
        if not parameter_name:
            MessageBox.Show("Please enter a parameter name", "Input Required")
            return
        
        if not parameter_value:
            MessageBox.Show("Please enter a parameter value", "Input Required") 
            return
        
        # Get elements to update
        elements_to_update = []
        
        if self.chkUseSelection.Checked:
            # Use current selection
            selected_ids = uidoc.Selection.GetElementIds()
            if not selected_ids:
                MessageBox.Show("No elements are currently selected", "Selection Required")
                return
            
            for elem_id in selected_ids:
                element = doc.GetElement(elem_id)
                if element:
                    elements_to_update.append(element)
        else:
            # Filter by family names and level
            self.family_names = [name.strip() for name in self.txtFamilyNames.Text.Split('\n') if name.strip()]
            
            # Get all family instances
            collector = FilteredElementCollector(doc).OfClass(FamilyInstance)
            
            # Filter by level if specified
            if self.cboLevel.SelectedIndex > 0:
                level_name = self.cboLevel.SelectedItem
                levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
                target_level = None
                for level in levels:
                    if level.Name == level_name:
                        target_level = level
                        break
                
                if target_level:
                    level_filter = ElementLevelFilter(target_level.Id)
                    collector = collector.WherePasses(level_filter)
            
            # Filter by family names if specified
            if self.family_names:
                for element in collector:
                    try:
                        if element.Symbol and element.Symbol.Family:
                            family_name = element.Symbol.Family.Name
                            if any(fn.lower() in family_name.lower() or family_name.lower() in fn.lower() 
                                   for fn in self.family_names):
                                elements_to_update.append(element)
                    except:
                        continue
            else:
                # Use all family instances if no family filter
                elements_to_update = list(collector)
        
        if not elements_to_update:
            MessageBox.Show("No elements found to update", "No Elements")
            return
        
        # Filter elements that have the specified parameter
        valid_elements = []
        for element in elements_to_update:
            try:
                param = element.LookupParameter(parameter_name)
                if param and not param.IsReadOnly:
                    valid_elements.append(element)
            except:
                continue
        
        if not valid_elements:
            MessageBox.Show("No elements found with the parameter '{}'".format(parameter_name), "Parameter Not Found")
            return
        
        # Preview if requested
        if self.chkPreview.Checked:
            message = "Found {} elements with parameter '{}'.\n\nProceed with update?".format(
                len(valid_elements), parameter_name)
            
            result = MessageBox.Show(message, "Confirm Update", 
                                   System.Windows.Forms.MessageBoxButtons.YesNo,
                                   System.Windows.Forms.MessageBoxIcon.Question)
            
            if result != System.Windows.Forms.DialogResult.Yes:
                return
        
        # Update parameters
        updated_count = 0
        
        with Transaction(doc, "Update Parameter Values") as t:
            t.Start()
            
            for element in valid_elements:
                try:
                    param = element.LookupParameter(parameter_name)
                    if param and not param.IsReadOnly:
                        # Set parameter value based on storage type
                        if param.StorageType == StorageType.String:
                            param.Set(parameter_value)
                            updated_count += 1
                        elif param.StorageType == StorageType.Double:
                            try:
                                double_value = float(parameter_value)
                                param.Set(double_value)
                                updated_count += 1
                            except:
                                continue
                        elif param.StorageType == StorageType.Integer:
                            try:
                                int_value = int(parameter_value)
                                param.Set(int_value)
                                updated_count += 1
                            except:
                                continue
                except Exception:
                    continue
            
            t.Commit()
        
        MessageBox.Show("Successfully updated {} elements".format(updated_count), "Update Complete")
        self.DialogResult = DialogResult.OK
        self.Close()
    
    def CancelForm(self, sender, e):
        self.DialogResult = DialogResult.Cancel
        self.Close()

# Execute the form
form = ParameterUpdateForm()
form.ShowDialog()
