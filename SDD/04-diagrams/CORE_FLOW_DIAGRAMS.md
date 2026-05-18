# Core Flow Diagrams - Hotel Booking

Source documents:

- `SDD/01-product/PRD.md`
- `SDD/03-technical/TECH_SPEC.md`
- `SDD/02-business/BUSINESS_PROCESS.md`
- `SDD/02-business/business-processes/*.md`

## 1. Login And Register

```mermaid
flowchart TD
    Start([Guest opens auth screen])
    Choice{Choose action}

    Start --> Choice

    Choice -->|Register| RegisterForm[Enter fullName, email, phone, dob, password]
    RegisterForm --> RegisterAPI[POST /api/auth/register]
    RegisterAPI --> ValidateRegister{Required fields and formats valid?}
    ValidateRegister -->|No| RegisterValidationError[Return VALIDATION_ERROR]
    ValidateRegister -->|Yes| UniqueEmail{Email unique in user?}
    UniqueEmail -->|No| DuplicateEmail[Return DUPLICATE_EMAIL]
    UniqueEmail -->|Yes| HashPassword[Hash password with BCrypt]
    HashPassword --> AssignRole[Assign default role CUSTOMER]
    AssignRole --> SaveUser[(Save user and user_role)]
    SaveUser --> RegisterSuccess[Return created user summary]

    Choice -->|Login| LoginForm[Enter email and password]
    LoginForm --> LoginAPI[POST /api/auth/login]
    LoginAPI --> FindUser{User found by email?}
    FindUser -->|No| InvalidCredentials[Return AUTH_INVALID_CREDENTIALS]
    FindUser -->|Yes| ActiveCheck{Account activate is true?}
    ActiveCheck -->|No| Locked[Return AUTH_ACCOUNT_LOCKED]
    ActiveCheck -->|Yes| PasswordCheck{Password matches BCrypt hash?}
    PasswordCheck -->|No| InvalidCredentials
    PasswordCheck -->|Yes| LoadRoles[Load roles]
    LoadRoles --> IssueJWT[Issue JWT with userId and roles]
    IssueJWT --> LoginSuccess[Return token and user info]
    LoginSuccess --> RouteByRole{Role}
    RouteByRole -->|CUSTOMER| CustomerHome[Redirect to customer home]
    RouteByRole -->|ADMIN| AdminDashboard[Redirect to admin dashboard]
```

## 2. Search Availability

```mermaid
flowchart TD
    Start([Guest or Customer searches rooms])
    Input[Enter location, checkinDate, checkoutDate, adultAmount, childrenAmount, quantity]
    API[GET /api/rooms/available]
    ValidateDates{checkoutDate > checkinDate and checkinDate >= today?}
    FindHotels[Find active hotels by location]
    FindRooms[Find candidate rooms under matched hotels]
    FindBlockingBookings[Find BOOKED or CHECKED_IN bookings]
    Overlap{Date overlap exists?}
    Capacity{adultAmount + childrenAmount <= room.capacity?}
    Quantity{requested quantity + blocked quantity <= room.amount?}
    Include[Include room in available results]
    Exclude[Exclude room]
    Results{Any available rooms?}
    ShowResults[Display available rooms]
    EmptyState[Display empty state]
    DateError[Return VALIDATION_ERROR]

    Start --> Input --> API --> ValidateDates
    ValidateDates -->|No| DateError
    ValidateDates -->|Yes| FindHotels --> FindRooms --> FindBlockingBookings --> Overlap
    Overlap -->|Yes| Exclude
    Overlap -->|No| Capacity
    Capacity -->|No| Exclude
    Capacity -->|Yes| Quantity
    Quantity -->|No| Exclude
    Quantity -->|Yes| Include
    Include --> Results
    Exclude --> Results
    Results -->|Yes| ShowResults
    Results -->|No| EmptyState
```

## 3. Create Booking

