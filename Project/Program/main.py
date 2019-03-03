from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import animation

"""
    [[2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.]] """



# tworzymy pietra
fig, (ax, ay) = plt.subplots(1, 2)
fig.suptitle('Elevator', fontsize=20, fontweight='bold')

# wymiar pietra nrowsXncols ( +1 aby konczylo sie sciana)
nrows, ncols = 10 + 1, 10 + 1

# tworzymy pietro
floor_wall = np.zeros(nrows*ncols)
# z macierzy 1wymiarowej robimy 2wymiarowa
floor_wall = floor_wall.reshape((nrows, ncols))

# budujemy ulozenie pietra (sciezki/sciany)
# 2 - sciana
# 0 - sciezka
# 4 - source
# 1 - destination
for wiersz in range(nrows):
    for kolumna in range(ncols):
        if wiersz % 2 == 0 and kolumna % 2 == 0:
            floor_wall[wiersz][kolumna] = 4

# generowanie punktu startowego
source_x = 0
source_y = 0
SOURCE = []

while floor_wall[source_x][source_y] == 4:
    source_x = random.randint(0, 10)
    source_y = random.randint(0, 10)
SOURCE = [source_x, source_y]
floor_wall[source_x][source_y] = 3

# generowanie punktu koncowego
destination_x = 0
destination_y = 0
DESTINATION = []

while floor_wall[destination_x][destination_y] == 4 and (source_x != destination_x or source_y != destination_y):
    destination_x = random.randint(0, 10)
    destination_y = random.randint(0, 10)
DESTINATION = [destination_x, destination_y]
floor_wall[source_x][source_y] = 2


def najkrotsza_sciezka():
    
    dystans_x = abs(SOURCE[0] - DESTINATION[0])
    dystans_y = abs(SOURCE[1] - DESTINATION[1])

    # dwie metody szukania sciezki
    
    # w lini prostej
    #  euclidean_distance = np.sqrt(dystans_x ** 2 + dystans_y ** 2)
    # po wspolrzednych

    manhattan_distance = abs(dystans_x + dystans_y)
    dystans = manhattan_distance
    return dystans


def aktualizowanie_danych(data):
    floor_1.set_data(data)
    floor_2.set_data(data)
    return floor_1, floor_2


def dane_do_animacji():
    for wiersz in range(nrows):
        for kolumna in range(ncols):
            if wiersz == DESTINATION[0] and kolumna == DESTINATION[1]:
                ani.event_source.stop()
            if floor_wall[wiersz][kolumna] == 0:
                floor_wall[wiersz][kolumna] = 1
                yield floor_wall
            if floor_wall[wiersz][kolumna] == 1:
                floor_wall[wiersz][kolumna] = 0
                yield floor_wall


row_labels = range(nrows)
col_labels = row_labels

ax.set_title('Floor no 1')
ay.set_title('Floor no 2')

ax.set_xticks(row_labels)
ax.set_yticks(col_labels)

ay.set_xticks(row_labels)
ay.set_yticks(col_labels)

pprint(floor_wall)

floor_1 = ax.imshow(floor_wall, cmap=plt.cm.get_cmap('Blues'))
floor_2 = ay.imshow(floor_wall, cmap=plt.cm.get_cmap('Blues'))

path = najkrotsza_sciezka()

ani = animation.FuncAnimation(fig, aktualizowanie_danych, dane_do_animacji, interval=500,
                              save_count=50, blit=True)

plt.show()
