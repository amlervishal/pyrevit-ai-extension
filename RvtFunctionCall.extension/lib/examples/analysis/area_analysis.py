"""
Area Analysis Tool
Comprehensive area analysis with boundary extraction, parameter collection, and statistical summaries.
"""
import clr
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, AreaScheme, SpatialElement, Area, ElementId, SpatialElementBoundaryOptions, SpatialElementGeometryCalculator, Options, XYZ, UnitUtils, DisplayUnitType, Transaction
import json
import System
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, Button, DialogResult, FormBorderStyle, StartPosition, TextBox, MessageBox, DataGridView, DataGridViewTextBoxColumn
import math

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

class AreaAnalysisForm(Form):
    def __init__(self):
        self.InitializeComponent()
        self.area_data = None
        
    def InitializeComponent(self):
        self.Text = "Area Analysis Tool"
        self.Width = 800
        self.Height = 600
        self.FormBorderStyle = FormBorderStyle.Sizable
        self.StartPosition = StartPosition.CenterScreen
        
        # Instructions label
        self.lblInstructions = Label()
        self.lblInstructions.Text = "Click 'Analyze Areas' to extract comprehensive area data from the project."
        self.lblInstructions.Location = System.Drawing.Point(20, 20)
        self.lblInstructions.Size = System.Drawing.Size(750, 40)
        
        # Results display
        self.txtResults = TextBox()
        self.txtResults.Multiline = True
        self.txtResults.ReadOnly = True
        self.txtResults.Location = System.Drawing.Point(20, 70)
        self.txtResults.Size = System.Drawing.Size(750, 450)
        self.txtResults.ScrollBars = System.Windows.Forms.ScrollBars.Both
        self.txtResults.Font = System.Drawing.Font("Consolas", 9)
        
        # Analyze button
        self.btnAnalyze = Button()
        self.btnAnalyze.Text = "Analyze Areas"
        self.btnAnalyze.Location = System.Drawing.Point(20, 530)
        self.btnAnalyze.Size = System.Drawing.Size(120, 30)
        self.btnAnalyze.Click += self.AnalyzeAreas
        
        # Export button
        self.btnExport = Button()
        self.btnExport.Text = "Export to JSON"
        self.btnExport.Location = System.Drawing.Point(150, 530)
        self.btnExport.Size = System.Drawing.Size(120, 30)
        self.btnExport.Click += self.ExportToJson
        self.btnExport.Enabled = False
        
        # Close button
        self.btnClose = Button()
        self.btnClose.Text = "Close"
        self.btnClose.Location = System.Drawing.Point(650, 530)
        self.btnClose.Size = System.Drawing.Size(120, 30)
        self.btnClose.Click += self.CloseForm
        
        # Add controls to form
        self.Controls.Add(self.lblInstructions)
        self.Controls.Add(self.txtResults)
        self.Controls.Add(self.btnAnalyze)
        self.Controls.Add(self.btnExport)
        self.Controls.Add(self.btnClose)
        
    def AnalyzeAreas(self, sender, e):
        try:
            self.txtResults.Text = "Analyzing areas..."
            self.area_data = self.extract_area_data()
            self.display_results()
            self.btnExport.Enabled = True
        except Exception as ex:
            MessageBox.Show("Error analyzing areas: {}".format(str(ex)), "Analysis Error")
    
    def extract_area_data(self):
        """Extract comprehensive area data from the project"""
        # Initialize the data structure
        area_data = {
            "project_info": {
                "total_area_schemes": 0,
                "total_areas": 0,
                "analysis_date": System.DateTime.Now.ToString()
            },
            "area_schemes": [],
            "areas": [],
            "summary_statistics": {}
        }
        
        # Get all area schemes
        area_schemes = FilteredElementCollector(doc).OfClass(AreaScheme).ToElements()
        area_data["project_info"]["total_area_schemes"] = len(area_schemes)
        
        for scheme in area_schemes:
            scheme_data = {
                "id": scheme.Id.IntegerValue,
                "name": scheme.Name,
                "area_type": str(scheme.AreaType)
            }
            area_data["area_schemes"].append(scheme_data)
        
        # Get all areas
        areas = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Areas).WhereElementIsNotElementType().ToElements()
        area_data["project_info"]["total_areas"] = len(areas)
        
        total_area_sqft = 0
        level_areas = {}
        scheme_areas = {}
        
        for area in areas:
            if not isinstance(area, Area):
                continue
                
            # Get basic area properties
            area_scheme_id = area.AreaSchemeId.IntegerValue
            area_id = area.Id.IntegerValue
            area_name = area.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() or "Unnamed Area"
            area_number = area.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() or ""
            area_value = area.get_Parameter(BuiltInParameter.AREA_AREA).AsDouble()
            area_value_sqft = UnitUtils.ConvertFromInternalUnits(area_value, DisplayUnitType.DUT_SQUARE_FEET)
            
            # Update totals
            total_area_sqft += area_value_sqft
            
            # Get level information
            level_id = area.LevelId
            level_name = doc.GetElement(level_id).Name if level_id != ElementId.InvalidElementId else "Unknown Level"
            
            # Track areas by level
            if level_name not in level_areas:
                level_areas[level_name] = {"count": 0, "total_area": 0}
            level_areas[level_name]["count"] += 1
            level_areas[level_name]["total_area"] += area_value_sqft
            
            # Track areas by scheme
            if area_scheme_id not in scheme_areas:
                scheme_areas[area_scheme_id] = {"count": 0, "total_area": 0}
            scheme_areas[area_scheme_id]["count"] += 1
            scheme_areas[area_scheme_id]["total_area"] += area_value_sqft
            
            # Get all parameters
            params = {}
            for param in area.Parameters:
                if param.HasValue:
                    param_name = param.Definition.Name
                    try:
                        if param.StorageType.ToString() == "String":
                            params[param_name] = param.AsString()
                        elif param.StorageType.ToString() == "Double":
                            params[param_name] = param.AsDouble()
                        elif param.StorageType.ToString() == "Integer":
                            params[param_name] = param.AsInteger()
                        elif param.StorageType.ToString() == "ElementId":
                            params[param_name] = param.AsElementId().IntegerValue
                    except:
                        params[param_name] = "Error reading value"
            
            # Get boundary information
            boundary_points = []
            perimeter = 0
            try:
                options = SpatialElementBoundaryOptions()
                boundaries = area.GetBoundarySegments(options)
                
                if boundaries and boundaries.Count > 0:
                    for boundary_loop in boundaries:
                        loop_points = []
                        loop_perimeter = 0
                        for segment in boundary_loop:
                            curve = segment.GetCurve()
                            start_point = curve.GetEndPoint(0)
                            end_point = curve.GetEndPoint(1)
                            
                            loop_points.append({
                                "x": start_point.X,
                                "y": start_point.Y,
                                "z": start_point.Z
                            })
                            
                            # Calculate segment length
                            segment_length = curve.Length
                            loop_perimeter += segment_length
                        
                        boundary_points.append(loop_points)
                        perimeter += loop_perimeter
            except Exception as ex:
                # If boundary extraction fails, note it but continue
                boundary_points = [{"error": "Could not extract boundary: {}".format(str(ex))}]
            
            # Convert perimeter to feet
            perimeter_ft = UnitUtils.ConvertFromInternalUnits(perimeter, DisplayUnitType.DUT_DECIMAL_FEET)
            
            # Compile comprehensive area data
            area_info = {
                "id": area_id,
                "name": area_name,
                "number": area_number,
                "area_scheme_id": area_scheme_id,
                "level_name": level_name,
                "area_sqft": round(area_value_sqft, 2),
                "area_internal_units": area_value,
                "perimeter_ft": round(perimeter_ft, 2),
                "boundary_points": boundary_points,
                "parameters": params
            }
            
            area_data["areas"].append(area_info)
        
        # Calculate summary statistics
        area_data["summary_statistics"] = {
            "total_area_sqft": round(total_area_sqft, 2),
            "average_area_sqft": round(total_area_sqft / len(areas), 2) if areas else 0,
            "level_breakdown": level_areas,
            "scheme_breakdown": scheme_areas,
            "largest_area": max(area_data["areas"], key=lambda x: x["area_sqft"]) if area_data["areas"] else None,
            "smallest_area": min(area_data["areas"], key=lambda x: x["area_sqft"]) if area_data["areas"] else None
        }
        
        return area_data
    
    def display_results(self):
        """Display the analysis results in a formatted text view"""
        if not self.area_data:
            return
        
        output = []
        output.append("=" * 60)
        output.append("AREA ANALYSIS REPORT")
        output.append("=" * 60)
        output.append("")
        
        # Project overview
        proj_info = self.area_data["project_info"]
        output.append("PROJECT OVERVIEW:")
        output.append("- Total Area Schemes: {}".format(proj_info["total_area_schemes"]))
        output.append("- Total Areas: {}".format(proj_info["total_areas"]))
        output.append("- Analysis Date: {}".format(proj_info["analysis_date"]))
        output.append("")
        
        # Summary statistics
        stats = self.area_data["summary_statistics"]
        output.append("SUMMARY STATISTICS:")
        output.append("- Total Area: {:,.2f} sq ft".format(stats["total_area_sqft"]))
        output.append("- Average Area: {:,.2f} sq ft".format(stats["average_area_sqft"]))
        
        if stats["largest_area"]:
            output.append("- Largest Area: {} ({:,.2f} sq ft)".format(
                stats["largest_area"]["name"], stats["largest_area"]["area_sqft"]))
        
        if stats["smallest_area"]:
            output.append("- Smallest Area: {} ({:,.2f} sq ft)".format(
                stats["smallest_area"]["name"], stats["smallest_area"]["area_sqft"]))
        output.append("")
        
        # Area schemes
        output.append("AREA SCHEMES:")
        for scheme in self.area_data["area_schemes"]:
            output.append("- {} (ID: {}, Type: {})".format(
                scheme["name"], scheme["id"], scheme["area_type"]))
        output.append("")
        
        # Level breakdown
        output.append("BREAKDOWN BY LEVEL:")
        for level_name, data in stats["level_breakdown"].items():
            output.append("- {}: {} areas, {:,.2f} sq ft".format(
                level_name, data["count"], data["total_area"]))
        output.append("")
        
        # Individual areas (first 10)
        output.append("AREA DETAILS (First 10):")
        for i, area in enumerate(self.area_data["areas"][:10]):
            output.append("{}. {} ({})".format(i+1, area["name"], area["number"]))
            output.append("   Level: {}, Area: {:,.2f} sq ft, Perimeter: {:,.2f} ft".format(
                area["level_name"], area["area_sqft"], area["perimeter_ft"]))
            output.append("   Boundary Points: {} loops".format(len(area["boundary_points"])))
            output.append("")
        
        if len(self.area_data["areas"]) > 10:
            output.append("... and {} more areas".format(len(self.area_data["areas"]) - 10))
        
        # Join and display
        self.txtResults.Text = "\r\n".join(output)
    
    def ExportToJson(self, sender, e):
        """Export the analysis data to a JSON file"""
        if not self.area_data:
            MessageBox.Show("No data to export. Please run analysis first.", "No Data")
            return
        
        try:
            # Use a simple filename for now
            import tempfile
            import os
            
            # Create temp file
            temp_dir = tempfile.gettempdir()
            json_path = os.path.join(temp_dir, "area_analysis_export.json")
            
            # Write JSON data
            with open(json_path, 'w') as f:
                json.dump(self.area_data, f, indent=2)
            
            MessageBox.Show("Data exported to: {}".format(json_path), "Export Complete")
            
        except Exception as ex:
            MessageBox.Show("Error exporting data: {}".format(str(ex)), "Export Error")
    
    def CloseForm(self, sender, e):
        self.DialogResult = DialogResult.OK
        self.Close()

# Execute the form
form = AreaAnalysisForm()
form.ShowDialog()
