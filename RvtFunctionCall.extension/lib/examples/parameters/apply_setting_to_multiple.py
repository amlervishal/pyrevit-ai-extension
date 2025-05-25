import clr
from Autodesk.Revit.DB import FilteredElementCollector, ElementLevelFilter, ElementCategoryFilter, BuiltInCategory, LogicalAndFilter, Level, Transaction, FamilyInstance, ElementId, ElementParameterFilter, ParameterValueProvider, FilterStringRule, BuiltInParameter, Parameter, StorageType, FilterNumericRuleEvaluator, FilterDoubleRule, FilterIntegerRule, FilterRule
import System
from System.Collections.Generic import List, Dictionary
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, CheckedListBox, CheckState, Panel, TextBox, ComboBox, GroupBox, RadioButton, NumericUpDown, MessageBox, CheckBox, DataGridView, DataGridViewTextBoxColumn, DataGridViewRow, AutoSizeMode, ColumnHeaderStyle

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

class ParameterUpdateForm(Form):
    def __init__(self):
        self.InitializeComponent()
        self.template_element = None
        self.target_elements = []
        self.parameter_map = Dictionary[str, object]()
        
    def InitializeComponent(self):
        self.Text = "Update Parameter Values"
        self.Width = 700
        self.Height = 650
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.StartPosition = StartPosition.CenterScreen
        
        # Template element selection
        self.lblTemplate = Label()
        self.lblTemplate.Text = "Select a template element:"
        self.lblTemplate.Location = System.Drawing.Point(20, 20)
        self.lblTemplate.AutoSize = True
        
        self.btnSelectTemplate = Button()
        self.btnSelectTemplate.Text = "Select Template Element"
        self.btnSelectTemplate.Location = System.Drawing.Point(20, 45)
        self.btnSelectTemplate.Size = System.Drawing.Size(200, 30)
        self.btnSelectTemplate.Click += self.SelectTemplateElement
        
        self.lblTemplateInfo = Label()
        self.lblTemplateInfo.Text = "No template element selected"
        self.lblTemplateInfo.Location = System.Drawing.Point(230, 50)
        self.lblTemplateInfo.AutoSize = True
        
        # Parameter grid view
        self.lblParameters = Label()
        self.lblParameters.Text = "Parameters to apply:"
        self.lblParameters.Location = System.Drawing.Point(20, 90)
        self.lblParameters.AutoSize = True
        
        self.paramGrid = DataGridView()
        self.paramGrid.Location = System.Drawing.Point(20, 115)
        self.paramGrid.Size = System.Drawing.Size(650, 200)
        self.paramGrid.AutoGenerateColumns = False
        self.paramGrid.AllowUserToAddRows = False
        self.paramGrid.AllowUserToDeleteRows = False
        self.paramGrid.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect
        self.paramGrid.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
        
        checkColumn = DataGridViewCheckBoxColumn()
        checkColumn.HeaderText = "Apply"
        checkColumn.Width = 50
        checkColumn.Name = "Apply"
        
        nameColumn = DataGridViewTextBoxColumn()
        nameColumn.HeaderText = "Parameter Name"
        nameColumn.Width = 200
        nameColumn.Name = "Name"
        nameColumn.ReadOnly = True
        
        valueColumn = DataGridViewTextBoxColumn()
        valueColumn.HeaderText = "Value"
        valueColumn.Width = 350
        valueColumn.Name = "Value"
        valueColumn.ReadOnly = True
        
        self.paramGrid.Columns.Add(checkColumn)
        self.paramGrid.Columns.Add(nameColumn)
        self.paramGrid.Columns.Add(valueColumn)
        
        # Target elements selection
        self.lblTarget = Label()
        self.lblTarget.Text = "Target Elements:"
        self