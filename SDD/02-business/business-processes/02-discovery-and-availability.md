# 02 - Tra Cứu Khách Sạn, Phòng Và Kiểm Tra Phòng Trống

## 1. Scope

| Process ID | Process | Actor |
| --- | --- | --- |
| BP-DISC-001 | Xem danh sách khách sạn | Guest, Customer |
| BP-DISC-002 | Xem chi tiết khách sạn | Guest, Customer |
| BP-DISC-003 | Tìm kiếm khách sạn | Guest, Customer |
| BP-DISC-004 | Xem danh sách phòng của khách sạn | Guest, Customer |
| BP-DISC-005 | Xem danh sách tất cả phòng | Guest, Customer |
| BP-DISC-006 | Xem chi tiết phòng | Guest, Customer |
| BP-DISC-007 | Tìm phòng theo từ khóa/loại phòng | Guest, Customer |
| BP-DISC-008 | Kiểm tra phòng trống theo ngày | Guest, Customer |

## 2. BP-DISC-001 - Xem Danh Sách Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer |
| Trigger | Actor mở trang danh sách khách sạn |
| Preconditions | None |
| Inputs | Pagination/filter optional |
| Outputs | Hotel list |
| Data touched | `hotel`, `image`, `hotel_amenity` |
| Related screens | Xem tất cả khách sạn |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor mở danh sách khách sạn. |
| 2 | System truy vấn các hotel active. |
| 3 | System load ảnh đại diện và thông tin tóm tắt. |
| 4 | System trả danh sách cho frontend. |
| 5 | Frontend hiển thị danh sách hoặc empty state. |

### Display Fields

| Field | Source |
| --- | --- |
| Tên khách sạn | `hotel.name` |
| Địa điểm | `hotel.location` |
| Ảnh đại diện | `image.path` where `hotel_id` |
| Số sao | `hotel.star_rating` |
| Mô tả ngắn | `hotel.description` |

## 3. BP-DISC-002 - Xem Chi Tiết Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer |
| Trigger | Actor click vào khách sạn |
| Preconditions | Hotel ID tồn tại |
| Inputs | `hotelId` |
| Outputs | Hotel detail |
| Data touched | `hotel`, `room`, `image`, `amenity`, `hotel_amenity` |
| Related screens | Chi tiết khách sạn |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor chọn khách sạn từ danh sách/kết quả tìm kiếm. |
| 2 | System tìm hotel theo ID. |
| 3 | System kiểm tra hotel tồn tại và active. |
| 4 | System load ảnh, tiện ích, thông tin liên hệ. |
| 5 | System load danh sách phòng thuộc hotel. |
| 6 | Frontend hiển thị trang chi tiết khách sạn. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Hotel not found | `hotelId` không tồn tại | Hiển thị 404 hoặc thông báo không tìm thấy |
| Hotel inactive | Hotel bị vô hiệu hóa | Không hiển thị public hoặc trả not found |

## 4. BP-DISC-003 - Tìm Kiếm Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer |
| Trigger | Actor nhập tiêu chí tìm kiếm |
| Preconditions | None |
| Inputs | `location`, `checkinDate`, `checkoutDate`, optional guest count |
| Outputs | Hotel search results |
| Data touched | `hotel`, `room`, `booking`, `booking_room` |
| Related screens | Trang chủ, danh sách khách sạn |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor nhập địa điểm và ngày lưu trú. |
| 2 | Frontend gửi request tìm kiếm. |
| 3 | System validate ngày: check-out sau check-in. |
| 4 | System tìm hotel theo location. |
| 5 | Nếu có ngày lưu trú, system kiểm tra hotel có phòng khả dụng. |
| 6 | System trả danh sách khách sạn phù hợp. |
| 7 | Frontend hiển thị kết quả. |

### Error/Empty Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Invalid date | Check-out <= check-in hoặc check-in trong quá khứ | Hiển thị lỗi ngày không hợp lệ |
| No result | Không có khách sạn phù hợp | Hiển thị empty state |

## 5. BP-DISC-004 - Xem Danh Sách Phòng Của Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer |
| Trigger | Actor mở chi tiết khách sạn hoặc nhấn xem phòng |
| Preconditions | Hotel tồn tại |
| Inputs | `hotelId`, optional date filters |
| Outputs | Room list under hotel |
| Data touched | `hotel`, `room`, `image`, `room_amenity`, `amenity` |
| Related screens | Danh sách phòng của khách sạn |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor ở trang chi tiết khách sạn. |
| 2 | Actor cuộn tới danh sách phòng hoặc nhấn xem phòng trống. |
| 3 | System kiểm tra hotel tồn tại. |
| 4 | System truy vấn room theo `hotel_id`. |
| 5 | System load ảnh và tiện ích phòng. |
| 6 | Frontend hiển thị danh sách phòng. |

