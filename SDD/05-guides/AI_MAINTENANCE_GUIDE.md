# AI Maintenance Guide - Hotel Booking

Tài liệu này dành cho AI agent tiếp theo khi maintain hoặc phát triển feature cho Hotel Booking. Mục tiêu là giữ PRD, use case, business process, API, schema và diagram luôn đồng bộ; đặc biệt không làm sai các rule booking, availability và permission.

## 1. Nguyên Tắc Làm Việc

- Chỉ thay đổi đúng phạm vi được giao. Không revert hoặc ghi đè edits của người khác.
- Trước khi sửa code hoặc docs, đọc tài liệu SDD theo thứ tự ở mục 2 và xác định feature thuộc module nào.
- Với câu hỏi codebase hoặc quan hệ cross-file, nếu `graphify-out/graph.json` tồn tại thì chạy `graphify query "<câu hỏi>"` trước khi tự grep rộng.
- Nếu được phép sửa code và đã sửa code, cập nhật graph bằng `graphify update .`. Nếu task giới hạn file được sửa, không chạy lệnh nào sinh thay đổi ngoài phạm vi đó.
- Mọi thay đổi nghiệp vụ phải trace được từ requirement tới API/schema/flow. Nếu không trace được, hỏi người dùng thay vì tự đặt policy.
- Tuyệt đối tuân thủ Data Format và Validation Regex đã định nghĩa trong API Contract. Không tự ý nới lỏng hoặc thay đổi kiểu dữ liệu khi sinh code.

## 2. Thứ Tự Đọc Tài Liệu SDD

1. `SDD/01-product/PRD.md`
   - Đọc scope MVP, personas, role/permission matrix, functional requirements, use case map, business rules, NFR và open questions.
   - Đây là nguồn đầu tiên cho câu hỏi "feature này có thuộc scope không?".

2. `SDD/01-product/IMPLEMENTATION_STATUS.md`
   - Đọc ma trận đạt/chưa đạt từ luận văn, đặc biệt các gap quên mật khẩu, thống kê doanh thu, thanh toán thật, HTTPS, recommendation và breadcrumb.
   - Đây là nguồn để biết một capability đã được thesis đánh giá thế nào, không thay thế PRD scope.

3. `SDD/02-business/BUSINESS_PROCESS.md`
   - Đọc module map, customer/admin journey và state machine tổng quát.
   - Dùng để chọn file business process chi tiết cần mở.

4. `SDD/02-business/business-processes/07-business-rules-and-edge-cases.md`
   - Đọc rule tổng hợp trước khi động tới booking, availability, permission, delete, amenity hoặc status.
   - Đây là checklist chống regression nghiệp vụ.

5. File business process theo module:
   - Auth/account: `SDD/02-business/business-processes/01-auth-and-account.md`
   - Discovery/availability: `SDD/02-business/business-processes/02-discovery-and-availability.md`
   - Customer booking lifecycle: `SDD/02-business/business-processes/03-booking-lifecycle.md`
   - Admin hotel/room: `SDD/02-business/business-processes/04-admin-hotel-room-management.md`
   - Admin booking operations: `SDD/02-business/business-processes/05-admin-booking-operations.md`
   - Amenity: `SDD/02-business/business-processes/06-amenity-management.md`

6. `SDD/03-technical/TECH_SPEC.md`
   - Đọc architecture, module boundaries, protected endpoint rules, API surface, database schema, enums, core flows, transaction boundaries và concurrency notes.
   - Đây là nguồn chính để map nghiệp vụ sang controller/service/repository/API/schema.

7. Diagram và màn hình nguồn
   - Trong SDD, diagram được tham chiếu qua Source References tới `thesis/chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/` và screen inventory trong `thesis/chapters/03_thiet_ke/3_3_he_thong_man_hinh.md`.
   - Với use case đặt/hủy booking, có thể tham chiếu thêm graphify wiki nếu tồn tại: `graphify-out/wiki/3.2.1_Use_case_chi_tiết_-_3.2.1.10_Usecase_đặt_phòng_-_3.2.1.11_Usecase_tra_cứu_và_hủy_đơn_đặt_phòng.md`.
   - Screen inventory nằm trong `SDD/01-product/PRD.md` mục 8.

8. `SDD/06-quality/ACCEPTANCE_TEST_PLAN.md`
   - Đọc khi cần kiểm thử, cập nhật trạng thái đạt/chưa đạt, hoặc bổ sung evidence cho Chương 4/5 của thesis.

9. `SDD/05-guides/USER_BOOKING_FLOW_GUIDE.md`
   - Đọc khi cần viết/chỉnh phụ lục hướng dẫn sử dụng hoặc đối chiếu luồng thao tác đặt phòng từ góc nhìn người dùng.

## 3. Cách Trace Requirement End-To-End

Khi thêm/sửa feature, tạo một trace ngắn theo chuỗi:

`PRD FR/BR -> PRD UC -> Business Process BP -> TECH_SPEC API -> TECH_SPEC schema/entity -> TECH_SPEC core flow/diagram source`

