---
status: imported_chunk
last_updated: 2026-05-22
chapter: "03 - Thiết kế"
chunk: "3.1"
source_file: "../03_thiet_ke.md"
related_memory: ../../THESIS_MEMORY.md
school_rules: ../../SCHOOL_RULES.md
dependencies:
  - "../02_phuong_phap_thuc_hien/2_4_phan_tich_yeu_cau.md"
  - "3_2_mo_hinh_xu_ly/index.md"
---

<ai_context>
File này là mảnh Level-2 thuộc Chương 3, mục 3.1. Chứa mô hình dữ liệu mức ý niệm, mức luận lý và mức vật lý của hệ thống đặt phòng khách sạn; các khối PlantUML trong file là nguồn đối chiếu chính cho ERD, bảng dữ liệu và quan hệ dữ liệu.
</ai_context>

<system_instruction>
TUYỆT ĐỐI KHÔNG tự ý thay đổi, xóa, định dạng lại mã nguồn PlantUML hoặc code fence trừ khi tác vụ yêu cầu đích danh việc sửa mô hình dữ liệu. Khi sửa sơ đồ dữ liệu, phải đối chiếu dependencies trước và bảo toàn PK/FK, cardinality, tên bảng/cột, kiểu dữ liệu, quan hệ luận lý/vật lý và caption hình nếu không có yêu cầu rõ ràng.
</system_instruction>

## 3.1 Mô hình dữ liệu (mức ý niệm, mức luận lý, mức vật lý)

### 3.1.1 Mức ý niệm

> Hình 2.9: Mô hình dữ liệu mức ý niệm

![image-009.png](../../figures/imported/image-009.png)

### 3.1.2 Mức luận lý


```plantuml
@startuml
!theme plain

skinparam monochrome true
skinparam shadowing false
skinparam backgroundColor white
skinparam defaultFontName "Times New Roman"
skinparam defaultTextAlignment center
skinparam classAttributeIconSize 0
skinparam linetype ortho
hide circle

entity "Role" as role {
  * PK id : Integer
  --
  name : String
}

entity "User_Role" as user_role {
  * PK, FK user_id : Integer
  * PK, FK role_id : Integer
}

entity "User" as user {
  * PK id : Integer
  --
  full_name : String
  email : String
  password : String
  phone : String
  dob : Date
  is_active : Boolean
}

entity "Amenity" as amenity {
  * PK id : Integer
  --
  name : String
  type : String
}

entity "Hotel_Amenity" as hotel_amenity {
  * PK, FK hotel_id : Integer
  * PK, FK amenity_id : Integer
}

entity "Room_Amenity" as room_amenity {
  * PK, FK room_id : Integer
  * PK, FK amenity_id : Integer
}

entity "Hotel" as hotel {
  * PK id : Integer
  --
  name : String
  description : String
  location : String
  phone : String
  email : String
  contact_name : String
  star_rating : Integer
  is_active : Boolean
  * FK user_id : Integer
}

entity "Room" as room {
  * PK id : Integer
  --
  name : String
  type : Enum
  price : Money/Decimal
  amount : Integer
  capacity : Integer
  description : String
  * FK hotel_id : Integer
}

entity "Image" as image {
  * PK id : Integer
  --
  path : String
  * FK hotel_id : Integer
  * FK room_id : Integer
}

entity "Booking" as booking {
  * PK id : Integer
  --
  booking_reference : String
  customer_name : String
  total_price : Money
  status : Enum
  checkin_date : Date
  checkout_date : Date
  adult_amount : Integer
  children_amount : Integer
  booking_date : Date
  * FK user_id : Integer
}

entity "Booking_Room" as booking_room {
  * PK id : Integer
  --
  * FK booking_id : Integer
  * FK room_id : Integer
}

role ||--o{ user_role
user ||--o{ user_role

user ||--o{ hotel : owner
user ||--o{ booking : booker

hotel ||--o{ room
hotel ||--o{ image
room ||--o{ image

booking ||--|{ booking_room
room ||--o{ booking_room

hotel ||--o{ hotel_amenity
amenity ||--o{ hotel_amenity

room ||--o{ room_amenity
amenity ||--o{ room_amenity
@enduml
```
> Hình 2.10: Mô hình dữ liệu mức luận lý
### 3.1.3 Mức vật lý


