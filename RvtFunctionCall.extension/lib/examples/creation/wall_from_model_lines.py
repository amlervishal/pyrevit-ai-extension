import clr
import System

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

# Get the current document and create a transaction
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collect all model lines in the document
collector = FilteredElementCollector(doc).OfClass(CurveElement)
model_lines = [elem for elem in collector if elem.Category.Name == "Model Lines"]

# Get the default wall type
wall_types = FilteredElementCollector(doc).OfClass(WallType)
default_wall_type = wall_types.FirstElement()

# Start a transaction
transaction = Transaction(doc, "Create Walls from Model Lines")
transaction.Start()

try:
    # Create walls from each model line
    for line in model_lines:
        curve = line.GeometryCurve
        
        # Skip non-linear curves (can be expanded to handle arcs if needed)
        if not isinstance(curve, Line):
            continue
            
        # Create wall by curve
        level = FilteredElementCollector(doc).OfClass(Level).FirstElement()
        wall_height = 10.0  # Default height in feet
        
        # Create the wall
        Wall.Create(
            doc,
            curve,
            default_wall_type.Id,
            level.Id,
            wall_height,
            0.0,  # Offset
            False,  # Flip
            True   # Structural
        )
    
    transaction.Commit()
    TaskDialog.Show("Success", f"Created {len(model_lines)} walls from model lines")
    
except Exception as e:
    transaction.RollBack()
    TaskDialog.Show("Error", f"Failed to create walls: {str(e)}")