import os
import requests
from bs4 import BeautifulSoup
import time
import json
import re

# Configuration
BASE_URL = "https://www.revitapidocs.com/2024/"
OUTPUT_DIR = "/Users/vishal/Work/MCP_Projects/rvt-function-call/RvtFunctionCall.extension/lib/revit_api_docs"
DELAY = 0.5  # Delay between requests to avoid overloading the server

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to clean text
def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

# Function to save text to file
def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to download and parse a class page
def scrape_class(url, class_name):
    print(f"Scraping class: {class_name}")
    
    # Create safe filename
    safe_name = re.sub(r'[^\w\-\.]', '_', class_name)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Fetch the page
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return
    
    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract class information
    class_info = {}
    class_info["name"] = class_name
    class_info["url"] = url
    
    # Extract description
    description_div = soup.select_one('.topicContent')
    if description_div:
        class_info["description"] = clean_text(description_div.get_text())
    else:
        class_info["description"] = ""
    
    # Extract properties
    class_info["properties"] = []
    property_tables = soup.find_all('table', {'class': 'memberList'})
    for table in property_tables:
        # Check if this is a properties table
        prev_h2 = table.find_previous('h2')
        if prev_h2 and 'Properties' in prev_h2.text:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    property_name = clean_text(cols[0].get_text())
                    property_desc = clean_text(cols[1].get_text())
                    class_info["properties"].append({
                        "name": property_name,
                        "description": property_desc
                    })
    
    # Extract methods
    class_info["methods"] = []
    method_tables = soup.find_all('table', {'class': 'memberList'})
    for table in method_tables:
        # Check if this is a methods table
        prev_h2 = table.find_previous('h2')
        if prev_h2 and 'Methods' in prev_h2.text:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    method_name = clean_text(cols[0].get_text())
                    method_desc = clean_text(cols[1].get_text())
                    class_info["methods"].append({
                        "name": method_name,
                        "description": method_desc
                    })
    
    # Create markdown file
    markdown = f"# {class_name}\n\n"
    
    if class_info["description"]:
        markdown += f"{class_info['description']}\n\n"
    
    if class_info["properties"]:
        markdown += "## Properties\n\n"
        for prop in class_info["properties"]:
            markdown += f"- `{prop['name']}`: {prop['description']}\n"
        markdown += "\n"
    
    if class_info["methods"]:
        markdown += "## Methods\n\n"
        for method in class_info["methods"]:
            markdown += f"- `{method['name']}`: {method['description']}\n"
        markdown += "\n"
    
    markdown += f"## Source\n\n{url}\n"
    
    # Save as text file
    file_path = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")
    save_to_file(file_path, markdown)
    
    # Save as JSON
    json_path = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(class_info, json_file, indent=2)
    
    return True