```plantuml
@startuml
!theme plain

skinparam monochrome true
skinparam shadowing false
skinparam backgroundColor white
skinparam defaultFontName "Times New Roman"
skinparam defaultTextAlignment center
skinparam classAttributeIconSize 0
skinparam linetype ortho
hide circle

entity "role" as role_physical {
  * PK id : INT
  --
  * name : VARCHAR(255)
}

entity "user_role" as user_role_physical {
  * PK, FK role_id : INT
  * PK, FK user_id : INT
}

entity "user" as user_physical {
  * PK id : INT
  --
  * activate : BIT(1)
  created_at : DATETIME(6)
  * dob : DATE
  * email : VARCHAR(255)
  * full_name : VARCHAR(255)
  * password : VARCHAR(255)
  * phone : VARCHAR(255)
}

entity "amenity" as amenity_physical {
  * PK id : INT
  --
  * name : VARCHAR(255)
  * type : VARCHAR(255)
}

entity "hotel_amenity" as hotel_amenity_physical {
  * PK, FK amenity_id : INT
  * PK, FK hotel_id : INT
}

entity "room_amenity" as room_amenity_physical {
  * PK, FK amenity_id : INT
  * PK, FK room_id : INT
}

entity "hotel" as hotel_physical {
  * PK id : INT
  --
  * name : VARCHAR(255)
  * description : VARCHAR(255)
  * location : VARCHAR(255)
  * phone : VARCHAR(255)
  * email : VARCHAR(255)
  * contact_name : VARCHAR(255)
  * contact_phone : VARCHAR(255)
  * star_rating : INT
  * is_active : BIT(1)
  --
  * FK user_id : INT
}

entity "room" as room_physical {
  * PK id : INT
  --
  * name : VARCHAR(255)
  * type : ENUM('DOUBLE','SINGLE','SUIT','TRIPLE')
  * price : DECIMAL(38,2)
  * amount : INT
  * capacity : INT
  * description : VARCHAR(255)
  --
  * FK hotel_id : INT
}

entity "image" as image_physical {
  * PK id : INT
  --
  * path : VARCHAR(255)
  --
  * FK hotel_id : INT (NULL)
  * FK room_id : INT (NULL)
}

entity "booking" as booking_physical {
  * PK id : INT
  --
  * booking_reference : VARCHAR(255)
  * customer_name : VARCHAR(255)
  * total_price : FLOAT
  * status : ENUM('BOOKED','CANCELLED',...)
  * checkin_date : DATE
  * checkout_date : DATE
  * adult_amount : INT
  * children_amount : INT
  * create_at : DATE
  cancel_reason : VARCHAR(255)
  refund : FLOAT
  room_number : VARCHAR(10)
  special_require : VARCHAR(255)
  --
  * FK user_id : INT
}

entity "booking_room" as booking_room_physical {
  * PK id : INT
  --
  * FK booking_id : INT
  * FK room_id : INT
}

role_physical ||..o{ user_role_physical
user_physical ||..o{ user_role_physical

user_physical ||--o{ hotel_physical
user_physical ||--o{ booking_physical

hotel_physical ||--o{ room_physical
hotel_physical ||--o{ image_physical
room_physical ||--o{ image_physical

booking_physical ||--|{ booking_room_physical
room_physical ||--o{ booking_room_physical

hotel_physical ||--o{ hotel_amenity_physical
amenity_physical ||..o{ hotel_amenity_physical

room_physical ||..o{ room_amenity_physical
amenity_physical ||..o{ room_amenity_physical
@enduml
```
> Hình 2.11: Mô hình dữ liệu mức vật lý
### 3.1.4 Mô tả chi tiết bảng

Bảng Role

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| id | Mã định danh của quyền | INT | x | x | x |
| name | Tên quyền hạn (ví dụ: ADMIN) | VARCHAR(255) |  |  | x |

Bảng User

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| id | Mã định danh người dùng | INT | x | x | x |
| activate | Trạng thái kích hoạt (1: Active, 0: Inactive) | BIT(1) |  |  | x |
| created_at | Thời gian tạo tài khoản | DATETIME(6) |  |  |  |
| dob | Ngày sinh | DATE |  |  | x |
| email | Địa chỉ email | VARCHAR(255) |  |  | x |
| full_name | Họ và tên đầy đủ | VARCHAR(255) |  |  | x |
| password | Mật khẩu (đã mã hóa) | VARCHAR(255) |  |  | x |
| phone | Số điện thoại | VARCHAR(255) |  |  | x |

