import os
from osgeo import gdal
import string
import overpass
import geojson
import json
import tempfile
import subprocess
from osgeo import gdal
from geojson import Feature, FeatureCollection, dump, MultiPolygon, MultiLineString, LineString, GeometryCollection, Polygon,Point
maxsize:1073741824

def get_osm_airport(path,bbox,filename_ext):
    #bbox_input=['37.600632','-122.407608','37.643053','-122.34993']
    
    bbox_input=bbox
    api=overpass.API()
    print(bbox_input[0])
    q=bbox_input[0]+','+bbox_input[1]+','+bbox_input[2]+','+bbox_input[3]
    #print(q)
    full_query='way["aeroway"="aerodrome"]('+q+');'
    print(full_query)
    res=api.get(full_query,responseformat="geojson",verbosity="geom")
    print ('Query completed')
    print(res) 
    #Prepare Geometry
    #Export Geojson file
    #collection =geojson.FeatureCollection(res)
    jsonfile= os.path.join(path, "Json_"+filename_ext+".json")
    with open(jsonfile, 'w+') as f:
        geojson.dump(res, f)
    #Save to shp
    # args=['ogr2ogr','-f','esri shapefile','destination_data.shp', 'res.geojson']
    # subprocess.Popen(args)
    print ("Finished exporting Geojson file")
    return jsonfile
if __name__=='__main__':
    get_osm_airport()
    
