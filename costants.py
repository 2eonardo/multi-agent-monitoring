# constants.py

# Number of iteration
NUM_ITERATIONS = 100
ITERATIONS_STEP = NUM_ITERATIONS//10

# map parameters
DECAY_RATE = 0.95

# agent parameters
# Suppose the agent dimension negligible respect to the cell
NUM_AGENTS = 10
SENSOR_RANGE = 8 # Euclidean distance from the center of a cell to another
MAX_DISPLACEMENT = 10 #range of max step
NUM_SAMPLES = 30

# Start position of the agents (row, col)
START_ROW = 100
START_COL = 150

# Random start position of the agents (row, col)
RANDOM_SPAWN = False