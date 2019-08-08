import matplotlib.pyplot as plt


class ElevatorConst:

    NUM_OF_ELEVATORS = 2
    NUM_OF_ITERATION = 2

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

    SHAFT_DESC = '#00140d33'
    SHAFT_ASC = '#6a101033'
    WALL = '#2952a3'
    SHAFT_DESC_NO_TRANSPARECNY = '#00140d'
    SHAFT_ASC_NO_TRANSPARECNY = '#6a1010'
    PATH = '#1f77b430'
    DESTINATION = ['#ff99ff4D', '#42f4e24D']
    SOURCE = ['', '']
    ELEVATOR = ['#ff99ff', '#49fdb8']

    EDGE = '#7D84A6'


class PlotConst:
    wall_color = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.WALL)
    path_color = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.PATH)
    desc_shaft = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.SHAFT_DESC_NO_TRANSPARECNY)
    asc_shaft = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.SHAFT_ASC_NO_TRANSPARECNY)
    elevator_1 = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.ELEVATOR[0])
    elevator_2 = plt.Rectangle((0, 0), 1, 1, fc=ElevatorColors.ELEVATOR[1])

    color_list = [wall_color, path_color, desc_shaft, asc_shaft, elevator_1, elevator_2]
    color_labels = ["Wall", "Path", "Descending shaft", "Ascending shaft", "Elevator no 1", "Elevator no 2"]
