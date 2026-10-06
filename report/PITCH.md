# Pitch khoảng 4 phút — NGUYỄN HỒNG CƯỜNG, 2A202602415

## 0:00–0:35 — Problem

Em chọn T4: lệch thời gian camera–LiDAR trong ADAS. Nếu camera nhìn mục tiêu hiện tại còn LiDAR trả dữ liệu cũ 150 ms, ghép hai tọa độ có thể sai dù từng sensor vẫn đo được. Claim là offset tăng làm sai số tăng gần tốc độ nhân thời gian khi chuyển động đều.

## 0:35–1:10 — Method

Nguồn liên quan là iKalibr; nguồn và đường chạy gốc ở SOURCES.md. Em dùng mô phỏng độc lập vì không có dữ liệu và môi trường chạy gốc. Camera/LiDAR là tọa độ 2D có noise. Em đo sai số vị trí và ghép sai ID, không phải mAP detector thật.

## 1:10–2:05 — Benchmark

Mở `figs/s1_error_vs_dt.png` và `results/summary.md`.

Baseline và lỗi cùng trajectory, noise, 10 seed và 97 thời điểm đo. Tại 10 m/s, baseline 0,0616 m, offset 150 ms là 1,5029 m, gần lý thuyết 1,5 m. Bù bằng vận tốc hai mẫu còn 0,1749 m. Nếu offset bù sai ±20 ms, sai số khoảng 0,246–0,263 m.

## 2:05–2:50 — Failure

Mở `figs/s3_assoc_heatmap.png`.

Hai mục tiêu cách 2 m, chuyển động 10 m/s, offset 150 ms làm 50% ghép sai ID so với 0% baseline. Đây là số đo trong mô hình. Nguy cơ cập nhật nhầm track là suy luận; em chưa chạy tracker thật. S2 là gia tốc có thể đổi chiều tương đối, không phải xe phanh tới dừng.

## 2:50–3:40 — Decision

Em đề xuất log timestamp thu/nhận, offset, residual và chất lượng association. Thử bù khi offset đáng tin; giảm trọng số dữ liệu cũ khi residual cao. Ngưỡng 0,5 m là giả định lab. Bù nhạy noise; chờ đồng bộ tăng latency; bỏ frame giảm dữ liệu. Fallback và latency cần thử tiếp.

## 3:40–4:00 — Giới hạn và bằng chứng

Dữ liệu tổng hợp, chưa có jitter hay sensor thật. Repo có CSV 500 hàng, 5 plot, config, log và 6 test. Log mới ghi môi trường và hash code. Bài do một mình em thực hiện; yêu cầu 5 thành viên cần giảng viên xác nhận ngoại lệ.

## Khi được hỏi

- Baseline khác 0 vì noise; ± là độ lệch chuẩn giữa seed.
- Không chạy iKalibr và không coi số paper là số tự đo.
- Nearest-neighbor độc lập có thể ghép nhiều LiDAR cùng camera ID.
- Bù đúng chưa về baseline do noise vận tốc.
- Kiểm tra số bằng cách lọc CSV theo scenario, tốc độ, offset, khoảng cách và seed.
