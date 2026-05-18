# Technical Specification - Hotel Booking

## 1. Metadata

| Field | Value |
| --- | --- |
| Document type | Tech Spec |
| Product | Hotel Booking |
| Depends on | `SDD/01-product/PRD.md` |
| Status | Draft |
| Primary roles | Customer, Admin |
| Scope | Web app, REST API, relational database, image storage |

## 2. Tech Stack

| Layer | Technology | Status | Notes |
| --- | --- | --- | --- |
| Frontend | React.js | Documented | Component-based SPA UI |
| Frontend routing | React Router | Documented | Client-side route management |
| Frontend styling | Tailwind CSS | Documented | Utility-first styling |
| API client | Axios | Documented | Attach auth token to protected API requests |
| Backend language | Java | Documented | Backend service implementation |
| Backend framework | Spring Boot | Documented | REST API, DI, embedded server |
| Backend security | JWT, BCrypt | Documented | JWT for API auth, BCrypt for password hashing |
| Backend security framework | Spring Security | Implementation convention | Mentioned as Spring ecosystem; use for RBAC/JWT filter |
| Persistence | Spring Data JPA/Hibernate | Implementation convention | Recommended Spring Boot pattern for MySQL |
| Database | MySQL | Documented | Relational data store |
| Cloud/storage | Cloudinary | Documented | Hotel/room image upload and URL storage |
| Transport security | HTTPS/SSL-TLS | Required for production | Not completed in current implementation notes |

## 3. System Architecture

### 3.1 Architecture Style

- Type: Modular monolith web application.
- Client: React SPA.
- Server: Spring Boot REST API.
- Database: MySQL relational database.
- External storage: Cloudinary for image assets.
- Auth model: JWT bearer token, role-based authorization.

### 3.2 High-Level Components

| Component ID | Component | Responsibility |
| --- | --- | --- |
| CMP-FE-001 | React SPA | Render screens, manage routes, collect user input, call backend APIs |
| CMP-FE-002 | Axios API Client | Centralized HTTP client, attach `Authorization: Bearer <token>` |
| CMP-BE-001 | Auth Module | Register, login, password hashing, JWT issuance, current user context |
| CMP-BE-002 | User Module | Profile, user list, lock/unlock user |
| CMP-BE-003 | Hotel Module | CRUD hotels, owner checks, hotel amenities, hotel images |
| CMP-BE-004 | Room Module | CRUD rooms, availability search, room amenities, room images |
| CMP-BE-005 | Booking Module | Create booking, lookup, cancel, check-in, check-out, room number assignment |
| CMP-BE-006 | Amenity Module | Amenity catalog CRUD, assign/remove links |
| CMP-BE-007 | Image Storage Module | Upload image file to Cloudinary, persist returned URL |
| CMP-DB-001 | MySQL Database | Store users, hotels, rooms, bookings, amenities, image URLs |

### 3.3 Request Path

| Step | Flow |
| --- | --- |
| 1 | User interacts with React screen. |
| 2 | React validates basic form inputs. |
| 3 | Axios sends REST request to Spring Boot API. |
| 4 | JWT filter validates token for protected endpoints. |
| 5 | Controller delegates to service layer. |
| 6 | Service applies business rules and permission checks. |
| 7 | Repository reads/writes MySQL data. |
| 8 | Image upload flows call Cloudinary before persisting image URL. |
| 9 | API returns JSON response. |
| 10 | React updates UI state and navigation. |

### 3.4 Module Boundaries

| Module | Owns Entities | Calls |
| --- | --- | --- |
| Auth | `user`, `role`, `user_role` | User repository, JWT provider, password encoder |
| User | `user`, `role`, `user_role` | Auth context |
| Hotel | `hotel`, `hotel_amenity`, `image` | Auth context, Cloudinary, Amenity |
| Room | `room`, `room_amenity`, `image` | Hotel owner check, Cloudinary, Amenity |
| Booking | `booking`, `booking_room` | Room availability, User context |
| Amenity | `amenity`, `hotel_amenity`, `room_amenity` | Hotel/Room owner checks for assignment removal |

