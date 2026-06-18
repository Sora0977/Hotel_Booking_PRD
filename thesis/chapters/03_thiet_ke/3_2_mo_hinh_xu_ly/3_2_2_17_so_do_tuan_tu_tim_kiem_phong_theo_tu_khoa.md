---
status: draft
dependencies:
  - 3_2_1_6_usecase_tra_cuu_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.17"
title: "Sơ đồ tuần tự tìm kiếm phòng theo từ khóa"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.29: Sơ đồ tuần tự tìm kiếm phòng theo từ khóa


- Sơ đồ tuần tự xem loại phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem loại phòng

actor "Guest/User" as GuestUser
boundary CategoryView
control RoomService
entity RoomDB

GuestUser -> CategoryView : 1 Chọn menu "Loại phòng" (hoặc bộ lọc)
CategoryView -> RoomService : 2 Yêu cầu lấy danh sách loại phòng
RoomService -> RoomDB : 3 Truy vấn dữ liệu Loại phòng (Enum/Table)
RoomDB --> RoomService : 4 Trả về danh sách loại phòng

alt Dữ liệu trống (Empty Data)
    RoomService --> CategoryView : 5 Trả về thông báo "Chưa có dữ liệu loại phòng"
    CategoryView --> GuestUser : 6 Hiển thị thông báo dữ liệu trống
else Có dữ liệu (Success)
    RoomService --> CategoryView : 7 Trả về danh sách (Tên loại, Mô tả...)
    CategoryView --> GuestUser : 8 Hiển thị danh sách các loại phòng
end
@enduml
```
