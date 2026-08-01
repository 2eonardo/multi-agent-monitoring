# spawn_utils.py
import math
import numpy as np


def random_spawn(start_row, start_col, spawn_radius, num_agents, map_reference):
    candidate_points = []

    # Limit of the map
    min_r = max(0, start_row - spawn_radius)
    max_r = min(map_reference.shape[0] - 1, start_row + spawn_radius)
    min_c = max(0, start_col - spawn_radius)
    max_c = min(map_reference.shape[1] - 1, start_col + spawn_radius)

    # Search sea cells
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if math.dist((start_row, start_col), (r, c)) <= spawn_radius:
                if map_reference.is_sea(r, c):
                    candidate_points.append((r, c))

    if len(candidate_points) < num_agents:
        raise ValueError("Insufficient number of sea cells")

    # It is not a normal distribution
    chosen_indices = np.random.choice(len(candidate_points), size=num_agents, replace=False)

    return [candidate_points[idx] for idx in chosen_indices]