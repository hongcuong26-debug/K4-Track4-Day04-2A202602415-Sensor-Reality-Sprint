"""Simple constant-velocity motion compensation."""
from __future__ import annotations

import numpy as np


def compensate_positions(lidar: np.ndarray, sample_period_s: float, assumed_dt_s: float) -> np.ndarray:
    """Extrapolate each LiDAR sample using velocity from the two latest samples."""
    arr = np.asarray(lidar, dtype=float)
    out = arr.copy()
    if len(arr) < 2:
        return out
    velocity = np.zeros_like(arr)
    velocity[1:] = (arr[1:] - arr[:-1]) / sample_period_s
    velocity[0] = velocity[1]
    return arr + velocity * assumed_dt_s
