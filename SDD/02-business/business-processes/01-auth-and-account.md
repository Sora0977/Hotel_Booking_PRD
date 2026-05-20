# 01 - Tài Khoản Và Xác Thực

## 1. Scope

| Process ID | Process | Actor |
| --- | --- | --- |
| BP-AUTH-001 | Đăng ký tài khoản | Guest |
| BP-AUTH-002 | Đăng nhập | Guest, Customer, Admin |
| BP-AUTH-003 | Đăng xuất | Customer, Admin |
| BP-AUTH-004 | Xem profile | Customer, Admin |
| BP-AUTH-005 | Cập nhật profile | Customer, Admin |
| BP-AUTH-006 | Đổi mật khẩu | Customer, Admin |
| BP-AUTH-007 | Xóa/vô hiệu hóa tài khoản cá nhân | Customer, Admin |
| BP-AUTH-008 | Admin xem danh sách user | Admin |
| BP-AUTH-009 | Admin khóa tài khoản user | Admin |
| BP-AUTH-010 | Admin mở khóa tài khoản user | Admin |

## 2. BP-AUTH-001 - Đăng Ký Tài Khoản

| Field | Detail |
| --- | --- |
| Actor | Guest |
| Trigger | Guest nhấn nút đăng ký |
| Preconditions | Guest chưa đăng nhập |
| Inputs | `fullName`, `email`, `phone`, `dob`, `password` |
| Outputs | User mới, role `CUSTOMER`, trạng thái active |
| Data touched | `user`, `role`, `user_role` |
| Related screens | Đăng ký |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Guest nhập thông tin đăng ký. |
| 2 | Frontend gửi request đăng ký. |
| 3 | System validate các trường bắt buộc và định dạng dữ liệu. |
| 4 | System kiểm tra email đã tồn tại trong `user`. |
| 5 | Nếu email chưa tồn tại, system hash mật khẩu bằng BCrypt. |
| 6 | System tạo user mới với trạng thái active. |
| 7 | System gán role mặc định `CUSTOMER`. |
| 8 | System lưu user và mapping role vào database. |
| 9 | System trả thông báo đăng ký thành công. |

### Alternate/Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Invalid input | Thiếu trường bắt buộc hoặc sai định dạng | Trả `VALIDATION_ERROR`, yêu cầu nhập lại |
| Duplicate email | Email đã tồn tại | Trả `DUPLICATE_EMAIL`, không tạo user |
| Password invalid | Mật khẩu không đạt rule | Trả lỗi validation |

### Business Rules

| Rule ID | Rule |
| --- | --- |
| BR-AUTH-001 | Email là định danh đăng nhập và phải unique. |
| BR-AUTH-002 | Mật khẩu không được lưu dạng plain text. |
| BR-AUTH-003 | User mới có role mặc định `CUSTOMER`. |
| BR-AUTH-004 | User mới được active ngay sau khi đăng ký, trừ khi sau này bổ sung email verification. |

## 3. BP-AUTH-002 - Đăng Nhập

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer, Admin |
| Trigger | Người dùng nhấn nút đăng nhập |
| Preconditions | Người dùng có tài khoản |
| Inputs | `email`, `password` |
| Outputs | JWT token, user info, role |
| Data touched | `user`, `role`, `user_role` |
| Related screens | Đăng nhập |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor nhập email và mật khẩu. |
| 2 | Frontend gửi request login. |
| 3 | System tìm user theo email. |
| 4 | System kiểm tra tài khoản có tồn tại. |
| 5 | System kiểm tra trạng thái `activate`. |
| 6 | System so khớp mật khẩu nhập vào với password hash. |
| 7 | Nếu hợp lệ, system tạo JWT chứa định danh và role. |
| 8 | System trả token và user info. |
| 9 | Frontend lưu token và điều hướng theo role. |

### Alternate/Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Invalid credentials | Email không tồn tại hoặc mật khẩu sai | Trả lỗi đăng nhập chung, không tiết lộ field nào sai |
| Locked account | `activate = false` | Trả lỗi tài khoản bị khóa |
| Missing role | User không có role hợp lệ | Trả lỗi phân quyền hoặc yêu cầu admin xử lý |

### Business Rules

| Rule ID | Rule |
| --- | --- |
| BR-AUTH-005 | JWT dùng cho các request cần xác thực sau đăng nhập. |
| BR-AUTH-006 | Tài khoản inactive/locked không được đăng nhập. |
| BR-AUTH-007 | Token theo tài liệu gốc có hiệu lực 6 tháng. |

## 4. BP-AUTH-003 - Đăng Xuất

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor chọn đăng xuất |
| Preconditions | Actor đang đăng nhập |
| Inputs | Current session/token |
| Outputs | JWT blacklisted, client session cleared |
| Data touched | Token blacklist store (`Redis`/DB) |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor nhấn đăng xuất. |
| 2 | Frontend gửi `POST /api/auth/logout` kèm JWT hiện tại. |
| 3 | Backend nhận request logout, lấy JWT hiện tại và lưu vào Token Blacklist (`Redis`/DB) để chặn các request sau này. |
| 4 | Backend trả logout success. |
| 5 | Frontend xóa token khỏi storage. |
| 6 | Frontend xóa user context. |
| 7 | Frontend điều hướng về trang public/login. |

