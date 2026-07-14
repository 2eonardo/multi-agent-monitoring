import matplotlib.pyplot as plt


def save_coverage_table(coverage_history, iteration_step = 1, filename= "coverage_table.png"):
    # Data preparation for the table
    table_data = []
    # Initial state
    #table_data.append([0, f"{coverage_history[0]:.4f}"])

    # Sampling the next iterations
    for i in range(0, len(coverage_history)):
        if i % iteration_step == 0:
            table_data.append([i, f"{coverage_history[i]:.4f}"])

    # figure configuration
    # The height adapts dynamically to the number of rows extracted
    fig, ax = plt.subplots(figsize=(6, 1 + len(table_data) * 0.35))
    ax.axis('tight')
    ax.axis('off')

    # Creation of the table
    table = ax.table(
        cellText=table_data,
        colLabels=["Time", "Coverage Value"],
        colWidths=[0.25, 0.55],
        loc='center',
        cellLoc='center'
    )

    # table formatting
    table.auto_set_font_size(False) # Disable Matplotlib's automatic font resizing.
    table.set_fontsize(10) # Set fontsize
    table.scale(1.2, 1.4)  # Scaling table

    #Save file
    #plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()
    print(f"Table saved as {filename}.")

def save_coverage_plot(coverage_history, iteration_step, filename= "coverage_plot.png"):
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
    # plt.savefig("coverage_trend.png", bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()
    print(f"Plot saved as {filename}.")