PYTHON ?= python
export PYTHONPATH := src

.PHONY: test run all clean

test:
	$(PYTHON) -m pytest -q

run:
	$(PYTHON) -m sensor_sprint.run_benchmark --config configs/t4.yaml

all: test run

clean:
	rm -f results/results.csv results/summary.md figs/*.png logs/*.log
