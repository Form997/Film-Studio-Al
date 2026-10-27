# V0.6 — Đạo diễn thông minh dựa trên quy tắc có thể giải thích

## Kiến trúc
Tách planner trong studio/story_engine.py khỏi bộ máy sinh video. Đầu vào là project đã kiểm định theo schema V0.4. Đầu ra gồm nodes (phân cảnh), edges (chuyển cảnh), đề xuất góc máy, thời lượng, nhân vật xuất hiện/rời cảnh và dấu hash SHA-256.

## Nguyên lý tự viết
- Phân loại cảnh theo từ khóa và trọng số đơn giản cho establish/detail/action/dialogue/neutral.
- Đề xuất góc máy từ nhãn cảnh. Mọi quyết định có thể truy vết bằng kind.
- Chuyển cảnh: mặc định cut; hai cảnh establish liền nhau có thể dùng dissolve.
- Scene graph: cạnh nối các cảnh kề nhau, không suy luận quan hệ nhân quả.
- Không dịch nội dung kịch bản; từ điển vi/en/zh được xây dựng thủ công.
- Kết quả xác định với cùng dữ liệu đầu vào; dùng hash để đối chiếu.

## Giới hạn
Đây là heuristic planner, không phải LLM, không hiểu ngữ nghĩa sâu, không tự dựng video, không đảm bảo mạch truyện điện ảnh. Cần dữ liệu kịch bản có nhãn và đánh giá chuyên gia để học thuật toán phân cảnh nâng cao.

## Nguồn nghiên cứu thuật toán và kiến trúc
- OpenTimelineIO: https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- MoviePy: https://github.com/Zulko/moviepy
- PySceneDetect: https://github.com/Breakthrough/PySceneDetect
- MMPose (English/中文): https://github.com/open-mmlab/mmpose
- Wan2.2: https://github.com/Wan-Video/Wan2.2

Không sao chép mã nguồn từ các kho tham khảo. Kiểm tra giấy phép riêng cho code, model và dữ liệu.

## Kiểm thử
Chạy python -m pytest -q. Kiểm tra phân loại vi/en/zh, số nút/cạnh, tổng thời lượng, thay đổi nhân vật, hash ổn định và đầu vào không hợp lệ.