## 5. BP-AUTH-004 - Xem Profile

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor mở trang thông tin cá nhân |
| Preconditions | Actor đã đăng nhập |
| Inputs | JWT/current user context |
| Outputs | Profile của current user |
| Data touched | `user` |
| Related screens | Thông tin cá nhân |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor mở profile. |
| 2 | Frontend gọi API current user. |
| 3 | System lấy user ID từ JWT. |
| 4 | System truy vấn user hiện tại. |
| 5 | System trả dữ liệu profile. |
| 6 | Frontend hiển thị profile. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Expired token | Token không hợp lệ | Điều hướng login |
| User missing | User ID trong token không còn tồn tại | Trả `RESOURCE_NOT_FOUND`, yêu cầu đăng nhập lại |

## 6. BP-AUTH-005 - Cập Nhật Profile

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor nhấn lưu thay đổi profile |
| Preconditions | Actor đã đăng nhập |
| Inputs | Profile fields |
| Outputs | Updated profile |
| Data touched | `user` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor chỉnh sửa thông tin cá nhân. |
| 2 | Frontend validate cơ bản. |
| 3 | Frontend gửi request update. |
| 4 | System lấy current user từ JWT. |
| 5 | System validate dữ liệu. |
| 6 | System cập nhật user record. |
| 7 | System trả profile mới. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Invalid phone/date/name | Dữ liệu sai định dạng | Trả validation error |
| Email change conflict | Nếu cho đổi email và email đã tồn tại | Trả duplicate error |

## 7. BP-AUTH-006 - Đổi Mật Khẩu

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor nhấn đổi mật khẩu |
| Preconditions | Actor đã đăng nhập và nhớ mật khẩu cũ |
| Inputs | `oldPassword`, `newPassword`, `confirmPassword` |
| Outputs | Password hash mới |
| Data touched | `user.password` |
| Related screens | Thông tin cá nhân/đổi mật khẩu |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor nhập mật khẩu cũ, mật khẩu mới, xác nhận mật khẩu mới. |
| 2 | System lấy current user. |
| 3 | System so khớp mật khẩu cũ với hash đang lưu. |
| 4 | System kiểm tra mật khẩu mới không trùng mật khẩu cũ. |
| 5 | System kiểm tra confirm password khớp. |
| 6 | System hash mật khẩu mới. |
| 7 | System cập nhật `user.password`. |
| 8 | System trả thông báo thành công. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Wrong old password | Mật khẩu cũ sai | Trả lỗi, không đổi mật khẩu |
| Same password | Mật khẩu mới trùng mật khẩu cũ | Trả lỗi nghiệp vụ |
| Confirm mismatch | Confirm password không khớp | Trả validation error |

## 8. BP-AUTH-007 - Xóa/Vô Hiệu Hóa Tài Khoản Cá Nhân

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor xác nhận xóa tài khoản |
| Preconditions | Actor đã đăng nhập |
| Inputs | Confirmation |
| Outputs | Account deleted/inactive |
| Data touched | `user.activate` hoặc user record |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor chọn xóa tài khoản. |
| 2 | System hiển thị cảnh báo xác nhận. |
| 3 | Actor xác nhận. |
| 4 | System lấy current user. |
| 5 | System kiểm tra ràng buộc booking chưa hoàn tất nếu rule được bật. |
| 6 | System soft-delete hoặc chuyển `activate = false`. |
| 7 | Frontend đăng xuất actor. |

### Open Policy

| Question | Impact |
| --- | --- |
| Xóa hard delete hay soft delete? | Ảnh hưởng lịch sử booking và audit |
| Có chặn xóa nếu có booking chưa hoàn tất không? | Ảnh hưởng vận hành booking |

## 9. BP-AUTH-008 - Admin Xem Danh Sách User

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin mở module quản lý tài khoản |
| Preconditions | Actor có role `ADMIN` |
| Inputs | Pagination/search filters |
| Outputs | User list |
| Data touched | `user`, `role`, `user_role` |
| Related screens | Quản lý tài khoản |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin mở màn hình quản lý tài khoản. |
| 2 | System kiểm tra JWT và role Admin. |
| 3 | System truy vấn danh sách user. |
| 4 | System trả danh sách user và trạng thái. |
| 5 | Frontend hiển thị danh sách. |

## 10. BP-AUTH-009 - Admin Khóa Tài Khoản

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn khóa tài khoản |
| Preconditions | Actor có role `ADMIN`, user mục tiêu tồn tại |
| Inputs | `userId` |
| Outputs | User inactive/locked |
| Data touched | `user.activate` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin chọn user cần khóa. |
| 2 | System kiểm tra quyền Admin. |
| 3 | System tìm user theo ID. |
| 4 | System cập nhật `activate = false`. |
| 5 | System trả thông báo khóa thành công. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| User not found | `userId` không tồn tại | Trả `RESOURCE_NOT_FOUND` |
| Not admin | Actor không có role Admin | Trả `AUTH_FORBIDDEN` |

## 11. BP-AUTH-010 - Admin Mở Khóa Tài Khoản

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn mở khóa tài khoản |
| Preconditions | Actor có role `ADMIN`, user mục tiêu tồn tại |
| Inputs | `userId` |
| Outputs | User active |
| Data touched | `user.activate` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin chọn user cần mở khóa. |
| 2 | System kiểm tra quyền Admin. |
| 3 | System tìm user theo ID. |
| 4 | System cập nhật `activate = true`. |
| 5 | System trả thông báo mở khóa thành công. |
