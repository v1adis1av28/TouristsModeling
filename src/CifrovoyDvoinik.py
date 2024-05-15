import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import json
import h3
import folium
import warnings
from shapely import wkt
from folium.plugins import HeatMap
from shapely.geometry import Polygon
import random
import warnings
warnings.filterwarnings("ignore")


def GetCenterPoint():
    places = ['mamaev', 'sarepta', 'panorama', 'ppb', 'nabka', 'lisaya gora', 'dom pavlova']
    place = random.choice(places)
    #print(place)
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
def Transit(Tranzit_tourists_count):
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

    def GetRandStayArea():
        place = [(48.8799494, 44.5898155), (48.7989878, 44.4570284), (48.7015364, 44.3946255), (48.4479420, 44.5143119)]
        return random.choice(place)

    def Places(center_point, tags):
        gdf = ox.geometries.geometries_from_point(center_point, dist=3000, tags=tags)

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

    # print("Словарь заведений общественного питания с присвоенными значениями вместимости и среднего чека:")

    # print(amenity_info)
    # print("Введите кол-во транзитных туристов:")
    #Tranzit_tourists_count = int(input())
    Tranzit_touristsStay_count = math.ceil(Tranzit_tourists_count * random.random())
    summa = 0
    i = 0
    for i in range(4):
        center = GetCenterPoint()
        amenity_info_items = Places(center, tags)
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
        Count = int(Tranzit_tourists_count / 4)
        center = GetCenterPoint()
        amenity_info_items = Places(center, tags)
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

    hotels_gdf = ox.geometries.geometries_from_point(GetCenterPoint(), dist=4000, tags=building_tags)

    # Присваиваем каждому отелю соответствующую вместимость и средний чек
    for index, row in hotels_gdf.iterrows():
        building_type = row['building']
        if building_type in hotel_capacity:
            hotels_gdf.at[index, 'capacity'] = hotel_capacity[building_type]['capacity']
            hotels_gdf.at[index, 'avg_bill'] = hotel_capacity[building_type]['avg_bill']()

    # Сортируем отели по удаленности от центральной точки
    hotels_gdf['distance'] = hotels_gdf.distance(hotels_gdf.geometry.centroid.iloc[0])
    hotels_gdf = hotels_gdf.sort_values(by='distance')

    # Извлекаем имена заведений и фильтруем пустые значения
    hotels = []

    for index, row in hotels_gdf.iterrows():
        name = row['name']
        if pd.notna(name):
            hotels.append({'name': name, 'capacity': row['capacity'], 'avg_bill': row['avg_bill']})

    Tourists = remaining_tourists_half
    for i in range(int(Tourists)):
        rand_hotel = int(random.randint(0, len(hotels)-1))
        hotel_ = hotels[rand_hotel]
        capacity_ = hotel_['capacity']
        avg_bill_ = hotel_['avg_bill']
        summa +=  avg_bill_
    return summa*0.2

def Parom(Tourists):
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
    gdf['capacity'] = gdf['amenity'].apply(
        lambda x: amenity_capacity.get(x, {'capacity': 0, 'avg_bill': 0})['capacity'])
    gdf['avg_bill'] = gdf['amenity'].apply(
        lambda x: amenity_capacity.get(x, {'capacity': 0, 'avg_bill': 0})['avg_bill'])

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

    Tranzit_tourists_count = Tourists
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

    return summa*0.2


