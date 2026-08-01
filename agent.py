import math
from bresenham_utilities import is_path_free
import numpy as np


class Agent:
    def __init__(self, start_row: int, start_col: int, map_reference, sensor_range: int = 1, max_displacement: int = 1):
        # Start position must be in the sea
        if not map_reference.is_sea(start_row, start_col):
            raise ValueError(
                f"Initialization error: The robot cannot be positioned on the land or outside the map. "
            )

        self.row = start_row
        self.col = start_col
        self.map = map_reference
        self.sensor_range = sensor_range
        self.max_displacement = max_displacement

        # Add agent on the map
        self.map.cell_view(self.row, self.col, self.sensor_range)

    def get_samples(self, num_samples: int):

        # Sampling based on a normal distribution
        rows = np.random.normal(loc=self.row, scale=self.max_displacement, size=num_samples)
        cols = np.random.normal(loc=self.col, scale=self.max_displacement, size=num_samples)

        # Let's round to the nearest cells
        rows = np.round(rows).astype(int)
        cols = np.round(cols).astype(int)

        samples = set()
        for r, c in zip(rows, cols):
            # 1. Check if the sampled point is in the sea
            if self.map.is_sea(r, c):
                # 2. Check if the sampled point is within the max displacement
                dist = math.dist((self.row, self.col), (r, c))
                if dist <= self.max_displacement:
                    samples.add((r, c))

        return list(samples)

    def filter_samples(self, samples: list, other_agents: list ):
        filtered = []

        for p_row, p_col in samples:
            dist_to_self = math.dist((self.row, self.col), (p_row, p_col))

            is_closest_to_self = True
            # Check if any other agent is closer to the sampled point than self
            for other in other_agents:
                if other is self:
                    continue

                # Allows start from a same position
                if other.row == self.row and other.col == self.col:
                    continue

                dist_to_other = math.dist((other.row, other.col), (p_row, p_col))

                if dist_to_other <= dist_to_self:
                    is_closest_to_self = False
                    break

            if is_closest_to_self:
                # Check that the straight-line trajectory does not hit the land
                if is_path_free(self.row, self.col, p_row, p_col, self.map):
                    filtered.append((p_row, p_col))

        return filtered

    def find_goal_point(self, samples: list):
        g_row = self.row
        g_col = self.col
        value = self.map.coverage_value
        for p_row, p_col in samples:
            coverage  = self.map.theorical_coverage(self, p_row, p_col)
            if coverage > value:
                value = coverage
                g_row, g_col = p_row, p_col

            #Missing operative flow when coverage value are the same
        return g_row, g_col

    def move_to(self, row: int, col: int):
        self.row = row
        self.col = col
        self.map.cell_view(row, col, self.sensor_range)

    def find_next_position(self, num_samples: int, other_agents: list):
        samples = self.get_samples(num_samples)
        samples = self.filter_samples(samples, other_agents)
        row, col = self.find_goal_point(samples)
        return row, col

    def update_position(self, row, col):
        self.move_to(row, col)
        value = self.map.update_coverage_value()
        return value

