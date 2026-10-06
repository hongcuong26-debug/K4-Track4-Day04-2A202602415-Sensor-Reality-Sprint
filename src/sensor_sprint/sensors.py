"""Synthetic camera and LiDAR measurement models."""
from __future__ import annotations

from collections.abc import Callable
import numpy as np

PositionFn = Callable[[np.ndarray | float], np.ndarray]


def camera_measure(position_fn: PositionFn, t: np.ndarray, sigma: float, rng: np.random.Generator) -> np.ndarray:
    """Measure synthetic camera position at the correct timestamp t."""
    truth = np.asarray(position_fn(t), dtype=float)
    return truth + rng.normal(0.0, sigma, size=truth.shape)


def lidar_measure(position_fn: PositionFn, t: np.ndarray, dt_offset_s: float, sigma: float, rng: np.random.Generator) -> np.ndarray:
    """Measure synthetic LiDAR data stamped at t but sampled from t-dt_offset."""
    source_t = np.maximum(0.0, np.asarray(t, dtype=float) - dt_offset_s)
    truth_old = np.asarray(position_fn(source_t), dtype=float)
    return truth_old + rng.normal(0.0, sigma, size=truth_old.shape)
