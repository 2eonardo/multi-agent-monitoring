# constants.py

# Number of iteration
NUM_ITERATIONS = 100
ITERATIONS_STEP = NUM_ITERATIONS//10
NUM_SAMPLES = 30

# map parameters
DECAY_RATE = 0.95
NUM_SEA_CELLS = 39330

# agent parameters
# Suppose the agent dimension negligible respect to the cell
NUM_AGENTS = 10
SENSOR_RANGE = 8 # Euclidean distance from the center of a cell to another
# speed of the agent in m/s
v_agent = 2
# pixel_dimension = 10m x 10m
pixel_dimension = 10
# Single step duration t in sec
TIMESTEP = 60
MAX_DISPLACEMENT = (v_agent*TIMESTEP) // pixel_dimension #range of max step

# Start position of the agents (row, col)
START_ROW = 100
START_COL = 150

# Random start position of the agents (row, col)
RANDOM_SPAWN = False
SPAWN_RADIUS = 20 # Set to 391 minimum to cover all map