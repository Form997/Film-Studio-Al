# V2.0 Alpha: ghép clip MP4 đã kiểm định

Quy trình: tạo dự án và cảnh, đưa MP4 vào STUDIO_HOME/outputs, dùng attach-verified cho từng cảnh, sau đó POST /api/projects/{project_id}/assemble với width=1280, height=720, fps=24 và header X-Studio-Token. Cần cấu hình STUDIO_TOKEN. Tải kết quả bằng GET /api/projects/{project_id}/assembled.mp4 với cùng header.

FFmpeg chuẩn hóa kích thước và tốc độ khung hình, nối theo thứ tự cảnh. Trước khi ghép, hệ thống kiểm tra lại SHA-256 của mỗi clip. Đầu ra nằm trong STUDIO_HOME/renders.

Giới hạn: không tự sinh video AI, không tự tải clip từ ComfyUI, không xử lý tiếng nói/nhạc/phụ đề, chỉ nối cắt thẳng. Chưa nghiệm thu GPU hay kiểm thử với video thật. Không triển khai công khai trên Internet.

Kiểm thử: python -m pytest -q, sau đó thử thủ công hai clip MP4 hợp lệ và kiểm tra thời lượng, thứ tự, hình ảnh, âm thanh. Nguồn tham khảo: https://github.com/FFmpeg/FFmpeg và https://github.com/AcademySoftwareFoundation/OpenTimelineIO . Mã điều phối tự viết.
