# -*- coding: utf-8 -*-
"""
Documentation lookup for Revit API
"""
import os

def find_relevant_context(query):
    """Return relevant Revit API context from documentation files"""
    try:
        current_dir = os.path.dirname(__file__)
        lib_dir = os.path.dirname(current_dir)
        docs_dir = os.path.join(lib_dir, 'revit_api_docs')
        
        context = {
            "documentation": [],
            "patterns": {}
        }
        
        quick_ref_path = os.path.join(docs_dir, 'quick_reference.py')
        if os.path.exists(quick_ref_path):
            try:
                with open(quick_ref_path, 'r') as f:
                    content = f.read()
                    context["documentation"].append({
                        "source": "quick_reference",
                        "content": content
                    })
            except Exception:
                pass
        
        core_dir = os.path.join(docs_dir, 'core')
        if os.path.exists(core_dir):
            document_path = os.path.join(core_dir, 'document.py')
            if os.path.exists(document_path):
                try:
                    with open(document_path, 'r') as f:
                        content = f.read()
                        context["documentation"].append({
                            "source": "core_document",
                            "content": content
                        })
                except Exception:
                    pass
        
        transactions_dir = os.path.join(docs_dir, 'transactions')
        if os.path.exists(transactions_dir):
            basic_trans_path = os.path.join(transactions_dir, 'basic_transactions.py')
            if os.path.exists(basic_trans_path):
                try:
                    with open(basic_trans_path, 'r') as f:
                        content = f.read()
                        context["documentation"].append({
                            "source": "basic_transactions",
                            "content": content
                        })
                except Exception:
                    pass
        
        selection_dir = os.path.join(docs_dir, 'selection')
        if os.path.exists(selection_dir):
            selection_path = os.path.join(selection_dir, 'selection.py')
            if os.path.exists(selection_path):
                try:
                    with open(selection_path, 'r') as f:
                        content = f.read()
                        context["documentation"].append({
                            "source": "selection_patterns",
                            "content": content
                        })
                except Exception:
                    pass
        
        elements_dir = os.path.join(docs_dir, 'elements')
        if os.path.exists(elements_dir):
            creation_path = os.path.join(elements_dir, 'creation.py')
            if os.path.exists(creation_path):
                try:
                    with open(creation_path, 'r') as f:
                        content = f.read()
                        context["documentation"].append({
                            "source": "element_creation",
                            "content": content
                        })
                except Exception:
                    pass
        
        if not context["documentation"]:
            context["documentation"].append({
                "source": "fallback_patterns",
                "content": """
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

with Transaction(doc, 'Operation') as t:
    t.Start()
    # code here
    t.Commit()

elements = FilteredElementCollector(doc).OfClass(Wall).ToElements()
selection = uidoc.Selection.GetElementIds()
param = element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
"""
            })
        
        return context
        
    except Exception as e:
        return {
            "documentation": [{
                "source": "error_fallback", 
                "content": "Basic Revit API patterns available"
            }],
            "patterns": {}
        }
