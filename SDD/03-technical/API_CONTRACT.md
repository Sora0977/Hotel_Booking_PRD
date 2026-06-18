# API Contract - Hotel Booking

## 1. Metadata

| Field | Value |
| --- | --- |
| Document type | API Contract |
| Product | Hotel Booking |
| Depends on | `SDD/01-product/PRD.md`, `SDD/03-technical/TECH_SPEC.md`, `SDD/02-business/BUSINESS_PROCESS.md` |
| Purpose | Stable API reference for AI maintenance and feature development |

## 2. API Conventions

### 2.1 Base URL

| Environment | Base URL |
| --- | --- |
| Local | `http://localhost:<backend-port>/api` |
| Production | `https://<domain>/api` |

### 2.2 Authentication

| Type | Header |
| --- | --- |
| JWT Bearer | `Authorization: Bearer <token>` |

| Token Policy | Rule |
| --- | --- |
| Expiry source | Clients should rely on the JWT `exp` claim. |
| Baseline validity | Chapter 2 source and `BP-AUTH-002` state a 6-month token validity. |
| Production hardening | If the project switches to short-lived access tokens plus refresh tokens, update `TECH_SPEC`, this contract, logout/blacklist behavior, and frontend storage rules together. |

### 2.3 Standard Success Response

```json
{
  "success": true,
  "message": "OK",
  "data": {}
}
```

### 2.4 Standard Error Response

All API errors MUST return this JSON shape. Do not create endpoint-specific error shapes.

```json
{
  "timestamp": "2026-05-18T10:15:30Z",
  "status_code": 400,
  "error_code": "VALIDATION_ERROR",
  "message": "Invalid request data",
  "path": "/api/auth/register",
  "details": [
    {
      "field": "email",
      "rejected_value": "invalid-email",
      "message": "email must match ^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
    }
  ]
}
```

| Field | Type | Required | Constraint |
| --- | --- | --- | --- |
| `timestamp` | string | Yes | ISO-8601 UTC datetime, format `YYYY-MM-DDTHH:mm:ssZ` |
| `status_code` | number | Yes | Must match HTTP response status |
| `error_code` | string | Yes | Must match Error Code Mapping below |
| `message` | string | Yes | Human-readable stable message; do not expose stack trace |
| `path` | string | Yes | Request path beginning with `/api` |
| `details` | array | Yes | Empty array allowed; field-level validation errors only |

#### Error Code Mapping

| Error Code | HTTP Status | Applies To | Condition |
| --- | --- | --- | --- |
| `VALIDATION_ERROR` | `400 Bad Request` | All APIs | Request body/query/path parameter fails validation |
| `AUTH_UNAUTHORIZED` | `401 Unauthorized` | Protected APIs | Missing, expired, malformed, or invalid JWT |
| `AUTH_INVALID_CREDENTIALS` | `401 Unauthorized` | Login, change password | Email/password or old password is incorrect |
| `AUTH_ACCOUNT_LOCKED` | `403 Forbidden` | Login | User exists but `activate = false` |
| `AUTH_FORBIDDEN` | `403 Forbidden` | Admin/owner APIs | Actor lacks role or ownership permission |
| `RESOURCE_NOT_FOUND` | `404 Not Found` | Entity lookup APIs | Requested entity does not exist or is not visible to actor |
| `DUPLICATE_EMAIL` | `409 Conflict` | Register/user update | Email already exists |
| `DUPLICATE_HOTEL` | `409 Conflict` | Create/update hotel | Same hotel `name + location` already exists |
| `DUPLICATE_AMENITY` | `409 Conflict` | Create/update amenity | Amenity name already exists |
| `PASSWORD_REUSED` | `409 Conflict` | Change password | New password matches old password |
| `ROOM_UNAVAILABLE` | `409 Conflict` | Availability/booking | Room is blocked by overlapping active booking |
| `ROOM_QUANTITY_EXCEEDED` | `409 Conflict` | Availability/booking | Requested quantity exceeds available room amount |
| `ROOM_QUANTITY_CONFLICT` | `409 Conflict` | Update room | Không thể giảm số lượng phòng xuống thấp hơn số lượng đang được đặt trong tương lai |
| `ROOM_NUMBER_OCCUPIED` | `409 Conflict` | Check-in | Physical room number is already assigned to active checked-in booking |
| `BOOKING_CANNOT_CANCEL` | `409 Conflict` | Cancel booking | Booking status does not allow cancellation |
| `AMENITY_IN_USE` | `409 Conflict` | Delete amenity | Amenity is still linked to at least one hotel or room |
| `IMAGE_UPLOAD_FAILED` | `502 Bad Gateway` | Hotel/room image upload | Cloud/storage provider upload failed |
| `INTERNAL_SERVER_ERROR` | `500 Internal Server Error` | All APIs | Unhandled server error |

