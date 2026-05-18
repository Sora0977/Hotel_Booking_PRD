# Use Case Catalog - Hotel Booking

## 1. Metadata

| Field | Value |
| --- | --- |
| Document type | Use Case Catalog |
| Product | Hotel Booking |
| Purpose | Complete use case inventory for AI-assisted maintenance |
| Related docs | `SDD/01-product/PRD.md`, `SDD/02-business/BUSINESS_PROCESS.md`, `SDD/02-business/business-processes/*.md`, `SDD/03-technical/API_CONTRACT.md` |

## 2. Actor Catalog

| Actor | Description |
| --- | --- |
| Guest | Visitor not logged in; can browse/search public data and register/login |
| Customer | Logged-in user who can book rooms and manage own booking/profile |
| Admin | Logged-in administrator who manages users, hotels, rooms, amenities, bookings |
| System | Backend/frontend system behavior |
| Cloudinary | External image storage service |

## 3. Customer/Guest Use Cases

| UC ID | Name | Actor | Priority | Related Process | Related APIs |
| --- | --- | --- | --- | --- | --- |
| UC-CUS-001 | Đăng ký tài khoản | Guest | Must | `BP-AUTH-001` | `API-AUTH-001` |
| UC-CUS-002 | Đăng nhập | Guest, Customer | Must | `BP-AUTH-002` | `API-AUTH-002` |
| UC-CUS-003 | Đăng xuất | Customer | Must | `BP-AUTH-003` | `API-AUTH-003` |
| UC-CUS-004 | Xem profile | Customer | Must | `BP-AUTH-004` | `API-USER-001` |
| UC-CUS-005 | Cập nhật profile | Customer | Must | `BP-AUTH-005` | `API-USER-002` |
| UC-CUS-006 | Đổi mật khẩu | Customer | Must | `BP-AUTH-006` | `API-AUTH-004` |
| UC-CUS-007 | Xóa/vô hiệu hóa tài khoản cá nhân | Customer | Should | `BP-AUTH-007` | `API-USER-003` |
| UC-CUS-008 | Xem danh sách khách sạn | Guest, Customer | Must | `BP-DISC-001` | `API-HOTEL-001` |
| UC-CUS-009 | Xem chi tiết khách sạn | Guest, Customer | Must | `BP-DISC-002` | `API-HOTEL-002` |
| UC-CUS-010 | Tìm kiếm khách sạn | Guest, Customer | Must | `BP-DISC-003` | `API-HOTEL-001` |
| UC-CUS-011 | Xem phòng của khách sạn | Guest, Customer | Must | `BP-DISC-004` | `API-HOTEL-003` |
| UC-CUS-012 | Xem danh sách tất cả phòng | Guest, Customer | Should | `BP-DISC-005` | `API-ROOM-001` |
| UC-CUS-013 | Xem chi tiết phòng | Guest, Customer | Must | `BP-DISC-006` | `API-ROOM-002` |
| UC-CUS-014 | Tìm phòng theo từ khóa/loại phòng | Guest, Customer | Should | `BP-DISC-007` | `API-ROOM-001` |
| UC-CUS-015 | Kiểm tra phòng trống | Guest, Customer | Must | `BP-DISC-008` | `API-ROOM-003` |
| UC-CUS-016 | Tạo booking mới | Customer | Must | `BP-BOOK-001` | `API-BOOK-001` |
| UC-CUS-017 | Xem đặt phòng thành công | Customer | Must | `BP-BOOK-002` | `API-BOOK-001` |
| UC-CUS-018 | Xem lịch sử booking | Customer | Must | `BP-BOOK-003` | `API-BOOK-002` |
| UC-CUS-019 | Tra cứu booking theo mã | Customer | Must | `BP-BOOK-004` | `API-BOOK-003` |
| UC-CUS-020 | Xem chi tiết booking | Customer | Must | `BP-BOOK-005` | `API-BOOK-004` |
| UC-CUS-021 | Hủy booking | Customer | Must | `BP-BOOK-006` | `API-BOOK-005` |

## 4. Admin Use Cases

