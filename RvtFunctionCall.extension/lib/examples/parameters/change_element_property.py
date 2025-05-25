import clr
from Autodesk.Revit.DB import FilteredElementCollector, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, Level, Transaction, FamilyInstance, ElementId, ElementParameterFilter, ParameterValueProvider, FilterStringRule, BuiltInParameter, Parameter, StorageType, FilterNumericRuleEvaluator, FilterDoubleRule, FilterIntegerRule, FilterRule
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, Panel, TextBox, ComboBox, GroupBox, RadioButton, NumericUpDown, MessageBox, CheckBox, DataGridView, DataGridViewTextBoxColumn, DataGridViewRow, AutoSizeMode

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

class ParameterUpdateForm(Form):
    def __init__(self):
        self.InitializeComponent()
        self.selected_elements = None
        self.family_names = []
        
    def InitializeComponent(self):
        self.Text = "Update Parameter Values"
        self.Width = 500
        self.Height = 650
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Create family type selection
        self.lblFamilyTypes = Label()
        self.lblFamilyTypes.Text = "Enter Family Names (one per line):"
        self.lblFamilyTypes.Location = System.Drawing.Point(20, 20)
        self.lblFamilyTypes.AutoSize = True
        
        self.txtFamilyNames = TextBox()
        self.txtFamilyNames.Multiline = True
        self.txtFamilyNames.Location = System.Drawing.Point(20, 45)
        self.txtFamilyNames.Size = System.Drawing.Size(440, 150)
        self.txtFamilyNames.ScrollBars = System.Windows.Forms.ScrollBars.Vertical
        
        # Level selection
        self.lblLevel = Label()
        self.lblLevel.Text = "Filter by Level (optional):"
        self.lblLevel.Location = System.Drawing.Point(20, 205)
        self.lblLevel.AutoSize = True
        
        self.cboLevel = ComboBox()
        self.cboLevel.Location = System.Drawing.Point(20, 230)
        self.cboLevel.Size = System.Drawing.Size(200, 21)
        self.cboLevel.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        self.cboLevel.Items.Add("All Levels")
        for level in FilteredElementCollector(doc).OfClass(Level).ToElements():
            self.cboLevel.Items.Add(level.Name)
        self.cboLevel.SelectedIndex = 0
        
        # Parameter name
        self.lblParamName = Label()
        self.lblParamName.Text = "Parameter Name:"
        self.lblParamName.Location = System.Drawing.Point(20, 270)
        self.lblParamName.AutoSize = True
        
        self.txtParamName = TextBox()
        self.txtParamName.Location = System.Drawing.Point(20, 295)
        self.txtParamName.Size = System.Drawing.Size(440, 21)
        
        # Parameter value
        self.lblParamValue = Label()
        self.lblParamValue.Text = "New Parameter Value:"
        self.lblParamValue.Location = System.Drawing.Point(20, 330)
        self.lblParamValue.AutoSize = True
        
        self.txtParamValue = TextBox()
        self.txtParamValue.Location = System.Drawing.Point(20, 355)
        self.txtParamValue.Size = System.Drawing.Size(440, 21)
        
        # Preview checkbox
        self.chkPreview = CheckBox()
        self.chkPreview.Text = "Preview elements before updating"
        