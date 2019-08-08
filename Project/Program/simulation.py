import numpy as np

from elevator import Elevator
from constant import ElevatorConst, ElevatorColors


class Simulation:

    def __init__(self):
        super().__init__()
        self.building = None
        self.facecolors, self.edgecolors = None, None

        self.elevators = []
        for elev in range(ElevatorConst.NUM_OF_ELEVATORS):
            id = len(self.elevators)
            elev = Elevator(id)
            self.elevators.append(elev)

        self.building_for_plot()

    def fulfill_building_floor(self):

        self.facecolors = np.array([[['#1f77b430'] *
                                     ElevatorConst.NUM_OF_FLOORS] *
                                    ElevatorConst.NUM_OF_FLOORS_VERTICAL] *
                                   ElevatorConst.NUM_OF_FLOORS_HORIZONTAL)

        for floor in range(ElevatorConst.NUM_OF_FLOORS):
            for row in range(ElevatorConst.NUM_OF_FLOORS_VERTICAL):
                for col in range(ElevatorConst.NUM_OF_FLOORS_HORIZONTAL):
                    for elev in self.elevators:
                        if [row, col] == ElevatorConst.SHAFT_DESC:
                            self.facecolors[row][col][floor] = ElevatorColors.SHAFT_DESC
                        elif [row, col] == ElevatorConst.SHAFT_ASC:
                            self.facecolors[row][col][floor] = ElevatorColors.SHAFT_ASC
                        elif [floor, row, col] == elev.DESTINATION:
                            if elev.id == 0:
                                self.facecolors[row][col][floor] = ElevatorColors.DESTINATION[elev.id]
                            elif elev.id == 1:
                                self.facecolors[row][col][floor] = ElevatorColors.DESTINATION[elev.id]
                        elif row % 2 == 0 and col % 2 == 0:
                            self.facecolors[row][col][floor] = ElevatorColors.WALL

    def building_for_plot(self):

        self.building = np.ones((ElevatorConst.NUM_OF_FLOORS,
                                 ElevatorConst.NUM_OF_FLOORS_VERTICAL,
                                 ElevatorConst.NUM_OF_FLOORS_HORIZONTAL),
                                dtype=int)
        self.fulfill_building_floor()
        self.edgecolors  =np.array([[['#7D84A6'] *
                                     ElevatorConst.NUM_OF_FLOORS] *
                                    ElevatorConst.NUM_OF_FLOORS_VERTICAL] *
                                   ElevatorConst.NUM_OF_FLOORS_HORIZONTAL)