## 4. Authentication And Authorization

### 4.1 Roles

| Role | Capabilities |
| --- | --- |
| `CUSTOMER` | Search/view hotels and rooms, create booking, view own booking history, cancel own booking, manage profile |
| `ADMIN` | Manage users, hotels, rooms, amenities, all bookings, booking operations |

### 4.2 JWT Claims

| Claim    | Type     | Required | Notes                                                         |
| -------- | -------- | -------- | ------------------------------------------------------------- |
| `sub`    | string   | Yes      | User email or user ID                                         |
| `userId` | number   | Yes      | Current user ID                                               |
| `roles`  | string[] | Yes      | `CUSTOMER`, `ADMIN`                                           |
| `iat`    | number   | Yes      | Issued-at timestamp                                           |
| `exp`    | number   | Yes      | Expiration; source document states token validity is 6 months |

### 4.3 Protected Endpoint Rules

| Endpoint Group | Access |
| --- | --- |
| `/api/auth/register` | Public |
| `/api/auth/login` | Public |
| Hotel/room search and detail APIs | Public |
| Booking create/history/cancel | Authenticated Customer/Admin |
| User management APIs | Admin only |
| Hotel/room management APIs | Admin only plus owner check |
| Amenity management APIs | Admin only |
| Booking operations APIs | Admin only |

## 5. API Surface

### 5.1 Auth APIs

| Method | Path | Access | Request | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/api/auth/register` | Public | `fullName`, `email`, `phone`, `dob`, `password` | Created user summary |
| `POST` | `/api/auth/login` | Public | `email`, `password` | `token`, `user` |
| `POST` | `/api/auth/logout` | Authenticated | None | Success message |
| `PUT` | `/api/auth/password` | Authenticated | `oldPassword`, `newPassword`, `confirmPassword` | Success message |

### 5.2 User APIs

| Method | Path | Access | Request | Response |
| --- | --- | --- | --- | --- |
| `GET` | `/api/users/me` | Authenticated | None | Current user profile |
| `PUT` | `/api/users/me` | Authenticated | Profile fields | Updated profile |
| `DELETE` | `/api/users/me` | Authenticated | Confirmation | Success message |
| `GET` | `/api/admin/users` | Admin | Query params | User list |
| `PATCH` | `/api/admin/users/{id}/lock` | Admin | None | Updated user status |
| `PATCH` | `/api/admin/users/{id}/unlock` | Admin | None | Updated user status |

### 5.3 Hotel APIs

| Method | Path | Access | Request | Response |
| --- | --- | --- | --- | --- |
| `GET` | `/api/hotels` | Public | `location`, `checkinDate`, `checkoutDate`, pagination | Hotel list |
| `GET` | `/api/hotels/{id}` | Public | None | Hotel detail |
| `GET` | `/api/hotels/{id}/rooms` | Public | Optional date filters | Room list |
| `GET` | `/api/admin/hotels` | Admin | None | Admin-owned hotels |
| `POST` | `/api/admin/hotels` | Admin | Hotel fields, images | Created hotel |
| `PUT` | `/api/admin/hotels/{id}` | Admin owner | Hotel fields, optional images | Updated hotel |
| `DELETE` | `/api/admin/hotels/{id}` | Admin owner | Confirmation | Success message |

### 5.4 Room APIs

| Method | Path | Access | Request | Response |
| --- | --- | --- | --- | --- |
| `GET` | `/api/rooms` | Public | `keyword`, `type`, `checkinDate`, `checkoutDate`, `capacity`, pagination | Room list |
| `GET` | `/api/rooms/{id}` | Public | None | Room detail |
| `GET` | `/api/rooms/available` | Public | `location`, `checkinDate`, `checkoutDate`, `adultAmount`, `childrenAmount`, `quantity` | Available rooms |
| `POST` | `/api/admin/hotels/{hotelId}/rooms` | Admin owner | Room fields, images, amenities | Created room |
| `PUT` | `/api/admin/rooms/{id}` | Admin owner | Room fields, optional images/amenities | Updated room |
| `DELETE` | `/api/admin/rooms/{id}` | Admin owner | Confirmation | Success message |

### 5.5 Booking APIs

| Method | Path | Access | Request | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/api/bookings` | Authenticated | `roomId`, dates, quantity, guest counts, special request | Created booking |
| `GET` | `/api/bookings/me` | Authenticated | Pagination/status filters | Current user's bookings |
| `GET` | `/api/bookings/reference/{reference}` | Authenticated | Reference code | Booking detail |
| `GET` | `/api/bookings/{id}` | Owner or Admin | None | Booking detail |
| `PATCH` | `/api/bookings/{id}/cancel` | Owner or Admin | `cancelReason` | Cancelled booking |
| `GET` | `/api/admin/bookings` | Admin | Pagination/status/search filters | Booking list |
| `PATCH` | `/api/admin/bookings/{id}/check-in` | Admin | `roomNumber` | Updated booking |
| `PATCH` | `/api/admin/bookings/{id}/check-out` | Admin | None | Updated booking |

