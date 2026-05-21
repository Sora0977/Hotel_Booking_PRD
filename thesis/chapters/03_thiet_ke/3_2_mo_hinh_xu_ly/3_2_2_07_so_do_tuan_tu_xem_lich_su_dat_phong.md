---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.07"
title: "Sơ đồ tuần tự xem lịch sử đặt phòng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.19: Sơ đồ tuần tự xem lịch sử đặt phòng


- Sơ đồ tuần tự xem danh sách người dùng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem danh sách người dùng

actor Admin
boundary UserManagementView
control UserService
entity UserDB
control Control

Admin -> UserManagementView : 1 Chọn menu "Quản lý người dùng"
UserManagementView -> Control : 2 Yêu cầu lấy danh sách người dùng
Control -> Control : 3 Kiểm tra quyền Admin (Check Role)

alt Không có quyền Admin (Truy cập trái phép)
    Control --> UserManagementView : 4 Từ chối truy cập & Báo lỗi
    UserManagementView --> Admin : 5 Hiển thị thông báo "Bạn không có quyền truy cập"
else Có quyền Admin (Hợp lệ)
    Control -> UserDB : 6 Truy vấn toàn bộ danh sách người dùng
    UserDB --> Control : 7 Trả về danh sách User (ID, Tên, Email, Trạng thái...)
    Control --> UserManagementView : 8 Trả về dữ liệu danh sách
    UserManagementView --> Admin : 9 Hiển thị danh sách người dùng lên giao diện
end
@enduml
```
