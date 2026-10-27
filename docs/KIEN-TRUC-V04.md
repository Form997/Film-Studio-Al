# V0.4 — Nền móng bền vững (foundation release)

## Mục đích
Tách dữ liệu, kế hoạch đạo diễn và bộ máy sinh video để sau này thay mô hình mà không phải viết lại ứng dụng. Tự lập trình từ nguyên lý; tham khảo công trình và API, không sao chép nguyên mã.

## Các hợp đồng
- `studio/contracts.py`: schema version 0.4.0, tỷ lệ khung hình, FPS, ngôn ngữ vi/en/zh, kiểm tra tham chiếu nhân vật và ID cảnh, hash dữ liệu ổn định.
- `studio/engine_contract.py`: GenerationRequest, GenerationResult, giao diện VideoEngine, DryRunEngine.
- DryRunEngine **luôn từ chối sinh video** khi chưa cấu hình mô hình: tránh tạo cảm giác video AI đã chạy.
- `GET /api/projects/{id}/contract`: báo cáo hợp lệ dữ liệu, không sửa dự án.
- `GET /api/projects/{id}/generation-plan?language=vi&aspect=landscape`: kế hoạch cảnh kèm manifest SHA-256 để đối chiếu tái lập.

## Học thuật và mã nguồn tham khảo
- Video diffusion / DiT: https://github.com/Wan-Video/Wan2.2
- Video foundation model: https://github.com/Tencent-Hunyuan/HunyuanVideo
- Workflow node-based: https://github.com/Comfy-Org/ComfyUI
- Timeline interchange: https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- Video processing: https://github.com/FFmpeg/FFmpeg

Tham khảo thuật toán, cấu trúc và các paper dẫn nguồn; kiểm tra license riêng cho code/weights/dataset. Không khẳng định những thuật toán trên đã được tái triển khai đầy đủ trong V0.4.

## Tiêu chí nghiệm thu
1. Hợp đồng có version, không phụ thuộc model bên ngoài.
2. Hash không đổi nếu thứ tự khóa JSON thay đổi.
3. Thiếu ID nhân vật và trùng ID bị phát hiện.
4. Dry-run không giả tạo video.
5. Kiểm thử cũ không bị phá.
6. Trước khi phát hành production: thêm auth đầy đủ, quyền media, sandbox đường dẫn, tải nặng và test GPU.

## Giới hạn
Đây là V0.4 foundation, **không phải** mô hình sinh phim AI tự huấn luyện. Tính nhất quán khuôn mặt thực tế cần embedding/pose/tracking và đánh giá dữ liệu có quyền sử dụng.
