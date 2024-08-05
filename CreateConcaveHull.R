rm(list=ls())

library(sf)
library(concaveman)

##### Set the Parameters Below #####

PWS_ID = "OH8301512"
concavity_setting = 2

workspace_dir = "C:/Users/TRichman.ERG/Tyler/Projects/2024/PWS Georeferencing/GIS/Tool Runs"

####################################

fc <- st_read(dsn = file.path(workspace_dir, paste0(PWS_ID, ".gdb")), layer = "_03_digitized_features_vertices")

coordinates <- st_coordinates(fc)
hull <- concaveman(coordinates, concavity = concavity_setting)

hull_sf <- st_sf(geometry = st_sfc(st_polygon(list(hull))), crs = st_crs(fc))

if (!dir.exists(file.path(workspace_dir, paste0("./", PWS_ID)))){
  dir.create(file.path(workspace_dir, paste0("./", PWS_ID)))
}

st_write(hull_sf, file.path(workspace_dir, paste0("./", PWS_ID, "/", PWS_ID, ".shp")))