# Function to find and scrape documentation from the site
def scrape_documentation():
    # Create a list of known class URLs using search results
    common_classes = [
        {"name": "Rebar", "url": BASE_URL + "70fd7426-f4a4-591c-8c06-3c18dda45e7d.htm"},
        {"name": "Units", "url": BASE_URL + "e416927f-551c-97a9-d5cf-ee255d9bdf2b.htm"},
        {"name": "DWGExport", "url": BASE_URL + "44ee91ff-c9f3-7df5-b8c0-81c17ac75dc7.htm"}
    ]
    
    # Scrape the known classes
    success_count = 0
    for class_info in common_classes:
        if scrape_class(class_info["url"], class_info["name"]):
            success_count += 1
        time.sleep(DELAY)
    
    # Try to get the homepage to find more classes
    print("Fetching main page to find more classes...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print(f"Failed to fetch {BASE_URL}: {response.status_code}")
            return success_count
    except Exception as e:
        print(f"Error fetching {BASE_URL}: {str(e)}")
        return success_count
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for links to namespaces
    namespace_links = soup.select('a[href]')
    namespaces_found = False
    
    for link in namespace_links:
        href = link.get('href')
        # Check if this looks like a namespace link
        if href and 'htm' in href and not href.startswith('http'):
            text = clean_text(link.get_text())
            if text and '.' in text and text.startswith('Autodesk'):
                namespaces_found = True
                print(f"Found namespace: {text}")
                namespace_url = BASE_URL + href
                
                # Fetch the namespace page
                try:
                    namespace_response = requests.get(namespace_url)
                    if namespace_response.status_code != 200:
                        print(f"Failed to fetch {namespace_url}: {namespace_response.status_code}")
                        continue
                    
                    namespace_soup = BeautifulSoup(namespace_response.content, 'html.parser')
                    
                    # Find classes in this namespace
                    class_links = namespace_soup.select('a[href]')
                    for class_link in class_links:
                        class_href = class_link.get('href')
                        if class_href and 'htm' in class_href and not class_href.startswith('http'):
                            class_text = clean_text(class_link.get_text())
                            if class_text and not '.' in class_text:  # Simple heuristic for class names
                                class_url = BASE_URL + class_href
                                if scrape_class(class_url, class_text):
                                    success_count += 1
                                time.sleep(DELAY)
                except Exception as e:
                    print(f"Error processing namespace {text}: {str(e)}")
                
                time.sleep(DELAY)
    
    if not namespaces_found:
        print("No namespaces found, looking for direct class links...")
        
        # Look for direct class links
        for link in namespace_links:
            href = link.get('href')
            if href and 'htm' in href and not href.startswith('http'):
                text = clean_text(link.get_text())
                if text and not '.' in text and text[0].isupper():  # Simple heuristic for class names
                    class_url = BASE_URL + href
                    if scrape_class(class_url, text):
                        success_count += 1
                    time.sleep(DELAY)
    
    return success_count

# Create a simple index file
def create_index_file():
    # Gather all class files
    class_files = []
    for root, _, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith('.txt'):
                rel_path = os.path.relpath(os.path.join(root, file), OUTPUT_DIR)
                class_name = os.path.splitext(file)[0]
                class_files.append({"name": class_name, "path": rel_path})
    
    # Sort by class name
    class_files.sort(key=lambda x: x["name"])
    
    # Create index content
    index_content = "# Revit API Documentation Index\n\n"
    
    # Add all classes
    for class_file in class_files:
        index_content += f"- [{class_file['name']}]({class_file['path']})\n"
    
    # Save index file
    index_path = os.path.join(OUTPUT_DIR, "index.md")
    save_to_file(index_path, index_content)
    print(f"Created index file at {index_path}")

# Create our own simple documentation for common Revit classes
def create_manual_documentation():
    # Dictionary of common classes with descriptions
    common_classes = {
        "Document": """
The Document class represents an open Revit project or family document. It provides access to document-level elements, settings, and parameters.

## Properties
- `ActiveView`: Gets or sets the active view of the document.
- `Application`: Gets the Application object that represents the Revit application.
- `PathName`: Gets the fully qualified path to the file.
- `Title`: Gets the title of the document.
- `IsFamilyDocument`: Indicates whether the document is a family document.
- `IsModified`: Indicates whether the document has been modified.
- `IsLinked`: Indicates whether the document is a linked document.

## Methods
- `Create(Application)`: Creates a new document.
- `Close()`: Closes the document.
- `SaveAs(String)`: Saves the document to a new file.
- `Delete(Element)`: Removes an element from the document.
- `GetElement(ElementId)`: Gets an element by its ID.
- `GetElements()`: Gets all elements in the document.
- `GetElementById(Int32)`: Gets an element by its integer ID.
- `CreateFamilyInstance(XYZ, FamilySymbol, Level, StructuralType)`: Creates a new family instance.
""",
        "Element": """
The Element class is the base class for all Revit elements. It provides common functionality for all elements in a document.

## Properties
- `Id`: Gets the ElementId of the element.
- `Name`: Gets or sets the name of the element.
- `Category`: Gets the category of the element.
- `Parameters`: Gets the parameters of the element.
- `Pinned`: Gets or sets whether the element is pinned.
- `Location`: Gets the location of the element.
- `Document`: Gets the document that owns the element.
- `UniqueId`: Gets the unique identifier for the element.

## Methods
- `Delete()`: Deletes the element from the document.
- `GetParameters(String)`: Gets parameters by name.
- `GetParameter(BuiltInParameter)`: Gets a built-in parameter.
- `get_Parameter(String)`: Gets a parameter by name.
- `GetGeometryObjectFromReference(Reference)`: Gets geometry from a reference.
- `SetParameterByName(String, Object)`: Sets a parameter value by name.
- `GetParameterValueByName(String)`: Gets a parameter value by name.
""",
        "FilteredElementCollector": """
The FilteredElementCollector class is used to query elements in a document. It provides a powerful API for filtering and selecting elements.

## Properties
- `Count`: Gets the number of elements in the collector.

## Methods
- `OfCategory(BuiltInCategory)`: Filters elements by category.
- `OfClass(Type)`: Filters elements by class type.
- `WhereElementIsNotElementType()`: Filters for non-element type elements.
- `WhereElementIsElementType()`: Filters for element type elements.
- `WherePasses(ISelectionFilter)`: Applies a custom filter.
- `ToElements()`: Gets all elements in the collector.
- `ToElementIds()`: Gets the IDs of all elements in the collector.
- `FirstElement()`: Gets the first element in the collector.
- `OfCategoryId(ElementId)`: Filters elements by category ID.
- `OfType<T>()`: Returns elements of a specific type.
""",
        "Transaction": """
The Transaction class represents a transaction in Revit. All changes to the Revit model must be made within a transaction.

## Properties
- `Name`: Gets or sets the name of the transaction.
- `Status`: Gets the status of the transaction.
- `HasEnded`: Indicates whether the transaction has ended.
- `HasStarted`: Indicates whether the transaction has started.

## Methods
- `Start()`: Starts the transaction.
- `Commit()`: Commits the changes made in the transaction.
- `RollBack()`: Rolls back the changes made in the transaction.
- `Dispose()`: Disposes of the transaction.
- `GetFailureHandlingOptions()`: Gets the failure handling options.
- `SetFailureHandlingOptions(FailureHandlingOptions)`: Sets failure handling options.
""",
        "Wall": """
The Wall class represents a wall in a Revit project.

## Properties
- `Location`: Gets the location of the wall.
- `Width`: Gets the width of the wall.
- `WallType`: Gets or sets the wall type.
- `Orientation`: Gets the orientation of the wall.
- `Flipped`: Gets or sets whether the wall is flipped.
- `Length`: Gets the length of the wall.
- `Height`: Gets the height of the wall.

## Methods
- `Create(Document, Curve, ElementId, ElementId, Double, Double, Boolean, Boolean)`: Creates a new wall.
- `Flip()`: Flips the wall.
- `GetWallLayers()`: Gets the layers of the wall.
- `SetCompoundStructure(CompoundStructure)`: Sets the compound structure of the wall.
""",
        "Floor": """
The Floor class represents a floor in a Revit project.

## Properties
- `FloorType`: Gets or sets the floor type.
- `Level`: Gets the level of the floor.
- `Thickness`: Gets the thickness of the floor.
- `Area`: Gets the area of the floor.

## Methods
- `Create(Document, CurveArray, ElementId, ElementId)`: Creates a new floor.
- `GetBoundary()`: Gets the boundary of the floor.
- `GetCompoundStructure()`: Gets the compound structure of the floor.
""",
        "XYZ": """
The XYZ class represents a point or vector in 3D space.

## Properties
- `X`: Gets the X-coordinate.
- `Y`: Gets the Y-coordinate.
- `Z`: Gets the Z-coordinate.
- `IsZeroLength()`: Gets whether the vector is of zero length.
- `IsUnitLength()`: Gets whether the vector is of unit length.

## Methods
- `Add(XYZ)`: Adds two vectors.
- `Subtract(XYZ)`: Subtracts a vector from this vector.
- `CrossProduct(XYZ)`: Computes the cross product with another vector.
- `DotProduct(XYZ)`: Computes the dot product with another vector.
- `Normalize()`: Normalizes the vector to unit length.
- `DistanceTo(XYZ)`: Computes the distance to another point.
""",
        "ElementId": """
The ElementId class uniquely identifies elements within a document. It encapsulates an integer value.

## Properties
- `IntegerValue`: Gets the integer value of the ElementId.
- `InvalidElementId`: A static property representing an invalid element ID.

## Methods
- `Equals(Object)`: Determines whether the specified object is equal to the current ElementId.
- `GetHashCode()`: Serves as a hash function for ElementId.
- `ToString()`: Returns a string representation of the ElementId.
""",
        "Parameter": """
The Parameter class represents a parameter of a Revit element. It provides access to the parameter's value and properties.

## Properties
- `Definition`: Gets the parameter definition.
- `Element`: Gets the element that owns the parameter.
- `Id`: Gets the parameter's ID.
- `IsReadOnly`: Indicates whether the parameter is read-only.
- `IsShared`: Indicates whether the parameter is a shared parameter.
- `StorageType`: Gets the storage type of the parameter.

## Methods
- `AsDouble()`: Gets the parameter value as a double.
- `AsInteger()`: Gets the parameter value as an integer.
- `AsString()`: Gets the parameter value as a string.
- `AsElementId()`: Gets the parameter value as an ElementId.
- `Set(Double)`: Sets the parameter value as a double.
- `Set(Integer)`: Sets the parameter value as an integer.
- `Set(String)`: Sets the parameter value as a string.
- `Set(ElementId)`: Sets the parameter value as an ElementId.
- `Clear()`: Clears the parameter value.
""",
        "BuiltInParameter": """
The BuiltInParameter enumeration represents built-in parameters in Revit elements.

## Values
- `ALL_MODEL_INSTANCE_COMMENTS`: Comments parameter for all element instances.
- `ALL_MODEL_MARK`: Mark parameter for all elements.
- `WALL_BASE_CONSTRAINT`: The base constraint of a wall.
- `WALL_HEIGHT`: The height of a wall.
- `WALL_WIDTH`: The width of a wall.
- `ELEM_CATEGORY_PARAM`: The category of an element.
- `ELEM_FAMILY_PARAM`: The family of an element.
- `ELEM_TYPE_PARAM`: The type of an element.
- `DOOR_HEIGHT`: The height of a door.
- `DOOR_WIDTH`: The width of a door.
- `WINDOW_HEIGHT`: The height of a window.
- `WINDOW_WIDTH`: The width of a window.
""",
        "Category": """
The Category class represents a category in Revit, which is a group of similar elements.

## Properties
- `Id`: Gets the ElementId of the category.
- `Name`: Gets the name of the category.
- `Parent`: Gets the parent category.
- `AllowsBoundParameters`: Indicates whether the category allows bound parameters.
- `CategoryType`: Gets the type of the category.
- `Material`: Gets or sets the default material for the category.

## Methods
- `GetBuiltInCategory()`: Gets the built-in category corresponding to this category.
- `IsTagCategory()`: Determines whether this is a tag category.
- `IsSubcategory()`: Determines whether this is a subcategory.
- `GetCategoryType()`: Gets the category type.
- `GetBuiltInParameter(BuiltInParameter)`: Gets a built-in parameter for the category.
""",
        "View": """
The View class represents a view in a Revit project.

## Properties
- `Name`: Gets or sets the name of the view.
- `Title`: Gets the title of the view.
- `Scale`: Gets or sets the scale of the view.
- `DetailLevel`: Gets or sets the detail level of the view.
- `DisplayStyle`: Gets or sets the display style of the view.
- `Document`: Gets the document of the view.
- `Id`: Gets the ElementId of the view.
- `IsTemplate`: Gets whether the view is a template.

## Methods
- `Duplicate(ViewDuplicateOption)`: Duplicates the view.
- `SetCategoryHidden(ElementId, Boolean)`: Sets whether a category is hidden in the view.
- `SetDetailLevel(ViewDetailLevel)`: Sets the detail level of the view.
- `SetScale(Integer)`: Sets the scale of the view.
- `GetCategoryHidden(ElementId)`: Gets whether a category is hidden in the view.
- `GetDependentViewIds()`: Gets the IDs of dependent views.
"""
    }
    
    # Add more advanced classes
    advanced_classes = {
        "UIApplication": """
The UIApplication class represents the Revit application and provides access to the user interface.

## Properties
- `Application`: Gets the Application object.
- `ActiveUIDocument`: Gets the active UI document.

## Methods
- `OpenAndActivateDocument(String)`: Opens and activates a document.
- `GetRibbonPanels(String)`: Gets the ribbon panels in a tab.
- `CreateRibbonTab(String)`: Creates a new ribbon tab.
- `CreateRibbonPanel(String)`: Creates a new ribbon panel.
- `LoadAddIn(String)`: Loads an add-in from a file.
""",
        "UIDocument": """
The UIDocument class represents the user interface for a Revit document.

## Properties
- `Document`: Gets the document.
- `Selection`: Gets the current selection.
- `ActiveView`: Gets or sets the active view.
- `ActiveGraphicalView`: Gets the active graphical view.

## Methods
- `ShowElements(ElementSet)`: Shows elements in the active view.
- `ShowElements(Element)`: Shows an element in the active view.
- `GetOpenUIViews()`: Gets all open UI views.
- `RefreshActiveView()`: Refreshes the active view.
- `PromptToSelectElementsOfType(Type, String)`: Prompts the user to select elements of a specific type.
""",
        "ModelLine": """
The ModelLine class represents a model line in Revit.

## Properties
- `GeometryCurve`: Gets the geometry curve of the model line.
- `LineStyle`: Gets or sets the line style.

## Methods
- `Create(Document, Curve, SketchPlane)`: Creates a new model line.
- `GetLineStyle()`: Gets the line style of the model line.
- `SetLineStyle(ElementId)`: Sets the line style of the model line.
""",
        "FamilyInstance": """
The FamilyInstance class represents an instance of a family in a Revit project.

## Properties
- `Symbol`: Gets or sets the family symbol.
- `Host`: Gets the host element.
- `Room`: Gets the room that contains the instance.
- `Space`: Gets the space that contains the instance.
- `FacingOrientation`: Gets the facing orientation.
- `HandOrientation`: Gets the hand orientation.

## Methods
- `Create(Document, FamilySymbol, XYZ, Element, StructuralType)`: Creates a new family instance.
- `GetTransform()`: Gets the transform of the instance.
- `GetTypeId()`: Gets the type ID of the instance.
- `MoveWithHost(ElementId, ElementId)`: Moves the instance with its host.
""",
        "Level": """
The Level class represents a level in a Revit project.

## Properties
- `Elevation`: Gets or sets the elevation of the level.
- `Name`: Gets or sets the name of the level.
- `ProjectElevation`: Gets the project elevation of the level.

## Methods
- `Create(Document, Double)`: Creates a new level.
- `get_Parameter(BuiltInParameter)`: Gets a built-in parameter of the level.
- `GetPlaneReference()`: Gets the plane reference of the level.
""",
        "Line": """
The Line class represents a line in 3D space.

## Properties
- `Length`: Gets the length of the line.
- `Direction`: Gets the direction of the line.
- `Origin`: Gets the origin of the line.
- `EndPoint`: Gets the end point of the line.

## Methods
- `CreateBound(XYZ, XYZ)`: Creates a bounded line between two points.
- `CreateUnbound(XYZ, XYZ)`: Creates an unbounded line through a point in a direction.
- `Intersect(Curve)`: Intersects the line with another curve.
- `Project(XYZ)`: Projects a point onto the line.
"""
    }
    
    # Combine common and advanced classes
    all_classes = {}
    all_classes.update(common_classes)
    all_classes.update(advanced_classes)
    
    # Create manual documentation for all classes
    for class_name, content in all_classes.items():
        # Create safe filename
        safe_name = re.sub(r'[^\w\-\.]', '_', class_name)
        
        # Save as text file
        file_path = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")
        save_to_file(file_path, f"# {class_name}\n{content}\n\n## Source\n\nManually created documentation for Revit API.")
        
        # Extract properties and methods
        properties = []
        methods = []
        
        prop_section = re.search(r'## Properties\n(.*?)(?=##|\Z)', content, re.DOTALL)
        if prop_section:
            prop_lines = prop_section.group(1).strip().split('\n')
            for line in prop_lines:
                if line.startswith('- `'):
                    prop_name = re.search(r'`([^`]+)`', line).group(1)
                    prop_desc = line.split('`: ', 1)[1] if '`: ' in line else ""
                    properties.append({"name": prop_name, "description": prop_desc})
        
        method_section = re.search(r'## Methods\n(.*?)(?=##|\Z)', content, re.DOTALL)
        if method_section:
            method_lines = method_section.group(1).strip().split('\n')
            for line in method_lines:
                if line.startswith('- `'):
                    method_name = re.search(r'`([^`]+)`', line).group(1)
                    method_desc = line.split('`: ', 1)[1] if '`: ' in line else ""
                    methods.append({"name": method_name, "description": method_desc})
        
        # Create JSON structure
        class_info = {
            "name": class_name,
            "description": content.split('##')[0].strip(),
            "properties": properties,
            "methods": methods,
            "url": "Manual documentation"
        }
        
        # Save as JSON
        json_path = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(class_info, json_file, indent=2)
        
        print(f"Created manual documentation for {class_name}")

if __name__ == "__main__":
    print("Starting to scrape Revit API documentation...")
    
    print("Creating manual documentation for common classes...")
    create_manual_documentation()
    
    print("Attempting to scrape online documentation...")
    success_count = scrape_documentation()
    print(f"Successfully scraped {success_count} classes from the online documentation.")
    
    print("Creating index file...")
    create_index_file()
    
    print("Documentation created successfully!")
