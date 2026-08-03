import pickle
import sys
from map import Map
from agent import Agent
import costants as c
import os
import numpy as np
from spawn_utilities import random_spawn

def main():
    coverage_histories = []
    percent_histories = []
    final_grids = []

    trajectory_run_0 = None
    coverage_history_run_0 = None

    for run in range(1, c.NUM_RUNS+1):
        print(f"Processing Run: {run}/{c.NUM_RUNS}...")

        #Load map
        try:
            m = Map("sea_land_mask_10m_Cecina.npz")
        except FileNotFoundError:
            print("Error: Map file not found.")
            sys.exit()

        if c.RANDOM_SPAWN:
            try:
                spawn_positions = random_spawn(c.START_ROW, c.START_COL, c.SPAWN_RADIUS, c.NUM_AGENTS, m)
            except ValueError as e:
                print(f"Spawn error: {e}")
                sys.exit()
        else:
            spawn_positions = [(c.START_ROW, c.START_COL)] * c.NUM_AGENTS

        #Load agents
        fleet= []
        for i in range(c.NUM_AGENTS):
            try:
                start_r, start_c = spawn_positions[i]
                new_agent = Agent(
                    start_row=start_r,
                    start_col=start_c,
                    map_reference=m,
                    sensor_range=c.SENSOR_RANGE)
                fleet.append(new_agent)
            except ValueError as e:
                print(f"Detail: {e}")
                sys.exit()

        m.update_coverage_value()

        coverage_history = [m.coverage_value]
        coverage_percent_history = [(m.coverage_value/c.NUM_SEA_CELLS)*100]

        # Sequence of agents position
        trajectory = [{"positions": [(a.col, a.row) for a in fleet]}]

        for t in range(1, c.NUM_ITERATIONS+1):
            m.decay(c.DECAY_RATE)
            m.update_coverage_value()
            # Simultaneous simulation
            for agent in fleet:
                agent.update_position(c.NUM_SAMPLES, fleet)
            # next_position = []
            # for agent in fleet:
            #     row, col = agent.find_next_position(c.NUM_SAMPLES, fleet)
            #     next_position.append((row, col))
            # for i, agent in enumerate(fleet):
            #     row, col = next_position[i]
            #     agent.update_position(row, col)

            coverage_history.append(m.coverage_value)
            coverage_percent_history.append((m.coverage_value/c.NUM_SEA_CELLS)*100)
            # State for each t
            trajectory.append({"positions": [(a.col, a.row) for a in fleet]})

        coverage_histories.append(coverage_history)
        percent_histories.append(coverage_percent_history)
        final_grids.append(m.grid)

        if run == 1:
            trajectory_run_0 = trajectory
            coverage_history_run_0 = coverage_history

        print(f"Coverage value: {m.coverage_value} Coverage percent: {(m.coverage_value / c.NUM_SEA_CELLS) * 100:.2f}%")

    average_coverage = np.mean(coverage_histories, axis=0)
    average_percent = np.mean(percent_histories, axis=0)
    average_final_grid = np.mean(final_grids, axis=0)

    # Storage simulation data
    first_run_trajectory_data = {
        "map_file_name": "sea_land_mask_10m_Cecina.npz",
        "sensor_range": c.SENSOR_RANGE,
        "decay_rate": c.DECAY_RATE,
        "trajectory": trajectory_run_0,
        "coverage_history": coverage_history_run_0
    }

    media_data = {
        "map_file_name": "sea_land_mask_10m_Cecina.npz",
        "coverage_history": list(average_coverage),
        "coverage_percent_history": list(average_percent),
        "final_grid": average_final_grid,
        "sea_mask": m.sea_mask
    }

    print("\nSimulation completed.")

    # Save data file
    file_name_first_run = "results/first_run_trajectory_data"
    file_name_media = "results/media_data"
    try:
        os.makedirs("results", exist_ok=True)
        with open(file_name_first_run, "wb") as f:
            pickle.dump(first_run_trajectory_data, f)
        with open(file_name_media, "wb") as f:
            pickle.dump(media_data, f)
        print(f"Simulation Log saved in'{file_name_media}' and '{file_name_first_run}'.")
    except Exception as e:
        print(f"Error during Log saving: {e}")

if __name__ == "__main__":
    main()