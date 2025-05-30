"""
Revit API - Quick Reference Guide
Essential operations at a glance
"""

# DOCUMENT ACCESS
DOCUMENT_ACCESS = {
    "Get UI Application": "UIApplication uiApp = commandData.Application;",
    "Get UI Document": "UIDocument uiDoc = uiApp.ActiveUIDocument;",
    "Get Document": "Document doc = uiDoc.Document;",
    "Get Application": "Application app = uiApp.Application;",
    "Document Title": "string title = doc.Title;",
    "Document Path": "string path = doc.PathName;",
    "Is Modified": "bool modified = doc.IsModified;",
    "Active View": "View activeView = doc.ActiveView;"
}

# TRANSACTIONS
TRANSACTIONS = {
    "Basic Transaction": """
using (Transaction trans = new Transaction(doc, "Operation"))
{
    trans.Start();
    // modifications
    trans.Commit();
}""",
    "Transaction Group": """
using (TransactionGroup group = new TransactionGroup(doc, "Multiple Ops"))
{
    group.Start();
    // multiple transactions
    group.Assimilate();
}""",
    "Sub Transaction": """
using (SubTransaction subTrans = new SubTransaction(doc))
{
    subTrans.Start();
    // temporary changes
    subTrans.RollBack(); // or Commit()
}"""
}

# ELEMENT SELECTION
SELECTION = {
    "Current Selection": "ICollection<ElementId> ids = uiDoc.Selection.GetElementIds();",
    "Pick Element": "Reference ref = selection.PickObject(ObjectType.Element);",
    "Pick Multiple": "IList<Reference> refs = selection.PickObjects(ObjectType.Element);",
    "Set Selection": "selection.SetElementIds(elementIds);",
    "Clear Selection": "selection.SetElementIds(new List<ElementId>());"
}

# ELEMENT COLLECTION
COLLECTION = {
    "All Elements": "new FilteredElementCollector(doc)",
    "By Category": "collector.OfCategory(BuiltInCategory.OST_Walls)",
    "By Class": "collector.OfClass(typeof(Wall))",
    "Element Types": "collector.WhereElementIsElementType()",
    "Element Instances": "collector.WhereElementIsNotElementType()",
    "Apply Filter": "collector.WherePasses(filter)",
    "To List": "collector.ToElements() or .ToElementIds()"
}

# ELEMENT CREATION
CREATION = {
    "Create Wall": "Wall.Create(doc, line, wallTypeId, levelId, height, offset, flip, structural)",
    "Create Floor": "Floor.Create(doc, curveArray, floorTypeId, levelId, structural)",
    "Place Family": "doc.Create.NewFamilyInstance(location, familySymbol, level, structuralType)",
    "Create Grid": "Grid.Create(doc, line)",
    "Create Level": "Level.Create(doc, elevation)",
    "Create Line": "Line.CreateBound(startPoint, endPoint)",
    "Create Arc": "Arc.Create(startPoint, endPoint, pointOnArc)"
}

# ELEMENT MODIFICATION
MODIFICATION = {
    "Move Element": "ElementTransformUtils.MoveElement(doc, elementId, translation)",
    "Copy Element": "ElementTransformUtils.CopyElement(doc, elementId, translation)",
    "Rotate Element": "ElementTransformUtils.RotateElement(doc, elementId, axis, angle)",
    "Mirror Element": "ElementTransformUtils.MirrorElement(doc, elementId, plane)",
    "Delete Element": "doc.Delete(elementId)",
    "Delete Multiple": "doc.Delete(elementIds)"
}

# PARAMETERS
PARAMETERS = {
    "Get Parameter": "Parameter param = element.get_Parameter(BuiltInParameter.PARAM_NAME);",
    "Set String": "param.Set(\"string value\");",
    "Set Double": "param.Set(doubleValue);",
    "Set Integer": "param.Set(intValue);",
    "Set ElementId": "param.Set(elementId);",
    "Get Value": "object value = param.AsString() / .AsDouble() / .AsInteger() / .AsElementId();",
    "Is Read Only": "bool readOnly = param.IsReadOnly;"
}

# GEOMETRY
GEOMETRY = {
    "Point": "XYZ point = new XYZ(x, y, z);",
    "Vector": "XYZ vector = point2.Subtract(point1);",
    "Distance": "double dist = point1.DistanceTo(point2);",
    "Unit Vector": "XYZ unit = vector.Normalize();",
    "Dot Product": "double dot = vector1.DotProduct(vector2);",
    "Cross Product": "XYZ cross = vector1.CrossProduct(vector2);",
    "Transform": "Transform transform = Transform.CreateTranslation(vector);"
}

# COMMON CATEGORIES
CATEGORIES = {
    "Walls": "BuiltInCategory.OST_Walls",
    "Doors": "BuiltInCategory.OST_Doors",
    "Windows": "BuiltInCategory.OST_Windows",
    "Floors": "BuiltInCategory.OST_Floors",
    "Roofs": "BuiltInCategory.OST_Roofs",
    "Ceilings": "BuiltInCategory.OST_Ceilings",
    "Columns": "BuiltInCategory.OST_Columns",
    "Beams": "BuiltInCategory.OST_StructuralFraming",
    "Furniture": "BuiltInCategory.OST_Furniture",
    "Generic Models": "BuiltInCategory.OST_GenericModel"
}

# COMMON WORKFLOWS
WORKFLOWS = {
    "Basic Command Structure": """
public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
{
    UIApplication uiApp = commandData.Application;
    UIDocument uiDoc = uiApp.ActiveUIDocument;
    Document doc = uiDoc.Document;
    
    using (Transaction trans = new Transaction(doc, "Command"))
    {
        trans.Start();
        try
        {
            // Your operations here
            trans.Commit();
            return Result.Succeeded;
        }
        catch (Exception ex)
        {
            trans.RollBack();
            message = ex.Message;
            return Result.Failed;
        }
    }
}""",
    "Selection and Processing": """
Selection sel = uiDoc.Selection;
ICollection<ElementId> ids = sel.GetElementIds();
if (ids.Count == 0)
{
    Reference ref = sel.PickObject(ObjectType.Element);
    ids = new List<ElementId> { ref.ElementId };
}

using (Transaction trans = new Transaction(doc, "Process"))
{
    trans.Start();
    foreach (ElementId id in ids)
    {
        Element elem = doc.GetElement(id);
        ProcessElement(elem);
    }
    trans.Commit();
}"""
}
