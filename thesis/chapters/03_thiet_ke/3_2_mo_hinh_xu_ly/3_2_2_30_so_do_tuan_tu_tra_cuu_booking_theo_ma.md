---
status: draft
dependencies:
  - 3_2_1_11_usecase_tra_cuu_va_huy_don_dat_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.30"
title: "Sơ đồ tuần tự tra cứu booking theo mã"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.42: Sơ đồ tuần tự tra cứu booking theo mã


- Sơ đồ tuần tự hủy đặt phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Hủy đặt phòng

actor "Customer/Admin" as User
boundary BookingDetailView
control BookingService
entity BookingDB

User -> BookingDetailView: 1 Nhấn nút "Hủy đặt phòng"
BookingDetailView --> User: 2 Hiển thị hộp thoại nhập lý do hủy
User -> BookingDetailView: 3 Nhập lý do & Nhấn "Xác nhận hủy"
BookingDetailView -> BookingService: 4 Gửi yêu cầu hủy(bookingId, reason)
BookingService -> BookingDB: 5 Lấy thông tin Booking từ DB
BookingDB --> BookingService: 6 Trả về dữ liệu Booking
BookingService -> BookingService: 7 Kiểm tra quyền sở hữu (User vs Booking Owner)

alt [Không có quyền (Unauthorized)]
    BookingService --> BookingDetailView: 8 Trả về lỗi "Bạn không có quyền thao tác trên đơn hàng này"
    BookingDetailView --> User: 9 Hiển thị cảnh báo bảo mật
else [Có quyền hợp lệ (Authorized)]
    BookingService -> BookingService: 10 Kiểm tra trạng thái hiện tại (Status Check)

    alt [Trạng thái không thể hủy (Completed/Cancelled)]
        BookingService --> BookingDetailView: 11 Trả về lỗi "Đơn hàng này không thể hủy vì đã hoàn tất/đã hủy"
        BookingDetailView --> User: 12 Hiển thị thông báo lỗi
    else [Trạng thái hợp lệ (Pending/Confirmed)]
        BookingService -> BookingDB: 13 Cập nhật trạng thái "Đã hủy" & Lưu lý do
        BookingDB --> BookingService: 14 Xác nhận cập nhật thành công
        BookingService --> BookingDetailView: 15 Thông báo "Hủy đặt phòng thành công"
        BookingDetailView --> User: 16 Hiển thị thông báo & Cập nhật trạng thái đơn hàng
    end
end

@enduml
```
