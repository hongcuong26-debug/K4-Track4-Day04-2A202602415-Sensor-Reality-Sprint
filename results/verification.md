# Kiểm tra bản hoàn thiện ngày 06/10/2026

Môi trường: Python 3.11.9 trong `.venv`, dependency ở `requirements-lock.txt`.

## Kết quả thực chạy

```text
python -m pytest -q
6 passed in 2.16s

python -m sensor_sprint.run_benchmark --config configs/t4.yaml
Synthetic benchmark complete: 500 rows in 1.41s
```

Log: [run_20261006T042135Z.log](../logs/run_20261006T042135Z.log).

Sau lần chạy này, đã gọi lại `run_s1`, `run_s2`, `run_s3` với cùng YAML và dùng `pandas.testing.assert_frame_equal` đối chiếu CSV, `rtol=atol=1e-12`: **500 hàng khớp**. Đã tính SHA-256 từng code/config/dependency trong log và đối chiếu file hiện tại: **khớp**. Đã kiểm tra link cục bộ trong các Markdown: **đều tồn tại**. Đã mở xem đủ 5 PNG: tiêu đề, đơn vị và legend đọc được, không bị cắt.

Các kiểm tra này xác nhận pipeline tổng hợp và bằng chứng lưu trong repo, không xác nhận độ chính xác sensor thật, quyền truy cập GitHub hay lượt nộp VLearn.
