import clr
from Autodesk.Revit.DB import FilteredElementCollector, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, Level, ParameterValueProvider, ElementId, FilterStringRule, FilterNumericRule, FilterDoubleRule, FilterIntegerRule, ElementParameterFilter, ParameterFilterRuleFactory, CurveLoop, XYZ, BoundingBoxIntersectsFilter, Outline, Transaction, BuiltInParameter
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, Panel, TextBox, ComboBox, GroupBox, RadioButton, NumericUpDown, MessageBox

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get all levels in the document
levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
level_dict = {level.Name: level for level in levels}

# Get all major categories to consider
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

category_names = {
    BuiltInCategory.OST_Walls: "Walls",
    BuiltInCategory.OST_Floors: "Floors",
    BuiltInCategory.OST_StructuralFraming: "Structural Framing",
    BuiltInCategory.OST_Furniture: "Furniture",
    BuiltInCategory.OST_Doors: "Doors",
    BuiltInCategory.OST_Windows: "Windows",
    BuiltInCategory.OST_GenericModel: "Generic Models",
    BuiltInCategory.OST_ElectricalFixtures: "Electrical Fixtures",
    BuiltInCategory.OST_ElectricalEquipment: "Electrical Equipment",
    BuiltInCategory.OST_MechanicalEquipment: "Mechanical Equipment",
    BuiltInCategory.OST_PlumbingFixtures: "Plumbing Fixtures",
    BuiltInCategory.OST_Casework: "Casework",
    BuiltInCategory.OST_Columns: "Columns",
    BuiltInCategory.OST_Ceilings: "Ceilings"
}

class SelectByBoundaryForm(Form):
    def __init__(self):
        self.InitializeComponent()
        self.selected_elements = None
        self.boundary_points = []
    
    def InitializeComponent(self):
        self.Text = "Select Elements Within Boundary"
        self.Width = 500
        self.Height = 700
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Create category selection
        self.lblCategories = Label()
        self.lblCategories.Text = "Select Categories:"
        self.lblCategories.Location = System.Drawing.Point(20, 20)
        self.lblCategories.AutoSize = True
        
        self.checkedListCategories = CheckedListBox()
        self.checkedListCategories.Location = System.Drawing.Point(20, 45)
        self.checkedListCategories.Size = System.Drawing.Size(200,