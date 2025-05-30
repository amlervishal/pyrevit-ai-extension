"""
Revit API - Document Class Reference
Essential methods and properties for accessing and working with Revit documents.
"""

class DocumentAPI:
    """
    Document Class - Represents an open Autodesk Revit project
    Namespace: Autodesk.Revit.DB
    
    The Document object represents an Autodesk Revit project. Revit can have multiple
    projects open and multiple views to those projects. The active or top most view will be the
    active project and hence the active document which is available from the Application object.
    """
    
    # ESSENTIAL PROPERTIES
    PROPERTIES = {
        'Application': 'Application - Gets the Revit application object',
        'Title': 'string - Gets the title of the document',
        'PathName': 'string - Gets the full path name of the document file',
        'IsModified': 'bool - Indicates whether the document has been modified',
        'IsFamilyDocument': 'bool - Indicates if this document is a family document',
        'IsWorkshared': 'bool - Indicates if this document uses worksharing',
        'ActiveView': 'View - Gets or sets the active view',
        'Settings': 'Settings - Gets the settings for this document',
        'ProjectInformation': 'ProjectInfo - Gets project information element'
    }
    
    # ESSENTIAL METHODS FOR DOCUMENT ACCESS
    DOCUMENT_ACCESS_METHODS = {
        'Save()': 'void - Saves the document',
        'SaveAs(string)': 'void - Saves the document with a new name',
        'Close(bool)': 'bool - Closes the document',
        'Print()': 'bool - Prints the document using current print settings',
        'Export(string, string, ViewSet, ExportOptions)': 'bool - Exports views from document',
        'GetElement(ElementId)': 'Element - Gets element by ElementId',
        'GetElement(Reference)': 'Element - Gets element by Reference',
        'Delete(ElementId)': 'void - Deletes element with given ElementId',
        'Delete(ICollection<ElementId>)': 'void - Deletes multiple elements'
    }
    
    # ESSENTIAL METHODS FOR ELEMENT OPERATIONS
    ELEMENT_OPERATIONS = {
        'Create': {
            'NewFamilyInstance(XYZ, FamilySymbol, Level, StructuralType)': 'FamilyInstance - Creates a new family instance',
            'NewWall(Curve, WallType, Level, double, double, bool, bool)': 'Wall - Creates a new wall',
            'NewFloor(CurveArray, bool)': 'Floor - Creates a new floor',
            'NewCeiling(CurveArray, CeilingType, Level, XYZ)': 'Ceiling - Creates a new ceiling',
            'NewGrid(Line)': 'Grid - Creates a new grid line',
            'NewLevel(double)': 'Level - Creates a new level',
            'NewReferencePlane(XYZ, XYZ, XYZ, View)': 'ReferencePlane - Creates a reference plane'
        },
        'Regenerate': {
            'Regenerate()': 'void - Regenerates the document',
            'RegenerateActiveView()': 'void - Regenerates only the active view'
        }
    }
    
    # COLLECTION AND FILTERING METHODS
    COLLECTION_METHODS = {
        'GetElements(Filter)': 'FilteredElementCollector - Gets elements matching filter criteria',
        'GetUnusedElements(ICollection<BuiltInCategory>)': 'ISet<ElementId> - Gets unused elements of specified categories'
    }
    
    # TRANSACTION METHODS (Essential for modifications)
    TRANSACTION_METHODS = {
        'Transaction(Document, string)': 'Transaction - Creates new transaction for modifications',
        'TransactionGroup(Document, string)': 'TransactionGroup - Creates transaction group',
        'SubTransaction(Document)': 'SubTransaction - Creates sub-transaction'
    }

# USAGE EXAMPLES
USAGE_EXAMPLES = """
# Getting the Active Document
UIApplication uiApp = commandData.Application;
Application app = uiApp.Application;
Document doc = uiApp.ActiveUIDocument.Document;

# Basic Document Operations
string docTitle = doc.Title;
string docPath = doc.PathName;
bool isModified = doc.IsModified;

# Getting Elements
Element element = doc.GetElement(elementId);
FilteredElementCollector collector = new FilteredElementCollector(doc);

# Creating Elements (within Transaction)
using (Transaction trans = new Transaction(doc, "Create Wall"))
{
    trans.Start();
    
    // Create a wall
    Line line = Line.CreateBound(new XYZ(0, 0, 0), new XYZ(10, 0, 0));
    Wall wall = Wall.Create(doc, line, wallTypeId, levelId, 10, 0, false, false);
    
    trans.Commit();
}

# Deleting Elements
using (Transaction trans = new Transaction(doc, "Delete Elements"))
{
    trans.Start();
    doc.Delete(elementId);
    trans.Commit();
}

# Saving Document
doc.Save();
doc.SaveAs("C:\\\\path\\\\to\\\\new\\\\document.rvt");
"""

# ESSENTIAL DOCUMENT PROPERTIES AND METHODS QUICK REFERENCE
QUICK_REFERENCE = {
    "Access Current Document": "UIApplication.ActiveUIDocument.Document",
    "Get Element by ID": "doc.GetElement(elementId)",
    "Create Transaction": "new Transaction(doc, \"Description\")",
    "Start Transaction": "transaction.Start()",
    "Commit Transaction": "transaction.Commit()",
    "Get All Elements": "new FilteredElementCollector(doc)",
    "Get Active View": "doc.ActiveView",
    "Check if Modified": "doc.IsModified",
    "Save Document": "doc.Save()",
    "Close Document": "doc.Close(false)"
}
