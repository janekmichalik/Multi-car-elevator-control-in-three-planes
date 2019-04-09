import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from Program.constant import ElevatorConst
from Program.simulation import Simulation
from mpl_toolkits.mplot3d import Axes3D


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
        self.t = self.elevators[0]
        self.ani = animation.FuncAnimation(self.fig, self.update, lenght, interval=350, blit=False, repeat=True)
        self.draw_plot()

    def logs(self):
        """
        The functions that returns logs.
        :return: logs
        """

        print(f"Destination: ({self.t.DESTINATION})")
        print(f"Source: ({self.t.SOURCE})")

        path = self.t.shortest_path
        print(len(path))
        print(path)
        if list(path[-1]) == self.t.DESTINATION:
            print("Destination succeeded")
        if path[0] == self.t.SOURCE:
            print("Source succeeded")

    def update(self, num):
        """
        The function which update the plot for every frame
        :param num: iterations
        :return: plot animation
        """
        self.ax.cla()
        point = self.t.shortest_path
        floor, row, col = point[num]

        self.facecolors[row][col][floor] = '#ff99ff'
        self.fcolors_2 = self.explode(self.facecolors)

        self.voxels = self.ax.voxels(self.x, self.y, self.z, self.filled_2,
                       facecolors=self.fcolors_2, edgecolors=self.ecolors_2)
        if [floor, row, col] == self.t.DESTINATION:
            self.facecolors[row][col][floor] = '#ff99ff4D'
        elif [row, col] != ElevatorConst.SHAFT_3D:
            self.facecolors[row][col][floor] = '#1f77b430'
        else:
            self.facecolors[row][col][floor] = '#ff000026'

    def shrink_gaps(self):
        """
        The function that removing gaps between voxels on a plot
        :return:
        """
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
        """
        The function that makes all voxels visible and rendered
        :param data: voxels to be operated
        :return: new voxels
        """
        size = np.array(data.shape) * 2
        data_e = np.zeros(size - 1, dtype=data.dtype)
        data_e[::2, ::2, ::2] = data
        return data_e

    def draw_plot(self):
        """
        The function that drawing the plot
        :return: plot
        """
        self.fig.canvas.set_window_title('Multi-car elevator control in three planes')
        self.ax = self.fig.gca(projection='3d')
        self.voxels = self.ax.voxels(self.x, self.y, self.z, self.filled_2,
                       facecolors=self.fcolors_2, edgecolors=self.ecolors_2)
        plt.show()
