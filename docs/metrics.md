# Metrics — synthetic benchmark

All metrics below are computed only from **synthetic** trajectories and **synthetic** camera/LiDAR measurements.

## `pos_error` (m)

\[
\mathrm{pos\_error}(t)=\|p_{lidar\_stamped}(t)-p_{true}(t)\|_2
\]

Reported as the mean over LiDAR sample times, then summarized across random seeds. Lower is better.
This is a sensor-health proxy, **not mAP** and not a complete ADAS safety metric.

## `theory_error` (m)

For S1 constant relative speed only:

\[
\mathrm{theory\_error}=v_{rel}\Delta t
\]

It is the ideal no-noise positional mismatch induced by temporal offset. `approx_gap = pos_error - theory_error`. Lower absolute gap means the approximation matches better.

## `assoc_swap_rate` (%)

For S3 two-target nearest-neighbor association: percentage of target-frame assignments in which a LiDAR target is matched to a camera target with a different ID. Lower is better.

## `residual_error` (m)

Position error after motion compensation using velocity estimated from the two most recent LiDAR samples and extrapolation by an assumed time offset. Lower is better.

## Reference threshold

`pos_error > 0.5 m` is treated as “concerning” **only as a group assumption for this sprint**. It is not presented as an industry standard.