Mẫu trace:

```text
Requirement: FR-CUS-BOOK-001
Use case: UC-010 Đặt phòng
Business process: BP-BOOK-001 trong 03-booking-lifecycle.md
Business rules: BR-BOOK-001..005, BR-AVAIL-001..006, BR-PRICE-001..004
API: POST /api/bookings
Schema: booking, booking_room, room, hotel, user
Flow/diagram: TECH_SPEC 8.4 Create Booking Flow; source diagram ở thesis chapter 3 nếu cần đối chiếu
```

Trace theo module thường gặp:

| Feature | PRD | Business Process | API chính | Schema chính | Flow/Diagram |
| --- | --- | --- | --- | --- | --- |
| Tìm phòng trống | `FR-CUS-ROOM-004`, `UC-006` | `BP-DISC-008` | `GET /api/rooms/available` | `hotel`, `room`, `booking`, `booking_room` | `TECH_SPEC` 8.3 |
| Tạo booking | `FR-CUS-BOOK-001`, `UC-010` | `BP-BOOK-001` | `POST /api/bookings` | `booking`, `booking_room`, `room`, `hotel`, `user` | `TECH_SPEC` 8.4 |
| Hủy booking | `FR-CUS-BOOK-006`, `FR-ADM-BOOK-004`, `UC-011` | `BP-BOOK-006`, `BP-OPS-005` | `PATCH /api/bookings/{id}/cancel` | `booking.status`, `booking.cancel_reason` | `TECH_SPEC` 8.5 |
| Admin check-in/out | `FR-ADM-BOOK-002`, `UC-009` | `05-admin-booking-operations.md` | `/api/admin/bookings/{id}/check-in`, `/check-out` | `booking.status`, `booking_room.room_number` | `TECH_SPEC` 8.8 |
| Quản lý hotel/room | `UC-005`, `UC-007` | `04-admin-hotel-room-management.md` | `/api/admin/hotels`, `/api/admin/rooms` | `hotel`, `room`, `image`, amenity mappings | `TECH_SPEC` 8.6, 8.7 |
| Quản lý amenity | `UC-012` | `06-amenity-management.md` | `/api/amenities`, mapping endpoints | `amenity`, `hotel_amenity`, `room_amenity` | `TECH_SPEC` 8.9 |

## 4. Quy Tắc Khi Thêm Feature Mới

- Bắt đầu từ PRD: thêm hoặc cập nhật FR, acceptance criteria, priority, UC map, business rules, NFR/security nếu có.
- Cập nhật business process: thêm BP mới hoặc mở rộng BP hiện có với trigger, preconditions, inputs, outputs, data touched, main flow, error flows và business rules.
- Cập nhật TECH_SPEC: API endpoint, auth rule, request/response contract, schema/table/index/entity, enum, validation, errors, transaction/concurrency nếu có.
- Không thêm endpoint public cho dữ liệu nhạy cảm nếu PRD chưa cho phép. Booking detail/reference lookup mặc định yêu cầu authenticated và owner/Admin.
- Không thay đổi state machine booking nếu chưa cập nhật PRD, BP, TECH_SPEC và hỏi policy khi rule còn mở.
- Nếu thêm field DB, xác định field đó thuộc entity nào, nullable hay required, có cần index/unique constraint không, và ảnh hưởng migration/test ra sao.
- Khi thêm/sửa field dữ liệu, phải ghi đủ: API field name, DB column, type, nullable/required, format, min/max, enum values, default value, normalization rule, error code và migration impact.
- Không tự suy diễn default. Nếu SDD chưa nêu default cho boolean/status/date/money/role, dừng và hỏi hoặc cập nhật SDD trước khi sinh code.
- Không dùng `float`/`double` cho tiền; dùng decimal và server-side calculation.
- Nếu thêm role/permission, cập nhật permission matrix trong PRD, protected endpoint rules trong TECH_SPEC và rule tổng hợp trong `07-business-rules-and-edge-cases.md`.
- Nếu thêm UI/screen, cập nhật screen inventory hoặc ghi rõ source screen/diagram cần bổ sung.

## 5. Checklist Cập Nhật Docs

Trước khi kết thúc task feature, kiểm tra:

- `SDD/01-product/PRD.md`: scope MVP, FR, acceptance criteria, UC map, BR, NFR, screen inventory, open questions.
- `SDD/01-product/IMPLEMENTATION_STATUS.md`: cập nhật nếu thay đổi trạng thái thesis đạt/chưa đạt hoặc roadmap boundary.
- `SDD/02-business/BUSINESS_PROCESS.md`: module map, customer/admin journey, state machine nếu feature chạm lifecycle.
- File trong `SDD/02-business/business-processes/`: BP chi tiết, main flow, error flow, business rules, open policy.
- `SDD/02-business/business-processes/07-business-rules-and-edge-cases.md`: rule tổng hợp, error catalog, edge cases.
- `SDD/03-technical/TECH_SPEC.md`: API surface, protected endpoint rules, schema, relationships, indexes, enums, validation, errors, transaction boundaries, concurrency notes.
- Diagram/source references: nếu flow thay đổi, ghi rõ diagram/source nào cần cập nhật hoặc đã cập nhật.
- `SDD/06-quality/ACCEPTANCE_TEST_PLAN.md`: thêm hoặc cập nhật acceptance/negative scenarios và evidence checklist cho feature.
- `SDD/05-guides/USER_BOOKING_FLOW_GUIDE.md`: cập nhật nếu luồng màn hình đặt phòng, booking success, lịch sử hoặc hủy booking thay đổi.
- Trace: trong PR/summary phải nêu được FR/UC/BP/API/schema chính đã chạm.

