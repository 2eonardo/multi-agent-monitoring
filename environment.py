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

    # check if cell belongs to the sea
    def is_sea(self, x, y):
        # avoid IndexError
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
            return self.sea_mask[x, y]
        return False

    # Set cell value to 1 when visited by a robot.
    def cell_view(self, x, y):
        if self.is_sea(x, y):
            self.grid[x, y] = 1.0
            return True
        return False

    # decay function
    def decay(self, decay_rate):
        self.grid[self.sea_mask] = np.clip(self.grid[self.sea_mask] * decay_rate, 0, 1.0)