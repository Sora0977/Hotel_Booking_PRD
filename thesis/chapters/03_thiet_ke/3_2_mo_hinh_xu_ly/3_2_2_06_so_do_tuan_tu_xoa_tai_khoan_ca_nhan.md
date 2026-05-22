---
status: draft
dependencies:
  - 3_2_1_3_usecase_quan_ly_thong_tin_ca_nhan.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.06"
title: "Sơ đồ tuần tự xóa tài khoản cá nhân"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.18: Sơ đồ tuần tự xóa tài khoản cá nhân


- Sơ đồ tuần tự xem lịch sử đặt phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem lịch sử đặt phòng

actor User
boundary HistoryView
control BookingService
entity BookingDB

User -> HistoryView : 1 Chọn mục "Lịch sử đặt phòng"
HistoryView -> BookingService : 2 Yêu cầu lấy danh sách đặt phòng
BookingService -> BookingService : 3 Lấy User ID từ Context (Session/Token)
BookingService -> BookingDB : 4 Truy vấn danh sách Booking theo User ID
BookingDB --> BookingService : 5 Trả về danh sách Booking (List)

alt Danh sách trống (Chưa từng đặt phòng)
    BookingService --> HistoryView : 6 Trả về thông báo "Bạn chưa có lịch sử đặt phòng nào"
    HistoryView --> User : 7 Hiển thị thông báo trống
else Danh sách có dữ liệu (Success)
    BookingService --> HistoryView : 8 Trả về danh sách đơn hàng (Ngày, KS, Trạng thái...)
    HistoryView --> User : 9 Hiển thị bảng lịch sử đặt phòng
end
@enduml
```