## 6. BP-DISC-005 - Xem Danh Sách Tất Cả Phòng

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer |
| Trigger | Actor mở trang danh sách phòng |
| Preconditions | None |
| Inputs | Pagination/filter optional |
| Outputs | Room list |
| Data touched | `room`, `hotel`, `image`, `amenity` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor mở danh sách phòng. |
| 2 | System truy vấn room đang khả dụng. |
| 3 | System trả thông tin tóm tắt phòng. |
| 4 | Frontend hiển thị danh sách. |

### Display Fields

| Field | Source |
| --- | --- |
| Tên phòng | `room.name` |
| Loại phòng | `room.type` |
| Giá | `room.price` |
| Sức chứa | `room.capacity` |
| Số lượng | `room.amount` |
| Khách sạn | `hotel.name` |
| Ảnh | `image.path` where `room_id` |

## 7. BP-DISC-006 - Xem Chi Tiết Phòng

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer |
| Trigger | Actor click vào phòng |
| Preconditions | Room ID tồn tại |
| Inputs | `roomId` |
| Outputs | Room detail and booking form |
| Data touched | `room`, `hotel`, `image`, `amenity` |
| Related screens | Chi tiết phòng và form đặt phòng |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor chọn phòng. |
| 2 | System tìm room theo ID. |
| 3 | System load hotel chứa phòng. |
| 4 | System load ảnh và tiện ích phòng. |
| 5 | Frontend hiển thị chi tiết phòng và form đặt phòng. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Room not found | `roomId` không tồn tại | Hiển thị 404 hoặc thông báo không tìm thấy |

## 8. BP-DISC-007 - Tìm Phòng Theo Từ Khóa/Loại Phòng

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer |
| Trigger | Actor nhập keyword hoặc chọn loại phòng |
| Inputs | `keyword`, `type`, optional filters |
| Outputs | Room results |
| Data touched | `room`, `hotel`, `image` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor nhập keyword hoặc chọn loại phòng. |
| 2 | System validate filter. |
| 3 | System query room theo keyword/type. |
| 4 | System trả danh sách kết quả. |
| 5 | Frontend hiển thị danh sách hoặc empty state. |

### Search Rules

| Rule | Detail |
| --- | --- |
| Keyword | Match theo tên phòng hoặc mô tả phòng. |
| Room type | Một trong `SINGLE`, `DOUBLE`, `TRIPLE`, `SUIT`. |
| Empty result | Không lỗi hệ thống, chỉ hiển thị không có kết quả. |

## 9. BP-DISC-008 - Kiểm Tra Phòng Trống Theo Ngày

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer |
| Trigger | Actor tìm phòng trống hoặc tạo booking |
| Inputs | `location`, `roomId` optional, `checkinDate`, `checkoutDate`, `adultAmount`, `childrenAmount`, `quantity` |
| Outputs | Available room list or availability result |
| Data touched | `hotel`, `room`, `booking`, `booking_room` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor nhập location, ngày check-in/check-out, số khách, số lượng phòng. |
| 2 | System validate ngày. |
| 3 | System lấy hotel theo location hoặc room cụ thể nếu đang ở trang chi tiết. |
| 4 | System lấy các room ứng viên. |
| 5 | System tìm booking có trạng thái `BOOKED` hoặc `CHECKED_IN`. |
| 6 | System loại room có booking giao ngày với khoảng tìm kiếm. |
| 7 | System kiểm tra `room.capacity` đáp ứng tổng khách. |
| 8 | System kiểm tra số lượng còn lại theo `room.amount`. |
| 9 | System trả danh sách phòng trống. |

### Availability Formula

| Rule ID | Formula |
| --- | --- |
| BR-AVAIL-001 | Existing booking conflicts if `existing_checkin < new_checkout AND existing_checkout > new_checkin`. |
| BR-AVAIL-002 | Only statuses `BOOKED` and `CHECKED_IN` block availability. |
| BR-AVAIL-003 | `requested_quantity + booked_quantity <= room.amount`. |
| BR-AVAIL-004 | `adultAmount + childrenAmount <= room.capacity` unless policy defines child capacity differently. |

### Error Flows

| Case | Condition | System Behavior |
| --- | --- | --- |
| Invalid date | Check-in in past or checkout before/equal checkin | Return validation error |
| No room | No room meets filters | Return empty result, not system error |
| Capacity exceeded | Guest count exceeds room capacity | Exclude room or return capacity error in booking flow |

