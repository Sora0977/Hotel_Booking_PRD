---
status: draft
dependencies:
  - 3_2_1_12_usecase_quan_ly_tien_ich.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.35"
title: "Sơ đồ tuần tự gỡ tiện ích khỏi khách sạn"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.47: Sơ đồ tuần tự gỡ tiện ích khỏi khách sạn


- Sơ đồ tuần tự gỡ tiện ích khỏi phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Gỡ tiện ích khỏi Phòng

actor Admin
boundary EditRoomView
control RoomService
entity RoomDB

Admin -> EditRoomView: 1 Nhấn nút "Xóa" (icon X) trên tiện ích của phòng
EditRoomView -> RoomService: 2 Gửi yêu cầu gỡ tiện ích(roomId, amenityId)
RoomService -> RoomService: 3 Kiểm tra quyền sở hữu (Check Owner via Hotel)
note right of RoomDB
Admin phải là chủ của Khách sạn chứa Phòng này
end note

alt [Không có quyền (Unauthorized)]
    RoomService --> EditRoomView: 4 Trả về lỗi "Bạn không có quyền sửa đổi phòng này"
    EditRoomView --> Admin: 5 Hiển thị cảnh báo bảo mật
else [Quyền hợp lệ (Authorized)]
    RoomService -> RoomDB: 6 Kiểm tra tiện ích có đang gắn với Phòng không?
    note right of RoomDB
    Query bảng trung gian (room_amenities)
    để xác nhận liên kết
    end note
    RoomDB --> RoomService: 7 Kết quả (Có/Không)

    alt [Liên kết không tồn tại (Not Found)]
        RoomService --> EditRoomView: 8 Trả về thông báo "Tiện ích này đã được gỡ hoặc không tồn tại"
        EditRoomView --> Admin: 9 Cập nhật giao diện (loại bỏ tag tiện ích)
    else [Liên kết tồn tại (Valid)]
        RoomService -> RoomDB: 10 Xóa dòng trong bảng liên kết (Delete Relation)
        RoomDB --> RoomService: 11 Xác nhận gỡ thành công
        RoomService --> EditRoomView: 12 Thông báo "Đã gỡ tiện ích thành công"
        EditRoomView --> Admin: 13 Loại bỏ tiện ích khỏi danh sách hiển thị
    end
end

@enduml
```
