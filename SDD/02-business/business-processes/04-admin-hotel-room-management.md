# 04 - Admin Quản Lý Khách Sạn Và Phòng

## 1. Scope

| Process ID | Process | Actor |
| --- | --- | --- |
| BP-HR-001 | Xem danh sách khách sạn của tôi | Admin |
| BP-HR-002 | Thêm khách sạn mới | Admin |
| BP-HR-003 | Cập nhật khách sạn | Admin |
| BP-HR-004 | Xóa khách sạn | Admin |
| BP-HR-005 | Xem phòng theo khách sạn | Admin |
| BP-HR-006 | Thêm phòng mới | Admin |
| BP-HR-007 | Cập nhật phòng | Admin |
| BP-HR-008 | Xóa phòng | Admin |

## 2. Shared Rules

| Rule ID | Rule |
| --- | --- |
| BR-HR-001 | Mọi thao tác quản lý khách sạn/phòng yêu cầu role `ADMIN`. |
| BR-HR-002 | Admin chỉ sửa/xóa khách sạn do mình sở hữu. |
| BR-HR-003 | Admin chỉ thêm/sửa/xóa phòng trong khách sạn do mình sở hữu. |
| BR-HR-004 | Ảnh khách sạn/phòng upload lên Cloudinary hoặc storage tương đương. |
| BR-HR-005 | Database chỉ lưu URL ảnh, không lưu binary image. |
| BR-HR-006 | Tên và địa điểm khách sạn không được trùng. |

## 3. BP-HR-001 - Xem Danh Sách Khách Sạn Của Tôi

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin mở module quản lý khách sạn |
| Preconditions | Admin đã đăng nhập |
| Inputs | Current admin ID |
| Outputs | Admin-owned hotel list |
| Data touched | `hotel`, `image` |
| Related screens | Quản lý khách sạn |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin mở trang quản lý khách sạn. |
| 2 | System kiểm tra role Admin. |
| 3 | System lấy `currentAdminId` từ JWT. |
| 4 | System truy vấn hotel với `user_id = currentAdminId`. |
| 5 | System trả danh sách khách sạn. |
| 6 | Frontend hiển thị danh sách hoặc empty state. |

## 4. BP-HR-002 - Thêm Khách Sạn Mới

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn tạo khách sạn |
| Preconditions | Admin đã đăng nhập |
| Inputs | Hotel data, image files |
| Outputs | Created hotel |
| Data touched | `hotel`, `image` |
| Related screens | Thêm khách sạn |

### Required Inputs

| Field | Required |
| --- | --- |
| `name` | Yes |
| `description` | Yes |
| `location` | Yes |
| `phone` | Yes |
| `email` | Yes |
| `contactName` | Yes |
| `contactPhone` | Yes |
| `starRating` | Yes |
| Images | Yes |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin nhập thông tin khách sạn. |
| 2 | Admin chọn/tải ảnh khách sạn. |
| 3 | Frontend gửi request tạo khách sạn. |
| 4 | System kiểm tra role Admin. |
| 5 | System validate dữ liệu bắt buộc. |
| 6 | System kiểm tra trùng `name + location`. |
| 7 | System upload ảnh lên Cloudinary. |
| 8 | Cloudinary trả URL ảnh. |
| 9 | System tạo hotel với `user_id = currentAdminId`. |
| 10 | System lưu image records gắn `hotel_id`. |
| 11 | System trả hotel mới. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Duplicate hotel | Trùng tên và location | Trả `DUPLICATE_HOTEL` |
| Missing image | Không có ảnh hợp lệ | Trả validation error |
| Upload failed | Cloudinary lỗi | Không tạo hotel, trả upload error |
| Not admin | Role không hợp lệ | Trả forbidden |

## 5. BP-HR-003 - Cập Nhật Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn lưu chỉnh sửa khách sạn |
| Preconditions | Hotel tồn tại, Admin là owner |
| Inputs | Updated hotel data, optional new images |
| Outputs | Updated hotel |
| Data touched | `hotel`, `image` |
| Related screens | Chỉnh sửa khách sạn |

### Main Flow

| Step | Action                                                        |
| ---- | ------------------------------------------------------------- |
| 1    | Admin mở khách sạn cần chỉnh sửa.                             |
| 2    | System load hotel và kiểm tra owner.                          |
| 3    | Admin thay đổi thông tin.                                     |
| 4    | Admin tải ảnh mới nếu cần.                                    |
| 5    | System validate dữ liệu.                                      |
| 6    | System kiểm tra hotel vẫn tồn tại.                            |
| 7    | System kiểm tra owner bằng `hotel.user_id == currentAdminId`. |
| 8    | Nếu có ảnh mới, system upload ảnh và cập nhật URL.            |
| 9    | System lưu thay đổi.                                          |
| 10   | System trả thông tin mới.                                     |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Hotel not found | Hotel bị xóa hoặc ID sai | Trả `RESOURCE_NOT_FOUND` |
| Not owner | Admin không sở hữu khách sạn | Trả `AUTH_FORBIDDEN` |
| Invalid image | Ảnh sai định dạng | Trả image validation error |

