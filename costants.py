# constants.py

# File name for map
FILE_NAME = "sea_land_mask_10m_Cecina.npz"

# Simulation data
NUM_RUNS = 5
NUM_ITERATIONS = 720
ITERATIONS_STEP = NUM_ITERATIONS//10
NUM_SAMPLES = 50

# agent parameters
NUM_AGENTS = 10
SENSOR_RANGE = 8 # Euclidean distance from the center of a cell to another
v_agent = 2 # m/s
pixel_dimension = 10 # 10m x 10m
t = pixel_dimension/v_agent

# map parameters
NUM_SEA_CELLS = 39330
DECAY_RATE_REF = 0.95
LOSS_REF = 1- DECAY_RATE_REF
TIMESTEP = 30 #s
LOSS = LOSS_REF * (t/TIMESTEP)
DECAY_RATE = 1 - LOSS

# Start position of the agents (row, col)
START_ROW = 100
START_COL = 150

# Random start position of the agents (row, col)
RANDOM_SPAWN = True
SPAWN_RADIUS = 20 # Set to 391 minimum to cover all map