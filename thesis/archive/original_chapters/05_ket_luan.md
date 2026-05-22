---
status: imported
last_updated: 2026-05-21
chapter: "05 - Kết luận"
related_memory: THESIS_MEMORY.md
school_rules: ../SCHOOL_RULES.md
source_chapters:
  - "Hotel booking service/Thesis-report/chapters/chuong-4-ket-luan.md"
---

# Chương 5 — Kết luận

<!-- Chương này được tái cấu trúc theo Rules.md của trường: 5.1 đối chiếu mục tiêu, 5.2 vấn đề tồn đọng, 5.3 mở rộng/hướng phát triển. -->

## 5.1 Kết quả đối chiếu với mục tiêu

Luận văn đã xây dựng và đánh giá hệ thống đặt phòng khách sạn trực tuyến với các chức năng chính như quản lý tài khoản, quản lý khách sạn, quản lý phòng, quản lý tiện nghi, đăng ký, đăng nhập, tìm kiếm khách sạn, đặt phòng, xem lịch sử đặt phòng và hủy đặt phòng. Một số chức năng và yêu cầu phi chức năng vẫn cần được hoàn thiện thêm, đặc biệt là quên mật khẩu, thống kê doanh thu, xử lý thanh toán thực tế và triển khai HTTPS.

Kết quả mục tiêu chức năng:

| Chức năng | Tiêu chí đánh giá hoàn thành | Kết quả | Ghi chú |
| --- | --- | --- | --- |
| Quản lý tài khoản (Quản trị viên) | Quản trị viên thêm/xóa/sửa/khóa/mở khóa tài khoản. | Đạt | CRUD, quản lý trạng thái |
| Quản lý khách sạn (Quản trị viên) | Quản trị viên thêm/xóa khách sạn. | Đạt | CRUD, upload ảnh lên Cloudinary |
| Quản lý phòng khách sạn | Quản trị viên thêm/sửa/xóa phòng khách sạn. | Đạt | CRUD, upload ảnh lên Cloudinary |
| Quản lý tiện nghi | Quản trị viên thêm/xóa/sửa tiện nghi cấp khách sạn/phòng. | Đạt | CRUD |
| Đăng ký tài khoản | Người dùng đăng ký tài khoản thành công. | Đạt | Validate chưa chặt chẽ nhưng về cơ bản đã hoàn thành |
| Đăng nhập tài khoản | Người dùng đăng nhập tài khoản thành công. | Đạt | Thành công |
| Quên mật khẩu | Người dùng có thể lấy lại mật khẩu khi quên mật khẩu. | Không đạt | Gặp khó khăn trong quá trình thực hiện |
| Quản lý thông tin cá nhân | Người dùng xem, sửa thông tin tài khoản cá nhân. | Đạt | Xem, cập nhật thông tin thành công |
| Tìm kiếm khách sạn | Hệ thống trả kết quả phù hợp với các tiêu chí mà người dùng chọn. | Đạt | Tìm/lọc đúng khách sạn theo yêu cầu |
| Đặt phòng | Người dùng có thể đặt phòng. | Đạt | Đặt phòng thành công |
| Xem lịch sử đặt phòng | Người dùng có thể xem chi tiết thông tin phòng đặt phòng. | Đạt | Xem được tất cả đặt phòng |
| Hủy đặt phòng | Cho phép người dùng hủy phòng đã đặt theo chính sách. | Đạt | Hủy đặt phòng và điền lý do hủy |
| Thống kê doanh thu | Thống kê doanh thu của khách sạn theo tháng/năm/quý. | Không đạt | Gặp khó khăn trong quá trình thực hiện |

Kết quả mục tiêu phi chức năng:

