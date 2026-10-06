# Metrics — synthetic benchmark

All metrics below are computed only from **synthetic** trajectories and **synthetic** camera/LiDAR measurements.

## `pos_error` (m)

\[
\mathrm{pos\_error}(t)=\|p_{lidar\_stamped}(t)-p_{true}(t)\|_2
\]

Reported as the mean over LiDAR sample times, then summarized across random seeds. Lower is better.
This is a sensor-health proxy, **not mAP** and not a complete ADAS safety metric.

Every condition shares times `t >= max(offsets_ms)/1000 + 1/lidar_hz`: 97 timestamps from 0.3 to 9.9 s for the submitted config. This excludes clamped historical samples and velocity warm-up. Reported ± is the sample STD of 10 seed-level means, not a confidence interval or frame-level STD.

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

`v_hat(t)=(p_lidar(t)-p_lidar(t-h))/h`, `p_corrected=p_lidar+v_hat*assumed_offset`, `h=0.1 s`. Assumed offsets are true offset, `max(0,true_offset-20 ms)`, and `true_offset+20 ms` (fixed in the runner). Even exact compensation retains measurement noise and amplifies noise in velocity.

## S2 interpretation

`x(t)=100-v0*t-0.5*a*t²`; instantaneous closing speed is `v0+a*t`. The trajectory is not clipped at zero speed and may reverse relative motion. It is a mathematical constant-acceleration stress test, not braking to rest. Noise-free mismatch is `abs((v0+a*t)*offset-0.5*a*offset²)`. The S2 comparator uses initial `v0*offset`, so `approx_gap` measures departure from that simplified comparator.

## Association interpretation

Each LiDAR point independently chooses the nearest camera target in 2D; two points may choose the same ID. "Swap rate" means wrong-ID assignment, not necessarily a bijective exchange. S3 does not simulate radar ghosts or a production tracker.

## Reference threshold

`pos_error > 0.5 m` is treated as “concerning” **only as a group assumption for this sprint**. It is not presented as an industry standard.
