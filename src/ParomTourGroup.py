import geopandas as gpd
import pandas as pd
import numpy as np
import json
import h3
import folium
import warnings
import osmnx as ox
from shapely import wkt
from folium.plugins import HeatMap
from shapely.geometry import Polygon
import random

# Ignore warnings
warnings.filterwarnings('ignore')

amenity_capacity = {
    'restaurant': {'capacity': 30, 'avg_bill': lambda: random.randint(1500, 3000)},
    'cafe': {'capacity': 40, 'avg_bill': lambda: random.randint(300, 1500)},
    'fast_food': {'capacity': 60, 'avg_bill': lambda: random.randint(200, 1000)},
    'food_court': {'capacity': 100, 'avg_bill': lambda: random.randint(200, 1000)}
}
tags = {'amenity': ['restaurant', 'fast_food', 'cafe', 'food_court']}

# Set the central point (Mamayev Kurgan in this case)
center_point = (48.7034462, 44.5241342)
gdf = ox.geometries.geometries_from_point(center_point, dist=500, tags=tags)

# Assign capacity and average bill to each establishment based on its type
gdf['capacity'] = gdf['amenity'].apply(lambda x: amenity_capacity.get(x, {'capacity': 0, 'avg_bill': 0})['capacity'])
gdf['avg_bill'] = gdf['amenity'].apply(lambda x: amenity_capacity.get(x, {'capacity': 0, 'avg_bill': 0})['avg_bill'])

# Call the function for each establishment to get the specific average bill value
for index, row in gdf.iterrows():
    gdf.at[index, 'avg_bill'] = row['avg_bill']()

# Sort establishments by distance from the central point
gdf['distance'] = gdf.distance(gdf.geometry.centroid.iloc[0])
gdf = gdf.sort_values(by='distance')

# Extract establishment names and filter out empty values
amenity_info = {
    name: {
        'capacity': gdf.loc[gdf['name'] == name, 'capacity'].iloc[0],
        'avg_bill': gdf.loc[gdf['name'] == name, 'avg_bill'].iloc[0]
    } for name in gdf['name'].tolist() if pd.notna(name)
}

# Convert amenity_info to a dictionary if it's not already one
if not isinstance(amenity_info, dict):
    amenity_info = {name: {'capacity': None, 'avg_bill': None} for name in amenity_info}

print("Dictionary of food service establishments with assigned capacity and average bill values:")
print(amenity_info)

print("Enter the number of transit tourists:")
Tranzit_tourists_count = int(input())
summa = 0
i = 0
Percent_going_museum = int(0.4 * Tranzit_tourists_count)
Grow_ticket_cost = 1500
Children_ticket_cost = 1000

for i in range(Percent_going_museum):
    summa += 1 * random.choice((Grow_ticket_cost, Children_ticket_cost))

Percent_going_eat = int(0.2 * Tranzit_tourists_count)

for i in range(Percent_going_eat):
    food = random.choice(list(amenity_info.keys()))
    food_ = amenity_info[food]
    capacity_ = food_['capacity']
    avg_bill_ = food_['avg_bill']
    summa += 1 * avg_bill_

print("Region's revenue from value-added tax on ferry tourists:")
print(int(summa * 0.2))
