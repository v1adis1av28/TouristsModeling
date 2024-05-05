import osmnx as ox
import pandas as pd
import random

# Игнорировать предупреждения
import warnings
warnings.filterwarnings('ignore')

# Определение тегов для кафе и остановок
amenity_capacity = {
    'bus_station': {'capacity': int(random.randint(50, 120)), 'avg_bill': None},
    'cafe': {'capacity': int(random.randint(30, 40)), 'avg_bill': lambda: random.randint(300, 1500)}
}
tags = {'amenity': ['cafe', 'bus_station']}
building_tags = {'building': 'hotel'}
hotel_capacity = {
    'hotel': {'capacity': int(random.randint(200, 1500)), 'avg_bill': lambda: random.randint(800, 5000)}
}

# Задаем центрированный объект в нашем случае это мамаев курган
center_point = (48.7128912, 44.5132646)

# Загружаем данные для кафе и остановок
gdf = ox.geometries.geometries_from_point(center_point, dist=4000, tags=tags)

# Присваиваем каждому заведению соответствующую вместимость и средний чек в соответствии с его типом
for index, row in gdf.iterrows():
    amenity = row['amenity']
    if amenity in amenity_capacity:
        gdf.at[index, 'capacity'] = amenity_capacity[amenity]['capacity']
        if amenity_capacity[amenity]['avg_bill'] is None:
            gdf.at[index, 'avg_bill'] = random.randint(300, 1500)
        else:
            gdf.at[index, 'avg_bill'] = amenity_capacity[amenity]['avg_bill']()

# Загружаем данные для отелей
hotels_gdf = ox.geometries.geometries_from_point(center_point, dist=4000, tags=building_tags)

# Присваиваем каждому отелю соответствующую вместимость и средний чек
for index, row in hotels_gdf.iterrows():
    building_type = row['building']
    if building_type in hotel_capacity:
        hotels_gdf.at[index, 'capacity'] = hotel_capacity[building_type]['capacity']
        hotels_gdf.at[index, 'avg_bill'] = hotel_capacity[building_type]['avg_bill']()

# Сортируем заведения по удаленности от центральной точки
gdf['distance'] = gdf.distance(gdf.geometry.centroid.iloc[0])
gdf = gdf.sort_values(by='distance')

# Сортируем отели по удаленности от центральной точки
hotels_gdf['distance'] = hotels_gdf.distance(hotels_gdf.geometry.centroid.iloc[0])
hotels_gdf = hotels_gdf.sort_values(by='distance')

# Извлекаем имена заведений и фильтруем пустые значения
cafes = []
stations = []
hotels = []

for index, row in gdf.iterrows():
    name = row['name']
    if pd.notna(name):
        if row['amenity'] == 'cafe':
            cafes.append({'name': name, 'capacity': row['capacity'], 'avg_bill': row['avg_bill']})
        elif row['amenity'] == 'bus_station':
            stations.append({'name': name, 'capacity': row['capacity'], 'avg_bill': row['avg_bill']})

for index, row in hotels_gdf.iterrows():
    name = row['name']
    if pd.notna(name):
        hotels.append({'name': name, 'capacity': row['capacity'], 'avg_bill': row['avg_bill']})

rand_hotel = int(random.randint(0,len(hotels)))
rand_cafe_d1 = int(random.randint(0,len(cafes)))
print("Введите кол-во туристов спортсменов: ")
Tourists = int(input())
summa_hotel = 0
summa_food = 0
Comanda_count = 15
Count_of_comands = int(Tourists/15)
for i in range(Count_of_comands):
    rand_hotel = int(random.randint(0, len(hotels)))
    hotel_ = hotels[rand_hotel]
    capacity_ = hotel_['capacity']
    avg_bill_ = hotel_['avg_bill']
    if(capacity_ > 15):
        summa_hotel += Comanda_count * avg_bill_
    else:
        rand_hotel = int(random.randint(0, len(hotels)))
        hotel_ = hotels[rand_hotel]
        capacity_ = hotel_['capacity']
        avg_bill_ = hotel_['avg_bill']
        summa_hotel += Comanda_count*avg_bill_

for i in range(2):
    for i in range(Count_of_comands):
        rand_cafe_d1 = int(random.randint(0, len(cafes)))
        cafe = cafes[rand_cafe_d1]
        capacity_ = cafe['capacity']
        avg_bill_ = cafe['avg_bill']
        if (capacity_ > 15):
            summa_food += Comanda_count * avg_bill_
        else:
            rand_cafe_d1 = int(random.randint(0, len(cafes)))
            cafe = cafes[rand_cafe_d1]
            capacity_ = cafe['capacity']
            avg_bill_ = cafe['avg_bill']
            summa_food += Comanda_count*avg_bill_
