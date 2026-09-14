import os
import pickle
import sys

import numpy as np
from visualization.compare_runs import plot_multiple_curves, plot_discrete_trend


# Load data and calculation
def calculate_data(raw_runs, num_sea_cells):
    # Mean
    raw_mean = np.mean(raw_runs, axis=0)
    # Percentage
    return (raw_mean / num_sea_cells) * 100

def main():
    directory = "no_filter"
    test_tag = "range filter"
    # Data for the multi-curve graph
    curves_input = {
        f"With {test_tag}": "results/data/media_data",
        f"Without {test_tag}": "results_no_filter/data/media_data"
    }

    # Data for discrete graph
    discrete_input = {
    }

    if curves_input:
        print(f"\n Elaboration curves for {test_tag}...")
        plots_dict = {}

        for label, file_path in curves_input.items():
            try:
                with open(file_path, "rb") as f:
                    graph_data = pickle.load(f)
                num_sea_cells = graph_data["num_sea_cells"]
                raw_runs = graph_data["coverage_history"]
                num_iterations = graph_data["num_iterations"]
                dt = graph_data["t"]
                minutes = (num_iterations*dt)/60
                coverage_history = calculate_data(raw_runs, num_sea_cells)
            except FileNotFoundError:
                print(f"Error: the file '{file_path}' does not exist.")
                print("Make sure to run 'main.py' first to generate the numeric data!")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error while reading the graph file: {e}")
                sys.exit(1)
            if coverage_history is not None:
                plots_dict[label] = coverage_history

        if plots_dict:
            plot_multiple_curves(curves_dict=plots_dict, xlabel="Time (min)", ylabel="Coverage (%)",
                                 save_path=f"plots_multi_run/{directory}/compare.png", time_minutes=minutes)


    if discrete_input:
        print(f"\n Elaboration data for {test_tag}...")
        data_dict = {}

        for x_value, file_path in discrete_input.items():
            try:
                with open(file_path, "rb") as f:
                    graph_data = pickle.load(f)
                num_sea_cells = graph_data["num_sea_cells"]
                raw_runs = graph_data["coverage_history"]
                coverage_history = calculate_data(raw_runs, num_sea_cells)
            except FileNotFoundError:
                print(f"Error: the file '{file_path}' does not exist.")
                print("Make sure to run 'main.py' first to generate the numeric data!")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error while reading the graph file: {e}")
                sys.exit(1)
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