# bresenham_utils.py
import math


def bresenham_line(r0, c0, r1, c1):
    """
    Classic implementation of Bresenham's algorithm.
    Returns the list of (row, col) coordinates forming
    the discrete line segment between (r0, c0) and (r1, c1).
    """
    points = []
    dr = abs(r1 - r0)
    dc = abs(c1 - c0)
    sr = 1 if r0 < r1 else -1
    sc = 1 if c0 < c1 else -1
    err = dr - dc

    while True:
        points.append((r0, c0))
        if r0 == r1 and c0 == c1:
            break
        e2 = 2 * err
        if e2 > -dc:
            err -= dc
            r0 += sr
        if e2 < dr:
            err += dr
            c0 += sc
    return points


def is_path_free(r0, c0, r1, c1, map_reference):
    """
    Checks if the straight-line path between two points crosses land.
    Returns True if the path is completely clear (sea only), False otherwise.
    """
    path = bresenham_line(r0, c0, r1, c1)
    for r, c in path:
        if not map_reference.is_sea(r, c):
            return False
    return True


def get_visible_cells(r0, c0, radius, map_reference):
    """
    Calculates the set of all sea coordinates visible from the center (r0, c0)
    without being able to see beyond the land cells.
    """
    visible_set = set()

    # Limits to avoid calculating indices outside the map
    min_r = max(0, r0 - radius)
    max_r = min(map_reference.shape[0] - 1, r0 + radius)
    min_c = max(0, c0 - radius)
    max_c = min(map_reference.shape[1] - 1, c0 + radius)

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if math.dist((r0, c0), (r, c)) <= radius:
                line = bresenham_line(r0, c0, r, c)

                for cell_r, cell_c in line:
                    if not map_reference.is_sea(cell_r, cell_c):
                        break
                    visible_set.add((cell_r, cell_c))

    return visible_set