def Group(Tourists):
    # Игнорировать предупреждения
    warnings.filterwarnings('ignore')

    amenity_capacity = {
        'restaurant': {'capacity': 30, 'avg_bill': lambda: random.randint(1500, 3000)},
        'cafe': {'capacity': 40, 'avg_bill': lambda: random.randint(300, 1500)},
        'fast_food': {'capacity': 60, 'avg_bill': lambda: random.randint(200, 1000)},
        'food_court': {'capacity': 100, 'avg_bill': lambda: random.randint(200, 1000)}
    }
    tags = {'amenity': ['restaurant', 'fast_food', 'cafe', 'food_court']}

    # Задаем центрированный объект в нашем случае это мамаев курган
    mamaev_kurgan = (48.7423657, 44.5371442)
    # ToDoo:- добавить координаты дом павлова -фонтана на набережной и для каждой просчитать по аналогии с транзитными туристами
    dom_pavlova = (48.7161374, 44.5310905)
    fountain_of_friendship = (48.7045859, 44.5203912)

    def GetDictionaryFood(center_point):
        gdf = ox.geometries.geometries_from_point(center_point, dist=3500, tags=tags)

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
                'capacity': int(gdf.loc[gdf['name'] == name, 'capacity'].iloc[0]),
                'avg_bill': gdf.loc[gdf['name'] == name, 'avg_bill'].iloc[0]
            } for name in gdf['name'].tolist() if pd.notna(name)
        }

        # Если amenity_info не является словарем, преобразовать его в словарь
        if not isinstance(amenity_info, dict):
            amenity_info = {name: {'capacity': None, 'avg_bill': None} for name in amenity_info}
        return amenity_info

    def MorningOp(center_point, amenity_type='cafe'):
        gdf = ox.geometries.geometries_from_point(center_point, dist=3500, tags={"amenity": amenity_type})

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
                'capacity': int(gdf.loc[gdf['name'] == name, 'capacity'].iloc[0]),
                'avg_bill': gdf.loc[gdf['name'] == name, 'avg_bill'].iloc[0]
            } for name in gdf['name'].tolist() if pd.notna(name)
        }

        # Если amenity_info не является словарем, преобразовать его в словарь
        if not isinstance(amenity_info, dict):
            amenity_info = {name: {'capacity': None, 'avg_bill': None} for name in amenity_info}
        return amenity_info

    def CountSumma(Op, Tourists_per_object):
        summa = 0
        for name, info in Kurgan_op.items():
            capacity = info['capacity']
            avg_bill = info['avg_bill']
            # Если количество туристов больше, чем вместимость, добавляем к сумме стоимость всех посетителей в заведении
            if Tourists_per_object > capacity:
                summa += capacity * avg_bill
                Tourists_per_object -= capacity
            # Иначе добавляем к сумме стоимость только указанного количества туристов и завершаем цикл
            else:
                summa += Tourists_per_object * avg_bill
                return summa
        return summa

    tourists_per_group = 20
    count_of_groups = Tourists / tourists_per_group
    Groups_per_object = count_of_groups / 3
    Kurgan_op = MorningOp(GetCenterPoint())
    Pavlova_op = MorningOp(GetCenterPoint())
    Fountain_op = MorningOp(GetCenterPoint())
    # Следовательно группы не будут ходить в дорогие рестораны поэтому мы рассматриваем для утреннего кофейни и кафе
    summa = 0
    Tourists_per_object = Groups_per_object * tourists_per_group
    summa += CountSumma(Pavlova_op, Tourists_per_object)
    summa += CountSumma(Fountain_op, Tourists_per_object)
    summa += CountSumma(Kurgan_op, Tourists_per_object)
    summa += CountSumma(GetDictionaryFood(mamaev_kurgan), Tourists_per_object)
    summa += CountSumma(GetDictionaryFood(dom_pavlova), Tourists_per_object)
    summa += CountSumma(GetDictionaryFood(fountain_of_friendship), Tourists_per_object)
    summa = summa * 0.2
    print("Сумма полученная региональным бюджетом с групп туристов: ", summa)
    return summa * 0.2

def SportGroup(Tourists):
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
    center_point = GetCenterPoint()

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

    rand_hotel = int(random.randint(0, len(hotels)))
    rand_cafe_d1 = int(random.randint(0, len(cafes)))
    summa_hotel = 0
    summa_food = 0
    Comanda_count = 15
    Count_of_comands = int(Tourists / 15)
    for i in range(Count_of_comands):
        rand_hotel = int(random.randint(0, len(hotels)-1))
        hotel_ = hotels[rand_hotel]
        capacity_ = hotel_['capacity']
        avg_bill_ = hotel_['avg_bill']
        if (capacity_ > 15):
            summa_hotel += Comanda_count * avg_bill_
        else:
            rand_hotel = int(random.randint(0, len(hotels)-1))
            hotel_ = hotels[rand_hotel]
            capacity_ = hotel_['capacity']
            avg_bill_ = hotel_['avg_bill']
            summa_hotel += Comanda_count * avg_bill_

    for i in range(2):
        for i in range(Count_of_comands):
            rand_cafe_d1 = int(random.randint(0, len(cafes)-1))
            cafe = cafes[rand_cafe_d1]
            capacity_ = cafe['capacity']
            avg_bill_ = cafe['avg_bill']
            if (capacity_ > 15):
                summa_food += Comanda_count * avg_bill_
            else:
                rand_cafe_d1 = int(random.randint(0, len(cafes)-1))
                cafe = cafes[rand_cafe_d1]
                capacity_ = cafe['capacity']
                avg_bill_ = cafe['avg_bill']
                summa_food += Comanda_count * avg_bill_
    return (summa_food+summa_hotel)*0.2

