---
status: draft
dependencies:
  - 3_2_1_12_usecase_quan_ly_tien_ich.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.33"
title: "Sơ đồ tuần tự cập nhật tiện ích"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.45: Sơ đồ tuần tự cập nhật tiện ích


- Sơ đồ tuần tự xóa tiện ích hệ thống

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xóa tiện ích hệ thống

actor Admin
boundary AmenityView
control RoomService
entity Database

Admin -> AmenityView: 1 Nhấn nút "Xóa" tại dòng tiện ích
AmenityView --> Admin: 2 Hiển thị hộp thoại xác nhận xóa
Admin -> AmenityView: 3 Nhấn "Đồng ý"
AmenityView -> RoomService: 4 Gửi yêu cầu xóa(amenityId)
RoomService -> Database: 5 Tìm tiện ích theo ID
entity --> RoomService: 6 Kết quả (Amenity hoặc Null)

alt [Tiện ích không tồn tại]
    RoomService --> AmenityView: 7 Trả về lỗi "Tiện ích không tồn tại"
    AmenityView --> Admin: 8 Hiển thị thông báo lỗi & Làm mới danh sách
else [Tiện ích tồn tại]
    RoomService -> Database: 9 Kiểm tra xem tiện ích có đang được dùng không?
    Database --> RoomService: 10 Kết quả (Đang dùng / Chưa dùng)

    alt [Đang được sử dụng bởi các phòng (In Use)]
        RoomService --> AmenityView: 11 Trả về lỗi "Không thể xóa: Tiện ích đang được sử dụng bởi các phòng"
        AmenityView --> Admin: 12 Hiển thị cảnh báo & Từ chối xóa
    else [Không được sử dụng (Safe to Delete)]
        RoomService -> Database: 13 Xóa tiện ích khỏi DB
        Database --> RoomService: 14 Xác nhận xóa thành công
        RoomService --> AmenityView: 15 Thông báo "Đã xóa tiện ích thành công"
        AmenityView --> Admin: 16 Hiển thị thông báo & Cập nhật danh sách
    end
end

@enduml
```
