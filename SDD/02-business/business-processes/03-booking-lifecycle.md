# 03 - Vòng Đời Đặt Phòng Của Customer

## 1. Scope

| Process ID  | Process                       | Actor           |
| ----------- | ----------------------------- | --------------- |
| BP-BOOK-001 | Tạo booking mới               | Customer, Admin |
| BP-BOOK-002 | Hiển thị đặt phòng thành công | Customer        |
| BP-BOOK-003 | Xem lịch sử booking           | Customer        |
| BP-BOOK-004 | Tra cứu booking theo mã       | Customer, Admin |
| BP-BOOK-005 | Xem chi tiết booking          | Customer, Admin |
| BP-BOOK-006 | Hủy booking                   | Customer, Admin |

## 2. Booking Data Contract

| Field | Required | Notes |
| --- | --- | --- |
| `roomId` | Yes | Room được đặt |
| `checkinDate` | Yes | Không được trong quá khứ |
| `checkoutDate` | Yes | Phải sau check-in |
| `quantity` | Yes | Số lượng phòng cần đặt |
| `adultAmount` | Yes | Số người lớn |
| `childrenAmount` | Yes | Số trẻ em |
| `customerName` | Yes | Có thể lấy từ profile hoặc form |
| `specialRequire` | No | Yêu cầu đặc biệt |
| `bookingReference` | System-generated | Mã booking duy nhất, tài liệu gốc nêu 10 ký tự |
| `totalPrice` | System-generated | Giá phòng x số đêm x số lượng |
| `status` | System-generated | Default `BOOKED` |

## 3. BP-BOOK-001 - Tạo Booking Mới

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor nhấn nút đặt phòng |
| Preconditions | Actor đã đăng nhập, room tồn tại |
| Inputs | Booking data contract |
| Outputs | Booking mới trạng thái `BOOKED` |
| Data touched | `booking`, `booking_room`, `room`, `hotel`, `user` |
| Related screens | Chi tiết phòng và form đặt phòng, đặt phòng thành công |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Customer mở trang chi tiết phòng hoặc form đặt phòng. |
| 2 | Customer chọn check-in, check-out, số lượng phòng, số khách. |
| 3 | Customer nhập yêu cầu đặc biệt nếu có. |
| 4 | Customer nhấn đặt phòng. |
| 5 | System xác thực JWT/current user. |
| 6 | System validate ngày: check-in không trong quá khứ, check-out sau check-in. |
| 7 | System kiểm tra room và hotel tồn tại. |
| 8 | System kiểm tra room thuộc hotel hợp lệ. |
| 9 | System kiểm tra phòng trống theo overlap formula. |
| 10 | System kiểm tra số lượng phòng còn lại. |
| 11 | System kiểm tra sức chứa. |
| 12 | System tính tổng tiền. |
| 13 | System sinh `booking_reference` duy nhất. |
| 14 | System lưu booking với status `BOOKED`. |
| 15 | System lưu mapping `booking_room`. |
| 16 | System trả booking detail. |
| 17 | Frontend chuyển tới màn hình đặt phòng thành công. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Not authenticated | Customer chưa đăng nhập | Chuyển login hoặc trả `401` |
| Invalid date | Ngày không hợp lệ | Trả validation error |
| Room not found | `roomId` không tồn tại | Trả `RESOURCE_NOT_FOUND` |
| Room unavailable | Có booking giao ngày | Trả `ROOM_UNAVAILABLE` |
| Quantity exceeded | Số lượng yêu cầu vượt số còn lại | Trả `ROOM_QUANTITY_EXCEEDED` |
| Capacity exceeded | Số khách vượt sức chứa | Trả validation/capacity error |

### Business Rules

| Rule ID | Rule |
| --- | --- |
| BR-BOOK-001 | Booking chỉ tạo được khi actor đã xác thực. |
| BR-BOOK-002 | Booking mới có trạng thái `BOOKED`. |
| BR-BOOK-003 | Mã booking phải unique. |
| BR-BOOK-004 | Tổng tiền = `room.price * number_of_nights * quantity`. |
| BR-BOOK-005 | Phòng bị chặn nếu có booking `BOOKED` hoặc `CHECKED_IN` giao ngày. |

## 4. BP-BOOK-002 - Hiển Thị Đặt Phòng Thành Công

| Field | Detail |
| --- | --- |
| Actor | Customer |
| Trigger | Booking created successfully |
| Inputs | Created booking detail |
| Outputs | Success screen |
| Related screens | Đặt phòng thành công |

### Display Requirements

| Field | Source |
| --- | --- |
| Mã booking | `booking.booking_reference` |
| Trạng thái | `booking.status` |
| Khách sạn | `hotel.name` |
| Phòng | `room.name`, `room.type` |
| Ngày check-in/check-out | `booking.checkin_date`, `booking.checkout_date` |
| Tổng tiền | `booking.total_price` |
| Số người | `adult_amount`, `children_amount` |
| Yêu cầu đặc biệt | `special_require` |

## 5. BP-BOOK-003 - Xem Lịch Sử Booking

