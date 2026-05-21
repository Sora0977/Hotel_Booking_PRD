---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.10"
title: "Sơ đồ tuần tự mở khóa tài khoản người dùng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.22: Sơ đồ tuần tự mở khóa tài khoản người dùng


- Sơ đồ tuần tự thêm phòng mới

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Thêm phòng mới

actor Admin
boundary AddRoomForm
control RoomService
participant CloudinaryService
entity RoomDB

Admin -> AddRoomForm : 1 Nhập thông tin phòng, chọn tiện ích & chọn ảnh
Admin -> AddRoomForm : 2 Nhấn nút "Lưu" (Save)
AddRoomForm -> RoomService : 3 Gửi yêu cầu thêm phòng(data, image, amenities)
RoomService -> RoomService : 4 Kiểm tra quyền sở hữu Khách sạn (Check Owner)

alt Không phải chủ sở hữu (Unauthorized)
    RoomService --> AddRoomForm : 5 Trả về lỗi "Bạn không có quyền thêm phòng"
    AddRoomForm --> Admin : 6 Hiển thị cảnh báo bảo mật & Chặn hành động
else Quyền sở hữu hợp lệ (Owner Verified)
    RoomService -> CloudinaryService : 7 Upload hình ảnh lên Server
    CloudinaryService --> RoomService : 8 Trả về URL ảnh (hoặc Lỗi định dạng)
    alt Lỗi Upload hoặc Sai định dạng ảnh
        RoomService --> AddRoomForm : 9 Trả về lỗi "Định dạng ảnh không hợp lệ"
        AddRoomForm --> Admin : 10 Hiển thị cảnh báo lỗi ảnh
    else Upload thành công (URL hợp lệ)
        RoomService -> RoomDB : 11 Lưu thông tin phòng mới (kèm URL ảnh)
        RoomDB -> RoomDB : 12 Liên kết tiện ích cho phòng (Add Amenities)
        RoomDB --> RoomService : 13 Xác nhận lưu thành công
        RoomService --> AddRoomForm : 14 Thông báo "Thêm phòng thành công"
        AddRoomForm --> Admin : 15 Hiển thị thông báo thành công
    end
end
@enduml
```
