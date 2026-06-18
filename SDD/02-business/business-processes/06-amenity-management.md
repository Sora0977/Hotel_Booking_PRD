# 06 - Quản Lý Tiện Ích

## 1. Scope

| Process ID | Process | Actor |
| --- | --- | --- |
| BP-AMN-001 | Xem danh sách tiện ích | Guest, Customer, Admin |
| BP-AMN-002 | Tạo tiện ích mới | Admin |
| BP-AMN-003 | Cập nhật tiện ích | Admin |
| BP-AMN-004 | Xóa tiện ích hệ thống | Admin |
| BP-AMN-005 | Gán tiện ích cho khách sạn | Admin |
| BP-AMN-006 | Gỡ tiện ích khỏi khách sạn | Admin |
| BP-AMN-007 | Gán tiện ích cho phòng | Admin |
| BP-AMN-008 | Gỡ tiện ích khỏi phòng | Admin |

## 2. Shared Rules

| Rule ID | Rule |
| --- | --- |
| BR-AMN-001 | Tạo/sửa/xóa tiện ích hệ thống yêu cầu role `ADMIN`. |
| BR-AMN-002 | Tên tiện ích không được trùng. |
| BR-AMN-003 | Không được xóa tiện ích nếu đang được gán cho hotel hoặc room. |
| BR-AMN-004 | Gỡ tiện ích khỏi hotel/room chỉ xóa mapping, không xóa tiện ích gốc. |
| BR-AMN-005 | Admin chỉ gán/gỡ tiện ích trên hotel/room mình có quyền sở hữu. |

## 3. BP-AMN-001 - Xem Danh Sách Tiện Ích

| Field | Detail |
| --- | --- |
| Actor | Guest, Customer, Admin |
| Trigger | Actor mở thông tin tiện ích |
| Inputs | Optional `type` |
| Outputs | Amenity list |
| Data touched | `amenity` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Actor mở danh sách tiện ích hoặc chi tiết hotel/room. |
| 2 | System truy vấn tiện ích theo type hoặc mapping. |
| 3 | System trả danh sách tiện ích. |
| 4 | Frontend hiển thị tiện ích. |

## 4. BP-AMN-002 - Tạo Tiện Ích Mới

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn thêm tiện ích mới |
| Preconditions | Admin đã đăng nhập |
| Inputs | `name`, `type`, optional description/icon/image |
| Outputs | Created amenity |
| Data touched | `amenity` |
| Related screens | Quản lý tiện nghi, thêm tiện nghi |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin mở màn hình quản lý tiện ích. |
| 2 | Admin nhấn thêm tiện ích mới. |
| 3 | Admin nhập tên, loại, mô tả/icon nếu có. |
| 4 | System kiểm tra role Admin. |
| 5 | System validate dữ liệu. |
| 6 | System kiểm tra trùng tên. |
| 7 | System lưu tiện ích. |
| 8 | System trả thông báo thành công. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Duplicate name | Tên tiện ích đã tồn tại | Trả `DUPLICATE_AMENITY` |
| Invalid input | Thiếu tên/type | Trả validation error |

## 5. BP-AMN-003 - Cập Nhật Tiện Ích

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn lưu chỉnh sửa tiện ích |
| Preconditions | Tiện ích tồn tại |
| Inputs | Amenity fields |
| Outputs | Updated amenity |
| Data touched | `amenity` |
| Related screens | Chỉnh sửa tiện nghi |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin chọn tiện ích cần sửa. |
| 2 | System kiểm tra role Admin. |
| 3 | System kiểm tra tiện ích tồn tại. |
| 4 | Admin thay đổi thông tin. |
| 5 | System kiểm tra tên mới có trùng tiện ích khác không. |
| 6 | System lưu thay đổi. |
| 7 | System trả thông báo cập nhật thành công. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| Not found | Tiện ích không tồn tại hoặc đã bị xóa | Trả not found |
| Duplicate name | Tên mới bị trùng | Trả duplicate error |

