# V0.7 — Giao thức thực nghiệm sinh video có thể tái lập

## Nguyên tắc
Nghiên cứu thuật toán của cộng đồng quốc tế nhưng tự viết mã điều phối và đánh giá. Không sao chép nguyên mã nguồn hoặc tự nhận đã huấn luyện mô hình.

## Quy trình
1. Kiểm định dự án và tạo shot prompts qua film_brain.
2. Sinh manifest thử nghiệm với nhiều seed xác định (mặc định 11, 23, 37).
3. Ghi hash SHA-256 cho từng request và toàn bộ protocol để có thể đối chiếu.
4. Khi có engine được kết nối và thực sự tạo video, người đánh giá xem video và nhập bốn điểm [0,5]: identity consistency, motion smoothness, prompt alignment, visual quality.
5. Tổng hợp điểm trung bình và số mẫu, không gán điểm khi chưa có quan sát.

## API
- GET /api/projects/{id}/experiment-plan?language=vi&aspect=landscape
- POST /api/experiments/evaluate với JSON {"observations":[{"request_sha256":"64 ký tự hex", "scores":{"identity_consistency":4,"motion_smoothness":3,"prompt_alignment":5,"visual_quality":4}}]}
- API POST yêu cầu STUDIO_TOKEN nếu đã cấu hình.

## Giới hạn
V0.7 chưa chạy text-to-video, chưa có GPU runner, chưa đo video tự động. Đây là nền tảng kiểm thử và đo lường, không phải kết quả thực nghiệm chất lượng mô hình. Để kiểm định mô hình thực tế cần log phần cứng, version weights, thời gian chạy, bộ dữ liệu được phép dùng và người đánh giá độc lập.

## Nguồn nghiên cứu
- Wan2.2: https://github.com/Wan-Video/Wan2.2
- HunyuanVideo: https://github.com/Tencent-Hunyuan/HunyuanVideo
- LTX: https://github.com/Lightricks/LTX-2
- ComfyUI: https://github.com/Comfy-Org/ComfyUI
- VBench: https://github.com/Vchitect/VBench
- OpenTimelineIO: https://github.com/AcademySoftwareFoundation/OpenTimelineIO

Không sao chép mã; kiểm tra giấy phép riêng của weights, dữ liệu và thư viện trước tích hợp.