### 5.6 Amenity APIs

| Method | Path | Access | Request | Response |
| --- | --- | --- | --- | --- |
| `GET` | `/api/amenities` | Public | `type` | Amenity list |
| `POST` | `/api/admin/amenities` | Admin | `name`, `type`, optional metadata | Created amenity |
| `PUT` | `/api/admin/amenities/{id}` | Admin | Amenity fields | Updated amenity |
| `DELETE` | `/api/admin/amenities/{id}` | Admin | Confirmation | Success message |
| `POST` | `/api/admin/hotels/{hotelId}/amenities/{amenityId}` | Admin owner | None | Link created |
| `DELETE` | `/api/admin/hotels/{hotelId}/amenities/{amenityId}` | Admin owner | None | Link removed |
| `POST` | `/api/admin/rooms/{roomId}/amenities/{amenityId}` | Admin owner | None | Link created |
| `DELETE` | `/api/admin/rooms/{roomId}/amenities/{amenityId}` | Admin owner | None | Link removed |

## 6. Database Schema

### 6.1 Entity Summary

| Entity | Table | Purpose |
| --- | --- | --- |
| Role | `role` | User roles such as `ADMIN`, `CUSTOMER` |
| User | `user` | Account, profile, login credentials |
| UserRole | `user_role` | Many-to-many user-role mapping |
| Hotel | `hotel` | Hotel profile owned by an Admin |
| Room | `room` | Room inventory under a hotel |
| Image | `image` | Stored image URLs for hotel or room |
| Booking | `booking` | Booking header and status |
| BookingRoom | `booking_room` | Booking-room mapping |
| Amenity | `amenity` | Amenity catalog |
| HotelAmenity | `hotel_amenity` | Hotel-amenity mapping |
| RoomAmenity | `room_amenity` | Room-amenity mapping |

### 6.2 Tables

