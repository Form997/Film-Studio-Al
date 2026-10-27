# V0.9 — Kiểm định đầu ra MP4 cục bộ

## Phạm vi
Bổ sung kiểm định metadata bằng ffprobe, hash SHA-256, kích thước, thời lượng, codec và độ phân giải. Mã audit tự viết, ffprobe là công cụ ngoài được gọi qua subprocess. Không sao chép mã FFmpeg.

## Quy trình
1. Cài FFmpeg và ffprobe trên PATH.
2. Đặt video vào thư mục STUDIO_HOME/outputs (tự tạo thư mục).
3. Đặt STUDIO_TOKEN trước khi chạy ứng dụng; không công khai API ra Internet.
4. POST /api/experiments/audit-local với body {"filename":"clip.mp4"} và header X-Studio-Token.
5. Xem duration, resolution, codec, bytes, sha256 và cảnh báo.

## Bảo vệ
Chỉ chấp nhận tên tệp MP4 đơn thuần, không cho đường dẫn tuyệt đối hay ../, resolve đường dẫn thật và từ chối symlink trỏ ra ngoài thư mục. Giới hạn kích thước 8 GiB và timeout ffprobe.

## Chưa có
Không tự tải video từ ComfyUI, không tự gán kết quả vào cảnh, không đo chất lượng cảm nhận, không kiểm tra toàn bộ frame, không xác nhận danh tính khuôn mặt, không có benchmark GPU thực tế.

## Nghiên cứu
- FFmpeg / ffprobe: https://github.com/FFmpeg/FFmpeg
- VBench: https://github.com/Vchitect/VBench
- OpenTimelineIO: https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- Wan2.2: https://github.com/Wan-Video/Wan2.2

Đây là nghiên cứu nguyên lý và giao diện công cụ, không bê nguyên mã nguồn.
