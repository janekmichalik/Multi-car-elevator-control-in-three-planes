import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from pprint import pprint
from Program.elevator import Elevator
from Program.constant import ElevatorConst
from matplotlib import animation


class Plot(Elevator):

    def __init__(self):

        super().__init__()
        self.fig = None
        self.ax, self.ay = None, None
        self.row_labels = range(self.floor_rows)
        self.col_labels = self.row_labels

        self.fig, (self.ax, self.ay) = plt.subplots(self.num_of_floors_x, self.num_of_floors_y, figsize=(16, 12))
        self.fig.canvas.set_window_title('Multi-car elevator control in three planes')
        self.floor_1 = self.ax.imshow(self.floor, cmap=plt.cm.get_cmap('Accent'))
        self.floor_2 = self.ay.imshow(self.floor, cmap=plt.cm.get_cmap('Accent'))
        self.ani = animation.FuncAnimation(self.fig, self.update, self.data, interval=500, save_count=50)
        self.values = np.arange(0, 5, 1)
        self.labels = ["Path", "Elevator", "Destination", "Source", "Wall"]
        self.colors = [self.floor_1.cmap(self.floor_1.norm(value)) for value in self.values]
        self.patches = [patches.Patch(color=self.colors[i], label=f"{self.labels[i]}") for i in range(len(self.values))]

        self.draw_plot()

    def update(self, data):
        """
        The function that updates the data during simulation.
        :param data:
        :return: simulation
        """
        self.floor_1.set_data(data)
        self.floor_2.set_data(data)
        return self.floor_1, self.floor_2

    def data(self):
        """
        The function using by matplotlib.animation to create simulation data.
        :return: data
        """
        for point in self.shortest_path:
            row, col = point[0], point[1]

            if [row, col] == self.destination:
                self.floor[row][col] = ElevatorConst.ELEVATOR
                return self.ani.event_source.stop()
            if self.floor[row][col] == ElevatorConst.PATH:
                self.floor[row][col] = ElevatorConst.ELEVATOR
                yield self.floor
            if self.floor[row][col] == ElevatorConst.ELEVATOR:
                self.floor[row][col] = ElevatorConst.PATH
                yield self.floor

    def logs(self):
        """
        The functions that returns logs.
        :return: logs
        """

        pprint(self.floor)

        print(f"Destination: ({self.destination})")
        print(f"Source: ({self.source})")

        path = self.shortest_path
        print(path)
        if list(path[-1]) == self.destination:
            print("Destination succeeded")
        if path[0] == self.source:
            print("Source succeeded")

    def draw_plot(self):
        """
        THe function which drawing a plot to UI.
        :return: plot
        """

        self.ax.set_title('Floor no 1')
        self.ay.set_title('Floor no 2')

        self.ax.set_xticks(self.row_labels)
        self.ax.set_yticks(self.col_labels)

        self.ay.set_xticks(self.row_labels)
        self.ay.set_yticks(self.col_labels)

        plt.legend(handles=self.patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