## 6. BP-AMN-004 - Xóa Tiện Ích Hệ Thống

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn xóa tiện ích và xác nhận |
| Preconditions | Tiện ích tồn tại và chưa được sử dụng |
| Inputs | `amenityId`, confirmation |
| Outputs | Amenity deleted |
| Data touched | `amenity`, `hotel_amenity`, `room_amenity` |
| Related screens | Xác nhận xóa tiện nghi |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin nhấn xóa tiện ích. |
| 2 | Frontend hiển thị hộp thoại xác nhận. |
| 3 | Admin xác nhận. |
| 4 | System kiểm tra role Admin. |
| 5 | System kiểm tra tiện ích tồn tại. |
| 6 | System kiểm tra tiện ích có mapping trong hotel/room không. |
| 7 | Nếu không đang dùng, system xóa tiện ích. |
| 8 | System trả thông báo xóa thành công. |

### Error Flows

| Case | Condition | Behavior |
| --- | --- | --- |
| In use | Có record trong `hotel_amenity` hoặc `room_amenity` | Chặn xóa, trả `AMENITY_IN_USE` |
| Not found | Amenity ID không tồn tại | Trả not found |

## 7. BP-AMN-005 - Gán Tiện Ích Cho Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin chọn tiện ích để gán vào khách sạn |
| Preconditions | Admin là owner hotel, amenity tồn tại |
| Inputs | `hotelId`, `amenityId` |
| Outputs | `hotel_amenity` mapping |
| Data touched | `hotel`, `amenity`, `hotel_amenity` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin mở cấu hình tiện ích khách sạn. |
| 2 | Admin chọn tiện ích. |
| 3 | System kiểm tra hotel tồn tại. |
| 4 | System kiểm tra owner hotel. |
| 5 | System kiểm tra amenity tồn tại. |
| 6 | System kiểm tra mapping chưa tồn tại. |
| 7 | System tạo mapping `hotel_amenity`. |

## 8. BP-AMN-006 - Gỡ Tiện Ích Khỏi Khách Sạn

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn gỡ tiện ích khỏi khách sạn |
| Preconditions | Mapping tồn tại, Admin là owner hotel |
| Inputs | `hotelId`, `amenityId` |
| Outputs | Mapping removed |
| Data touched | `hotel_amenity` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin nhấn gỡ tiện ích. |
| 2 | Frontend yêu cầu xác nhận. |
| 3 | System kiểm tra owner hotel. |
| 4 | System xóa mapping `hotel_amenity`. |
| 5 | System không xóa record trong `amenity`. |
| 6 | System trả thông báo thành công. |

## 9. BP-AMN-007 - Gán Tiện Ích Cho Phòng

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin chọn tiện ích để gán vào phòng |
| Preconditions | Room tồn tại, Admin là owner hotel chứa room |
| Inputs | `roomId`, `amenityId` |
| Outputs | `room_amenity` mapping |
| Data touched | `room`, `amenity`, `room_amenity` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin mở cấu hình tiện ích phòng. |
| 2 | Admin chọn tiện ích. |
| 3 | System kiểm tra room tồn tại. |
| 4 | System kiểm tra owner của hotel chứa room. |
| 5 | System kiểm tra amenity tồn tại. |
| 6 | System kiểm tra mapping chưa tồn tại. |
| 7 | System tạo mapping `room_amenity`. |

## 10. BP-AMN-008 - Gỡ Tiện Ích Khỏi Phòng

| Field | Detail |
| --- | --- |
| Actor | Admin |
| Trigger | Admin nhấn gỡ tiện ích khỏi phòng |
| Preconditions | Mapping tồn tại, Admin là owner hotel chứa room |
| Inputs | `roomId`, `amenityId` |
| Outputs | Mapping removed |
| Data touched | `room_amenity` |

### Main Flow

| Step | Action |
| --- | --- |
| 1 | Admin nhấn gỡ tiện ích khỏi phòng. |
| 2 | Frontend yêu cầu xác nhận. |
| 3 | System kiểm tra owner của hotel chứa room. |
| 4 | System xóa mapping `room_amenity`. |
| 5 | System không xóa record trong `amenity`. |
| 6 | System trả thông báo thành công. |

