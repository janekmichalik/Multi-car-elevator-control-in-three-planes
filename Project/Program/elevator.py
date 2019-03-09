import random
import collections

from Program.constant import ElevatorConst
from Program.floor import Floor


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

        while self.floor[self.source_x][self.source_y] == ElevatorConst.WALL:
            self.source_x = random.randint(0, 10)
            self.source_y = random.randint(0, 10)
        self.source = [self.source_x, self.source_y]
        self.floor[self.source_x, self.source_y] = ElevatorConst.SOURCE

    def generate_ending_point(self):
        """
        The function that generate the ending point (destination) randomly.
        :return: destination
        """

        while self.floor[self.dest_x][self.dest_y] == ElevatorConst.WALL \
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
                if 0 <= x2 < self.floor_rows and 0 <= y2 < self.floor_cols \
                        and self.floor[y2][x2] != ElevatorConst.WALL and (x2, y2) not in seen:
                    queue.append(self.shortest_path + [(x2, y2)])
                    seen.append((x2, y2))
