# Sensor Reality Sprint — T4 Camera–LiDAR Temporal Offset

This repository is a **synthetic** benchmark for studying timestamp misalignment between camera and LiDAR in an ADAS-style forward-target tracking setup. It does **not** claim measurements from real sensors.

## Run

```bash
python -m pip install -r requirements-lock.txt
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

## Bài nộp cá nhân

**NGUYỄN HỒNG CƯỜNG — 2A202602415**.

- [Báo cáo đủ 5 mục](report/2A202602415-NguyenHongCuong.md)
- [Pitch khoảng 4 phút](report/PITCH.md)
- [Checklist nộp](SUBMISSION.md)
- [Bảng kết quả](results/summary.md), [nguồn](SOURCES.md), [thành viên](TEAMMATES.md)

Đề gốc yêu cầu đúng 5 thành viên/5 lượt nộp. Thực tế hiện có 1 người; chưa có xác nhận ngoại lệ cho nộp cá nhân.

## Chạy trên PowerShell với Python 3.11

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
$env:PYTHONPATH = 'src'
$env:MPLBACKEND = 'Agg'
$env:MPLCONFIGDIR = Join-Path $env:TEMP 'sensor-sprint-matplotlib'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m sensor_sprint.run_benchmark --config configs/t4.yaml
```

Nếu máy dùng launcher `py`, thay lệnh đầu bằng `py -3.11 -m venv .venv`.

## Claim và kết quả

Tăng offset 0 → 50–200 ms làm sai số vị trí tăng; chuyển động đều gần công thức `v_rel × Δt`. Camera trong mô hình trả tọa độ 2D cùng hệ với LiDAR, không có detector hay chiếu pixel. Baseline/lỗi cùng trajectory, noise và seed; mọi điều kiện dùng 97 thời điểm từ 0,3 tới 9,9 s ở 10 Hz để loại warm-up. S2 là stress test gia tốc không giới hạn, có thể đổi chiều tương đối.

Tại 10 m/s: baseline **0,0616 m**, offset 150 ms **1,5029 m**, sau bù đúng **0,1749 m**. S3 khoảng cách 2 m: sai ID **0% → 50%** từ baseline tới 150 ms. Chỉ kết luận trong mô hình tổng hợp.

Log mới ghi lệnh, Python/packages, commit nền, trạng thái dirty và SHA-256 code/config. Các log cũ là lịch sử trước khi cố định cửa sổ đo; báo cáo dùng kết quả mới.

Repository: https://github.com/hongcuong26-debug/K4-Track4-Day04-2A202602415-Sensor-Reality-Sprint
