# analyze.py
import sys
import pickle
from visualization import plots as p, renderer as r
import costants as c


def main():
    file_media = "results/data/media_data"
    file_first_run = "results/data/first_run_trajectory_data"

    # Load graph data
    try:
        with open(file_media, "rb") as f:
            graph_data = pickle.load(f)
        coverage_history = graph_data["coverage_history"]
        coverage_percent_history = graph_data["coverage_percent_history"]
        std_percent_coverage = graph_data["std_percent_coverage"]
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

    # Generation of tables and plots
    print("\n[Phase 1] Generating tables and trend plots...")
    p.save_coverage_table(coverage_history, coverage_percent_history, std_percent_coverage, c.ITERATIONS_STEP, "results/plots/coverage_table.png")
    p.save_coverage_plot(coverage_percent_history, c.ITERATIONS_STEP, "results/plots/coverage_plot.png")
    for i in range(1, len(grids_history)):
        step = i*c.ITERATIONS_STEP
        path = f"results/plots/histograms/coverage_histogram_{step}.png"
        p.save_coverage_histogram(grids_history[i], sea_mask, path)

    # Generation video and frame
    print("\n[Phase 2] Starting rendering...")

    try:
        r.generate_video_from_log(video_data, video_path="results/video/simulation_video.mp4", fps=24,
                                  iteration_step=c.ITERATIONS_STEP, frames_path="results/video/frames")
    except ValueError as e:
        print(f"\n[CRITICAL ERROR] {e}")
        sys.exit(1)

    print("\nAll simulation results have been successfully generated!")


if __name__ == "__main__":
    main()