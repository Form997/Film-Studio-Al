# Kết quả chạy thử V0.1–V2.0 — 27/10/2026

## Kết quả đã thực sự quan sát
- Thử `git clone --depth 1 https://github.com/Form997/Film-Studio-Al.git` trong môi trường thực thi: **FAIL (môi trường mạng)**. Lỗi: `Could not resolve host: github.com`. Không thể tải repo để chạy pytest cục bộ.
- Kiểm tra `https://github.com` và `https://api.github.com` bằng requests: **FAIL (môi trường mạng)** do DNS/name resolution.
- Qua GitHub connector: đã ghi thành công bài test `tests/test_e2e_real_mp4.py` và cập nhật workflow `.github/workflows/test.yml` để chạy `pytest -ra -q`, tạo JUnit XML và upload artifact dù test thất bại.
- Kiểm tra trạng thái commit workflow `064f1230664ce2d5420175b466b358a1717d6914`: combined statuses trả về mảng rỗng; truy vấn workflow runs liên kết commit cũng trả về mảng rỗng (API hiện chỉ tìm runs kiểu pull request). **Không được suy diễn PASS/FAIL từ mảng rỗng.**

## Kết quả kiểm thử ứng dụng
- Tổng số pytest thực sự chạy trong môi trường này: **0**.
- PASS/FAIL/SKIP của pytest: **CHƯA CÓ LOG**.
- Kiểm thử MP4 thật: **ĐÃ TẠO MÃ TEST**, **CHƯA XÁC NHẬN ĐÃ CHẠY**.
- Kiểm thử GPU/ComfyUI/model video: **CHƯA CHẠY**.
- Trạng thái nghiệm thu: **BLOCKED — chưa đủ bằng chứng runtime**.

## Cách lấy bằng chứng từ GitHub Actions
Mở https://github.com/Form997/Film-Studio-Al/actions , chọn workflow **Test Studio and Save Evidence** ở commit mới nhất, mở run, kiểm tra bước `Run full test suite and real MP4 E2E`. Tải artifact `studio-v01-v20-test-evidence` để xem `pytest.log`, `pytest.xml`, `environment.txt`. Artifact giữ 30 ngày.

Lưu ý: đây là báo cáo trung thực của các lệnh đã thực hiện và trạng thái có thể xác minh. Không có kết quả chạy pytest thành công nào được giả định.

## THỬ LẠI: Kết quả thực thi kiểm thử trên bản lưu trữ (27/10/2026)

### Dữ liệu thực tế
- Trên container Linux với Python 3.13.5, pytest 9.0.2, FFmpeg 7.1.5.
- Bản ZIP lưu trữ V0.1 (`hai-dat-ai-film-studio-v0.1.zip`): chạy `python -m pytest -q --junitxml=...`; **6 passed, 0 failed**, exit code 0, 0.85 giây.
- Bản ZIP lưu trữ V0.2 (`hai-dat-ai-film-studio-v0.2-self-coded.zip`): chạy cùng lệnh; **12 passed, 0 failed**, exit code 0, 0.77 giây. Trong bộ V0.2 có bài kiểm thử API export video thẻ tiêu đề với FFmpeg.
- Thử độc lập FFmpeg CLI tạo hai video MP4 đỏ/xanh 320x240, nối thành một MP4 2 giây; dùng ffprobe xác minh có luồng video. **PASS**, SHA-256 file nối `5ea89fd2b1bb3b1f2a73df40cb0d969cd594edfa980463feb0c2008bcd7be507`. Đây **không phải** chạy code `studio/assembly.py` V2.0.
- Lệnh `git ls-remote https://github.com/Form997/Film-Studio-Al.git HEAD` vẫn **FAIL**: `Could not resolve host: github.com`.
- **Chưa chạy pytest trên snapshot GitHub V2.0**; cũng chưa thử ComfyUI/GPU/model AI.

### Giới hạn suy luận
Hai bản ZIP V0.1, V0.2 là bản lưu trữ có sẵn trong môi trường và không được chứng minh tương ứng bit-for-bit với commit GitHub của các phiên bản tương ứng. Do đó 18 lượt test PASS chỉ áp dụng cho hai ZIP đã chạy, **không phải** xác nhận toàn repo từ V0.1 tới V2.0 đạt.

Bằng chứng gồm `v01.log`, `v02.log`, `v01-results.xml`, `v02-results.xml`, `mp4-smoke/result.json`, được tạo và nén thành ZIP trong phiên chạy thử này. Xem artifact từ phiên làm việc để tải.
