# Airports digitalization using python and overpass api


This project is about automating the process of airport digitalization which can be divided into two major steps: Airport Edges Detection and Airport Edges Extraction. For the first, we used the “OpenCV” python library to enhance rasters as well as detect edges. The next step was about converting edge raster to polyline using “arcpy” library, defining the area of interest (which is going to be used later on for the OSM query) by calculating the raster extent, also, exporting the airport polygon to Geojson and then converting it to shapefile to finally, clip the Polyline Edges to the airport polygon and get our airport edges.

One of the challenges faced here was to maintain the same coordinate system for different intermediate results, which was done using the “gdal” Python library.
Requirements:
This tool uses modules from python3:

Opencv

Arcpy

GDAL

Glob

Requests

Overpass

Geojson

String

Steps:
1- Setup your python environment as described in the section “Requirements”

2- Put your input airports rasters (.tif) under: D:\Input_images\SynthaaS_Aircraft

3- Edge detection:  - Convert image to gray scale 

                    - Reduce unwanted noise while keeping edges fairly sharp

                    -  Apply edge detection filter 

4- Export binary edge raster with same coordinate system as input raster

5- Convert binary edge raster to polylines

6- Define the area of interest: Get bounding box from airport raster

7- Use OSM query and bounding box to get airport polygon

8- Export Query result to GeoJSON file

9- Convert GeoJSON data to Features

10- Clip Edge polyline to Airport limits
