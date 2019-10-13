import random

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

        # <----DO TESTOW---->
        self.elevators[0].final_path = [
            [4,1,0], [4,1,1], [4,1,2], [4,1,3], [4,1,4],
            [4,1,3], [4,0,3]
        ]
        self.elevators[1].final_path = [
            [4,2,1], [4,1,1], [4,0,1],
            [4,1,1], [4,2,1], [4,3,1], [4,4,1]
        ]

        elev1 = self.elevators[0].final_path
        elev2 = self.elevators[1].final_path
        lenght = min(len(elev1), len(elev2))
        cnt = 0
        for pnt in range(lenght):
            if elev1[pnt] == elev2[pnt]:
                jinx_id = 0 if cnt % 2 == 0 else 1
                jinx_elev = self.elevators[jinx_id]
                not_jinx_id = int(not jinx_id)
                not_jinx_elev = self.elevators[not_jinx_id]

                # jesli obecny punkt pechowej windy nie znajduje sie w sciezce szczesliwej windy
                # - winda pechowa czeka
                t1 = jinx_elev.final_path[pnt-1]
                t2 = not_jinx_elev.final_path
                if jinx_elev.final_path[pnt-1] \
                        not in not_jinx_elev.final_path:
                    wait_point = jinx_elev.final_path[pnt-1]
                    wait_pint_index = jinx_elev.final_path.index(wait_point)
                    tmp = jinx_elev.final_path
                    stops = 3 if wait_point == jinx_elev.DESTINATION else 2
                    [tmp.insert(wait_pint_index, wait_point) for _ in range(stops)]
                cnt = cnt + 1
            else:
                print("Brak punktow wspolnych")


        self.building_for_plot()

    def fulfill_building_floor(self):

        self.facecolors = np.array([[[ElevatorColors.PATH] *
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
                        elif row % 2 == 0 and col % 2 == 0:
                            self.facecolors[row][col][floor] = ElevatorColors.WALL

    def building_for_plot(self):

        self.building = np.ones((ElevatorConst.NUM_OF_FLOORS,
                                 ElevatorConst.NUM_OF_FLOORS_VERTICAL,
                                 ElevatorConst.NUM_OF_FLOORS_HORIZONTAL),
                                dtype=int)
        self.fulfill_building_floor()
        self.edgecolors  =np.array([[[ElevatorColors.EDGE] *
                                     ElevatorConst.NUM_OF_FLOORS] *
                                    ElevatorConst.NUM_OF_FLOORS_VERTICAL] *
                                   ElevatorConst.NUM_OF_FLOORS_HORIZONTAL)
