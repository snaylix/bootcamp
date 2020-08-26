import pandas as pd
import geopandas as gpd

from bokeh.io import output_notebook, show, curdoc
from bokeh.models import LinearColorMapper, GeoJSONDataSource, ColorBar, Slider, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, column

# STEP 1: Read in historical temperature data
# - Historical temperature data scraped for all countries from [Berkeley Earth](http://berkeleyearth.lbl.gov/country-list/)
# - According to Berkeley Earth: "Temperatures are in Celsius and reported as anomalies relative to the Jan 1951-Dec 1980 average."
DATA = '_RES/all_country_temp_data_CLEAN.csv'

#Read in the data with pandas
df = pd.read_csv(DATA)

# STEP 2: Read in the geographic data (geometric shapes of all countries in the world)
SHAPEFILE = '_RES/ne_110m_admin_0_countries.shp'

#Read in the shapefile with geopandas
gdf = gpd.read_file(SHAPEFILE)[['ADMIN', 'geometry']]

# STEP 3: Group / aggregate the temperature anomaly data by country, year
df = df.groupby(['country', 'year'])[['monthly_anomaly']].mean().reset_index()

# STEP 4: Merge Data Sets.
gdf = pd.merge(left=gdf, right=df, left_on='ADMIN', right_on='country', how='inner')

def get_geojson(year):
    """Input a year (int) and return corresponding GeoJSON"""
    gdf_year = gdf[gdf['year'] == year]
    return gdf_year.to_json()

geosource = GeoJSONDataSource(geojson = get_geojson(2000))

# STEP 5: Plot data on a map for a single year.
# 5a. Generate a blank canvas / figure.
p = figure(title = 'Average temperature anomaly of countries over time',
           plot_height = 600,
           plot_width = 1000,
          )

palette = brewer['YlGn'][5]

color_mapper = LinearColorMapper(palette = palette,
                                 low = -2.4,
                                 high = 4,
                                 nan_color = palette[2])

color_bar = ColorBar(color_mapper = color_mapper,
                     label_standoff = 8,
                     width = 200,
                     height = 10,
                     location = (0,0),
                     orientation = 'horizontal'
                    )

p.add_layout(color_bar, 'below')
p.patches('xs',
          'ys',
          source = geosource,
          fill_color = {'field' :'monthly_anomaly', 'transform': color_mapper}, ### NEW ###
          line_color = 'white',
          line_width = 0.25)

# STEP 6: Add a slider
slider = Slider(title = 'Year', start = 1900, end = 2013, step = 5, value = 1900)

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

# To view this application in interactive mode you need to set up a local Bokeh server
# In the terminal, run: 'bokeh serve --show 07_01_Bokeh_Tutorial_INCOMPLETE.py'

# Adding hover tool
hover = HoverTool(tooltips = [ ('Country','@country'), ('Temp. Anomaly', '@monthly_anomaly')])
p.tools.append(hover)


# - Any other cool widgets you can think of?


# - Get more data up through 2019/2020.
#     - Any data source / API where you might be able to get this?
# - Create predictions through 2050, and add them to the visualization.
# - **Why does the data load slowly, and how could we improve the speed?**
