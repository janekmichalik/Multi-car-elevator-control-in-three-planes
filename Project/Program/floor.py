import numpy as np
from Program.constant import ElevatorConst


class Floor:

    def __init__(self):

        self.num_of_floors_x = 1
        self.num_of_floors_y = 3

        self.floor_rows = 10 + 1
        self.floor_cols = self.floor_rows

        self.floor = None
        self.create_floor()

    def create_floor(self):
        """
        The function that creates the floor according to the following scheme:
        -> 4 - wall
        -> 0 - path
        -> 3 - source
        -> 2 - destination
        -> 1 - elevator
        -> 5 - shaft
        :return: floor
        """

        self.floor = np.zeros(self.floor_rows * self.floor_cols)
        self.floor = self.floor.reshape((self.floor_rows, self.floor_cols))

        for row in range(self.floor_rows):
            for col in range(self.floor_cols):
                if [row, col] == ElevatorConst.SHAFT_1:
                    self.floor[row][col] = ElevatorConst.SHAFT
                elif [row, col] == ElevatorConst.SHAFT_2:
                    self.floor[row][col] = ElevatorConst.SHAFT
                elif row % 2 == 0 and col % 2 == 0:
                    self.floor[row][col] = ElevatorConst.WALL
