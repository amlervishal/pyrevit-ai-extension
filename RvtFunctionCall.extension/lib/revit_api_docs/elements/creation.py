"""
Revit API - Element Creation Reference
Essential methods for creating different types of elements.
"""

class ElementCreationAPI:
    """
    Element Creation Methods
    All element creation must occur within a Transaction.
    """
    
    # BASIC BUILDING ELEMENTS
    BUILDING_ELEMENTS = {
        'Wall.Create()': {
            'signature': 'Wall.Create(Document, Line, ElementId, ElementId, double, double, bool, bool)',
            'parameters': [
                'Document doc - The document',
                'Line locationLine - The location line for the wall',
                'ElementId wallTypeId - Wall type ElementId',
                'ElementId levelId - Level ElementId',
                'double height - Wall height',
                'double offset - Offset from level',
                'bool flip - Whether to flip the wall',
                'bool structural - Whether wall is structural'
            ],
            'returns': 'Wall - The created wall element',
            'example': '''
Line wallLine = Line.CreateBound(new XYZ(0, 0, 0), new XYZ(20, 0, 0));
Wall wall = Wall.Create(doc, wallLine, wallTypeId, levelId, 10, 0, false, false);
            '''
        },
        
        'Floor.Create()': {
            'signature': 'Floor.Create(Document, CurveArray, ElementId, ElementId, bool, XYZ, double)',
            'parameters': [
                'Document doc - The document',
                'CurveArray profile - Floor boundary curves',
                'ElementId floorTypeId - Floor type ElementId',
                'ElementId levelId - Level ElementId',
                'bool structural - Whether floor is structural',
                'XYZ normal - Normal vector (optional)',
                'double slope - Slope angle (optional)'
            ],
            'returns': 'Floor - The created floor element',
            'example': '''
CurveArray floorProfile = new CurveArray();
floorProfile.Append(Line.CreateBound(new XYZ(0, 0, 0), new XYZ(10, 0, 0)));
floorProfile.Append(Line.CreateBound(new XYZ(10, 0, 0), new XYZ(10, 10, 0)));
floorProfile.Append(Line.CreateBound(new XYZ(10, 10, 0), new XYZ(0, 10, 0)));
floorProfile.Append(Line.CreateBound(new XYZ(0, 10, 0), new XYZ(0, 0, 0)));
Floor floor = Floor.Create(doc, floorProfile, floorTypeId, levelId, false);
            '''
        }
    }

# QUICK REFERENCE
QUICK_REFERENCE = {
    "Create Wall": "Wall.Create(doc, line, wallTypeId, levelId, height, offset, flip, structural)",
    "Create Floor": "Floor.Create(doc, curveArray, floorTypeId, levelId, structural)",
    "Place Family": "doc.Create.NewFamilyInstance(location, familySymbol, level, structuralType)",
    "Move Element": "ElementTransformUtils.MoveElement(doc, elementId, translation)",
    "Copy Element": "ElementTransformUtils.CopyElement(doc, elementId, translation)",
    "Rotate Element": "ElementTransformUtils.RotateElement(doc, elementId, axis, angle)",
    "Mirror Element": "ElementTransformUtils.MirrorElement(doc, elementId, plane)",
    "Set Parameter": "parameter.Set(value)",
    "Get Parameter": "element.get_Parameter(BuiltInParameter.PARAM_NAME)",
    "Create Line": "Line.CreateBound(startPoint, endPoint)",
    "Create Arc": "Arc.Create(startPoint, endPoint, pointOnArc)"
}
