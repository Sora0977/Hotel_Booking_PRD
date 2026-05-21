---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2"
title: "3.2.2 Sơ đồ tuần tự"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

### 3.2.2 Sơ đồ tuần tự

- Sơ đồ tuần tự đăng nhập

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Đăng nhập

actor Guest
boundary "Login Form" as LoginForm
control AuthService
entity UserDB

Guest -> LoginForm : 1 Nhập Email và Mật khẩu
Guest -> LoginForm : 2 Nhấn nút "Đăng nhập"
LoginForm -> AuthService : 3 Gửi yêu cầu đăng nhập(email, password)
AuthService -> UserDB : 4 Truy vấn kiểm tra Email tồn tại
UserDB --> AuthService : 5 Trả về thông tin User (hoặc Null)
AuthService -> AuthService : 6 Kiểm tra mật khẩu (So khớp Hash)

alt Email không tồn tại HOẶC Sai mật khẩu
    AuthService --> LoginForm : 7 Trả về lỗi "Tên đăng nhập hoặc mật khẩu không đúng"
    LoginForm --> Guest : 8 Hiển thị thông báo sai thông tin
else Thông tin hợp lệ (Email đúng và Pass đúng)
    AuthService -> AuthService : 9 Kiểm tra trạng thái khóa (Activate)
    alt Tài khoản chưa kích hoạt (Activate == false)
        AuthService --> LoginForm : 10 Trả về lỗi "Tài khoản bị khóa"
        LoginForm --> Guest : 11 Hiển thị thông báo tài khoản bị khóa
    else Tài khoản hợp lệ (Success)
        AuthService -> AuthService : 12 Tạo JWT Token
        AuthService --> LoginForm : 13 Trả về Token & Thông báo thành công
        LoginForm --> Guest : 14 Chuyển hướng vào trang chủ
    end
end
@enduml
```
