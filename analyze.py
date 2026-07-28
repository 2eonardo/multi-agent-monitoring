import sys
import pickle
import plots as p
import renderer as r
import costants as c


def main():
    name_log_file = "results/simulation_log.pkl"

    # Load log_data
    try:
        with open(name_log_file, "rb") as f:
            log_data = pickle.load(f)
        print(f"Simulation log successfully loaded from '{name_log_file}'.")
    except FileNotFoundError:
        print(f"Error: the file '{name_log_file}' does not exist.")
        print("Make sure to run 'main.py' first to generate the numeric data!")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while reading the log file: {e}")
        sys.exit(1)

    # Extract coverage history from log_data
    coverage_history = log_data["coverage_history"]

    # Generation of tables and plots
    print("\n[Phase 1] Generating tables and trend plots...")
    p.save_coverage_table(coverage_history, c.ITERATIONS_STEP, "results/coverage_table.png")
    p.save_coverage_plot(coverage_history, c.ITERATIONS_STEP, "results/coverage_plot.png")

    # Generation video and frame
    print("\n[Phase 2] Starting rendering...")

    try:
        r.generate_video_from_log(log_data, video_path="results/simulation_video.mp4", fps=6,
                                  iteration_step=c.ITERATIONS_STEP, frames_path="results/frames")
    except ValueError as e:
        print(f"\n[CRITICAL ERROR] {e}")
        sys.exit(1)

    print("\nAll simulation results have been successfully generated!")


if __name__ == "__main__":
    main()