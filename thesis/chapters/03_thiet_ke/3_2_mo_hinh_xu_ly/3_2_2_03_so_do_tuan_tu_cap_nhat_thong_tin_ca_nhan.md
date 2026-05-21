---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.03"
title: "Sơ đồ tuần tự cập nhật thông tin cá nhân"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.15: Sơ đồ tuần tự cập nhật thông tin cá nhân


- Sơ đồ tuần tự đổi mật khẩu

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Đổi mật khẩu

actor User
boundary ChangePasswordForm
control AccountService
entity UserDB

User -> ChangePasswordForm : 1 Nhập Mật khẩu cũ, Mật khẩu mới, Xác nhận
User -> ChangePasswordForm : 2 Nhấn nút "Đổi mật khẩu"
ChangePasswordForm -> AccountService : 3 Gửi yêu cầu đổi mật khẩu(oldPass, newPass)
AccountService -> AccountService : 4 Lấy thông tin User hiện tại (Context)
AccountService -> UserDB : 5 Lấy mật khẩu hiện tại (Hash)
UserDB --> AccountService : 6 Trả về chuỗi Hash mật khẩu
AccountService -> AccountService : 7 So sánh Mật khẩu cũ (Hash Check)

alt Mật khẩu cũ không đúng
    AccountService --> ChangePasswordForm : 8 Trả về lỗi "Mật khẩu hiện tại không đúng"
    ChangePasswordForm --> User : 9 Hiển thị thông báo & Xóa trường nhập liệu
else Mật khẩu cũ hợp lệ
    AccountService -> AccountService : 10 Kiểm tra mật khẩu mới khác mật khẩu cũ
    alt Mật khẩu mới trùng mật khẩu cũ
        AccountService --> ChangePasswordForm : 11 Trả về lỗi "Mật khẩu mới phải khác cũ"
        ChangePasswordForm --> User : 12 Hiển thị cảnh báo
    else Dữ liệu hợp lệ (Success)
        AccountService -> AccountService : 13 Mã hóa mật khẩu mới (Hash)
        AccountService -> UserDB : 14 Cập nhật mật khẩu mới vào DB
        UserDB --> AccountService : 15 Xác nhận cập nhật thành công
        AccountService --> ChangePasswordForm : 16 Thông báo "Đổi mật khẩu thành công"
        ChangePasswordForm --> User : 17 Hiển thị thông báo thành công
    end
end
@enduml
```
