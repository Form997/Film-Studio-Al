# V1.0 — Tích hợp chuỗi sản xuất và nghiệm thu Alpha

## Phạm vi
Mã điều phối tự viết liên kết project -> scene plan -> submit workflow cục bộ -> kiểm tra history -> audit MP4 -> gắn metadata video vào đúng scene.

## Quy trình thao tác
1. Tạo project và scene từ giao diện hoặc API.
2. GET /api/projects/{id}/pipeline-preview để xem kế hoạch phân cảnh.
3. Cài ComfyUI và mô hình video hợp lệ, chuẩn bị workflow API-format tương thích.
4. Cấu hình STUDIO_TOKEN, POST /api/projects/{id}/scenes/{scene_id}/submit-workflow với workflow và model_label. Phải có ComfyUI trên localhost.
5. Kiểm tra prompt_id qua GET /api/experiments/local-status/{prompt_id}; trạng thái history_available chưa chứng minh có video.
6. Tự kiểm tra và đặt tệp MP4 trong STUDIO_HOME/outputs.
7. POST /api/projects/{id}/scenes/{scene_id}/attach-verified với filename để ffprobe kiểm định metadata và gắn đúng scene.

## Nghiệm thu bắt buộc
- python -m pytest -q: chạy toàn bộ test cũ và mới.
- TestClient kiểm tra auth 401/403, project/scene không tồn tại, workflow sai.
- Thử ComfyUI thật với một model/video workflow được cấp phép, ghi GPU/VRAM, thời gian chạy, weights, seed và kiểm tra video đầu ra.
- Kiểm tra cảnh ghép phim: renderer V0.2 hiện chỉ xuất thẻ tiêu đề, chưa ghép các video AI đã gắn. Chưa có phép đo chất lượng hình ảnh tự động.

## Giới hạn
V1.0 Alpha không có video model mặc định, không tự lấy video từ ComfyUI, không tự dựng phim AI từ nhiều clip, không có face verification. Trường verified_media chỉ xác minh metadata qua ffprobe và hash tệp cục bộ. Không được công bố nghiệm thu GPU/video thực tế trước khi chạy.

## Nguồn tham khảo kiến trúc
- https://github.com/Comfy-Org/ComfyUI
- https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- https://github.com/FFmpeg/FFmpeg
- https://github.com/Wan-Video/Wan2.2

Không sao chép mã các dự án trên; kiểm tra license code và weights riêng.
