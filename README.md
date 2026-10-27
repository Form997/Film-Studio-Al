# 🎬 HAI ĐẤT AI FILM STUDIO

**Nền tảng sản xuất phim AI tự chủ mã nguồn, ưu tiên tiếng Việt.**

> V0.2 Alpha — ứng dụng điều phối, biên kịch, quản lý nhân vật và dựng video thẻ tiêu đề chạy cục bộ. **Chưa phải hệ thống sinh phim AI hoàn chỉnh**; cần GPU + mô hình thích hợp để sinh cảnh video AI.

## Cài đặt nhanh
Cần Python 3.11+, FFmpeg và FFprobe trên PATH.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m studio
```

Mở **http://127.0.0.1:7860**. Để kiểm thử: `pip install -r requirements-dev.txt && pytest -q`.

### Có gì trong V0.2?
- Giao diện Web tiếng Việt; lưu nhiều dự án dạng JSON cục bộ.
- Kịch bản thành phân cảnh; hồ sơ nhân vật, lời thoại, thời lượng và góc máy.
- Kiểm định cấu trúc và xuất shotlist JSON, không nhận diện gương mặt bằng AI.
- Dựng video minh họa có thẻ tiêu đề (MP4) bằng Pillow + FFmpeg, không cần GPU.
- Bộ kết nối ComfyUI tách biệt, không sao chép source bên ngoài, chưa có workflow sinh video chạy sẵn.
- Tests + GitHub Actions CI.

### Giới hạn, trách nhiệm
- **Chưa có** khóa danh tính khuôn mặt, chuyển động nhân vật AI nhất quán, môi/giọng Việt tự động hoặc SaaS nhiều người dùng.
- Bản này chỉ phục vụ **một người trên máy cục bộ**. Không mở port 7860 lên Internet khi chưa triển khai xác thực đầy đủ.
- Không đóng gói model, weights, nhạc, ảnh của bên thứ ba. Giấy phép mỗi mô hình/dữ liệu phải xem riêng.

## Định hướng tự chủ
Toàn bộ mã điều phối ứng dụng trong kho được phát triển độc lập. Tham khảo API và kiến trúc các dự án quốc tế; FFmpeg và ComfyUI chỉ là chương trình bên ngoài có thể thay thế.

## Cấu trúc
- `studio/`: FastAPI, lưu dự án, phân cảnh, dựng thử, ComfyUI adapter
- `web/`: giao diện HTML/CSS/JS
- `tests/`: kiểm thử
- `docs/`: kỹ thuật, nguồn tham khảo và lộ trình

## Nguồn tham khảo
- https://github.com/Comfy-Org/ComfyUI
- https://github.com/Wan-Video/Wan2.2
- https://github.com/Lightricks/LTX-2
- https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- https://github.com/FFmpeg/FFmpeg

**Tác giả/điều phối:** Form997 — HAI ĐẤT AI FILM STUDIO. **License:** MIT cho mã tự viết; không bao gồm model bên ngoài.

Đây là bản lõi được tái xây dựng trực tiếp trên GitHub; lưu trữ V0.2 trước đây vẫn được giữ riêng để đối chiếu tính năng và tiếp tục nghiệm thu.
