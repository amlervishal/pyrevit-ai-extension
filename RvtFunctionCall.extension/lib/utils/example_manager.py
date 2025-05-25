"""
Example Manager for Revit Function Call Extension - Complete Version
Manages and provides access to all example scripts with enhanced AI integration
"""
import os
import json
import re

class ExampleManager:
    def __init__(self, examples_dir):
        self.examples_dir = examples_dir
        self.examples_metadata = self._build_metadata()
    
    def _build_metadata(self):
        """Build metadata for all 18 example scripts"""
        metadata = {}
        
        # Define example categories and their metadata
        examples_data = {
            # SELECTION EXAMPLES
            "selection/select_by_family.py": {
                "title": "Select Elements by Family Name",
                "description": "Select elements by specifying family names with optional level filtering",
                "keywords": ["select", "family", "filter", "level", "family instance"],
                "category": "selection",
                "ui_components": ["form", "textbox", "combobox", "button"],
                "revit_classes": ["FilteredElementCollector", "FamilyInstance", "Level", "ElementLevelFilter"],
                "use_cases": ["select all chairs", "find specific families", "filter by level and family"],
                "parameters": {
                    "family_names": {"type": "string", "description": "List of family names to search for"},
                    "level": {"type": "string", "description": "Optional level filter", "optional": True}
                }
            },
            "selection/select_by_parameter.py": {
                "title": "Select Elements by Parameter Value",
                "description": "Select elements based on parameter values with category filtering",
                "keywords": ["select", "parameter", "value", "filter", "category"],
                "category": "selection", 
                "ui_components": ["form", "checkedlistbox", "textbox", "combobox"],
                "revit_classes": ["FilteredElementCollector", "Parameter", "ElementParameterFilter"],
                "use_cases": ["select by mark", "filter by parameter value", "find elements with specific properties"],
                "parameters": {
                    "parameter_name": {"type": "string", "description": "Name of parameter to filter by"},
                    "parameter_value": {"type": "string", "description": "Value to match"},
                    "categories": {"type": "list", "description": "Categories to search in"}
                }
            },
            "selection/select_by_level_category.py": {
                "title": "Select Elements by Level and Category",
                "description": "Select elements filtering by both level and category combinations",
                "keywords": ["select", "level", "category", "filter", "combination"],
                "category": "selection",
                "ui_components": ["form", "checkedlistbox", "combobox"],
                "revit_classes": ["FilteredElementCollector", "Level", "ElementCategoryFilter", "LogicalAndFilter"],
                "use_cases": ["select walls on specific level", "filter by level and category", "multi-criteria selection"],
                "parameters": {
                    "levels": {"type": "list", "description": "Levels to filter by"},
                    "categories": {"type": "list", "description": "Categories to include"}
                }
            },
            "selection/select_within_boundary.py": {
                "title": "Select Elements Within Boundary",
                "description": "Select elements that fall within a specified boundary or region",
                "keywords": ["select", "boundary", "region", "spatial", "filter"],
                "category": "selection",
                "ui_components": ["form", "checkedlistbox", "textbox"],
                "revit_classes": ["FilteredElementCollector", "BoundingBoxIntersectsFilter", "Outline"],
                "use_cases": ["select within room", "boundary selection", "spatial filtering"],
                "parameters": {
                    "boundary_points": {"type": "list", "description": "Points defining the boundary"},
                    "categories": {"type": "list", "description": "Categories to search in"}
                }
            },
            
            # MANIPULATION EXAMPLES
            "manipulation/align_to_elements.py": {
                "title": "Align Elements to Target Elements",
                "description": "Align multiple elements to target reference elements",
                "keywords": ["align", "move", "position", "target", "reference"],
                "category": "manipulation",
                "ui_components": ["form", "listbox", "radiobutton", "button"],
                "revit_classes": ["ElementTransformUtils", "Transform", "XYZ", "Transaction"],
                "use_cases": ["align furniture", "align to grid", "position elements"],
                "parameters": {
                    "source_elements": {"type": "list", "description": "Elements to align"},
                    "target_elements": {"type": "list", "description": "Reference elements for alignment"}
                }
            },
            "manipulation/align_to_reference.py": {
                "title": "Align Elements to Reference Line/Grid",
                "description": "Align elements to reference lines, grids, or other reference objects",
                "keywords": ["align", "reference", "grid", "line", "position"],
                "category": "manipulation",
                "ui_components": ["form", "combobox", "radiobutton"],
                "revit_classes": ["ElementTransformUtils", "Grid", "ReferencePlane", "Transform"],
                "use_cases": ["align to grid", "align to reference plane", "snap to reference"],
                "parameters": {
                    "elements": {"type": "list", "description": "Elements to align"},
                    "reference": {"type": "string", "description": "Reference object to align to"}
                }
            },
            "manipulation/move_by_distance.py": {
                "title": "Move Elements by Distance and Direction",
                "description": "Move elements by specified distance and direction",
                "keywords": ["move", "distance", "direction", "translate", "offset"],
                "category": "manipulation",
                "ui_components": ["form", "numericupdown", "combobox", "checkedlistbox"],
                "revit_classes": ["ElementTransformUtils", "XYZ", "Transform", "Transaction"],
                "use_cases": ["move furniture", "offset elements", "translate by distance"],
                "parameters": {
                    "distance": {"type": "double", "description": "Distance to move elements"},
                    "direction": {"type": "string", "description": "Direction (X, Y, Z)"},
                    "elements": {"type": "list", "description": "Elements to move"}
                }
            },
            "manipulation/move_to_level.py": {
                "title": "Move Elements to Different Level",
                "description": "Move elements from one level to another with proper level association",
                "keywords": ["move", "level", "transfer", "relocate"],
                "category": "manipulation",
                "ui_components": ["form", "combobox", "checkedlistbox"],
                "revit_classes": ["ElementTransformUtils", "Level", "Transform", "Transaction"],
                "use_cases": ["move to different floor", "relocate elements", "level transfer"],
                "parameters": {
                    "source_level": {"type": "string", "description": "Current level"},
                    "target_level": {"type": "string", "description": "Destination level"},
                    "elements": {"type": "list", "description": "Elements to move"}
                }
            },
            
            # COPYING EXAMPLES
            "copying/copy_to_levels.py": {
                "title": "Copy Elements to Multiple Levels",
                "description": "Copy selected elements from one level to multiple target levels",
                "keywords": ["copy", "level", "duplicate", "multiple levels"],
                "category": "copying",
                "ui_components": ["form", "combobox", "checkedlistbox", "textbox"],
                "revit_classes": ["ElementTransformUtils", "Level", "Transform", "CopyPasteOptions"],
                "use_cases": ["copy furniture to floors", "duplicate typical elements", "copy across levels"],
                "parameters": {
                    "source_level": {"type": "string", "description": "Source level name"},
                    "target_levels": {"type": "list", "description": "Target level names"}
                }
            },
            "copying/copy_multiple_spacing.py": {
                "title": "Copy Elements with Regular Spacing",
                "description": "Create multiple copies of elements with regular spacing intervals",
                "keywords": ["copy", "array", "spacing", "duplicate", "pattern", "regular"],
                "category": "copying",
                "ui_components": ["form", "numericupdown", "radiobutton"],
                "revit_classes": ["ElementTransformUtils", "XYZ", "Transform"],
                "use_cases": ["array furniture", "create patterns", "duplicate with spacing"],
                "parameters": {
                    "count": {"type": "integer", "description": "Number of copies"},
                    "spacing": {"type": "double", "description": "Distance between copies"},
                    "direction": {"type": "string", "description": "Direction for copying"}
                }
            },
            "copying/copy_to_distance.py": {
                "title": "Copy Elements to Specific Distance",
                "description": "Copy elements to a specific distance with offset options",
                "keywords": ["copy", "distance", "offset", "specific", "placement"],
                "category": "copying",
                "ui_components": ["form", "numericupdown", "combobox"],
                "revit_classes": ["ElementTransformUtils", "XYZ", "Transform"],
                "use_cases": ["copy at distance", "offset copying", "precise placement"],
                "parameters": {
                    "distance": {"type": "double", "description": "Distance for copying"},
                    "direction": {"type": "string", "description": "Copy direction"},
                    "offset": {"type": "double", "description": "Additional offset", "optional": True}
                }
            },
            "copying/copy_to_grid_intersection.py": {
                "title": "Copy Elements to Grid Intersections",
                "description": "Copy elements to intersections of selected grids",
                "keywords": ["copy", "grid", "intersection", "placement", "coordinate"],
                "category": "copying",
                "ui_components": ["form", "checkedlistbox", "combobox"],
                "revit_classes": ["ElementTransformUtils", "Grid", "XYZ", "Transform"],
                "use_cases": ["copy to grid points", "systematic placement", "grid-based copying"],
                "parameters": {
                    "grids_x": {"type": "list", "description": "X-direction grids"},
                    "grids_y": {"type": "list", "description": "Y-direction grids"},
                    "elements": {"type": "list", "description": "Elements to copy"}
                }
            },
            
            # CREATION EXAMPLES
            "creation/create_walls.py": {
                "title": "Create Walls",
                "description": "Create walls using various methods and parameters",
                "keywords": ["create", "wall", "new", "build", "construct"],
                "category": "creation",
                "ui_components": ["form", "combobox", "numericupdown"],
                "revit_classes": ["Wall", "WallType", "Level", "Line", "Transaction"],
                "use_cases": ["create simple wall", "build walls from lines", "new wall construction"],
                "parameters": {
                    "wall_type": {"type": "string", "description": "Wall type name"},
                    "height": {"type": "double", "description": "Wall height"},
                    "level": {"type": "string", "description": "Base level"}
                }
            },
            "creation/create_dimensions.py": {
                "title": "Create Dimensions",
                "description": "Create various types of dimensions between elements",
                "keywords": ["create", "dimension", "measure", "annotate"],
                "category": "creation",
                "ui_components": ["form", "combobox", "radiobutton"],
                "revit_classes": ["Dimension", "Transaction", "Reference", "Line"],
                "use_cases": ["dimension walls", "create annotations", "add measurements"],
                "parameters": {
                    "dimension_type": {"type": "string", "description": "Type of dimension"},
                    "elements": {"type": "list", "description": "Elements to dimension"}
                }
            },
            "creation/wall_from_model_lines.py": {
                "title": "Create Walls from Model Lines",
                "description": "Convert model lines into walls with specified parameters",
                "keywords": ["create", "wall", "model lines", "convert", "trace"],
                "category": "creation",
                "ui_components": ["form", "combobox", "numericupdown"],
                "revit_classes": ["Wall", "ModelLine", "CurveElement", "Transaction"],
                "use_cases": ["trace walls from lines", "convert lines to walls", "follow path"],
                "parameters": {
                    "model_lines": {"type": "list", "description": "Model lines to trace"},
                    "wall_type": {"type": "string", "description": "Wall type to create"},
                    "height": {"type": "double", "description": "Wall height"}
                }
            },
            
            # PARAMETER EXAMPLES
            "parameters/update_parameter_values.py": {
                "title": "Update Parameter Values",
                "description": "Update parameter values for selected elements",
                "keywords": ["parameter", "update", "modify", "value", "property"],
                "category": "parameters",
                "ui_components": ["form", "textbox", "combobox", "checkbox"],
                "revit_classes": ["Parameter", "FamilyInstance", "Transaction"],
                "use_cases": ["update marks", "modify properties", "batch parameter updates"],
                "parameters": {
                    "parameter_name": {"type": "string", "description": "Parameter name to update"},
                    "new_value": {"type": "string", "description": "New parameter value"},
                    "elements": {"type": "list", "description": "Elements to update"}
                }
            },
            "parameters/apply_setting_to_multiple.py": {
                "title": "Apply Settings to Multiple Elements",
                "description": "Apply the same parameter settings to multiple selected elements",
                "keywords": ["apply", "settings", "multiple", "batch", "parameter"],
                "category": "parameters",
                "ui_components": ["form", "textbox", "checkedlistbox"],
                "revit_classes": ["Parameter", "Transaction", "ElementId"],
                "use_cases": ["batch apply settings", "standardize parameters", "bulk updates"],
                "parameters": {
                    "settings": {"type": "dict", "description": "Settings to apply"},
                    "elements": {"type": "list", "description": "Target elements"}
                }
            },
            "parameters/change_element_property.py": {
                "title": "Change Element Properties",
                "description": "Change various properties of selected elements",
                "keywords": ["change", "property", "element", "modify", "attribute"],
                "category": "parameters",
                "ui_components": ["form", "textbox", "combobox"],
                "revit_classes": ["Element", "Parameter", "Transaction"],
                "use_cases": ["change element properties", "modify attributes", "update settings"],
                "parameters": {
                    "property_name": {"type": "string", "description": "Property to change"},
                    "new_value": {"type": "string", "description": "New property value"},
                    "elements": {"type": "list", "description": "Elements to modify"}
                }
            },
            
            # IMPORT/EXPORT EXAMPLES
            "import_export/cad_importer.py": {
                "title": "CAD Import Tool",
                "description": "Import CAD files with various options and settings",
                "keywords": ["import", "cad", "dwg", "dxf", "file"],
                "category": "import_export",
                "ui_components": ["form", "textbox", "combobox", "checkbox"],
                "revit_classes": ["ImportInstance", "DWGImportOptions", "Transaction"],
                "use_cases": ["import dwg files", "cad import", "external file import"],
                "parameters": {
                    "file_path": {"type": "string", "description": "Path to CAD file"},
                    "import_options": {"type": "dict", "description": "Import settings"}
                }
            },
            "import_export/custom_print_set.py": {
                "title": "Custom Print Set Creation",
                "description": "Create custom print sets with specified views and settings",
                "keywords": ["print", "export", "pdf", "views", "set"],
                "category": "import_export",
                "ui_components": ["form", "checkedlistbox", "textbox"],
                "revit_classes": ["ViewSet", "PrintManager", "PrintSetup"],
                "use_cases": ["create print sets", "batch printing", "export views"],
                "parameters": {
                    "views": {"type": "list", "description": "Views to include"},
                    "print_settings": {"type": "dict", "description": "Print configuration"}
                }
            }
        }
        
        return examples_data
    
    def find_relevant_examples(self, query, max_examples=3):
        """Find examples relevant to the user query"""
        query_lower = query.lower()
        
        # Score each example based on relevance
        scored_examples = []
        
        for example_path, metadata in self.examples_metadata.items():
            score = 0
            
            # Check title and description
            if any(word in metadata["title"].lower() for word in query_lower.split()):
                score += 3
            if any(word in metadata["description"].lower() for word in query_lower.split()):
                score += 2
            
            # Check keywords
            for keyword in metadata["keywords"]:
                if keyword.lower() in query_lower:
                    score += 2
            
            # Check use cases
            for use_case in metadata["use_cases"]:
                if any(word in use_case.lower() for word in query_lower.split()):
                    score += 1
            
            # Check Revit classes
            for revit_class in metadata["revit_classes"]:
                if revit_class.lower() in query_lower:
                    score += 2
            
            if score > 0:
                scored_examples.append((example_path, metadata, score))
        
        # Sort by score and return top examples
        scored_examples.sort(key=lambda x: x[2], reverse=True)
        return scored_examples[:max_examples]
    
    def get_example_content(self, example_path):
        """Get the content of an example script"""
        full_path = os.path.join(self.examples_dir, example_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                return ""
        return ""
    
    def get_example_patterns(self, query):
        """Extract common patterns from relevant examples"""
        relevant_examples = self.find_relevant_examples(query)
        
        patterns = {
            "ui_components": set(),
            "revit_classes": set(),
            "common_imports": set(),
            "transaction_patterns": [],
            "form_patterns": []
        }
        
        for example_path, metadata, score in relevant_examples:
            patterns["ui_components"].update(metadata["ui_components"])
            patterns["revit_classes"].update(metadata["revit_classes"])
            
            # Extract patterns from actual code
            content = self.get_example_content(example_path)
            if content:
                # Find import patterns
                import_lines = re.findall(r'^(?:from|import)\s+.*$', content, re.MULTILINE)
                patterns["common_imports"].update(import_lines)
                
                # Find transaction patterns
                transaction_matches = re.findall(r'(with\s+Transaction.*?:|Transaction\([^)]+\).*?)', content, re.MULTILINE)
                patterns["transaction_patterns"].extend(transaction_matches)
        
        # Convert sets to lists for JSON serialization
        patterns["ui_components"] = list(patterns["ui_components"])
        patterns["revit_classes"] = list(patterns["revit_classes"])  
        patterns["common_imports"] = list(patterns["common_imports"])
        
        return patterns
    
    def get_all_examples(self):
        """Get metadata for all examples"""
        return self.examples_metadata
    
    def get_examples_by_category(self, category):
        """Get examples filtered by category"""
        return {path: metadata for path, metadata in self.examples_metadata.items() 
                if metadata["category"] == category}
    
    def get_example_categories(self):
        """Get all available categories"""
        categories = set()
        for metadata in self.examples_metadata.values():
            categories.add(metadata["category"])
        return sorted(list(categories))
    
    def search_examples(self, search_term):
        """Search examples by term in title, description, or keywords"""
        search_lower = search_term.lower()
        matching_examples = []
        
        for example_path, metadata in self.examples_metadata.items():
            if (search_lower in metadata["title"].lower() or 
                search_lower in metadata["description"].lower() or
                any(search_lower in keyword.lower() for keyword in metadata["keywords"])):
                matching_examples.append((example_path, metadata))
        
        return matching_examples
