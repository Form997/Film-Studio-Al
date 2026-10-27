# V0.5: Nền tảng thuật toán chuyển động

Mục tiêu: tự triển khai phép đo toán học, có kiểm thử và không phụ thuộc mô hình.

## Các phép đo
- Pose distance: trung bình khoảng cách Euclid giữa các khớp chung của hai khung hình, trên tọa độ chuẩn hóa 0..1.
- Motion report: đánh dấu các bước có khoảng cách vượt ngưỡng cấu hình.
- Median displacement: trung vị các bước đo được.
- Metadata consistency: so sánh chính xác các thuộc tính appearance, costume, voice.

## Giới hạn
Dữ liệu keypoint phải được cung cấp từ bên ngoài. Chưa có mô hình phát hiện khớp xương, nhận dạng danh tính hay xác thực khuôn mặt. Chuyển động camera có thể làm sai lệch chỉ số. Không có khớp chung được báo là insufficient_data, không gán bằng 0. Ngưỡng cần hiệu chuẩn trên dữ liệu có nhãn.

## Nguồn nghiên cứu thuật toán, không sao chép mã
- OpenPose: https://github.com/CMU-Perceptual-Computing-Lab/openpose
- MMPose (English / 中文): https://github.com/open-mmlab/mmpose
- MediaPipe: https://github.com/google-ai-edge/mediapipe
- RAFT optical flow: https://github.com/princeton-vl/RAFT
- ByteTrack: https://github.com/ifzhang/ByteTrack

## Nghiệm thu
Chạy pytest trên tests/test_continuity.py; kiểm tra NaN, tọa độ sai, thiếu khớp chung, phát hiện bước nhảy và metadata. Đây là nền tảng nghiên cứu, không phải hệ thống AI video hoàn chỉnh.
