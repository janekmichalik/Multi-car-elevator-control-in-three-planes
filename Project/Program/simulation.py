import random
import numpy as np

from elevator import Elevator
from constant import ElevatorConst, ElevatorColors
from algorithms import waiter_two_elev, waiter_three_elev

LEN = 0


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

        # <----DO TESTOW---->
        # czekanie
        self.elevators[0].final_path = [[4, 3, 2], [4, 3, 3], [4, 2, 3], [4, 1, 3], [4, 1, 4]]
        self.elevators[1].final_path = [[4, 1, 4], [4, 1, 3], [4, 1, 2], [4, 1, 1], [4, 0, 1]]
        self.elevators[2].final_path = [[4, 3, 3], [4, 2, 3], [4, 1, 3], [4, 1, 2], [4, 1, 1], [4, 0, 1]]

        self.elevators[0].DESTINATION = self.elevators[0].final_path[-1]
        self.elevators[1].DESTINATION = self.elevators[1].final_path[-1]
        self.elevators[2].DESTINATION = self.elevators[2].final_path[-1]

        # chowanie
        # self.elevators[0].final_path = [[4, 0, 3], [4, 1, 3], [4, 2, 3], [4, 3, 3], [4, 3, 2]]
        # self.elevators[1].final_path = [[4, 0, 1], [4, 1, 1], [4, 2, 1], [4, 3, 1], [4, 3, 2], [4, 3, 3]]

        self.elev1 = self.elevators[0].final_path
        self.elev2 = self.elevators[1].final_path
        self.elev3 = self.elevators[2].final_path
        global LEN
        LEN = min(len(self.elev1), len(self.elev2), len(self.elev3))
        cnt = 0
        pnt = 0
        lenn = 0
        while pnt <= LEN:
            print(pnt)
            if lenn:
                LEN = lenn
            if self.elev1[pnt] == self.elev2[pnt] == self.elev3[pnt]:
                jinx1, jinx2,  not_jinx = waiter_three_elev(cnt=cnt, pnt=pnt, elevators=self.elevators)
                if cnt % 2:
                    jinx_ids = [0, 1]
                    not_jinx_id = 2
                    self.elev1 = self.elevators[jinx_ids[0]]
                    self.elev2 = self.elevators[jinx_ids[1]]
                    self.elev3 = self.elevators[not_jinx_id]
                elif cnt % 3:
                    jinx_ids = [1, 2]
                    not_jinx_id = 0
                    self.elev1 = self.elevators[jinx_ids[1]]
                    self.elev2 = self.elevators[jinx_ids[2]]
                    self.elev3 = self.elevators[not_jinx_id]
                else:
                    jinx_ids = [0, 2]
                    not_jinx_id = 1
                    self.elev1 = self.elevators[jinx_ids[0]]
                    self.elev2 = self.elevators[jinx_ids[2]]
                    self.elev3 = self.elevators[not_jinx_id]
                LEN = min(len(jinx1), len(jinx2), len(not_jinx))
            elif self.elev1[pnt] == self.elev2[pnt]:
                jinx_id = 0 if cnt % 2 == 0 else 1
                not_jinx_id = 1 if jinx_id == 0 else 0
                lenn = self.short_for_wait(jinx_id, not_jinx_id, cnt, pnt=pnt)
            elif self.elev1[pnt] == self.elev3[pnt]:
                jinx_id = 0 if cnt % 2 == 0 else 2
                not_jinx_id = 2 if jinx_id == 0 else 0
                lenn = self.short_for_wait(jinx_id, not_jinx_id, cnt, pnt=pnt)
            elif self.elev2[pnt] == self.elev3[pnt]:
                jinx_id = 1 if cnt % 2 == 0 else 2
                not_jinx_id = 2 if jinx_id == 0 else 1
                lenn = self.short_for_wait(jinx_id, not_jinx_id, cnt, pnt=pnt)
            else:
                print("Brak punktow wspolnych")
            self.max_len = self.calculate_anim_steps()
            for elev in self.elevators:
                num = self.max_len - len(elev.final_path)
                [elev.final_path.insert(elev.final_path.index(elev.final_path[-1]),
                                        elev.final_path[-1]) for _ in range(num)]
            cnt = cnt + 1
            pnt = pnt + 1

        self.building_for_plot()

    def short_for_wait(self, jinx_id, not_jinx_id, cnt, pnt):
        jinx_elev = self.elevators[jinx_id]
        not_jinx_elev = self.elevators[not_jinx_id]
        jinx, not_jinx = waiter_two_elev(jinx_elev=jinx_elev, not_jinx_elev=not_jinx_elev, pnt=pnt)
        if cnt % 2 == 0:
            self.elev1 = jinx
            self.elev2 = not_jinx
        else:
            self.elev2 = jinx
            self.elev1 = not_jinx
        return min(len(jinx), len(not_jinx))

    def calculate_anim_steps(self):
        tmp = []
        for elev in self.elevators:
            tmp.append(len(elev.final_path))
        self.max_len = max(tmp)
        return self.max_len

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