```mermaid
sequenceDiagram
    autonumber
    actor Customer
    participant FE as React SPA
    participant API as Booking API
    participant Auth as JWT Filter
    participant Booking as BookingService
    participant Room as RoomService
    participant DB as MySQL

    Customer->>FE: Submit roomId, dates, quantity, guest counts, specialRequire
    FE->>API: POST /api/bookings with Authorization bearer token
    API->>Auth: Validate JWT
    alt Token invalid or missing
        Auth-->>API: 401
        API-->>FE: AUTH_INVALID_CREDENTIALS or unauthorized
        FE-->>Customer: Ask user to login again
    else Token valid
        Auth-->>API: Current user context
        API->>Booking: createBooking(request, currentUser)
        Booking->>Booking: Validate checkinDate and checkoutDate
        alt Invalid dates
            Booking-->>API: VALIDATION_ERROR
        else Dates valid
            Booking->>DB: Load room and hotel
            alt Room or hotel not found or inactive
                DB-->>Booking: Missing resource
                Booking-->>API: RESOURCE_NOT_FOUND
            else Room and hotel valid
                Booking->>Room: Check availability in transaction
                Room->>DB: Query overlapping BOOKED and CHECKED_IN bookings
                DB-->>Room: Blocking bookings and quantities
                alt Room unavailable
                    Room-->>Booking: ROOM_UNAVAILABLE or ROOM_QUANTITY_EXCEEDED
                    Booking-->>API: Conflict response
                else Available
                    Booking->>Booking: Calculate totalPrice = room.price * nights * quantity
                    Booking->>Booking: Generate unique bookingReference
                    Booking->>DB: Save booking with status BOOKED
                    Booking->>DB: Save booking_room mapping
                    DB-->>Booking: Created booking detail
                    Booking-->>API: Booking detail
                end
            end
        end
        API-->>FE: JSON response
        FE-->>Customer: Show success screen or error
    end
```

## 4. Cancel Booking

```mermaid
flowchart TD
    Start([Customer or Admin opens booking detail])
    Confirm[Show cancel confirmation and collect cancelReason]
    API[PATCH /api/bookings/{id}/cancel]
    Auth{JWT valid?}
    LoadBooking{Booking exists?}
    Permission{Actor is owner or ADMIN?}
    Status{Status can be cancelled?}
    SaveReason[Save cancel_reason]
    UpdateStatus[Set status to CANCELLED]
    ReturnUpdated[Return updated booking detail]
    Success[Show cancel success state]
    Unauthorized[Return unauthorized]
    NotFound[Return RESOURCE_NOT_FOUND]
    Forbidden[Return AUTH_FORBIDDEN]
    CannotCancel[Return BOOKING_CANNOT_CANCEL]

    Start --> Confirm --> API --> Auth
    Auth -->|No| Unauthorized
    Auth -->|Yes| LoadBooking
    LoadBooking -->|No| NotFound
    LoadBooking -->|Yes| Permission
    Permission -->|No| Forbidden
    Permission -->|Yes| Status
    Status -->|CHECKED_OUT or CANCELLED| CannotCancel
    Status -->|BOOKED| SaveReason --> UpdateStatus --> ReturnUpdated --> Success
    Status -->|CHECKED_IN| Policy{Policy allows cancel after check-in?}
    Policy -->|No or undefined| CannotCancel
    Policy -->|Admin exception| SaveReason
```

## 5. Admin Check-In And Check-Out

```mermaid
stateDiagram-v2
    [*] --> BOOKED: Create booking
    BOOKED --> CHECKED_IN: Admin check-in with roomNumber
    CHECKED_IN --> CHECKED_OUT: Admin check-out
    BOOKED --> CANCELLED: Owner/Admin cancel
    CHECKED_OUT --> [*]
    CANCELLED --> [*]

    BOOKED --> BOOKED: Reject check-in if roomNumber occupied
    CHECKED_IN --> CHECKED_IN: Reject check-out if booking not active
    CHECKED_OUT --> CHECKED_OUT: Reject cancel
    CANCELLED --> CANCELLED: Reject cancel or check-in
```

