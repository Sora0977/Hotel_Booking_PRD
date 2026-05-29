# Business Process Documentation - Hotel Booking

## 1. Mục Đích

- Tài liệu này là file điều hướng nghiệp vụ chính cho hệ thống Hotel Booking.
- Chi tiết nghiệp vụ được chia nhỏ theo module trong thư mục `SDD/02-business/business-processes/`.
- Mỗi file con mô tả:
  - Actor.
  - Trigger.
  - Preconditions.
  - Input/Output.
  - Main flow.
  - Alternate/Error flows.
  - Business rules.
  - Data touchpoints.
  - Related screens.

## 2. Cấu Trúc Tài Liệu

| File | Module | Nội dung |
| --- | --- | --- |
| `02-business/business-processes/01-auth-and-account.md` | Tài khoản và xác thực | Đăng ký, đăng nhập, đăng xuất, profile, đổi mật khẩu, xóa tài khoản, admin khóa/mở khóa user |
| `02-business/business-processes/02-discovery-and-availability.md` | Tra cứu khách sạn/phòng | Danh sách khách sạn, chi tiết khách sạn, danh sách phòng, chi tiết phòng, tìm kiếm, kiểm tra phòng trống |
| `02-business/business-processes/03-booking-lifecycle.md` | Vòng đời đặt phòng của Customer | Tạo booking, tính tiền, sinh mã, lịch sử, tra cứu mã, xem chi tiết, hủy booking |
| `02-business/business-processes/04-admin-hotel-room-management.md` | Admin quản lý khách sạn/phòng | CRUD khách sạn, CRUD phòng, upload ảnh, owner check, gán tiện ích |
| `02-business/business-processes/05-admin-booking-operations.md` | Admin vận hành booking | Xem toàn bộ booking, check-in, check-out, gán số phòng, hủy booking |
| `02-business/business-processes/06-amenity-management.md` | Quản lý tiện ích | CRUD tiện ích, gán/gỡ tiện ích khỏi khách sạn/phòng, chặn xóa khi đang sử dụng |
| `02-business/business-processes/07-business-rules-and-edge-cases.md` | Rule tổng hợp | State machine, quyền truy cập, validation, lỗi nghiệp vụ, edge cases |
| `03-technical/API_CONTRACT.md` | API contract | Endpoint, request/response, access control, error code, mapping sang process |
| `03-technical/ENTITY_SCHEMA.md` | Entity schema | Table, field, relation, enum, constraint, index, delete policy |
| `01-product/USE_CASE_CATALOG.md` | Use case catalog | Danh sách đầy đủ use case theo role, process, API, priority |
| `01-product/IMPLEMENTATION_STATUS.md` | Implementation status | Ma trận đạt/chưa đạt từ luận văn và ranh giới roadmap |
| `05-guides/AI_MAINTENANCE_GUIDE.md` | AI maintenance guide | Thứ tự đọc tài liệu, checklist khi thêm feature, guardrails cho AI |
| `04-diagrams/CORE_FLOW_DIAGRAMS.md` | Core diagrams | Mermaid diagrams cho entity và flow chính |
| `06-quality/ACCEPTANCE_TEST_PLAN.md` | Acceptance tests | Kịch bản kiểm thử, ngoại lệ và evidence từ Chương 4 |

## 3. Module Map

| Module ID | Module | Primary Actor | Supporting Actor | Related Entities |
| --- | --- | --- | --- | --- |
| BP-AUTH | Tài khoản và xác thực | Guest, Customer, Admin | System | `user`, `role`, `user_role` |
| BP-DISCOVERY | Tra cứu khách sạn/phòng | Guest, Customer | System | `hotel`, `room`, `image`, `amenity`, `booking` |
| BP-BOOKING | Đặt phòng | Customer | Admin, System | `booking`, `booking_room`, `room`, `hotel`, `user` |
| BP-HOTEL-ROOM | Quản lý khách sạn/phòng | Admin | Cloudinary, System | `hotel`, `room`, `image`, `amenity` |
| BP-OPS | Vận hành booking | Admin | Customer, System | `booking`, `room`, `user` |
| BP-AMENITY | Quản lý tiện ích | Admin | System | `amenity`, `hotel_amenity`, `room_amenity` |

