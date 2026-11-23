# HOA PHƯỢNG AI ASSISTANT – phiên bản demo 1.0

Đơn vị đề xuất: PGD Hoa Phượng – VietinBank Chi nhánh Lê Chân.

## Khởi chạy trên máy tính
1. Cài Python 3.10 trở lên.
2. Mở Terminal tại thư mục này.
3. Chạy `python -m pip install -r requirements.txt`.
4. Chạy `python -m streamlit run app.py`.
5. Mở đường dẫn localhost do Streamlit hiển thị.

## Hai chế độ
- **Không có API:** phân tích bảng tính, biểu đồ, tra cứu từ khóa, soạn văn bản mẫu, danh sách công việc. Chatbot chỉ hiển thị phản hồi mô phỏng có nhãn rõ ràng.
- **Có API được phép:** nhập API key vào sidebar hoặc biến môi trường `OPENAI_API_KEY`. Khi đó có thể hỏi đáp linh hoạt, tóm tắt tài liệu, tạo nhận xét và bản nháp qua mô hình AI. API có thể phát sinh phí.

## Tạo link demo công khai
1. Đưa `app.py`, `requirements.txt` lên repository GitHub **chỉ chứa mã nguồn và dữ liệu giả lập**.
2. Nếu quy định cuộc thi và chính sách VietinBank cho phép, đăng nhập Streamlit Community Cloud, tạo app mới từ repository, chọn `app.py`.
3. Sau khi triển khai, thử link trên cửa sổ ẩn danh và điện thoại. Sao chép URL vào trường Đường dẫn của hồ sơ dự thi.
4. Không đưa API key vào repository. Cấu hình bằng secrets của dịch vụ triển khai nếu được phép.

**Lưu ý:** ChatGPT không thể tự tạo đường dẫn triển khai trong tài khoản của bạn. URL chỉ xuất hiện sau khi bạn triển khai thành công. Không tải dữ liệu ngân hàng thật hoặc tài liệu nội bộ lên nền tảng công khai khi chưa được phê duyệt.

## Kịch bản trình diễn 3 phút
1. Mở trang tổng quan và giải thích hai chế độ (20 giây).
2. Mở Báo cáo Excel, xem biểu đồ từ dữ liệu giả lập, tải báo cáo TXT (60 giây).
3. Mở Soạn văn bản, tạo email nhắc tiến độ (40 giây).
4. Mở Tra cứu tài liệu, tìm từ khóa 'quy trình' (30 giây).
5. Mở Công việc, thêm nhiệm vụ, xuất CSV (30 giây).

## Giới hạn hiện tại
- Chưa có đường dẫn public; cần triển khai riêng.
- Không có AI thật khi chưa có API.
- Tra cứu tài liệu không có trích dẫn trang; chỉ dò từ khóa.
- Dữ liệu công việc chỉ lưu trong phiên; không có đăng nhập và phân quyền.
- Chưa tích hợp hệ thống VietinBank; không dùng cho nghiệp vụ thực tế.