| UC ID | Name | Actor | Priority | Related Process | Related APIs |
| --- | --- | --- | --- | --- | --- |
| UC-ADM-001 | Đăng nhập Admin | Admin | Must | `BP-AUTH-002` | `API-AUTH-002` |
| UC-ADM-002 | Xem dashboard quản trị | Admin | Should | Admin journey | N/A |
| UC-ADM-003 | Xem danh sách user | Admin | Must | `BP-AUTH-008` | `API-USER-004` |
| UC-ADM-004 | Khóa tài khoản user | Admin | Must | `BP-AUTH-009` | `API-USER-005` |
| UC-ADM-005 | Mở khóa tài khoản user | Admin | Must | `BP-AUTH-010` | `API-USER-006` |
| UC-ADM-006 | Xem khách sạn của tôi | Admin | Must | `BP-HR-001` | `API-HOTEL-004` |
| UC-ADM-007 | Thêm khách sạn | Admin | Must | `BP-HR-002` | `API-HOTEL-005` |
| UC-ADM-008 | Cập nhật khách sạn | Admin | Must | `BP-HR-003` | `API-HOTEL-006` |
| UC-ADM-009 | Xóa khách sạn | Admin | Must | `BP-HR-004` | `API-HOTEL-007` |
| UC-ADM-010 | Xem phòng theo khách sạn | Admin | Must | `BP-HR-005` | `API-HOTEL-003` |
| UC-ADM-011 | Thêm phòng | Admin | Must | `BP-HR-006` | `API-ROOM-004` |
| UC-ADM-012 | Cập nhật phòng | Admin | Must | `BP-HR-007` | `API-ROOM-005` |
| UC-ADM-013 | Xóa phòng | Admin | Must | `BP-HR-008` | `API-ROOM-006` |
| UC-ADM-014 | Xem toàn bộ booking | Admin | Must | `BP-OPS-001` | `API-BOOK-006` |
| UC-ADM-015 | Tìm kiếm/lọc booking | Admin | Should | `BP-OPS-002` | `API-BOOK-006` |
| UC-ADM-016 | Check-in booking | Admin | Must | `BP-OPS-003` | `API-BOOK-007` |
| UC-ADM-017 | Check-out booking | Admin | Must | `BP-OPS-004` | `API-BOOK-008` |
| UC-ADM-018 | Hủy booking bởi Admin | Admin | Must | `BP-OPS-005` | `API-BOOK-005` |
| UC-ADM-019 | Xem danh sách tiện ích | Admin | Must | `BP-AMN-001` | `API-AMN-001` |
| UC-ADM-020 | Tạo tiện ích | Admin | Must | `BP-AMN-002` | `API-AMN-002` |
| UC-ADM-021 | Cập nhật tiện ích | Admin | Must | `BP-AMN-003` | `API-AMN-003` |
| UC-ADM-022 | Xóa tiện ích | Admin | Must | `BP-AMN-004` | `API-AMN-004` |
| UC-ADM-023 | Gán tiện ích cho khách sạn | Admin | Must | `BP-AMN-005` | `API-AMN-005` |
| UC-ADM-024 | Gỡ tiện ích khỏi khách sạn | Admin | Must | `BP-AMN-006` | `API-AMN-006` |
| UC-ADM-025 | Gán tiện ích cho phòng | Admin | Must | `BP-AMN-007` | `API-AMN-007` |
| UC-ADM-026 | Gỡ tiện ích khỏi phòng | Admin | Must | `BP-AMN-008` | `API-AMN-008` |

## 5. Detailed Use Case Template

Use this template when adding a new use case:

| Field | Value |
| --- | --- |
| UC ID | `UC-<ROLE>-###` |
| Name | Short action name |
| Actor | Guest/Customer/Admin/System |
| Goal | What actor wants to accomplish |
| Preconditions | Required state before action |
| Trigger | Actor/system trigger |
| Inputs | User/system inputs |
| Outputs | Expected outputs |
| Main Flow | Step-by-step happy path |
| Alternate Flows | Branches and errors |
| Business Rules | Rule IDs |
| Data Touched | Entity/table list |
| API IDs | Related APIs |
| Screens | Related screens |
| Priority | Must/Should/Could |

## 6. Use Case Detail Matrix

| UC ID | Preconditions | Success Output | Main Failure Modes |
| --- | --- | --- | --- |
| UC-CUS-001 | Guest not logged in | Customer account active | Duplicate email, invalid input |
| UC-CUS-002 | Account exists | JWT and user info | Invalid credentials, account locked |
| UC-CUS-006 | Logged in, old password known | Password updated | Old password wrong, reused password |
| UC-CUS-015 | Valid search dates | Available rooms | Invalid date, no room, capacity exceeded |
| UC-CUS-016 | Logged in, room exists | Booking `BOOKED` | Invalid dates, room unavailable, quantity exceeded |
| UC-CUS-021 | Booking exists, owner | Booking `CANCELLED` | Not owner, checked out, already cancelled |
| UC-ADM-004 | Admin logged in, user exists | User locked | User not found, forbidden |
| UC-ADM-007 | Admin logged in | Hotel created | Duplicate hotel, missing image |
| UC-ADM-011 | Admin owns hotel | Room created | Not owner, invalid room data, upload failure |
| UC-ADM-016 | Admin logged in, booking exists | Booking `CHECKED_IN` | Room number occupied, invalid status |
| UC-ADM-017 | Admin logged in, booking checked in | Booking `CHECKED_OUT` | Booking not found, invalid status |
| UC-ADM-022 | Amenity exists and unused | Amenity deleted | Amenity in use, not found |

## 7. Feature Extension Notes

| New Feature | Use Case Updates Needed |
| --- | --- |
| Forgot password | Add Customer use case, auth API, token/email rules |
| Real payment | Add payment use cases, payment status, callback/webhook, refund flow |
| Review/rating | Add review use cases, rule that only completed bookings can review |
| Partner role | Split Admin use cases into System Admin and Hotel Partner |
| Promotion/discount | Add promotion CRUD and pricing rule extension |
| Recommendation | Add discovery use cases and personalization rules |
