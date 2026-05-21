# CHƯƠNG 1. GIỚI THIỆU

## 1.1 ĐẶT VẤN ĐỀ, MỤC TIÊU LUẬN VĂN

### 1.1.1 Đặt vấn đề

Trong bối cảnh ngành du lịch và dịch vụ lưu trú đang phát triển mạnh mẽ, nhu cầu tìm kiếm, đặt phòng và thanh toán trực tuyến ngày càng trở nên phổ biến. Tuy nhiên, nhiều khách hàng vẫn gặp khó khăn khi tìm kiếm khách sạn phù hợp, so sánh giá, kiểm tra phòng trống, hoặc thực hiện thanh toán an toàn.

Mặt khác, các doanh nghiệp khách sạn nhỏ lẻ lại thiếu nền tảng số để quản lý thông tin phòng, đặt chỗ, hoặc thống kê doanh thu một cách hiệu quả.

Từ những bất cập đó, nhóm tiến hành xây dựng Hệ thống đặt phòng khách sạn trực tuyến (Hotel Booking System) với mục tiêu tối ưu trải nghiệm cho khách hàng, đồng thời hỗ trợ các doanh nghiệp quản lý hoạt động kinh doanh hiệu quả hơn.

### 1.1.2 Mục tiêu luận văn

Xây dựng một hệ thống web cho phép khách hàng tìm kiếm, đặt phòng trực tuyến.

Phát triển giao diện thân thiện, dễ sử dụng và tương thích đa thiết bị.

Cung cấp công cụ quản lý cho Admin quản lý khách sạn, đặt phòng, tài khoản và báo cáo doanh thu.

Đảm bảo hệ thống đạt các tiêu chí về hiệu suất, bảo mật, và khả năng mở rộng trong tương lai.

## 1.2 NHỮNG THÁCH THỨC CẦN GIẢI QUYẾT

Quản lý dữ liệu phức tạp: Dữ liệu liên quan đến nhiều bảng (khách sạn, phòng, đặt phòng, hủy phòng, đánh giá). Việc đảm bảo tính toàn vẹn và hiệu suất truy vấn là một thách thức.

Tìm kiếm và lọc dữ liệu: Cần tối ưu truy vấn để đảm bảo kết quả tìm kiếm trả về nhanh (≤ 3 giây) khi có nhiều tiêu chí tìm kiếm đồng thời.

Quản lý phân quyền người dùng: Cần xây dựng cơ chế phân quyền rõ ràng cho ba vai trò: Khách hàng, Quản trị viên.

Tính thân thiện với người dùng: Thiết kế giao diện trực quan dễ sử dụng, trải nghiệm nhất quán trên cả desktop, tablet và mobile.

Tối ưu hóa tìm kiếm khách sạn : Xử lý truy vấn phức tạp với khối lượng dữ liệu lớn trong thời gian thực, đòi hỏi thiết kế cơ sở dữ liệu hiệu quả và thuật toán tìm kiếm tối ưu.

Đồng bộ dữ liệu tồn kho : Quản lý số lượng phòng trống để tránh tình trạng đặt trùng phòng (overbooking), yêu cầu cơ chế khóa giao dịch.

## 1.3 NỘI DUNG, PHẠM VI THỰC HIỆN

### 1.3.1 Nội dung thực hiện

Phân tích và thiết kế hệ thống:

Xác định yêu cầu chức năng và phi chức năng.

Thiết kế cơ sở dữ liệu, sơ đồ use case, sơ đồ hoạt động và kiến trúc hệ thống.

Xây dựng hệ thống (Develop):

Giao diện người dùng (Frontend): xây dựng bằng ReactJS hoặc tương tự.

Backend: phát triển API bắng Spring boot, kết nối với cơ sở dữ liệu MySQL.

Kiểm thử và đánh giá hệ thống:

Kiểm thử chức năng: đăng ký, tìm kiếm, đặt phòng, thanh toán, quản lý tài khoản, quản lý khách sạn, quản lý phòng, quản lý tiện nghi.

Kiểm thử phi chức năng: hiệu suất, bảo mật, tính tương thích trình duyệt và thiết bị.

### 1.3.1 Phạm vi thực hiện

Đối tượng sử dụng: Khách hàng, Quản trị viên.

Phạm vi kỹ thuật:

Hệ thống web (chưa phát triển ứng dụng di động).

Sử dụng cơ sở dữ liệu quan hệ MySQL.

Tích hợp thanh toán ở mức mô phỏng hoặc sandbox (chưa triển khai thực tế).

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
