import pandas as pd
import os
import re
import geopandas as gpd

from bokeh.models import LinearColorMapper, GeoJSONDataSource, HoverTool, Slider, ColorBar

DIRECTORY = '_RES/01_Einwohnerzahlen/'

df_list = []

for file in os.listdir(DIRECTORY):
    path = os.path.join(DIRECTORY, file)
    if os.path.isdir(path):
        continue
    else:
        df = pd.read_excel(path, sheet_name=1, skiprows=5, skipfooter=2, skipcolumns=1, header=None, usecols=range(1,3))
        df.columns = ['year', 'population']
        pattern = 'i[mn]-(\w+-?\w+)-[-b][ib]'
        state = re.findall(pattern, file)[0]
        print(state)
        df['state'] = state
        df_list.append(df)
        print(df.shape)
df.head()

DF = pd.concat(df_list, ignore_index=True)
DF[DF['state'] == 'bayern']['year'].unique()
DF[DF['state'] == 'sachsen']['year'].unique()

gjson = gpd.read_file(f'{DIRECTORY}2_bundeslaender/3_mittel.geo.json')

gjson.shape
gjson

GEOSOURCE = GeoJSONDataSource(geojson = gjson)




*Pseudo-Code*

1. Create an empty list and append lists pd.concat
2. Loop over all files in the directory
    3. Read in each file and merge it with the dataframe (use 'year' as index)
    4. Extract the name of state out of  file name and create an entry for all years into column "state"
5. Read in geojson data
