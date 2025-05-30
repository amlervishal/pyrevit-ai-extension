"""
Revit API - Built-in Parameters and Elements Reference
Essential built-in parameters and elements used in regular drawing workflows
"""

class BuiltInParametersAPI:
    """
    Built-in Parameters - Essential parameters available in all Revit elements
    These are the most commonly used parameters in drawing workflows
    """

# ELEMENT IDENTIFICATION PARAMETERS
ELEMENT_ID_PARAMETERS = {
    'ALL_MODEL_MARK': 'Mark - Unique identifier for element',
    'ALL_MODEL_TYPE_MARK': 'Type Mark - Type identifier',
    'ALL_MODEL_INSTANCE_COMMENTS': 'Comments - Instance comments',
    'ALL_MODEL_TYPE_COMMENTS': 'Type Comments - Type comments',
    'ELEM_FAMILY_PARAM': 'Family - Family name',
    'ELEM_TYPE_PARAM': 'Type - Type name',
    'ELEM_FAMILY_AND_TYPE_PARAM': 'Family and Type - Combined name'
}

# DIMENSIONAL PARAMETERS
DIMENSIONAL_PARAMETERS = {
    # Length/Distance
    'CURVE_ELEM_LENGTH': 'Length - Element length',
    'WALL_USER_HEIGHT_PARAM': 'Unconnected Height - Wall height',
    'WALL_BASE_OFFSET': 'Base Offset - Wall base offset',
    'WALL_TOP_OFFSET': 'Top Offset - Wall top offset',
    
    # Area/Volume
    'HOST_AREA_COMPUTED': 'Area - Computed area',
    'HOST_VOLUME_COMPUTED': 'Volume - Computed volume',
    'HOST_PERIMETER_COMPUTED': 'Perimeter - Computed perimeter',
    
    # Thickness
    'WALL_ATTR_WIDTH_PARAM': 'Width - Wall thickness',
    'FLOOR_ATTR_THICKNESS_PARAM': 'Thickness - Floor thickness',
    'ROOF_ATTR_THICKNESS_PARAM': 'Thickness - Roof thickness'
}

# ROOM AND SPATIAL PARAMETERS
ROOM_SPACE_PARAMETERS = {
    'ROOM_NUMBER': 'Number - Room number',
    'ROOM_NAME': 'Name - Room name', 
    'ROOM_AREA': 'Area - Room area',
    'ROOM_VOLUME': 'Volume - Room volume',
    'ROOM_PERIMETER': 'Perimeter - Room perimeter',
    'ROOM_HEIGHT': 'Height - Room height',
    'ROOM_COMMENTS': 'Comments - Room comments',
    'ROOM_DEPARTMENT': 'Department - Room department',
    'ROOM_OCCUPANCY': 'Occupancy - Occupancy count',
    'ROOM_PHASE': 'Phase Created - Room phase',
    
    # Area parameters
    'AREA_AREA': 'Area - Area value',
    'AREA_PERIMETER': 'Perimeter - Area perimeter',
    'AREA_NUMBER': 'Number - Area number',
    'AREA_NAME': 'Name - Area name'
}

# COMMONLY USED BUILT-IN CATEGORIES
BUILT_IN_CATEGORIES = {
    # Basic Building Elements
    'OST_Walls': 'Walls',
    'OST_Floors': 'Floors', 
    'OST_Roofs': 'Roofs',
    'OST_Ceilings': 'Ceilings',
    'OST_Columns': 'Columns',
    'OST_StructuralFraming': 'Structural Framing (Beams)',
    'OST_StructuralFoundation': 'Structural Foundations',
    'OST_Stairs': 'Stairs',
    'OST_Ramps': 'Ramps',
    
    # Openings
    'OST_Doors': 'Doors',
    'OST_Windows': 'Windows',
    'OST_CurtainWallPanels': 'Curtain Panels',
    'OST_CurtainWallMullions': 'Curtain Wall Mullions',
    
    # MEP Elements
    'OST_DuctSystems': 'Duct Systems',
    'OST_PipingSystems': 'Piping Systems',
    'OST_ElectricalEquipment': 'Electrical Equipment',
    'OST_MechanicalEquipment': 'Mechanical Equipment',
    'OST_PlumbingFixtures': 'Plumbing Fixtures',
    'OST_LightingFixtures': 'Lighting Fixtures',
    
    # Space Elements
    'OST_Rooms': 'Rooms',
    'OST_Areas': 'Areas', 
    'OST_MEPSpaces': 'Spaces',
    
    # Model Elements
    'OST_GenericModel': 'Generic Models',
    'OST_Furniture': 'Furniture',
    'OST_FurnitureSystems': 'Furniture Systems',
    'OST_Casework': 'Casework',
    'OST_SpecialtyEquipment': 'Specialty Equipment',
    
    # Datum Elements
    'OST_Levels': 'Levels',
    'OST_Grids': 'Grids', 
    'OST_ReferencePlanes': 'Reference Planes',
    
    # Views and Sheets
    'OST_Views': 'Views',
    'OST_Sheets': 'Sheets',
    'OST_Schedules': 'Schedules',
    'OST_Viewports': 'Viewports'
}

# PARAMETER QUICK REFERENCE
PARAMETER_QUICK_REFERENCE = {
    "Get Parameter": "element.get_Parameter(BuiltInParameter.PARAM_NAME)",
    "Set String Parameter": "parameter.Set('string_value')",
    "Set Double Parameter": "parameter.Set(double_value)",
    "Set Integer Parameter": "parameter.Set(int_value)",
    "Set ElementId Parameter": "parameter.Set(elementId)",
    "Get String Value": "parameter.AsString()",
    "Get Double Value": "parameter.AsDouble()",
    "Get Integer Value": "parameter.AsInteger()",
    "Get ElementId Value": "parameter.AsElementId()",
    "Check if Has Value": "parameter.HasValue",
    "Check if Read Only": "parameter.IsReadOnly"
}