def BuisnesTourists(Tourists):
    warnings.filterwarnings('ignore')

    # Определение тегов для кафе и остановок
    amenity_capacity = {
        'bus_station': {'capacity': int(random.randint(50, 120)), 'avg_bill': None},
        'cafe': {'capacity': int(random.randint(30, 40)), 'avg_bill': lambda: random.randint(300, 1500)}
    }
    tags = {'amenity': ['cafe', 'bus_station']}
    building_tags = {'building': 'hotel'}
    hotel_capacity = {
        'hotel': {'capacity': int(random.randint(200, 1500)), 'avg_bill': lambda: random.randint(3000, 10000)}
    }

    # Задаем центрированный объект в нашем случае это мамаев курган
    center_point = (48.7081520, 44.5154185)

    # Загружаем данные для кафе и остановок
    gdf = ox.geometries.geometries_from_point(center_point, dist=5000, tags=tags)

    # Присваиваем каждому заведению соответствующую вместимость и средний чек в соответствии с его типом
    for index, row in gdf.iterrows():
        amenity = row['amenity']
        if amenity in amenity_capacity:
            gdf.at[index, 'capacity'] = amenity_capacity[amenity]['capacity']
            if amenity_capacity[amenity]['avg_bill'] is None:
                gdf.at[index, 'avg_bill'] = random.randint(3000, 15000)
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

    rand_hotel = int(random.randint(0, len(hotels)))
    rand_cafe_d1 = int(random.randint(0, len(cafes)))
    summa_hotel = 0
    summa_food = 0
    Comanda_count = 15
    for i in range(int(Tourists)):
        rand_hotel = int(random.randint(0, len(hotels)-1))
        hotel_ = hotels[rand_hotel]
        capacity_ = hotel_['capacity']
        avg_bill_ = hotel_['avg_bill']
        if (capacity_ > 15):
            summa_hotel += Comanda_count * avg_bill_
        else:
            rand_hotel = int(random.randint(0, len(hotels)-1))
            hotel_ = hotels[rand_hotel]
            capacity_ = hotel_['capacity']
            avg_bill_ = hotel_['avg_bill']
            summa_hotel += Comanda_count * avg_bill_

    for i in range(2):
        for i in range(int(Tourists)):
            rand_cafe_d1 = int(random.randint(0, len(cafes)-1))
            cafe = cafes[rand_cafe_d1]
            capacity_ = cafe['capacity']
            avg_bill_ = cafe['avg_bill']
            if (capacity_ > 15):
                summa_food += Comanda_count * avg_bill_
            else:
                rand_cafe_d1 = int(random.randint(0, len(cafes)-1))
                cafe = cafes[rand_cafe_d1]
                capacity_ = cafe['capacity']
                avg_bill_ = cafe['avg_bill']
                summa_food += Comanda_count * avg_bill_
    return int((summa_food+summa_hotel)*0.2)

