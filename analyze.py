import pickle
import plots as p
import renderer as r
import costants as c


def main():
    nome_file_log = "simulation_log.pkl"

    # Load log_data
    try:
        with open(nome_file_log, "rb") as f:
            log_data = pickle.load(f)
        print(f"Simulation log successfully loaded from '{nome_file_log}'.")
    except FileNotFoundError:
        print(f"Error: the file '{nome_file_log}' does not exist.")
        print("Make sure to run 'main.py' first to generate the numeric data!")
        return
    except Exception as e:
        print(f"Unexpected error while reading the log file: {e}")
        return

    # 
    coverage_history = log_data["coverage_history"]

    # Generation of tables and plots
    print("\n[Phase 1] Generating tables and trend plots...")
    p.save_coverage_table(coverage_history, c.ITERATIONS_STEP)
    p.save_coverage_plot(coverage_history, c.ITERATIONS_STEP)

    # Generation video and frame
    print("\n[Phase 2] Starting rendering...")
    r.generate_video_from_log(
        log_data,
        video_name="simulation_video.mp4",
        fps=8,
        iteration_step=c.ITERATIONS_STEP,
        output_dir="frames"
    )

    print("\nAll simulation results have been successfully generated!")


if __name__ == "__main__":
    main()