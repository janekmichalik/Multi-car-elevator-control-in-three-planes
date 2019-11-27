import numpy as np

from elevator import Elevator
from constant import ElevatorConst, ElevatorColors
from algorithms import waiter_two_elev, waiter_three_elev, _pick_jinxs, scheduler

WAITER = 0


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
            print("ELEV{}: {}".format(id, elev.final_path))

        self.max_len = self.calculate_anim_steps()

        # <----DO TESTOW---->
        # czekanie
        self.elevators[0].final_path = [[4, 3, 4], [4, 3, 3], [4, 2, 3], [4, 1, 3], [4, 0, 3]]
        self.elevators[1].final_path = [[4, 3, 2], [4, 3, 1], [4, 2, 1], [4, 1, 1], [4, 0, 1]]
        self.elevators[2].final_path = [[4, 1, 4], [4, 1, 3], [4, 0, 3]]

        # self.elevators[0].final_path = [[4, 3, 2], [4, 3, 3], [4, 2, 3], [4, 1, 3], [4, 1, 4]]
        # self.elevators[1].final_path = [[4, 1, 4], [4, 1, 3], [4, 1, 2], [4, 1, 1], [4, 0, 1]]
        # self.elevators[2].final_path = [[4, 3, 3], [4, 2, 3], [4, 1, 3], [4, 1, 2], [4, 1, 1], [4, 0, 1]]

        # czekanie 3 windy
        # self.elevators[0].final_path =[[4, 0, 1], [4, 1, 1], [4, 1, 2]]
        # self.elevators[1].final_path =[[4, 2, 1], [4, 1, 1], [4, 1, 2], [4, 1, 3], [4, 1, 4]]
        # self.elevators[2].final_path =[[4, 3, 4], [4, 3, 3], [4, 2, 3], [4, 1, 3], [4, 1, 2]]

        # self.elevators[0].final_path = [[4, 1, 4], [4, 1, 3], [4, 0, 3]]
        # self.elevators[1].final_path = [[4, 1, 2], [4, 1, 3], [4, 1, 4]]
        # self.elevators[2].final_path = [[4, 0, 3], [4, 1, 3], [4, 1, 4]]

        self.elevators[0].DESTINATION = self.elevators[0].final_path[-1]
        self.elevators[1].DESTINATION = self.elevators[1].final_path[-1]
        self.elevators[2].DESTINATION = self.elevators[2].final_path[-1]

        elev1_dest = self.elevators[0].final_path.copy()[-1]
        elev2_dest = self.elevators[1].final_path.copy()[-1]
        elev3_dest = self.elevators[2].final_path.copy()[-1]


        elev1 = self.elevators[0].final_path  # type: List
        elev2 = self.elevators[1].final_path  # type: List
        elev3 = self.elevators[2].final_path  # type: List

        RESTRICTED = []

        steps_for_while = max(len(elev1), len(elev2), len(elev3)) - 1
        cnt, pnt, lenn = 0, 0, 0
        while pnt <= steps_for_while:
            print(pnt)
            if lenn:
                steps_for_while = lenn

            if elev1[pnt] == elev2[pnt] == elev3[pnt]:
                jinx_elev1_waiter, jinx_elev2_hider, not_jinx_elev = _pick_jinxs(cnt=cnt, elevators=self.elevators)
                if jinx_elev1_waiter.final_path[pnt - 1] in not_jinx_elev.final_path[pnt:]:
                    jinx_elev1_waiter, jinx_elev2_hider, not_jinx_elev = _pick_jinxs(cnt=cnt, elevators=self.elevators,
                                                                                     reversed=True)
                jinx1, jinx2,  not_jinx = waiter_three_elev(jinx_elev1_waiter=jinx_elev1_waiter,
                                                            jinx_elev2_hider=jinx_elev2_hider,
                                                            not_jinx_elev=not_jinx_elev, pnt=pnt)
                steps_for_while = max(len(jinx1), len(jinx2), len(not_jinx)) - 1
                del RESTRICTED[:]
            elif elev1[pnt] == elev2[pnt]:
                elev1_ind = self.ret_index(elev1)
                elev2_ind = self.ret_index(elev2)
                if elev1_dest in elev2[pnt:-2]:
                    jinx_elev = self.elevators[elev1_ind]
                    not_jinx_elev = self.elevators[elev2_ind]
                else:
                    jinx_elev = self.elevators[elev2_ind]
                    not_jinx_elev = self.elevators[elev1_ind]

                lenn = self.short_for_wait(jinx_elev, not_jinx_elev, pnt, other_elev=elev3)
                if not_jinx_elev.final_path[pnt] == not_jinx_elev.final_path[pnt - 1]:
                    lenn = self.short_for_wait(not_jinx_elev, jinx_elev, pnt,
                                               find_again=True, other_elev=elev3)
            elif elev1[pnt] == elev3[pnt]:
                elev1_ind = self.ret_index(elev1)
                elev3_ind = self.ret_index(elev3)
                # RESTRICTED = []
                # scheduler(elevX=self.elevators[elev1_ind], elevY=self.elevators[elev3_ind],
                #           RESTRICTED=RESTRICTED, pnt=pnt)
                if elev1_dest in elev3[pnt:]:
                    jinx_elev = self.elevators[elev1_ind]
                    not_jinx_elev = self.elevators[elev3_ind]
                else:
                    jinx_elev = self.elevators[elev3_ind]
                    not_jinx_elev = self.elevators[elev1_ind]

                lenn = self.short_for_wait(jinx_elev, not_jinx_elev, pnt, other_elev=elev2)
                if not_jinx_elev.final_path[pnt] == not_jinx_elev.final_path[pnt - 1]:
                    lenn = self.short_for_wait(not_jinx_elev, jinx_elev, pnt,
                                               find_again=True, other_elev=elev2)
            elif elev2[pnt] == elev3[pnt]:
                elev2_ind = self.ret_index(elev2)
                elev3_ind = self.ret_index(elev3)
                if elev2_dest in elev3[pnt:-2]:
                    jinx_elev = self.elevators[elev2_ind]
                    not_jinx_elev = self.elevators[elev3_ind]
                else:
                    jinx_elev = self.elevators[elev3_ind]
                    not_jinx_elev = self.elevators[elev2_ind]

                lenn = self.short_for_wait(jinx_elev, not_jinx_elev, pnt, other_elev=elev1)
                if not_jinx_elev.final_path[pnt] == not_jinx_elev.final_path[pnt - 1]:
                    lenn = self.short_for_wait(not_jinx_elev, jinx_elev, pnt,
                                               find_again=True, other_elev=elev1)
            else:
                print("Brak punktow wspolnych")
            self.max_len = self.calculate_anim_steps()
            for elev in self.elevators:
                num = self.max_len - len(elev.final_path)
                [elev.final_path.insert(elev.final_path.index(elev.final_path[-1]),
                                        elev.final_path[-1]) for _ in range(num)]
            # try:
            #     for elev in self.elevators:
            #         for p in elev.final_path:
            #             prev = elev.final_path[elev.final_path.index(p)-1]
            #             nxt = elev.final_path[elev.final_path.index(p)+1]
            #             if p != prev and p != nxt and nxt == prev:
            #                 elev.final_path.remove(p)
            # except IndexError:
            #     pass

            cnt = cnt + 1
            pnt = pnt + 1

        self.building_for_plot()

    def ret_index(self, elev):
        ind = 0
        for find in self.elevators:
            if elev == find.final_path:
                ind = self.elevators.index(find)
        return ind

    @staticmethod
    def short_for_wait(jinx_elev, not_jinx_elev, pnt, other_elev, find_again=False):
        jinx, not_jinx = waiter_two_elev(jinx_elev=jinx_elev, not_jinx_elev=not_jinx_elev, pnt=pnt,
                                         find_again=find_again, other_elev=other_elev)
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
