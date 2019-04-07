import random
import collections

from Program.constant import ElevatorConst
from Program.floor import Floor


class Elevator(Floor):

    def __init__(self):

        super().__init__()

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

        self.SOURCE = [self.source_flr, self.source_x, self.source_y]
        self.DESTINATION = [self.destination_flr, self.dest_x, self.dest_y]

        if self.source_flr == self.destination_flr:
            self.shortest_path = self.compute_shortest_path(self.source_flr, self.source, self.floors[self.source_flr])
            pass
        else:
            path_1 = self.compute_shortest_path(self.source_flr, self.source, self.floors[self.source_flr],
                                                destination=ElevatorConst.SHAFT)
            self.floors[self.source_flr][self.source[0]][self.source[1]] = ElevatorConst.PATH
            path_2 = self.compute_shortest_path(self.source_flr, self.source, self.floors[self.source_flr],
                                                destination=ElevatorConst.SHAFT)
            if len(path_1) > len(path_2):
                self.path = path_2
            else:
                self.path = path_1

            self.shortest_path.extend(self.path)
            tmp = self.path[-1]
            tmp1, tmp2 = tmp[1], tmp[2]
            source = [tmp1,tmp2]
            self.extend_path = self.compute_shortest_path(self.destination_flr,
                                                     source,
                                                     self.floors[self.destination_flr])
            self.shortest_path.extend(self.extend_path)


    def generate_starting_floor(self):
        """
        The function that generates the starting floor (source) randomly.
        :return: source floor
        """

        self.source_flr = 4
        # self.source_flr = random.randint(0, ElevatorConst.NUM_OF_FLOORS - 1)

    def generate_ending_floor(self):
        """
        The function that generates the ending floor (destination) randomly.
        :return: destination floor
        """

        self.destination_flr = 4
        # self.destination_flr = random.randint(0, ElevatorConst.NUM_OF_FLOORS - 1)

    def generate_starting_point(self):
        """
        The function that generates the starting point (source) randomly.
        :return: source
        """

        while self.floor[self.source_x][self.source_y] == ElevatorConst.WALL:
            self.source_x = random.randint(0, ElevatorConst.NUM_OF_FLOORS_HORIZONTAL-1)
            self.source_y = random.randint(0, ElevatorConst.NUM_OF_FLOORS_VERTICAL-1)
        self.source = [self.source_x, self.source_y]
        self.floors[self.source_flr][self.source_x][self.source_y] = ElevatorConst.SOURCE

    def generate_ending_point(self):
        """
        The function that generate the ending point (destination) randomly.
        :return: destination
        """

        while self.floor[self.dest_x][self.dest_y] == ElevatorConst.WALL \
                and (self.source_x != self.dest_x or self.source_y != self.dest_y):
            self.dest_x = random.randint(0, ElevatorConst.NUM_OF_FLOORS_HORIZONTAL-1)
            self.dest_y = random.randint(0, ElevatorConst.NUM_OF_FLOORS_VERTICAL-1)
        self.destination = [self.dest_x, self.dest_y]
        self.floors[self.destination_flr][self.dest_x][self.dest_y] = ElevatorConst.DESTINATION

    @staticmethod
    def compute_shortest_path(flr, source, floor, destination=ElevatorConst.DESTINATION):
        """
        The function that compute the shortest path from source to destination.
        :return: shortest_path
        """

        source_x, source_y = source
        tmp = [flr, source_x, source_y]
        queue = collections.deque([[tmp]])
        seen = []
        seen.append(set(source))
        while queue:
            shortest_path = queue.popleft()
            _, x, y = shortest_path[-1]
            if floor[x][y] == destination:
                return shortest_path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < ElevatorConst.NUM_OF_FLOORS_VERTICAL and 0 <= y2 < ElevatorConst.NUM_OF_FLOORS_HORIZONTAL \
                        and floor[y2][x2] != ElevatorConst.WALL and (x2, y2) not in seen:
                    queue.append(shortest_path + [(flr, x2, y2)])
                    seen.append((x2, y2))
