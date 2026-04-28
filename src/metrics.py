import numpy as np

def calculate_progress(change_map):
    """
    Calculate percentage of changed area
    """

    # Total pixels
    total_pixels = change_map.size

    # Count white pixels (changed)
    changed_pixels = np.count_nonzero(change_map)

    # Percentage
    progress = (changed_pixels / total_pixels) * 100

    return progress