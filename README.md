# 🎬 HAI ĐẤT AI FILM STUDIO

Nền tảng **tự viết mã nguồn** hỗ trợ người Việt sản xuất phim AI. Trọng tâm: kiểm soát dự án, kịch bản, phân cảnh, hồ sơ nhân vật, nguồn tư liệu, xuất phim, và kết nối các mô hình AI bằng adapter có thể thay thế.

**Trạng thái: V0.2 Alpha.** Không tuyên bố tạo phim AI hoàn chỉnh nếu chưa cấu hình mô hình và GPU.

## Mục tiêu

- Giao diện và tài liệu tiếng Việt.
- Toàn bộ mã điều phối/ứng dụng tự phát triển, không trộn repository bên ngoài.
- Kịch bản → phân cảnh → nhân vật → kiểm tra nhất quán → tài sản → dựng phim.
- Sử dụng FFmpeg và ComfyUI như dịch vụ ngoài tùy chọn; giấy phép mô hình được kiểm tra riêng.
- Mỗi thành phần có thể kiểm thử, thay thế hoặc nâng cấp độc lập.

## Cài đặt (bản nguồn V0.2)

Xem mã nguồn và hướng dẫn cài đặt trong các thư mục `studio/`, `web/`, `tests/`, `docs/` sau khi được đồng bộ. Máy chạy Python 3.11 và FFmpeg; sinh video AI còn cần ComfyUI/model tương thích.

**Kho:** https://github.com/Form997/Film-Studio-Al
**Chủ dự án:** Form997.
**Giấy phép nguồn tự viết:** MIT (không áp dụng mặc nhiên cho mô hình, trọng số, hay tài sản bên ngoài).
