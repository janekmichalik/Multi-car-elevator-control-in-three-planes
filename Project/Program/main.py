import collections
import random
from pprint import pprint

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
import numpy as np


class ElevatorConst:

    WALL = 4
    PATH = 0
    ELEVATOR = 1
    SOURCE = 3
    DESTINATION = 2

    floor_schema = """
                    [[2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.],
                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                    [2., 0., 2., 0., 2., 0., 2., 0., 2., 0., 2.]] """


class Floor:

    def __init__(self):

        self.num_of_floors_x = 1
        self.num_of_floors_y = 2

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
        :return: floor
        """

        self.floor = np.zeros(self.floor_rows * self.floor_cols)
        self.floor = self.floor.reshape((self.floor_rows, self.floor_cols))

        for row in range(self.floor_rows):
            for col in range(self.floor_cols):
                if row % 2 == 0 and col % 2 == 0:
                    self.floor[row][col] = ElevatorConst.WALL


class Elevator(Floor):

    def __init__(self):

        super().__init__()

        self.source_x = 0
        self.source_y = 0
        self.source = [self.source_x, self.source_y]

        self.shortest_path = None

        self.dest_x = 0
        self.dest_y = 0
        self.destination = [self.dest_x, self.dest_y]
        self.generate_starting_point()
        self.generate_ending_point()
        self.compute_shortest_path()

    def generate_starting_point(self):
        """
        The function that generate the starting point (source) randomly.
        :return: source
        """

        while self.floor[self.source_x][self.source_y] == 4:
            self.source_x = random.randint(0, 10)
            self.source_y = random.randint(0, 10)
        self.source = [self.source_x, self.source_y]
        self.floor[self.source_x, self.source_y] = ElevatorConst.SOURCE

    def generate_ending_point(self):
        """
        The function that generate the ending point (destination) randomly.
        :return: destination
        """

        while self.floor[self.dest_x][self.dest_y] == 4 \
                and (self.source_x != self.dest_x or self.source_y != self.dest_y):
            self.dest_x = random.randint(0, 10)
            self.dest_y = random.randint(0, 10)
        self.destination = [self.dest_x, self.dest_y]
        self.floor[self.dest_x][self.dest_y] = ElevatorConst.DESTINATION

    def compute_shortest_path(self):
        """
        The function that compute the shortest path from source to destination.
        :return: shortest_path
        """

        queue = collections.deque([[self.source]])
        seen = []
        seen.append(set(self.source))
        while queue:
            self.shortest_path = queue.popleft()
            x, y = self.shortest_path[-1]
            if self.floor[x][y] == 2:
                return
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < self.floor_rows and 0 <= y2 < self.floor_cols and self.floor[y2][x2] != 4 and (x2, y2) not in seen:
                    queue.append(self.shortest_path + [(x2, y2)])
                    seen.append((x2, y2))


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


def main():
    simulation = Plot()
    simulation.logs()

main()
