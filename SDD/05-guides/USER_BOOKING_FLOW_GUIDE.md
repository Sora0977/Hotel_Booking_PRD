# User Booking Flow Guide - Hotel Booking

## 1. Metadata

| Field | Value |
| --- | --- |
| Document type | User flow guide |
| Product | Hotel Booking |
| Depends on | `SDD/01-product/PRD.md`, `SDD/02-business/business-processes/02-discovery-and-availability.md`, `SDD/02-business/business-processes/03-booking-lifecycle.md`, `SDD/03-technical/API_CONTRACT.md` |
| Source thesis appendix | `thesis/appendices/huong_dan_su_dung.md` |
| Purpose | Preserve the appendix's booking walkthrough as an SDD traceable flow |

## 2. Scope

This guide describes the main Customer path: login/register, search hotel, inspect rooms, create a booking, then track or cancel the booking. It is not a replacement for business-process rules; any behavior conflict must follow PRD, business process, API contract, and entity schema.

## 3. Five-Step Booking Walkthrough

| Step | User action | Screen trace | API / process trace | Expected system behavior |
| --- | --- | --- | --- | --- |
| 1 | Đăng nhập hoặc đăng ký tài khoản | `SCR-CUS-001`, `SCR-CUS-002` | `BP-AUTH-001`, `BP-AUTH-002`, `API-AUTH-001`, `API-AUTH-002` | User can create a Customer account or receive a JWT after valid login. Locked or invalid accounts show stable errors. |
| 2 | Tìm kiếm khách sạn | `SCR-CUS-003`, `SCR-CUS-004` | `BP-DISC-001`, `BP-DISC-003`, `API-HOTEL-001` | User enters location/date criteria and sees matching hotels or an empty state. |
| 3 | Xem chi tiết khách sạn và phòng | `SCR-CUS-005`, `SCR-CUS-006`, `SCR-CUS-007` | `BP-DISC-002`, `BP-DISC-004`, `BP-DISC-006`, `API-HOTEL-002`, `API-HOTEL-003`, `API-ROOM-002` | User can inspect hotel information, room information, images, amenities, price, capacity, and booking form fields. |
| 4 | Thực hiện đặt phòng | `SCR-CUS-007`, `SCR-CUS-008` | `BP-DISC-008`, `BP-BOOK-001`, `BP-BOOK-002`, `API-ROOM-003`, `API-BOOK-001` | System validates date/quantity/capacity, checks availability again server-side, calculates total price, generates booking reference, and shows booking success. |
| 5 | Theo dõi hoặc hủy đặt phòng | `SCR-CUS-009`, `SCR-CUS-010`, `SCR-CUS-011` | `BP-BOOK-003`, `BP-BOOK-004`, `BP-BOOK-005`, `BP-BOOK-006`, `API-BOOK-002..005` | User sees own bookings, opens booking detail, searches by reference, and can cancel eligible bookings with a reason. |

## 4. User-Facing Rules To Preserve

| Rule area | User-facing behavior |
| --- | --- |
| Authentication | Booking creation, booking history, booking detail, and cancel require authenticated user by default. |
| Date selection | `checkoutDate` must be after `checkinDate`; past check-in dates are rejected. |
| Availability | A room shown as available in search must still be rechecked when creating the booking. |
| Price | Total price is calculated by backend; frontend must not be the source of truth. |
| Cancellation | User can cancel only own eligible bookings; reason is captured and stored. |
| Payment | MVP has no real payment gateway. Do not show language that implies real online settlement unless payment is implemented and approved. |

## 5. Evidence For Thesis Appendix

When completing `thesis/appendices/huong_dan_su_dung.md`, use this SDD guide as the trace source and attach screenshots only from real UI screens listed in PRD screen inventory. Do not invent screenshots or pass/fail results.
