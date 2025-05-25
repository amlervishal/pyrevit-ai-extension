# This script imports a CAD file into Revit

import clr
import os
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Windows.Forms import OpenFileDialog, DialogResult

# Get the current Revit document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to get CAD file from user
def get_cad_file():
    dialog = OpenFileDialog()
    dialog.Filter = "CAD Files (*.dwg;*.dxf)|*.dwg;*.dxf|All files (*.*)|*.*"
    dialog.Title = "Select CAD File to Import"
    
    if dialog.ShowDialog() == DialogResult.OK:
        return dialog.FileName
    return None

# Main execution
cad_file = get_cad_file()

if cad_file:
    # Create import options
    options = DWGImportOptions()
    options.AutoCADVersion = ACADVersion.Default
    options.Placement = ImportPlacement.Origin
    options.ThisViewOnly = False
    options.ColorMode = ImportColorMode.BlackAndWhite
    options.CustomScale = 1.0
    
    # Start transaction
    t = Transaction(doc, "Import CAD")
    t.Start()
    
    try:
        # Import the CAD file
        doc.Import(cad_file, options, doc.ActiveView)
        t.Commit()
        TaskDialog.Show("Success", "CAD file was successfully imported into Revit.")
    except Exception as e:
        t.RollBack()
        TaskDialog.Show("Error", "Failed to import CAD file.\n" + str(e))
else:
    TaskDialog.Show("Cancelled", "Operation was cancelled by user.")