import numpy as np

class Map:
    def __init__(self, filename="sea_land_mask_10m_Cecina.npz"):
        #Load Map
        data = np.load(filename)
        #store data
        self.x = data["x"]
        self.y = data["y"]
        self.sea_mask = data["sea_mask"]
        self.land_mask = data["land_mask"]
        #grid of monitoring value
        self.shape = self.land_mask.shape
        self.grid = np.zeros(self.shape)
        #function to be maximized
        self.function_value = 0.0

    def update_function_value(self):
        # Update the function value based on the current grid state
        self.function_value = float(np.sum(self.grid[self.sea_mask]))
        return self.function_value

    # check if cell belongs to the sea
    def is_sea(self, x, y):
        # avoid IndexError
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            return self.sea_mask[x, y]
        return False

    # Set cell value to 1 when visited by a robot.
    def cell_view(self, x, y, radius):
        if radius == 0:
            if self.is_sea(x, y):
                self.grid[x, y] = 1.0
                return True
            return False
        any_cell_updated = False
        for r in range(x -radius,x + radius + 1):
            for c in range(y -radius,y + radius + 1):
                if self.is_sea(r, c):
                    self.grid[r, c] = 1.0
                    any_cell_updated = True
        return any_cell_updated

    # decay function
    def decay(self, decay_rate):
        self.grid[self.sea_mask] = np.clip(self.grid[self.sea_mask] * decay_rate, 0, 1.0)