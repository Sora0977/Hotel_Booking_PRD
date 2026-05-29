# Implementation Status And Thesis Gap Matrix - Hotel Booking

## 1. Metadata

| Field | Value |
| --- | --- |
| Document type | Implementation status / thesis alignment |
| Product | Hotel Booking |
| Depends on | `SDD/01-product/PRD.md`, `SDD/01-product/USE_CASE_CATALOG.md` |
| Source thesis chapters | `thesis/chapters/01_mo_dau/`, `thesis/chapters/04_thu_nghiem/`, `thesis/chapters/05_ket_luan/` |
| Purpose | Preserve what the thesis marks as achieved, not achieved, pending evidence, or future roadmap |

## 2. How To Use This Document

- Use `PRD.md` to decide whether a capability is in MVP scope.
- Use this file to know whether the thesis says that capability was implemented, partially implemented, not implemented, or still lacks evidence.
- Do not promote a `Not achieved` item into MVP implementation without updating PRD, use cases, business process, API contract, schema, diagrams, and tests.

## 3. Functional Completion Matrix

| Thesis capability | Thesis status | Canonical SDD decision | Primary SDD trace | Notes / missing work |
| --- | --- | --- | --- | --- |
| Admin xem danh sách, khóa, mở khóa tài khoản | Achieved | In canonical MVP | `FR-ADM-USER-001..003`, `UC-ADM-003..005`, `BP-AUTH-008..010`, `API-USER-004..006` | This is the part fully modeled by Chapter 3 detailed use cases and current SDD. |
| Admin thêm/sửa/xóa tài khoản người dùng | Thesis target/status says achieved, but detailed use case coverage is incomplete | Scope conflict / not canonical until approved | `MVP-007`, `OQ-011` in `PRD.md` | Thesis Chapter 1/5 says admin can add/delete/edit/lock/unlock accounts, while current detailed use case and API model only cover list/lock/unlock. Add create/update/delete user only after policy, validation, audit, and delete/deactivate rules are approved. |
| Quản lý khách sạn | Achieved | In MVP | `FR-ADM-HOTEL-001..004`, `UC-ADM-006..009`, `BP-HR-001..004`, `API-HOTEL-004..007` | Thesis mentions Cloudinary image upload; SDD keeps HTTPS image URL constraints. |
| Quản lý phòng khách sạn | Achieved | In MVP | `FR-ADM-ROOM-001..004`, `UC-ADM-010..013`, `BP-HR-005..008`, `API-ROOM-004..006` | Owner check and active/delete policy must stay aligned with business rules. |
| Quản lý tiện nghi | Achieved | In MVP | `FR-ADM-AMENITY-001..005`, `UC-ADM-019..026`, `BP-AMN-001..008`, `API-AMN-001..008` | Includes catalog CRUD and hotel/room assignment/removal. |
| Đăng ký tài khoản | Achieved | In MVP | `FR-CUS-AUTH-001`, `UC-CUS-001`, `BP-AUTH-001`, `API-AUTH-001` | Thesis notes validation is basic; SDD requires stricter validation from API Contract. |
| Đăng nhập tài khoản | Achieved | In MVP | `FR-CUS-AUTH-002`, `FR-ADM-AUTH-001`, `UC-CUS-002`, `UC-ADM-001`, `API-AUTH-002` | Account lock handling is required. |
| Quên mật khẩu | Not achieved | Out of MVP / roadmap only | `MVP-009`, `USE_CASE_CATALOG` Feature Extension Notes | Needs reset token entity or table, email/OTP policy, expiry rule, rate limit, and new auth APIs. |
| Quản lý thông tin cá nhân | Achieved | In MVP | `FR-CUS-PROFILE-001..004`, `UC-CUS-004..007`, `BP-AUTH-004..007`, `API-USER-001..003` | Delete/deactivate behavior remains policy-sensitive. |
| Tìm kiếm khách sạn | Achieved | In MVP | `FR-CUS-HOTEL-001..003`, `UC-CUS-008..010`, `BP-DISC-001..003`, `API-HOTEL-001..002` | Advanced filters from Booking.com/Traveloka remain roadmap. |
| Đặt phòng | Achieved | In MVP | `FR-CUS-BOOK-001..002`, `UC-CUS-016..017`, `BP-BOOK-001..002`, `API-BOOK-001` | Payment is simulated/manual only; no real gateway side effects. |
| Xem lịch sử đặt phòng | Achieved | In MVP | `FR-CUS-BOOK-003..005`, `UC-CUS-018..020`, `BP-BOOK-003..005`, `API-BOOK-002..004` | Reference lookup is authenticated by default. |
| Hủy đặt phòng | Achieved | In MVP | `FR-CUS-BOOK-006`, `FR-ADM-BOOK-004`, `BP-BOOK-006`, `BP-OPS-005`, `API-BOOK-005` | Must persist cancel reason and obey booking state machine. |
| Thống kê doanh thu | Not achieved | Out of MVP / reporting roadmap | `MVP-010`, `OQ-007`, `USE_CASE_CATALOG` Feature Extension Notes | Needs reporting module, date aggregation, payment/revenue source of truth, admin/partner access rules, and export policy. |

## 4. Non-Functional Completion Matrix

