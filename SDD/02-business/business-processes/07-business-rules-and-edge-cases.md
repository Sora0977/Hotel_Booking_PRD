# 07 - Business Rules Và Edge Cases Tổng Hợp

## 1. Authentication Rules

| Rule ID | Rule | Applies To |
| --- | --- | --- |
| BR-AUTH-001 | Email không được trùng. | Register |
| BR-AUTH-002 | Mật khẩu phải hash trước khi lưu. | Register, change password |
| BR-AUTH-003 | Tài khoản locked/inactive không được login. | Login |
| BR-AUTH-004 | Role mặc định khi đăng ký là `CUSTOMER`. | Register |
| BR-AUTH-005 | API protected yêu cầu JWT hợp lệ. | All protected APIs |
| BR-AUTH-006 | Admin-only APIs yêu cầu role `ADMIN`. | Admin modules |

## 2. Permission Rules

| Rule ID | Rule |
| --- | --- |
| BR-PERM-001 | Customer chỉ xem/sửa profile của chính mình. |
| BR-PERM-002 | Customer chỉ xem/hủy booking của chính mình. |
| BR-PERM-003 | Admin được xem toàn bộ booking. |
| BR-PERM-004 | Admin chỉ sửa/xóa khách sạn do mình sở hữu. |
| BR-PERM-005 | Admin chỉ quản lý phòng thuộc khách sạn mình sở hữu. |
| BR-PERM-006 | Admin chỉ gán/gỡ tiện ích trên hotel/room mình sở hữu. |

## 3. Date And Availability Rules

| Rule ID | Rule |
| --- | --- |
| BR-DATE-001 | `checkin_date` không được ở quá khứ. |
| BR-DATE-002 | `checkout_date` phải sau `checkin_date`. |
| BR-AVAIL-001 | Booking conflict nếu `existing_checkin < new_checkout AND existing_checkout > new_checkin`. |
| BR-AVAIL-002 | Chỉ booking `BOOKED` và `CHECKED_IN` chặn phòng. |
| BR-AVAIL-003 | Booking `CANCELLED` không chặn phòng. |
| BR-AVAIL-004 | Booking `CHECKED_OUT` không chặn phòng cho booking tương lai. |
| BR-AVAIL-005 | Số lượng đặt không vượt quá `room.amount` sau khi trừ booking đang chặn. |
| BR-AVAIL-006 | Tổng khách không vượt quá `room.capacity`, trừ khi có rule riêng cho trẻ em. |
| BR-DATE-003 | Date input/output dùng `YYYY-MM-DD`; không nhận datetime cho `checkin_date`/`checkout_date`. |
| BR-DATE-004 | "Quá khứ" được tính theo business timezone UTC+7 tại thời điểm server xử lý. |
| BR-AVAIL-007 | Nếu booking có `quantity`, capacity check là `adult_amount + children_amount <= room.capacity * quantity`, trừ khi có policy trẻ em riêng. |
| BR-AVAIL-008 | Availability chỉ tính hotel/room có active flag bằng `true`/`1`. |

## 4. Booking State Machine

| Current | Trigger | Actor | Next | Allowed |
| --- | --- | --- | --- | --- |
| None | Create booking | Customer/Admin | `BOOKED` | Yes |
| `BOOKED` | Cancel | Customer owner/Admin | `CANCELLED` | Yes |
| `BOOKED` | Check-in | Admin | `CHECKED_IN` | Yes |
| `CHECKED_IN` | Check-out | Admin | `CHECKED_OUT` | Yes |
| `CHECKED_IN` | Cancel | Admin | None | Blocked by default until policy is explicitly approved; return `BOOKING_CANNOT_CANCEL`. |
| `CHECKED_OUT` | Cancel | Customer/Admin | None | No |
| `CANCELLED` | Cancel | Customer/Admin | None | No |
| `CANCELLED` | Check-in | Admin | None | No |
| `CHECKED_OUT` | Check-in | Admin | None | No |

## 5. Pricing Rules

| Rule ID | Rule |
| --- | --- |
| BR-PRICE-001 | `number_of_nights = checkout_date - checkin_date`. |
| BR-PRICE-002 | `total_price = room.price * number_of_nights * quantity`. |
| BR-PRICE-003 | `room.price` phải >= 0. |
| BR-PRICE-004 | `quantity` phải > 0. |
| BR-PRICE-005 | Refund hiện chỉ là field dữ liệu, chưa có payment/refund flow thật trong MVP. |
| BR-PRICE-006 | Tiền tệ mặc định là VND; không tự thêm multi-currency nếu PRD chưa yêu cầu. |
| BR-PRICE-007 | `total_price` do backend tính bằng decimal scale 2; client gửi lên nếu có phải bị bỏ qua hoặc đối chiếu. |
| BR-PRICE-008 | `refund` mặc định `NULL` trong MVP; chỉ validate `>= 0` nếu được set, chưa tự tính refund khi chưa có payment flow. |

## 6. Hotel And Room Rules

