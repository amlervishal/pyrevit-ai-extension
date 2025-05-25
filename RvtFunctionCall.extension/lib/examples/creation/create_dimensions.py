import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collect all walls, doors, and windows
walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
windows = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()

t = Transaction(doc, "Create Dimensions")
t.Start()

# Create dimensions for walls
for wall in walls:
    loc = wall.Location
    if isinstance(loc, LocationCurve):
        curve = loc.Curve
        p1 = curve.GetEndPoint(0)
        p2 = curve.GetEndPoint(1)
        line = Line.CreateBound(p1, p2)
        ref_array = ReferenceArray()
        ref_array.Append(wall.References[0])
        ref_array.Append(wall.References[1])
        try:
            dim = doc.Create.NewDimension(doc.ActiveView, line, ref_array)
        except:
            continue

# Create dimensions for doors and windows
for element in list(doors) + list(windows):
    try:
        host = element.Host
        if isinstance(host, Wall):
            face_ref = host.References[0]
            opening_refs = element.References
            ref_array = ReferenceArray()
            ref_array.Append(face_ref)
            ref_array.Append(opening_refs[0])
            
            bb = element.get_BoundingBox(doc.ActiveView)
            p1 = XYZ(bb.Min.X, bb.Min.Y, bb.Min.Z)
            p2 = XYZ(bb.Max.X, bb.Min.Y, bb.Min.Z)
            line = Line.CreateBound(p1, p2)
            
            dim = doc.Create.NewDimension(doc.ActiveView, line, ref_array)
    except:
        continue

t.Commit()