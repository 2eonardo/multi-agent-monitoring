import numpy as np
from bresenham_utilities import get_visible_cells

class Map:
    def __init__(self, filename="sea_land_mask_10m_Cecina.npz"):
        #Load Map
        data = np.load(filename) # 39.330 Number o sea cells
        #store data
        self.x = data["x"]
        self.y = data["y"]
        self.sea_mask = data["sea_mask"].astype(bool)
        self.land_mask = data["land_mask"].astype(bool)
        #grid of monitoring value
        self.shape = self.land_mask.shape
        self.grid = np.zeros(self.shape)
        #function to be maximized
        self.coverage_value = 0.0

    def theorical_coverage(self, agent, row, col):
        #Define limit of the map
        limit = agent.max_displacement + agent.sensor_range + 1
        r_min = max(0, row - limit)
        r_max = min(self.shape[0], row + limit + 1)
        c_min = max(0, col - limit)
        c_max = min(self.shape[1], col + limit + 1)
        # Copy a matrix of the original grid to restore it later
        subgrid_backup = self.grid[r_min:r_max, c_min:c_max].copy()

        self.cell_view(row, col, agent.sensor_range)
        value = float(np.sum(self.grid[self.sea_mask]))
        #Restore map
        self.grid[r_min:r_max, c_min:c_max] = subgrid_backup
        return value

    # Update the function value based on the current grid state
    def update_coverage_value(self):
        self.coverage_value = float(np.sum(self.grid[self.sea_mask]))
        return self.coverage_value

    # check if cell belongs to the sea
    def is_sea(self, row, col):
        # avoid IndexError
        if 0 <= row < self.shape[0] and 0 <= col < self.shape[1]:
            return self.sea_mask[row, col]
        return False

    # Set cell value to 1 when visited by a robot.
    # Missing algorithm to handle land barriers between sea cells
    def cell_view(self, row, col, radius):
        if radius == 0:
            if self.is_sea(row, col):
                self.grid[row, col] = 1.0
                return True
            return False

        cell_viewed = get_visible_cells(row, col, radius, self)
        any_cell_updated = False
        for r, c in cell_viewed:
            self.grid[r, c] = 1.0
            any_cell_updated = True
        return any_cell_updated

    # decay function
    def decay(self, decay_rate):
        self.grid[self.sea_mask] = np.clip(self.grid[self.sea_mask] * decay_rate, 0, 1.0)