import numpy as np
from Program.constant import ElevatorConst


class Floor:

    def __init__(self):

        self.floors = []
        self.create_floor()

    def create_floor(self):
        """
        The function that creates the floor according to the following scheme:
        -> 4 - wall - #2952a3
        -> 0 - path - #1f77b430
        -> 3 - source
        -> 2 - destination - #ff99ff4D
        -> 1 - elevator -  #ff99ff
        -> 5 - shaft - #ff000026
        :return: floor
        """

        self.floor = np.zeros(ElevatorConst.NUM_OF_FLOORS_VERTICAL * ElevatorConst.NUM_OF_FLOORS_HORIZONTAL)
        self.floor = self.floor.reshape((ElevatorConst.NUM_OF_FLOORS_VERTICAL, ElevatorConst.NUM_OF_FLOORS_HORIZONTAL))

        for row in range(ElevatorConst.NUM_OF_FLOORS_VERTICAL):
            for col in range(ElevatorConst.NUM_OF_FLOORS_HORIZONTAL):
                if [row, col] == ElevatorConst.SHAFT_3D:
                    self.floor[row][col] = ElevatorConst.SHAFT
                elif row % 2 == 0 and col % 2 == 0:
                    self.floor[row][col] = ElevatorConst.WALL

        # self.floor = np.zeros(ElevatorConst.FLOOR_ROWS * ElevatorConst.FLOOR_COLS)
        # self.floor = self.floor.reshape((ElevatorConst.FLOOR_ROWS, ElevatorConst.FLOOR_COLS))
        #
        # for row in range(ElevatorConst.FLOOR_ROWS):
        #     for col in range(ElevatorConst.FLOOR_COLS):
        #         if [row, col] == ElevatorConst.SHAFT_1:
        #             self.floor[row][col] = ElevatorConst.SHAFT
        #         elif [row, col] == ElevatorConst.SHAFT_2:
        #             self.floor[row][col] = ElevatorConst.SHAFT
        #         elif row % 2 == 0 and col % 2 == 0:
        #             self.floor[row][col] = ElevatorConst.WALL

        for _ in range(ElevatorConst.NUM_OF_FLOORS):
            self.floors.append(self.floor.copy())