| Table | Primary Key | Required Columns | Nullable/Optional Columns |
| --- | --- | --- | --- |
| `role` | `id INT` | `name VARCHAR(255)` | None |
| `user` | `id INT` | `activate BIT(1)`, `dob DATE`, `email VARCHAR(255)`, `full_name VARCHAR(255)`, `password VARCHAR(255)`, `phone VARCHAR(20)` | `created_at DATETIME(6)` |
| `user_role` | `role_id INT`, `user_id INT` | `role_id FK`, `user_id FK` | None |
| `hotel` | `id INT` | `name`, `description`, `location`, `phone`, `email`, `contact_name`, `contact_phone`, `star_rating`, `is_active`, `user_id FK` | None |
| `room` | `id INT` | `name`, `type ENUM('SINGLE','DOUBLE','TRIPLE','SUIT')`, `price DECIMAL(10,2)`, `amount INT`, `capacity INT`, `description`, `is_active BIT(1)`, `hotel_id FK` | None |
| `image` | `id INT` | `path VARCHAR(1024)` | `hotel_id FK`, `room_id FK` |
| `booking` | `id INT` | `booking_reference VARCHAR(10)`, `customer_name`, `total_price DECIMAL(10,2)`, `status`, `checkin_date`, `checkout_date`, `adult_amount`, `children_amount`, `created_at`, `user_id FK` | `cancel_reason`, `refund DECIMAL(10,2)`, `room_number`, `special_require` |
| `booking_room` | `id INT` | `booking_id FK`, `room_id FK`, `quantity INT` | None |
| `amenity` | `id INT` | `name VARCHAR(255)`, `type ENUM('HOTEL_SERVICE','ROOM_FEATURE')` | None |
| `hotel_amenity` | `amenity_id INT`, `hotel_id INT` | `amenity_id FK`, `hotel_id FK` | None |
| `room_amenity` | `amenity_id INT`, `room_id INT` | `amenity_id FK`, `room_id FK` | None |

### 6.3 Relationships

| Relationship | Cardinality | Notes |
| --- | --- | --- |
| `user` -> `user_role` -> `role` | Many-to-many | One user can have multiple roles |
| `user` -> `hotel` | One-to-many | User/Admin owns hotels |
| `user` -> `booking` | One-to-many | Customer creates bookings |
| `hotel` -> `room` | One-to-many | Hotel contains room types/inventory |
| `hotel` -> `image` | One-to-many | Hotel images |
| `room` -> `image` | One-to-many | Room images |
| `booking` -> `booking_room` -> `room` | Many-to-many via mapping | Booking can reference room(s) |
| `hotel` -> `hotel_amenity` -> `amenity` | Many-to-many | Hotel-level amenities |
| `room` -> `room_amenity` -> `amenity` | Many-to-many | Room-level amenities |

### 6.4 Recommended Indexes

| Table | Index | Reason |
| --- | --- | --- |
| `user` | Unique index on `email` | Login lookup, duplicate prevention |
| `hotel` | Index on `location` | Hotel search |
| `hotel` | Composite index on `name`, `location` | Duplicate hotel check |
| `hotel` | Index on `user_id` | Admin-owned hotel lookup |
| `room` | Index on `hotel_id` | List rooms by hotel |
| `room` | Index on `type` | Room type filtering |
| `booking` | Unique index on `booking_reference` | Booking lookup |
| `booking` | Index on `user_id` | Customer booking history |
| `booking` | Composite index on `status`, `checkin_date`, `checkout_date` | Availability conflict checks |
| `booking_room` | Composite index on `room_id`, `booking_id` | Availability join |
| `hotel_amenity` | Composite unique index on `hotel_id`, `amenity_id` | Prevent duplicate links |
| `room_amenity` | Composite unique index on `room_id`, `amenity_id` | Prevent duplicate links |

## 7. Domain Enums

### 7.1 Room Type

| Enum | Description |
| --- | --- |
| `SINGLE` | Single room |
| `DOUBLE` | Double room |
| `TRIPLE` | Triple room |
| `SUIT` | Suite room; spelling preserved from source schema |

### 7.2 Booking Status

| Enum | Description |
| --- | --- |
| `BOOKED` | Booking created and active |
| `CHECKED_IN` | Guest has checked in |
| `CHECKED_OUT` | Guest has checked out |
| `CANCELLED` | Booking cancelled |

### 7.3 Amenity Type

| Enum/Value | Description |
| --- | --- |
| `HOTEL_SERVICE` | Hotel-level amenity/service |
| `ROOM_FEATURE` | Room-level amenity/feature |

## 8. Core Flow Specifications

