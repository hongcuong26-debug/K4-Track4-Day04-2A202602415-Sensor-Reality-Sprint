# Sensor Reality Sprint — T4 Camera–LiDAR Temporal Offset

This repository is a **synthetic** benchmark for studying timestamp misalignment between camera and LiDAR in an ADAS-style forward-target tracking setup. It does **not** claim measurements from real sensors.

## Run

```bash
python -m pip install -r requirements.txt
make all
```

On Windows CMD without `make`:

```bat
set PYTHONPATH=src
python -m pytest -q
python -m sensor_sprint.run_benchmark --config configs/t4.yaml
```

Generated artifacts:

- `results/results.csv`
- `results/summary.md`
- `figs/*.png`
- `logs/run_*.log`

## Structure

- `configs/t4.yaml`: all synthetic benchmark parameters
- `docs/metrics.md`: metric definitions and units
- `src/sensor_sprint/`: implementation
- `tests/`: deterministic acceptance tests
- `SOURCES.md`: human-read sources only
- `TEAMMATES.md`: human-maintained participant list

## Reproducibility

The runner records the full config, every seed, runtime, and git commit (or `UNKNOWN` when no commit exists yet) in the generated log.

## Human-only TODOs

Fill `SOURCES.md`, `TEAMMATES.md`, and the final report/slide after reading actual sources and inspecting generated results.
