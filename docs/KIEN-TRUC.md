# Kiến trúc tự chủ mã nguồn

```text
WEB (HTML/CSS/JS) → FastAPI (studio/api.py)
                         ├─ storage.py: dữ liệu JSON cục bộ
                         ├─ director.py: scene, shotlist, continuity metadata, QA
                         ├─ prompts.py: prompt contract độc lập model
                         ├─ render.py: MP4 minh họa thông qua FFmpeg
                         └─ comfy.py: adapter HTTP ComfyUI tùy chọn
```

## Nguyên tắc không khóa vào một mô hình
- Project, Scene và Character thuộc studio, không thuộc ComfyUI/Wan/LTX.
- Không fork/chỉnh trực tiếp mã các engine ngoài vào kho này.
- Việc thay model chỉ cần lớp adapter + workflow, kèm kiểm thử hồi quy.
- Phân biệt rõ: *prompt continuity* chưa bằng *identity lock* thị giác.
- Quyền sử dụng model, checkpoint, giọng, ảnh và nhạc được kiểm tra riêng.

## Bảo mật trước khi triển khai
Bản hiện tại **chỉ localhost**, chưa có auth/permission đầy đủ; không đưa ra mạng công cộng. Trước khi cung cấp SaaS phải bổ sung xác thực mọi endpoint đọc/ghi, CSRF nếu dùng cookie, quota, giới hạn tệp, chống SSRF, quét dữ liệu cá nhân và audit log.

## Tính năng thực tế
Đã có API tạo dự án, tách cảnh, hồ sơ nhân vật, audit cấu trúc, shotlist, dựng MP4 minh họa. Chưa chạy nghiệm thu tạo cảnh phim AI bằng GPU.
