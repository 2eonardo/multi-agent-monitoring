# analyze.py
import sys
import pickle
import plots as p
import renderer as r
import costants as c


def main():
    file_media = "results/media_data"
    file_first_run = "results/first_run_trajectory_data"

    # Load graph data
    try:
        with open(file_media, "rb") as f:
            graph_data = pickle.load(f)
        coverage_history = graph_data["coverage_history"]
        coverage_percent_history = graph_data["coverage_percent_history"]
        final_grid = graph_data["final_grid"]
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
    p.save_coverage_table(coverage_history, coverage_percent_history, c.ITERATIONS_STEP, "results/coverage_table.png")
    p.save_coverage_plot(coverage_history, c.ITERATIONS_STEP, "results/coverage_plot.png")
    p.save_coverage_histogram(final_grid, sea_mask, "results/final_coverage_histogram.png")

    # Generation video and frame
    print("\n[Phase 2] Starting rendering...")

    try:
        r.generate_video_from_log(video_data, video_path="results/simulation_video.mp4", fps=6,
                                  iteration_step=c.ITERATIONS_STEP, frames_path="results/frames")
    except ValueError as e:
        print(f"\n[CRITICAL ERROR] {e}")
        sys.exit(1)

    print("\nAll simulation results have been successfully generated!")


if __name__ == "__main__":
    main()