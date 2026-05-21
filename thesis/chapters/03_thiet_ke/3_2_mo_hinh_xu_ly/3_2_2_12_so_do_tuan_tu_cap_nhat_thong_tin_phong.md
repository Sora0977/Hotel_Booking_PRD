---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.12"
title: "Sơ đồ tuần tự cập nhật thông tin phòng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.24: Sơ đồ tuần tự cập nhật thông tin phòng


- Sơ đồ tuần tự xóa phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xóa phòng

actor Admin
boundary RoomManagementView
control RoomService
entity RoomDB

Admin -> RoomManagementView : 1 Nhấn nút "Xóa" tại dòng phòng cần xóa
RoomManagementView --> Admin : 2 Hiển thị hộp thoại yêu cầu xác nhận
Admin -> RoomManagementView : 3 Nhấn nút "Đồng ý" (Confirm)
RoomManagementView -> RoomService : 4 Gửi yêu cầu xóa phòng(roomId)
RoomService -> RoomDB : 5 Kiểm tra phòng tồn tại (Check Exists)
RoomDB --> RoomService : 6 Trả về kết quả (True/False)

alt Phòng không tồn tại (Not Found)
    RoomService --> RoomManagementView : 7 Trả về lỗi "Phòng này không tồn tại hoặc đã bị xóa"
    RoomManagementView --> Admin : 8 Hiển thị thông báo lỗi & Làm mới danh sách
else Phòng tồn tại (Valid)
    RoomService -> RoomDB : 9 Xóa dữ liệu phòng (Delete)
    RoomDB --> RoomService : 10 Xác nhận xóa thành công
    RoomService --> RoomManagementView : 11 Thông báo "Đã xóa phòng thành công"
    RoomManagementView --> Admin : 12 Hiển thị thông báo & Cập nhật danh sách phòng
end
@enduml
```