Bảng Hotel

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| id | Mã định danh khách sạn | INT | x | x | x |
| name | Tên khách sạn | VARCHAR(255) |  |  | x |
| description | Mô tả về khách sạn | VARCHAR(255) |  |  | x |
| location | Địa chỉ/Vị trí | VARCHAR(255) |  |  | x |
| star_rating | Xếp hạng sao (ví dụ: 3, 4, 5) | INT |  |  | x |
| contact_name | Tên người liên hệ | VARCHAR(255) |  |  | x |
| contact_phone | Số điện thoại liên hệ | VARCHAR(255) |  |  | x |
| email | Email của khách sạn | VARCHAR(255) |  |  | x |
| is_active | Trạng thái hoạt động | BIT(1) |  |  | x |
| user_id | Mã người dùng sở hữu (FK) | INT |  |  | x |

Bảng Room

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| id | Mã định danh phòng | INT | x | x | x |
| name | Tên phòng/Mã phòng | VARCHAR(255) |  |  | x |
| type | Loại phòng (DOUBLE, SINGLE, SUIT, TRIPLE) | ENUM |  |  | x |
| price | Giá phòng | DECIMAL(38,2) |  |  | x |
| capacity | Sức chứa (số người) | INT |  |  | x |
| amount | Số lượng phòng loại này | INT |  |  | x |
| description | Mô tả chi tiết phòng | VARCHAR(255) |  |  | x |
| hotel_id | Thuộc khách sạn nào (FK) | INT |  |  | x |

Bảng Booking

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| id | Mã đơn đặt phòng | INT | x | x | x |
| booking_reference | Mã tham chiếu đặt phòng | VARCHAR(255) |  |  | x |
| customer_name | Tên khách hàng đặt | VARCHAR(255) |  |  | x |
| checkin_date | Ngày nhận phòng | DATE |  |  | x |
| checkout_date | Ngày trả phòng | DATE |  |  | x |
| create_at | Ngày tạo đơn | DATE |  |  | x |
| total_price | Tổng giá trị đơn hàng | FLOAT |  |  | x |
| status | Trạng thái (BOOKED, CANCELLED...) | ENUM |  |  | x |
| adult_amount | Số lượng người lớn | INT |  |  | x |
| children_amount | Số lượng trẻ em | INT |  |  | x |
| user_id | Người dùng thực hiện đặt (FK) | INT |  |  | x |
| cancel_reason | Lý do hủy (nếu có) | VARCHAR(255) |  |  |  |
| refund | Số tiền hoàn lại (nếu có) | FLOAT |  |  |  |
| room_number | Số phòng được gán | VARCHAR(10) |  |  |  |
| special_require | Yêu cầu đặc biệt | VARCHAR(255) |  |  |  |

Bảng Amenity

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| id | Mã tiện nghi | INT | x | x | x |
| name | Tên tiện nghi | VARCHAR(255) |  |  | x |
| type | Loại tiện nghi | VARCHAR(255) |  |  | x |

Bảng Image

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| id | Mã hình ảnh | INT | x | x | x |
| path | Đường dẫn lưu file ảnh | VARCHAR(255) |  |  | x |
| hotel_id | Ảnh thuộc khách sạn nào (FK) | INT |  |  |  |
| room_id | Ảnh thuộc phòng nào (FK) | INT |  |  |  |

Bảng Booking_room

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| id | Mã chi tiết | INT | x | x | x |
| booking_id | Mã đơn đặt (FK) | INT |  |  | x |
| room_id | Mã phòng (FK) | INT |  |  | x |

Bảng Hotel_Amenity

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| amenity_id | Mã tiện nghi (FK) | INT | x |  | x |
| hotel_id | Mã khách sạn (FK) | INT | x |  | x |

Bảng Room_Amenity

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| amenity_id | Mã tiện nghi (FK) | INT | x |  | x |
| room_id | Mã phòng (FK) | INT | x |  | x |

Bảng User_Role

| Thuộc tính | Giải thích | Kiểu dữ liệu | K | U | M |
| --- | --- | --- | --- | --- | --- |
| role_id | Mã quyền (FK) | INT | x |  | x |
| user_id | Mã người dùng (FK) | INT | x |  | x |
