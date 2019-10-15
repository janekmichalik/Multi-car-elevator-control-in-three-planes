import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from constant import ElevatorConst, ElevatorColors, PlotConst
from simulation import Simulation
from mpl_toolkits.mplot3d import Axes3D


class Plot(Simulation):

    def __init__(self, logger: bool = True):
        super().__init__()
        self.logger = logger

        self.ax, self.voxels = None, None
        self.fig = plt.figure(figsize=(10, 6))
        self.filled = np.ones(self.building.shape)

        # upscale the above voxel image, leaving gaps
        self.filled_2 = self.explode(self.filled)
        self.fcolors_2 = self.explode(self.facecolors)
        self.ecolors_2 = self.explode(self.edgecolors)

        self.x, self.y, self.z = None, None, None

        self.shrink_gaps()

        # Creating the Animation object
        lenght = self.calculate_anim_steps()
        self.ani = animation.FuncAnimation(self.fig, self.update, lenght,
                                           init_func=self.init, interval=1000, blit=False, repeat=True)
        self.draw_plot()

    def calculate_anim_steps(self):
        tmp = []
        for elev in self.elevators:
            tmp.append(len(elev.final_path))
        lenght = max(tmp)
        return lenght

    def logs(self):
        """
        The functions that returns logs.
        :return: logs
        """
        for elev in self.elevators:
            print(f"Winda nr: {elev.id}")
            print(f"Destination: ({elev.DESTINATION})")
            print(f"Source: ({elev.SOURCE})")
            print(f"finalpath: {elev.final_path}")

            for path in elev.iterration_paths:
                print(f"Dlugosc sciezki: {len(path)}")
                print(f"Sciezka: {path}")

    def init(self):
        for elev in self.elevators:
            floor, row, col = elev.iterration_paths[0][-1]
            # self.facecolors[row][col][floor] = ElevatorColors.DESTINATION[elev.id]

    def update(self, num):
        """
        The function which update the plot for every frame
        :param num: iterations
        :return: plot animation
        """
        def get_next_item():
            try:
                return elev.iterration_paths[(elev.counter + 1)][-1]
            except IndexError:
                return None
        self.ax.cla()
        for elev in self.elevators:
            point = elev.final_path
            if len(self.elevators) is not 1:
                itr = elev.id + 1 if elev.id == 0 else elev.id - 1
            else:
                itr = 0
            if num < len(point):
                floor, row, col = point[num]

                self.facecolors[row][col][floor] = ElevatorColors.ELEVATOR[elev.id]
                self.fcolors_2 = self.explode(self.facecolors)
                self.voxels = self.ax.voxels(self.x, self.y, self.z, self.filled_2,
                                             facecolors=self.fcolors_2, edgecolors=self.ecolors_2)
                pth_list = [floor, row, col]
                # destynacja biezacej windy
                dest = elev.iterration_paths[elev.counter][-1]
                # destynacja nastepnej windy
                new = get_next_item()

                if pth_list == dest and new is not None:
                    z, x, y = new
                    self.facecolors[x][y][z] = ElevatorColors.DESTINATION[elev.id]
                    self.facecolors[row][col][floor] = ElevatorColors.PATH
                    elev.counter = elev.counter + 1
                elif [row, col] != ElevatorConst.SHAFT_DESC and [row, col] != ElevatorConst.SHAFT_ASC:
                    self.facecolors[row][col][floor] = ElevatorColors.PATH
                else:
                    if [row, col] == ElevatorConst.SHAFT_DESC:
                        color = ElevatorColors.SHAFT_DESC
                        self.facecolors[row][col][floor] = color
                    else:
                        color = ElevatorColors.SHAFT_ASC
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
        self.fig.legend(PlotConst.color_list, PlotConst.color_labels)
        plt.show()
        if self.logger:
            self.logs()