### 8.1 Login Flow

| Step | Actor/Component | Action |
| --- | --- | --- |
| 1 | User | Enters `email`, `password` on login form. |
| 2 | Frontend | Sends `POST /api/auth/login`. |
| 3 | AuthService | Looks up user by email. |
| 4 | AuthService | If user not found, returns authentication error. |
| 5 | AuthService | Compares raw password with stored BCrypt hash. |
| 6 | AuthService | If password invalid, returns authentication error. |
| 7 | AuthService | Checks `activate`/active status. |
| 8 | AuthService | If inactive/locked, returns account locked error. |
| 9 | AuthService | Generates JWT containing user identity and roles. |
| 10 | API | Returns `token` and user info. |
| 11 | Frontend | Stores token and redirects by role: Customer home or Admin dashboard. |

### 8.2 Register Flow

| Step | Actor/Component | Action |
| --- | --- | --- |
| 1 | Guest | Enters full name, email, phone, DOB, password. |
| 2 | Frontend | Sends `POST /api/auth/register`. |
| 3 | AuthService | Validates required fields and formats. |
| 4 | AuthService | Checks email uniqueness. |
| 5 | AuthService | Hashes password with BCrypt. |
| 6 | AuthService | Assigns default role `CUSTOMER`. |
| 7 | AuthService | Saves active user record to MySQL. |
| 8 | API | Returns success response. |

### 8.3 Search Available Rooms Flow

| Step | Actor/Component | Action |
| --- | --- | --- |
| 1 | Guest/Customer | Inputs `location`, `checkinDate`, `checkoutDate`, guest count, quantity. |
| 2 | Frontend | Calls available-room search API. |
| 3 | RoomService | Validates dates: `checkoutDate > checkinDate >= today`. |
| 4 | RoomService | Finds hotels by location. |
| 5 | RoomService | Finds rooms under matched hotels. |
| 6 | RoomService | Excludes rooms with booking status `BOOKED` or `CHECKED_IN` where date ranges overlap. |
| 7 | RoomService | Applies capacity and amount checks. |
| 8 | API | Returns available rooms. |
| 9 | Frontend | Displays results or empty state. |

### 8.4 Create Booking Flow

| Step | Actor/Component | Action |
| --- | --- | --- |
| 1 | Customer | Selects room, check-in/check-out, quantity, adult/children amount, special request. |
| 2 | Frontend | Sends `POST /api/bookings` with JWT. |
| 3 | BookingService | Validates authenticated user. |
| 4 | BookingService | Validates booking dates. |
| 5 | BookingService | Loads room and related hotel. |
| 6 | BookingService | Checks room availability by overlapping bookings. |
| 7 | BookingService | Checks requested quantity does not exceed remaining amount. |
| 8 | BookingService | Calculates total price: `room.price * nights * quantity`. |
| 9 | BookingService | Generates unique booking reference code. |
| 10 | BookingService | Saves booking with status `BOOKED`. |
| 11 | BookingService | Saves `booking_room` mapping. |
| 12 | API | Returns booking detail. |
| 13 | Frontend | Shows booking success screen. |

### 8.5 Cancel Booking Flow

| Step | Actor/Component | Action |
| --- | --- | --- |
| 1 | Customer/Admin | Opens booking detail and requests cancel. |
| 2 | Frontend | Shows confirmation dialog and optional/required cancel reason. |
| 3 | Frontend | Sends cancel request. |
| 4 | BookingService | Loads booking by ID/reference. |
| 5 | BookingService | Checks actor is booking owner or Admin. |
| 6 | BookingService | Rejects if status is `CHECKED_OUT` or `CANCELLED`. |
| 7 | BookingService | Saves `cancel_reason`. |
| 8 | BookingService | Updates status to `CANCELLED`. |
| 9 | API | Returns updated booking detail. |
| 10 | Frontend | Shows cancel success state. |

### 8.6 Admin Add Hotel Flow