### 2.5 Pagination Query And Response

| Param | Type | Default | Notes |
| --- | --- | --- | --- |
| `page` | number | `0` | Zero-based page index; min `0` |
| `size` | number | `20` | Page size; min `1`, max `100` |
| `sort` | string | `created_at,desc` | Format `<field>,<asc|desc>` |

#### Paginated Success Response

All GET list APIs MUST return this JSON shape.

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "content": [],
    "page": 0,
    "size": 20,
    "sort": "created_at,desc",
    "total_elements": 125,
    "total_pages": 7,
    "first": true,
    "last": false,
    "number_of_elements": 20
  }
}
```

| Field | Type | Required | Constraint |
| --- | --- | --- | --- |
| `content` | array | Yes | List item DTOs; empty array allowed |
| `page` | number | Yes | Current zero-based page index |
| `size` | number | Yes | Current page size |
| `sort` | string | Yes | Applied sort in `<field>,<asc|desc>` format |
| `total_elements` | number | Yes | Total matching records before pagination |
| `total_pages` | number | Yes | `ceil(total_elements / size)` |
| `first` | boolean | Yes | `true` when `page = 0` |
| `last` | boolean | Yes | `true` when `page + 1 >= total_pages` |
| `number_of_elements` | number | Yes | Number of items in current `content` |

#### GET List APIs Requiring Pagination

| API ID | Method | Path | Default Pagination |
| --- | --- | --- | --- |
| API-USER-004 | `GET` | `/admin/users` | `page=0&size=20&sort=created_at,desc` |
| API-HOTEL-001 | `GET` | `/hotels` | `page=0&size=20&sort=created_at,desc` |
| API-HOTEL-003 | `GET` | `/hotels/{id}/rooms` | `page=0&size=20&sort=created_at,desc` |
| API-HOTEL-004 | `GET` | `/admin/hotels` | `page=0&size=20&sort=created_at,desc` |
| API-ROOM-001 | `GET` | `/rooms` | `page=0&size=20&sort=created_at,desc` |
| API-ROOM-003 | `GET` | `/rooms/available` | `page=0&size=20&sort=created_at,desc` |
| API-BOOK-002 | `GET` | `/bookings/me` | `page=0&size=20&sort=created_at,desc` |
| API-BOOK-006 | `GET` | `/admin/bookings` | `page=0&size=20&sort=created_at,desc` |
| API-AMN-001 | `GET` | `/amenities` | `page=0&size=20&sort=created_at,desc` |

### 2.6 Validation Constraint Catalog

All request DTOs, query parameters, database writes, and frontend forms MUST use the same constraints below.

#### Primitive Formats

| Validation ID | Field Pattern | Type | Required Constraint |
| --- | --- | --- | --- |
| VAL-ID-001 | `id`, `hotelId`, `roomId`, `amenityId`, `roleId`, `userId` | integer | Min `1`; path/query IDs must be positive integers |
| VAL-EMAIL-001 | `email` | string | Trim, lowercase before unique check; max length `255`; regex `^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$` |
| VAL-PASSWORD-001 | `password`, `oldPassword`, `newPassword`, `confirmPassword` | string | Min length `8`, max length `72`; must contain at least one letter and one digit; regex `^(?=.*[A-Za-z])(?=.*\\d).{8,72}$` |
| VAL-PHONE-001 | `phone`, `contactPhone`, `customerPhone` | string | VN phone only; max length `20`; regex `^(0|\\+84)(2[0-9]{8,9}|[35789][0-9]{8})$` |
| VAL-DATE-001 | `dob`, `checkinDate`, `checkoutDate` | string | ISO date only; format `YYYY-MM-DD`; regex `^\\d{4}-\\d{2}-\\d{2}$` |
| VAL-PRICE-001 | `price`, `totalPrice`, `refund` | decimal | Min `0`; decimal precision `15,2`; max `9999999999999.99`; no floating-point storage |
| VAL-IMAGE-URL-001 | `imageUrl`, `imageUrls[]`, `path` | string | HTTPS URL only; max length `1024`; regex `^https://.{1,1016}$` |
| VAL-NAME-001 | `fullName`, `customerName`, `contactName`, `name` | string | Trim; min length `1`; max length `255`; must not be blank |
| VAL-DESC-001 | `description`, `specialRequire`, `cancelReason` | string | Trim; max length `255`; optional fields may be `null` |
| VAL-BOOK-REF-001 | `bookingReference` | string | Uppercase alphanumeric; length `10`; regex `^[A-Z0-9]{10}$` |
| VAL-ROOM-NUMBER-001 | `roomNumber` | string | Max length `255`; regex `^[A-Za-z0-9-,\s]{1,255}$`; comma-separated values allowed when `quantity > 1`, example `"301, 302"` |

