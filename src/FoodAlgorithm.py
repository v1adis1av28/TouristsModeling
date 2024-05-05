import numpy as np
import math
import random
from tabulate import tabulate

# Данные
Tourists = [200, 500, 1500, 3000, 10000, 50000]
PricesInArea = [700, 300, 450, 600, 800, 1500, 500, 900, 300, 800]
MiddleCapacity = 30
Nalog = 0.2

# Вычисление среднего чека
MiddleCheck = np.mean(PricesInArea)
print("Средний чек:", MiddleCheck)

# Вычисление полной выручки
income = []
for i in range(len(Tourists)):
    tmp = [(Tourists[i] / 4 * random.choice(PricesInArea)) * Nalog for _ in range(4)]
    income.append(tmp)

print("Полная загруженность без учета внешних параметров:")
print(income)

# Утренняя выручка
percent_morning_capacity = [0.2, 0.4, 0.6]
morning_income = []
print("Утренняя выручка:")
for i in range(len(Tourists)):
    total_morning_income = 0
    for j in range(len(percent_morning_capacity)):
        customers = Tourists[i] * percent_morning_capacity[j]
        total_morning_income += sum([Nalog*(math.ceil(customers / 4) * random.choice(PricesInArea)) for _ in range(4)])
    morning_income.append(total_morning_income*Nalog)
print(morning_income)

# Вечерняя выручка
percent_evening_capacity = [0.8, 0.6, 0.4]
evening_income = []
print("Вечерняя выручка:")
for i in range(len(Tourists)):
    total_evening_income = 0
    for j in range(len(percent_evening_capacity)):
        customers = Tourists[i] * percent_evening_capacity[j]
        total_evening_income += sum([Nalog*(math.ceil(customers / 4) * random.choice(PricesInArea)) for _ in range(4)])
    evening_income.append(total_evening_income*Nalog)
print(evening_income)

# Форматирование данных для таблицы
income_data = [["Туристы", "Полная загруженность", "Утренняя выручка", "Вечерняя выручка"]]
for i in range(len(Tourists)):
    row = [
        Tourists[i],
        sum(income[i]),
        morning_income[i],
        evening_income[i]
    ]
    income_data.append(row)

# Вывод таблицы
print(tabulate(income_data, headers="firstrow", tablefmt="grid"))

#osm nx библиотека для работы с городом,