import numpy as np

from Program.elevator import ElevatorConst, Elevator


class Simulation(Elevator):

    def __init__(self):
        super().__init__()
        self.building = None
        self.facecolors, self.edgecolors = None, None

        self.elevators = []
        for elev in range(ElevatorConst.NUM_OF_ELEVATORS):
            elev = Elevator()
            self.elevators.append(elev)

        # for elev in self.elevators:
        #     self.floors[elev.source_flr][elev.source_x, elev.source_y] = ElevatorConst.SOURCE
        #     self.floors[elev.destination_flr][elev.dest_x, elev.dest_y] = ElevatorConst.DESTINATION

        self.building_for_plot()

    def fulfill_building_floor(self):

        self.facecolors = np.array([[['#1f77b430'] *
                                     ElevatorConst.NUM_OF_FLOORS] *
                                    ElevatorConst.NUM_OF_FLOORS_VERTICAL] *
                                   ElevatorConst.NUM_OF_FLOORS_HORIZONTAL)

        for floor in range(ElevatorConst.NUM_OF_FLOORS):
            for row in range(ElevatorConst.NUM_OF_FLOORS_VERTICAL):
                for col in range(ElevatorConst.NUM_OF_FLOORS_HORIZONTAL):
                    if [row, col] == ElevatorConst.SHAFT_3D:
                        self.facecolors[row][col][floor] = '#ff000026'
                    elif [floor, row, col] == self.SOURCE:
                        self.facecolors[row][col][floor] = '#ff99ff'
                    elif [floor, row, col] == self.DESTINATION:
                        self.facecolors[row][col][floor] = '#00cc99'
                    elif row % 2 == 0 and col % 2 == 0:
                        self.facecolors[row][col][floor] = '#2952a3BF'

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