```mermaid
flowchart TD
    Start([Admin opens booking management])
    SelectAction{Operation}

    Start --> AdminAuth{Role ADMIN?}
    AdminAuth -->|No| Forbidden[Return AUTH_FORBIDDEN]
    AdminAuth -->|Yes| SelectAction

    SelectAction -->|Check-in| CheckInRequest[PATCH /api/admin/bookings/{id}/check-in with roomNumber]
    CheckInRequest --> LoadForCheckIn{Booking exists and status BOOKED?}
    LoadForCheckIn -->|No| StateError[Return RESOURCE_NOT_FOUND or state error]
    LoadForCheckIn -->|Yes| RoomNumberRequired{roomNumber provided?}
    RoomNumberRequired -->|No| ValidationError[Return VALIDATION_ERROR]
    RoomNumberRequired -->|Yes| Occupancy{roomNumber already assigned to active CHECKED_IN booking?}
    Occupancy -->|Yes| Occupied[Return ROOM_NUMBER_OCCUPIED]
    Occupancy -->|No| AssignRoom[Set booking.room_number]
    AssignRoom --> MarkCheckedIn[Set status CHECKED_IN]
    MarkCheckedIn --> ReturnCheckIn[Return updated booking]

    SelectAction -->|Check-out| CheckOutRequest[PATCH /api/admin/bookings/{id}/check-out]
    CheckOutRequest --> LoadForCheckOut{Booking exists and status CHECKED_IN?}
    LoadForCheckOut -->|No| StateError
    LoadForCheckOut -->|Yes| MarkCheckedOut[Set status CHECKED_OUT]
    MarkCheckedOut --> ReturnCheckOut[Return updated booking]
```

## 6. Admin Hotel And Room Management

```mermaid
flowchart TD
    Start([Admin opens hotel or room management])
    Auth{Role ADMIN?}
    Module{Manage Hotel or Room?}

    Start --> Auth
    Auth -->|No| Forbidden[Return AUTH_FORBIDDEN]
    Auth -->|Yes| Module

    Module -->|Create hotel| HotelInput[Enter hotel fields and images]
    HotelInput --> ValidateHotel{Required fields and image valid?}
    ValidateHotel -->|No| ValidationError[Return VALIDATION_ERROR]
    ValidateHotel -->|Yes| DuplicateHotel{Name + location unique?}
    DuplicateHotel -->|No| DuplicateHotelError[Return DUPLICATE_HOTEL]
    DuplicateHotel -->|Yes| UploadHotelImages[Upload images to Cloudinary]
    UploadHotelImages --> HotelUploadOk{Upload success?}
    HotelUploadOk -->|No| UploadFailed[Return IMAGE_UPLOAD_FAILED]
    HotelUploadOk -->|Yes| SaveHotel[(Save hotel with user_id = currentAdminId)]
    SaveHotel --> SaveHotelImages[(Save hotel image URLs)]
    SaveHotelImages --> HotelCreated[Return created hotel]

    Module -->|Update or delete hotel| LoadHotel{Hotel exists?}
    LoadHotel -->|No| NotFound[Return RESOURCE_NOT_FOUND]
    LoadHotel -->|Yes| OwnHotel{hotel.user_id == currentAdminId?}
    OwnHotel -->|No| Forbidden
    OwnHotel -->|Yes| HotelChange{Action}
    HotelChange -->|Update| UpdateHotel[Validate fields, upload optional images, save hotel]
    HotelChange -->|Delete| DeleteHotel[Soft delete or deactivate per policy]
    UpdateHotel --> HotelUpdated[Return updated hotel]
    DeleteHotel --> HotelDeleted[Return success]

    Module -->|Create room| RoomInput[Enter room fields, images, amenities]
    RoomInput --> LoadParentHotel{Parent hotel exists?}
    LoadParentHotel -->|No| NotFound
    LoadParentHotel -->|Yes| OwnParentHotel{Admin owns parent hotel?}
    OwnParentHotel -->|No| Forbidden
    OwnParentHotel -->|Yes| ValidateRoom{Type, price, amount, capacity valid?}
    ValidateRoom -->|No| ValidationError
    ValidateRoom -->|Yes| UploadRoomImages[Upload images to Cloudinary]
    UploadRoomImages --> RoomUploadOk{Upload success?}
    RoomUploadOk -->|No| UploadFailed
    RoomUploadOk -->|Yes| SaveRoom[(Save room with hotel_id)]
    SaveRoom --> SaveRoomImages[(Save room image URLs)]
    SaveRoomImages --> SaveRoomAmenities[(Save room_amenity mappings)]
    SaveRoomAmenities --> RoomCreated[Return created room]

    Module -->|Update or delete room| LoadRoom{Room exists?}
    LoadRoom -->|No| NotFound
    LoadRoom -->|Yes| OwnRoomHotel{Admin owns room hotel?}
    OwnRoomHotel -->|No| Forbidden
    OwnRoomHotel -->|Yes| RoomChange{Action}
    RoomChange -->|Update| UpdateRoom[Validate fields, upload optional images, update amenities]
    RoomChange -->|Delete| DeleteRoom[Soft delete or deactivate per policy]
    UpdateRoom --> RoomUpdated[Return updated room]
    DeleteRoom --> RoomDeleted[Return success]
```

