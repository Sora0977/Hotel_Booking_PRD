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
| Hotel Partner | Future split from Admin if marketplace partner role is approved |

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

## 7. Chapter 3 Include/Extend Traceability

Chapter 3 models detailed use cases with PlantUML include/extend relationships. The table below keeps those relationships searchable without duplicating every diagram verbatim.

| Source Use Case | Include Relationships | Extend/Error Relationships | SDD Coverage |
| --- | --- | --- | --- |
| Đăng nhập | Check email, check password, check `activate`, issue JWT token | Invalid credentials, locked account | `UC-CUS-002`, `UC-ADM-001`, `BP-AUTH-002` |
| Đăng ký | Validate input, check duplicate email, hash password, assign default `CUSTOMER` role | Validation or duplicate email error | `UC-CUS-001`, `BP-AUTH-001` |
| Quản lý thông tin cá nhân | Verify session, get current user context, validate update form, verify old password, check password reuse | Validation error, wrong old password | `UC-CUS-003` to `UC-CUS-007`, `BP-AUTH-003` to `BP-AUTH-007` |
| Quản trị người dùng | Verify Admin session, check Admin role, find user, update `activate` | User not found, forbidden | `UC-ADM-003` to `UC-ADM-005`, `BP-AUTH-008` to `BP-AUTH-010` |
| Quản lý phòng | Check hotel owner, check room exists, upload image, add room amenities | Room not found, invalid image, permission error | `UC-ADM-010` to `UC-ADM-013`, `BP-HR-005` to `BP-HR-008` |
| Tra cứu phòng | Query DB, validate dates, view room type, keyword search | Invalid dates, not found, no result | `UC-CUS-011` to `UC-CUS-015`, `BP-DISC-004` to `BP-DISC-008` |
| Quản lý khách sạn | Check Admin, login/session, check hotel exists, owner check, duplicate name/location check, upload image | Permission error, duplicate hotel, missing image | `UC-ADM-006` to `UC-ADM-009`, `BP-HR-001` to `BP-HR-004` |
| Tra cứu khách sạn | Find hotel in DB, validate search dates, view hotel rooms/details | Invalid dates, hotel not found | `UC-CUS-008` to `UC-CUS-010`, `BP-DISC-001` to `BP-DISC-004` |
| Quản lý đặt phòng | Check Admin, login/session, assign room number, check room occupancy | Room occupied, booking not found | `UC-ADM-014` to `UC-ADM-018`, `BP-OPS-001` to `BP-OPS-005` |
| Đặt phòng | Login/session, validate booking dates, availability check, capacity/quantity check, calculate total price, generate reference code | Invalid dates, full room, room-hotel mismatch | `UC-CUS-016`, `UC-CUS-017`, `BP-BOOK-001`, `BP-BOOK-002` |
| Tra cứu và hủy booking | Login/session, owner/Admin check, status check, save cancel reason | Cannot cancel, permission error, code not found | `UC-CUS-019` to `UC-CUS-021`, `UC-ADM-018`, `BP-BOOK-004` to `BP-BOOK-006` |
| Quản lý tiện ích | Check Admin, login/session, check duplicate name, check exists, check in-use, check hotel owner for assignment/removal | Permission error, in-use, not found, duplicate name | `UC-ADM-019` to `UC-ADM-026`, `BP-AMN-001` to `BP-AMN-008` |

## 8. Feature Extension Notes

| New Feature | Use Case Updates Needed |
| --- | --- |
| Forgot password | Add Customer use case, auth API, token/email rules |
| Real payment/local payment | Add payment use cases, payment status, callback/webhook, refund flow, VietQR/MoMo/bank transfer/pay-at-property options |
| Review/rating | Add review use cases, rule that only completed `CHECKED_OUT` bookings can review, anti-fake-review checks |
| Partner role/marketplace commission | Split Admin use cases into System Admin and Hotel Partner, add commission/reporting/payout if approved |
| Partner quality control | Add partner score, violation handling, audit log, temporary hotel/partner suspension |
| Promotion/discount/loyalty | Add promotion CRUD, loyalty points, member offers, and pricing rule extension |
| Recommendation | Add discovery use cases and personalization rules |
| Support/chatbot | Add support ticket/FAQ/chatbot use cases and escalation rules |
