"""
Select Elements by Family Name
Allows users to select elements by specifying family names and optionally filter by level.
"""
import clr
from Autodesk.Revit.DB import FilteredElementCollector, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, Level, Transaction, FamilyInstance, ElementId, ElementParameterFilter, ParameterValueProvider, FilterStringRule, BuiltInParameter
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, Panel, TextBox, ComboBox, GroupBox, RadioButton, NumericUpDown, MessageBox

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

class SelectByFamilyTypesForm(Form):
    def __init__(self):
        self.InitializeComponent()
        self.selected_elements = None
        self.family_names = []
        
    def InitializeComponent(self):
        self.Text = "Select by Family Types"
        self.Width = 500
        self.Height = 600
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Create family type selection
        self.lblFamilyTypes = Label()
        self.lblFamilyTypes.Text = "Enter Family Names (one per line):"
        self.lblFamilyTypes.Location = System.Drawing.Point(20, 20)
        self.lblFamilyTypes.AutoSize = True
        
        self.txtFamilyNames = TextBox()
        self.txtFamilyNames.Multiline = True
        self.txtFamilyNames.Location = System.Drawing.Point(20, 45)
        self.txtFamilyNames.Size = System.Drawing.Size(440, 200)
        self.txtFamilyNames.ScrollBars = System.Windows.Forms.ScrollBars.Vertical
        
        # Level selection
        self.lblLevel = Label()
        self.lblLevel.Text = "Filter by Level (optional):"
        self.lblLevel.Location = System.Drawing.Point(20, 255)
        self.lblLevel.AutoSize = True
        
        self.cboLevel = ComboBox()
        self.cboLevel.Location = System.Drawing.Point(20, 280)
        self.cboLevel.Size = System.Drawing.Size(200, 21)
        self.cboLevel.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        self.cboLevel.Items.Add("All Levels")
        for level in FilteredElementCollector(doc).OfClass(Level).ToElements():
            self.cboLevel.Items.Add(level.Name)
        self.cboLevel.SelectedIndex = 0
        
        # Buttons
        self.btnSelect = Button()
        self.btnSelect.Text = "Select Elements"
        self.btnSelect.Location = System.Drawing.Point(20, 320)
        self.btnSelect.Size = System.Drawing.Size(150, 30)
        self.btnSelect.Click += self.SelectElements
        
        self.btnCancel = Button()
        self.btnCancel.Text = "Cancel"
        self.btnCancel.Location = System.Drawing.Point(180, 320)
        self.btnCancel.Size = System.Drawing.Size(150, 30)
        self.btnCancel.Click += self.CancelForm
        
        # Add controls to form
        self.Controls.Add(self.lblFamilyTypes)
        self.Controls.Add(self.txtFamilyNames)
        self.Controls.Add(self.lblLevel)
        self.Controls.Add(self.cboLevel)
        self.Controls.Add(self.btnSelect)
        self.Controls.Add(self.btnCancel)
        
    def SelectElements(self, sender, e):
        # Get family names from textbox
        self.family_names = [name.strip() for name in self.txtFamilyNames.Text.Split('\n') if name.strip()]
        
        if not self.family_names:
            MessageBox.Show("Please enter at least one family name", "Input Required")
            return
        
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
        
        # Filter by family names
        matching_elements = []
        for element in collector:
            try:
                if element.Symbol and element.Symbol.Family:
                    family_name = element.Symbol.Family.Name
                    if any(fn.lower() in family_name.lower() or family_name.lower() in fn.lower() 
                           for fn in self.family_names):
                        matching_elements.append(element)
            except:
                continue
        
        if matching_elements:
            # Select the elements
            element_ids = List[ElementId]([elem.Id for elem in matching_elements])
            uidoc.Selection.SetElementIds(element_ids)
            MessageBox.Show("Selected {} elements".format(len(matching_elements)), "Selection Complete")
        else:
            MessageBox.Show("No elements found matching the specified family names", "No Results")
        
        self.DialogResult = DialogResult.OK
        self.Close()
    
    def CancelForm(self, sender, e):
        self.DialogResult = DialogResult.Cancel
        self.Close()

# Execute the form
form = SelectByFamilyTypesForm()
form.ShowDialog()