## 6. BP-HR-004 - Xóa Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn xóa khách sạn và xác nhận |
| Preconditions | Hotel tồn tại, Admin là owner |
| Inputs | `hotelId`, confirmation |
| Outputs | Hotel removed/inactive |
| Data touched | `hotel`, possibly `room`, `image`, mapping tables |
| Related screens | Xác nhận xóa khách sạn |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin nhấn xóa khách sạn. |
| 2 | Frontend hiển thị xác nhận. |
| 3 | Admin xác nhận. |
| 4 | System kiểm tra role Admin. |
| 5 | System tìm hotel theo ID. |
| 6 | System kiểm tra owner. |
| 7 | System xóa hoặc vô hiệu hóa hotel theo policy. |
| 8 | System trả kết quả thành công. |

### Open Policy

| Question | Impact |
| --- | --- |
| Hard delete hay soft delete hotel? | Recommended: soft delete/deactivate (`is_active = 0`) to preserve room and booking history. |
| Có cho xóa hotel khi có booking chưa hoàn tất không? | Recommended: block destructive delete; allow deactivate only if active booking handling is explicit. |

## 7. BP-HR-005 - Xem Phòng Theo Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin chọn quản lý một khách sạn |
| Preconditions | Admin là owner hotel |
| Inputs | `hotelId` |
| Outputs | Room list |
| Data touched | `hotel`, `room`, `image`, `amenity` |
| Related screens | Quản lý một khách sạn cụ thể, quản lý phòng |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin chọn quản lý khách sạn. |
| 2 | System kiểm tra hotel tồn tại. |
| 3 | System kiểm tra owner. |
| 4 | System truy vấn room theo `hotel_id`. |
| 5 | Frontend hiển thị danh sách phòng. |

## 8. BP-HR-006 - Thêm Phòng Mới

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn thêm phòng |
| Preconditions | Hotel tồn tại, Admin là owner |
| Inputs | Room data, images, amenity IDs |
| Outputs | Created room |
| Data touched | `room`, `image`, `room_amenity` |
| Related screens | Thêm phòng mới |

### Required Inputs

| Field | Required |
| --- | --- |
| `hotelId` | Yes |
| `name` | Yes |
| `type` | Yes |
| `price` | Yes |
| `amount` | Yes |
| `capacity` | Yes |
| `description` | Yes |
| Images | Yes/Recommended by current screens |
| Amenity IDs | Optional |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin mở khách sạn mình quản lý. |
| 2 | Admin nhấn thêm phòng. |
| 3 | Admin nhập thông tin phòng. |
| 4 | Admin chọn ảnh và tiện ích. |
| 5 | System kiểm tra role Admin. |
| 6 | System kiểm tra hotel tồn tại. |
| 7 | System kiểm tra owner. |
| 8 | System validate loại phòng, giá, số lượng, sức chứa. |
| 9 | System upload ảnh lên Cloudinary. |
| 10 | System lưu room. |
| 11 | System lưu ảnh gắn `room_id`. |
| 12 | System lưu mapping `room_amenity`. |
| 13 | System trả room mới. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Not owner | Admin không sở hữu hotel | Trả forbidden |
| Invalid room type | Type không thuộc enum | Trả validation error |
| Invalid price/amount | Giá âm hoặc amount <= 0 | Trả validation error |
| Image upload failed | Cloudinary lỗi | Không lưu room |

## 9. BP-HR-007 - Cập Nhật Phòng

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn lưu chỉnh sửa phòng |
| Preconditions | Room tồn tại, Admin là owner của hotel chứa room |
| Inputs | Room fields, optional images, amenity IDs |
| Outputs | Updated room |
| Data touched | `room`, `image`, `room_amenity` |
| Related screens | Chỉnh sửa phòng |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin chọn chỉnh sửa phòng. |
| 2 | System load room và hotel chứa room. |
| 3 | System kiểm tra owner hotel. |
| 4 | Admin thay đổi thông tin. |
| 5 | System validate dữ liệu. |
| 6 | System kiểm tra `amount` mới không được nhỏ hơn số lượng phòng đã được đặt (`booked_quantity`) cao nhất trong bất kỳ ngày nào ở tương lai. |
| 7 | Nếu có ảnh mới, system upload ảnh. |
| 8 | System cập nhật room. |
| 9 | System cập nhật ảnh/tiện ích nếu có thay đổi. |
| 10 | System trả room mới. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Room quantity conflict | `new_amount < max(booked_quantity)` trong bất kỳ ngày nào ở tương lai | Trả `ROOM_QUANTITY_CONFLICT` |

## 10. BP-HR-008 - Xóa Phòng

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn xóa phòng và xác nhận |
| Preconditions | Room tồn tại, Admin là owner của hotel chứa room |
| Inputs | `roomId`, confirmation |
| Outputs | Room deleted/inactive |
| Data touched | `room`, `image`, `room_amenity` |
| Related screens | Xác nhận xóa phòng |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin nhấn xóa phòng. |
| 2 | Frontend hiển thị hộp thoại xác nhận. |
| 3 | Admin xác nhận. |
| 4 | System kiểm tra room tồn tại. |
| 5 | System kiểm tra owner của hotel chứa room. |
| 6 | System xóa hoặc vô hiệu hóa room theo policy. |
| 7 | System trả thông báo thành công. |

### Open Policy

| Question | Impact |
| --- | --- |
| Hard delete hay soft delete room? | Recommended: soft delete/deactivate when `room.is_active` exists; otherwise block delete if booking history exists. |
| Có cho xóa room đang có booking `BOOKED`/`CHECKED_IN` không? | Recommended: block hard delete; deactivate only after defining how active/future bookings are handled. |