## 7. Amenity Management

```mermaid
flowchart TD
    Start([Admin opens amenity management])
    Auth{Role ADMIN?}
    Action{Action}

    Start --> Auth
    Auth -->|No| Forbidden[Return AUTH_FORBIDDEN]
    Auth -->|Yes| Action

    Action -->|Create| CreateInput[Enter name, type, optional metadata]
    CreateInput --> ValidateCreate{Input valid and name unique?}
    ValidateCreate -->|No duplicate| SaveAmenity[(Save amenity)]
    ValidateCreate -->|Duplicate| Duplicate[Return DUPLICATE_AMENITY]
    ValidateCreate -->|Invalid| Validation[Return VALIDATION_ERROR]
    SaveAmenity --> Created[Return created amenity]

    Action -->|Update| LoadAmenity{Amenity exists?}
    LoadAmenity -->|No| NotFound[Return RESOURCE_NOT_FOUND]
    LoadAmenity -->|Yes| CheckDuplicate{Name unique after update?}
    CheckDuplicate -->|No| Duplicate
    CheckDuplicate -->|Yes| UpdateAmenity[(Save amenity changes)]
    UpdateAmenity --> Updated[Return updated amenity]

    Action -->|Delete| DeleteLoad{Amenity exists?}
    DeleteLoad -->|No| NotFound
    DeleteLoad -->|Yes| InUse{Mapped in hotel_amenity or room_amenity?}
    InUse -->|Yes| InUseError[Return AMENITY_IN_USE]
    InUse -->|No| DeleteAmenity[(Delete amenity)]
    DeleteAmenity --> Deleted[Return success]

    Action -->|Assign to hotel| AssignHotel[Receive hotelId and amenityId]
    AssignHotel --> HotelOwner{Hotel exists and admin owns it?}
    HotelOwner -->|No| Forbidden
    HotelOwner -->|Yes| HotelAmenityExists{Amenity exists and mapping is new?}
    HotelAmenityExists -->|No| Validation
    HotelAmenityExists -->|Yes| SaveHotelMapping[(Create hotel_amenity)]
    SaveHotelMapping --> AssignedHotel[Return success]

    Action -->|Remove from hotel| RemoveHotel[Receive hotelId and amenityId]
    RemoveHotel --> RemoveHotelOwner{Admin owns hotel?}
    RemoveHotelOwner -->|No| Forbidden
    RemoveHotelOwner -->|Yes| DeleteHotelMapping[(Delete hotel_amenity only)]
    DeleteHotelMapping --> RemovedHotel[Return success]

    Action -->|Assign to room| AssignRoom[Receive roomId and amenityId]
    AssignRoom --> RoomOwner{Room exists and admin owns hotel containing room?}
    RoomOwner -->|No| Forbidden
    RoomOwner -->|Yes| RoomAmenityExists{Amenity exists and mapping is new?}
    RoomAmenityExists -->|No| Validation
    RoomAmenityExists -->|Yes| SaveRoomMapping[(Create room_amenity)]
    SaveRoomMapping --> AssignedRoom[Return success]

    Action -->|Remove from room| RemoveRoom[Receive roomId and amenityId]
    RemoveRoom --> RemoveRoomOwner{Admin owns hotel containing room?}
    RemoveRoomOwner -->|No| Forbidden
    RemoveRoomOwner -->|Yes| DeleteRoomMapping[(Delete room_amenity only)]
    DeleteRoomMapping --> RemovedRoom[Return success]
```

