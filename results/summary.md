# Synthetic benchmark summary

All values below were generated automatically from the synthetic benchmark. No real-sensor measurements are claimed.

## S1 baseline vs temporal offset

| v_rel (m/s) | Δt (ms) | pos_error mean ± std (m) | theory vΔt (m) |
|---:|---:|---:|---:|
| 5 | 0 | 0.0621 ± 0.0030 | 0.0000 |
| 5 | 50 | 0.2570 ± 0.0056 | 0.2500 |
| 5 | 100 | 0.5046 ± 0.0055 | 0.5000 |
| 5 | 150 | 0.7538 ± 0.0054 | 0.7500 |
| 5 | 200 | 1.0034 ± 0.0054 | 1.0000 |
| 10 | 0 | 0.0621 ± 0.0030 | 0.0000 |
| 10 | 50 | 0.5046 ± 0.0055 | 0.5000 |
| 10 | 100 | 1.0035 ± 0.0054 | 1.0000 |
| 10 | 150 | 1.5030 ± 0.0053 | 1.5000 |
| 10 | 200 | 2.0028 ± 0.0053 | 2.0000 |
| 20 | 0 | 0.0621 ± 0.0030 | 0.0000 |
| 20 | 50 | 1.0035 ± 0.0054 | 1.0000 |
| 20 | 100 | 2.0029 ± 0.0054 | 2.0000 |
| 20 | 150 | 3.0026 ± 0.0053 | 3.0000 |
| 20 | 200 | 4.0025 ± 0.0053 | 4.0000 |

## First offset above group reference threshold

Reference threshold: pos_error > 0.50 m (group assumption, not an industry standard).

- v_rel=5 m/s: 100 ms
- v_rel=10 m/s: 50 ms
- v_rel=20 m/s: 50 ms

## S2 braking approximation gap

| v_rel | accel | Δt | mean pos_error (m) | mean approx_gap (m) |
|---:|---:|---:|---:|---:|
| 10 | -6 | 0 | 0.0621 | 0.0621 |
| 10 | -6 | 50 | 1.0771 | 0.5771 |
| 10 | -6 | 100 | 2.1397 | 1.1397 |
| 10 | -6 | 150 | 3.2109 | 1.7109 |
| 10 | -6 | 200 | 4.2603 | 2.2603 |
| 10 | -3 | 0 | 0.0621 | 0.0621 |
| 10 | -3 | 50 | 0.4201 | -0.0799 |
| 10 | -3 | 100 | 0.8267 | -0.1733 |
| 10 | -3 | 150 | 1.2301 | -0.2699 |
| 10 | -3 | 200 | 1.6332 | -0.3668 |
| 20 | -6 | 0 | 0.0621 | 0.0621 |
| 20 | -6 | 50 | 0.8291 | -0.1709 |
| 20 | -6 | 100 | 1.6466 | -0.3534 |
| 20 | -6 | 150 | 2.4550 | -0.5450 |
| 20 | -6 | 200 | 3.2622 | -0.7378 |
| 20 | -3 | 0 | 0.0621 | 0.0621 |
| 20 | -3 | 50 | 0.4225 | -0.5775 |
| 20 | -3 | 100 | 0.8364 | -1.1636 |
| 20 | -3 | 150 | 1.2374 | -1.7626 |
| 20 | -3 | 200 | 1.6534 | -2.3466 |

## S3 association swap rate

| d_gap (m) | Δt (ms) | mean swap rate (%) |
|---:|---:|---:|
| 2 | 0 | 0.00 |
| 2 | 50 | 0.00 |
| 2 | 100 | 25.25 |
| 2 | 150 | 50.00 |
| 2 | 200 | 50.00 |
| 4 | 0 | 0.00 |
| 4 | 50 | 0.00 |
| 4 | 100 | 0.00 |
| 4 | 150 | 0.00 |
| 4 | 200 | 25.26 |
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
