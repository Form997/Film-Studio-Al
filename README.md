# 🎬 AI FILM STUDIO

**Nền tảng sản xuất phim AI tự chủ mã nguồn, ưu tiên tiếng Việt.**

> V2.0 Alpha — ứng dụng điều phối, biên kịch, quản lý nhân vật và dựng video thẻ tiêu đề chạy cục bộ. **Chưa phải hệ thống sinh phim AI hoàn chỉnh**; cần GPU + mô hình thích hợp để sinh cảnh video AI.


## V2.0 Alpha — Ghép video cảnh MP4
- `studio/assembly.py`: đối chiếu SHA-256 của clip đã gắn vào cảnh, chuẩn hóa video bằng FFmpeg và nối theo thứ tự cảnh.
- `POST /api/projects/{id}/assemble` và `GET /api/projects/{id}/assembled.mp4` yêu cầu `STUDIO_TOKEN`.
- `tests/test_assembly.py`; [hướng dẫn V2.0](docs/PHAT-HANH-V20.md).
- **Chưa tự sinh video AI, chưa ghép âm thanh và chưa nghiệm thu end-to-end với clip thực tế.**

## V1.0 Alpha — Chuỗi sản xuất tích hợp
- `studio/pipeline.py`: kiểm tra project/scene, lập kế hoạch, gửi workflow ComfyUI, gắn MP4 đã kiểm định vào đúng cảnh.
- API: `GET /api/projects/{id}/pipeline-preview`, `POST /api/projects/{id}/scenes/{scene_id}/submit-workflow`, `POST /api/projects/{id}/scenes/{scene_id}/attach-verified`.
- Thao tác ghi/thực thi mới bắt buộc `STUDIO_TOKEN`; video đặt trong `STUDIO_HOME/outputs`.
- Test: `tests/test_pipeline.py`; [nghiệm thu V1.0](docs/NGHIEM-THU-V10.md).
- **V1.0 Alpha chưa có model video mặc định, chưa tự thu clip từ ComfyUI, chưa ghép các clip AI vào phim. Chưa nghiệm thu GPU/video thật.**

## V0.9 — Kiểm định video MP4 cục bộ
- `studio/media_audit.py`: ffprobe metadata, SHA-256, duration, resolution, codec, file size.
- `POST /api/experiments/audit-local` kiểm tra tệp trong `STUDIO_HOME/outputs`, yêu cầu `STUDIO_TOKEN`.
- [Tài liệu V0.9](docs/NGHIEM-THU-V09.md); tests `tests/test_media_audit.py`.
- **Chưa tự thu video từ ComfyUI; chưa đánh giá chất lượng hình ảnh hoặc giải mã toàn bộ frame.**

## V0.8 — Thử nghiệm thực thi ComfyUI cục bộ
- `studio/runner.py`: kiểm định workflow, hash, gửi job khi chủ động yêu cầu, kiểm tra lịch sử job.
- API: `POST /api/experiments/submit-local`, `GET /api/experiments/local-status/{prompt_id}`.
- Bắt buộc cấu hình `STUDIO_TOKEN`; ComfyUI chỉ trên loopback.
- [Tài liệu V0.8](docs/THUC-THI-V08.md) và `tests/test_runner.py`.
- **Chưa có model video tích hợp sẵn; job được gửi không đồng nghĩa video hoàn thành.**

## V0.7 — Giao thức thực nghiệm
- Tạo kế hoạch nhiều seed, SHA-256 và tổng hợp điểm đánh giá được nhập.
- API: /api/projects/{id}/experiment-plan và /api/experiments/evaluate.
- Xem docs/THUC-NGHIEM-V07.md. Chưa tích hợp mô hình sinh video.

## V0.6 — Đạo diễn phân cảnh và mạch truyện
- `studio/story_engine.py`: scene graph, gợi ý góc máy, quy tắc chuyển cảnh, nhân vật vào/ra và tổng thời lượng.
- Hỗ trợ từ điển quy tắc Việt/Anh/Trung; không dịch tự động và không phải mô hình ngôn ngữ.
- API `GET /api/projects/{id}/story-plan?language=vi` (hoặc en/zh).
- Test: `tests/test_story_engine.py`. Tài liệu: [THUAT-TOAN-V06](docs/THUAT-TOAN-V06.md).
- **Đây là bộ lập kế hoạch dựa quy tắc, chưa tự hiểu sâu hoặc dựng video AI.**

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

**Tác giả/điều phối:** Form997 — AI FILM STUDIO. **License:** MIT cho mã tự viết; không bao gồm model bên ngoài.

Đây là bản lõi được tái xây dựng trực tiếp trên GitHub; lưu trữ V0.2 trước đây vẫn được giữ riêng để đối chiếu tính năng và tiếp tục nghiệm thu.
