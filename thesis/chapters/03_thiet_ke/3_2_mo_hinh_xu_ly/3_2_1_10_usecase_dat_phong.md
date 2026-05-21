---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.1.10"
title: "3.2.1.10 Usecase đặt phòng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

#### 3.2.1.10 Usecase đặt phòng

```plantuml
@startuml
!theme plain
left to right direction

actor "Quản trị viên (Admin)" as Admin
actor "Khách hàng (Customer)" as Customer
Admin -right-|> Customer

rectangle "Quy trình Tạo đơn đặt phòng" {
  usecase "Thực hiện giao dịch Đặt phòng" as BookingTransaction
  usecase "Đăng nhập hệ thống" as LoginSystem
  usecase "Thông báo ngày không hợp lệ" as InvalidDate
  usecase "Thông báo phòng đã hết chỗ" as FullRoomNotice
  usecase "Thông báo phòng không thuộc khách sạn" as RoomHotelNotice
  usecase "Tạo Booking mới" as CreateBooking
  usecase "Sinh mã đặt phòng (Reference Code)" as ReferenceCode
  usecase "Tính tổng giá tiền" as TotalPrice
  usecase "Kiểm tra số lượng phòng còn lại\n(Capacity Check)" as CapacityCheck
  usecase "Kiểm tra phòng trống (Availability)" as AvailabilityCheck
  usecase "Kiểm tra tính hợp lệ ngày đặt" as ValidateBookingDate
}

Customer --> BookingTransaction

CreateBooking -up-|> BookingTransaction

BookingTransaction ..> LoginSystem : <<include>>
CreateBooking ..> ValidateBookingDate : <<include>>
CreateBooking ..> AvailabilityCheck : <<include>>
CreateBooking ..> CapacityCheck : <<include>>
CreateBooking ..> TotalPrice : <<include>>
CreateBooking ..> ReferenceCode : <<include>>

InvalidDate .up.> CreateBooking : <<extend>>
FullRoomNotice .up.> CreateBooking : <<extend>>
RoomHotelNotice .up.> CreateBooking : <<extend>>
@enduml
```

> Hình 3.10: Usecase quản lý đặt phòng


Đặc tả Usecase tạo booking mới

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Tạo Booking mới |
| Actor | Khách hàng (Customer), Quản trị viên (Admin) |
| Mô tả | Người dùng thực hiện quy trình tạo một đơn đặt phòng mới, bao gồm việc chọn thời gian, kiểm tra phòng trống và xác nhận thanh toán để hệ thống ghi nhận giao dịch. |
| Pre-conditions | - Actor đã đăng nhập vào hệ thống.<br>- Actor đang ở trang chi tiết phòng hoặc giao diện đặt phòng. |
| Post-conditions | Success: Đơn đặt phòng được tạo thành công, mã đặt phòng (Reference Code) được sinh ra.<br>Fail: Hệ thống hiển thị thông báo lỗi cụ thể và không tạo đơn. |
| Luồng sự kiện chính | 1. Actor chọn ngày check-in, check-out và số lượng phòng cần đặt.<br>2. Actor nhấn nút "Đặt phòng".<br>3. Hệ thống thực hiện kiểm tra tính hợp lệ ngày đặt.<br>4. Hệ thống thực hiện kiểm tra phòng trống.<br>5. Hệ thống thực hiện kiểm tra số lượng phòng còn lại.<br>6. Hệ thống thực hiện tính tổng giá tiền.<br>7. Hệ thống thực hiện sinh mã đặt phòng.<br>8. Hệ thống lưu thông tin đơn hàng và thông báo đặt phòng thành công. |
| Luồng sự kiện phụ | - Nếu ngày check-in/check-out sai quy tắc: Hệ thống thực hiện thông báo ngày không hợp lệ.<br>- Nếu phòng không còn trống trong khoảng thời gian chọn: Hệ thống thực hiện thông báo phòng đã hết chỗ.<br>- Nếu có lỗi liên quan đến dữ liệu khách sạn: Hệ thống thực hiện thông báo phòng không thuộc khách sạn. |
| <Include Use Case><br>Quy trình Nghiệp vụ | - Kiểm tra tính hợp lệ ngày đặt: Hệ thống xác nhận ngày check-in phải trước ngày check-out và lớn hơn hoặc bằng ngày hiện tại.<br>- Kiểm tra phòng trống: Hệ thống truy vấn cơ sở dữ liệu để đảm bảo phòng chưa được đặt trong khoảng thời gian khách chọn.<br>- Kiểm tra số lượng phòng: Hệ thống xác minh sức chứa (Capacity) còn lại của loại phòng đó.<br>- Tính tổng giá tiền: Hệ thống tự động tính toán chi phí dựa trên đơn giá phòng và số ngày lưu trú.<br>- Sinh mã đặt phòng: Hệ thống tạo ra một mã tham chiếu duy nhất (Reference Code) để định danh cho đơn đặt phòng này. |
| <Extend Use Case><br>Các trường hợp ngoại lệ | Thông báo ngày không hợp lệ:<br>- Điều kiện: Khi ngày nhập vào vi phạm logic nghiệp vụ.<br>- Hành động: Hệ thống hiển thị lỗi "Ngày đặt không hợp lệ" và yêu cầu chọn lại.<br>Thông báo phòng đã hết chỗ:<br>- Điều kiện: Khi kết quả kiểm tra phòng trống trả về False.<br>- Hành động: Hệ thống báo lỗi "Phòng đã hết chỗ trong khoảng thời gian này".<br>Thông báo phòng không thuộc khách sạn:<br>- Điều kiện: Khi dữ liệu phòng và khách sạn không khớp (lỗi dữ liệu hệ thống).<br>- Hành động: Hệ thống hiển thị thông báo lỗi kỹ thuật tương ứng. |