#### Domain Field Constraints

| Field | Required | Constraint |
| --- | --- | --- |
| `dob` | Yes for register/profile | Must be before current date |
| `checkinDate` | Yes for availability/booking | Must be `>=` current date |
| `checkoutDate` | Yes for availability/booking | Must be `>` `checkinDate` |
| `adultAmount` | Yes for availability/booking | Integer min `1`, max `20` |
| `childrenAmount` | Yes for availability/booking | Integer min `0`, max `20` |
| `quantity` | Yes for availability/booking | Integer min `1`; must not exceed available quantity |
| `amount` | Yes for room write | Integer min `1`, max `999` |
| `capacity` | Yes for room write | Integer min `1`, max `20` |
| `starRating` | Yes for hotel write | Integer min `1`, max `5` |
| `type` for room | Yes for room write | One of `SINGLE`, `DOUBLE`, `TRIPLE`, `SUIT` |
| `type` for amenity | Yes for amenity write | One of `HOTEL_SERVICE`, `ROOM_FEATURE` |
| `imageUrls` | Yes for hotel/room write | Array size min `1`, max `20`; each item must satisfy `VAL-IMAGE-URL-001` |

## 3. Auth APIs

### 3.1 Register

| Field | Value |
| --- | --- |
| API ID | API-AUTH-001 |
| Method | `POST` |
| Path | `/auth/register` |
| Access | Public |
| Business process | `BP-AUTH-001` |

#### Request

```json
{
  "fullName": "Nguyen Van A",
  "email": "customer@example.com",
  "phone": "0900000000",
  "dob": "1999-01-01",
  "password": "secret123"
}
```

#### Response

```json
{
  "id": 1,
  "fullName": "Nguyen Van A",
  "email": "customer@example.com",
  "phone": "0900000000",
  "dob": "1999-01-01",
  "activate": true,
  "roles": ["CUSTOMER"]
}
```

Token expiry is carried by the JWT `exp` claim. The source baseline is 6 months; do not add refresh-token fields to this response unless the token policy is explicitly changed.

#### Errors

| Error Code | HTTP | Condition |
| --- | --- | --- |
| `VALIDATION_ERROR` | `400` | Missing or invalid field |
| `DUPLICATE_EMAIL` | `409` | Email already exists |

### 3.2 Login

| Field | Value |
| --- | --- |
| API ID | API-AUTH-002 |
| Method | `POST` |
| Path | `/auth/login` |
| Access | Public |
| Business process | `BP-AUTH-002` |

#### Request

```json
{
  "email": "customer@example.com",
  "password": "secret123"
}
```

#### Response

```json
{
  "token": "<jwt-token>",
  "user": {
    "id": 1,
    "fullName": "Nguyen Van A",
    "email": "customer@example.com",
    "roles": ["CUSTOMER"]
  }
}
```

#### Errors

| Error Code | HTTP | Condition |
| --- | --- | --- |
| `AUTH_INVALID_CREDENTIALS` | `401` | Email not found or password mismatch |
| `AUTH_ACCOUNT_LOCKED` | `403` | User `activate = false` |

### 3.3 Logout

| Field | Value |
| --- | --- |
| API ID | API-AUTH-003 |
| Method | `POST` |
| Path | `/auth/logout` |
| Access | Authenticated |
| Business process | `BP-AUTH-003` |

#### Response

