import pickle
import sys
from environment import Map
from agent import Agent
import costants as c
import plots as p
import renderer as r

def main():
    #Load map
    try:
        m = Map("sea_land_mask_10m_Cecina.npz")
        print("Map successfully loaded")
    except FileNotFoundError:
        print("Error: Map file not found.")
        sys.exit()

    #Load agents
    fleet= []
    for i in range(c.NUM_AGENTS):
        try:
            new_agent =Agent(
                start_row=c.START_ROW,
                start_col=c.START_COL,
                map_reference=m,
                sensor_range=c.SENSOR_RANGE,
                max_displacement=c.MAX_DISPLACEMENT
            )
            fleet.append(new_agent)
        except ValueError as e:
            print(f"Detail: {e}")
            sys.exit()
    print(f"{len(fleet)} Agents successfully loaded")

    print("Starting simulation...")
    m.update_coverage_value()

    coverage_history = [m.coverage_value]

    # Sequence of agents position
    trajectory = [{"positions": [(a.col, a.row) for a in fleet]}]

    print("Iteration: ", 0)
    print(f"Coverage value 0: {m.coverage_value}")

    for t in range(1, c.NUM_ITERATIONS+1):
        m.decay(c.DECAY_RATE)
        for agent in fleet:
            agent.update_position(c.NUM_SAMPLES, fleet)

        coverage_history.append(m.coverage_value)
        print("Iteration: ", t)
        print(f"Coverage value {t}: {m.coverage_value}")

        # State for each t
        trajectory.append({"positions": [(a.col, a.row) for a in fleet]})

    # Storage simulation data
    log_data = {
        "map_file_name": "sea_land_mask_10m_Cecina.npz",
        "sensor_range": c.SENSOR_RANGE,
        "decay_rate": c.DECAY_RATE,
        "coverage_history": coverage_history,
        "trajectory": trajectory
    }

    print("\nSimulation completed.")

    # Save data file
    file_name_log = "simulation_log.pkl"
    try:
        with open(file_name_log, "wb") as f:
            pickle.dump(log_data, f)
        print(f"Simulation Log saved as '{file_name_log}'.")
    except Exception as e:
        print(f"Error during Log saving: {e}")

if __name__ == "__main__":
    main()