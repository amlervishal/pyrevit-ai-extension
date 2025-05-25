"""
Move Elements by Distance and Direction
Move selected elements by a specified distance in a given direction.
"""
import clr
from Autodesk.Revit.DB import FilteredElementCollector, ElementId, Transform, XYZ, ElementTransformUtils, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, Level, Transaction
import System
from math import sin, cos, radians
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, NumericUpDown, RadioButton, ComboBox, Panel, MessageBox

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get all major categories to consider for moving
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

class MoveElementsForm(Form):
    def __init__(self):
        self.Text = "Move Elements by Distance and Direction"
        self.Width = 450
        self.Height = 500
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Use current selection checkbox
        self.chkUseSelection = System.Windows.Forms.CheckBox()
        self.chkUseSelection.Text = "Use current selection"
        self.chkUseSelection.Location = System.Drawing.Point(20, 20)
        self.chkUseSelection.Size = System.Drawing.Size(200, 20)
        self.chkUseSelection.Checked = True
        self.Controls.Add(self.chkUseSelection)
        
        # Category selection (disabled when using selection)
        lblCategories = Label()
        lblCategories.Text = "Categories to Move (if not using selection):"
        lblCategories.Location = System.Drawing.Point(20, 50)
        lblCategories.Width = 300
        self.Controls.Add(lblCategories)
        
        self.chkCategories = CheckedListBox()
        self.chkCategories.Location = System.Drawing.Point(20, 75)
        self.chkCategories.Width = 400
        self.chkCategories.Height = 120
        self.chkCategories.Enabled = False  # Disabled by default
        
        # Add categories to the checklist
        category_names = {
            BuiltInCategory.OST_Walls: "Walls",
            BuiltInCategory.OST_Floors: "Floors", 
            BuiltInCategory.OST_Furniture: "Furniture",
            BuiltInCategory.OST_Doors: "Doors",
            BuiltInCategory.OST_Windows: "Windows",
            BuiltInCategory.OST_GenericModel: "Generic Models"
        }
        
        for category in categories[:6]:  # Show only first 6 for space
            if category in category_names:
                self.chkCategories.Items.Add(category_names[category], CheckState.Checked)
            
        self.Controls.Add(self.chkCategories)
        
        # Source level selection (for category mode)
        lblSource = Label()
        lblSource.Text = "Source Level (for category mode):"
        lblSource.Location = System.Drawing.Point(20, 205)
        lblSource.Width = 200
        self.Controls.Add(lblSource)
        
        self.cmbSource = ComboBox()
        self.cmbSource.Location = System.Drawing.Point(230, 205)
        self.cmbSource.Width = 190
        self.cmbSource.Enabled = False
        levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
        level_names = sorted([level.Name for level in levels])
        self.cmbSource.Items.AddRange(level_names)
        self.cmbSource.DropDownStyle = ComboBox.DropDownStyle.DropDownList
        if self.cmbSource.Items.Count > 0:
            self.cmbSource.SelectedIndex = 0
        self.Controls.Add(self.cmbSource)
        
        # Distance input
        lblDistance = Label()
        lblDistance.Text = "Distance (ft):"
        lblDistance.Location = System.Drawing.Point(20, 240)
        lblDistance.Width = 100
        self.Controls.Add(lblDistance)
        
        self.numDistance = NumericUpDown()
        self.numDistance.Location = System.Drawing.Point(130, 240)
        self.numDistance.Width = 100
        self.numDistance.Minimum = System.Decimal(0.1)
        self.numDistance.Maximum = System.Decimal(1000)
        self.numDistance.Value = System.Decimal(5)
        self.numDistance.DecimalPlaces = 2
        self.Controls.Add(self.numDistance)
        
        # Direction selection
        lblDirection = Label()
        lblDirection.Text = "Direction:"
        lblDirection.Location = System.Drawing.Point(20, 280)
        lblDirection.Width = 100
        self.Controls.Add(lblDirection)
        
        # Direction radio buttons
        self.rdoX = RadioButton()
        self.rdoX.Text = "X (East)"
        self.rdoX.Location = System.Drawing.Point(130, 280)
        self.rdoX.Width = 80
        self.rdoX.Checked = True
        self.Controls.Add(self.rdoX)
        
        self.rdoY = RadioButton()
        self.rdoY.Text = "Y (North)"
        self.rdoY.Location = System.Drawing.Point(220, 280)
        self.rdoY.Width = 80
        self.Controls.Add(self.rdoY)
        
        self.rdoZ = RadioButton()
        self.rdoZ.Text = "Z (Up)"
        self.rdoZ.Location = System.Drawing.Point(310, 280)
        self.rdoZ.Width = 80
        self.Controls.Add(self.rdoZ)
        
        self.rdoNegX = RadioButton()
        self.rdoNegX.Text = "-X (West)"
        self.rdoNegX.Location = System.Drawing.Point(130, 310)
        self.rdoNegX.Width = 80
        self.Controls.Add(self.rdoNegX)
        
        self.rdoNegY = RadioButton()
        self.rdoNegY.Text = "-Y (South)"
        self.rdoNegY.Location = System.Drawing.Point(220, 310)
        self.rdoNegY.Width = 80
        self.Controls.Add(self.rdoNegY)
        
        self.rdoNegZ = RadioButton()
        self.rdoNegZ.Text = "-Z (Down)"
        self.rdoNegZ.Location = System.Drawing.Point(310, 310)
        self.rdoNegZ.Width = 80
        self.Controls.Add(self.rdoNegZ)
        
        # Move button
        btnMove = Button()
        btnMove.Text = "Move Elements"
        btnMove.Location = System.Drawing.Point(130, 360)
        btnMove.Width = 120
        btnMove.Click += self.MoveElements
        self.Controls.Add(btnMove)
        
        # Cancel button
        btnCancel = Button()
        btnCancel.Text = "Cancel"
        btnCancel.Location = System.Drawing.Point(270, 360)
        btnCancel.Width = 100
        btnCancel.Click += self.CancelForm
        self.Controls.Add(btnCancel)
        
        # Wire up checkbox event
        self.chkUseSelection.CheckedChanged += self.OnUseSelectionChanged
    
    def OnUseSelectionChanged(self, sender, e):
        use_selection = self.chkUseSelection.Checked
        self.chkCategories.Enabled = not use_selection
        self.cmbSource.Enabled = not use_selection
    
    def MoveElements(self, sender, e):
        # Get distance
        distance = float(self.numDistance.Value)
        
        # Get direction vector
        direction_vector = XYZ(0, 0, 0)
        if self.rdoX.Checked:
            direction_vector = XYZ(distance, 0, 0)
        elif self.rdoY.Checked:
            direction_vector = XYZ(0, distance, 0)
        elif self.rdoZ.Checked:
            direction_vector = XYZ(0, 0, distance)
        elif self.rdoNegX.Checked:
            direction_vector = XYZ(-distance, 0, 0)
        elif self.rdoNegY.Checked:
            direction_vector = XYZ(0, -distance, 0)
        elif self.rdoNegZ.Checked:
            direction_vector = XYZ(0, 0, -distance)
        
        # Get elements to move
        elements_to_move = []
        
        if self.chkUseSelection.Checked:
            # Use current selection
            selected_ids = uidoc.Selection.GetElementIds()
            if not selected_ids:
                MessageBox.Show("No elements are currently selected", "Selection Required")
                return
            elements_to_move = list(selected_ids)
        else:
            # Get elements by category and level
            if not any(self.chkCategories.GetItemChecked(i) for i in range(self.chkCategories.Items.Count)):
                MessageBox.Show("Please select at least one category", "Category Required")
                return
            
            source_level_name = self.cmbSource.SelectedItem
            if not source_level_name:
                MessageBox.Show("Please select a source level", "Level Required")
                return
            
            # Find source level
            levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
            source_level = None
            for level in levels:
                if level.Name == source_level_name:
                    source_level = level
                    break
            
            if not source_level:
                MessageBox.Show("Source level not found", "Error")
                return
            
            # Collect elements from selected categories
            for i in range(self.chkCategories.Items.Count):
                if self.chkCategories.GetItemChecked(i):
                    category_name = self.chkCategories.Items[i]
                    
                    # Map category name back to BuiltInCategory
                    category_map = {
                        "Walls": BuiltInCategory.OST_Walls,
                        "Floors": BuiltInCategory.OST_Floors,
                        "Furniture": BuiltInCategory.OST_Furniture,
                        "Doors": BuiltInCategory.OST_Doors,
                        "Windows": BuiltInCategory.OST_Windows,
                        "Generic Models": BuiltInCategory.OST_GenericModel
                    }
                    
                    if category_name in category_map:
                        category = category_map[category_name]
                        
                        # Create filters
                        category_filter = ElementCategoryFilter(category)
                        level_filter = ElementLevelFilter(source_level.Id)
                        combined_filter = LogicalAndFilter(category_filter, level_filter)
                        
                        # Collect elements
                        collector = FilteredElementCollector(doc).WherePasses(combined_filter).WhereElementIsNotElementType()
                        elements_to_move.extend([elem.Id for elem in collector])
        
        if not elements_to_move:
            MessageBox.Show("No elements found to move", "No Elements")
            return
        
        # Move elements
        with Transaction(doc, "Move Elements by Distance") as t:
            t.Start()
            
            try:
                element_ids = List[ElementId](elements_to_move)
                ElementTransformUtils.MoveElements(doc, element_ids, direction_vector)
                
                t.Commit()
                
                MessageBox.Show("Successfully moved {} elements".format(len(elements_to_move)), "Move Complete")
                self.DialogResult = DialogResult.OK
                self.Close()
                
            except Exception as ex:
                t.RollBack()
                MessageBox.Show("Error moving elements: {}".format(str(ex)), "Error")
    
    def CancelForm(self, sender, e):
        self.DialogResult = DialogResult.Cancel
        self.Close()

# Execute the form
form = MoveElementsForm()
form.ShowDialog()
