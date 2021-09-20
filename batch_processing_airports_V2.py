import json
import cv2
import arcpy
import re
import string
import numpy as np
import gdal
from osgeo import ogr
from osgeo import osr
import os
from glob import glob
import sys
import overpass
from osm_airports_V2 import gInpIet_osm_airport
from shapely.geometry import shape, mapping
#arcpy.env.workspace = "D:\Input_images\SynthaaS_Aircraft"
#arcpy.env.overwriteOutput = True
in_imgpath = r'D:\Input_images\SynthaaS_Aircraft\*.TIF'
print("Start processing...")
if __name__=='__main__':
    for filename in glob(in_imgpath):
#Open Raster...
        img = cv2.imread(filename, 3)
        path, base_filename = os.path.split(filename)
        dataset1 = gdal.Open(filename)
#Get projection and transformation from original raster
        projection = dataset1.GetProjection()
        geotransform = dataset1.GetGeoTransform()
        
#Export Edge Raster
        #Convert RGB image to grayscale
        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #Apply Gaussian filter to reduce the noise (Smoothing images)
        blur = cv2.GaussianBlur(gray_img,(5,5),0)
        #Apply Canny Filter to detect edges
        edges = cv2.Canny(blur, 50, 100, 3, L2gradient=True)
        print("Processing completed for {}".format(base_filename))
        
        out_imgpath = os.path.join(path, "Edges_"+base_filename)
        path2, base_filename2 = os.path.split(out_imgpath)
        cv2.imwrite(out_imgpath ,edges)
        filename_ext=os.path.splitext(base_filename2)[0]
        print("Edges raster named {} saved.".format(out_imgpath))
        
#Assign Projection And Transformation To Edge Raster
        dataset2 = gdal.Open(out_imgpath, gdal.GA_Update)
        dataset2.SetGeoTransform( geotransform )
        dataset2.SetProjection( projection )
        #print("Projection for {} set.".format(out_imgpath))
        #print(geotransform)
#Calculate Raster Extent 
        upx=geotransform[0]
        
        xres=geotransform[1]
        xskew=geotransform[2]
        
        upy=geotransform[3]
        
        yskew=geotransform[4]
        yres=geotransform[5]
        
        cols = dataset2.RasterXSize
        rows = dataset2.RasterYSize
 
        lrx = upx + cols*xres + rows*xskew
        lry = upy + cols*yskew + rows*yres
        
        bbox=[str(lry),str(upx),str(upy),str(lrx)]
        print(bbox)
#Close output raster dataset 
        dataset1 = None
        dataset2 = None
#Convert Edge Raster To Polyline
        out_layername = os.path.join(path, "Lines_"+filename_ext+".shp")
        arcpy.conversion.RasterToPolyline(out_imgpath, out_layername, "ZERO", 0, "SIMPLIFY", "Value")
#Download Airport OSM Data
        jsonfile=get_osm_airport(path,bbox,filename_ext)
        #print(jsonfile)
#Convert OSM JSON Data To Features
        featurepath=os.path.join(path, "Feature_"+filename_ext+".shp")
        #arcpy.conversion.JSONToFeatures(jsonfile, featurepath, "POLYGON")
        arcpy.JSONToFeatures_conversion(jsonfile, featurepath, "POLYGON")
        
#Clip Edge polyline To Airport Feature
        airport_features=os.path.join(path, "Airport_features_"+filename_ext+".shp")
        arcpy.analysis.Clip(out_layername,featurepath,airport_features)
        