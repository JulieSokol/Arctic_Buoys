#=======================================================================================================================
#=======================================================================================================================
#====    PURPOSE OF THE SCRIPT: Downloading buoy data from the portal International Arctic Buoy Programme (IABP)    ====
#====    BRIEF DESCRIPTION: You can use this script, if you need buoy data on dayly basis. Just put it in the Task  ====
#====    Manager of your OS, so you could get new data automatically. See README file to get more information about ====
#====    the content of downloaded tables with parameters, recieved by buoys.                                       ====
#====    the content of downloaded tables with parameters, recieved by buoys.                                       ====
#====                                                                                                               ====
#====    AUTHOR: Julia Sokolova.            E-MAIL: luliksokol@gmail.com                                            ====
#====    LAST EDITION:  19/10/2022                                                                                  ====
#=======================================================================================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import shutil
import os
from osgeo import ogr, osr


# Parsing of the page, in the result of which we get a list of links
url = 'https://iabp.apl.uw.edu/Data_Products/Daily_Full_Res_Data/Arctic/'                 # url of the page
r = requests.get(url, verify=False)                                                       # Setting connection
soup = BeautifulSoup(r.text,features="html.parser")                                       # Sending the resulting page to the parsing library

L = []                                                                                   # Creating an empty list
for link in soup.find_all('a'):
    href = link.get('href')
    new_link='https://iabp.apl.uw.edu/Data_Products/Daily_Full_Res_Data/Arctic/'+ href    # Getting all links
    #print(new_link)
    L.append(new_link)                                                                    # Putting every link to the list  
actual_link = L[-1]                                                                       # Choosing the last link
print(actual_link)

# Modification of the list to a DataFrame
links_table = pd.DataFrame(L, columns=['links'])                                          # Saving the table of links
links_table.to_csv('links_arc.csv', index=False)

# Reading the last link from the DataFrame in order to download it
r = requests.get(actual_link, allow_redirects=True, verify=False)                         # Getting the last link 
open(href, 'wb').write(r.content)                                                        # ... and download the file (dat-file)
file_name = re.split('/', actual_link)[-1]                                               # Extracting the filename
df = pd.read_csv(file_name, sep=';')                                                     # Opening dat-file
#df = df.replace(-999.0, np.NaN)                                                         # Uncomment this line if you want to change no data values, expressed with -999.0, to NaN
print(df)

shp_name = file_name.split('.')[0]  + '.shp'                                             # Excluding an extension from the filename

# Creating a shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")                                           # Set up the shapefile driver
shapeData = driver.CreateDataSource(shp_name)                                            # Create the data source
spatialReference = osr.SpatialReference()                                                # Create the spatial reference system, WGS84
spatialReference.ImportFromProj4('+proj=longlat +datum=WGS84 +no_defs')
layer = shapeData.CreateLayer("arctic_buoys", spatialReference, ogr.wkbPoint)            # This will create a corresponding layer for our data with given spatial information.
layer_defn = layer.GetLayerDefn()

# Creating a dictionary of attributes and its types 
shp_fields = {'BuoyID': ogr.OFTString,'Year': ogr.OFTInteger,'Hour': ogr.OFTInteger,'Min': ogr.OFTInteger,
              'DOY': ogr.OFTReal,'POS_DOY': ogr.OFTReal, 'LAT': ogr.OFTReal,'LONG': ogr.OFTReal,
              'BP': ogr.OFTReal,'Ts': ogr.OFTReal,'Ta': ogr.OFTReal}
for key, value in shp_fields.items():
    layer.CreateField(ogr.FieldDefn(key, value))                                       # Defining and creating attributes in the shapefile in an iterative way

# Filling fields of attributes with values from the text-file
for index, row in df.iterrows():
    feature = ogr.Feature(layer_defn)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(row[7]), float(row[6]))
    feature.SetGeometry(point)  # set the coordinates
    feature.SetFID(index)
    field_list = {'BuoyID':row[0],'Year':row[1],'Hour':row[2],'Min':row[3],'DOY':row[4],'POS_DOY':row[5],       # Associating names of shapefile attributes with respective columns of the dataframe
                  'LAT':row[6],'LONG':row[7],'BP':row[8],'Ts':row[9],'Ta':row[10]}

    for key, value in field_list.items():                # Looping through the dictionary
        feature.SetField(key, value)                     # Filling fields with values

    layer.CreateFeature(feature)
shapeData.Destroy()



#=======================================================================================================================
#=======================================================================================================================
#========   If you want to move downloaded files to a specific destination folder, uncomment the code below  ===========
#=======================================================================================================================
#=======================================================================================================================

"""
# Saving shapefile to the destination folder
dest_folder = '..\\BUOYS\\Arctic'                                               # You can change the path to whatever appropriate for you
split_name = re.findall(r'FR_(\d{4})(\d{2})(\d{2}).shp', shp_name)              # The following 5 code lines are used, if you want to create a folder structure like: ..\BUOYS\Arctic\Year\Month. Otherwise, delete it.
Year = split_name[0][0]
Month = split_name[0][1]
Day = split_name[0][2]
dest_folder = dest_folder + '\\' + Year + '\\' + Month


if os.path.exists(dest_folder):
    pass
else:
    os.makedirs(dest_folder)

for filename in os.listdir():
    if filename.startswith('FR_' + Year + Month + Day):
        shutil.copy(filename, dest_folder)
"""
