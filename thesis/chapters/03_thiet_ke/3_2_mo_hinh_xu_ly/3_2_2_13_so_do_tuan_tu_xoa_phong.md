---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.13"
title: "Sơ đồ tuần tự xóa phòng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.25: Sơ đồ tuần tự xóa phòng


- Sơ đồ tuần tự xem danh sách tất cả phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem danh sách tất cả phòng

actor "Guest/User" as GuestUser
boundary RoomListView
control RoomService
entity RoomDB

GuestUser -> RoomListView : 1 Chọn menu "Danh sách phòng"
RoomListView -> RoomService : 2 Yêu cầu lấy toàn bộ danh sách phòng
RoomService -> RoomDB : 3 Truy vấn dữ liệu phòng (Select All)
RoomDB --> RoomService : 4 Trả về danh sách phòng (List<Room>)

alt Danh sách trống (Empty List)
    RoomService --> RoomListView : 5 Trả về thông báo "Chưa có phòng nào được cập nhật"
    RoomListView --> GuestUser : 6 Hiển thị thông báo dữ liệu trống
else Có dữ liệu (Success)
    RoomService --> RoomListView : 7 Trả về danh sách phòng (Tên, Giá, Ảnh...)
    RoomListView --> GuestUser : 8 Hiển thị danh sách phòng lên giao diện (Phân trang)
end
@enduml
```
