# -*- coding: utf-8 -*-
"""
Agentic Task Understanding for Revit Operations
Analyzes user queries and formulates specific tasks
"""

def understand_and_formulate_tasks(query):
    """
    Analyze user query to understand intent and formulate specific tasks
    Returns structured task information for better code generation
    """
    query_lower = query.lower()
    
    # Task analysis patterns
    task_analysis = {
        "primary_action": None,
        "target_elements": [],
        "parameters": {},
        "complexity": "simple",
        "requires_selection": False,
        "requires_transaction": False,
        "suggested_approach": ""
    }
    
    # Identify primary actions
    if any(word in query_lower for word in ["create", "make", "add", "new", "generate"]):
        task_analysis["primary_action"] = "create"
        task_analysis["requires_transaction"] = True
        
    elif any(word in query_lower for word in ["select", "find", "get", "collect", "filter"]):
        task_analysis["primary_action"] = "select"
        task_analysis["requires_selection"] = False
        
    elif any(word in query_lower for word in ["move", "copy", "rotate", "modify", "change", "update"]):
        task_analysis["primary_action"] = "modify"
        task_analysis["requires_selection"] = True
        task_analysis["requires_transaction"] = True
        
    elif any(word in query_lower for word in ["delete", "remove", "erase"]):
        task_analysis["primary_action"] = "delete"
        task_analysis["requires_selection"] = True
        task_analysis["requires_transaction"] = True
        
    elif any(word in query_lower for word in ["list", "show", "display", "report", "analyze"]):
        task_analysis["primary_action"] = "analyze"
        
    # Identify target elements
    element_types = {
        "walls": ["wall", "walls"],
        "doors": ["door", "doors"], 
        "windows": ["window", "windows"],
        "floors": ["floor", "floors", "slab"],
        "ceilings": ["ceiling", "ceilings"],
        "rooms": ["room", "rooms", "space", "spaces"],
        "grids": ["grid", "grids", "gridline"],
        "levels": ["level", "levels"],
        "families": ["family", "families", "family instance"],
        "elements": ["element", "elements", "component", "components"]
    }
    
    for element_type, keywords in element_types.items():
        if any(keyword in query_lower for keyword in keywords):
            task_analysis["target_elements"].append(element_type)
    
    # Identify parameters and values
    parameter_indicators = {
        "height": ["height", "tall", "elevation"],
        "width": ["width", "wide", "thickness"],
        "length": ["length", "long", "distance"],
        "location": ["location", "position", "coordinate", "point"],
        "material": ["material", "finish"],
        "type": ["type", "family", "style"],
        "level": ["level", "floor"],
        "name": ["name", "tag", "mark", "label"]
    }
    
    for param, keywords in parameter_indicators.items():
        if any(keyword in query_lower for keyword in keywords):
            task_analysis["parameters"][param] = True
    
    # Determine complexity
    complexity_indicators = {
        "complex": ["all", "multiple", "batch", "many", "every", "loop", "iterate"],
        "simple": ["one", "single", "this", "selected"]
    }
    
    for complexity, keywords in complexity_indicators.items():
        if any(keyword in query_lower for keyword in keywords):
            task_analysis["complexity"] = complexity
            break
    
    # Generate suggested approach based on analysis
    if task_analysis["primary_action"] == "create":
        if task_analysis["target_elements"]:
            task_analysis["suggested_approach"] = "Use Revit creation API with transaction for {}".format(
                ", ".join(task_analysis["target_elements"])
            )
        else:
            task_analysis["suggested_approach"] = "Create new Revit elements with proper transaction handling"
            
    elif task_analysis["primary_action"] == "select":
        task_analysis["suggested_approach"] = "Use FilteredElementCollector with appropriate filters"
        
    elif task_analysis["primary_action"] == "modify":
        task_analysis["suggested_approach"] = "Get selected elements, modify properties in transaction"
        
    elif task_analysis["primary_action"] == "delete":
        task_analysis["suggested_approach"] = "Get elements to delete, use doc.Delete() in transaction"
        
    elif task_analysis["primary_action"] == "analyze":
        task_analysis["suggested_approach"] = "Collect elements and analyze properties, display results"
    
    return task_analysis

def formulate_enhanced_query(original_query, task_analysis):
    """
    Create an enhanced query for the AI agent based on task analysis
    """
    enhanced_parts = [
        "TASK: {}".format(original_query),
        "",
        "ANALYSIS:",
        "- Primary Action: {}".format(task_analysis["primary_action"] or "general"),
        "- Target Elements: {}".format(", ".join(task_analysis["target_elements"]) if task_analysis["target_elements"] else "unspecified"),
        "- Complexity: {}".format(task_analysis["complexity"]),
        "- Requires Selection: {}".format(task_analysis["requires_selection"]),
        "- Requires Transaction: {}".format(task_analysis["requires_transaction"]),
        "- Suggested Approach: {}".format(task_analysis["suggested_approach"]),
    ]
    
    if task_analysis["parameters"]:
        enhanced_parts.append("- Parameters Involved: {}".format(", ".join(task_analysis["parameters"].keys())))
    
    enhanced_parts.extend([
        "",
        "Generate IronPython 2.7 code that implements this task using the suggested approach."
    ])
    
    return "\n".join(enhanced_parts)
