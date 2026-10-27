# KIỂM ĐỊNH TOÀN BỘ V0.1–V2.0 (27/10/2026)

## Phạm vi và phương pháp
Đọc trực tiếp mã nguồn và test trên nhánh mặc định, xem lịch sử commit và cấu hình GitHub Actions. Đây là **rà soát tĩnh**, không phải xác nhận tất cả test đã chạy. Môi trường thực thi không tải được repository từ GitHub để chạy pytest. GitHub combined commit statuses tại commit 2e5c173a4d744ef4ab6a75795f028e18649e6219 không trả về trạng thái nào. Workflow tồn tại ở .github/workflows/test.yml nhưng chưa xác nhận được kết quả chạy mới nhất.

## Bảng kiểm định
| Giai đoạn | Chức năng có mã | Nghiệm thu thực thi |
|---|---|---|
| V0.1 | Chưa xác minh được mốc phát hành V0.1 độc lập | Chưa xác nhận |
| V0.2 | Dự án JSON, phân cảnh, thẻ tiêu đề MP4, API | Trước đây ghi nhận 12 tests passed; chưa chạy lại |
| V0.3 | Đạo diễn quy tắc vi/en/zh | Chưa chạy test |
| V0.4 | Hợp đồng dữ liệu và VideoEngine | Chưa chạy test |
| V0.5 | Phân tích keypoint/continuity | Chưa chạy test |
| V0.6 | Story graph và chuyển cảnh quy tắc | Chưa chạy test |
| V0.7 | Manifest thử nghiệm và chấm điểm nhập tay | Chưa chạy test |
| V0.8 | Gửi workflow ComfyUI cục bộ | Chưa thử model/GPU |
| V0.9 | Kiểm định MP4 qua ffprobe và SHA-256 | Chưa thử video thật |
| V1.0 | Gắn metadata clip vào scene | Chưa nghiệm thu tích hợp thật |
| V2.0 | FFmpeg nối clip theo thứ tự cảnh | Chưa thử end-to-end |

## Phát hiện và phân loại
### P0: chưa đủ điều kiện phát hành Stable
1. Chưa có bằng chứng test suite toàn bộ đạt trên commit V2.0.
2. Chưa có chạy thực nghiệm end-to-end trên máy có FFmpeg, ComfyUI và model video.
3. Không có model text-to-video mặc định; việc tạo clip AI chưa được chứng minh.

### P1: cần sửa trước khi dùng sản xuất
1. studio/api.py: guard() cho phép ghi project/scene khi STUDIO_TOKEN chưa được cấu hình; nhiều GET đọc dữ liệu dự án không yêu cầu xác thực. Chỉ dùng loopback, không mở Internet.
2. studio/assembly.py: kết quả nối video không có audio (-an), chưa có phụ đề, lời thoại hoặc chuyển cảnh; tên assembled_not_quality_checked đúng với mức xác minh hiện có.
3. studio/pipeline.py: verified_media ghi nhận MP4 do người dùng đặt vào thư mục, không chứng minh clip đến từ ComfyUI hay model nào.
4. studio/media_audit.py: ffprobe kiểm tra metadata/container, không kiểm tra mọi frame giải mã hoặc độ trung thực nhân vật.
5. studio/assembly.py: trước khi ghép chỉ đối chiếu hash, không tái chạy ffprobe trên mỗi nguồn; lỗi giải mã/codec có thể làm ffmpeg thất bại.

### P2: tăng độ tin cậy
1. Tạo kiểm thử end-to-end hai MP4 thật (FFmpeg lavfi) và xác nhận thứ tự, thời lượng, video stream, checksum.
2. Lưu provenance prompt_id, model version, seed, GPU, VRAM và workflow hash cùng từng clip.
3. Bổ sung kiểm thử xác thực API, đường dẫn symlink, file rỗng, video hỏng, clip bị thay đổi sau attach.
4. Tách job FFmpeg ra hàng đợi có timeout/cancel/log, tránh chặn request đồng bộ.
5. Bổ sung ma trận CI Windows/Linux và phát hành tag theo chuẩn semver.

## Lệnh nghiệm thu trên máy có mã nguồn
```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
ffmpeg -version
ffprobe -version
```
Sau đó tạo 2 clip MP4 thực tế, attach vào hai cảnh, gọi /assemble, xác minh file assembled bằng ffprobe và xem bằng trình phát video. Nếu có ComfyUI, thử workflow thật và ghi log model/GPU. Không ghi PASS nếu không có log.

## Quyết định
**V2.0 Alpha: chưa nghiệm thu đạt để phát hành Stable.** Mã và test hiện diện; không có bằng chứng kiểm thử runtime toàn bộ trong phiên rà soát này. Các vấn đề trên là phát hiện từ mã nguồn, không phải lỗi runtime đã tái hiện.