| Rule ID | Rule |
| --- | --- |
| BR-HOTEL-001 | Tạo hotel yêu cầu role Admin. |
| BR-HOTEL-002 | Tạo hotel yêu cầu tên, location, mô tả, liên hệ, star rating. |
| BR-HOTEL-003 | Tên + location của hotel không được trùng. |
| BR-HOTEL-004 | Hotel image upload qua Cloudinary hoặc storage tương đương. |
| BR-ROOM-001 | Room phải thuộc một hotel. |
| BR-ROOM-002 | Room type thuộc `SINGLE`, `DOUBLE`, `TRIPLE`, `SUIT`. |
| BR-ROOM-003 | Room amount phải > 0. |
| BR-ROOM-004 | Room capacity phải > 0. |
| BR-ROOM-005 | Room price không âm. |

## 7. Amenity Rules

| Rule ID | Rule |
| --- | --- |
| BR-AMN-001 | Amenity name phải unique. |
| BR-AMN-002 | Amenity type phân biệt tiện ích cấp hotel và cấp room. |
| BR-AMN-003 | Không xóa amenity đang có mapping trong `hotel_amenity` hoặc `room_amenity`. |
| BR-AMN-004 | Gỡ tiện ích khỏi hotel/room chỉ xóa mapping. |
| BR-AMN-005 | Không tạo mapping trùng cho cùng hotel/room và amenity. |

## 8. Error Catalog

| Error Code | Business Meaning | Typical HTTP Status |
| --- | --- | --- |
| `VALIDATION_ERROR` | Dữ liệu nhập không hợp lệ | `400` |
| `AUTH_UNAUTHORIZED` | Thiếu, hết hạn, sai định dạng hoặc JWT không hợp lệ | `401` |
| `AUTH_INVALID_CREDENTIALS` | Email hoặc mật khẩu sai | `401` |
| `AUTH_ACCOUNT_LOCKED` | Tài khoản bị khóa | `403` |
| `AUTH_FORBIDDEN` | Không có quyền hoặc không phải owner | `403` |
| `RESOURCE_NOT_FOUND` | Không tìm thấy entity | `404` |
| `DUPLICATE_EMAIL` | Email đã tồn tại | `409` |
| `DUPLICATE_HOTEL` | Khách sạn trùng tên/location | `409` |
| `DUPLICATE_AMENITY` | Tiện ích trùng tên | `409` |
| `ROOM_UNAVAILABLE` | Phòng đã hết trong khoảng ngày | `409` |
| `ROOM_QUANTITY_EXCEEDED` | Số lượng phòng không đủ | `409` |
| `ROOM_NUMBER_OCCUPIED` | Số phòng thực tế đang có khách | `409` |
| `BOOKING_CANNOT_CANCEL` | Booking không được hủy | `409` |
| `AMENITY_IN_USE` | Tiện ích đang được sử dụng | `409` |
| `IMAGE_UPLOAD_FAILED` | Upload ảnh qua cloud/storage provider thất bại | `502` |
| `INTERNAL_SERVER_ERROR` | Lỗi server không xử lý được | `500` |

## 9. Edge Cases

| Edge Case ID | Scenario | Expected Handling |
| --- | --- | --- |
| EC-001 | Hai customer đặt cùng phòng còn lại cùng lúc | Availability check và insert booking phải chạy trong transaction |
| EC-002 | Customer mở phòng còn trống nhưng khi submit thì hết phòng | Booking API kiểm tra lại availability trước khi lưu |
| EC-003 | Admin xóa room đang có booking active | Nên chặn hoặc chuyển sang inactive, không hard delete |
| EC-004 | Admin xóa hotel đang có booking active | Nên chặn hoặc chuyển sang inactive, không hard delete |
| EC-005 | Customer hủy booking đã check-out | Chặn và hiển thị lỗi không thể hủy |
| EC-006 | Admin gán room number đang có khách | Chặn và yêu cầu chọn phòng khác |
| EC-007 | Amenity đang gán cho phòng bị xóa | Chặn xóa, yêu cầu gỡ mapping trước |
| EC-008 | JWT hết hạn khi đang thao tác form | Yêu cầu đăng nhập lại, không lưu thao tác |
| EC-009 | Cloudinary upload thành công nhưng DB save thất bại | Cần rollback DB và cân nhắc cleanup ảnh orphan |
| EC-010 | DB save thành công nhưng frontend mất kết nối | Customer có thể tra cứu bằng mã booking hoặc xem lịch sử |

## 10. Open Questions

| Question ID | Question | Suggested Decision |
| --- | --- | --- |
| OQ-001 | Tra cứu booking theo mã có cho guest chưa login không? | Nên yêu cầu login ở MVP để tránh lộ dữ liệu |
| OQ-002 | Có cần mở chính sách hủy booking `CHECKED_IN` trong phiên bản sau không? | MVP mặc định chặn và trả `BOOKING_CANNOT_CANCEL`; chỉ thay đổi khi có policy mới |
| OQ-003 | Xóa hotel/room là hard delete hay soft delete? | Nên soft delete để bảo toàn booking history |
| OQ-004 | Có cần audit log cho admin actions không? | Nên có trong bản sau |
| OQ-005 | Payment thật có nằm trong scope gần không? | Hiện để out-of-scope theo PRD |
