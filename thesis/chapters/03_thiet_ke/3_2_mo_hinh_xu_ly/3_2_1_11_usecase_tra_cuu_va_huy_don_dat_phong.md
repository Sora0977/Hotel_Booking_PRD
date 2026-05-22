---
status: draft
dependencies:
  - 3_2_1_use_case_chi_tiet.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.1.11"
title: "3.2.1.11 Usecase tra cứu và hủy đơn đặt phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

#### 3.2.1.11 Usecase tra cứu và hủy đơn đặt phòng

```plantuml
@startuml
!theme plain
left to right direction

actor "Khách hàng (Customer)" as Customer
actor "Quản trị viên (Admin)" as Admin

rectangle "Hệ thống Quản lý tra cứu và hủy đơn đặt phòng" {
  usecase "Quản lý Tra cứu/Hủy Đơn đặt phòng" as SearchCancelManage
  usecase "Đăng nhập hệ thống" as LoginSystem
  usecase "Thông báo không thể hủy\n(Đã Check-out/Đã hủy)" as CannotCancel
  usecase "Thông báo không có quyền" as PermissionError
  usecase "Tra cứu Booking theo mã" as SearchBookingCode
  usecase "Thông báo mã không tồn tại" as CodeNotFound
  usecase "Hủy đặt phòng" as CancelBooking
  usecase "Ghi nhận lý do hủy" as SaveCancelReason
  usecase "Kiểm tra trạng thái đơn hàng" as CheckOrderStatus
  usecase "Kiểm tra quyền sở hữu đơn\n(User/Admin Check)" as CheckOrderOwner
}

Customer --> SearchCancelManage
Admin --> SearchCancelManage

SearchBookingCode -up-|> SearchCancelManage
CancelBooking -up-|> SearchCancelManage

SearchCancelManage ..> LoginSystem : <<include>>
CancelBooking ..> CheckOrderOwner : <<include>>
CancelBooking ..> CheckOrderStatus : <<include>>
CancelBooking ..> SaveCancelReason : <<include>>

CannotCancel .up.> CancelBooking : <<extend>>
PermissionError .up.> CancelBooking : <<extend>>
CodeNotFound .up.> SearchBookingCode : <<extend>>
@enduml
```

> Hình 3.11: Usecase tra cứu và hủy đơn đặt phòng


Đặc tả Usecase tra cứu Booking theo mã

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Tra cứu Booking theo mã |
| Actor | Khách hàng (Customer), Quản trị viên (Admin) |
| Mô tả | Người dùng tìm kiếm và xem chi tiết thông tin của một đơn đặt phòng cụ thể dựa trên mã đặt phòng (Reference Code) đã được cấp trước đó. |
| Pre-conditions | - Actor đã đăng nhập vào hệ thống.<br>- Actor có mã đặt phòng cần tra cứu. |
| Post-conditions | Success: Hệ thống hiển thị đầy đủ thông tin chi tiết của đơn đặt phòng.<br>Fail: Hệ thống thông báo không tìm thấy đơn hàng. |
| Luồng sự kiện chính | 1. Actor truy cập trang tra cứu.<br>2. Actor nhập mã đặt phòng (Reference Code).<br>3. Actor nhấn nút "Tìm kiếm".<br>4. Hệ thống thực hiện truy vấn đơn hàng trong cơ sở dữ liệu.<br>5. Nếu mã hợp lệ, hệ thống hiển thị thông tin chi tiết của Booking.<br>6. Hệ thống thực hiện kiểm tra quyền truy cập (ẩn danh tính nếu không phải chủ sở hữu - tùy nghiệp vụ). |
| Luồng sự kiện phụ | - Nếu mã đặt phòng không tồn tại trong hệ thống: Hệ thống thực hiện thông báo mã không tồn tại. |
| <Include Use Case><br>Quy trình Nghiệp vụ | - Đăng nhập: (Kế thừa từ Parent) Đảm bảo người dùng đã xác thực danh tính trước khi thực hiện tra cứu. |
| <Extend Use Case><br>Thông báo mã không tồn tại | Điều kiện: Khi kết quả truy vấn cơ sở dữ liệu trả về rỗng.<br>Hành động:<br>- Hệ thống hiển thị thông báo: "Mã đặt phòng không tồn tại".<br>- Hệ thống yêu cầu người dùng kiểm tra và nhập lại. |

Đặc tả Usecase hủy đặt phòng

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Hủy đặt phòng (Cancel Booking) |
| Actor | Khách hàng (Customer), Quản trị viên (Admin) |
| Mô tả | Người dùng thực hiện hủy một đơn đặt phòng đã đặt. Hệ thống cần kiểm tra các điều kiện về quyền hạn và trạng thái đơn hàng trước khi cho phép hủy. |
| Pre-conditions | - Actor đã đăng nhập.<br>- Đơn đặt phòng đã được tìm thấy và đang hiển thị chi tiết.<br>- Đơn hàng chưa Check-out hoặc chưa bị hủy trước đó. |
| Post-conditions | Success: Trạng thái đơn hàng chuyển sang "Cancelled", lý do hủy được ghi nhận.<br>Fail: Hệ thống báo lỗi và giữ nguyên trạng thái đơn hàng. |
| Luồng sự kiện chính | 1. Actor nhấn nút "Hủy đặt phòng" trên giao diện chi tiết đơn hàng.<br>2. Actor nhập lý do hủy (tùy chọn hoặc bắt buộc).<br>3. Actor xác nhận hành động hủy.<br>4. Hệ thống thực hiện kiểm tra quyền sở hữu đơn.<br>5. Hệ thống thực hiện kiểm tra trạng thái đơn hàng.<br>6. Nếu hợp lệ, hệ thống thực hiện ghi nhận lý do hủy.<br>7. Hệ thống cập nhật trạng thái đơn hàng thành "Đã hủy" và thông báo thành công. |
| Luồng sự kiện phụ | - Nếu đơn hàng đã hoàn thành hoặc đã hủy trước đó: Hệ thống thực hiện thông báo không thể hủy.<br>- Nếu Actor cố tình hủy đơn hàng không phải của mình (và không phải Admin): Hệ thống thực hiện thông báo không có quyền. |
| <Include Use Case><br>Quy trình Kiểm tra & Xử lý | - Kiểm tra quyền sở hữu: Hệ thống đối chiếu ID người dùng hiện tại với ID người đặt của đơn hàng (hoặc check quyền Admin).<br>- Kiểm tra trạng thái: Hệ thống đảm bảo đơn hàng đang ở trạng thái cho phép hủy (ví dụ: "Confirmed" hoặc "Pending").<br>- Ghi nhận lý do: Hệ thống lưu trữ lý do hủy vào lịch sử đơn hàng để phục vụ thống kê hoặc CSKH. |
| <Extend Use Case><br>Thông báo không thể hủy | Điều kiện: Khi đơn hàng đang ở trạng thái Checked-out hoặc Cancelled.<br>Hành động:<br>- Hệ thống hiển thị lỗi: "Đơn hàng này không thể hủy vì đã hoàn tất hoặc đã bị hủy". |
| <Extend Use Case><br>Thông báo không có quyền | Điều kiện: Khi quy trình kiểm tra quyền sở hữu thất bại.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo bảo mật: "Bạn không có quyền thao tác trên đơn hàng này". |
