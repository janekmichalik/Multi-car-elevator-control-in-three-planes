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

        self.max_len = self.calculate_anim_steps()
        for elev in self.elevators:
            num = self.max_len - len(elev.final_path)
            [elev.final_path.insert(elev.final_path.index(elev.final_path[-1]),
                                    elev.final_path[-1]) for _ in range(num)]

        # # <----DO TESTOW---->
        # self.elevators[0].final_path = [
        #     [4,4,3], [4,3,3], [4,3,2], [4,3,1], [4,3,0]
        # ]
        # self.elevators[1].final_path = [
        #     [4,2,3], [4,3,3], [4,3,2],[4,3,1], [4,4,1]
        # ]
        # self.elevators[2].final_path = [
        #     [4,3,4], [4,3,3], [4,3,2], [4,3,1], [4,2,1]
        # ]

        elev1 = self.elevators[0].final_path
        elev2 = self.elevators[1].final_path
        elev3 = self.elevators[2].final_path
        lenght = min(len(elev1), len(elev2), len(elev3))
        cnt = 0
        for pnt in range(lenght):
            if elev1[pnt] == elev2[pnt] == elev3[pnt]:
                if cnt % 2:
                    jinx_ids = [0,1]
                    not_jinx_id = 2
                elif cnt % 3:
                    jinx_ids = [1,2]
                    not_jinx_id = 0
                else:
                    jinx_ids = [0,2]
                    not_jinx_id = 1
                jinx_elev1 = self.elevators[jinx_ids[0]]
                jinx_elev2 = self.elevators[jinx_ids[1]]
                not_jinx_elev = self.elevators[not_jinx_id]

                # jesli obecny punkt pechowej windy nie znajduje sie w sciezce szczesliwej windy
                # - winda pechowa czeka
                if (jinx_elev1.final_path[pnt-1]
                    not in not_jinx_elev.final_path) and\
                        (jinx_elev2.final_path[pnt-1] not in not_jinx_elev.final_path):
                    wait_point1 = jinx_elev1.final_path[pnt-1]
                    wait_point2 = jinx_elev2.final_path[pnt-1]
                    wait_pint_index1 = jinx_elev1.final_path.index(wait_point1)
                    wait_pint_index2 = jinx_elev2.final_path.index(wait_point2)

                    tmp1 = jinx_elev1.final_path
                    tmp2 = jinx_elev2.final_path
                    stops1 = 3 if wait_point1 == jinx_elev1.DESTINATION else 2
                    [tmp1.insert(wait_pint_index1, wait_point1) for _ in range(stops1)]
                    stops2 = 4 if wait_point2 == jinx_elev2.DESTINATION else 3
                    [tmp2.insert(wait_pint_index2, wait_point2) for _ in range(stops2)]
            elif elev1[pnt] == elev2[pnt]:
                jinx_id = 0 if cnt % 2 == 0 else 1
                jinx_elev = self.elevators[jinx_id]
                not_jinx_id = int(not jinx_id)
                not_jinx_elev = self.elevators[not_jinx_id]
                self.waiter(jinx_elev=jinx_elev, not_jinx_elev=not_jinx_elev, pnt=pnt)
            elif elev1[pnt] == elev3[pnt]:
                jinx_id = 0 if cnt % 2 == 0 else 2
                jinx_elev = self.elevators[jinx_id]
                not_jinx_id = int(not jinx_id)
                not_jinx_elev = self.elevators[not_jinx_id]
                self.waiter(jinx_elev=jinx_elev, not_jinx_elev=not_jinx_elev, pnt=pnt)
            elif elev2[pnt] == elev3[pnt]:
                jinx_id = 1 if cnt % 2 == 0 else 2
                jinx_elev = self.elevators[jinx_id]
                not_jinx_id = int(not jinx_id)
                not_jinx_elev = self.elevators[not_jinx_id]
                self.waiter(jinx_elev=jinx_elev, not_jinx_elev=not_jinx_elev, pnt=pnt)
            else:
                print("Brak punktow wspolnych")
            cnt = cnt + 1


        self.building_for_plot()

    def calculate_anim_steps(self):
        tmp = []
        for elev in self.elevators:
            tmp.append(len(elev.final_path))
        self.max_len = max(tmp)
        return self.max_len

    @staticmethod
    def waiter(jinx_elev, not_jinx_elev, pnt):

        # jesli obecny punkt pechowej windy nie znajduje sie w sciezce szczesliwej windy
        # - winda pechowa czeka
        if jinx_elev.final_path[pnt - 1] \
                not in not_jinx_elev.final_path:
            wait_point = jinx_elev.final_path[pnt - 1]
            wait_pint_index = jinx_elev.final_path.index(wait_point)
            tmp = jinx_elev.final_path
            stops = 3 if wait_point == jinx_elev.DESTINATION else 2
            [tmp.insert(wait_pint_index, wait_point) for _ in range(stops)]
        return

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
