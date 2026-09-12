# compare_runs.py
import os
import matplotlib.pyplot as plt
import numpy as np

def plot_multiple_curves(curves_dict, xlabel, ylabel, save_path, time, time_minutes):

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10.colors

    # Create curve
    for idx, (label, y_data) in enumerate(curves_dict.items()):
        color = colors[idx % len(colors)]
        y = np.array(y_data)

        if time:
            x = np.linspace(0, time_minutes, len(y))
        else:
            x = np.arange(len(y))

        ax.plot(x, y, label=label, color=color, linewidth=2)

    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=10)

    dir_name = os.path.dirname(save_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"[Compare graph] Saved in: {save_path}")


def plot_discrete_trend(data_dict, xlabel, ylabel, save_path):

    sorted_items = sorted(data_dict.items(), key=lambda item: item[0])
    x_vals = [item[0] for item in sorted_items]
    y_vals = [item[1] for item in sorted_items]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x_vals, y_vals, color='royalblue', linestyle='--', linewidth=1.8, alpha=0.8)
    ax.scatter(x_vals, y_vals, color='red', s=60, zorder=5, edgecolor='black', label='Coverage Value (%)')

    for x, y in zip(x_vals, y_vals):
        ax.annotate(
            f"{y:.2f}%",
            (x, y),
            textcoords="offset points",
            xytext=(0, 8),
            ha='center',
            fontsize=9,
            fontweight='bold'
        )

    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)
    ax.set_xticks(x_vals)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_ylim(min(y_vals) * 0.9, max(y_vals) * 1.1)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)

    dir_name = os.path.dirname(save_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"[Trend graph] Saved in: {save_path}")