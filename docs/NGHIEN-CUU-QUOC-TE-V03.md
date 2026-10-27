# V0.3 — Nghiên cứu nguồn quốc tế (Việt / English / 中文)

## Nguyên tắc
Chỉ nghiên cứu tài liệu, API, ý tưởng và cách tổ chức; không sao chép nguyên mã hoặc trọng số.
Mỗi mô hình phải kiểm tra giấy phép code, giấy phép weights và quyền dữ liệu đầu vào riêng.
Từ 'AI director' trong V0.3 chỉ là hệ thống điều phối dựa quy tắc; chưa có LLM suy luận.

## Nguồn Trung Quốc
1. Wan2.2 (Alibaba/Wan): https://github.com/Wan-Video/Wan2.2
   - Text-to-video, image-to-video, Animate; tài liệu tiếng Anh và tiếng Trung.
   - Học kiến trúc chia chế độ tạo cảnh; không tự nhận đã tích hợp trọng số.
2. HunyuanVideo / HunyuanVideo-1.5 (Tencent):
   https://github.com/Tencent-Hunyuan/HunyuanVideo
   https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5
   - Tham khảo mô hình video và prompt rewrite; kiểm tra license trước sử dụng.

## Nguồn quốc tế/tiếng Anh
3. OpenTimelineIO: https://github.com/AcademySoftwareFoundation/OpenTimelineIO
   - Tham khảo ý tưởng shot list, thứ tự cảnh và timeline, không sao chép mã.
4. ComfyUI: https://github.com/Comfy-Org/ComfyUI
   - API workflow và bộ kết nối model có thể thay thế.
5. FFmpeg: https://github.com/FFmpeg/FFmpeg
   - Dựng video; giấy phép LGPL/GPL tùy cấu hình build.

## Những gì V0.3 thực sự làm
- API đạo diễn /director?language=vi|en|zh: prompt, góc máy, kiểm tra nhân vật mất liên kết.
- Bản dấu vân tay hồ sơ nhân vật: phát hiện sửa thông tin, KHÔNG phải nhận dạng khuôn mặt.
- Tạo chỉ dẫn cảnh bằng ngôn ngữ người dùng chọn; không dịch máy văn bản kịch bản.
- Kiểm thử ba ngôn ngữ, phát hiện nhân vật vào/ra cảnh và nhân vật thiếu.

## Chưa hoàn thành
- Không có model video/LLM/nhận diện mặt chạy nội bộ.
- Chưa có bộ dịch Việt-Anh-Trung tự động hoặc đồng bộ môi/giọng.
- Chưa kiểm chứng chất lượng hình ảnh hay nhất quán mặt bằng video thực tế.
