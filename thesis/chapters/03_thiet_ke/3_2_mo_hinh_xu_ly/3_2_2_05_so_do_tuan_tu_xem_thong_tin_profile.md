---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.05"
title: "Sơ đồ tuần tự xem thông tin profile"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.17: Sơ đồ tuần tự xem thông tin profile


- Sơ đồ tuần tự xóa tài khoản cá nhân

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xóa tài khoản cá nhân

actor User
boundary SettingsView
control AccountService
entity UserDB

User -> SettingsView : 1 Chọn chức năng "Xóa tài khoản"
SettingsView --> User : 2 Hiển thị cảnh báo & Yêu cầu xác nhận
User -> SettingsView : 3 Nhấn nút "Đồng ý" (Confirm)
SettingsView -> AccountService : 4 Gửi yêu cầu xóa tài khoản
AccountService -> AccountService : 5 Lấy thông tin User từ Context
AccountService -> UserDB : 6 Kiểm tra ràng buộc dữ liệu (Booking chưa hoàn tất)
UserDB --> AccountService : 7 Kết quả kiểm tra

alt Có ràng buộc dữ liệu (Ví dụ: Đơn phòng chưa hoàn tất)
    AccountService --> SettingsView : 8 Trả về lỗi "Không thể xóa tài khoản"
    SettingsView --> User : 9 Hiển thị thông báo lỗi (Fail)
else Không có ràng buộc (Hợp lệ)
    AccountService -> UserDB : 10 Cập nhật trạng thái sang "Đã xóa" (Soft Delete)
    UserDB --> AccountService : 11 Xác nhận xóa thành công
    AccountService -> AccountService : 12 Thực hiện Đăng xuất (Hủy phiên làm việc)
    AccountService --> SettingsView : 13 Thông báo thành công & Chuyển hướng
    SettingsView --> User : 14 Chuyển hướng về Trang chủ
end
@enduml
```
