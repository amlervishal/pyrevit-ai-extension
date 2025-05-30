"""
Revit API - Selection Operations Reference
Essential methods for element selection, filtering, and collection.
"""

class SelectionAPI:
    """
    Selection Class - Current selection in the Revit UI
    Namespace: Autodesk.Revit.UI.Selection
    
    Provides access to the current selection and methods to modify it.
    """
    
    # SELECTION OBJECT ACCESS
    SELECTION_ACCESS = {
        'GetSelection': 'UIDocument.Selection - Gets the current selection object',
        'GetElementIds': 'ICollection<ElementId> - Gets ElementIds of selected elements',
        'GetElements': 'ICollection<Element> - Gets selected elements',
        'SetElementIds': 'void - Sets selection to specified ElementIds'
    }
    
    # INTERACTIVE SELECTION METHODS
    INTERACTIVE_SELECTION = {
        'PickObject(ObjectType)': 'Reference - Pick a single object interactively',
        'PickObjects(ObjectType)': 'IList<Reference> - Pick multiple objects',
        'PickPoint()': 'XYZ - Pick a point in the model',
        'PickElementsByRectangle()': 'IList<Element> - Select elements by rectangle',
        'PickBox(PickBoxStyle)': 'PickedBox - Pick a 3D box region'
    }
    
    # SELECTION FILTERS
    SELECTION_FILTERS = {
        'ISelectionFilter': 'Interface for custom selection filtering',
        'ElementCategoryFilter': 'Filter by element category',
        'ElementClassFilter': 'Filter by element class',
        'ElementTypeFilter': 'Filter by element type'
    }

class FilteredElementCollectorAPI:
    """
    FilteredElementCollector - Primary tool for finding and collecting elements
    Namespace: Autodesk.Revit.DB
    
    Provides powerful filtering and collection capabilities for elements in the document.
    """
    
    # BASIC COLLECTION METHODS
    BASIC_COLLECTION = {
        'FilteredElementCollector(Document)': 'Constructor - Creates collector for document',
        'FilteredElementCollector(Document, ElementId)': 'Constructor - Creates collector for view',
        'ToElements()': 'IList<Element> - Converts to element list',
        'ToElementIds()': 'IList<ElementId> - Converts to ElementId list',
        'FirstElement()': 'Element - Gets first element or null',
        'Count()': 'int - Gets count of elements'
    }
    
    # CATEGORY FILTERING
    CATEGORY_FILTERING = {
        'OfCategory(BuiltInCategory)': 'FilteredElementCollector - Filter by built-in category',
        'OfCategoryId(ElementId)': 'FilteredElementCollector - Filter by category ElementId',
        'WhereElementIsElementType()': 'FilteredElementCollector - Only element types',
        'WhereElementIsNotElementType()': 'FilteredElementCollector - Only element instances'
    }
    
    # CLASS FILTERING  
    CLASS_FILTERING = {
        'OfClass(Type)': 'FilteredElementCollector - Filter by .NET type',
        'OfClass<T>()': 'FilteredElementCollector - Filter by generic type'
    }
    
    # ADVANCED FILTERING
    ADVANCED_FILTERING = {
        'WherePasses(ElementFilter)': 'FilteredElementCollector - Apply custom filter',
        'UnionWith(FilteredElementCollector)': 'FilteredElementCollector - Union with another collector',
        'IntersectWith(FilteredElementCollector)': 'FilteredElementCollector - Intersect with another collector',
        'Excluding(ICollection<ElementId>)': 'FilteredElementCollector - Exclude specific elements'
    }

# ESSENTIAL FILTER CLASSES
class ElementFiltersAPI:
    """
    Element Filter Classes for advanced filtering operations
    """
    
    LOGICAL_FILTERS = {
        'LogicalAndFilter(params ElementFilter[])': 'Combines filters with AND logic',
        'LogicalOrFilter(params ElementFilter[])': 'Combines filters with OR logic',
        'ExclusionFilter(ICollection<ElementId>)': 'Excludes specific elements'
    }
    
    QUICK_FILTERS = {
        'ElementCategoryFilter(BuiltInCategory)': 'Filter by category',
        'ElementClassFilter(Type)': 'Filter by class type',
        'ElementOwnerViewFilter(ElementId)': 'Filter by view ownership',
        'ElementLevelFilter(ElementId)': 'Filter by level association'
    }
    
    SLOW_FILTERS = {
        'BoundingBoxIntersectsFilter(Outline)': 'Filter by bounding box intersection',
        'BoundingBoxContainsPointFilter(XYZ)': 'Filter by point containment',
        'ElementIntersectsElementFilter(Element)': 'Filter by element intersection'
    }

