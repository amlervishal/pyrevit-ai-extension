"""
Revit API - Schedules and Sheets Reference
Creating and managing schedules, sheets, and viewports for documentation
"""

class ScheduleAPI:
    """
    Schedule Creation and Management
    Essential for creating material takeoffs, room schedules, and element schedules
    """

# SCHEDULE CLASSES
SCHEDULE_CLASSES = {
    'ViewSchedule': {
        'description': 'Represents a schedule view in Revit',
        'namespace': 'Autodesk.Revit.DB',
        'key_properties': [
            'Name - Schedule name',
            'Definition - Gets ScheduleDefinition',
            'IsTitleblockRevisionSchedule - Is titleblock revision schedule',
            'IsValidForReportCreation - Can be used for reports'
        ],
        'key_methods': [
            'Create() - Creates new schedule',
            'Export() - Exports schedule data', 
            'GetTableData() - Gets schedule table data',
            'GetAvailableFields() - Gets available fields'
        ]
    },
    
    'ScheduleDefinition': {
        'description': 'Defines the structure and content of a schedule',
        'key_properties': [
            'CategoryId - Category being scheduled',
            'IsKeySchedule - Is this a key schedule',
            'ShowHeaders - Whether to show headers',
            'ShowTitle - Whether to show title'
        ],
        'key_methods': [
            'GetFields() - Gets all schedule fields',
            'AddField() - Adds field to schedule',
            'GetFilters() - Gets schedule filters',
            'AddFilter() - Adds filter to schedule',
            'GetSortGroupFields() - Gets sort/group fields',
            'AddSortGroupField() - Adds sort/group field'
        ]
    }
}

class SheetAPI:
    """
    Sheet Creation and Management
    Essential for creating drawing sheets and placing views
    """

# SHEET CLASSES
SHEET_CLASSES = {
    'ViewSheet': {
        'description': 'Represents a drawing sheet',
        'namespace': 'Autodesk.Revit.DB',
        'key_properties': [
            'Name - Sheet name',
            'SheetNumber - Sheet number',
            'TitleBlock - Associated titleblock',
            'IsPlaceholder - Is placeholder sheet'
        ],
        'key_methods': [
            'Create() - Creates new sheet',
            'GetAllViewports() - Gets all viewports on sheet',
            'CanViewBePlaced() - Checks if view can be placed',
            'GetAllPlacedViews() - Gets all placed views'
        ]
    },
    
    'Viewport': {
        'description': 'Represents a view placement on a sheet',  
        'key_properties': [
            'ViewId - ID of placed view',
            'SheetId - ID of parent sheet',
            'GetBoxCenter() - Center point of viewport',
            'GetBoxOutline() - Viewport outline'
        ],
        'key_methods': [
            'Create() - Creates viewport',
            'SetBoxCenter() - Sets viewport center',
            'GetLabelOutline() - Gets label outline',
            'CanChangeTypeId() - Can change viewport type'
        ]
    }
}

# USAGE EXAMPLES
SCHEDULE_EXAMPLES = """
# Creating a Room Schedule
def create_room_schedule(doc):
    with Transaction(doc, "Create Room Schedule") as trans:
        trans.Start()
        
        # Create room schedule
        schedule = ViewSchedule.CreateSchedule(doc, ElementId(BuiltInCategory.OST_Rooms))
        schedule.Name = "Room Schedule"
        
        # Get schedule definition
        definition = schedule.Definition
        available_fields = definition.GetSchedulableFields()
        
        # Add Room Number, Name, Area, Level fields
        field_names = ["Number", "Name", "Area", "Level"]
        
        for field_name in field_names:
            for field in available_fields:
                if field.GetName(doc) == field_name:
                    definition.AddField(field)
                    break
        
        trans.Commit()
        return schedule

# Creating Material Takeoff
def create_material_takeoff(doc):
    with Transaction(doc, "Create Material Takeoff") as trans:
        trans.Start()
        
        schedule = ViewSchedule.CreateMaterialTakeoff(doc, ElementId(BuiltInCategory.OST_Walls))
        schedule.Name = "Wall Material Takeoff"
        
        definition = schedule.Definition
        available_fields = definition.GetSchedulableFields()
        
        # Add material fields
        for field in available_fields:
            if "Material" in field.GetName(doc):
                definition.AddField(field)
        
        trans.Commit()
        return schedule
"""

SHEET_EXAMPLES = """
# Creating Sheets with Views
def create_sheets_from_views(doc, view_list, titleblock_id):
    created_sheets = []
    
    with Transaction(doc, "Create Sheets") as trans:
        trans.Start()
        
        for i, view in enumerate(view_list):
            # Create sheet
            sheet = ViewSheet.Create(doc, titleblock_id)
            sheet.SheetNumber = f"A-{i+1:03d}"
            sheet.Name = f"{view.Name} - Plan"
            
            # Place view on sheet
            if ViewSheet.CanViewBePlaced(sheet, view):
                sheet_center = XYZ(11, 8.5, 0)
                viewport = Viewport.Create(doc, sheet.Id, view.Id, sheet_center)
                
                created_sheets.append({
                    'sheet': sheet,
                    'viewport': viewport,
                    'view': view
                })
        
        trans.Commit()
    return created_sheets
"""

# QUICK REFERENCE
QUICK_REFERENCE = {
    "Create Room Schedule": "ViewSchedule.CreateSchedule(doc, ElementId(BuiltInCategory.OST_Rooms))",
    "Create Material Takeoff": "ViewSchedule.CreateMaterialTakeoff(doc, categoryId)",
    "Add Schedule Field": "definition.AddField(schedulableField)",
    "Add Schedule Filter": "definition.AddFilter(scheduleFilter)",
    "Create Sheet": "ViewSheet.Create(doc, titleblockId)",
    "Place View on Sheet": "Viewport.Create(doc, sheetId, viewId, location)",
    "Get Sheet Viewports": "sheet.GetAllViewports()",
    "Check if View Can Be Placed": "ViewSheet.CanViewBePlaced(sheet, view)"
}
