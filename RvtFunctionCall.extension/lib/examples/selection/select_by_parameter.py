"""
Select Elements by Parameter Value
Allows selection of elements based on parameter values with category filtering.
"""
import clr
from Autodesk.Revit.DB import FilteredElementCollector, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, Level, ParameterValueProvider, ElementId, FilterStringRule, FilterNumericRule, FilterDoubleRule, FilterIntegerRule, ElementParameterFilter, ParameterFilterRuleFactory
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, Panel, TextBox, ComboBox, GroupBox, RadioButton, NumericUpDown, MessageBox

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get all major categories to consider
categories = [
    BuiltInCategory.OST_Walls,
    BuiltInCategory.OST_Floors,
    BuiltInCategory.OST_StructuralFraming,
    BuiltInCategory.OST_Furniture,
    BuiltInCategory.OST_Doors,
    BuiltInCategory.OST_Windows,
    BuiltInCategory.OST_GenericModel,
    BuiltInCategory.OST_ElectricalFixtures,
    BuiltInCategory.OST_ElectricalEquipment,
    BuiltInCategory.OST_MechanicalEquipment,
    BuiltInCategory.OST_PlumbingFixtures,
    BuiltInCategory.OST_Casework,
    BuiltInCategory.OST_Columns,
    BuiltInCategory.OST_Ceilings
]

category_names = {
    BuiltInCategory.OST_Walls: "Walls",
    BuiltInCategory.OST_Floors: "Floors",
    BuiltInCategory.OST_StructuralFraming: "Structural Framing",
    BuiltInCategory.OST_Furniture: "Furniture",
    BuiltInCategory.OST_Doors: "Doors",
    BuiltInCategory.OST_Windows: "Windows",
    BuiltInCategory.OST_GenericModel: "Generic Models",
    BuiltInCategory.OST_ElectricalFixtures: "Electrical Fixtures",
    BuiltInCategory.OST_ElectricalEquipment: "Electrical Equipment",
    BuiltInCategory.OST_MechanicalEquipment: "Mechanical Equipment",
    BuiltInCategory.OST_PlumbingFixtures: "Plumbing Fixtures",
    BuiltInCategory.OST_Casework: "Casework",
    BuiltInCategory.OST_Columns: "Columns",
    BuiltInCategory.OST_Ceilings: "Ceilings"
}

class SelectByParameterForm(Form):
    def __init__(self):
        self.InitializeComponent()
        self.selected_elements = None
    
    def InitializeComponent(self):
        self.Text = "Select by Parameter Value"
        self.Width = 500
        self.Height = 600
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Create category selection
        self.lblCategories = Label()
        self.lblCategories.Text = "Select Categories:"
        self.lblCategories.Location = System.Drawing.Point(20, 20)
        self.lblCategories.AutoSize = True
        
        self.checkedListCategories = CheckedListBox()
        self.checkedListCategories.Location = System.Drawing.Point(20, 45)
        self.checkedListCategories.Size = System.Drawing.Size(200, 250)
        self.checkedListCategories.CheckOnClick = True
        
        # Add categories to the list
        for category in categories:
            self.checkedListCategories.Items.Add(category_names[category])
        
        # Parameter name input
        self.lblParameterName = Label()
        self.lblParameterName.Text = "Parameter Name:"
        self.lblParameterName.Location = System.Drawing.Point(240, 45)
        self.lblParameterName.AutoSize = True
        
        self.txtParameterName = TextBox()
        self.txtParameterName.Location = System.Drawing.Point(240, 70)
        self.txtParameterName.Size = System.Drawing.Size(220, 21)
        
        # Parameter value input
        self.lblParameterValue = Label()
        self.lblParameterValue.Text = "Parameter Value:"
        self.lblParameterValue.Location = System.Drawing.Point(240, 105)
        self.lblParameterValue.AutoSize = True
        
        self.txtParameterValue = TextBox()
        self.txtParameterValue.Location = System.Drawing.Point(240, 130)
        self.txtParameterValue.Size = System.Drawing.Size(220, 21)
        
        # Buttons
        self.btnSelect = Button()
        self.btnSelect.Text = "Select Elements"
        self.btnSelect.Location = System.Drawing.Point(240, 200)
        self.btnSelect.Size = System.Drawing.Size(150, 30)
        self.btnSelect.Click += self.SelectElements
        
        self.btnCancel = Button()
        self.btnCancel.Text = "Cancel"
        self.btnCancel.Location = System.Drawing.Point(240, 240)
        self.btnCancel.Size = System.Drawing.Size(150, 30)
        self.btnCancel.Click += self.CancelForm
        
        # Add controls to form
        self.Controls.Add(self.lblCategories)
        self.Controls.Add(self.checkedListCategories)
        self.Controls.Add(self.lblParameterName)
        self.Controls.Add(self.txtParameterName)
        self.Controls.Add(self.lblParameterValue)
        self.Controls.Add(self.txtParameterValue)
        self.Controls.Add(self.btnSelect)
        self.Controls.Add(self.btnCancel)
    
    def SelectElements(self, sender, e):
        parameter_name = self.txtParameterName.Text.strip()
        parameter_value = self.txtParameterValue.Text.strip()
        
        if not parameter_name or not parameter_value:
            MessageBox.Show("Please enter both parameter name and value", "Input Required")
            return
        
        # Get selected categories
        selected_categories = []
        for i in range(self.checkedListCategories.Items.Count):
            if self.checkedListCategories.GetItemChecked(i):
                category_name = self.checkedListCategories.Items[i]
                for cat, name in category_names.items():
                    if name == category_name:
                        selected_categories.append(cat)
                        break
        
        if not selected_categories:
            MessageBox.Show("Please select at least one category", "Selection Required")
            return
        
        # Collect elements from selected categories
        matching_elements = []
        
        for category in selected_categories:
            collector = FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType()
            
            for element in collector:
                try:
                    # Look for the parameter
                    param = element.LookupParameter(parameter_name)
                    if param and param.HasValue:
                        if param.AsString() == parameter_value:
                            matching_elements.append(element)
                        elif str(param.AsValueString()) == parameter_value:
                            matching_elements.append(element)
                except:
                    continue
        
        if matching_elements:
            # Select the elements
            element_ids = List[ElementId]([elem.Id for elem in matching_elements])
            uidoc.Selection.SetElementIds(element_ids)
            MessageBox.Show("Selected {} elements".format(len(matching_elements)), "Selection Complete")
        else:
            MessageBox.Show("No elements found with the specified parameter value", "No Results")
        
        self.DialogResult = DialogResult.OK
        self.Close()
    
    def CancelForm(self, sender, e):
        self.DialogResult = DialogResult.Cancel
        self.Close()

# Execute the form
form = SelectByParameterForm()
form.ShowDialog()
