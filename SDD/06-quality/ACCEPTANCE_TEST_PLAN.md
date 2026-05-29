# Acceptance Test Plan - Hotel Booking

## 1. Metadata

| Field | Value |
| --- | --- |
| Document type | Acceptance test plan |
| Product | Hotel Booking |
| Depends on | `SDD/01-product/PRD.md`, `SDD/01-product/IMPLEMENTATION_STATUS.md`, `SDD/02-business/BUSINESS_PROCESS.md`, `SDD/03-technical/API_CONTRACT.md` |
| Source thesis chapter | `thesis/chapters/04_thu_nghiem/` |
| Purpose | Convert thesis testing outline into executable SDD-level acceptance checks |

## 2. Test Data Baseline

Use deterministic test data so screenshots, API responses, and database checks can be compared between runs.

| Data set | Minimum data |
| --- | --- |
| Customer account | Active customer with valid email, phone, DOB, hashed password |
| Admin account | Active admin with access to admin dashboard |
| Locked account | User with `activate = false` for negative login test |
| Hotel | At least one active hotel with location, contact fields, star rating, and HTTPS image URL |
| Room | At least one active room with price, amount, capacity, image URL, and room amenities |
| Booking | One `BOOKED`, one `CHECKED_IN`, one `CHECKED_OUT`, and one `CANCELLED` booking where possible |
| Date range | Future `checkinDate` and `checkoutDate` where `checkoutDate > checkinDate` |

## 3. Acceptance Scenarios

Thesis Chapter 4 currently contains scenario outlines and placeholders for data/results. Therefore every scenario below starts as `Not executed - needs data/evidence`; do not mark pass/fail without captured evidence from section 5.

| Test ID | Thesis seed | SDD trace | Preconditions / data | Expected result | Priority | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AT-01 | TC-01 Đăng ký tài khoản | `FR-CUS-AUTH-001`, `BP-AUTH-001`, `API-AUTH-001` | Guest email not used before; valid phone, DOB, password | Account is created, default role is `CUSTOMER`, password is hashed, duplicate email is blocked | Must | Not executed - needs data/evidence |
| AT-02 | TC-02 Đăng nhập tài khoản | `FR-CUS-AUTH-002`, `BP-AUTH-002`, `API-AUTH-002` | Active Customer/Admin account exists | Valid credentials return JWT and user info; invalid or locked accounts return defined errors | Must | Not executed - needs data/evidence |
| AT-03 | TC-03 Tìm kiếm khách sạn | `FR-CUS-HOTEL-001..003`, `BP-DISC-001..003`, `API-HOTEL-001` | Active hotels exist for searched location/date | Search returns matching hotels only; empty search returns stable empty-state response | Must | Not executed - needs data/evidence |
| AT-04 | TC-03/TC-04 Kiểm tra phòng trống | `FR-CUS-ROOM-004`, `BP-DISC-008`, `API-ROOM-003` | Room inventory and overlapping bookings exist | Availability excludes `BOOKED`/`CHECKED_IN` conflicts and respects quantity/capacity | Must | Not executed - needs data/evidence |
| AT-05 | TC-04 Đặt phòng | `FR-CUS-BOOK-001..002`, `BP-BOOK-001..002`, `API-BOOK-001` | Customer logged in; room is available for future dates | Booking is created as `BOOKED`, reference is unique, total is server-calculated, success screen can show booking detail | Must | Not executed - needs data/evidence |
| AT-06 | TC-05 Hủy đặt phòng | `FR-CUS-BOOK-006`, `BP-BOOK-006`, `API-BOOK-005` | Customer owns a `BOOKED` booking | Cancel reason is stored, status becomes `CANCELLED`, room availability is released | Must | Not executed - needs data/evidence |
| AT-07 | TC-06 Quản lý khách sạn/phòng | `FR-ADM-HOTEL-*`, `FR-ADM-ROOM-*`, `BP-HR-*`, admin hotel/room APIs | Admin logged in and owns target hotel | Admin can create/update/delete or deactivate owned hotel/room; non-owner operations are blocked | Must | Not executed - needs data/evidence |
| AT-08 | Thesis function list: quản lý tiện nghi | `FR-ADM-AMENITY-*`, `BP-AMN-*`, `API-AMN-*` | Admin logged in; amenity catalog exists | Admin can CRUD amenities, assign/remove from hotel/room, and cannot delete in-use amenity | Must | Not executed - needs data/evidence |
| AT-09 | Thesis function list: lịch sử booking | `FR-CUS-BOOK-003..005`, `BP-BOOK-003..005`, `API-BOOK-002..004` | Customer has multiple bookings | Customer sees only own booking history and can open/lookup authorized booking detail | Must | Not executed - needs data/evidence |
| AT-10 | Admin vận hành booking | `FR-ADM-BOOK-001..004`, `BP-OPS-*`, `API-BOOK-006..008` | Admin logged in; booking in valid status | Admin can search bookings, check in with available room number, check out, or cancel within state-machine rules | Must | Not executed - needs data/evidence |
| AT-11 | NFR search/page load/responsive | `NFR-PERF-001..002`, `NFR-UX-001` | Representative dataset and desktop/tablet/mobile viewports | Search response is within target, key pages load within target, responsive layout remains usable | Should | Needs measured evidence |
| AT-12 | NFR auth/security | `NFR-SEC-001..005`, `NFR-TECH-003..005` | Protected endpoints and production-like config | JWT/RBAC/owner checks work; passwords are hashed; HTTPS is verified for production deployment | Should | HTTPS evidence pending |

