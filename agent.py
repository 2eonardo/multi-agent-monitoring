import math

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
            #Check if any other agent is closer to the sampled point than self
            for other in other_agents:
                if other is self:
                    continue
                dist_to_other = math.dist((other.row, other.col), (p_row, p_col))

                if dist_to_other <= dist_to_self:
                    is_closest_to_self = False
                    break

            if is_closest_to_self:
                filtered.append((p_row, p_col))

        return filtered

