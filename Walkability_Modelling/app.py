import folium
from branca.colormap import linear
import pandas as pd
import os
import streamlit as st
from streamlit_folium import folium_static
import webbrowser
import json
import os.path

# print(os.getcwd())

geojson_file = os.path.join(os.getcwd(), 'Walkability', 'Data/karura-crs.geojson')
geojson_data = json.load(open(geojson_file))

m = folium.Map(location=[-1.237856, 36.831322], tiles='cartodb positron',name="Light Map",
           zoom_start=12,
           attr='My Data Attribution')

karura_neighborhood = "C:\\Users\\Dell\\OneDrive\\Desktop\\urban-green-spaces\\Walkability\\Data\\fid-walkability.csv"
karura_neighborhood_data = pd.read_csv(karura_neighborhood)
choice = ['Green Index', 'Population Density', 'Building Density', 'Street Intersection Density', 
          'Temperature', 'Elevation', 'Walkability Score']
choice_selected = st.selectbox("Select Choice ", choice)

fillcolor = 'YlGn'

folium.Choropleth(
    geo_data=geojson_data,
    name="choropleth",
    data=karura_neighborhood_data,
    columns=['fid_2', choice_selected],
    key_on="feature.properties.fid",
    fill_color=fillcolor,
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=choice_selected,
).add_to(m)
folium.features.GeoJson('C:\\Users\\Dell\\OneDrive\\Desktop\\urban-green-spaces\\Walkability\\Data\\karura-crs.geojson', 
                        name="karura-walkability",
                           popup=folium.features.GeoJsonPopup(fields=['NAME_3'])).add_to(m)
folium_static(m, width=1000, height=550)

m.save('walkability.html')
# webbrowser.open('walkability.html')