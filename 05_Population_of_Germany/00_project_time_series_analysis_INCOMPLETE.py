import os
import re
import pandas as pd
import geopandas as gpd

from bokeh.io import output_notebook, show, curdoc
from bokeh.models import LinearColorMapper, GeoJSONDataSource, ColorBar, Slider, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, column



def create_dataframe():
    """
    takes excel tables for state's population data and creates a combined create_dataframe

    Returns: dataframe
    """


    df_list= []
    for file in os.listdir(DIRECTORY):
        path = os.path.join(DIRECTORY, file)
        if os.path.isdir(path):
            continue
        else:
            df = pd.read_excel(path, sheet_name=1, skiprows=5, skipfooter=2, skipcolumns=1, header=None, usecols=range(1,3))
            df.columns = ['year', 'population']
            pattern = 'i[mn]-(\w+-?\w+)-[-b][ib]'
            state = re.findall(pattern, file)[0]
            df['state'] = state
            df_list.append(df)
    df_list
    df = pd.concat(df_list, ignore_index=True)
    return df

def format_state_names(state_name):
    """
    Takes a string name of a state and returns name with first letters in uppercase

    Parameters: string state name
    Returns: new string state name
    """

    pattern = '\w+'
    parts = re.findall(pattern, state_name)
    for index, part in enumerate(parts):
        parts[index] = part[0].upper() + part[1:]
    if len(parts) > 1:
        new_name = parts[0] + '-' + parts[1]
    else:
        new_name = parts[0]
    if new_name == 'Baden-Wuerttemberg':
        new_name = 'Baden-Württemberg'
    if new_name == 'Thueringen':
        new_name = 'Thüringen'
    return new_name

DIRECTORY = '_RES/01_Einwohnerzahlen/'
DF = create_dataframe()

DF.head()
DF['population'].describe()
DF['population'].min()
DF['population'].max()


DF[DF['state'] == 'bayern']['year'].unique()
DF[DF['state'] == 'sachsen']['year'].unique()

# def clean_up_new_states(x):
#     new_states = ['Sachsen', 'Thüringen', 'Sachsen-Anhalt', 'Brandenburg', 'Mecklenburg-Vorpommern']
#
# DF['population'] = DF['population'].apply(clean_up_new_states)


GJSON = gpd.read_file(f'{DIRECTORY}2_bundeslaender/3_mittel.geo.json')

DF['state'].unique()

DF['state'] = DF['state'].apply(format_state_names)

# for state in DF['state'].unique():
#     if state in GJSON['name'].unique():
#         print(f'{state} in GJSON data')
#     else:
#         print(f'Did not find {state} in GJSON data')

GJSON.shape
GJSON
gdf = pd.merge(left=GJSON, right=DF, left_on='name', right_on='state', how='inner')
gdf.drop(['type', 'state', 'id'], axis=1, inplace=True)
gdf
gdf.groupby('name')['population'].mean()
def get_geojson(year):
    """Input a year (int) and return corresponding GeoJSON"""
    gdf_year = gdf[gdf['year'] == year]
    return gdf_year.to_json()

geosource = GeoJSONDataSource(geojson = get_geojson(2000))

# Plot data on a map for a single year.
# 5a. Generate a blank canvas / figure.
p = figure(title = 'Population growth in the states of Germany since the reunification',
           plot_height = 800,
           plot_width = 800,
          )

palette = brewer['YlGn'][5]

color_mapper = LinearColorMapper(palette = palette,
                                 low = 0,
                                 high = 2000000,
                                 nan_color = palette[1])

color_bar = ColorBar(color_mapper = color_mapper,
                     label_standoff = 8,
                     width = 500,
                     height = 10,
                     location = (0,0),
                     orientation = 'horizontal'
                    )

p.add_layout(color_bar, 'below')
p.patches('xs',
          'ys',
          source = geosource,
          fill_color = {'field' :'population', 'transform': color_mapper}, ### NEW ###
          line_color = 'white',
          line_width = 0.5)

# Add a slider
slider = Slider(title = 'Year', start = 1990, end = 2019, step = 1, value = 1990)

# Write a "callback" function that defines what happens whenever we move the slider
def update_plot(attr, old, new):

    """Change properties / attributes of the datasource and title depending on slider value / position."""

    yr = slider.value
    new_data = get_geojson(yr)
    geosource.geojson = new_data
    p.title.text = f'Average temperature anomaly of countries for year {yr}'

slider.on_change('value', update_plot)

# Wrapping slider in a widget box, combining it with the figure in a column layout, adding it all to the current document
curdoc().add_root(column(p,widgetbox(slider)))

# Adding hover tool
hover = HoverTool(tooltips = [ ('State','@name'), ('Absolute Population', '@population')])
p.tools.append(hover)

# To view this application in interactive mode you need to set up a local Bokeh server
# In the terminal, run: 'bokeh serve --show 07_01_Bokeh_Tutorial_INCOMPLETE.py'
