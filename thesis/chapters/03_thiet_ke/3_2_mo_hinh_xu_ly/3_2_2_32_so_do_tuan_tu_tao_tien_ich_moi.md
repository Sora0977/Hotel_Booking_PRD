---
status: draft
dependencies:
  - 3_2_1_12_usecase_quan_ly_tien_ich.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.32"
title: "Sơ đồ tuần tự tạo tiện ích mới"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.44: Sơ đồ tuần tự tạo tiện ích mới


- Sơ đồ tuần tự cập nhật tiện ích

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Cập nhật tiện ích

actor Admin
boundary EditAmenityForm
control "RoomService/AmenityService" as AmenityService
entity AmenityDB

Admin -> EditAmenityForm: 1 Sửa tên tiện ích (Ví dụ: Từ "Wifi" thành "Wifi 5G")
Admin -> EditAmenityForm: 2 Nhấn nút "Lưu thay đổi"
EditAmenityForm -> AmenityService: 3 Gửi yêu cầu cập nhật(id, newName)
AmenityService -> AmenityDB: 4 Tìm tiện ích theo ID
AmenityDB --> AmenityService: 5 Kết quả (Amenity hoặc Null)

alt [Tiện ích không tồn tại (Not Found)]
    AmenityService --> EditAmenityForm: 6 Trả về lỗi "Tiện ích không tồn tại hoặc đã bị xóa"
    EditAmenityForm --> Admin: 7 Hiển thị thông báo lỗi & Quay lại danh sách
else [Tiện ích tồn tại (Valid ID)]
    AmenityService -> AmenityDB: 8 Kiểm tra trùng tên (Check Name Exist AND ID != currentID)
    AmenityDB --> AmenityService: 9 Kết quả (Trùng/Không trùng)

    alt [Tên đã được sử dụng bởi tiện ích khác]
        AmenityService --> EditAmenityForm: 10 Trả về lỗi "Tên tiện ích này đã tồn tại"
        EditAmenityForm --> Admin: 11 Hiển thị cảnh báo trùng lặp
    else [Tên hợp lệ (Success)]
        AmenityService -> AmenityDB: 12 Cập nhật dữ liệu vào DB (Update)
        AmenityDB --> AmenityService: 13 Xác nhận cập nhật thành công
        AmenityService --> EditAmenityForm: 14 Thông báo "Cập nhật tiện ích thành công"
        EditAmenityForm --> Admin: 15 Hiển thị thông báo thành công
    end
end

@enduml
```
