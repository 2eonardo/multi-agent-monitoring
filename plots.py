import matplotlib.pyplot as plt
import os
import costants


def save_coverage_table(coverage_history, coverage_percent_history, iteration_step, path):
    # Data preparation for the table
    table_data = []

    # Sampling the next iterations
    for i in range(0, len(coverage_history)):
        if i % iteration_step == 0:
            absolute_value = coverage_history[i]
            percentage = coverage_percent_history[i]

            table_data.append([
                i,
                f"{absolute_value:.4f}",
                f"{percentage:.2f}%"
            ])

    # figure configuration
    # The height adapts dynamically to the number of rows extracted
    fig, ax = plt.subplots(figsize=(6, 1 + len(table_data) * 0.35))
    ax.axis('tight')
    ax.axis('off')

    # Creation of the table
    table = ax.table(
        cellText=table_data,
        colLabels=["Time", "Coverage Value", "Coverage (%)"],
        colWidths=[0.20, 0.40, 0.40],
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

def save_coverage_plot(coverage_history, iteration_step, path="coverage_plot.png"):
    # Figure dimension
    plt.figure(figsize=(10, 6))

    # x-axis assignment
    iterations = list(range(len(coverage_history)))

    # Plotting
    plt.plot(
        iterations,
        coverage_history,
        label='Coverage Value',
        color='royalblue',
        linewidth=2,
        linestyle='-'
    )

    # axis labels
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Coverage value', fontsize=12)

    # Title
    plt.title('Trend of coverage value over time', fontsize=14, pad=15)

    # Grid configuration
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(range(0, len(coverage_history), iteration_step))

    # Legend position
    plt.legend(loc='lower right')

    # Save plot
    repository = os.path.dirname(path)
    if repository:
        os.makedirs(repository, exist_ok=True)
    plt.savefig(path, bbox_inches='tight', dpi=300)
    #plt.show()
    plt.close()
    print(f"Plot saved in {path}.")

def save_coverage_histogram(map_grid, sea_mask, path="results/coverage_histogram.png"):
    sea_values = map_grid[sea_mask]

    plt.figure(figsize=(10, 6))

    # Intervals definition
    bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # Creation of Histogram
    plt.hist(
        sea_values,
        bins=bins,
        edgecolor='black',
        color='royalblue',
        rwidth=0.8,
        alpha=0.85
    )

    # Label
    plt.xlabel('Cell Coverage Value', fontsize=12)
    plt.ylabel('Number of Sea Cells', fontsize=12)
    plt.title('Distribution of Coverage Values on Sea Cells', fontsize=14, pad=15)

    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.xticks(bins)

    # Save
    repository = os.path.dirname(path)
    if repository:
        os.makedirs(repository, exist_ok=True)
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Histogram saved in {path}.")