```json
{
  "message": "Logged out"
}
```

### 3.4 Change Password

| Field | Value |
| --- | --- |
| API ID | API-AUTH-004 |
| Method | `PUT` |
| Path | `/auth/password` |
| Access | Authenticated |
| Business process | `BP-AUTH-006` |

#### Request

```json
{
  "oldPassword": "oldSecret1",
  "newPassword": "newSecret1",
  "confirmPassword": "newSecret1"
}
```

#### Errors

| Error Code | HTTP | Condition |
| --- | --- | --- |
| `VALIDATION_ERROR` | `400` | New password invalid or confirmation mismatch |
| `AUTH_INVALID_CREDENTIALS` | `401` | Old password does not match |
| `PASSWORD_REUSED` | `409` | New password matches old password |

## 4. User APIs

| API ID | Method | Path | Access | Process | Description |
| --- | --- | --- | --- | --- | --- |
| API-USER-001 | `GET` | `/users/me` | Authenticated | `BP-AUTH-004` | Get current user profile |
| API-USER-002 | `PUT` | `/users/me` | Authenticated | `BP-AUTH-005` | Update current user profile |
| API-USER-003 | `DELETE` | `/users/me` | Authenticated | `BP-AUTH-007` | Delete/deactivate own account |
| API-USER-004 | `GET` | `/admin/users` | Admin | `BP-AUTH-008` | List users |
| API-USER-005 | `PATCH` | `/admin/users/{id}/lock` | Admin | `BP-AUTH-009` | Lock user |
| API-USER-006 | `PATCH` | `/admin/users/{id}/unlock` | Admin | `BP-AUTH-010` | Unlock user |

### 4.1 Update Profile Request

```json
{
  "fullName": "Nguyen Van A",
  "phone": "0900000000",
  "dob": "1999-01-01"
}
```

## 5. Hotel APIs

| API ID | Method | Path | Access | Process | Description |
| --- | --- | --- | --- | --- | --- |
| API-HOTEL-001 | `GET` | `/hotels` | Public | `BP-DISC-001`, `BP-DISC-003` | List/search hotels |
| API-HOTEL-002 | `GET` | `/hotels/{id}` | Public | `BP-DISC-002` | Get hotel detail |
| API-HOTEL-003 | `GET` | `/hotels/{id}/rooms` | Public | `BP-DISC-004` | Get rooms of a hotel |
| API-HOTEL-004 | `GET` | `/admin/hotels` | Admin | `BP-HR-001` | List current admin's hotels |
| API-HOTEL-005 | `POST` | `/admin/hotels` | Admin | `BP-HR-002` | Create hotel |
| API-HOTEL-006 | `PUT` | `/admin/hotels/{id}` | Admin owner | `BP-HR-003` | Update hotel |
| API-HOTEL-007 | `DELETE` | `/admin/hotels/{id}` | Admin owner | `BP-HR-004` | Delete/deactivate hotel |

### 5.1 Search Hotels Query

| Param | Type | Required | Notes |
| --- | --- | --- | --- |
| `location` | string | No | Hotel location/city/address keyword |
| `checkinDate` | date | No | Required if checking availability |
| `checkoutDate` | date | No | Required if checking availability |
| `adultAmount` | number | No | Capacity filter |
| `childrenAmount` | number | No | Capacity filter |
| `page` | integer | No | Default `0`; see section `2.5 Pagination Query And Response` |
| `size` | integer | No | Default `20`, max `100`; see section `2.5 Pagination Query And Response` |
| `sort` | string | No | Default `created_at,desc`; see section `2.5 Pagination Query And Response` |

#### Future Search Filters From Benchmark

These filters come from the Booking.com/Traveloka benchmark in Chapter 2 and are not mandatory until explicitly moved into MVP scope.

| Param | Type | Applies To | Notes |
| --- | --- | --- | --- |
| `priceMin`, `priceMax` | decimal | Hotel/room search | Requires stable room price aggregation for hotel results |
| `amenityIds` | number[] | Hotel/room search | Filter by mapped hotel/room amenities |
| `starRating` | number | Hotel search | Integer `1..5` |
| `reviewScore` | decimal | Hotel/room search | Requires review/rating feature |
| `sort=price|rating|distance` | string | Hotel/room search | Requires normalized price/rating/location data |

### 5.2 Create/Update Hotel Request

