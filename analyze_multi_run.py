import os
import pickle
import numpy as np
from visualization.compare_runs import plot_multiple_curves, plot_discrete_trend


# Load data and calculation
def load_and_calculate_data(file_path):
    if not os.path.exists(file_path):
        print(f"  [Skip] File not yet generate: '{file_path}'")
        return None

    with open(file_path, "rb") as f:
        graph_data = pickle.load(f)

    num_sea_cells = graph_data["num_sea_cells"]
    raw_runs = graph_data["coverage_history"]

    # Mean
    raw_mean = np.mean(raw_runs, axis=0)
    # Percentage
    return (raw_mean / num_sea_cells) * 100

def main():
    directory = "spawn_radius"
    test_tag = "Spawn radius"
    time = True
    simulation_time = 60

    # Data for the multi-curve graph
    curves_input = {
        f"20 {test_tag}": "results/data/media_data",
        f"100 {test_tag}": "results_spawn_radius_100/data/media_data"
    }

    # Data for discrete graph
    discrete_input = {
    }

    if curves_input:
        print(f"\n Elaboration curves for {test_tag}...")
        plots_dict = {}

        for label, file_path in curves_input.items():
            coverage_history = load_and_calculate_data(file_path)
            if coverage_history is not None:
                plots_dict[label] = coverage_history

        if plots_dict:
            plot_multiple_curves(curves_dict=plots_dict,
                                 xlabel="Time",
                                 ylabel="Coverage (%)",
                                 save_path=f"plots_multi_run/{directory}/compare.png",
                                 time=time,
                                 time_minutes=simulation_time)


    if discrete_input:
        print(f"\n Elaboration data for {test_tag}...")
        data_dict = {}

        for x_value, file_path in discrete_input.items():
            coverage_history = load_and_calculate_data(file_path)
            if coverage_history is not None:
                final_value = float(coverage_history[-1])
                data_dict[x_value] = final_value

        if data_dict:
            plot_discrete_trend(data_dict=data_dict,
                                xlabel=f"Number of {test_tag}",
                                ylabel="Coverage (%)",
                                save_path=f"plots_multi_run/{directory}/trend.png")

    print("\nAll simulation results have been successfully generated!")

if __name__ == "__main__":
    main()