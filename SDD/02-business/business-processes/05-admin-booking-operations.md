# 05 - Admin Vận Hành Booking

## 1. Scope

| Process ID | Process | Actor |
| --- | --- | --- |
| BP-OPS-001 | Xem toàn bộ booking | Admin |
| BP-OPS-002 | Tìm kiếm/lọc booking | Admin |
| BP-OPS-003 | Check-in booking | Admin |
| BP-OPS-004 | Check-out booking | Admin |
| BP-OPS-005 | Hủy booking bởi Admin | Admin |

## 2. Shared Rules

| Rule ID | Rule |
| --- | --- |
| BR-OPS-001 | Mọi thao tác vận hành booking yêu cầu role `ADMIN`. |
| BR-OPS-002 | Booking phải tồn tại trước khi cập nhật trạng thái. |
| BR-OPS-003 | Khi check-in phải gán số phòng thực tế. |
| BR-OPS-004 | Số phòng thực tế không được đang được gán cho booking `CHECKED_IN` khác. |
| BR-OPS-005 | Booking `CHECKED_OUT` hoặc `CANCELLED` không được hủy. |

## 3. BP-OPS-001 - Xem Toàn Bộ Booking

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin mở module quản lý đặt phòng |
| Preconditions | Admin đã đăng nhập |
| Inputs | Pagination, filters optional |
| Outputs | Booking list |
| Data touched | `booking`, `booking_room`, `room`, `hotel`, `user` |
| Related screens | Quản lý và tìm kiếm đặt phòng |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin chọn quản lý đặt phòng. |
| 2 | System kiểm tra role Admin. |
| 3 | System truy vấn danh sách booking. |
| 4 | System join thông tin user, room, hotel nếu cần. |
| 5 | System trả booking list. |
| 6 | Frontend hiển thị danh sách. |

### Display Fields

| Field            | Source                                    |
| ---------------- | ----------------------------------------- |
| Mã booking       | `booking.booking_reference`               |
| Khách hàng       | `booking.customer_name`, `user.full_name` |
| Phòng            | `room.name`, `room.type`                  |
| Khách sạn        | `hotel.name`                              |
| Ngày lưu trú     | `checkin_date`, `checkout_date`           |
| Trạng thái       | `booking.status`                          |
| Số phòng thực tế | `booking_room.room_number`                |

## 4. BP-OPS-002 - Tìm Kiếm/Lọc Booking

| Field        | Detail                                                |
| ------------ | ----------------------------------------------------- |
| Actor        | Admin                                                 |
| Trigger      | Admin nhập từ khóa hoặc chọn filter                   |
| Inputs       | `bookingReference`, customer info, status, date range |
| Outputs      | Filtered booking list                                 |
| Data touched | `booking`, `user`, `room`, `hotel`                    |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin nhập tiêu chí tìm kiếm. |
| 2 | System validate filters. |
| 3 | System query booking theo tiêu chí. |
| 4 | System trả kết quả. |
| 5 | Frontend hiển thị danh sách lọc. |

## 5. BP-OPS-003 - Check-In Booking

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Khách đến nhận phòng, Admin nhấn check-in |
| Preconditions | Booking tồn tại, thường ở trạng thái `BOOKED` |
| Inputs | `bookingId`, `roomNumber` |
| Outputs | Booking status `CHECKED_IN`, room number assigned |
| Data touched | `booking.status`, `booking_room.room_number` |
| Related screens | Chuyển booking từ đã đặt sang đã nhận phòng |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin mở booking cần xử lý. |
| 2 | Admin chọn check-in. |
| 3 | Admin nhập/chọn số phòng thực tế (có thể nhập nhiều số phòng cách nhau bằng dấu phẩy nếu `quantity > 1`). |
| 4 | System kiểm tra role Admin. |
| 5 | System tìm booking theo ID. |
| 6 | System kiểm tra booking có thể check-in. |
| 7 | System kiểm tra số phòng không đang có khách. |
| 8 | System kiểm tra số lượng mã phòng vật lý được nhập (đếm qua dấu phẩy) BẮT BUỘC phải bằng với `quantity` của phòng đó trong booking. |
| 9 | System gán `room_number` vào `booking_room`. |
| 10 | System cập nhật status `CHECKED_IN`. |
| 11 | System trả thông báo thành công. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Booking not found | ID không tồn tại | Trả `RESOURCE_NOT_FOUND` |
| Room occupied | Room number đang thuộc booking `CHECKED_IN` khác | Trả `ROOM_NUMBER_OCCUPIED` |
| Room number count mismatch | Số lượng mã phòng nhập vào không khớp với số lượng phòng đã đặt (`quantity`) | Trả `VALIDATION_ERROR` |
| Invalid status | Booking không ở trạng thái có thể check-in | Trả state error |

### Occupancy Rule

| Rule ID | Rule |
| --- | --- |
| BR-OPS-CI-001 | Một `booking_room.room_number` không được gán cho nhiều booking đang `CHECKED_IN` cùng lúc. |
| BR-OPS-CI-003 | Số lượng mã phòng vật lý được nhập phải bằng `booking_room.quantity`; nếu không khớp trả `VALIDATION_ERROR`. |
| BR-OPS-CI-002 | Check-in phải chạy trong transaction với occupancy check. |

## 6. BP-OPS-004 - Check-Out Booking

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Khách trả phòng, Admin nhấn check-out |
| Preconditions | Booking tồn tại, thường ở trạng thái `CHECKED_IN` |
| Inputs | `bookingId` |
| Outputs | Booking status `CHECKED_OUT` |
| Data touched | `booking.status` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin mở booking đang lưu trú. |
| 2 | Admin chọn check-out. |
| 3 | System kiểm tra role Admin. |
| 4 | System tìm booking. |
| 5 | System kiểm tra trạng thái hiện tại. |
| 6 | System cập nhật status `CHECKED_OUT`. |
| 7 | System trả thông báo thành công. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Booking not found | ID không tồn tại | Trả not found |
| Invalid status | Booking chưa check-in hoặc đã hủy | Trả state error |

## 7. BP-OPS-005 - Hủy Booking Bởi Admin

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin hủy booking trong màn hình quản lý |
| Preconditions | Booking tồn tại và chưa hoàn tất/chưa hủy |
| Inputs | `bookingId`, `cancelReason` |
| Outputs | Booking status `CANCELLED` |
| Data touched | `booking.status`, `booking.cancel_reason` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin chọn booking cần hủy. |
| 2 | Admin nhấn hủy booking. |
| 3 | Frontend yêu cầu xác nhận và lý do. |
| 4 | System kiểm tra role Admin. |
| 5 | System tìm booking. |
| 6 | System kiểm tra trạng thái có thể hủy. |
| 7 | System lưu lý do hủy. |
| 8 | System cập nhật status `CANCELLED`. |
| 9 | System trả thông báo thành công. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Already checked out | Status `CHECKED_OUT` | Không cho hủy |
| Already cancelled | Status `CANCELLED` | Không cho hủy |
| Not found | Booking không tồn tại | Trả not found |
