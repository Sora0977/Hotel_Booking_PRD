---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.31"
title: "Sơ đồ tuần tự hủy đặt phòng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.43: Sơ đồ tuần tự hủy đặt phòng


- Sơ đồ tuần tự tạo tiện ích mới

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Tạo tiện ích mới

actor Admin
boundary AmenityForm
control "RoomService/AmenityService" as AmenityService
entity AmenityDB

Admin -> AmenityForm: 1 Nhập tên tiện ích (Ví dụ: "Hồ bơi", "Wifi")
Admin -> AmenityForm: 2 Nhấn nút "Thêm mới"
AmenityForm -> AmenityService: 3 Gửi yêu cầu thêm tiện ích(name)
AmenityService -> AmenityDB: 4 Kiểm tra tên tiện ích đã tồn tại chưa (Check Exists)
AmenityDB --> AmenityService: 5 Kết quả (True/False)

alt [Tiện ích đã tồn tại (Duplicate)]
    AmenityService --> AmenityForm: 6 Trả về lỗi "Tiện ích này đã tồn tại trong hệ thống"
    AmenityForm --> Admin: 7 Hiển thị cảnh báo & Yêu cầu nhập tên khác
else [Tên hợp lệ (Valid)]
    AmenityService -> AmenityDB: 8 Lưu tiện ích mới vào DB
    AmenityDB --> AmenityService: 9 Xác nhận lưu thành công
    AmenityService --> AmenityForm: 10 Thông báo "Thêm tiện ích thành công"
    AmenityForm --> Admin: 11 Hiển thị thông báo & Cập nhật danh sách
end

@enduml
```
