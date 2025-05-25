import clr
from Autodesk.Revit.DB import FilteredElementCollector, Floor, ElementId, Transform, XYZ, CopyPasteOptions, ElementTransformUtils, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, View, Level, Transaction, Grid
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

class GridIntersectionForm(Form):
    def __init__(self):
        self.Text = "Copy Elements to Grid Intersections"
        self.Width = 500
        self.Height = 400
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Grid selection (X direction)
        lblXGrids = Label()
        lblXGrids.Text = "X-Direction Grids (comma-separated):"
        lblXGrids.Location = (20, 20)
        lblXGrids.Width = 200
        self.Controls.Add(lblXGrids)
        
        self.txtXGrids = TextBox()
        self.txtXGrids.Location = (220, 20)
        self.txtXGrids.Width = 250
        self.txtXGrids.Text = ""
        self.Controls.Add(self.txtXGrids)
        
        # Grid selection (Y direction)
        lblYGrids = Label()
        lblYGrids.Text = "Y-Direction Grids (comma-separated):"
        lblYGrids.Location = (20, 60)
        lblYGrids.Width = 200
        self.Controls.Add(lblYGrids)
        
        self.txtYGrids = TextBox()
        self.txtYGrids.Location = (220, 60)
        self.txtYGrids.Width = 250
        self.txtYGrids.Text = ""
        self.Controls.Add(self.txtYGrids)
        
        # Source level selection
        lblSource = Label()
        lblSource.Text = "Source Level:"
        lblSource.Location = (20, 100)
        lblSource.Width = 100
        self.Controls.Add(lblSource)
        
        self.cmbSource = System.Windows.Forms.ComboBox()
        self.cmbSource.Location = (220, 100)
        self.cmbSource.Width = 250
        self.cmbSource.Items.AddRange(sorted([level.Name for level in levels]))
        self.cmbSource.DropDownStyle = System.Windows.Forms.ComboBox.DropDownStyle.DropDownList
        self.Controls.Add(self.cmbSource)
        
        # Element selection label
        lblSelection = Label()
        lblSelection.Text = "Elements to Copy:"
        lblSelection.Location