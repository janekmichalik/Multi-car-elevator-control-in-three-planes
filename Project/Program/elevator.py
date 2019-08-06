import random
import collections
import numpy as np

from constant import ElevatorConst
from floor import Floor


class Elevator(Floor):

    def __init__(self, id):

        super().__init__()
        self.id = id

        self.source_x = 0
        self.source_y = 0
        self.source_flr = 0
        self.source = [self.source_x, self.source_y]

        self.shortest_path = []

        self.dest_x = 0
        self.dest_y = 0
        self.destination_flr = 0
        self.destination = [self.dest_x, self.dest_y]

        self.generate_starting_floor()
        self.generate_ending_floor()
        self.generate_starting_point()
        self.generate_ending_point()
        self.get_virtual_channel()

        self.SOURCE = [self.source_flr, self.source_x, self.source_y]
        self.DESTINATION = [self.destination_flr, self.dest_x, self.dest_y]

        self.get_path()

    def get_virtual_channel(self):
        if self.source_flr > self.destination_flr:
            self.virtual_channel = -1
        elif self.source_flr < self.destination_flr:
            self.virtual_channel = 1
        else:
            self.virtual_channel = 1

    def get_path_between_flrs(self):
        """
        The function that fulfill the shortest path with 3d coordinates on different floors
        :return: shortest pasth
        """
        absolut = np.abs(self.SOURCE[0] - self.DESTINATION[0])
        if absolut >= 1:
            final_path = []
            if self.SOURCE[0] > self.DESTINATION[0]:
                if absolut == 2 and self.SOURCE[0] != 2:
                    rng = [self.DESTINATION[0] + 1, absolut + 2]
                else:
                    rng = [self.DESTINATION[0] + 1, absolut + 1]
            else:
                if absolut == 2 and self.SOURCE[0] != 0:
                    rng = [self.SOURCE[0] + 1, absolut + 2]
                else:
                    rng = [self.SOURCE[0] + 1, absolut + 1]

            for flr in range(rng[0], rng[1]):
                _, y, z = self.path[-1]
                common_path = [flr, y, z]
                final_path.append(common_path)

            if self.SOURCE[0] > self.DESTINATION[0]:
                final_path.reverse()
            self.shortest_path.extend(final_path)

    def get_path(self):
        """
        The function that call 'compute_shortest_path' depending on source and destination floor
        :return: shortest path
        """

        if self.source_flr == self.destination_flr:
            self.shortest_path = self.compute_shortest_path(self.SOURCE, self.floors)
        else:
            if self.virtual_channel == 1:
                destination = ElevatorConst.SHAFT_A
            else:
                destination = ElevatorConst.SHAFT_D
            self.path = self.compute_shortest_path(self.SOURCE, self.floors, destination=destination)

            self.shortest_path.extend(self.path)
            source = [self.DESTINATION[0], self.path[-1][1], self.path[-1][2]]
            self.extend_path = self.compute_shortest_path(source, self.floors)
            self.get_path_between_flrs()
            self.shortest_path.extend(self.extend_path)
            self.list_remove_duplicates()

    def list_remove_duplicates(self):
        """
        The function that removes duplicates from shortest path
        :return: shortest path
        """
        tmp = []
        for elem in self.shortest_path:
            if list(elem) not in tmp:
                tmp.append(list(elem))
        self.shortest_path = tmp

    def generate_starting_floor(self):
        """
        The function that generates the starting floor (source) randomly.
        :return: source floor
        """

        if self.id == 0:
            self.source_flr = 0
        else:
            self.source_flr = 4

        # zostanie zmienione po dodaniu kolejnej windy
        # self.source_flr = random.randint(0, ElevatorConst.NUM_OF_FLOORS - 1)

    def generate_ending_floor(self):
        """
        The function that generates the ending floor (destination) randomly.
        :return: destination floor
        """

        if self.id == 0:
            self.destination_flr = 0
        else:
            self.destination_flr = 3

        # zostanie zmienione po dodaniu kolejnej windy
        # self.destination_flr = random.randint(0, ElevatorConst.NUM_OF_FLOORS - 1)

    def generate_starting_point(self):
        """
        The function that generates the starting point (source) randomly.
        :return: source
        """

        self.source_x = random.randint(0, ElevatorConst.NUM_OF_FLOORS_HORIZONTAL - 1)
        self.source_y = random.randint(0, ElevatorConst.NUM_OF_FLOORS_VERTICAL - 1)

        while self.floor[self.source_x][self.source_y] == ElevatorConst.WALL\
                or self.floor[self.source_x][self.source_y] == ElevatorConst.SHAFT_D \
                or self.floor[self.source_x][self.source_y] == ElevatorConst.SHAFT_A:
            self.source_x = random.randint(0, ElevatorConst.NUM_OF_FLOORS_HORIZONTAL-1)
            self.source_y = random.randint(0, ElevatorConst.NUM_OF_FLOORS_VERTICAL-1)
        self.source = [self.source_x, self.source_y]
        self.floors[self.source_flr][self.source_x][self.source_y] = ElevatorConst.SOURCE

    def generate_ending_point(self):
        """
        The function that generate the ending point (destination) randomly.
        :return: destination
        """

        self.dest_x = random.randint(0, ElevatorConst.NUM_OF_FLOORS_HORIZONTAL - 1)
        self.dest_y = random.randint(0, ElevatorConst.NUM_OF_FLOORS_VERTICAL - 1)

        while self.floor[self.dest_x][self.dest_y] == ElevatorConst.WALL \
                or (self.source_x == self.dest_x or self.source_y == self.dest_y) \
                or self.floor[self.dest_x][self.dest_y] == ElevatorConst.SHAFT_D \
                or self.floor[self.dest_x][self.dest_y] == ElevatorConst.SHAFT_A:
            self.dest_x = random.randint(0, ElevatorConst.NUM_OF_FLOORS_HORIZONTAL-1)
            self.dest_y = random.randint(0, ElevatorConst.NUM_OF_FLOORS_VERTICAL-1)
        self.destination = [self.dest_x, self.dest_y]
        self.floors[self.destination_flr][self.dest_x][self.dest_y] = ElevatorConst.DESTINATION

    @staticmethod
    def compute_shortest_path(source, floors, destination=ElevatorConst.DESTINATION):
        """
        The function that compute the shortest path from source to destination.
        :return: shortest_path
        """

        flr, x, y = source
        tmp = [flr, x, y]
        queue = collections.deque([[tmp]])
        floor = floors[flr]
        seen = []
        seen.append(source)
        while queue:
            shortest_path = queue.popleft()
            _, x, y = shortest_path[-1]

            if floor[x][y] == destination:
                return shortest_path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < ElevatorConst.NUM_OF_FLOORS_VERTICAL and 0 <= y2 < ElevatorConst.NUM_OF_FLOORS_HORIZONTAL \
                        and floor[y2][x2] != ElevatorConst.WALL and [x2, y2] not in seen:
                    queue.append(shortest_path + [[flr, x2, y2]])
                    seen.append([x2, y2])
