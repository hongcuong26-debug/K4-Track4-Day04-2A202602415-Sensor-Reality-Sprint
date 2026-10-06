"""Metrics for the synthetic temporal-offset benchmark."""
from __future__ import annotations

import numpy as np


def mean_position_error(measured: np.ndarray, truth: np.ndarray, valid: np.ndarray | None = None) -> float:
    """Mean Euclidean position error over valid samples."""
    err = np.linalg.norm(np.asarray(measured) - np.asarray(truth), axis=-1)
    if valid is not None:
        err = err[np.asarray(valid, dtype=bool)]
    return float(np.mean(err))


def theory_error(v_rel: float, dt_offset_s: float) -> float:
    """Ideal S1 temporal-offset error v*dt."""
    return float(v_rel * dt_offset_s)


def association_swap_rate(camera: np.ndarray, lidar: np.ndarray) -> float:
    """Nearest-neighbor cross-sensor ID swap rate in percent for shape [T,N,2]."""
    cam = np.asarray(camera)
    lid = np.asarray(lidar)
    swaps = 0
    total = cam.shape[0] * cam.shape[1]
    for k in range(cam.shape[0]):
        distances = np.linalg.norm(lid[k, :, None, :] - cam[k, None, :, :], axis=-1)
        assigned = np.argmin(distances, axis=1)
        swaps += int(np.sum(assigned != np.arange(cam.shape[1])))
    return 100.0 * swaps / total