```json
{
  "name": "Demo Hotel",
  "description": "Hotel description",
  "location": "Ho Chi Minh City",
  "phone": "0280000000",
  "email": "hotel@example.com",
  "contactName": "Hotel Manager",
  "contactPhone": "0900000000",
  "starRating": 4,
  "imageUrls": ["https://res.cloudinary.com/.../hotel.jpg"],
  "amenityIds": [1, 2, 3]
}
```

### 5.3 Hotel Errors

| Error Code | HTTP | Condition |
| --- | --- | --- |
| `RESOURCE_NOT_FOUND` | `404` | Hotel not found |
| `AUTH_FORBIDDEN` | `403` | Admin does not own hotel |
| `DUPLICATE_HOTEL` | `409` | Same hotel name and location |
| `IMAGE_UPLOAD_FAILED` | `502` | Cloud/storage provider upload failed |

## 6. Room APIs

| API ID | Method | Path | Access | Process | Description |
| --- | --- | --- | --- | --- | --- |
| API-ROOM-001 | `GET` | `/rooms` | Public | `BP-DISC-005`, `BP-DISC-007` | List/search rooms |
| API-ROOM-002 | `GET` | `/rooms/{id}` | Public | `BP-DISC-006` | Get room detail |
| API-ROOM-003 | `GET` | `/rooms/available` | Public | `BP-DISC-008` | Search available rooms |
| API-ROOM-004 | `POST` | `/admin/hotels/{hotelId}/rooms` | Admin owner | `BP-HR-006` | Create room |
| API-ROOM-005 | `PUT` | `/admin/rooms/{id}` | Admin owner | `BP-HR-007` | Update room |
| API-ROOM-006 | `DELETE` | `/admin/rooms/{id}` | Admin owner | `BP-HR-008` | Delete/deactivate room |

### 6.1 Available Rooms Query

| Param | Type | Required | Notes |
| --- | --- | --- | --- |
| `location` | string | No | Required if not searching by hotel/room context |
| `hotelId` | number | No | Filter rooms by hotel |
| `roomId` | number | No | Check one room |
| `checkinDate` | date | Yes | Must be `>= today` |
| `checkoutDate` | date | Yes | Must be after `checkinDate` |
| `adultAmount` | number | Yes | Capacity |
| `childrenAmount` | number | Yes | Capacity |
| `quantity` | number | Yes | Requested room quantity |
| `page` | integer | No | Default `0`; see section `2.5 Pagination Query And Response` |
| `size` | integer | No | Default `20`, max `100`; see section `2.5 Pagination Query And Response` |
| `sort` | string | No | Default `created_at,desc`; see section `2.5 Pagination Query And Response` |

### 6.2 Create/Update Room Request

```json
{
  "name": "Deluxe Double",
  "type": "DOUBLE",
  "price": 1200000,
  "amount": 5,
  "capacity": 2,
  "description": "Room description",
  "imageUrls": ["https://res.cloudinary.com/.../room.jpg"],
  "amenityIds": [4, 5, 6]
}
```

### 6.3 Room Errors

| Error Code | HTTP | Condition |
| --- | --- | --- |
| `RESOURCE_NOT_FOUND` | `404` | Room or hotel not found |
| `AUTH_FORBIDDEN` | `403` | Admin does not own hotel/room |
| `VALIDATION_ERROR` | `400` | Invalid type, price, amount, capacity, dates |
| `ROOM_UNAVAILABLE` | `409` | Room blocked by overlapping booking |
| `ROOM_QUANTITY_EXCEEDED` | `409` | Requested quantity exceeds available amount |
| `ROOM_QUANTITY_CONFLICT` | `409` | Không thể giảm số lượng phòng xuống thấp hơn số lượng đang được đặt trong tương lai |

## 7. Booking APIs

