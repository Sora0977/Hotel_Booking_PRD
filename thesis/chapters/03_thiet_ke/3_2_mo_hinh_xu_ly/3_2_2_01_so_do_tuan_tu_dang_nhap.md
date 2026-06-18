---
status: draft
last_updated: 2026-05-22
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.01"
title: "Sơ đồ tuần tự đăng nhập"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
dependencies:
  - "3_2_1_1_usecase_dang_nhap.md"
  - "3_2_3_01_so_do_hoat_dong_dang_nhap.md"
---

<ai_context>
File này là mảnh Level-3 thuộc mục 3.2. Chứa Sơ đồ tuần tự cho chức năng Đăng nhập.
</ai_context>

<system_instruction>
TUYỆT ĐỐI KHÔNG tự ý thay đổi, xóa, định dạng lại mã nguồn PlantUML hoặc code fence trừ khi tác vụ yêu cầu đích danh việc sửa sơ đồ.
</system_instruction>

> Hình 3.13: Sơ đồ tuần tự đăng nhập


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
boundary LoginForm
control AuthService
entity UserDB
control JwtService

Guest -> LoginForm : 1 Nhập Email và Mật khẩu
Guest -> LoginForm : 2 Nhấn nút "Đăng nhập"
LoginForm -> AuthService : 3 Gửi yêu cầu đăng nhập (email, password)
AuthService -> AuthService : 4 Kiểm tra định dạng dữ liệu

alt Dữ liệu không hợp lệ
    AuthService --> LoginForm : 5 Trả về lỗi Validation
    LoginForm --> Guest : 6 Hiển thị thông báo lỗi và yêu cầu nhập lại
else Dữ liệu hợp lệ
    AuthService -> UserDB : 7 Tìm tài khoản theo Email
    UserDB --> AuthService : 8 Thông tin tài khoản / Không tìm thấy
    alt Email không tồn tại
        AuthService --> LoginForm : 9 Trả về lỗi "Tên đăng nhập hoặc mật khẩu không đúng"
        LoginForm --> Guest : 10 Hiển thị thông báo lỗi
    else Email tồn tại
        AuthService -> AuthService : 11 So sánh mật khẩu đã hash
        alt Mật khẩu không đúng
            AuthService --> LoginForm : 12 Trả về lỗi "Tên đăng nhập hoặc mật khẩu không đúng"
            LoginForm --> Guest : 13 Hiển thị thông báo lỗi
        else Mật khẩu đúng
            AuthService -> AuthService : 14 Kiểm tra trạng thái tài khoản (is_active)
            alt Tài khoản chưa kích hoạt hoặc bị khóa
                AuthService --> LoginForm : 15 Trả về lỗi "Tài khoản bị khóa"
                LoginForm --> Guest : 16 Hiển thị thông báo tài khoản bị khóa
            else Tài khoản hợp lệ
                AuthService -> JwtService : 17 Tạo JWT Token
                JwtService --> AuthService : 18 Trả về JWT Token
                AuthService --> LoginForm : 19 Trả về token và thông tin người dùng
                LoginForm --> Guest : 20 Thông báo đăng nhập thành công và chuyển hướng
            end
        end
    end
end
@enduml
```
