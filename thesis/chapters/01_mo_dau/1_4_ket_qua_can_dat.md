---
status: imported_chunk
last_updated: 2026-05-21
chapter: "01 - Giới thiệu"
chunk: "1.4"
source_file: "../01_mo_dau.md"
related_memory: ../../THESIS_MEMORY.md
school_rules: ../../SCHOOL_RULES.md
---
<!-- Mảnh file được tạo từ 01_mo_dau.md. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này, không chỉnh file chương gốc. -->

## 1.4 Kết quả cần đạt

Kết quả chức năng:

| Chức năng | Tiêu chí đánh giá hoàn thành |
| --- | --- |
| Quản lý tài khoản (Quản trị viên) | Quản trị viên thêm/xóa/sửa/khóa/mở khóa tài khoản. |
| Quản lý khách sạn (Quản trị viên) | Quản trị viên thêm/xóa khách sạn. |
| Quản lý phòng khách sạn | Quản trị viên thêm/sửa/xóa phòng khách sạn. |
| Quản lý tiện nghi | Quản trị viên thêm/xóa/sửa tiện nghi cấp khách sạn/phòng. |
| Đăng ký tài khoản | Người dùng đăng ký tài khoản thành công. |
| Đăng nhập tài khoản | Người dùng đăng nhập tài khoản thành công. |
| Quên mật khẩu | Người dùng có thể lấy lại mật khẩu khi quên mật khẩu. |
| Quản lý thông tin cá nhân | Người dùng xem, sửa thông tin tài khoản cá nhân. |
| Tìm kiếm khách sạn | Hệ thống trả kết quả phù hợp với các tiêu chí mà người dùng chọn. |
| Đặt phòng | Người dùng có thể đặt phòng |
| Xem lịch sử đặt phòng | Người dùng có thể xem chi tiết thông tin phòng đặt phòng. |
| Hủy đặt phòng | Cho phép người dùng hủy phòng đã đặt theo chính sách. |
| Thống kê doanh thu | Thống kê doanh thu của khách sạn theo tháng/năm/quý |

Kết quả phi chức năng:

| Chức năng | Tiêu chí đánh giá hoàn thành |
| --- | --- |
| Thời gian phản hồi tìm kiếm | Hệ thống trả về kết quả tìm kiếm khách sạn không được vượt quá 3 giây. |
| Thời gian tải trang | Thời gian tải các trang chính (trang chủ, trang chi tiết khách sạn) không được vượt quá 2 giây. |
| Xử lý thanh toán | Thời gian xác nhận giao dịch (sau khi người dùng gửi thông tin thanh toán qua ví điện tử) không được vượt quá 5-7 giây. |
| Mã hóa mật khẩu | Tất cả mật khẩu người dùng phải được lưu trữ trong cơ sở dữ liệu dưới dạng băm (hashed). |
| Phân quyền | Hệ thống phải đảm bảo phân quyền nghiêm ngặt. |
| Bảo mật thanh toán | Mọi giao dịch thanh toán trực tuyến (qua ví điện tử) phải được thực hiện qua kết nối an toàn (HTTPS) và tuân thủ các tiêu chuẩn bảo mật. |
| Giao thức truyền tải | Toàn bộ hệ thống phải được truy cập qua giao thức HTTPS (SSL/TLS) để mã hóa dữ liệu truyền tải. |
| Xác thực API | Các API (nếu có) phải được bảo vệ bằng cơ chế xác thực (ví dụ: JWT, OAuth 2.0). |
| Bảo trì | Thời gian bảo trì hệ thống (nếu có) phải được lên kế hoạch và thực hiện ngoài giờ cao điểm và phải có thông báo trước cho người dùng. |
| Thiết kế đáp ứng - Responsive | Giao diện người dùng phải tương thích và hiển thị tốt trên các thiết bị phổ biến, bao gồm máy tính để bàn, máy tính bảng và điện thoại di động. |
| Tính module | Hệ thống nên được thiết kế theo kiến trúc module (ví dụ: Microservices hoặc module hóa) để dễ dàng nâng cấp, sửa lỗi và phát triển các tính năng mới. |
