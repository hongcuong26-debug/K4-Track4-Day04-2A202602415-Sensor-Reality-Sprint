# Nguồn tham khảo và phạm vi sử dụng

Tài liệu được mở và đối chiếu khi hoàn thiện repo ngày 06/10/2026 với hỗ trợ của Codex. Người nộp cần đọc các mục dẫn bên dưới trước khi pitch. Không tuyên bố đã chạy iKalibr; toàn bộ CSV trong repo là phép thử tổng hợp độc lập.

## S1 — Paper có phiên bản cố định

Chen và cộng sự, **iKalibr: Unified Targetless Spatiotemporal Calibration for Resilient Integrated Inertial Systems**, [arXiv:2407.11420v2](https://arxiv.org/html/2407.11420v2), 14/11/2024. README ghi bản xuất bản IEEE T-RO 2025.

- Mục đã đối chiếu: Abstract, IV–VI, VII-D/Table V, VIII.
- Phương pháp: khởi tạo động rồi tối ưu batch với biểu diễn chuyển động liên tục; ước lượng extrinsic và offset thời gian.
- Đánh giá nguồn: tham số hiệu chuẩn và độ lệch chuẩn qua các lần thử, với dữ liệu thật; Table V có LI-Calib. Không so trực tiếp với sai số vị trí của bài này.
- Hạn chế tác giả nêu ở VIII: thiếu ground truth spatiotemporal đầy đủ; cần kích thích chuyển động 6-DoF, khó với một số xe mặt đất; LiDAR FoV nhỏ còn hạn chế.

## S2 — Repository và tài liệu chạy

- [README](https://github.com/Unsigned-Long/iKalibr/blob/master/readme.md): input là dữ liệu đa sensor có ít nhất một IMU; output là tham số không gian/thời gian. README liệt kê dữ liệu tự thu, LI-Calib, River, TUM GS-RS và VECtor.
- [Build](https://github.com/Unsigned-Long/iKalibr/blob/master/docs/details/build_ikalibr.md): hướng dẫn Ubuntu/ROS và thư viện C++.
- [Run](https://github.com/Unsigned-Long/iKalibr/blob/master/docs/details/use_ikalibr.md): cần dữ liệu chuyển động đủ kích thích, YAML và SfM cho camera quang học.
- [Release v1.2.0](https://github.com/Unsigned-Long/iKalibr/releases/tag/v1.2.0), commit hiển thị `3b8741e`. Release được đối chiếu để ghi phiên bản; các hướng dẫn trên được đọc ở nhánh `master` ngày 06/10/2026, không tuyên bố chúng là snapshot của tag này.

Lệnh gốc trong tài liệu Run (chưa chạy trong bài):

```bash
rosrun ikalibr ikalibr_prog _config_path:="path_of_your_config_file"
```

## Phần thực sự chạy trong bài

Repo hiện tại không có rosbag/IMU, ảnh thật hay point cloud thật; setup gốc không phù hợp đường chạy tối thiểu trên Windows trong lab 120 phút. Chọn mô phỏng T4 được đề cho phép: giữ trajectory, noise và seed, thay offset, đo sai số vị trí và association ID. Đây là kiểm tra tác động của lỗi thời gian, không tái hiện thuật toán hiệu chuẩn iKalibr hay kết quả của paper.

Dữ liệu tạo bằng [scenarios.py](src/sensor_sprint/scenarios.py) và [sensors.py](src/sensor_sprint/sensors.py); cấu hình [t4.yaml](configs/t4.yaml); lệnh đã chạy và phiên bản môi trường nằm trong log mới nhất ở [logs/](logs/). Giới hạn phép thử ở [báo cáo](report/2A202602415-NguyenHongCuong.md).
