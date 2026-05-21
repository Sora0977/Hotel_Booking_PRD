---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.01"
title: "Sơ đồ tuần tự đăng nhập"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.13: Sơ đồ tuần tự đăng nhập


- Sơ đồ tuần tự đăng ký

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Đăng ký tài khoản

actor Guest
boundary RegisterForm
control AuthService
entity UserDB

Guest -> RegisterForm : 1 Nhập thông tin (Email, Pass, Họ tên...)
Guest -> RegisterForm : 2 Nhấn nút "Đăng ký"
RegisterForm -> AuthService : 3 Gửi yêu cầu đăng ký (data)
AuthService -> AuthService : 4 Kiểm tra định dạng dữ liệu (Validate)

alt Dữ liệu sai định dạng
    AuthService --> RegisterForm : 5 Trả về lỗi Validation (ví dụ: Pass ngắn)
    RegisterForm --> Guest : 6 Hiển thị thông báo lỗi chi tiết
else Định dạng hợp lệ
    AuthService -> UserDB : 7 Kiểm tra Email đã tồn tại?
    UserDB --> AuthService : 8 Kết quả (Có/Không)
    alt Email đã được sử dụng
        AuthService --> RegisterForm : 9 Trả về lỗi "Email đã tồn tại"
        RegisterForm --> Guest : 10 Hiển thị lỗi Validation
    else Email hợp lệ (Chưa tồn tại)
        AuthService -> AuthService : 11 Mã hóa mật khẩu (Hash)
        AuthService -> AuthService : 12 Gán quyền mặc định (Customer)
        AuthService -> UserDB : 13 Lưu tài khoản mới vào DB
        UserDB --> AuthService : 14 Xác nhận lưu thành công
        AuthService --> RegisterForm : 15 Thông báo đăng ký thành công
        RegisterForm --> Guest : 16 Hiển thị thông báo thành công
    end
end
@enduml
```
