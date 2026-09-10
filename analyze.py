# analyze.py
import sys
import pickle

import numpy as np

from visualization import plots as p, renderer as r
import costants as c


def main():
    test_tag = f"_num_agents_{c.NUM_AGENTS}"
    repository = f"results{test_tag}"
    file_media = f"{repository}/data/media_data"
    file_first_run = f"{repository}/data/first_run_trajectory_data"

    # Load graph data
    try:
        with open(file_media, "rb") as f:
            graph_data = pickle.load(f)
        num_sea_cells = graph_data["num_sea_cells"]
        raw_runs = graph_data["coverage_history"]
        grids_history = graph_data["grids_history"]
        sea_mask = graph_data["sea_mask"]
        print(f"Graph data successfully loaded from '{file_media}'.")
    except FileNotFoundError:
        print(f"Error: the file '{file_media}' does not exist.")
        print("Make sure to run 'main.py' first to generate the numeric data!")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while reading the graph file: {e}")
        sys.exit(1)

    # Load video data
    try:
        with open(file_first_run, "rb") as f:
            video_data = pickle.load(f)
        print(f"Video data successfully loaded from '{file_first_run}'.")
    except FileNotFoundError:
        print(f"Error: the file '{file_first_run}' does not exist.")
        print("Make sure to run 'main.py' first to generate the video data!")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while reading the video file: {e}")
        sys.exit(1)

    # Calculate data
    raw_mean = np.mean(raw_runs, axis=0)
    raw_std = np.std(raw_runs, axis=0)

    coverage_history = list(raw_mean)
    coverage_percent_history = list((raw_mean / num_sea_cells) * 100)
    std_percent_coverage = list((raw_std / num_sea_cells) * 100)

    # Generation of tables and plots
    print("\n[Phase 1] Generating tables and trend plots...")
    p.save_coverage_table(coverage_history, coverage_percent_history, std_percent_coverage, c.ITERATIONS_STEP, f"{repository}/plots/coverage_table.png")
    p.save_coverage_plot(coverage_percent_history, c.ITERATIONS_STEP, f"{repository}/plots/coverage_plot.png")
    for i in range(1, len(grids_history)):
        step = i*c.ITERATIONS_STEP
        path = f"{repository}/plots/histograms/coverage_histogram_{step}.png"
        p.save_coverage_histogram(grids_history[i], sea_mask, path)

    # Generation video and frame
    print("\n[Phase 2] Starting rendering...")

    try:
        r.generate_video_from_log(video_data, video_path=f"{repository}/video/simulation_video.mp4", fps=24,
                                  iteration_step=c.ITERATIONS_STEP, frames_path=f"{repository}/video/frames")
    except ValueError as e:
        print(f"\n[CRITICAL ERROR] {e}")
        sys.exit(1)

    print("\nAll simulation results have been successfully generated!")


if __name__ == "__main__":
    main()