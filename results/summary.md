# Synthetic benchmark summary

All values below were generated automatically from the synthetic benchmark. No real-sensor measurements are claimed.

## S1 baseline vs temporal offset

| v_rel (m/s) | Δt (ms) | pos_error mean ± std (m) | theory vΔt (m) |
|---:|---:|---:|---:|
| 5 | 0 | 0.0616 ± 0.0033 | 0.0000 |
| 5 | 50 | 0.2568 ± 0.0057 | 0.2500 |
| 5 | 100 | 0.5045 ± 0.0056 | 0.5000 |
| 5 | 150 | 0.7537 ± 0.0056 | 0.7500 |
| 5 | 200 | 1.0033 ± 0.0056 | 1.0000 |
| 10 | 0 | 0.0616 ± 0.0033 | 0.0000 |
| 10 | 50 | 0.5045 ± 0.0056 | 0.5000 |
| 10 | 100 | 1.0033 ± 0.0056 | 1.0000 |
| 10 | 150 | 1.5029 ± 0.0055 | 1.5000 |
| 10 | 200 | 2.0027 ± 0.0055 | 2.0000 |
| 20 | 0 | 0.0616 ± 0.0033 | 0.0000 |
| 20 | 50 | 1.0033 ± 0.0056 | 1.0000 |
| 20 | 100 | 2.0027 ± 0.0055 | 2.0000 |
| 20 | 150 | 3.0025 ± 0.0055 | 3.0000 |
| 20 | 200 | 4.0024 ± 0.0055 | 4.0000 |

## First offset above group reference threshold

Reference threshold: pos_error > 0.50 m (group assumption, not an industry standard).

- v_rel=5 m/s: 100 ms
- v_rel=10 m/s: 50 ms
- v_rel=20 m/s: 50 ms

Identical evaluation times are used for every condition, after max offset + one LiDAR period. Standard deviation is across seed-level means, not individual frames.

## S1 compensation at v_rel=10 m/s

| Δt (ms) | Before (m) | Exact offset (m) | Offset −20 ms (m) | Offset +20 ms (m) |
|---:|---:|---:|---:|---:|
| 0 | 0.0616 | 0.0616 | 0.0616 | 0.2067 |
| 50 | 0.5045 | 0.0956 | 0.2124 | 0.2183 |
| 100 | 1.0033 | 0.1345 | 0.2253 | 0.2375 |
| 150 | 1.5029 | 0.1749 | 0.2459 | 0.2629 |
| 200 | 2.0027 | 0.2160 | 0.2722 | 0.2929 |

## S2 constant-acceleration approximation gap

This unconstrained synthetic trajectory can reverse relative motion. It is not a braking-to-rest model. The comparator uses initial speed v0, not instantaneous speed.

| v0 (m/s) | accel (m/s²) | Δt (ms) | mean pos_error (m) | mean approx_gap (m) |
|---:|---:|---:|---:|---:|
| 10 | -6 | 0 | 0.0616 | 0.0616 |
| 10 | -6 | 50 | 1.0895 | 0.5895 |
| 10 | -6 | 100 | 2.1642 | 1.1642 |
| 10 | -6 | 150 | 3.2295 | 1.7295 |
| 10 | -6 | 200 | 4.2847 | 2.2847 |
| 10 | -3 | 0 | 0.0616 | 0.0616 |
| 10 | -3 | 50 | 0.4186 | -0.0814 |
| 10 | -3 | 100 | 0.8235 | -0.1765 |
| 10 | -3 | 150 | 1.2277 | -0.2723 |
| 10 | -3 | 200 | 1.6299 | -0.3701 |
| 20 | -6 | 0 | 0.0616 | 0.0616 |
| 20 | -6 | 50 | 0.8261 | -0.1739 |
| 20 | -6 | 100 | 1.6403 | -0.3597 |
| 20 | -6 | 150 | 2.4504 | -0.5496 |
| 20 | -6 | 200 | 3.2557 | -0.7443 |
| 20 | -3 | 0 | 0.0616 | 0.0616 |
| 20 | -3 | 50 | 0.4108 | -0.5892 |
| 20 | -3 | 100 | 0.8128 | -1.1872 |
| 20 | -3 | 150 | 1.2196 | -1.7804 |
| 20 | -3 | 200 | 1.6297 | -2.3703 |

## S3 association swap rate

| d_gap (m) | Δt (ms) | mean swap rate (%) |
|---:|---:|---:|
| 2 | 0 | 0.00 |
| 2 | 50 | 0.00 |
| 2 | 100 | 25.31 |
| 2 | 150 | 50.00 |
| 2 | 200 | 50.00 |
| 4 | 0 | 0.00 |
| 4 | 50 | 0.00 |
| 4 | 100 | 0.00 |
| 4 | 150 | 0.00 |
| 4 | 200 | 25.31 |
| 8 | 0 | 0.00 |
| 8 | 50 | 0.00 |
| 8 | 100 | 0.00 |
| 8 | 150 | 0.00 |
| 8 | 200 | 0.00 |

## Figures

- [S1 error vs Δt](../figs/s1_error_vs_dt.png)
- [S2 approximation gap](../figs/s2_approx_gap.png)
- [S3 association heatmap](../figs/s3_assoc_heatmap.png)
- [Timeline example](../figs/timeline_example.png)
- [Compensation bar](../figs/compensation_bar.png)
