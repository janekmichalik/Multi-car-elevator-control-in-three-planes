from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from IPython.display import HTML

from Program.constant import ElevatorConst
from Program.simulation import Simulation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


class Plot(Simulation):

    def __init__(self):
        super().__init__()

        self.ax, self.voxels = None, None
        self.fig = plt.figure()
        self.filled = np.ones(self.building.shape)

        # upscale the above voxel image, leaving gaps
        self.filled_2 = self.explode(self.filled)
        self.fcolors_2 = self.explode(self.facecolors)
        self.ecolors_2 = self.explode(self.edgecolors)

        self.x, self.y, self.z = None, None, None

        self.shrink_gaps()
        # Creating the Animation object
        lenght = len(self.elevators[0].shortest_path)
        self.ani = animation.FuncAnimation(self.fig, self.update, lenght, interval=100, blit=False)
        self.draw_plot()

    def logs(self):
        """
        The functions that returns logs.
        :return: logs
        """

        print(f"Destination: ({self.DESTINATION})")
        print(f"Source: ({self.SOURCE})")

        path = self.elevators[0].shortest_path
        print(len(path))
        print(path)
        if list(path[-1]) == self.DESTINATION:
            print("Destination succeeded")
        if path[0] == self.SOURCE:
            print("Source succeeded")

    def update(self, num):
        self.ax.cla()
        point = self.elevators[0].shortest_path
        floor, col, row = point[num]

        self.facecolors[row][col][floor] = '#993300'
        self.fcolors_2 = self.explode(self.facecolors)

        self.ax.voxels(self.x, self.y, self.z, self.filled_2,
                       facecolors=self.fcolors_2, edgecolors=self.ecolors_2)

    def shrink_gaps(self):
        # Shrink the gaps
        self.x, self.y, self.z = np.indices(np.array(self.filled_2.shape) + 1).astype(float) // 2
        self.x[0::2, :, :] += 0.05
        self.y[:, 0::2, :] += 0.05
        self.z[:, :, 0::2] += 0.05
        self.x[1::2, :, :] += 0.95
        self.y[:, 1::2, :] += 0.95
        self.z[:, :, 1::2] += 0.95

    @staticmethod
    def explode(data):
        size = np.array(data.shape) * 2
        data_e = np.zeros(size - 1, dtype=data.dtype)
        data_e[::2, ::2, ::2] = data
        return data_e

    def draw_plot(self):
        self.fig.canvas.set_window_title('Multi-car elevator control in three planes')
        self.ax = self.fig.gca(projection='3d')
        self.ax.voxels(self.x, self.y, self.z, self.filled_2,
                       facecolors=self.fcolors_2, edgecolors=self.ecolors_2)
        plt.show()