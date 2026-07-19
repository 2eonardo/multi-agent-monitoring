import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from environment import Map

try:
    import imageio.v2 as imageio
except ImportError:
    imageio = None


def generate_video_from_log(log_data, video_name="simulation_video.mp4", fps=15, iteration_step=1,
                            output_dir="frames"):
    """
    Read log file and make:
    1. A mp4 video file.
    2. Save some key frames.
    """
    # Create frames repository if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Init video writer (requires: pip install imageio[ffmpeg])
    if imageio is None:
        print("\n[Warning] Library 'imageio' is not installed.")
        print("Cannot produce video. Only static PNG frames will be saved; imageio[ffmpeg] is required for video generation.")
        writer = None
    else:
        print(f"\n Video generation '{video_name}'...")
        try:
            writer = imageio.get_writer(video_name, format='FFMPEG', mode='I', fps=fps, macro_block_size=None)
        except Exception as e:
            print(f"[Warning] Error starting writer: {e}")
            print("Cannot produce video. Only static PNG frames will be saved; imageio[ffmpeg] is required for video generation.")
            writer = None

    # Parameters extraction from log
    map_file_name = log_data["map_file_name"]
    sensor_range = log_data["sensor_range"]
    decay_rate = log_data["decay_rate"]

    # Load the map to perform the calculations
    m = Map(map_file_name)

    # Init agent trajectory tracking
    num_agents = len(log_data["trajectory"][0]["positions"])
    path_histories = [[] for _ in range(num_agents)]

    # Time cycle reconstruction and drawing of all frames
    for t, step_data in enumerate(log_data["trajectory"]):
        # Save position istant t
        positions = step_data["positions"]

        # Grid reconstruction
        # Apply decay and update the map with the position of this step
        if t > 0:
            m.decay(decay_rate)
        for p in positions:
            m.cell_view(p[1], p[0], sensor_range)

        # Creation of img
        fig, ax = plt.subplots(figsize=(12.5, 9))

        display_img = np.zeros((*m.shape, 3))
        display_img[m.land_mask] = [0.22, 0.32, 0.22]  # Land (green)
        display_img[m.sea_mask] = [0.06, 0.08, 0.15]  # Sea (navy)
        ax.imshow(display_img, origin='upper')
        # Disable map modification when the agent is near the boundary
        ax.set_xlim(0, m.shape[1])
        ax.set_ylim(m.shape[0], 0)

        # Coveerage grid
        # Exclude not viewed cell (coverage value < 1%), color: navy, and land cell, color : green
        masked_grid = np.ma.masked_where((~m.sea_mask) | (m.grid < 0.01), m.grid)
        #Print sea area visited
        im = ax.imshow(masked_grid, origin='upper', cmap='viridis', vmin=0.0, vmax=1.0)

        # Color bar
        cbar = fig.colorbar(im, ax=ax, orientation='vertical', pad=0.03, shrink=0.75)
        cbar.set_label('Cell coverage value', fontsize=11, labelpad=10)
        cbar.ax.tick_params(labelsize=9)

        # Trajectory tracking on the map
        for idx, p in enumerate(positions):
            if not path_histories[idx] or path_histories[idx][-1] != p:
                path_histories[idx].append(p)

            if len(path_histories[idx]) > 1:
                path_x, path_y = zip(*path_histories[idx])
                ax.plot(path_x, path_y, color='cyan', linestyle=':', linewidth=1.5, alpha=0.5, zorder=3)

        # Print agents position and sensor range
        for idx, p in enumerate(positions):
            agent_x, agent_y = p

            # Sensor ring
            circle = patches.Circle(
                (agent_x, agent_y),
                radius=sensor_range,
                facecolor='cyan',
                edgecolor='cyan',
                fill=True,
                alpha=0.15,
                linewidth=1.2,
                zorder=4
            )
            ax.add_patch(circle)

            # Agent icon
            label_agent = 'Agent' if idx == 0 else ""
            ax.scatter(
                agent_x, agent_y,
                marker='^',
                color='red',
                s=25,
                edgecolor='black',
                linewidth=0.5,
                zorder=5,
                label=label_agent
            )

        # Calculation control of map coverage value
        recalculated_coverage = m.update_coverage_value()
        original_coverage = log_data["coverage_history"][t]

        # Tolerance for float values
        is_correct = abs(recalculated_coverage - original_coverage) < 0.1

        if not is_correct:
            raise ValueError(
                f"\n[Serious error] differences observed in the map coverage value  t = {t}!\n"
                f" - recalculated value: {recalculated_coverage:.4f}\n"
                f" - original value: {original_coverage:.4f}\n"
                f"Verify the parameters"
            )

        ax.set_title(f"Multi-Agent Exploration System - Time Istant t = {t}", fontsize=14, fontweight='bold',
                     pad=15)
        ax.set_xlabel("Coordinate X [Cell / px]", fontsize=11, labelpad=8)
        ax.set_ylabel("Coordinate Y [Cell / px]", fontsize=11, labelpad=8)
        ax.grid(True, which='both', color='gray', linestyle='--', alpha=0.25, zorder=1)
        ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)

        # Frame generation
        if writer is not None:
            fig.canvas.draw()
            try:
                rgba_buffer = fig.canvas.buffer_rgba()
                frame_rgb = np.asarray(rgba_buffer)[:, :, :3]
            except AttributeError:
                width, height = fig.canvas.get_width_height()
                frame_rgb = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
                frame_rgb = frame_rgb.reshape((int(height), int(width), 3))

            writer.append_data(frame_rgb)

        # Frame saving
        if t % iteration_step == 0:
            save_path = os.path.join(output_dir, f"frame_{t:04d}.png")
            plt.savefig(save_path, bbox_inches='tight', dpi=150)

        plt.close(fig)

    # Secure Writer shutdown
    if writer is not None:
        writer.close()
        print(f"MP4 video successfully generated: '{video_name}'")