## 4. Exception And Negative Scenarios

| Exception ID | Thesis seed | SDD trace | Expected handling |
| --- | --- | --- | --- |
| EX-01 | Email đăng ký đã tồn tại | `DUPLICATE_EMAIL` | Register returns `409` with standard error shape. |
| EX-02 | Đăng nhập sai email hoặc mật khẩu | `AUTH_INVALID_CREDENTIALS` | Login returns `401` without revealing whether email or password was wrong. |
| EX-03 | Tài khoản bị khóa | `AUTH_ACCOUNT_LOCKED` | Login returns `403`; protected actions remain unavailable. |
| EX-04 | Tìm kiếm không có khách sạn phù hợp | `BP-DISC-003` | API returns empty paginated list; UI shows empty state. |
| EX-05 | Đặt phòng khi phòng đã hết | `ROOM_UNAVAILABLE`, `ROOM_QUANTITY_EXCEEDED` | Booking is rejected after a fresh server-side availability check. |
| EX-06 | Khoảng ngày không hợp lệ | `VALIDATION_ERROR`, `BR-DATE-001..004` | API rejects past check-in or checkout not after check-in. |
| EX-07 | Hủy booking ngoài chính sách | `BOOKING_CANNOT_CANCEL` | `CHECKED_OUT`/already `CANCELLED` booking cannot be cancelled. |
| EX-08 | Người dùng không có quyền quản trị | `AUTH_FORBIDDEN` | Customer cannot access admin APIs or mutate resources not owned/allowed. |
| EX-09 | Admin gán số phòng đang có khách | `ROOM_NUMBER_OCCUPIED` | Check-in is rejected and existing booking assignment remains unchanged. |
| EX-10 | Xóa tiện ích đang được dùng | `AMENITY_IN_USE` | Delete is blocked until hotel/room mappings are removed. |
| EX-11 | Quên mật khẩu | `MVP-009` out of scope | UI/API should not advertise a working reset flow until feature is designed. |
| EX-12 | Thanh toán thật | `MVP-012` out of scope | System must not send real gateway callbacks, store payment credentials, or imply real money settlement in MVP. |

## 5. Evidence Checklist

For thesis or release verification, capture enough proof to support the status in `IMPLEMENTATION_STATUS.md`.

| Evidence type | Minimum proof |
| --- | --- |
| API evidence | Request URL/method, request body/query, response status, response body, error code where relevant |
| UI evidence | Screenshot of key success/error screens, especially booking success, booking cancel, admin booking, and responsive views |
| Data evidence | Database row or admin view showing status transitions, cancel reason, hashed password, and booking reference |
| Performance evidence | Search response timing and page-load timing with dataset size noted |
| Security evidence | Protected endpoint negative test, owner-check negative test, HTTPS production URL proof when deployed |

## 6. Source Map

| Thesis source | SDD use |
| --- | --- |
| `thesis/chapters/04_thu_nghiem/4_1_cac_kich_ban_thu_nghiem.md` | Seeds AT-01 to AT-07 |
| `thesis/chapters/04_thu_nghiem/4_2_ket_qua_thu_nghiem_cac_kich_ban.md` | Marks measured results as pending evidence |
| `thesis/chapters/04_thu_nghiem/4_3_xu_ly_cac_truong_hop_ngoai_le.md` | Seeds EX-01 to EX-08 |
| `thesis/chapters/05_ket_luan/5_1_ket_qua_doi_chieu_voi_muc_tieu.md` | Seeds status and NFR verification expectations |
