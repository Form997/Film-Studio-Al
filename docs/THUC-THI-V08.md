# V0.8 — Thực thi thử nghiệm ComfyUI cục bộ

## Phạm vi thực hiện
Mã điều phối và kiểm định workflow do HAI ĐẤT AI tự viết, không sao chép code model. Tích hợp ComfyUI qua HTTP loopback đã có từ V0.2. Chỉ gửi workflow khi người dùng chủ động gọi API. Không tự tải model, không tự chạy nền.

## Cách dùng
1. Cài ComfyUI và một mô hình video tương thích riêng, kiểm tra license weights.
2. Chạy ComfyUI trên 127.0.0.1:8188.
3. Chuẩn bị workflow API-format có class_type và inputs ở từng node; workflow phải tương thích node đã cài.
4. POST /api/experiments/submit-local với JSON {"project_id":"p","scene_id":"s","workflow":{"1":{"class_type":"...","inputs":{...}}},"model_label":"..."}.
5. GET /api/experiments/local-status/{prompt_id} để xem history.
6. Ghi lại GPU, VRAM, model version, seed, thời gian xử lý và đầu ra khi nghiệm thu thực tế.

## An toàn
API submit-local yêu cầu STUDIO_TOKEN được cấu hình. Khi chưa đặt token, endpoint từ chối. ComfyUI chỉ kết nối loopback. Không đưa máy chủ công khai lên Internet. Workflow tùy ý có thể thực thi custom node đã cài: chỉ dùng workflow tin cậy.

## Giới hạn
V0.8 có thể gửi workflow cho ComfyUI cục bộ nhưng chưa có workflow Wan/Hunyuan sẵn, chưa có GPU runner riêng, chưa tải hoặc kiểm tra media đầu ra. Trạng thái submitted_not_completed không đồng nghĩa video đã sinh. Không công bố kết quả video thật nếu chưa thử nghiệm.
