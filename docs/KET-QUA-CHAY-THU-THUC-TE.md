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
