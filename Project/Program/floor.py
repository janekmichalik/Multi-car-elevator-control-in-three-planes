import numpy as np
from constant import ElevatorConst


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
        -> 2 - destination - #ff99ff4D - #42f4e24D
        -> 1 - elevator -  #ff99ff - #42f4e2
        -> 5 - shaft - #ff000026
        :return: floor
        """

        self.floor = np.zeros(ElevatorConst.NUM_OF_FLOORS_VERTICAL * ElevatorConst.NUM_OF_FLOORS_HORIZONTAL)
        self.floor = self.floor.reshape((ElevatorConst.NUM_OF_FLOORS_VERTICAL, ElevatorConst.NUM_OF_FLOORS_HORIZONTAL))

        for row in range(ElevatorConst.NUM_OF_FLOORS_VERTICAL):
            for col in range(ElevatorConst.NUM_OF_FLOORS_HORIZONTAL):
                if [row, col] == ElevatorConst.SHAFT_DESC:
                    self.floor[row][col] = ElevatorConst.SHAFT_D
                elif [row, col] == ElevatorConst.SHAFT_ASC:
                    self.floor[row][col] = ElevatorConst.SHAFT_A
                elif row % 2 == 0 and col % 2 == 0:
                    self.floor[row][col] = ElevatorConst.WALL

        for _ in range(ElevatorConst.NUM_OF_FLOORS):
            self.floors.append(self.floor.copy())