| API ID | Method | Path | Access | Process | Description |
| --- | --- | --- | --- | --- | --- |
| API-BOOK-001 | `POST` | `/bookings` | Authenticated | `BP-BOOK-001` | Create booking |
| API-BOOK-002 | `GET` | `/bookings/me` | Authenticated | `BP-BOOK-003` | Current user's booking history |
| API-BOOK-003 | `GET` | `/bookings/reference/{reference}` | Authenticated | `BP-BOOK-004` | Lookup booking by reference |
| API-BOOK-004 | `GET` | `/bookings/{id}` | Owner/Admin | `BP-BOOK-005` | Booking detail |
| API-BOOK-005 | `PATCH` | `/bookings/{id}/cancel` | Owner/Admin | `BP-BOOK-006` | Cancel booking |
| API-BOOK-006 | `GET` | `/admin/bookings` | Admin | `BP-OPS-001`, `BP-OPS-002` | Admin booking list/search |
| API-BOOK-007 | `PATCH` | `/admin/bookings/{id}/check-in` | Admin | `BP-OPS-003` | Check-in booking |
| API-BOOK-008 | `PATCH` | `/admin/bookings/{id}/check-out` | Admin | `BP-OPS-004` | Check-out booking |

### 7.1 Create Booking Request

```json
{
  "roomId": 10,
  "checkinDate": "2026-06-01",
  "checkoutDate": "2026-06-03",
  "quantity": 1,
  "adultAmount": 2,
  "childrenAmount": 0,
  "customerName": "Nguyen Van A",
  "customerPhone": "0900000000",
  "specialRequire": "Late check-in"
}
```

Note: MVP chỉ hỗ trợ đặt 1 loại phòng (Room Type) trên mỗi Booking. Cấu trúc DB hỗ trợ Many-to-Many nhưng API chỉ nhận 1 `roomId`.

### 7.2 Booking Response

```json
{
  "id": 100,
  "bookingReference": "A1B2C3D4E5",
  "customerName": "Nguyen Van A",
  "customerPhone": "0900000000",
  "status": "BOOKED",
  "checkinDate": "2026-06-01",
  "checkoutDate": "2026-06-03",
  "adultAmount": 2,
  "childrenAmount": 0,
  "totalPrice": 2400000,
  "specialRequire": "Late check-in",
  "cancelReason": null,
  "room": {
    "id": 10,
    "name": "Deluxe Double",
    "type": "DOUBLE",
    "quantity": 1,
    "roomNumber": null
  },
  "hotel": {
    "id": 2,
    "name": "Demo Hotel"
  }
}
```

### 7.3 Cancel Booking Request

```json
{
  "cancelReason": "Change of travel plan"
}
```

### 7.4 Check-In Request

```json
{
  "roomNumber": "301"
}
```

### 7.5 Booking Errors

| Error Code | HTTP | Condition |
| --- | --- | --- |
| `RESOURCE_NOT_FOUND` | `404` | Booking/room not found |
| `AUTH_FORBIDDEN` | `403` | Customer is not owner and not Admin |
| `VALIDATION_ERROR` | `400` | Invalid date, quantity, capacity |
| `ROOM_UNAVAILABLE` | `409` | Overlapping active booking |
| `ROOM_QUANTITY_EXCEEDED` | `409` | Not enough room quantity |
| `BOOKING_CANNOT_CANCEL` | `409` | Booking already checked out/cancelled |
| `ROOM_NUMBER_OCCUPIED` | `409` | Physical room number already in use |

## 8. Amenity APIs

| API ID | Method | Path | Access | Process | Description |
| --- | --- | --- | --- | --- | --- |
| API-AMN-001 | `GET` | `/amenities` | Public | `BP-AMN-001` | List amenities |
| API-AMN-002 | `POST` | `/admin/amenities` | Admin | `BP-AMN-002` | Create amenity |
| API-AMN-003 | `PUT` | `/admin/amenities/{id}` | Admin | `BP-AMN-003` | Update amenity |
| API-AMN-004 | `DELETE` | `/admin/amenities/{id}` | Admin | `BP-AMN-004` | Delete amenity |
| API-AMN-005 | `POST` | `/admin/hotels/{hotelId}/amenities/{amenityId}` | Admin owner | `BP-AMN-005` | Assign amenity to hotel |
| API-AMN-006 | `DELETE` | `/admin/hotels/{hotelId}/amenities/{amenityId}` | Admin owner | `BP-AMN-006` | Remove amenity from hotel |
| API-AMN-007 | `POST` | `/admin/rooms/{roomId}/amenities/{amenityId}` | Admin owner | `BP-AMN-007` | Assign amenity to room |
| API-AMN-008 | `DELETE` | `/admin/rooms/{roomId}/amenities/{amenityId}` | Admin owner | `BP-AMN-008` | Remove amenity from room |