# Вводим кол-во потока туристов
print("Введите кол-во потока туристов")
Tourists_count = int(input())
# тразнитные туристы будем полагать что они посещают одну достопремичательность кушают вблизи нее и едут дальге
print("Введите процент тразитных туристов(пр.20 = 20%):")
Tranzit_tourists_percent = int(input()) / 100
# Туристы в составе группы будем полагать что они посещают несколько достопремичательностей и кушают 2 раза(утром и вечером)
print("Введите процент туристов в составе групп(пребывающие в течении одного дня")
Group_tourists_percent = int(input()) / 100
# Туристы учавстующие в соревновательных мероприятиях, будем полагать что им интересна транспортная инфраструктура, а также расположени отеля
print("Введите процент туристов, участвующих в соревнованиях:")
Sportsmen_tourists_percent = int(input()) / 100
print("Введите процент туристов, прибывших на пароме:")
Parom_tourists_percent = int(input()) / 100
print("Введите процент деловых туристов:")
Buisnes_tourists_percent = int(input()) / 100
# 1)Задаем кол-во потоков туристов
# 2)Прописываем разные сценарии(транзитные, с ночевкой, соревнования и тд.)
# 3)Пользователь задает разделения процента туристов по разным сценариям
# 4)Прогоняем по процентам распределнным сценарии
# 5)Визуализируем полученные данные

# Сценарий транзитного туриста
# Посетить достопремичательность->покушать->ехать дальше
transit = Transit(Tourists_count * Tranzit_tourists_percent)
# Сценарий туристов в составе группы
# Посещаем достопремичательность №1->кушаем в ближайшем общепите -> едем к достопремичательности №2 ->
# -> едем к достопремичательности №3 -> ужинаем в ближейшем заведении
group = Group(Tourists_count * Group_tourists_percent)
sport = SportGroup(Tourists_count*Sportsmen_tourists_percent)
parom = Parom(Tourists_count*Parom_tourists_percent)
buisnes = BuisnesTourists(Tourists_count*Buisnes_tourists_percent)
print("-------------------------------------------------------------------------------------------")
print("Выручка полученная региональным бюджетом с налога на добавочную стоимость от групп туристов")
#print("Транзитные туристы(кол-во) ", int(Tourists_count * Tranzit_tourists_percent), " ------------> ", transit)
print("Организованные группы туристов(кол-во) ", int(Tourists_count * Group_tourists_percent), "-------> ", group)
print("Туристы учавствующие в соревнованиях(кол-во) ", int(Tourists_count * Sportsmen_tourists_percent), "-------> ", sport)
print("Туристы прибывшие на пароме(кол-во) ", int(Tourists_count * Parom_tourists_percent), "-------> ", parom)
print("Туристы прибывшие на деловую встречу(кол-во) ", int(Tourists_count * Buisnes_tourists_percent), "-------> ", buisnes)
print("Общая сумма полученная региональным бюджетом: ", group + transit + sport + parom+ buisnes)


# Данные для круговой диаграммы
labels = ['Транзитные туристы', 'Организованные группы', 'Туристы участвующие в соревнованиях', 'Туристы прибывшие на пароме', 'Туристы прибывшие на деловую встречу']
sizes = [transit, group, sport, parom, buisnes]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightpink']
explode = (0.1, 0, 0, 0, 0)  # Выделение сегмента

# Построение круговой диаграммы
plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Выручка от разных категорий туристов')
#Починить транизитные туристы
# Отображение легенды
plt.legend(loc='upper right')

# Отображение диаграммы
plt.axis('equal')
plt.savefig('tourist_revenue_pie_chart.png', bbox_inches='tight')

# Данные о выручке от разных видов туризма
tourism_types = ['Транзитные', 'Группы', 'Соревнования', 'Паром', 'Деловые встречи']
revenue = [transit, group, sport, parom, buisnes]
tourists_count = [Tourists_count * Tranzit_tourists_percent, Tourists_count * Group_tourists_percent, Tourists_count * Sportsmen_tourists_percent, Tourists_count * Parom_tourists_percent, Tourists_count * Buisnes_tourists_percent]

# Создание DataFrame
data = {'Тип туризма': tourism_types, 'Выручка, руб.': revenue, 'Количество туристов': tourists_count}
df = pd.DataFrame(data)

# Сохранение таблицы в виде изображения
plt.figure(figsize=(10, 6))
plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=[0.3, 0.3, 0.3])
plt.axis('off')  # Отключаем оси координат
plt.title('Выручка и количество туристов по типам туризма')

# Сохранение таблицы в файл
plt.savefig('tourism_revenue_and_tourists_table.png', bbox_inches='tight')
