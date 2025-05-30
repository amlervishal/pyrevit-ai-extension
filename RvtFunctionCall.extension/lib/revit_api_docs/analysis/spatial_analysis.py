"""
Revit API - Analysis Tools Reference
Area calculation, quantities, spatial elements, and room/space analysis
"""

class AnalysisToolsAPI:
    """
    Analysis and quantification tools in Revit API
    Essential for area takeoffs, room analysis, and quantity calculations
    """

# SPATIAL ELEMENTS - Core Analysis Classes
class SpatialElementsAPI:
    """
    Spatial Elements - Rooms, Areas, and Spaces
    Base classes for all spatial analysis in Revit
    """
    
    SPATIAL_ELEMENTS = {
        'Room': {
            'description': 'Represents a room element in the model',
            'namespace': 'Autodesk.Revit.DB.Architecture',
            'key_properties': [
                'Area - Gets room area in square feet',
                'Volume - Gets room volume in cubic feet', 
                'Perimeter - Gets room perimeter in feet',
                'UnboundedHeight - Gets height of room',
                'Number - Gets/sets room number',
                'Name - Gets/sets room name',
                'Level - Gets associated level',
                'Phase - Gets/sets room phase'
            ],
            'key_methods': [
                'GetBoundarySegments() - Gets room boundary segments',
                'GetRoomCalculationPoint() - Gets calculation point',
                'SetRoomCalculationPoint() - Sets calculation point'
            ]
        },
        
        'Area': {
            'description': 'Represents an area element for area plans',
            'namespace': 'Autodesk.Revit.DB',
            'key_properties': [
                'Area - Gets area value in square feet',
                'Perimeter - Gets area perimeter in feet',
                'AreaScheme - Gets associated area scheme',
                'Number - Gets/sets area number',
                'Name - Gets/sets area name',
                'Level - Gets associated level'
            ],
            'key_methods': [
                'GetBoundarySegments() - Gets area boundary segments'
            ]
        },
        
        'Space': {
            'description': 'Represents a space element for MEP analysis',
            'namespace': 'Autodesk.Revit.DB.Mechanical',
            'key_properties': [
                'Area - Gets space area in square feet',
                'Volume - Gets space volume in cubic feet',
                'Number - Gets/sets space number', 
                'Name - Gets/sets space name',
                'OccupancyNumber - Gets/sets occupancy count',
                'LightingLoad - Gets/sets lighting load',
                'PowerLoad - Gets/sets power load'
            ]
        }
    }

# USAGE EXAMPLES
ANALYSIS_EXAMPLES = """
# Getting Room Areas and Information
def get_room_analysis(doc):
    room_data = []
    
    # Get all rooms
    rooms = FilteredElementCollector(doc) \\
        .OfCategory(BuiltInCategory.OST_Rooms) \\
        .WhereElementIsNotElementType() \\
        .ToElements()
    
    for room in rooms:
        if room.Area > 0:  # Only rooms with calculated area
            room_info = {
                'Number': room.Number,
                'Name': room.Name, 
                'Area': room.Area,  # Square feet
                'Volume': room.Volume,  # Cubic feet
                'Perimeter': room.Perimeter,  # Feet
                'Level': room.Level.Name,
                'Phase': room.get_Parameter(BuiltInParameter.ROOM_PHASE).AsValueString()
            }
            room_data.append(room_info)
    
    return room_data

# Getting Room Areas by Level
def get_areas_by_level(doc):
    level_areas = {}
    
    rooms = FilteredElementCollector(doc) \\
        .OfCategory(BuiltInCategory.OST_Rooms) \\
        .WhereElementIsNotElementType()
    
    for room in rooms:
        if room.Area > 0:
            level_name = room.Level.Name
            if level_name not in level_areas:
                level_areas[level_name] = {
                    'total_area': 0,
                    'room_count': 0,
                    'rooms': []
                }
            
            level_areas[level_name]['total_area'] += room.Area
            level_areas[level_name]['room_count'] += 1
            level_areas[level_name]['rooms'].append({
                'name': room.Name,
                'number': room.Number,
                'area': room.Area
            })
    
    return level_areas
"""

# QUICK REFERENCE
QUICK_REFERENCE = {
    "Get All Rooms": "FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)",
    "Get Room Area": "room.Area",
    "Get Room Volume": "room.Volume", 
    "Get Room Perimeter": "room.Perimeter",
    "Get Room Boundaries": "room.GetBoundarySegments(options)",
    "Get Areas": "FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Areas)",
    "Get Area Schemes": "FilteredElementCollector(doc).OfClass(typeof(AreaScheme))",
    "Area Volume Settings": "AreaVolumeSettings.GetAreaVolumeSettings(doc)",
    "Room Calculation Point": "room.GetRoomCalculationPoint()",
    "Room by Point": "doc.GetRoomAtPoint(point)"
}

# COMMON BUILT-IN PARAMETERS FOR SPATIAL ELEMENTS
SPATIAL_PARAMETERS = {
    "Room Parameters": {
        'ROOM_AREA': 'Room area in square feet',
        'ROOM_VOLUME': 'Room volume in cubic feet',
        'ROOM_PERIMETER': 'Room perimeter in feet',
        'ROOM_HEIGHT': 'Room height',
        'ROOM_NUMBER': 'Room number',
        'ROOM_NAME': 'Room name',
        'ROOM_COMMENTS': 'Room comments',
        'ROOM_DEPARTMENT': 'Room department',
        'ROOM_OCCUPANCY': 'Room occupancy count',
        'ROOM_PHASE': 'Room phase'
    },
    
    "Area Parameters": {
        'AREA_AREA': 'Area value in square feet',
        'AREA_PERIMETER': 'Area perimeter in feet', 
        'AREA_NUMBER': 'Area number',
        'AREA_NAME': 'Area name',
        'AREA_COMMENTS': 'Area comments'
    }
}
