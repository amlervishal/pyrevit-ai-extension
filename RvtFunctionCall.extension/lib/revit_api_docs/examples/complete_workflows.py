"""
Revit API - Complete Workflow Examples
Common operations and workflows for Revit API development
"""

class BasicWorkflows:
    """
    Essential workflows for common Revit API operations
    """

# ACCESSING THE ACTIVE DOCUMENT
DOCUMENT_ACCESS = """
# Getting the Active Document - Essential First Step
public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
{
    // Get UI application and document
    UIApplication uiApp = commandData.Application;
    UIDocument uiDoc = uiApp.ActiveUIDocument;
    Application app = uiApp.Application;
    Document doc = uiDoc.Document;
    
    // Basic document information
    string docTitle = doc.Title;
    string docPath = doc.PathName;
    bool isModified = doc.IsModified;
    bool isWorkshared = doc.IsWorkshared;
    
    TaskDialog.Show("Document Info", $"Title: {docTitle}\\nPath: {docPath}\\nModified: {isModified}");
    
    return Result.Succeeded;
}
"""

# ELEMENT SELECTION WORKFLOW
SELECTION_WORKFLOW = """
# Complete Element Selection Workflow
public void SelectAndProcessElements(UIDocument uiDoc)
{
    Document doc = uiDoc.Document;
    Selection selection = uiDoc.Selection;
    
    try
    {
        // Method 1: Get current selection
        ICollection<ElementId> selectedIds = selection.GetElementIds();
        if (selectedIds.Count > 0)
        {
            foreach (ElementId id in selectedIds)
            {
                Element element = doc.GetElement(id);
                ProcessElement(element);
            }
        }
        
        // Method 2: Interactive selection
        Reference reference = selection.PickObject(ObjectType.Element, "Select an element");
        Element selectedElement = doc.GetElement(reference);
        
        // Method 3: Filter-based selection
        IList<Reference> references = selection.PickObjects(ObjectType.Element, 
            new WallSelectionFilter(), "Select walls");
        
        foreach (Reference ref in references)
        {
            Wall wall = doc.GetElement(ref) as Wall;
            if (wall != null)
            {
                ProcessWall(wall);
            }
        }
        
        // Method 4: Programmatic selection with FilteredElementCollector
        FilteredElementCollector collector = new FilteredElementCollector(doc)
            .OfClass(typeof(Wall))
            .WhereElementIsNotElementType();
            
        foreach (Wall wall in collector.Cast<Wall>())
        {
            ProcessWall(wall);
        }
    }
    catch (Autodesk.Revit.Exceptions.OperationCanceledException)
    {
        // User cancelled selection
        TaskDialog.Show("Info", "Selection cancelled by user");
    }
}

// Custom selection filter
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
"""

# ELEMENT CREATION WORKFLOW
CREATION_WORKFLOW = """
# Complete Element Creation Workflow
public void CreateBuildingElements(Document doc)
{
    using (Transaction trans = new Transaction(doc, "Create Building Elements"))
    {
        trans.Start();
        
        try
        {
            // Step 1: Get required types and levels
            Level level = GetOrCreateLevel(doc, 0, "Ground Floor");
            WallType wallType = GetWallType(doc, "Generic - 8\\\"");
            FloorType floorType = GetFloorType(doc, "Generic - 12\\\"");
            
            // Step 2: Create walls
            List<Wall> walls = CreateRoomWalls(doc, level, wallType);
            
            // Step 3: Create floor
            Floor floor = CreateFloorFromWalls(doc, walls, floorType, level);
            
            // Step 4: Add door to wall
            FamilySymbol doorSymbol = GetFamilySymbol(doc, "Single-Flush", "30\\\" x 80\\\"");
            FamilyInstance door = CreateDoorInWall(doc, walls[0], doorSymbol, level);
            
            // Step 5: Add window to wall
            FamilySymbol windowSymbol = GetFamilySymbol(doc, "Fixed", "24\\\" x 48\\\"");
            FamilyInstance window = CreateWindowInWall(doc, walls[1], windowSymbol, level);
            
            trans.Commit();
            TaskDialog.Show("Success", "Building elements created successfully!");
        }
        catch (Exception ex)
        {
            trans.RollBack();
            TaskDialog.Show("Error", $"Failed to create elements: {ex.Message}");
        }
    }
}

private List<Wall> CreateRoomWalls(Document doc, Level level, WallType wallType)
{
    List<Wall> walls = new List<Wall>();
    
    // Create rectangular room 20' x 15'
    List<Line> wallLines = new List<Line>
    {
        Line.CreateBound(new XYZ(0, 0, 0), new XYZ(20, 0, 0)),      // South wall
        Line.CreateBound(new XYZ(20, 0, 0), new XYZ(20, 15, 0)),    // East wall  
        Line.CreateBound(new XYZ(20, 15, 0), new XYZ(0, 15, 0)),    // North wall
        Line.CreateBound(new XYZ(0, 15, 0), new XYZ(0, 0, 0))       // West wall
    };
    
    foreach (Line line in wallLines)
    {
        Wall wall = Wall.Create(doc, line, wallType.Id, level.Id, 10, 0, false, false);
        walls.Add(wall);
    }
    
    return walls;
}
"""

# UTILITY METHODS
UTILITY_METHODS = """
# Essential Utility Methods
private Level GetOrCreateLevel(Document doc, double elevation, string name)
{
    // Try to find existing level
    FilteredElementCollector collector = new FilteredElementCollector(doc)
        .OfClass(typeof(Level))
        .WhereElementIsNotElementType();
    
    foreach (Level level in collector.Cast<Level>())
    {
        if (Math.Abs(level.Elevation - elevation) < 0.01)
        {
            return level;
        }
    }
    
    // Create new level
    Level newLevel = Level.Create(doc, elevation);
    newLevel.Name = name;
    return newLevel;
}

private WallType GetWallType(Document doc, string typeName)
{
    FilteredElementCollector collector = new FilteredElementCollector(doc)
        .OfClass(typeof(WallType));
    
    foreach (WallType wallType in collector.Cast<WallType>())
    {
        if (wallType.Name == typeName)
        {
            return wallType;
        }
    }
    
    return collector.FirstElement() as WallType; // Return first available if not found
}
"""
