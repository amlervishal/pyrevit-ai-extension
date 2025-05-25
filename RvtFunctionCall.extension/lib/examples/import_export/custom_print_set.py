import clr
import System
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collect all sheets in the project
collector = FilteredElementCollector(doc).OfClass(ViewSheet)
all_sheets = collector.ToElements()

# Create a dictionary to store sheets by number
sheets_by_number = {}
for sheet in all_sheets:
    sheet_number = sheet.SheetNumber
    sheets_by_number[sheet_number] = sheet

# Get sheet numbers from user
sheet_numbers_input = TaskDialog.Show("Print Set", "Enter sheet numbers separated by commas:", TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel)

if sheet_numbers_input == TaskDialogResult.Cancel:
    exit()

# Get list of sheet numbers
sheet_numbers = [num.strip() for num in TaskDialog.GetValue().split(',')]

# Create a list of sheet IDs to print
sheet_ids = List[ElementId]()
not_found_numbers = []

for number in sheet_numbers:
    if number in sheets_by_number:
        sheet_ids.Add(sheets_by_number[number].Id)
    else:
        not_found_numbers.append(number)

# Notify about sheets not found
if not_found_numbers:
    TaskDialog.Show("Warning", "The following sheets were not found: " + ", ".join(not_found_numbers))

# Check if we have sheets to print
if sheet_ids.Count == 0:
    TaskDialog.Show("Error", "No valid sheets were specified.")
    exit()

# Create a print set
t = Transaction(doc, "Create Print Set")
t.Start()

# Create a view set
print_set = ViewSet()
for sheet_id in sheet_ids:
    print_set.Insert(doc.GetElement(sheet_id))

# Get the print manager
print_manager = doc.PrintManager
print_manager.PrintRange = PrintRange.Select

# Apply print setup
view_sheet_setting = print_manager.ViewSheetSetting
view_sheet_setting.CurrentViewSheetSet.Views = print_set

# Save the view set
view_sheet_setting.SaveAs("Custom Print Set")

t.Commit()

TaskDialog.Show("Success", "Print set created successfully with " + str(sheet_ids.Count) + " sheets.")