| Chức năng | Tiêu chí đánh giá hoàn thành | Kết quả | Ghi chú |
| --- | --- | --- | --- |
| Thời gian phản hồi tìm kiếm | Hệ thống trả về kết quả tìm kiếm khách sạn không được vượt quá 3 giây. | Đạt |  |
| Thời gian tải trang | Thời gian tải các trang chính (trang chủ, trang chi tiết khách sạn) không được vượt quá 2 giây. | Đạt |  |
| Xử lý thanh toán | Thời gian xác nhận giao dịch sau khi người dùng gửi thông tin thanh toán qua ví điện tử không được vượt quá 5-7 giây. | Không đạt | Gặp khó khăn trong quá trình triển khai thanh toán |
| Mã hóa mật khẩu | Tất cả mật khẩu người dùng phải được lưu trữ trong cơ sở dữ liệu dưới dạng băm (hashed). | Đạt |  |
| Phân quyền | Hệ thống phải đảm bảo phân quyền nghiêm ngặt. | Đạt |  |
| Bảo mật thanh toán | Mọi giao dịch thanh toán trực tuyến qua ví điện tử phải được thực hiện qua kết nối an toàn (HTTPS) và tuân thủ các tiêu chuẩn bảo mật. | Đạt | Gặp khó khăn trong việc triển khai thanh toán |
| Giao thức truyền tải | Toàn bộ hệ thống phải được truy cập qua giao thức HTTPS (SSL/TLS) để mã hóa dữ liệu truyền tải. | Không đạt | Hiện tại website vẫn chưa truy cập qua giao thức HTTPS |
| Xác thực API | Các API phải được bảo vệ bằng cơ chế xác thực, ví dụ JWT hoặc OAuth 2.0. | Đạt |  |
| Bảo trì | Thời gian bảo trì hệ thống phải được lên kế hoạch và thực hiện ngoài giờ cao điểm, đồng thời có thông báo trước cho người dùng. | Đạt |  |
| Thiết kế đáp ứng - Responsive | Giao diện người dùng phải tương thích và hiển thị tốt trên các thiết bị phổ biến, bao gồm máy tính để bàn, máy tính bảng và điện thoại di động. | Đạt |  |
| Tính module | Hệ thống nên được thiết kế theo kiến trúc module để dễ dàng nâng cấp, sửa lỗi và phát triển các tính năng mới. | Đạt |  |

## 5.2 Các vấn đề còn tồn đọng

Thanh toán chưa thực tế: Như đã đề cập trong phạm vi thực hiện, chức năng thanh toán hiện tại mới chỉ tích hợp ở mức mô phỏng hoặc xác nhận thủ công, chưa kết nối trực tiếp với các cổng thanh toán ngân hàng thực tế như VNPAY hoặc MoMo để xử lý dòng tiền thật.

Hệ thống gợi ý: Chức năng tìm kiếm hiện tại hoạt động dựa trên bộ lọc cứng như địa điểm, ngày tháng và giá. Hệ thống chưa có khả năng gợi ý khách sạn dựa trên thói quen, lịch sử đặt phòng của người dùng hoặc sử dụng AI để cá nhân hóa trải nghiệm.

Hạn chế về điều hướng: Hệ thống hiện tại chưa tích hợp thanh điều hướng (breadcrumb). Điều này khiến người dùng khó nhận biết vị trí hiện tại của mình trong cấu trúc website và gặp bất tiện khi muốn quay lại các trang cấp cha hoặc danh mục trước đó.

## 5.3 Mở rộng (Hướng phát triển)

Nâng cấp thuật toán tìm kiếm và gợi ý: Tích hợp Machine Learning để phân tích dữ liệu người dùng, từ đó đưa ra các gợi ý khách sạn phù hợp hơn, góp phần nâng cao trải nghiệm cá nhân hóa và tăng tỷ lệ chuyển đổi đơn hàng.

Mở rộng hệ thống đặt vé: Bổ sung thêm các dịch vụ đi kèm như đặt vé máy bay, xe đưa đón sân bay hoặc tour du lịch để hệ thống trở nên toàn diện hơn.

Tối ưu hóa quy trình vận hành cho đối tác: Xây dựng một trang Extranet riêng biệt và chuyên nghiệp hơn cho các chủ khách sạn, cho phép họ tự quản lý khuyến mãi, flash sale và tương tác trực tiếp với đánh giá của khách hàng.
