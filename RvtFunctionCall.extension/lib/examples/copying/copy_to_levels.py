"""
Copy Elements to Multiple Levels
Copy selected elements from one level to multiple target levels with proper level adjustment.
"""
import clr
from Autodesk.Revit.DB import FilteredElementCollector, ElementId, Transform, XYZ, CopyPasteOptions, ElementTransformUtils, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, View, Level, Transaction
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, TextBox, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, ComboBox, MessageBox

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get all levels in the document
levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
level_dict = {level.Name: level for level in levels}

class CopyToLevelsForm(Form):
    def __init__(self, levels):
        self.Text = "Copy Elements to Levels"
        self.Width = 500
        self.Height = 400
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        self.level_names = sorted([level.Name for level in levels])
        
        # Source level selection
        lblSource = Label()
        lblSource.Text = "Source Level:"
        lblSource.Location = System.Drawing.Point(20, 20)
        lblSource.Width = 100
        self.Controls.Add(lblSource)
        
        self.cmbSource = ComboBox()
        self.cmbSource.Location = System.Drawing.Point(130, 20)
        self.cmbSource.Width = 250
        self.cmbSource.Items.AddRange(self.level_names)
        self.cmbSource.DropDownStyle = ComboBox.DropDownStyle.DropDownList
        self.Controls.Add(self.cmbSource)
        
        # Target levels selection
        lblTarget = Label()
        lblTarget.Text = "Target Levels:"
        lblTarget.Location = System.Drawing.Point(20, 60)
        lblTarget.Width = 100
        self.Controls.Add(lblTarget)
        
        self.chkTargets = CheckedListBox()
        self.chkTargets.Location = System.Drawing.Point(130, 60)
        self.chkTargets.Width = 250
        self.chkTargets.Height = 150
        self.chkTargets.Items.AddRange(self.level_names)
        self.Controls.Add(self.chkTargets)
        
        # Target levels text input (alternative)
        lblTargetText = Label()
        lblTargetText.Text = "Or enter level names (comma-separated):"
        lblTargetText.Location = System.Drawing.Point(20, 220)
        lblTargetText.Width = 220
        self.Controls.Add(lblTargetText)
        
        self.txtTargetLevels = TextBox()
        self.txtTargetLevels.Location = System.Drawing.Point(250, 220)
        self.txtTargetLevels.Width = 230
        self.txtTargetLevels.Text = ""
        self.Controls.Add(self.txtTargetLevels)
        
        # OK button
        btnOK = Button()
        btnOK.Text = "Copy Elements"
        btnOK.Location = System.Drawing.Point(250, 260)
        btnOK.Width = 120
        btnOK.Click += self.OnOK
        self.Controls.Add(btnOK)
        
        # Cancel button
        btnCancel = Button()
        btnCancel.Text = "Cancel"
        btnCancel.Location = System.Drawing.Point(380, 260)
        btnCancel.Width = 100
        btnCancel.Click += self.OnCancel
        self.Controls.Add(btnCancel)
    
    def OnOK(self, sender, e):
        if not self.cmbSource.SelectedItem:
            MessageBox.Show("Please select a source level", "Selection Required")
            return
        
        # Get target levels from checkboxes or text input
        target_levels = []
        
        # First try checkboxes
        for i in range(self.chkTargets.Items.Count):
            if self.chkTargets.GetItemChecked(i):
                target_levels.append(self.chkTargets.Items[i])
        
        # If no checkboxes selected, try text input
        if not target_levels and self.txtTargetLevels.Text.strip():
            target_levels = [name.strip() for name in self.txtTargetLevels.Text.split(',') if name.strip()]
        
        if not target_levels:
            MessageBox.Show("Please select target levels", "Selection Required")
            return
        
        self.source_level = self.cmbSource.SelectedItem
        self.target_levels = target_levels
        self.DialogResult = DialogResult.OK
        self.Close()
    
    def OnCancel(self, sender, e):
        self.DialogResult = DialogResult.Cancel
        self.Close()

def copy_elements_to_levels():
    # Show the form
    form = CopyToLevelsForm(levels)
    result = form.ShowDialog()
    
    if result != DialogResult.OK:
        return
    
    source_level_name = form.source_level
    target_level_names = form.target_levels
    
    # Get level objects
    source_level = level_dict.get(source_level_name)
    target_levels = [level_dict.get(name) for name in target_level_names if name in level_dict]
    
    if not source_level:
        MessageBox.Show("Source level not found", "Error")
        return
    
    if not target_levels:
        MessageBox.Show("No valid target levels found", "Error")
        return
    
    # Get elements from current selection or from source level
    selected_element_ids = uidoc.Selection.GetElementIds()
    
    if not selected_element_ids:
        MessageBox.Show("Please select elements to copy", "Selection Required")
        return
    
    # Start transaction
    with Transaction(doc, "Copy Elements to Levels") as t:
        t.Start()
        
        copied_count = 0
        
        for target_level in target_levels:
            if target_level.Id == source_level.Id:
                continue  # Skip if same as source level
            
            # Calculate vertical offset
            vertical_offset = target_level.Elevation - source_level.Elevation
            translation_vector = XYZ(0, 0, vertical_offset)
            
            try:
                # Copy elements
                new_element_ids = ElementTransformUtils.CopyElements(
                    doc, 
                    selected_element_ids, 
                    translation_vector
                )
                
                copied_count += len(new_element_ids)
                
            except Exception as ex:
                MessageBox.Show("Error copying to level {}: {}".format(target_level.Name, str(ex)), "Copy Error")
        
        t.Commit()
        
        if copied_count > 0:
            MessageBox.Show("Successfully copied {} elements to {} levels".format(
                len(selected_element_ids), len(target_levels)), "Copy Complete")
        else:
            MessageBox.Show("No elements were copied", "Copy Failed")

# Execute the function
copy_elements_to_levels()
