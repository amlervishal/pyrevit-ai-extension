import clr
from Autodesk.Revit.DB import FilteredElementCollector, Floor, ElementId, Transform, XYZ, CopyPasteOptions, ElementTransformUtils, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, View, Level, Transaction
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, TextBox, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, NumericUpDown

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

class LevelSelectionForm(Form):
    def __init__(self, levels):
        self.Text = "Copy Elements with Offset"
        self.Width = 500
        self.Height = 500
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        self.level_names = sorted([level.Name for level in levels])
        
        # Source level selection
        lblSource = Label()
        lblSource.Text = "Source Level:"
        lblSource.Location = (20, 20)
        lblSource.Width = 100
        self.Controls.Add(lblSource)
        
        self.cmbSource = System.Windows.Forms.ComboBox()
        self.cmbSource.Location = (130, 20)
        self.cmbSource.Width = 250
        self.cmbSource.Items.AddRange(self.level_names)
        self.cmbSource.DropDownStyle = System.Windows.Forms.ComboBox.DropDownStyle.DropDownList
        self.Controls.Add(self.cmbSource)
        
        # Target levels selection
        lblTarget = Label()
        lblTarget.Text = "Target Levels:"
        lblTarget.Location = (20, 60)
        lblTarget.Width = 100
        self.Controls.Add(lblTarget)
        
        self.chkTargets = CheckedListBox()
        self.chkTargets.Location = (130, 60)
        self.chkTargets.Width = 250
        self.chkTargets.Height = 150
        self.chkTargets.Items.AddRange(self.level_names)
        self.Controls.Add(self.chkTargets)
        
        # Target levels text input (alternative)
        lblTargetText = Label()
        lblTargetText.Text = "Or enter level names (comma-separated):"
        lblTargetText.Location = (20, 220)
        lblTargetText.Width = 220
        self.Controls.Add(lblTargetText)
        
        self.txtTargetLevels = TextBox()
        self.txtTargetLevels.Location = (230, 220)
        self.txtTargetLevels.Width = 250
        self.txtTargetLevels.Text = ""
        self.Controls.Add(self.txtTargetLevels)
        
        # Offset inputs