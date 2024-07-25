# -*- coding: utf-8 -*-import arcpyimport osclass Toolbox(object):    def __init__(self):        """Define the toolbox (the name of the toolbox is the name of the        .pyt file)."""        self.label = "Toolbox"        self.alias = "toolbox"        # List of tool classes associated with this toolbox        self.tools = [Digitize_Georeferenced_Image]class Digitize_Georeferenced_Image(object):    def __init__(self):        """Define the tool (tool name is the name of the class)."""        self.label = "Digitize Georeferenced Image"        self.description = ""        self.canRunInBackground = False    def getParameterInfo(self):        """Define parameter definitions"""        params = []        input_image_param = arcpy.Parameter(            displayName="Georeferenced Image",            name="georeferenced_image",            datatype="GPLayer",            parameterType="Required",            direction="Input"        )        params.append(input_image_param)        pwsid_param = arcpy.Parameter(            displayName="PWS ID",            name="pwsid",            datatype="GPString",            parameterType="Required",            direction="Input"        )        params.append(pwsid_param)        integer_series_param = arcpy.Parameter(            displayName="Pixel Values to Digitize",            name="pixel_values_to_digitize",            datatype="GPValueTable",            parameterType="Required",            direction="Input"        )        integer_series_param.columns = [['GPString', 'Statistic Type']]        params.append(integer_series_param)        output_folder_param = arcpy.Parameter(            displayName="Output Folder",            name="output_folder",            datatype="DEFolder",            parameterType="Required",            direction="Input"        )        params.append(output_folder_param)                return params    def isLicensed(self):        """Set whether tool is licensed to execute."""        return True    def updateParameters(self, parameters):        """Modify the values and properties of parameters before internal        validation is performed.  This method is called whenever a parameter        has been changed."""        return    def updateMessages(self, parameters):        """Modify the messages created by internal validation for each tool        parameter.  This method is called after internal validation."""        return    def execute(self, parameters, messages):        """The source code of the tool."""        ##### Retrieve Input Parameters #####                input_image = arcpy.Describe(parameters[0])        pwsid = parameters[1].valueAsText        pixels_to_digitize = parameters[2].values        output_folder = parameters[3].valueAsText        arcpy.AddMessage(input_image.catalogPath)        arcpy.AddMessage(pwsid)        arcpy.AddMessage(pixels_to_digitize)        arcpy.AddMessage(output_folder)        ##### Create Geodatabase #####        gdb_path = os.path.join(output_folder, f"{pwsid}.gdb")        if arcpy.Exists(gdb_path):            arcpy.management.Delete(gdb_path)                    arcpy.management.CreateFileGDB(            out_folder_path = output_folder,            out_name = f"{pwsid}.gdb"            )        arcpy.env.workspace = gdb_path        ##### Project the Raster to WGS84 #####        arcpy.management.ProjectRaster(            in_raster = input_image.catalogPath,            out_raster = "_00_projected_image",            out_coor_system = arcpy.SpatialReference(4326)            )        ##### Simplify Polygon #####        arcpy.conversion.RasterToPolygon(            in_raster = "_00_projected_image",            out_polygon_features = "_01_image_features",            simplify = "NO_SIMPLIFY"            )        ##### Export Features with Inputed Pixel Values #####        pixels_to_digitize = [item for sublist in pixels_to_digitize for item in sublist]        query = " Or gridcode = ".join(str(x) for x in pixels_to_digitize)        query = "gridcode = " + query        arcpy.conversion.ExportFeatures(            in_features = "_01_image_features",            out_features = "_02_digitized_features",            where_clause = query            )        ##### Extract Vertices from Polygon Feature #####        arcpy.management.CreateFeatureclass(            out_path = arcpy.env.workspace,            out_name = "_03_digitized_features_vertices",            geometry_type = "POINT",            spatial_reference = arcpy.SpatialReference(4326)        )        arcpy.management.AddField(            in_table = "_03_digitized_features_vertices",            field_name = "X",            field_type = "DOUBLE"            )        arcpy.management.AddField(            in_table = "_03_digitized_features_vertices",            field_name = "Y",            field_type = "DOUBLE"            )        with arcpy.da.InsertCursor("_03_digitized_features_vertices", ["X", "Y", "SHAPE@XY"]) as cursor:            for row in arcpy.da.SearchCursor("_02_digitized_features", ["OID@", "SHAPE@"]):                for part in row[1]:                    for point in part:                        if point:                            cursor.insertRow([point.X, point.Y, (point.X, point.Y)])                return    def postExecute(self, parameters):        """This method takes place after outputs are processed and        added to the display."""        return