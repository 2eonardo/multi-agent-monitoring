import numpy as np
import costants as c
from core.bresenham_utilities import get_visible_cells

class Map:
    def __init__(self, filename=c.FILE_NAME):
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

    def query_theoretical_coverage(self, radius, row, col):
        visible_cells = get_visible_cells(row, col, radius, self)

        # Calculate the increment in coverage value
        increment = 0.0
        for r, c in visible_cells:
            increment += (1.0 - self.grid[r, c])

        # Return theorical coverage
        return self.coverage_value + increment

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
    def cell_view(self, row, col, radius):
        if radius == 0:
            if self.is_sea(row, col):
                self.grid[row, col] = 1.0
                self.update_coverage_value()
                return True
            return False

        cell_viewed = get_visible_cells(row, col, radius, self)
        any_cell_updated = False
        for r, c in cell_viewed:
            self.grid[r, c] = 1.0
            any_cell_updated = True

        if any_cell_updated:
            self.update_coverage_value()
        return any_cell_updated

    # decay function
    def decay(self, decay_rate):
        self.grid[self.sea_mask] = np.clip(self.grid[self.sea_mask] * decay_rate, 0, 1.0)
        self.update_coverage_value()