import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from constant import ElevatorConst
from simulation import Simulation
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
        lenght_1 = len(self.elevators[0].shortest_path)
        lenght_2 = len(self.elevators[1].shortest_path)
        self.ani = animation.FuncAnimation(self.fig, self.update, lenght_1, interval=650, blit=False, repeat=True)
        self.ani1 = animation.FuncAnimation(self.fig, self.update_2nd, lenght_2, interval=650, blit=False, repeat=True)
        self.draw_plot()

    def logs(self):
        """
        The functions that returns logs.
        :return: logs
        """
        for elev in self.elevators:
            print(f"Winda nr: {elev.id}")
            print(f"Destination: ({elev.DESTINATION})")
            print(f"Source: ({elev.SOURCE})")

            path = elev.shortest_path
            print(f"Dlugosc sciezki: {len(path)}")
            print(f"Sciezka: {path}")
            if list(path[-1]) == elev.DESTINATION:
                print("Destination succeeded")
            if path[0] == elev.SOURCE:
                print("Source succeeded\n")

    def update(self, num):
        """
        The function which update the plot for every frame
        :param num: iterations
        :return: plot animation
        """
        self.ax.cla()
        elev = self.elevators[0]
        point = elev.shortest_path
        floor, row, col = point[num]

        self.facecolors[row][col][floor] = '#ff99ff'
        self.fcolors_2 = self.explode(self.facecolors)

        self.voxels = self.ax.voxels(self.x, self.y, self.z, self.filled_2,
                                     facecolors=self.fcolors_2, edgecolors=self.ecolors_2)
        if [floor, row, col] == elev.DESTINATION:
            self.facecolors[row][col][floor] = '#ff99ff4D'
        elif [row, col] != ElevatorConst.SHAFT_DESC and [row, col] != ElevatorConst.SHAFT_ASC:
            self.facecolors[row][col][floor] = '#1f77b430'
        else:
            if [row, col] == ElevatorConst.SHAFT_DESC:
                color = '#00140d33'
                self.facecolors[row][col][floor] = color
            else:
                color = '#ffffff33'
                self.facecolors[row][col][floor] = color

    def update_2nd(self, num):
        """
        The function which update the plot for every frame
        :param num: iterations
        :return: plot animation
        """
        self.ax.cla()
        elev = self.elevators[1]
        point = elev.shortest_path
        floor, row, col = point[num]

        self.facecolors[row][col][floor] = '#49fdb8'
        self.fcolors_2 = self.explode(self.facecolors)

        self.voxels = self.ax.voxels(self.x, self.y, self.z, self.filled_2,
                                     facecolors=self.fcolors_2, edgecolors=self.ecolors_2)
        if [floor, row, col] == elev.DESTINATION:
            self.facecolors[row][col][floor] = '#49fdb84D'
        elif [row, col] != ElevatorConst.SHAFT_DESC and [row, col] != ElevatorConst.SHAFT_ASC:
            self.facecolors[row][col][floor] = '#1f77b430'
        else:
            if [row, col] == ElevatorConst.SHAFT_DESC:
                color = '#00140d33'
                self.facecolors[row][col][floor] = color
            else:
                color = '#ffffff33'
                self.facecolors[row][col][floor] = color

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