## 4. End-To-End Customer Journey

| Step | Business Action | Document |
| --- | --- | --- |
| 1 | Guest đăng ký hoặc đăng nhập | `01-auth-and-account.md` |
| 2 | Customer/Guest tìm khách sạn theo địa điểm/ngày | `02-discovery-and-availability.md` |
| 3 | Customer/Guest xem chi tiết khách sạn và phòng | `02-discovery-and-availability.md` |
| 4 | Customer kiểm tra phòng trống | `02-discovery-and-availability.md` |
| 5 | Customer tạo booking | `03-booking-lifecycle.md` |
| 6 | Customer nhận mã booking và xem màn hình thành công | `03-booking-lifecycle.md` |
| 7 | Customer xem lịch sử hoặc tra cứu booking theo mã | `03-booking-lifecycle.md` |
| 8 | Customer hủy booking nếu hợp lệ | `03-booking-lifecycle.md` |

## 5. End-To-End Admin Journey

| Step | Business Action | Document |
| --- | --- | --- |
| 1 | Admin đăng nhập | `01-auth-and-account.md` |
| 2 | Admin quản lý user và trạng thái tài khoản | `01-auth-and-account.md` |
| 3 | Admin tạo/cập nhật khách sạn | `04-admin-hotel-room-management.md` |
| 4 | Admin tạo/cập nhật phòng cho khách sạn | `04-admin-hotel-room-management.md` |
| 5 | Admin tạo/gán/gỡ tiện ích | `06-amenity-management.md` |
| 6 | Admin xem toàn bộ booking | `05-admin-booking-operations.md` |
| 7 | Admin check-in, gán số phòng | `05-admin-booking-operations.md` |
| 8 | Admin check-out hoặc hủy booking | `05-admin-booking-operations.md` |

## 6. Core State Machines

### 6.1 Booking Status

| Current Status | Trigger | Actor | Next Status | Rule |
| --- | --- | --- | --- | --- |
| None | Create booking | Customer/Admin | `BOOKED` | Room available, valid dates, authenticated |
| `BOOKED` | Check-in | Admin | `CHECKED_IN` | Assign available physical room number |
| `CHECKED_IN` | Check-out | Admin | `CHECKED_OUT` | Booking exists and active |
| `BOOKED` | Cancel | Customer/Admin | `CANCELLED` | Customer owns booking or actor is Admin |
| `CHECKED_OUT` | Cancel | Customer/Admin | Not allowed | Completed booking cannot be cancelled |
| `CANCELLED` | Cancel | Customer/Admin | Not allowed | Already cancelled |

### 6.2 Account Status

| Current Status | Trigger | Actor | Next Status | Rule |
| --- | --- | --- | --- | --- |
| New | Register | Guest | Active | Default role `CUSTOMER` |
| Active | Lock account | Admin | Inactive/Locked | User cannot login |
| Inactive/Locked | Unlock account | Admin | Active | User can login again |
| Active | Delete own account | Customer | Deleted/Inactive | Requires confirmation |

## 7. Source References

| Source ID | Path                                                                                                                | Purpose                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| SRC-PRD   | `SDD/01-product/PRD.md`                                                                                             | Product requirements and business rules                  |
| SRC-TECH  | `SDD/03-technical/TECH_SPEC.md`                                                                                     | Entities, APIs, architecture, transaction notes          |
| SRC-CH1   | `thesis/chapters/01_mo_dau/1_3_noi_dung_pham_vi_thuc_hien.md`<br>`thesis/chapters/01_mo_dau/1_4_ket_qua_can_dat.md` | Scope, functional and non-functional targets             |
| SRC-CH2   | `thesis/chapters/02_phuong_phap_thuc_hien/2_4_phan_tich_yeu_cau.md`                                                 | Core business processes                                  |
| SRC-CH3   | `thesis/chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/`<br>`thesis/chapters/03_thiet_ke/3_3_he_thong_man_hinh.md`          | Use cases, sequence diagrams, activity diagrams, screens |
| SRC-CH4   | `thesis/chapters/04_thu_nghiem/`                                                                                    | Acceptance scenarios and exception cases                 |
| SRC-CH5   | `thesis/chapters/05_ket_luan/`                                                                                      | Completed and not completed scope, roadmap gaps          |
