from __future__ import annotations

import numpy as np

from sensor_sprint.compensation import compensate_positions
from sensor_sprint.metrics import association_swap_rate, mean_position_error
from sensor_sprint.scenarios import s1_position, s3_positions
from sensor_sprint.sensors import lidar_measure
from sensor_sprint.run_benchmark import evaluation_mask


def test_s1_sigma_zero_matches_vdt() -> None:
    v = 10.0
    dt = 0.15
    t = np.arange(0.0, 10.0, 0.1)
    rng = np.random.default_rng(0)
    fn = lambda x: s1_position(x, v)
    lidar = lidar_measure(fn, t, dt, 0.0, rng)
    truth = fn(t)
    valid = t >= dt
    assert abs(mean_position_error(lidar, truth, valid) - v * dt) < 1e-9


def test_same_seed_same_result() -> None:
    t = np.arange(0.0, 1.0, 0.1)
    fn = lambda x: s1_position(x, 5.0)
    a = lidar_measure(fn, t, 0.1, 0.05, np.random.default_rng(7))
    b = lidar_measure(fn, t, 0.1, 0.05, np.random.default_rng(7))
    assert np.array_equal(a, b)


def test_baseline_noise_nonzero_but_small() -> None:
    t = np.arange(0.0, 10.0, 0.1)
    fn = lambda x: s1_position(x, 10.0)
    lidar = lidar_measure(fn, t, 0.0, 0.05, np.random.default_rng(3))
    truth = fn(t)
    err = mean_position_error(lidar, truth)
    assert err > 0.0
    assert err < 3 * 0.05


def test_s3_zero_offset_large_gap_near_zero_swaps() -> None:
    t = np.arange(0.0, 10.0, 0.1)
    truth = s3_positions(t, 10.0, 8.0)
    assert association_swap_rate(truth, truth) == 0.0


def test_compensation_removes_s1_offset_without_noise() -> None:
    v = 10.0
    dt = 0.15
    period = 0.1
    t = np.arange(0.0, 10.0, period)
    fn = lambda x: s1_position(x, v)
    lidar = lidar_measure(fn, t, dt, 0.0, np.random.default_rng(0))
    corrected = compensate_positions(lidar, period, dt)
    truth = fn(t)
    valid = t >= dt + period
    assert mean_position_error(corrected, truth, valid) < 1e-9


def test_shared_window_excludes_clipped_velocity_for_all_offsets() -> None:
    period = 0.1
    t = np.arange(0.0, 10.0, period)
    offsets = [0, 50, 100, 150, 200]
    cfg = {"simulation": {"offsets_ms": offsets}}
    valid = evaluation_mask(cfg, t, period)
    assert valid.sum() == 97
    fn = lambda x: s1_position(x, 10.0)
    for offset in offsets:
        dt = offset / 1000.0
        lidar = lidar_measure(fn, t, dt, 0.0, np.random.default_rng(0))
        assert abs(mean_position_error(lidar, fn(t), valid) - 10.0 * dt) < 1e-9
        corrected = compensate_positions(lidar, period, dt)
        assert mean_position_error(corrected, fn(t), valid) < 1e-9
