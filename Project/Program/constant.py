import matplotlib.pyplot as plt


class ElevatorConst:

    NUM_OF_ELEVATORS = 3
    NUM_OF_ITERATION = 1

    NUM_OF_FLOORS = 5
    NUM_OF_FLOORS_VERTICAL = 5
    NUM_OF_FLOORS_HORIZONTAL = 5

    WALL = 4
    PATH = 0
    ELEVATOR = 1
    SOURCE = 3
    DESTINATION = 2
    SHAFT_D = 5
    SHAFT_A = 6

    SHAFT_DESC = [1, 3]
    SHAFT_ASC = [3, 1]


class ElevatorColors:

    SHAFT_DESC = '#00140d0D'
    SHAFT_ASC = '#6a10100D'
    WALL = '#2952a3'
    SHAFT_DESC_NO_TRANSPARECNY = '#00140d'
    SHAFT_ASC_NO_TRANSPARECNY = '#6a1010'
    PATH = '#1f77b41A'
    DESTINATION = ['#ff8b1f40', '#42f4e240', '#f44e8540']
    SOURCE = ['', '']
    ELEVATOR = ['#ecff42', '#49fdb8', '#f44e85']

    EDGE = '#c2c2c233'


class PlotConst:
    wall_color = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.WALL)
    path_color = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.PATH)
    desc_shaft = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.SHAFT_DESC_NO_TRANSPARECNY)
    asc_shaft = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.SHAFT_ASC_NO_TRANSPARECNY)
    elevator_1 = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.ELEVATOR[0])
    elevator_2 = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.ELEVATOR[1])
    elevator_3 = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.ELEVATOR[2])

    color_list = [wall_color, path_color, desc_shaft, asc_shaft, elevator_1, elevator_2, elevator_3]
    color_labels = ["Ściana", "Ścieżka", "Szacht w dół", "Szacht w górę", "Winda nr 1", "Winda nr 2", "Winda nr 3"]

