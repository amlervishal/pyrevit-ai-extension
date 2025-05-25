import clr
from Autodesk.Revit.DB import FilteredElementCollector, Floor, ElementId, Transform, XYZ, CopyPasteOptions, ElementTransformUtils, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, View, Level, Transaction, Grid
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, TextBox, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, NumericUpDown, RadioButton, ComboBox, Panel, ControlCollection

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get all levels in the document
levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
level_dict = {level.Name: level for level in levels}

# Get all major categories to consider for copying
categories = [
    BuiltInCategory.OST_Walls,
    BuiltInCategory.OST_Floors,
    BuiltInCategory.OST_StructuralFraming,
    BuiltInCategory.OST_Furniture,
    BuiltInCategory.OST_Doors,
    BuiltInCategory.OST_Windows,
    BuiltInCategory.OST_GenericModel,
    BuiltInCategory.OST_ElectricalFixtures,
    BuiltInCategory.OST_ElectricalEquipment,
    BuiltInCategory.OST_MechanicalEquipment,
    BuiltInCategory.OST_PlumbingFixtures,
    BuiltInCategory.OST_Casework,
    BuiltInCategory.OST_Columns,
    BuiltInCategory.OST_Ceilings
]

class CopyElementsForm(Form):
    def __init__(self):
        self.Text = "Copy Elements with Spacing"
        self.Width = 500
        self.Height = 500
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Category selection
        lblCategories = Label()
        lblCategories.Text = "Categories to Copy:"
        lblCategories.Location = (20, 20)
        lblCategories.Width = 200
        self.Controls.Add(lblCategories)
        
        self.chkCategories = CheckedListBox()
        self.chkCategories.Location = (20, 50)
        self.chkCategories.Width = 450
        self.chkCategories.Height = 150
        
        # Add categories to the checklist
        for category in categories:
            cat_name = System.Enum.ToObject(BuiltInCategory, category).ToString().Replace("OST_", "")
            self.chkCategories.Items.Add(cat_name, CheckState.Checked)
            
        self.Controls.Add(self.chkCategories)
        
        # Source level selection
        lblSource = Label()
        lblSource.Text = "Source Level:"
        lblSource.Location = (20, 210)
        lblSource.Width = 100
        self.Controls.Add(lblSource)
        
        self.cmbSource = ComboBox()
        self.cmbSource.Location = (150, 210)
        self.cmbSource.Width = 320
        self.cmbSource.Items.AddRange(sorted([level.Name for level in levels]))
        self.cmbSource.DropDownStyle = ComboBox.DropDownStyle.DropDownList
        if self.cmbSource.Items.Count > 0:
            self.cmbSource.SelectedIndex = 0
        self.Controls.Add(self.cmbSource)
        
        # Count
        lblCount = Label()
        lblCount.Text = "Number of Copies:"
        lblCount.Location = (20, 250)
        lblCount.Width = 120
        self.Controls.Add(lblCount)
        
        self.nudCount = NumericUpDown()
        self.nudCount.Location = (150, 250)
        self.nudCount.