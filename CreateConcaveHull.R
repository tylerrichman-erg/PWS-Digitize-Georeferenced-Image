rm(list=ls())

library(sf)
library(concaveman)

##### Only Edit PWS_ID #####

PWS_ID = "OH5300012"

############################

fc <- st_read(dsn = paste0(PWS_ID, ".gdb"), layer = "_03_digitized_features_vertices")

coordinates <- st_coordinates(fc)
hull <- concaveman(coordinates, concavity = 2)

hull_sf <- st_sf(geometry = st_sfc(st_polygon(list(hull))), crs = st_crs(fc))

if (!dir.exists(paste0("./", PWS_ID))){
  dir.create(paste0("./", PWS_ID))  
}

st_write(hull_sf, paste0("./", PWS_ID, "/", PWS_ID, ".shp"))

