import math
import matplotlib.pyplot as plt

# Вместимость стадиона
StadionCapacity = 45568

# Количество остановок в радиусе киллометра
StopsCount = 4  # 2-автобсу,маршртуки,троллейбусу. 2-трамваи
BusStops = 2
TrumStops = 2

# Вместимость маршрутки
MarshrutCapacity = 17
# Вместимость автобуса и троллейбуса
BusCapacity = 45
TrBusCapacity = 50
TrumCapacity = 100
ParkingLots = 1400



# Массив процентов загруженности стадиона
acommodations = [20, 40, 50, 75, 100]
StadionAccomodation = [23150, 16243, 16523, 10328, 14654, 5247]
sorted(StadionAccomodation)

# Вычисление количества общественного транспорта необходимого при различной заполненности стадиона
TransportCount = []
for i in range(len(acommodations)):
    percent = acommodations[i] / 100
    tmp = []
    for j in range(len(StadionAccomodation)):
        PeopleCount = StadionAccomodation[j] * percent
        TrumLoad = TrumStops * TrumCapacity
        BusLoad = BusCapacity * BusStops + BusStops * TrBusCapacity
        TransportNeed = math.ceil(PeopleCount / (TrumLoad + BusLoad))
        tmp.append(TransportNeed)
    TransportCount.append(tmp)

# Plotting the graph
plt.figure(figsize=(10, 6))

for i in range(len(acommodations)):
    plt.plot(StadionAccomodation, TransportCount[i], label=f'{acommodations[i]}%')

plt.title('Транспортная необходимость vs Количество зрителей')
plt.xlabel('Количество зрителей')
plt.ylabel('Транспортная необходимость')
plt.legend(title='Стадионное размещение')
plt.grid(True)
plt.show()