| Thesis NFR | Thesis status | SDD treatment | Required evidence before marking production-ready |
| --- | --- | --- | --- |
| Search response `<= 3s` | Achieved | `NFR-PERF-001`, `NFR-TECH-001` | Timed search run with representative hotel/room/booking data. |
| Main/detail page load `<= 2s` | Achieved | `NFR-PERF-002`, `NFR-TECH-002` | Browser timing or Lighthouse-style measurement for home and detail pages. |
| Payment confirmation `5-7s` | Not achieved | `NFR-PERF-003` only applies if online payment is approved | Real/sandbox payment gateway test with callback timing. |
| Password hashing | Achieved | `NFR-SEC-001`, `NFR-TECH-003` | Verify persisted password is BCrypt hash and raw password is never logged. |
| Role-based authorization | Achieved | `NFR-SEC-003`, `NFR-TECH-004` | Negative permission tests for Customer/Admin and owner checks. |
| Payment security | Thesis marks achieved, but real payment is not implemented | Canonical SDD: no real payment in MVP; reassess when payment domain exists | Gateway certification/security checklist, webhook verification, and no sensitive payment storage. |
| HTTPS/SSL-TLS | Not achieved in current implementation notes | Production hardening requirement | Deployment proof that production URL and API use HTTPS only. |
| API authentication | Achieved | JWT/RBAC in `TECH_SPEC` and `API_CONTRACT` | Protected endpoint tests with missing, expired, invalid, and valid JWT. |
| Maintenance process | Achieved as a process requirement | `AI_MAINTENANCE_GUIDE.md` | Future changes keep traceability updated. |
| Responsive UI | Achieved in thesis | `NFR-UX-001` | Desktop/tablet/mobile screenshots or viewport test evidence. |
| Modular design | Achieved | `NFR-OPS-001`, `NFR-TECH-008` | Code organization keeps controller/service/repository/module boundaries. |

## 5. Known Gaps And Roadmap Boundaries

| Gap / roadmap item | Current decision | Minimum SDD updates before implementation |
| --- | --- | --- |
| Forgot password | Out of MVP | Add Customer use case, auth process, reset token schema, email/OTP policy, API contract, rate-limit/error rules, tests. |
| Real payment via VNPAY/MoMo/VietQR/bank transfer | Out of MVP | Add payment entity/status, payment lifecycle, callback/webhook verification, reconciliation, refund rules, payment NFR/security tests. |
| Revenue report / báo biểu | Out of MVP | Add reporting requirements, reporting API, aggregation rules, permission split, screen inventory, export format, acceptance tests. |
| HTTPS production rollout | Production hardening | Add deployment checklist and environment requirements; verify all production assets/API endpoints use HTTPS. |
| Recommendation / personalization | Roadmap | Add recommendation use cases, data collection rules, privacy constraints, ranking behavior, fallback behavior, and tests. |
| Breadcrumb / navigation clarity | UX roadmap | Add screen requirements, route hierarchy, and UI acceptance criteria. |
| Partner extranet, promotion, flash sale, review interaction | Roadmap after partner role decision | Split Admin vs Hotel Partner, add promotion/review workflows, permissions, schema, APIs, and partner-facing screens. |
| Flight, airport transfer, tour add-ons | Product expansion, outside current hotel-booking MVP | Treat as new product domains with separate entities, booking lifecycle, pricing, cancellation, and supplier rules. |

## 6. Reporting/Báo Biểu Decision

Thesis section `3.4 Hệ thống báo biểu` is still a placeholder. Canonical SDD decision: reporting is not applicable to the current MVP because `Thống kê doanh thu` is marked not achieved in thesis Chapter 5 and `MVP-010` is out of scope. If reporting is approved later, add a dedicated report module with revenue source-of-truth, aggregation rules, permission boundaries, API contract, screen inventory, export policy, and acceptance tests.

## 7. Thesis Source Map

| Source | SDD use |
| --- | --- |
| `thesis/chapters/01_mo_dau/1_1_dat_van_de_muc_tieu_luan_van.md` | Problem statement, goals, admin revenue/reporting expectation |
| `thesis/chapters/01_mo_dau/1_3_noi_dung_pham_vi_thuc_hien.md` | Scope: web app, MySQL, simulated/sandbox payment |
| `thesis/chapters/01_mo_dau/1_4_ket_qua_can_dat.md` | Functional and non-functional target list |
| `thesis/chapters/03_thiet_ke/3_4_he_thong_bao_bieu.md` | Reporting/báo biểu placeholder; confirms reporting decision is needed |
| `thesis/chapters/04_thu_nghiem/4_1_cac_kich_ban_thu_nghiem.md` | Acceptance test scenario seeds |
| `thesis/chapters/04_thu_nghiem/4_3_xu_ly_cac_truong_hop_ngoai_le.md` | Exception scenario seeds |
| `thesis/chapters/05_ket_luan/5_1_ket_qua_doi_chieu_voi_muc_tieu.md` | Achieved/not-achieved status matrix |
| `thesis/chapters/05_ket_luan/5_2_cac_van_de_con_ton_dong.md` | Known limitations: payment, recommendation, breadcrumb |
| `thesis/chapters/05_ket_luan/5_3_mo_rong_huong_phat_trien.md` | Roadmap: ML recommendation, travel add-ons, partner extranet |