## 8. Entity Relationship Overview

```mermaid
erDiagram
    ROLE {
        int id PK
        string name
    }

    USER {
        int id PK
        string email UK
        string password
        string full_name
        string phone
        date dob
        boolean activate
        datetime created_at
    }

    USER_ROLE {
        int user_id FK
        int role_id FK
    }

    HOTEL {
        int id PK
        string name
        string description
        string location
        string phone
        string email
        string contact_name
        string contact_phone
        int star_rating
        boolean is_active
        int user_id FK
    }

    ROOM {
        int id PK
        string name
        string type
        decimal price
        int amount
        int capacity
        string description
        int hotel_id FK
    }

    IMAGE {
        int id PK
        string path
        int hotel_id FK
        int room_id FK
    }

    BOOKING {
        int id PK
        string booking_reference UK
        string customer_name
        decimal total_price
        string status
        date checkin_date
        date checkout_date
        int adult_amount
        int children_amount
        datetime created_at
        string cancel_reason
        decimal refund
        string room_number
        string special_require
        int user_id FK
    }

    BOOKING_ROOM {
        int id PK
        int booking_id FK
        int room_id FK
        int quantity
    }

    AMENITY {
        int id PK
        string name UK
        string type
    }

    HOTEL_AMENITY {
        int hotel_id FK
        int amenity_id FK
    }

    ROOM_AMENITY {
        int room_id FK
        int amenity_id FK
    }

    USER ||--o{ USER_ROLE : has
    ROLE ||--o{ USER_ROLE : grants
    USER ||--o{ HOTEL : owns
    USER ||--o{ BOOKING : creates
    HOTEL ||--o{ ROOM : contains
    HOTEL ||--o{ IMAGE : has
    ROOM ||--o{ IMAGE : has
    BOOKING ||--o{ BOOKING_ROOM : includes
    ROOM ||--o{ BOOKING_ROOM : booked_as
    HOTEL ||--o{ HOTEL_AMENITY : has
    AMENITY ||--o{ HOTEL_AMENITY : assigned_to_hotel
    ROOM ||--o{ ROOM_AMENITY : has
    AMENITY ||--o{ ROOM_AMENITY : assigned_to_room
```

## 9. Cross-Cutting Rules Represented

- Protected APIs require a valid JWT.
- Admin-only APIs require role `ADMIN`.
- Hotel, room, and amenity assignment changes require owner checks.
- Availability is blocked only by bookings in `BOOKED` or `CHECKED_IN`.
- Date overlap formula: `existing_checkin < new_checkout AND existing_checkout > new_checkin`.
- Booking creation, cancellation, check-in, check-out, and amenity delete checks should run in transaction boundaries.
- Hotel and room image files are uploaded to Cloudinary or equivalent storage; MySQL stores only URLs.
