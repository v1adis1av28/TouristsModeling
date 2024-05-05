import osmnx as ox
import geopandas as gpd
import pandas as pd
import numpy as np
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
def Transit(Tranzit_tourists_count):
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
    center_point = (48.7423657, 44.5371442)
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

    print("Словарь заведений общественного питания с присвоенными значениями вместимости и среднего чека:")
    print(amenity_info)
    summa = 0
    i = 0
    for name, info in amenity_info.items():
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
    print("Сумма, которую получает регион с налога на добавочную стоиомсть с транзитных туристов: ", summa * 0.2)
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
    Kurgan_op = MorningOp(mamaev_kurgan)
    Pavlova_op = MorningOp(dom_pavlova)
    Fountain_op = MorningOp(fountain_of_friendship)
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
print("-------------------------------------------------------------------------------------------")
print("Выручка полученная региональным бюджетом с налога на добавочную стоимость от групп туристов")
print("Транзитные туристы(кол-во) ", int(Tourists_count * Tranzit_tourists_percent), " ------------> ", transit)
print("Организованные группы туристов(кол-во) ", int(Tourists_count * Group_tourists_percent), "-------> ", group)
print("Туристы учавствующие в соревнованиях(кол-во) ", int(Tourists_count * Sportsmen_tourists_percent), "-------> ", sport)
print("Общая сумма полученная региональным бюджетом: ", group + transit + sport)