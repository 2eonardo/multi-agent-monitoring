import matplotlib.pyplot as plt
import os

def save_coverage_table(coverage_history, coverage_percent_history, std_percent_coverage, iteration_step, path):
    # Data preparation for the table
    table_data = []

    # Sampling the next iterations
    for i in range(0, len(coverage_history)):
        if i % iteration_step == 0:
            absolute_value = coverage_history[i]
            percentage = coverage_percent_history[i]
            std_percentage = std_percent_coverage[i]

            table_data.append([
                i,
                f"{absolute_value:.2f}",
                f"{percentage:.2f}",
                f"{std_percentage:.2f}"
            ])

    # figure configuration
    # The height adapts dynamically to the number of rows extracted
    fig, ax = plt.subplots(figsize=(6, 1 + len(table_data) * 0.35))
    ax.axis('tight')
    ax.axis('off')

    # Creation of the table
    table = ax.table(
        cellText=table_data,
        colLabels=["Time", "Coverage Value", "Coverage (%)", "Std Dev (%)"],
        colWidths=[0.15, 0.35, 0.25, 0.25],
        loc='center',
        cellLoc='center'
    )

    # table formatting
    table.auto_set_font_size(False) # Disable Matplotlib's automatic font resizing.
    table.set_fontsize(10) # Set fontsize
    table.scale(1.2, 1.4)  # Scaling table

    #Save file
    repository = os.path.dirname(path)
    if repository:
        os.makedirs(repository, exist_ok=True)
    plt.savefig(path, bbox_inches='tight', dpi=300)
    #plt.show()
    plt.close()
    print(f"Table saved in {path}.")

def save_coverage_plot(coverage_history,iteration_step, path):
    # Figure dimension
    fig , ax = plt.subplots(figsize=(10, 6))

    # x-axis assignment
    iterations = list(range(len(coverage_history)))

    # Plotting
    ax.plot(
        iterations,
        coverage_history,
        color='royalblue',
        linewidth=2,
        linestyle='-'
    )

    # axis labels
    ax.set_xlabel('Time', fontsize=12, labelpad=15)
    ax.set_ylabel('Coverage (%)', fontsize=12, labelpad=15)

    # Grid configuration
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xticks(range(0, len(coverage_history), iteration_step))

    # Save plot
    repository = os.path.dirname(path)
    if repository:
        os.makedirs(repository, exist_ok=True)
    plt.savefig(path, bbox_inches='tight', dpi=300)
    #plt.show()
    plt.close()
    print(f"Plot saved in {path}.")

def save_coverage_histogram(map_grid, sea_mask, path):
    sea_values = map_grid[sea_mask]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Intervals definition
    bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # Creation of Histogram
    counts, _ , patches = ax.hist(
        sea_values,
        bins=bins,
        edgecolor='black',
        color='royalblue',
        rwidth=0.8,
        alpha=0.85
    )

    # Cell percentage calculation
    total_cells = len(sea_values)
    percentages = (counts / total_cells) * 100

    labels = [f"{pct:.1f}%" if pct > 0 else "0%" for pct in percentages]
    ax.bar_label(
        patches,
        labels=labels,
        label_type='edge',
        padding=3,
        fontsize=9,
        fontweight='bold'
    )

    # Label
    ax.set_xlabel('Cell Coverage Value', fontsize=12, labelpad=15)
    ax.set_ylabel('Number of Sea Cells', fontsize=12, labelpad=15)

    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    ax.set_xticks(bins)

    ax.set_ylim(0, ax.get_ylim()[1] * 1.1)

    # Save
    repository = os.path.dirname(path)
    if repository:
        os.makedirs(repository, exist_ok=True)
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Histogram saved in {path}.")