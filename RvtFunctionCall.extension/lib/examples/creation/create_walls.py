"""
Create Walls Example
Demonstrates various methods for creating walls in Revit with different parameters.
"""
import clr
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, ComboBox, NumericUpDown, TextBox, MessageBox
import System

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

class CreateWallForm(Form):
    def __init__(self):
        self.Text = "Create Wall"
        self.Width = 400
        self.Height = 350
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Wall Type selection
        lblWallType = Label()
        lblWallType.Text = "Wall Type:"
        lblWallType.Location = System.Drawing.Point(20, 20)
        lblWallType.Width = 100
        self.Controls.Add(lblWallType)
        
        self.cmbWallType = ComboBox()
        self.cmbWallType.Location = System.Drawing.Point(130, 20)
        self.cmbWallType.Width = 220
        self.cmbWallType.DropDownStyle = ComboBox.DropDownStyle.DropDownList
        
        # Populate wall types
        wall_types = FilteredElementCollector(doc).OfClass(WallType).ToElements()
        for wall_type in wall_types:
            self.cmbWallType.Items.Add(wall_type.Name)
        
        if self.cmbWallType.Items.Count > 0:
            self.cmbWallType.SelectedIndex = 0
        
        self.Controls.Add(self.cmbWallType)
        
        # Level selection
        lblLevel = Label()
        lblLevel.Text = "Level:"
        lblLevel.Location = System.Drawing.Point(20, 60)
        lblLevel.Width = 100
        self.Controls.Add(lblLevel)
        
        self.cmbLevel = ComboBox()
        self.cmbLevel.Location = System.Drawing.Point(130, 60)
        self.cmbLevel.Width = 220
        self.cmbLevel.DropDownStyle = ComboBox.DropDownStyle.DropDownList
        
        # Populate levels
        levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
        for level in levels:
            self.cmbLevel.Items.Add(level.Name)
        
        if self.cmbLevel.Items.Count > 0:
            self.cmbLevel.SelectedIndex = 0
        
        self.Controls.Add(self.cmbLevel)
        
        # Wall height
        lblHeight = Label()
        lblHeight.Text = "Height (ft):"
        lblHeight.Location = System.Drawing.Point(20, 100)
        lblHeight.Width = 100
        self.Controls.Add(lblHeight)
        
        self.numHeight = NumericUpDown()
        self.numHeight.Location = System.Drawing.Point(130, 100)
        self.numHeight.Width = 100
        self.numHeight.Minimum = System.Decimal(1)
        self.numHeight.Maximum = System.Decimal(100)
        self.numHeight.Value = System.Decimal(10)
        self.numHeight.DecimalPlaces = 1
        self.Controls.Add(self.numHeight)
        
        # Start point coordinates
        lblStart = Label()
        lblStart.Text = "Start Point (X, Y):"
        lblStart.Location = System.Drawing.Point(20, 140)
        lblStart.Width = 100
        self.Controls.Add(lblStart)
        
        self.txtStartX = TextBox()
        self.txtStartX.Location = System.Drawing.Point(130, 140)
        self.txtStartX.Width = 60
        self.txtStartX.Text = "0"
        self.Controls.Add(self.txtStartX)
        
        self.txtStartY = TextBox()
        self.txtStartY.Location = System.Drawing.Point(200, 140)
        self.txtStartY.Width = 60
        self.txtStartY.Text = "0"
        self.Controls.Add(self.txtStartY)
        
        # End point coordinates  
        lblEnd = Label()
        lblEnd.Text = "End Point (X, Y):"
        lblEnd.Location = System.Drawing.Point(20, 180)
        lblEnd.Width = 100
        self.Controls.Add(lblEnd)
        
        self.txtEndX = TextBox()
        self.txtEndX.Location = System.Drawing.Point(130, 180)
        self.txtEndX.Width = 60
        self.txtEndX.Text = "10"
        self.Controls.Add(self.txtEndX)
        
        self.txtEndY = TextBox()
        self.txtEndY.Location = System.Drawing.Point(200, 180)
        self.txtEndY.Width = 60
        self.txtEndY.Text = "0"
        self.Controls.Add(self.txtEndY)
        
        # Create button
        btnCreate = Button()
        btnCreate.Text = "Create Wall"
        btnCreate.Location = System.Drawing.Point(130, 230)
        btnCreate.Width = 100
        btnCreate.Click += self.CreateWall
        self.Controls.Add(btnCreate)
        
        # Cancel button
        btnCancel = Button()
        btnCancel.Text = "Cancel"
        btnCancel.Location = System.Drawing.Point(240, 230)
        btnCancel.Width = 100
        btnCancel.Click += self.CancelForm
        self.Controls.Add(btnCancel)
    
    def CreateWall(self, sender, e):
        try:
            # Get selected wall type
            wall_type_name = self.cmbWallType.SelectedItem
            wall_types = FilteredElementCollector(doc).OfClass(WallType).ToElements()
            selected_wall_type = None
            
            for wall_type in wall_types:
                if wall_type.Name == wall_type_name:
                    selected_wall_type = wall_type
                    break
            
            if not selected_wall_type:
                MessageBox.Show("Wall type not found", "Error")
                return
            
            # Get selected level
            level_name = self.cmbLevel.SelectedItem
            levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
            selected_level = None
            
            for level in levels:
                if level.Name == level_name:
                    selected_level = level
                    break
            
            if not selected_level:
                MessageBox.Show("Level not found", "Error")
                return
            
            # Get coordinates
            start_x = float(self.txtStartX.Text)
            start_y = float(self.txtStartY.Text)
            end_x = float(self.txtEndX.Text)
            end_y = float(self.txtEndY.Text)
            height = float(self.numHeight.Value)
            
            # Create wall curve
            start_point = XYZ(start_x, start_y, 0)
            end_point = XYZ(end_x, end_y, 0)
            curve = Line.CreateBound(start_point, end_point)
            
            # Start transaction
            with Transaction(doc, "Create Wall") as t:
                t.Start()
                
                # Create the wall
                wall = Wall.Create(doc, curve, selected_wall_type.Id, selected_level.Id, height, 0, False, False)
                
                t.Commit()
                
                MessageBox.Show("Wall created successfully!", "Success")
                self.DialogResult = DialogResult.OK
                self.Close()
                
        except Exception as ex:
            MessageBox.Show("Error creating wall: {}".format(str(ex)), "Error")
    
    def CancelForm(self, sender, e):
        self.DialogResult = DialogResult.Cancel
        self.Close()

# Execute the form
form = CreateWallForm()
form.ShowDialog()