# USAGE EXAMPLES
USAGE_EXAMPLES = """
# Getting Current Selection
UIDocument uidoc = uiApp.ActiveUIDocument;
Selection selection = uidoc.Selection;
ICollection<ElementId> selectedIds = selection.GetElementIds();

# Interactive Selection
try
{
    Reference reference = selection.PickObject(ObjectType.Element, "Select an element");
    Element element = doc.GetElement(reference);
}
catch (Autodesk.Revit.Exceptions.OperationCanceledException)
{
    // User cancelled selection
}

# Collecting All Walls
FilteredElementCollector wallCollector = new FilteredElementCollector(doc)
    .OfClass(typeof(Wall))
    .WhereElementIsNotElementType();
    
IList<Element> walls = wallCollector.ToElements();

# Collecting Elements by Category
FilteredElementCollector doorCollector = new FilteredElementCollector(doc)
    .OfCategory(BuiltInCategory.OST_Doors)
    .WhereElementIsNotElementType();

# Complex Filtering Example
ElementCategoryFilter doorFilter = new ElementCategoryFilter(BuiltInCategory.OST_Doors);
ElementCategoryFilter windowFilter = new ElementCategoryFilter(BuiltInCategory.OST_Windows);
LogicalOrFilter doorWindowFilter = new LogicalOrFilter(doorFilter, windowFilter);

FilteredElementCollector collector = new FilteredElementCollector(doc)
    .WherePasses(doorWindowFilter)
    .WhereElementIsNotElementType();

# Filtering by Level
FilteredElementCollector levelElements = new FilteredElementCollector(doc)
    .WherePasses(new ElementLevelFilter(levelId));

# Setting Selection
List<ElementId> elementsToSelect = new List<ElementId>();
elementsToSelect.Add(elementId1);
elementsToSelect.Add(elementId2);
selection.SetElementIds(elementsToSelect);

# Custom Selection Filter
public class WallSelectionFilter : ISelectionFilter
{
    public bool AllowElement(Element elem)
    {
        return elem is Wall;
    }
    
    public bool AllowReference(Reference reference, XYZ position)
    {
        return true;
    }
}

// Usage of custom filter
WallSelectionFilter wallFilter = new WallSelectionFilter();
Reference wallRef = selection.PickObject(ObjectType.Element, wallFilter, "Select a wall");
"""

# QUICK REFERENCE FOR COMMON OPERATIONS
QUICK_REFERENCE = {
    "Get Current Selection": "uidoc.Selection.GetElementIds()",
    "Pick Single Element": "selection.PickObject(ObjectType.Element)",
    "Pick Multiple Elements": "selection.PickObjects(ObjectType.Element)",
    "Get All Walls": "new FilteredElementCollector(doc).OfClass(typeof(Wall))",
    "Get Elements by Category": "new FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls)",
    "Get Element Types Only": "collector.WhereElementIsElementType()",
    "Get Element Instances Only": "collector.WhereElementIsNotElementType()",
    "Apply Custom Filter": "collector.WherePasses(customFilter)",
    "Set Selection": "selection.SetElementIds(elementIdCollection)",
    "Clear Selection": "selection.SetElementIds(new List<ElementId>())"
}

# COMMON BUILT-IN CATEGORIES
COMMON_CATEGORIES = {
    'OST_Walls': 'Walls',
    'OST_Doors': 'Doors', 
    'OST_Windows': 'Windows',
    'OST_Floors': 'Floors',
    'OST_Ceilings': 'Ceilings',
    'OST_Roofs': 'Roofs',
    'OST_Columns': 'Columns',
    'OST_Beams': 'Beams',
    'OST_Grids': 'Grids',
    'OST_Levels': 'Levels',
    'OST_Rooms': 'Rooms',
    'OST_Areas': 'Areas',
    'OST_Furniture': 'Furniture',
    'OST_GenericModel': 'Generic Models',
    'OST_MechanicalEquipment': 'Mechanical Equipment',
    'OST_ElectricalEquipment': 'Electrical Equipment',
    'OST_PlumbingFixtures': 'Plumbing Fixtures'
}