| Step | Actor/Component | Action |
| --- | --- | --- |
| 1 | Admin | Enters hotel data and selects images. |
| 2 | Frontend | Sends create hotel request with JWT. |
| 3 | HotelService | Validates Admin role. |
| 4 | HotelService | Checks duplicate hotel by name and location. |
| 5 | HotelService | Uploads image(s) to Cloudinary. |
| 6 | Cloudinary | Returns image URL(s). |
| 7 | HotelService | Saves hotel with `user_id = currentAdminId`. |
| 8 | HotelService | Saves image URL records. |
| 9 | API | Returns created hotel. |

### 8.7 Admin Add Room Flow

| Step | Actor/Component | Action |
| --- | --- | --- |
| 1 | Admin | Opens owned hotel and enters room data, amenities, images. |
| 2 | Frontend | Sends create room request. |
| 3 | RoomService | Validates Admin role. |
| 4 | RoomService | Checks hotel exists. |
| 5 | RoomService | Checks current Admin owns the hotel. |
| 6 | RoomService | Uploads image(s) to Cloudinary. |
| 7 | Cloudinary | Returns image URL(s). |
| 8 | RoomService | Saves room with `hotel_id`. |
| 9 | RoomService | Saves image URL records. |
| 10 | RoomService | Saves room-amenity links. |
| 11 | API | Returns created room. |

### 8.8 Admin Update Booking Status Flow

| Step | Actor/Component | Action |
| --- | --- | --- |
| 1 | Admin | Opens booking management screen. |
| 2 | Frontend | Sends check-in or check-out request. |
| 3 | BookingService | Validates Admin role. |
| 4 | BookingService | Loads booking by ID. |
| 5 | BookingService | For check-in, requires `roomNumber`. |
| 6 | BookingService | Checks `roomNumber` is not assigned to another active `CHECKED_IN` booking. |
| 7 | BookingService | Updates `room_number` and status to `CHECKED_IN`. |
| 8 | BookingService | For check-out, updates status to `CHECKED_OUT`. |
| 9 | API | Returns updated booking detail. |

### 8.9 Admin Amenity Management Flow

| Flow | Steps |
| --- | --- |
| Create amenity | Validate Admin -> validate name uniqueness -> save amenity -> return created amenity |
| Update amenity | Validate Admin -> find amenity -> check duplicate name -> save updates |
| Delete amenity | Validate Admin -> find amenity -> check no `hotel_amenity`/`room_amenity` links -> delete |
| Remove from hotel | Validate Admin -> check hotel owner -> delete `hotel_amenity` link only |
| Remove from room | Validate Admin -> check room's hotel owner -> delete `room_amenity` link only |

## 9. Validation Rules

| Area | Rule |
| --- | --- |
| Email | Required, valid email format, unique in `user` |
| Password | Required, stored only as hash |
| DOB | Required in source schema |
| Hotel | Required name, description, location, phone, email, contact fields, star rating |
| Hotel duplicate | Same name and location should be blocked |
| Hotel image | At least one image required for create flow |
| Room | Required name, type, price, amount, capacity, description, hotel ID |
| Room type | Must be one of `SINGLE`, `DOUBLE`, `TRIPLE`, `SUIT` |
| Room price | Must be non-negative |
| Room amount | Must be positive integer |
| Booking dates | `checkoutDate > checkinDate >= today` |
| Booking quantity | Requested quantity must be positive and not exceed remaining room amount |
| Cancel booking | Actor must be owner or Admin; blocked for `CHECKED_OUT` and `CANCELLED` |
| Amenity | Required name and type; name should be unique |
| Image upload | File must be valid image type and within configured size limit |

## 10. Error Handling