### 8.1 Amenity Request

```json
{
  "name": "Wifi miễn phí",
  "type": "HOTEL_SERVICE"
}
```

### 8.2 Amenity Errors

| Error Code | HTTP | Condition |
| --- | --- | --- |
| `DUPLICATE_AMENITY` | `409` | Amenity name already exists |
| `AMENITY_IN_USE` | `409` | Amenity is linked to hotel/room |
| `AUTH_FORBIDDEN` | `403` | Admin does not own hotel/room |
| `RESOURCE_NOT_FOUND` | `404` | Amenity/hotel/room not found |

## 9. DTO And List Response Catalog

All list endpoints must wrap these DTOs in the paginated success response from section `2.5`.

### 9.1 User List Item

```json
{
  "id": 1,
  "fullName": "Nguyen Van A",
  "email": "customer@example.com",
  "phone": "0900000000",
  "dob": "1999-01-01",
  "activate": true,
  "roles": ["CUSTOMER"],
  "createdAt": "2026-05-18T10:15:30Z"
}
```

### 9.2 Hotel List Item

```json
{
  "id": 2,
  "name": "Demo Hotel",
  "location": "Ho Chi Minh City",
  "starRating": 4,
  "isActive": true,
  "thumbnailUrl": "https://res.cloudinary.com/.../hotel.jpg",
  "minRoomPrice": 1200000
}
```

### 9.3 Room List Item

```json
{
  "id": 10,
  "hotelId": 2,
  "hotelName": "Demo Hotel",
  "name": "Deluxe Double",
  "type": "DOUBLE",
  "price": 1200000,
  "amount": 5,
  "capacity": 2,
  "thumbnailUrl": "https://res.cloudinary.com/.../room.jpg"
}
```

### 9.4 Amenity Response

```json
{
  "id": 4,
  "name": "Wifi miễn phí",
  "type": "HOTEL_SERVICE"
}
```

### 9.5 Mutating Admin Response

Create/update/lock/unlock/check-in/check-out/delete APIs should return the updated resource summary when available. Delete/deactivate APIs may return:

```json
{
  "message": "Operation completed"
}
```

## 10. Cross-Reference Matrix

| Business Process | API IDs |
| --- | --- |
| Register/login/account | API-AUTH-001 to API-AUTH-004, API-USER-001 to API-USER-006 |
| Hotel discovery | API-HOTEL-001 to API-HOTEL-003 |
| Room discovery/availability | API-ROOM-001 to API-ROOM-003 |
| Booking lifecycle | API-BOOK-001 to API-BOOK-005 |
| Admin hotel/room management | API-HOTEL-004 to API-HOTEL-007, API-ROOM-004 to API-ROOM-006 |
| Admin booking operations | API-BOOK-006 to API-BOOK-008 |
| Amenity management | API-AMN-001 to API-AMN-008 |

## 11. Non-MVP API Boundary From Thesis Gaps

These capabilities appear in thesis goals, limitations, or roadmap notes, but they do not have active MVP endpoints. Do not invent endpoints for them without updating PRD, use cases, business process, tech spec, schema, diagrams, and tests first.

| Capability | Current API status | Minimum contract work before implementation |
| --- | --- | --- |
| Admin create/update/delete user | Scope conflict / no active endpoint beyond list/lock/unlock | Resolve PRD `OQ-011`, then define create/update/delete or deactivate endpoints, validation, role assignment, audit, and delete/deactivate behavior. |
| Forgot password | No active API | Add request reset, verify token/OTP, set new password, expiry/rate-limit errors, and email/OTP delivery policy. |
| Real payment | No active API | Add payment intent/create, gateway callback/webhook, payment status lookup, refund, signature verification, and idempotency rules. |
| Revenue reporting | No active API | Add admin/partner report endpoints with date range, hotel filter, status filter, aggregation definition, pagination/export policy. |
| Recommendation/personalization | No active API | Add recommendation query endpoint, fallback response, ranking metadata, privacy constraints, and empty-state behavior. |
| Breadcrumb/navigation | Frontend/UI concern; no backend API expected by default | Add route metadata endpoint only if frontend cannot derive breadcrumbs statically. |
| Partner extranet/promotions/reviews/travel add-ons | No active API | Treat as new modules/domains after role, schema, permission, and lifecycle decisions are approved. |
