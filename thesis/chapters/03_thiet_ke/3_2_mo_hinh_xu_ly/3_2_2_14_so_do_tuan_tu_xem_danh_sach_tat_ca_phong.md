---
status: draft
dependencies:
  - 3_2_1_5_usecase_quan_ly_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.14"
title: "Sơ đồ tuần tự xem danh sách tất cả phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.26: Sơ đồ tuần tự xem danh sách tất cả phòng


- Sơ đồ tuần tự tìm phòng trống theo ngày

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Tìm phòng trống theo ngày

actor "Guest/User" as GuestUser
boundary SearchForm
control RoomService
entity BookingDB

GuestUser -> SearchForm : 1 Chọn ngày Check-in & Check-out
GuestUser -> SearchForm : 2 Nhấn nút "Tìm kiếm"
SearchForm -> RoomService : 3 Gửi yêu cầu tìm phòng(checkIn, checkOut)
RoomService -> RoomService : 4 Kiểm tra Logic ngày (CheckOut > CheckIn >= Today)

alt Ngày không hợp lệ (Lỗi Logic)
    RoomService --> SearchForm : 5 Trả về lỗi "Ngày Check-in/Check-out không hợp lệ"
    SearchForm --> GuestUser : 6 Hiển thị cảnh báo & Yêu cầu nhập lại
else Ngày hợp lệ (Valid Date)
    RoomService -> BookingDB : 7 Truy vấn các phòng TRỐNG trong khoảng thời gian
    BookingDB --> RoomService : 8 Trả về danh sách phòng khả dụng
    RoomService --> SearchForm : 9 Trả về danh sách kết quả
    SearchForm --> GuestUser : 10 Hiển thị danh sách phòng trống phù hợp
end
@enduml
```
