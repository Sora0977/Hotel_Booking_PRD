---
status: draft
dependencies:
  - 3_2_1_6_usecase_tra_cuu_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.15"
title: "Sơ đồ tuần tự tìm phòng trống theo ngày"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.27: Sơ đồ tuần tự tìm phòng trống theo ngày


- Sơ đồ tuần tự xem chi tiết phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem chi tiết phòng

actor "Guest/User" as GuestUser
boundary RoomDetailView
control RoomService
entity RoomDB

GuestUser -> RoomDetailView : 1 Nhấn vào hình ảnh/tên của phòng
RoomDetailView -> RoomService : 2 Gửi yêu cầu xem chi tiết(roomId)
RoomService -> RoomDB : 3 Truy vấn thông tin phòng theo ID
RoomDB --> RoomService : 4 Trả về kết quả (Room hoặc Null)

alt Không tìm thấy phòng (Data Null)
    RoomService --> RoomDetailView : 5 Trả về lỗi "Không tìm thấy phòng bạn yêu cầu" (404)
    RoomDetailView --> GuestUser : 6 Hiển thị trang lỗi 404 & Nút quay lại
else Dữ liệu tồn tại (Success)
    RoomService -> RoomDB : 7 Lấy thêm danh sách tiện ích & hình ảnh chi tiết
    RoomDB --> RoomService : 8 Trả về dữ liệu đầy đủ (Info, Images, Amenities)
    RoomService --> RoomDetailView : 9 Trả về dữ liệu chi tiết phòng
    RoomDetailView --> GuestUser : 10 Hiển thị trang chi tiết phòng (Mô tả, Ảnh, Tiện ích...)
end
@enduml
```
