import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from pprint import pprint
from Program.elevator import Elevator
from Program.floor import Floor
from Program.constant import ElevatorConst
from matplotlib import animation


class Plot(Floor):

    def __init__(self):

        super().__init__()

        self.fig = None
        self.ax, self.ay, self.az = None, None, None
        self.row_labels = range(ElevatorConst.FLOOR_ROWS)
        self.col_labels = self.row_labels

        self.fig, (self.ax, self.ay) = plt.subplots(ElevatorConst.NUM_OF_FLOORS_X,
                                                    ElevatorConst.NUM_OF_FLOORS_Y,
                                                    figsize=(16, 12))
        self.fig.canvas.set_window_title('Multi-car elevator control in three planes')

        self.elevators = []
        for elev in range(ElevatorConst.NUM_OF_ELEVATORS):
            elev = Elevator()
            self.elevators.append(elev)

        for elev in self.elevators:
            self.floors[elev.source_flr][elev.source_x, elev.source_y] = ElevatorConst.SOURCE
            self.floors[elev.destination_flr][elev.dest_x, elev.dest_y] = ElevatorConst.DESTINATION

        # pierwsze pietro - wykres
        self.floor_1 = self.ax.imshow(self.floors[0], cmap=plt.cm.get_cmap('Accent'))
        # drugie pietro - wykres
        self.floor_2 = self.ay.imshow(self.floors[1], cmap=plt.cm.get_cmap('Accent'))
        # trzecie pietro - wykres
        # self.floor_3 = self.az.imshow(self.elevators[2].floors[2], cmap=plt.cm.get_cmap('Accent'))

        self.ani1 = animation.FuncAnimation(self.fig, self.update1, self.data1, interval=400, save_count=50, repeat=False)
        self.flag1 = True
        self.flag2 = True
        self.ani2 = animation.FuncAnimation(self.fig, self.update2, self.data2, interval=400, save_count=50, repeat=False)
        # self.ani3 = animation.FuncAnimation(self.fig, self.update3, self.data3, interval=500, save_count=50)

        self.draw_plot()

    def update1(self, data1):
        """
        The function that updates the data during simulation.
        :param data:
        :return: simulation
        """
        self.floor_1.set_data(data1)
        if self.flag1:
            return self.floor_1

    def update2(self, data2):
        """
        The function that updates the data during simulation.
        :param data:
        :return: simulation
        """
        self.floor_2.set_data(data2)
        return self.floor_2

    # def update3(self, data3):
    #     """
    #     The function that updates the data during simulation.
    #     :param data:
    #     :return: simulation
    #     """
    #     self.floor_3.set_data(data3)
    #     return self.floor_3

    def data1(self):
        """
        The function using by matplotlib.animation to create simulation data.
        :return: data
        """
        if self.elevators[0].source_flr != self.elevators[0].destination_flr:
            self.elevators[0].shortest_path = self.elevators[0].extend_path
            _, x, y = self.elevators[0].extend_path[-1]
            self.elevators[0].destination = [x, y]
        for point in self.elevators[0].shortest_path:
            _, row, col = point[0], point[1], point[2]
            if [row, col] == self.elevators[0].destination:
                self.floors[0][row][col] = ElevatorConst.ELEVATOR
                return self.ani1.event_source.stop()
            if [row, col] == ElevatorConst.SHAFT_1:
                self.floors[0][row][col] = ElevatorConst.ELEVATOR
                yield self.floors[0]
                self.floors[0][row][col] = ElevatorConst.SHAFT
            if [row, col] == ElevatorConst.SHAFT_2:
                self.floors[0][row][col] = ElevatorConst.ELEVATOR
                yield self.floors[0]
                self.floors[0][row][col] = ElevatorConst.SHAFT
            if self.floors[0][row][col] == ElevatorConst.PATH:
                self.floors[0][row][col] = ElevatorConst.ELEVATOR
                yield self.floors[0]
            if self.floors[0][row][col] == ElevatorConst.ELEVATOR:
                self.floors[0][row][col] = ElevatorConst.PATH
                yield self.floors[0]


    def data2(self):
        """
        The function using by matplotlib.animation to create simulation data.
        :return: data
        """
        if self.elevators[0].source_flr != self.elevators[0].destination_flr:
            self.elevators[0].shortest_path = self.elevators[0].path
            _, x, y = self.elevators[0].path[-1]
            self.elevators[0].destination = [x, y]
        for point in self.elevators[0].shortest_path:
            _, row, col = point[0], point[1], point[2]
            if [row, col] == self.elevators[0].destination:
                self.floors[1][row][col] = ElevatorConst.ELEVATOR
                return self.ani2.event_source.stop()
            if [row, col] == ElevatorConst.SHAFT_1:
                self.floors[1][row][col] = ElevatorConst.ELEVATOR
                yield self.floors[1]
                self.floors[1][row][col] = ElevatorConst.SHAFT
            if [row, col] == ElevatorConst.SHAFT_2:
                self.floors[1][row][col] = ElevatorConst.ELEVATOR
                yield self.floors[1]
                self.floors[1][row][col] = ElevatorConst.SHAFT
            if self.floors[1][row][col] == ElevatorConst.PATH:
                self.floors[1][row][col] = ElevatorConst.ELEVATOR
                yield self.floors[1]
            if self.floors[1][row][col] == ElevatorConst.ELEVATOR:
                self.floors[1][row][col] = ElevatorConst.PATH
                yield self.floors[1]

    # def data3(self):
    #     """
    #     The function using by matplotlib.animation to create simulation data.
    #     :return: data
    #     """
    #
    #     for point in self.elevators[2].shortest_path:
    #         row, col = point[0], point[1]
    #
    #         if [row, col] == ElevatorConst.SHAFT_1:
    #             self.elevators[2][row][col] = ElevatorConst.ELEVATOR
    #             yield self.elevators[2]
    #             self.elevators[2][row][col] = ElevatorConst.SHAFT
    #         if [row, col] == ElevatorConst.SHAFT_2:
    #             self.elevators[2][row][col] = ElevatorConst.ELEVATOR
    #             yield self.elevators[2]
    #             self.elevators[2][row][col] = ElevatorConst.SHAFT
    #         if [row, col] == self.elevators[2].destination:
    #             self.elevators[2][row][col] = ElevatorConst.ELEVATOR
    #             return self.ani3.event_source.stop()
    #         if self.elevators[2][row][col] == ElevatorConst.PATH:
    #             self.elevators[2][row][col] = ElevatorConst.ELEVATOR
    #             yield self.elevators[2]
    #         if self.elevators[2][row][col] == ElevatorConst.ELEVATOR:
    #             self.elevators[2][row][col] = ElevatorConst.PATH
    #             yield self.elevators[2]

    # def logs(self):
    #     """
    #     The functions that returns logs.
    #     :return: logs
    #     """
    #
    #     pprint(self.floor)
    #
    #     print(f"Destination: ({self.destination})")
    #     print(f"Source: ({self.source})")
    #
    #     path = self.shortest_path
    #     print(path)
    #     if list(path[-1]) == self.destination:
    #         print("Destination succeeded")
    #     if path[0] == self.source:
    #         print("Source succeeded")

    def draw_plot(self):
        """
        THe function which drawing a plot to UI.
        :return: plot
        """

        self.values = np.arange(0, 6, 1)
        self.labels = ["Path", "Elevator", "Destination", "Source", "Wall", "Shaft"]
        self.colors = [self.floor_1.cmap(self.floor_1.norm(value)) for value in self.values]
        self.patches = [patches.Patch(color=self.colors[i], label=f"{self.labels[i]}") for i in range(len(self.values))]

        self.ax.set_title('Floor no 1')
        self.ay.set_title('Floor no 2')
        # self.az.set_title('Floor no 3')

        self.ax.set_xticks(self.row_labels)
        self.ax.set_yticks(self.col_labels)

        self.ay.set_xticks(self.row_labels)
        self.ay.set_yticks(self.col_labels)

        # self.az.set_xticks(self.row_labels)
        # self.az.set_yticks(self.col_labels)

        plt.legend(handles=self.patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
