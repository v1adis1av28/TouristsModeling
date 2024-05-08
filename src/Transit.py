import math

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
building_tags = {'building': 'hotel'}
hotel_capacity = {
    'hotel': {'capacity': int(random.randint(200, 1500)), 'avg_bill': lambda: random.randint(800, 5000)}
}
def GetCenterPoint():
    places = ['mamaev', 'sarepta', 'panorama', 'ppb', 'nabka', 'lisaya gora', 'dom pavlova']
    place = random.choice(places)
    print(place)
    if place == 'mamaev':
        center_point = (48.7423657, 44.5371442)
    elif (place == 'sarepta'):
        center_point = (48.5222627, 44.5098335)
    elif (place == 'panorama'):
        center_point = (48.7154184, 44.5327745)
    elif place == 'ppb':
        center_point = (48.7082590, 44.5150334)

    elif place == 'nabka':
        center_point = (48.7029277, 44.5214930)
    elif place == 'lisaya gora':
        center_point = (48.6425061, 44.3923231)
    else:
        center_point = (48.7161142, 44.5311502)
    return center_point

def GetRandStayArea():
    place = [(48.8799494, 44.5898155),(48.7989878, 44.4570284),(48.7015364, 44.3946255),(48.4479420, 44.5143119)]
    return random.choice(place)
def Places(center_point, tags):
    gdf = ox.geometries.geometries_from_point(center_point, dist=1800, tags=tags)

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
#print("Словарь заведений общественного питания с присвоенными значениями вместимости и среднего чека:")

#print(amenity_info)
#print("Введите кол-во транзитных туристов:")
Tranzit_tourists_count = int(input())
Tranzit_touristsStay_count = math.ceil(Tranzit_tourists_count*random.random())
summa = 0
i = 0
for i in range(4):
    center = GetCenterPoint()
    amenity_info_items = Places(center,tags)
    for name, info in amenity_info_items.items():
        capacity = info['capacity']
        avg_bill = info['avg_bill']
        # Если количество туристов больше, чем вместимость, добавляем к сумме стоимость всех посетителей в заведении
        if Tranzit_tourists_count > capacity:
            summa += capacity * avg_bill
            Tranzit_tourists_count -= capacity
        # Иначе добавляем к сумме стоимость только указанного количества туристов и завершаем цикл
        else:
            summa += Tranzit_tourists_count * avg_bill
            break
for i in range(4):
    Count = int(Tranzit_tourists_count/4)
    center = GetCenterPoint()
    amenity_info_items = Places(center,tags)
    for name, info in amenity_info_items.items():
        capacity = info['capacity']
        avg_bill = info['avg_bill']
        # Если количество туристов больше, чем вместимость, добавляем к сумме стоимость всех посетителей в заведении
        if Count > capacity:
            summa += capacity * avg_bill
            Count -= capacity
        # Иначе добавляем к сумме стоимость только указанного количества туристов и завершаем цикл
        else:
            summa += Count * avg_bill
            break

remaining_tourists_half = Tranzit_tourists_count / 2

# Обработка информации об отелях
hotels_info = Places(GetRandStayArea(), building_tags)
hotels_sum = 0

# Первая точка проживания
first_location = GetCenterPoint()
first_location_info = Places(first_location, tags)
for name, info in first_location_info.items():
    capacity = info['capacity']
    avg_bill = info['avg_bill']
    # Если количество туристов больше, чем вместимость, добавляем к сумме стоимость всех посетителей в месте проживания
    if remaining_tourists_half > capacity:
        summa += capacity * avg_bill
        remaining_tourists_half -= capacity
    # Иначе добавляем к сумме стоимость только указанного количества туристов и завершаем цикл
    else:
        summa += remaining_tourists_half * avg_bill
        break

# Распределение оставшейся половины туристов между отелями
for name, info in hotels_info.items():
    capacity = info['capacity']
    avg_bill = info['avg_bill']
    # Если еще остались туристы для распределения
    while remaining_tourists_half > 0:
        # Если количество туристов больше, чем вместимость отеля, добавляем в отель столько туристов, сколько туда влезет
        if remaining_tourists_half > capacity:
            summa += capacity * avg_bill
            remaining_tourists_half -= capacity
        # Иначе добавляем в отель всех оставшихся туристов и заканчиваем распределение
        else:
            summa += remaining_tourists_half * avg_bill
            remaining_tourists_half = 0
            break


print("Сумма, которую получает регион с налога на добавочную стоиомсть с транзитных туристов:")
print(summa * 0.2)