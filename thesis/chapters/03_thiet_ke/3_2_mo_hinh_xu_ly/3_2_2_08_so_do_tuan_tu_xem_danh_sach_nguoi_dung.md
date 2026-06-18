---
status: draft
dependencies:
  - 3_2_1_4_usecase_quan_tri_nguoi_dung.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.08"
title: "Sơ đồ tuần tự xem danh sách người dùng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.20: Sơ đồ tuần tự xem danh sách người dùng


- Sơ đồ tuần tự khóa tài khoản người dùng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Khóa tài khoản người dùng

actor Admin
boundary UserManagementView
control UserService
entity UserDB

Admin -> UserManagementView : 1 Tìm kiếm & Chọn người dùng cần khóa
Admin -> UserManagementView : 2 Nhấn nút "Khóa tài khoản"
UserManagementView -> UserService : 3 Gửi yêu cầu khóa tài khoản(userId)
UserService -> UserDB : 4 Tìm User theo ID
UserDB --> UserService : 5 Trả về kết quả (User hoặc Null)

alt Người dùng không tồn tại (User not found)
    UserService --> UserManagementView : 6 Trả về lỗi "Người dùng không tồn tại"
    UserManagementView --> Admin : 7 Hiển thị thông báo lỗi & Hủy thao tác
else Tìm thấy Người dùng (User found)
    UserService -> UserDB : 8 Cập nhật trạng thái (Activate = False)
    UserDB --> UserService : 9 Xác nhận cập nhật thành công
    UserService --> UserManagementView : 10 Thông báo "Đã khóa tài khoản thành công"
    UserManagementView --> Admin : 11 Hiển thị thông báo & Cập nhật trạng thái trên danh sách
end
@enduml
```
