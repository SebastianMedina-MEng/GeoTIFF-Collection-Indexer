import os
from osgeo import gdal
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import glob

## global Variables
directory_path = 'C:/Indexing_test'
dir_list = list()
EPSG_CODE = 'epsg:25832' ##25833 for Sachsen
output_filename = "bundesland_dgm1_index.gpkg"

## set working directory
os.chdir(directory_path)

## create list to save data
r_data = list()

## create geodataframe

#extractor
def extent_extractor(input_data):
    print("Extracting data extents for: "+input_data)
    data = gdal.Open(input_data)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    print(minx, miny, maxx, maxy)
    data = None
    bbox = [[minx,miny],[minx,maxy],[maxx,maxy],[maxx,miny]] ## to create polygon, this coordinates are to be given in order
    return(bbox)

def create_shapefile_from_list(input_list):
    print("creating index shapefile...")
    base_gdf = gpd.GeoDataFrame()
    for elements in input_list:
        print("processing "+elements[1])
        # geom = elements[0] ## list
        # link = elements[1]
        # print(elements[0][0], elements[0][1])
        polygon_geom = Polygon(elements[0])
        gdf = gpd.GeoDataFrame(pd.DataFrame({'path': [elements[1]]}), crs=EPSG_CODE, geometry=[polygon_geom])
        base_gdf = pd.concat([base_gdf, gdf])
    base_gdf.to_file(filename=output_filename, driver="GPKG")
    print("data has been processed satisfactorily")

#read all *.tif files
for fname in glob.glob(os.path.join(directory_path, '*.tif')):
   dir_list.append(fname)
print(dir_list)

# convert files input # dir_list()
for paths in dir_list:
    t_bbox = extent_extractor(paths)
    r_data.append((t_bbox, paths))

create_shapefile_from_list(r_data)


### To improve:
### Correct the format "/" and "\"of the output: C:/Indexing_test\dgm1_32_413_5547_1_he.tif

