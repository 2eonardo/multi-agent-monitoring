class Agent:
    def __init__(self, start_row: int, start_col: int, map_reference, sensor_range: int = 1):
        # Start position must be in the sea
        if not map_reference.is_sea(start_row, start_col):
            raise ValueError(
                f"Initialization error: The robot cannot be positioned on the land or outside the map. "
            )

        self.row = start_row
        self.col = start_col
        self.map = map_reference
        self.sensor_range = sensor_range

        # Add agent on the map
        self.map.cell_view(self.row, self.col, self.sensor_range)