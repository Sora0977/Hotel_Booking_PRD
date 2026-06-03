
### Complete Business Logic of the Hotel Booking Service

**1. Account & Security (The Onboarding Experience)**

**As a Customer:** When you sign up, you provide your name, email, phone number, and date of birth. The system registers you with a standard CUSTOMER role. You can update your profile information later, but your email address becomes permanently locked to your account and cannot be changed. If you need to change your password, the system enforces a rule that your new password cannot be identical to your current one. If you decide to leave the platform, you have the right to completely delete your own account.

**As an Administrator:** You have elevated privileges. You can view the entire directory of users on the platform. If a user is acting suspiciously, you can click a button to lock their account, which updates their database status to inactive and prevents future logins.

> ⚠️ **Current Code Limitation (Session Invalidation):** The system does _not_ instantly invalidate active sessions. Because JWT tokens are validated purely by signature and expiration (set to 6 months), a locked user with an existing active token can continue to bypass the security filter and make API requests until their token naturally expires.

**2. Hotel & Property Management (The Admin Dashboard)**

**As an Administrator:**

You can list new properties on the platform. To prevent duplicates, the system runs a check to ensure no other hotel exists with the exact same name in the exact same location. When you upload photos for your new hotel, the system automatically designates the very first image you upload as the public "Cover Image." You are strictly isolated to your own business; you can only edit, update, or delete hotels that you personally created.

**3. Rooms & Amenities Configuration (Setting up the Offerings)**

**As an Administrator:**

You define what you are selling by creating Room Types (Single, Double, Suite, Triple) for your hotels. The system forces you to define two distinct numbers:

- **Capacity:** How many human beings can sleep in this room type.
    
- **Amount (Inventory):** How many identical physical rooms of this type exist in the building.
    

You can also browse a global list of Amenities (e.g., "Free Wi-Fi", "Ocean View"). You can attach these globally managed amenities to your entire hotel or to specific rooms. The system fiercely protects this data: if an amenity is currently assigned to your room, the system will block any overarching Admin from deleting that amenity from the global database.

**4. Search & Discovery (The Customer's Search)**

**As a Customer:**

You land on the homepage and search for a place to stay. You input a city, your check-in/check-out dates, how many people are in your group, and how many rooms you need.

> ⚠️ **Current Code Limitation (Availability Algorithm):** While the system attempts to calculate real-time availability, the current SQL query entirely excludes a Room Type if there is even a _single_ overlapping booking. If a hotel has 10 physical Single rooms and 1 is booked, the algorithm hides the remaining 9 rooms from the search results, prematurely making the hotel appear sold out of that tier.

**5. The Booking Engine (Making the Reservation)**

**As a Customer:**

When you click "Book," the system enforces strict time rules: you cannot book a check-in date in the past, your check-out date cannot be before your check-in date, and you must stay at least one night.

At the exact millisecond you confirm the booking, the system recalculates inventory to prevent double-booking. The formula is strict: (Current overlapping bookings for that room) + (The number of rooms you want) MUST BE <= (Total physical rooms available). If the hotel has 5 rooms, 3 are booked, and you try to book 3 more, the system blocks you and warns that only 2 are left.

If successful, the system calculates your total bill by multiplying the room's nightly base price by your number of nights. You receive a unique 10-character alphanumeric booking code, and your reservation is marked as BOOKED.

> ⚠️ **Current Code Limitation (Price Calculation):** The billing engine currently omits the requested room quantity (`roomQuantity`) from its final calculation. If a customer books 3 rooms for 2 nights, the system will only charge them the price of 1 room for 2 nights.

**Cancellations:**

If your plans change, you can cancel your reservation and provide a reason (if you leave it blank, the system automatically notes "Cancelled by user (No reason provided)"). However, the system removes your cancel button if your stay is already completed (CHECKED_OUT) or previously cancelled.

**6. Front Desk Operations (The Check-In/Check-Out Flow)**

**As an Administrator:**

When the customer arrives at your hotel lobby, you look up their reservation and change the status from BOOKED to CHECKED_IN. At this moment, you assign them a physical room key/number (e.g., "Room 205"). The system actively watches your back here: if you try to hand the customer the keys to "Room 205", but another guest's booking in the system is currently CHECKED_IN to "Room 205", the system throws a hard collision error and forces you to choose an empty room. When the guest's stay is over, you change their status to CHECKED_OUT.

**7. Verified Reviews & Ratings (The Post-Stay Experience)**

**As a Customer:**

You want to leave a glowing 5-star review. The system blocks spam by checking your booking history. You are only allowed to submit a rating and written review if the system verifies you have a booking at that exact hotel that has officially reached the CHECKED_OUT status. Once posted, your rating automatically updates the hotel's overall average score. You can delete your own review at any time.

**As an Administrator:**

You cannot write fake reviews for your own hotel. However, as a platform administrator, if a customer leaves a review containing inappropriate language, you have the supreme authority to delete any review across the entire platform.

**8. Revenue & Financial Tracking (The Business Analytics)**

**As an Administrator:**

You need to see how much money your properties are generating. You open your revenue dashboard. The financial engine has strict accounting rules: it exclusively counts revenue from bookings that are fully CHECKED_OUT. Money from upcoming or currently active stays is not recognized yet. You can generate reports by year/month or by a custom date range. Finally, the system automatically calculates a hardcoded 10% platform commission fee out of the gross revenue, showing you exactly what your hotel earned versus what is owed to the platform software providers.