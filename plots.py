import matplotlib.pyplot as plt


def save_coverage_table(coverage_history, iteration_step):
    # Data preparation for the table
    table_data = []

    # Initial state
    table_data.append(["Initial iteration", f"{coverage_history[0]:.4f}"])

    # Sampling the next iterations
    for i in range(1, len(coverage_history)):
        if i % iteration_step == 0:
            table_data.append([f"Iteration {i}", f"{coverage_history[i]:.4f}"])

    # figure configuration
    # The height adapts dynamically to the number of rows extracted
    fig, ax = plt.subplots(figsize=(6, 1 + len(table_data) * 0.35))
    ax.axis('tight')
    ax.axis('off')

    # Creation of the table
    table = ax.table(
        cellText=table_data,
        colLabels=["Iteration", "Coverage Value"],
        loc='center',
        cellLoc='center'
    )

    # table formatting
    table.auto_set_font_size(False) # Disable Matplotlib's automatic font resizing.
    table.set_fontsize(10) # Set fontsize
    table.scale(1.2, 1.4)  # Scaling table

    #Save file
    #plt.savefig("coverage_table.png", bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()
    #print("Table saved 'coverage_table.png'.")