## 6. Open Policy Cần Hỏi Người Dùng

Không tự quyết các policy sau nếu requirement chưa rõ:

- Admin là system admin duy nhất hay tách thêm hotel owner/partner role.
- Tra cứu booking theo mã có cho guest chưa đăng nhập không, hay bắt buộc login.
- Feature yêu cầu mở lại hủy booking `CHECKED_IN`; MVP hiện mặc định chặn và trả `BOOKING_CANNOT_CANCEL`.
- Xóa hotel/room/user là hard delete, soft delete hay deactivate; xử lý thế nào khi còn booking active/history.
- Có chặn xóa user/hotel/room khi còn booking `BOOKED` hoặc `CHECKED_IN` không.
- Payment thật, refund, promotion, policy engine, review/rating có thuộc roadmap gần không.
- Trẻ em có tính đủ vào `room.capacity` hay có capacity policy riêng.
- Admin action logging/audit là bắt buộc hay chỉ khuyến nghị.
- Booking reference lookup trả bao nhiêu dữ liệu và có cần mask thông tin khách hàng không.

## 7. Guardrails Booking, Availability, Permission

Booking:

- Booking mới chỉ tạo khi actor đã authenticated, ngày hợp lệ, room/hotel tồn tại và còn hoạt động.
- `checkout_date` phải sau `checkin_date`; `checkin_date` không được ở quá khứ.
- Booking mới mặc định `BOOKED`; mã `booking_reference` phải unique.
- Tổng tiền dùng `room.price * number_of_nights * quantity`; không tự thêm payment/refund thật khi MVP chưa cho phép.
- Check-in yêu cầu Admin và `roomNumber`; check-out chỉ từ trạng thái hợp lệ theo state machine.

Availability:

- Conflict formula bắt buộc: `existing_checkin < new_checkout AND existing_checkout > new_checkin`.
- Chỉ status `BOOKED` và `CHECKED_IN` chặn phòng.
- `CANCELLED` không chặn phòng; `CHECKED_OUT` không chặn phòng cho booking tương lai.
- `requested_quantity + booked_quantity <= room.amount`.
- `adultAmount + childrenAmount <= room.capacity` trừ khi người dùng xác nhận policy khác.
- Tạo booking phải kiểm tra lại availability trong service/API, kể cả frontend vừa search thấy còn phòng.
- Availability check và insert booking phải nằm trong cùng transaction hoặc có locking/optimistic locking để giảm overbooking.

Permission:

- Protected API phải có JWT hợp lệ; admin-only API phải có role `ADMIN`.
- Customer chỉ xem/sửa profile của chính mình.
- Customer chỉ xem/hủy booking của chính mình, trừ policy tra cứu public đã được xác nhận.
- Admin được xem và vận hành booking, nhưng hotel/room/amenity mapping vẫn phải check owner khi thao tác tài nguyên thuộc hotel.
- Admin chỉ sửa/xóa hotel do mình sở hữu; chỉ thêm/sửa/xóa room trong hotel do mình sở hữu.
- Admin chỉ gán/gỡ amenity trên hotel/room mình sở hữu; xóa amenity gốc phải bị chặn nếu đang được mapping.
- Không dựa vào client-side hiding để bảo mật. Rule owner/role phải nằm ở backend service layer.

## 8. Tín Hiệu Cần Dừng Và Hỏi Lại

Dừng và hỏi người dùng khi gặp một trong các trường hợp:

- Feature yêu cầu behavior mâu thuẫn giữa PRD, business process và TECH_SPEC.
- Feature cần thay đổi state machine booking hoặc meaning của status.
- Feature cần public endpoint cho booking/user data.
- Feature cần hard delete dữ liệu có lịch sử booking.
- Feature cần thay đổi công thức availability, capacity, pricing hoặc unique booking reference.
- Feature cần thêm role mới hoặc mở rộng quyền Admin ngoài owner check hiện tại.

## 9. Mẫu Summary Cho Agent Sau Khi Làm Xong

```text
Changed:
- <file path>

Trace:
- PRD: <FR/UC/BR>
- Business process: <BP file + BP ID>
- API/schema: <endpoint + tables/entities>

Guardrails checked:
- Booking state: <ok/changed + reason>
- Availability: <ok/changed + reason>
- Permission: <ok/changed + reason>

Open policy:
- <none hoặc câu hỏi còn chờ quyết định>
```
