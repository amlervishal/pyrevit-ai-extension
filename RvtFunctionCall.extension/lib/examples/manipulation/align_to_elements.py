import clr
from Autodesk.Revit.DB import FilteredElementCollector, Floor, ElementId, Transform, XYZ, CopyPasteOptions, ElementTransformUtils, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, View, Level, Transaction, Grid, Math, BoundingBoxXYZ, Line, Reference
import System
from math import sin, cos, radians
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, TextBox, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, NumericUpDown, RadioButton, ComboBox, Panel, ControlCollection, ListBox, SelectionMode

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get all levels in the document
levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
level_dict = {level.Name: level for level in levels}

# Get all major categories to consider for moving
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

def get_all_elements():
    """Get all elements in the document that could be moved or serve as targets"""
    all_elements = []
    for category in categories:
        filter = ElementCategoryFilter(category)
        elements = FilteredElementCollector(doc).WherePasses(filter).WhereElementIsNotElementType().ToElements()
        all_elements.extend(elements)
    return all_elements

def get_element_info(element):
    """Returns a string with element information"""
    try:
        category = element.Category.Name if element.Category else "No Category"
        element_id = element.Id.IntegerValue
        element_name = element.Name if hasattr(element, "Name") and element.Name else f"ID: {element_id}"
        return f"{category}: {element_name} (ID: {element_id})"
    except:
        return f"Element ID: {element.Id.IntegerValue}"

def get_element_centroid(element):
    """Get the centroid of an element"""
    try:
        bbox = element.get_BoundingBox(None)
        if bbox:
            return (bbox.Min + bbox.Max) / 2
        
        # If bounding box fails, try location property
        loc = element.Location
        if loc:
            if isinstance(loc, Line):
                return (loc.GetEndPoint(0) + loc.GetEndPoint(1)) / 2
            try:
                return loc.Point
            except:
                pass
    except:
        pass
    
    return None

class AlignElementsForm(Form):
    def __init__(self):
        self.Text = "Align Elements to Target Elements"
        self.Width = 700
        self.Height = 600
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # All elements in the model
        self.all_elements = get_all_elements()
        
        # Elements to move
        lblElementsToMove = Label()
        lblElementsToMove.Text = "Elements to Move:"
        lblElementsToMove.Location = (20, 20)
        lblElementsToMove.Width = 200
        self.Controls.Add(lbl