| Error Code | Trigger | HTTP Status |
| --- | --- | --- |
| `AUTH_INVALID_CREDENTIALS` | Email not found or password mismatch | `401` |
| `AUTH_ACCOUNT_LOCKED` | User inactive/locked | `403` |
| `AUTH_FORBIDDEN` | Role or ownership check failed | `403` |
| `VALIDATION_ERROR` | Invalid request fields | `400` |
| `RESOURCE_NOT_FOUND` | Entity ID/reference not found | `404` |
| `DUPLICATE_EMAIL` | Email already exists | `409` |
| `DUPLICATE_HOTEL` | Hotel name/location already exists | `409` |
| `DUPLICATE_AMENITY` | Amenity name already exists | `409` |
| `ROOM_UNAVAILABLE` | Room has overlapping booking | `409` |
| `ROOM_QUANTITY_EXCEEDED` | Requested quantity exceeds remaining room count | `409` |
| `BOOKING_CANNOT_CANCEL` | Booking already checked out or cancelled | `409` |
| `ROOM_NUMBER_OCCUPIED` | Room number already assigned to active stay | `409` |
| `AMENITY_IN_USE` | Amenity linked to hotel/room | `409` |
| `IMAGE_UPLOAD_FAILED` | Cloudinary/storage provider upload failure | `502` |

## 11. Non-Functional Technical Requirements

| NFR ID | Requirement | Implementation Notes |
| --- | --- | --- |
| NFR-TECH-001 | Search response `<= 3s` | Index `hotel.location`, booking date/status fields |
| NFR-TECH-002 | Main page/detail load `<= 2s` | Pagination, image optimization, avoid over-fetching |
| NFR-TECH-003 | Password security | BCrypt hashing, never log raw passwords |
| NFR-TECH-004 | API security | JWT filter, RBAC, owner checks in service layer |
| NFR-TECH-005 | Transport security | HTTPS in production |
| NFR-TECH-006 | Data integrity | DB constraints and service-level transaction boundaries |
| NFR-TECH-007 | Image storage | Store Cloudinary URL only, not binary image in MySQL |
| NFR-TECH-008 | Maintainability | Keep controller-service-repository separation |

## 12. Transaction Boundaries

| Operation | Transaction Requirement |
| --- | --- |
| Register | Save user and user-role mapping atomically |
| Create hotel | Save hotel and images atomically after successful Cloudinary upload |
| Create room | Save room, images, and amenity links atomically after successful Cloudinary upload |
| Create booking | Availability check and booking insert must run in one transaction to reduce overbooking risk |
| Cancel booking | Status update and cancel reason save atomically |
| Check-in | Room number occupancy check and status update atomically |
| Delete amenity | In-use check and delete atomically |

## 13. Concurrency Notes

| Risk | Mitigation |
| --- | --- |
| Two users book the last available room simultaneously | Use DB transaction, row-level lock or optimistic locking on room/booking availability check |
| Admin assigns same room number to two active stays | Check active `CHECKED_IN` booking by `room_number` inside transaction |
| Amenity deleted while another admin assigns it | Check existence and in-use status inside transaction |
| Hotel/room edited while another admin deletes it | Use existence checks and return `RESOURCE_NOT_FOUND` if stale |

## 14. Source References

| Source ID | Path | Used For |
| --- | --- | --- |
| SRC-001 | `SDD/01-product/PRD.md` | Product requirements, business rules, scope |
| SRC-002 | `Hotel booking service/Thesis-report/chapters/chuong-1-gioi-thieu.md` | High-level stack, NFR targets |
| SRC-003 | `Hotel booking service/Thesis-report/chapters/chuong-2-phuong-phap-thuc-hien.md` | Tech stack, auth flow, hotel/room flow, booking flow |
| SRC-004 | `Hotel booking service/Thesis-report/chapters/chuong-3-thiet-ke.md` | Database schema, use cases, sequence/activity flows |
| SRC-005 | `Hotel booking service/Thesis-report/chapters/chuong-4-ket-luan.md` | Known limitations and pending production gaps |
| SRC-006 | `graphify-out/wiki/index.md` | Knowledge graph navigation |