| Field | Detail |
| --- | --- |
| Actor | Customer |
| Trigger | Customer mở lịch sử đặt phòng |
| Preconditions | Customer đã đăng nhập |
| Inputs | Current user ID, filters optional |
| Outputs | Booking list của current user |
| Data touched | `booking`, `booking_room`, `room`, `hotel` |
| Related screens | Lịch sử đặt phòng và tìm kiếm |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Customer mở lịch sử đặt phòng. |
| 2 | System lấy current user từ JWT. |
| 3 | System truy vấn booking theo `user_id`. |
| 4 | System sắp xếp booking theo ngày tạo hoặc ngày lưu trú. |
| 5 | System trả danh sách booking. |
| 6 | Frontend hiển thị danh sách hoặc empty state. |

### Empty Flow

| Condition | Behavior |
| --- | --- |
| Customer chưa có booking | Hiển thị thông báo chưa có lịch sử đặt phòng |

## 6. BP-BOOK-004 - Tra Cứu Booking Theo Mã

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor nhập mã booking và nhấn tìm kiếm |
| Preconditions | Theo PRD hiện tại: actor đã đăng nhập |
| Inputs | `bookingReference` |
| Outputs | Booking detail |
| Data touched | `booking`, `booking_room`, `room`, `hotel`, `user` |
| Related screens | Lịch sử/tìm kiếm booking |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor mở trang tra cứu booking. |
| 2 | Actor nhập mã booking. |
| 3 | System truy vấn booking theo `booking_reference`. |
| 4 | System kiểm tra booking tồn tại. |
| 5 | System kiểm tra quyền xem: owner hoặc Admin. |
| 6 | System trả booking detail. |
| 7 | Frontend hiển thị chi tiết booking. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Code not found | Không có booking theo mã | Hiển thị mã không tồn tại |
| Forbidden | Customer không phải chủ booking | Trả `AUTH_FORBIDDEN` |

### Open Policy

| Question | Impact |
| --- | --- |
| Guest chưa đăng nhập có được tra cứu bằng mã không? | Nếu có, cần mask dữ liệu cá nhân hoặc yêu cầu thêm xác minh |

## 7. BP-BOOK-005 - Xem Chi Tiết Booking

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor mở booking detail |
| Preconditions | Booking tồn tại, actor có quyền xem |
| Inputs | `bookingId` hoặc `bookingReference` |
| Outputs | Full booking detail |
| Related screens | Chi tiết booking |

### Display Requirements

| Field | Source |
| --- | --- |
| Mã booking | `booking.booking_reference` |
| Trạng thái | `booking.status` |
| Tên khách | `booking.customer_name` |
| Check-in/check-out | `booking.checkin_date`, `booking.checkout_date` |
| Ngày tạo | `booking.created_at` |
| Người lớn/trẻ em | `adult_amount`, `children_amount` |
| Tổng tiền | `total_price` |
| Số phòng thực tế | `booking_room.room_number` |
| Yêu cầu đặc biệt | `special_require` |
| Lý do hủy | `cancel_reason` |
| Hoàn tiền | `refund` |

## 8. BP-BOOK-006 - Hủy Booking

| Field | Detail |
| --- | --- |
| Actor | Customer, Admin |
| Trigger | Actor nhấn hủy booking và xác nhận |
| Preconditions | Booking tồn tại, actor có quyền hủy, booking chưa hoàn tất/chưa hủy |
| Inputs | `bookingId` hoặc `bookingReference`, `cancelReason` |
| Outputs | Booking status `CANCELLED` |
| Data touched | `booking.status`, `booking.cancel_reason`, availability computed from booking status |
| Related screens | Xác nhận hủy booking |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor mở chi tiết booking. |
| 2 | Actor nhấn hủy booking. |
| 3 | Frontend hiển thị hộp thoại xác nhận. |
| 4 | Actor nhập hoặc chọn lý do hủy. |
| 5 | Actor xác nhận hủy. |
| 6 | System tìm booking. |
| 7 | System kiểm tra actor là chủ đơn hoặc Admin. |
| 8 | System kiểm tra trạng thái booking có thể hủy. |
| 9 | System lưu lý do hủy. |
| 10 | System cập nhật status thành `CANCELLED`. |
| 11 | System trả thông tin booking sau hủy. |
| 12 | Frontend hiển thị hủy thành công. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Not owner | Customer không phải chủ booking | Trả `AUTH_FORBIDDEN` |
| Already cancelled | Status `CANCELLED` | Trả lỗi không thể hủy |
| Completed | Status `CHECKED_OUT` | Trả lỗi không thể hủy |
| Not found | Booking không tồn tại | Trả `RESOURCE_NOT_FOUND` |

### Business Rules

| Rule ID | Rule |
| --- | --- |
| BR-CANCEL-001 | Customer chỉ hủy booking của chính mình. |
| BR-CANCEL-002 | Admin có thể hủy booking hợp lệ. |
| BR-CANCEL-003 | Booking `CHECKED_OUT` không được hủy. |
| BR-CANCEL-004 | Booking `CANCELLED` không được hủy lại. |
| BR-CANCEL-005 | Booking `CANCELLED` không còn chặn phòng trong availability search. |
