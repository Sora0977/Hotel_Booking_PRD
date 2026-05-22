---
status: draft
last_updated: 2026-05-22
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.1.1"
title: "3.2.1.1 Usecase đăng nhập"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
dependencies:
  - "3_2_2_01_so_do_tuan_tu_dang_nhap.md"
  - "3_2_3_01_so_do_hoat_dong_dang_nhap.md"
---

<ai_context>
File này là mảnh Level-3 thuộc mục 3.2. Chứa Đặc tả Use case cho chức năng Đăng nhập.
</ai_context>

<system_instruction>
TUYỆT ĐỐI KHÔNG tự ý thay đổi, xóa, định dạng lại mã nguồn PlantUML hoặc code fence trừ khi tác vụ yêu cầu đích danh việc sửa sơ đồ.
</system_instruction>

#### 3.2.1.1 Usecase đăng nhập

```plantuml
@startuml
!theme plain
left to right direction

actor "Khách (Guest)" as Guest

rectangle "Module Đăng nhập" {
  usecase "Đăng nhập" as Login
  usecase "Kiểm tra Email tồn tại" as CheckEmail
  usecase "Kiểm tra mật khẩu" as CheckPassword
  usecase "Kiểm tra trạng thái khóa\n(Activate)" as CheckActive
  usecase "Tạo JWT Token" as Token
  usecase "Thông báo sai thông tin" as WrongInfo
  usecase "Thông báo tài khoản bị khóa" as LockedAccount
}

Guest --> Login
Login ..> CheckEmail : <<include>>
Login ..> CheckPassword : <<include>>
Login ..> CheckActive : <<include>>
Login ..> Token : <<include>>\n[Thông tin hợp lệ]
WrongInfo .up.> Login : <<extend>>\n[Sai Email hoặc mật khẩu]
LockedAccount .up.> Login : <<extend>>\n[Activate == false]
@enduml
```

> Hình 3.1: Usecase đăng nhập


Đặc tả Usecase đăng nhập

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Đăng nhập |
| Actor | Khách (Guest) |
| Mô tả | Người dùng sử dụng Email và Mật khẩu để xác thực danh tính và truy cập vào hệ thống. Hệ thống sẽ cấp phát JWT Token nếu xác thực thành công. |
| Pre-conditions | Actor truy cập vào trang đăng nhập và chưa thực hiện đăng nhập. |
| Post-conditions | Success: Hệ thống trả về JWT Token, chuyển hướng người dùng vào trang chủ/trang quản trị.<br>Fail: Hệ thống hiển thị thông báo lỗi tương ứng. |
| Luồng sự kiện chính | 1. Actor nhập Email và Mật khẩu.<br>2. Actor nhấn nút "Đăng nhập".<br>3. Hệ thống thực hiện kiểm tra Email tồn tại.<br>4. Hệ thống thực hiện kiểm tra mật khẩu chính xác.<br>5. Hệ thống thực hiện kiểm tra trạng thái khóa của tài khoản.<br>6. Nếu tất cả thông tin hợp lệ, hệ thống thực hiện tạo JWT Token.<br>7. Hệ thống hiển thị thông báo thành công và chuyển hướng Actor. |
| Luồng sự kiện phụ | - Nếu Email không tồn tại hoặc sai Mật khẩu: Hệ thống thực hiện thông báo sai thông tin.<br>- Nếu tài khoản chưa kích hoạt (Activate == false): Hệ thống thực hiện thông báo tài khoản bị khóa. |
| <Include Use Case><br>Quy trình Kiểm tra & Xác thực | - Kiểm tra Email: Hệ thống truy vấn cơ sở dữ liệu để xác nhận email có tồn tại.<br>- Kiểm tra Mật khẩu: Hệ thống so sánh mật khẩu nhập vào (đã hash) với mật khẩu trong cơ sở dữ liệu.<br>- Kiểm tra Trạng thái: Hệ thống xem xét trạng thái is_active của tài khoản.<br>- Tạo Token: Hệ thống sinh chuỗi JWT chứa thông tin người dùng để xác thực các phiên làm việc sau. |
| <Extend Use Case><br>Thông báo sai thông tin | Điều kiện: Khi quy trình kiểm tra Email hoặc Mật khẩu thất bại.<br>Hành động:<br>- Hệ thống hiển thị thông báo lỗi: "Tên đăng nhập hoặc mật khẩu không đúng".<br>- Hệ thống xóa trường mật khẩu để người dùng nhập lại. |
