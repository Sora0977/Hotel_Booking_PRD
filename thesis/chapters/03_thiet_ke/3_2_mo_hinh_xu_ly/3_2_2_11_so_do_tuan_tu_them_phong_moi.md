---
status: draft
dependencies:
  - 3_2_1_5_usecase_quan_ly_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.11"
title: "Sơ đồ tuần tự thêm phòng mới"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.23: Sơ đồ tuần tự thêm phòng mới


- Sơ đồ tuần tự cập nhật thông tin phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Cập nhật thông tin phòng

actor Admin
boundary EditRoomForm
control RoomService
participant CloudinaryService
entity RoomDB

Admin -> EditRoomForm : 1 Thay đổi thông tin (Giá, Mô tả...) & Chọn ảnh mới (Tùy chọn)
Admin -> EditRoomForm : 2 Nhấn nút "Lưu thay đổi"
EditRoomForm -> RoomService : 3 Gửi yêu cầu cập nhật(roomId, data, newImage)
RoomService -> RoomDB : 4 Kiểm tra phòng tồn tại (Find By ID)
RoomDB --> RoomService : 5 Trả về kết quả (Room hoặc Null)

alt Phòng không tìm thấy (Not Found)
    RoomService --> EditRoomForm : 6 Trả về lỗi "Phòng này không còn tồn tại"
    EditRoomForm --> Admin : 7 Hiển thị thông báo lỗi & Quay lại danh sách
else Phòng tồn tại (Valid)
    opt Có tải lên ảnh mới
        RoomService -> CloudinaryService : 8 Upload hình ảnh mới
        CloudinaryService --> RoomService : 9 Trả về URL ảnh mới (hoặc Lỗi)
        alt Lỗi định dạng ảnh
            RoomService --> EditRoomForm : 10 Trả về lỗi "Định dạng ảnh không hợp lệ"
            EditRoomForm --> Admin : 11 Hiển thị cảnh báo lỗi ảnh
        else Upload thành công
            RoomService -> RoomService : 12 Cập nhật URL ảnh vào đối tượng Room
        end
    end
    RoomService -> RoomDB : 13 Lưu thông tin cập nhật vào DB
    RoomDB --> RoomService : 14 Xác nhận cập nhật thành công
    RoomService --> EditRoomForm : 15 Thông báo "Cập nhật thành công"
    EditRoomForm --> Admin : 16 Hiển thị thông báo thành công
end
@enduml
```
