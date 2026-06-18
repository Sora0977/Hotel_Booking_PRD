---
status: draft
dependencies:
  - 3_2_1_4_usecase_quan_tri_nguoi_dung.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.09"
title: "Sơ đồ tuần tự khóa tài khoản người dùng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.21: Sơ đồ tuần tự khóa tài khoản người dùng


- Sơ đồ tuần tự mở khóa tài khoản người dùng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Mở khóa tài khoản người dùng

actor Admin
boundary UserManagementView
control UserService
entity UserDB

Admin -> UserManagementView : 1 Chọn người dùng bị khóa & Nhấn nút "Mở khóa"
UserManagementView -> UserService : 2 Gửi yêu cầu mở khóa(userId)
UserService -> UserDB : 3 Tìm User theo ID
UserDB --> UserService : 4 Trả về kết quả (User hoặc Null)

alt Người dùng không tồn tại (User not found)
    UserService --> UserManagementView : 5 Trả về lỗi "Người dùng không tồn tại"
    UserManagementView --> Admin : 6 Hiển thị thông báo lỗi & Hủy thao tác
else Tìm thấy Người dùng (User found)
    UserService -> UserDB : 7 Cập nhật trạng thái (Activate = True)
    UserDB --> UserService : 8 Xác nhận cập nhật thành công
    UserService --> UserManagementView : 9 Thông báo "Đã mở khóa tài khoản thành công"
    UserManagementView --> Admin : 10 Hiển thị thông báo & Cập nhật trạng thái "Active"
end
@enduml
```
