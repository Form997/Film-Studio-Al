# 🎬 HAI ĐẤT AI FILM STUDIO

**Nền tảng sản xuất phim AI tự chủ mã nguồn, ưu tiên tiếng Việt.**

> V0.5 Alpha — ứng dụng điều phối, biên kịch, quản lý nhân vật và dựng video thẻ tiêu đề chạy cục bộ. **Chưa phải hệ thống sinh phim AI hoàn chỉnh**; cần GPU + mô hình thích hợp để sinh cảnh video AI.


## V0.5 — Thuật toán chuyển động tự viết
- `studio/continuity.py`: khoảng cách pose, phát hiện bước nhảy, trung vị chuyển động, đối chiếu metadata.
- API `POST /api/analysis/motion` nhận keypoint đã có, cần token ghi nếu cấu hình.
- Test: `tests/test_continuity.py`. Tài liệu: [THUAT-TOAN-V05](docs/THUAT-TOAN-V05.md).
- **Không có nhận dạng khuôn mặt hoặc mô hình pose detector tích hợp**. Không thể xác nhận tính nhất quán nhân vật chỉ từ chỉ số này.

## V0.4 — Nền tảng ổn định để phát triển dài hạn
- Schema dữ liệu có phiên bản, kiểm tra ID cảnh/nhân vật và tham chiếu.
- Chuẩn hóa cấu hình khung hình, FPS, ngôn ngữ Việt/Anh/Trung.
- Hợp đồng độc lập mô hình `VideoEngine`; không khóa vào một nhà cung cấp.
- Kế hoạch sinh cảnh có hash SHA-256, hỗ trợ đối chiếu và truy vết.
- API: `GET /api/projects/{id}/contract` và `GET /api/projects/{id}/generation-plan`.
- Kiểm thử nền tảng: `tests/test_contracts.py`.
- [Tài liệu kiến trúc V0.4](docs/KIEN-TRUC-V04.md).
- **Chưa sinh video AI thực tế**; cần engine/model được cấu hình và kiểm thử riêng.

## V0.3 — Đạo diễn đa ngôn ngữ (vi/en/zh)
- Tự viết `studio/film_brain.py`: kế hoạch cảnh, góc máy, prompt ba ngôn ngữ, nhân vật vào/ra cảnh, phát hiện ID nhân vật thiếu.
- API: `GET /api/projects/{project_id}/director?language=vi&aspect=landscape` (có thể đổi `en` hoặc `zh`).
- Kiểm tra sửa hồ sơ nhân vật bằng fingerprint; **chưa phải nhận diện khuôn mặt**.
- Kiểm thử: `tests/test_film_brain.py`.
- Nghiên cứu nguồn Trung Quốc và tiếng Anh: [docs/NGHIEN-CUU-QUOC-TE-V03.md](docs/NGHIEN-CUU-QUOC-TE-V03.md).
- **Giới hạn:** prompt đa ngôn ngữ không phải bản dịch kịch bản; không có mô hình video hay LLM được tích hợp sẵn.

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
