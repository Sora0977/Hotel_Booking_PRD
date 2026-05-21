---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.1.4"
title: "3.2.1.4 Usecase quản trị người dùng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

#### 3.2.1.4 Usecase quản trị người dùng

```plantuml
@startuml
!theme plain
left to right direction

actor "Quản trị viên (Admin)" as Admin

rectangle "Hệ thống Quản trị người dùng" {
  usecase "Quản trị người dùng" as UserAdmin
  usecase "Xem danh sách người dùng" as ListUsers
  usecase "Khóa tài khoản người dùng" as LockUser
  usecase "Mở khóa tài khoản người dùng" as UnlockUser
  usecase "Xác thực phiên Admin" as VerifyAdminSession
  usecase "Kiểm tra quyền Admin" as CheckAdmin
  usecase "Tìm User theo ID" as FindUser
  usecase "Cập nhật trạng thái Activate" as UpdateActive
  usecase "Thông báo User không tồn tại" as UserNotFound
}

Admin --> UserAdmin
ListUsers -up-|> UserAdmin
LockUser -up-|> UserAdmin
UnlockUser -up-|> UserAdmin
UserAdmin ..> VerifyAdminSession : <<include>>
UserAdmin ..> CheckAdmin : <<include>>
LockUser ..> FindUser : <<include>>
LockUser ..> UpdateActive : <<include>>
UnlockUser ..> FindUser : <<include>>
UnlockUser ..> UpdateActive : <<include>>
UserNotFound .up.> LockUser : <<extend>>\n[Không tìm thấy ID]
UserNotFound .up.> UnlockUser : <<extend>>\n[Không tìm thấy ID]
@enduml
```

> Hình 3.4: Usecase quản lý người dùng


Đặc tả Usecase xem danh sách người dùng

| Mục                                            | Nội dung                                                                                                                                                                                                              |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tên Use case                                   | Xem danh sách người dùng                                                                                                                                                                                              |
| Actor                                          | Quản trị viên (Admin)                                                                                                                                                                                                 |
| Mô tả                                          | Admin xem toàn bộ danh sách tài khoản người dùng trong hệ thống để phục vụ công tác quản trị, giám sát và xử lý tài khoản.                                                                                            |
| Pre-conditions                                 | - Actor đã đăng nhập vào hệ thống.<br>- Actor có quyền Admin.                                                                                                                                                         |
| Post-conditions                                | Success: Danh sách người dùng được hiển thị đầy đủ.<br>Fail: Hệ thống từ chối truy cập nếu Actor không có quyền.                                                                                                      |
| Luồng sự kiện chính                            | 1. Actor truy cập mục "Quản lý người dùng".<br>2. Hệ thống thực hiện kiểm tra quyền Admin.<br>3. Nếu hợp lệ, hệ thống truy vấn danh sách User.<br>4. Hệ thống hiển thị danh sách người dùng kèm trạng thái tài khoản. |
| Luồng sự kiện phụ                              | - Nếu Actor không có quyền Admin: Hệ thống thực hiện thông báo không có quyền truy cập.                                                                                                                               |
| <Include Use Case><br>Quy trình Xác thực quyền | - Xác thực phiên Admin: Đảm bảo Actor đã xác thực phiên làm việc hợp lệ.<br>- Kiểm tra quyền Admin: Xác minh Actor có vai trò Admin trước khi cho phép truy cập module quản trị.                                      |

Đặc tả Usecase khóa tài khoản người dùng

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Khóa tài khoản người dùng |
| Actor | Quản trị viên (Admin) |
| Mô tả | Admin thực hiện khóa tài khoản của một người dùng cụ thể để ngăn họ đăng nhập vào hệ thống (ví dụ: do vi phạm chính sách). |
| Pre-conditions | - Actor đã đăng nhập và có quyền Admin.<br><br>- Tài khoản người dùng cần khóa đang ở trạng thái hoạt động (Active). |
| Post-conditions | Success: Trạng thái tài khoản chuyển sang "Locked" (hoặc Inactive).<br>Fail: Hệ thống báo lỗi nếu người dùng không tồn tại. |
| Luồng sự kiện chính | 1. Actor tìm kiếm và chọn người dùng cần khóa từ danh sách.<br>2. Actor nhấn nút "Khóa tài khoản".<br>3. Hệ thống thực hiện tìm User theo ID.<br>4. Nếu tìm thấy, hệ thống thực hiện cập nhật trạng thái Activate thành False (Khóa).<br>5. Hệ thống hiển thị thông báo "Đã khóa tài khoản thành công". |
| Luồng sự kiện phụ | - Nếu ID người dùng không tồn tại: Hệ thống thực hiện thông báo User không tồn tại. |
| <Include Use Case><br>Quy trình Xử lý | - Tìm User theo ID: Xác định bản ghi người dùng trong CSDL.<br>- Cập nhật trạng thái Activate: Thay đổi giá trị cờ trạng thái của người dùng. |
| <Extend Use Case><br>Thông báo User không tồn tại | Điều kiện: Khi không tìm thấy ID người dùng.<br>Hành động: Hiển thị lỗi và hủy thao tác. |
| <Extend Use Case><br>Thông báo không có quyền | Điều kiện: Khi quy trình kiểm tra quyền sở hữu thất bại.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo bảo mật: "Bạn không có quyền thao tác trên đơn hàng này". |

Đặc tả Usecase mở khóa tài khoản người dùng

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Mở khóa tài khoản người dùng |
| Actor | Quản trị viên (Admin) |
| Mô tả | Admin khôi phục quyền truy cập cho một tài khoản người dùng đã bị khóa trước đó. |
| Pre-conditions | - Actor đã đăng nhập và có quyền Admin.<br>- Tài khoản người dùng đang ở trạng thái bị khóa. |
| Post-conditions | Success: Trạng thái tài khoản chuyển sang "Active".<br>Fail: Hệ thống báo lỗi nếu người dùng không tồn tại. |
| Luồng sự kiện chính | 1. Actor tìm kiếm và chọn người dùng bị khóa từ danh sách.<br>2. Actor nhấn nút "Mở khóa tài khoản".<br>3. Hệ thống thực hiện tìm User theo ID.<br>4. Nếu tìm thấy, hệ thống thực hiện cập nhật trạng thái Activate thành True (Hoạt động).<br>5. Hệ thống hiển thị thông báo "Đã mở khóa tài khoản thành công". |
| Luồng sự kiện phụ | - Nếu ID người dùng không tồn tại: Hệ thống thực hiện thông báo User không tồn tại. |
| <Include Use Case><br>Quy trình Xử lý | - Tìm User theo ID: Xác định bản ghi người dùng.<br>- Cập nhật trạng thái Activate: Thay đổi giá trị cờ trạng thái của người dùng về hoạt động. |
| <Extend Use Case> Thông báo User không tồn tại | Điều kiện: Khi không tìm thấy ID người dùng.<br>Hành động: Hiển thị lỗi và hủy thao tác. |
| <Extend Use Case><br>Thông báo không có quyền | Điều kiện: Khi quy trình kiểm tra quyền sở hữu thất bại.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo bảo mật: "Bạn không có quyền thao tác trên đơn hàng này". |
