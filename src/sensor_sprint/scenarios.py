"""Synthetic ground-truth trajectory generators."""
from __future__ import annotations

import numpy as np


def s1_position(t: np.ndarray | float, v_rel: float, x0: float = 100.0) -> np.ndarray:
    """Constant relative-speed target moving toward ego along +x axis coordinates."""
    tt = np.asarray(t, dtype=float)
    x = x0 - v_rel * tt
    y = np.zeros_like(tt)
    return np.stack([x, y], axis=-1)


def s2_position(t: np.ndarray | float, v_rel: float, accel: float, x0: float = 100.0) -> np.ndarray:
    """Constant-acceleration target relative trajectory in x; accel may be negative."""
    tt = np.asarray(t, dtype=float)
    x = x0 - v_rel * tt - 0.5 * accel * tt**2
    y = np.zeros_like(tt)
    return np.stack([x, y], axis=-1)


def s3_positions(t: np.ndarray | float, v_rel: float, d_gap: float, x0: float = 100.0) -> np.ndarray:
    """Two same-lane targets separated by fixed longitudinal gap."""
    lead = s1_position(t, v_rel=v_rel, x0=x0)
    follow = s1_position(t, v_rel=v_rel, x0=x0 - d_gap)
    return np.stack([lead, follow], axis=-2)
