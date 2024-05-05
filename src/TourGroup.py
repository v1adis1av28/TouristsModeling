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

# Игнорировать предупреждения
warnings.filterwarnings('ignore')

amenity_capacity = {
    'restaurant': {'capacity': 30, 'avg_bill': lambda: random.randint(1500, 3000)},
    'cafe': {'capacity': 40, 'avg_bill': lambda: random.randint(300, 1500)},
    'fast_food': {'capacity': 60, 'avg_bill': lambda: random.randint(200, 1000)},
    'food_court': {'capacity': 100, 'avg_bill': lambda: random.randint(200, 1000)}
}
tags = {'amenity': ['restaurant', 'fast_food', 'cafe', 'food_court']}

#Задаем центрированный объект в нашем случае это мамаев курган
mamaev_kurgan = (48.7423657, 44.5371442)
#ToDoo:- добавить координаты дом павлова -фонтана на набережной и для каждой просчитать по аналогии с транзитными туристами
dom_pavlova = ()
def GetDictionaryFood(center):
    gdf = ox.geometries.geometries_from_point(center_point, dist=1000, tags=tags)

    # Присвоение каждому заведению соответствующей вместимости и среднего чека в соответствии с его типом
    gdf['capacity'] = gdf['amenity'].apply(
        lambda x: amenity_capacity.get(x, {'capacity': 0, 'avg_bill': 0})['capacity'])
    gdf['avg_bill'] = gdf['amenity'].apply(
        lambda x: amenity_capacity.get(x, {'capacity': 0, 'avg_bill': 0})['avg_bill'])

    # Вызываем функцию для каждого заведения и получаем конкретное значение среднего чека
    for index, row in gdf.iterrows():
        gdf.at[index, 'avg_bill'] = row['avg_bill']()

    # Сортировка заведений по удаленности от центральной точки
    gdf['distance'] = gdf.distance(gdf.geometry.centroid.iloc[0])
    gdf = gdf.sort_values(by='distance')

    # Извлечение имен заведений и фильтрация пустых значений
    amenity_info = {
        name: {
            'capacity': gdf.loc[gdf['name'] == name, 'capacity'].iloc[0],
            'avg_bill': gdf.loc[gdf['name'] == name, 'avg_bill'].iloc[0]
        } for name in gdf['name'].tolist() if pd.notna(name)
    }

    # Если amenity_info не является словарем, преобразовать его в словарь
    if not isinstance(amenity_info, dict):
        amenity_info = {name: {'capacity': None, 'avg_bill': None} for name in amenity_info}
    return amenity_info

