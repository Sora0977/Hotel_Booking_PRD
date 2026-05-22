---
status: draft
dependencies:
  - 3_2_1_8_usecase_tra_cuu_khach_san.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.26"
title: "Sơ đồ tuần tự xem danh sách phòng của khách sạn"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.38: Sơ đồ tuần tự xem danh sách phòng của khách sạn


- Sơ đồ tuần tự xem danh sách tất cả booking

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem danh sách tất cả Booking

actor Admin
boundary BookingListView
control BookingService
entity BookingDB

Admin -> BookingListView: 1 Chọn chức năng "Quản lý Đặt phòng"
BookingListView -> BookingService: 2 Yêu cầu lấy danh sách Booking
BookingService -> BookingService: 3 Kiểm tra quyền Admin (Check Role)

alt [Không có quyền Admin (Unauthorized)]
    BookingService --> BookingListView: 4 Từ chối truy cập & Báo lỗi
    BookingListView --> Admin: 5 Hiển thị thông báo "Bạn không có quyền truy cập"
else [Có quyền Admin (Authorized)]
    BookingService -> BookingDB: 6 Truy vấn toàn bộ đơn đặt phòng
    BookingDB --> BookingService: 7 Trả về danh sách Booking (Khách, Phòng, Trạng thái...)
    BookingService --> BookingListView: 8 Trả về dữ liệu danh sách
    BookingListView --> Admin: 9 Hiển thị danh sách Booking lên giao diện
end

@enduml
```
