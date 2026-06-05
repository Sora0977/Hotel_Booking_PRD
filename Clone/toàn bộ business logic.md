# Toàn bộ business logic - hotel-booking-web

Tài liệu này tổng hợp business logic đọc từ source `Clone/hotel-booking-web`, gồm backend NestJS, Prisma schema, frontend Next.js, validators, API wrappers và các luồng nghiệp vụ chính.

Nguồn chính đã đối chiếu:

- `apps/api/prisma/schema.prisma`
- `apps/api/src/main.ts`, `apps/api/src/app.module.ts`
- `apps/api/src/modules/**/{controller,service,dto,guard,strategy}.ts`
- `apps/web/src/app/**/page.tsx`
- `apps/web/src/features/**/{api,queries,mutations,validator,types}.ts`
- `apps/web/src/providers/*`, `apps/web/src/lib/axios.ts`, `apps/web/src/proxy.ts`
- `actions.sql`

## 1. Tổng quan kiến trúc

Dự án là monorepo Turborepo gồm:

- `apps/api`: NestJS API, global prefix `api/v1`, Prisma/PostgreSQL, JWT, Google OAuth, VNPAY, Cloudinary, mailer.
- `apps/web`: Next.js App Router, React Query, React Hook Form, Zod, shadcn/ui, axios client.
- `actions.sql`: seed/upsert `ApiAction` cho hệ thống action permission.

Backend khởi tạo ở `main.ts`:

- Dùng `cookieParser`.
- Dùng `PrismaExceptionFilter`.
- Dùng global `ValidationPipe({ whitelist: true })`.
- CORS `origin: true`, `credentials: true`.
- Global prefix `api/v1`.
- Khi `NODE_ENV !== production`, tự listen port `PORT ?? 3000`.

`AppModule` import các module nghiệp vụ: auth, users, roles, permissions, actions, cloudinary, hotel, room type, amenity, room, inventory, booking, payment, commission, reviews, news, dashboard, banner, contact, policy, notification, promotion.

Global guard hiện chỉ có `ThrottlerGuard` với TTL 60s, limit 10. Các guard auth/permission như `JwtAuthGuard`, `ActionGuard`, `RolesGuard`, `PermissionsGuard` chỉ chạy khi controller/route gắn trực tiếp.

## 2. Domain model trong Prisma

### 2.1 User/Auth/RBAC

`User`

- Email unique.
- `emailVerified` mặc định `false`.
- `passwordHash` optional để hỗ trợ local hoặc OAuth.
- `provider` mặc định `LOCAL`, `providerId` unique optional cho Google.
- Có avatar qua `avatarId -> ImageAsset`.
- Quan hệ với roles, sessions, email verify tokens, password reset tokens.
- Là owner hotel, hotel member, người tạo gallery/news/banner, người review, người gửi contact, người nhận notification, người lưu trú/check-in.

`AuthSession`

- Lưu `jti` unique, `refreshHash`, provider, userAgent, ip, expiresAt.
- Có `revokedAt`, `revokedBy`, `reason` để quản lý phiên.

`EmailVerifyToken`, `PasswordResetToken`

- Lưu `tokenHash`, `expiresAt`, `usedAt`.
- Token thô không lưu trong DB.

`Role`, `Permission`, `UserRole`, `RolePermission`

- Role name unique.
- Permission name unique.
- `UserRole` khóa chính kép `[userId, roleId]`.
- `RolePermission` khóa chính kép `[roleId, permissionId]`.

`ApiAction`, `ApiActionPolicy`

- `ApiAction.key` unique, ví dụ `hotels.create`, `bookings.cancel`.
- `enabled` mặc định true.
- `mode`: `ANY` hoặc `ALL`.
- `ApiActionPolicy` nối action với permission, khóa chính kép `[actionId, permissionId]`.

### 2.2 Hotel/Room/Inventory

`Hotel`

- Thuộc owner `User`.
- Có status `DRAFT | ACTIVE | SUSPENDED | ARCHIVED`.
- Có room types, rooms, members, images, bookings, reviews, policies, promotions, inventories, notifications.
- Có optional `commissionPackageId`.
- Soft delete bằng `deletedAt`.

`HotelMember`

- Bảng nối user-hotel, khóa chính kép `[hotelId, userId]`.
- Schema có enum `HotelMemberRole`, nhưng model `HotelMember` hiện không có field role.

`RoomType`

- Thuộc hotel.
- Có `name`, `price_per_night Decimal(12,2)`, `max_guests`, `description`.
- Có rooms, amenities, images, booking items, inventories.
- Unique `[hotelId, name]`.
- Soft delete bằng `deletedAt`.

`Amenity`, `RoomTypeAmenity`

- Amenity có `key` unique, `label`, `sortOrder`, `isActive`.
- Room type nối với amenity qua khóa chính kép `[typeId, amenityId]`.

`Room`

- Phòng vật lý thuộc hotel và room type.
- Có `code`, `floor`, `note`.
- `status`: `ACTIVE | INACTIVE | MAINTENANCE`.
- `cleanStatus`: `CLEAN | DIRTY | INSPECT`.
- Unique `[hotelId, code]`.
- Soft delete bằng `deletedAt`.

`Inventory`

- Tồn phòng theo ngày, hotel, room type.
- `date` là date-only.
- `totalRooms`, `availableRooms`, `stopSell`.
- Unique `[roomTypeId, hotelId, date]`.
- Soft delete bằng `deletedAt`.

### 2.3 Booking/Payment/Check-in/Review

`Booking`

- Thuộc hotel, optional user.
- `status`: `PENDING | CONFIRMED | CANCELLED | CHECKED_IN | COMPLETED | NO_SHOW`.
- Có `checkIn`, `checkOut`, thông tin khách đại diện, `totalAmount`, `discountAmount`, `promotionId`.
- Lưu snapshot hoa hồng: `commissionRateSnapshot`, `commissionAmount`.
- Có items, payments, review, guests, check-in record.

`BookingItem`

- Dòng đặt phòng theo room type.
- Lưu `quantity`, `unitPrice`, `lineTotal`.

`Payment`

- Provider hiện chỉ có `VNPAY`.
- `status`: `INIT | PENDING | SUCCEEDED | FAILED | CANCELED | REFUND_PENDING | REFUNDED`.
- `merchantTxnRef` unique.
- Lưu các field đối soát VNPAY: transaction no, bank code, pay date, response code, transaction status.

`PaymentEvent`

- Audit log theo payment.
- `type`: ví dụ `RETURN`, `IPN`, `MAIL_PAYMENT_SUCCEEDED`.
- `payload` dạng JSON.

`CheckIn`

- 1-1 với booking qua `bookingId @unique`.
- Lưu `checkedInAt`, `checkedInBy`, `note`.

`BookingGuest`

- Danh sách khách lưu trú khi check-in.
- Có optional `userId`, họ tên, email, phone, dateOfBirth, gender, idNumber, nationality.

`Review`

- Thuộc hotel, user, booking.
- `bookingId` unique nên một booking chỉ review một lần.
- Có `rating`, `title`, `content`, `isHidden`, `deletedAt`.
- Ảnh qua `ReviewImage`.

### 2.4 Marketing/CMS/Support

`Promotion`

- `code` unique.
- `discountType`: `PERCENT | FIXED`.
- `discountValue`, `maxDiscountAmount`, `minBookingAmount`.
- `totalUsageLimit`, `usedCount`, `perUserLimit`.
- `startAt`, `endAt`, `isActive`.
- Optional `hotelId`.

`CommissionPackage`

- `code` unique.
- `commissionRate` là số từ 0 đến 1.
- `isActive`.
- Gắn cho nhiều hotel.

`HotelPolicy`

- Mỗi hotel có policy theo `PolicyType`.
- Unique `[hotelId, type]`.
- `enabled`, `order`.

`News`

- `slug` unique.
- `status`: `DRAFT | PUBLISHED | ARCHIVED`.
- `publishedAt`, `createdById`.
- Soft delete bằng `deletedAt`.

`Banner`

- `position`, `isActive`, `startAt`, `endAt`.
- `linkType`: `URL | HOTEL | NEWS`.
- Có images.

`ContactMessage`

- Public contact message.
- `status`: `NEW | IN_PROGRESS | RESOLVED | SPAM`.
- Có metadata ip/userAgent, optional handledBy, note.

`Notification`

- Gửi cho user.
- Optional hotel/booking.
- `type`: `NEW_BOOKING`, `BOOKING_CANCELLED`, `BOOKING_CONFIRMED`, `CHECK_IN`, `CHECK_OUT`, `PAYMENT_SUCCESS`, `PAYMENT_FAILED`, `SYSTEM`.
- `isRead`, `readAt`.

### 2.5 Image/Gallery

`ImageAsset`

- Dùng cho avatar user.
- `publicId` unique để xóa trên Cloudinary.

`ImageGallery`, `FolderGallery`

- Gallery theo user/folder.
- `FolderGallery.folderName` unique.
- Ảnh gallery được dùng khi tạo news/review.

`HotelImage`, `RoomTypeImage`, `NewsImage`, `BannerImage`, `ReviewImage`

- Lưu URL ảnh theo domain tương ứng.

### 2.6 Lưu ý schema/migration

`schema.prisma` hiện giàu hơn migrations. Migration `reset` và `add_payment` không bao phủ đầy đủ các model mới như `Review`, `News`, `Banner`, `ContactMessage`, `CommissionPackage`, `HotelPolicy`, `Notification`, `Promotion`, `CheckIn`, `BookingGuest`. Khi triển khai DB mới cần tạo migration cập nhật từ schema hiện tại.

## 3. Cross-cutting business logic

### 3.1 Xác thực JWT và session

Backend cấp access token và refresh token:

- Access token ký bằng `JWT_SECRET`.
- Refresh token ký bằng `JWT_REFRESH_SECRET ?? JWT_SECRET`.
- Refresh token lưu trong cookie `refresh_token`, HTTP-only, secure, sameSite lax.
- Refresh token được hash bằng argon2 trong `AuthSession.refreshHash`.
- Mỗi cặp token có `jti`.

Refresh rotation:

- Verify refresh JWT.
- Yêu cầu payload `type === 'refresh'`.
- Tìm session theo `jti`.
- Nếu session revoked hoặc không tồn tại: reject.
- Verify hash refresh token.
- Nếu hash mismatch: revoke toàn bộ session user vì nghi token reuse.
- Revoke session cũ và issue token mới.

Frontend:

- Lưu access token trong cookie `accessToken`.
- Axios request interceptor gắn `Authorization: Bearer <accessToken>`.
- Response 401 tự gọi `/auth/refresh`; nếu refresh fail thì xóa token và redirect login.
- Response 403 toast lỗi quyền và redirect `/forbidden`.

### 3.2 Public route và protected route

Backend:

- `@Public()` chỉ bypass `JwtAuthGuard` và `ActionGuard` khi các guard đó được gắn.
- Không có global JWT guard.

Frontend:

- `proxy.ts` chỉ chặn `/admin` và `/me` nếu thiếu `accessToken`.
- Nếu đã login mà vào `/login`, redirect `/me`.

### 3.3 RBAC và action permission

Cơ chế phân quyền đầy đủ:

1. User có nhiều role.
2. Role có nhiều permission.
3. ApiAction có nhiều required permission.
4. Action có `mode`:
   - `ANY`: user cần ít nhất một permission.
   - `ALL`: user cần đủ toàn bộ permission.
5. Route gắn `@Action('...')` và `ActionGuard` sẽ check quyền.

`ActionGuard`:

- Bypass nếu route `@Public`.
- Nếu route không public mà không có user: 401.
- Nếu route không có `@Action`: 403 `Action is not configured`.
- Nếu action không tồn tại hoặc disabled: 403 `No policy bound...`.
- Lấy user permissions từ role.
- Có Redis cache nếu cấu hình `REDIS_URL` hoặc `REDIS_HOST`, TTL 60s.

Frontend:

- `/users/me` trả thêm `allowedActions`.
- `PermissionProvider` chuyển `allowedActions` thành `Set`.
- Sidebar admin lọc menu theo action key.
- Component `Can` ẩn/hiện UI theo action.
- Đây là guard hiển thị UI; quyền thật vẫn do backend trả 403.

Lưu ý thực tế:

- Một số controller có `@Action` nhưng không gắn `ActionGuard`, nên metadata chưa enforce.
- `UsersController`, `RolesController`, `PermissionsController`, `ActionsController` có một số `@Action`, nhưng guard hiện tại không luôn chạy action-level.
- `PermissionsGuard` chỉ enforce khi có `@Permissions(...)`; nhiều controller không gắn metadata này.

### 3.4 Hotel-scoped access

Nhiều service tự check owner/member:

- Hotel owner có quyền.
- Hotel member trong `HotelMember` có quyền.
- Một số thao tác cho phép role `ADMIN`.

Guard liên quan:

- `HotelMemberGuard`: pass nếu user là member hoặc owner.
- `HotelMemberWithAdminGuard`: pass nếu role `ADMIN`, hoặc member/owner.
- `HotelContextGuard`/`HotelRoleGuard` tồn tại nhưng không phải luồng chính trong controller hotel hiện tại.

### 3.5 Soft delete

Soft delete dùng `deletedAt` ở:

- Hotel
- RoomType
- Room
- Inventory
- Review
- News

Các list/detail chính thường filter `deletedAt: null`. Riêng `Policy.remove` hard delete.

### 3.6 Upload và ảnh

Cloudinary:

- Upload thường vào folder `stayra` hoặc folder người dùng chọn.
- Avatar upload vào `stayra/avatars/{userId}`.
- Avatar cũ bị destroy trên Cloudinary và xóa `ImageAsset`.
- Gallery ảnh lưu `ImageGallery` theo user/folder.
- News/review chỉ dùng ảnh gallery thuộc user hiện tại.

### 3.7 Mail và notification

Mail service gửi:

- Verify email.
- Password reset.
- Payment success.
- Contact notification cho support/admin.

Notification service:

- Tạo notification nội bộ.
- User list notification của chính mình.
- Đếm unread.
- Mark one/all as read.
- Delete notification của chính mình.

Luồng tự tạo notification:

- Booking mới tạo `NEW_BOOKING` cho owner và hotel members.
- Contact mới tạo `SYSTEM` cho user có role `ADMIN`, `OWNER`, `STAFF`.

## 4. Backend business logic theo module

### 4.1 Auth

Endpoints chính:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/verify-email`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `POST /api/v1/auth/logout-all`
- `POST /api/v1/auth/forgot-password`
- `POST /api/v1/auth/reset-password`
- `GET /api/v1/auth/google`
- `GET /api/v1/auth/google/callback`
- `GET /api/v1/auth/sessions`
- `POST /api/v1/auth/resend`

Register:

- Email lower/trim.
- Tạo local user qua `UsersService.createLocalUser`.
- Password hash argon2id.
- Tạo email verify token raw 32 bytes, lưu hash SHA-256.
- Token verify TTL 30 phút.
- Gửi verify URL về frontend `PUBLIC_WEB_URL/auth/verify-email?token=...`.
- User mới chưa verify email nên chưa login được.

Verify email:

- Hash token raw.
- Check token tồn tại, chưa used, chưa expired.
- Transaction:
  - Set `user.emailVerified = true`.
  - Set `EmailVerifyToken.usedAt`.

Login local:

- Tìm user theo email.
- Bắt buộc có `passwordHash`.
- Verify argon2.
- Bắt buộc `emailVerified = true`.
- Issue access/refresh token.
- Set cookie `refresh_token`.
- Trả `{ accessToken, jti, tokenType: 'Bearer' }`.

Refresh:

- Đọc cookie `refresh_token`.
- Rotate refresh token theo session.
- Set cookie refresh mới.
- Trả access token mới.

Logout:

- Clear cookie refresh.
- Code revoke session hiện tại đang bị comment, nên logout thường không revoke DB session.

Logout all:

- Gọi `revokeAllUserSessions`.
- Clear cookie.
- Lưu ý: controller dùng `req.user.sub`, trong khi JWT strategy trả `id`; có nguy cơ không revoke đúng user.

Forgot/reset password:

- Forgot password không báo lỗi nếu email không tồn tại để tránh user enumeration.
- Xóa reset token chưa dùng trước đó của user.
- Tạo token reset 64 hex chars, lưu SHA-256 hash, TTL 30 phút.
- Reset password check token tồn tại/chưa dùng/chưa hết hạn.
- Hash password mới.
- Mark token used.
- Xóa toàn bộ `AuthSession` của user.

Google OAuth:

- Strategy lấy profile Google.
- Nếu email đã tồn tại nhưng provider/providerId không khớp:
  - Nếu account local: reject và yêu cầu login password/link Google sau.
  - Nếu provider khác: reject.
- Upsert user theo `providerId`.
- Set provider `GOOGLE`, `emailVerified = true`.
- Tạo auth session provider Google.
- Redirect frontend `/auth/callback#access_token=...`.

Lưu ý:

- Google strategy map `firstName = familyName`, `lastName = givenName`, có vẻ đảo.
- `resendVerificationEmail` gửi token trực tiếp cho `sendVerifyEmail` thay vì build URL đầy đủ như register.

### 4.2 Users

Endpoints chính:

- `POST /api/v1/users/me/change-password`
- `GET /api/v1/users/me`
- `PATCH /api/v1/users/me`
- `GET /api/v1/users/:id`
- `GET /api/v1/users`
- `POST /api/v1/users/me/avatar`
- `DELETE /api/v1/users/me/avatar`

Logic:

- `createLocalUser`: email unique, password hash argon2id.
- `changePassword`:
  - Check `newPassword === confirmPassword`.
  - User phải có password local.
  - Verify current password.
  - Update hash mới.
  - Xóa toàn bộ auth sessions.
- `me`:
  - Trả public user select gồm roles/avatar.
  - Tính thêm `allowedActions` từ RBAC/action policy.
- `getAllowedActions`:
  - Gom permission từ roles.
  - Lấy enabled `ApiAction`.
  - Check policy theo `ANY/ALL`.
  - Trả danh sách action key sorted.
- `getPublicProfile`:
  - Nếu requester không phải chính mình và không có role admin/manager, xóa email khỏi response.
- `listUsers`:
  - Filter q theo email/firstName/lastName.
  - Filter role, emailVerified.
  - Pagination limit/offset.
  - Sort theo query.

Lưu ý:

- Frontend có wrapper `PUT /users/:id` và `DELETE /users/:id`, nhưng backend users controller đã đọc không thấy endpoint update/delete user tương ứng.
- `ListUsersQuery.sortBy` cho phép `fullName`, nhưng Prisma model không có field `fullName`.
- `ChangePasswordDto` có custom match có thể đang trỏ sai field, service vẫn tự check lại.

### 4.3 Roles, Permissions, Actions

Roles:

- CRUD role.
- Role name unique.
- `setRolePermissions` là replace-all:
  - Trim id.
  - Cấm rỗng.
  - Cấm duplicate.
  - Check permission tồn tại.
  - Xóa toàn bộ role permissions cũ.
  - CreateMany permission mới.
- `setUserRoles` cũng replace-all roles của user.

Permissions:

- CRUD permission.
- List hỗ trợ search, limit clamp tối đa 200, sort sanitize.
- Remove xóa `RolePermission` trước rồi xóa permission.

Actions:

- Upsert `ApiAction` theo key.
- List action kèm policies/permission.
- Find action theo key.
- `setActionPermissions` replace-all policy permissions của action.
- `actions.sql` seed nhiều action nghiệp vụ: amenities, bookings, commission packages, hotels, inventories, news, reviews, rooms, room types.

### 4.4 Hotel

Endpoints chính:

- `GET /api/v1/hotels/public`
- `POST /api/v1/hotels`
- `GET /api/v1/hotels/me`
- `PATCH /api/v1/hotels/:hotelId`
- `POST /api/v1/hotels/:hotelId/members`
- `DELETE /api/v1/hotels/:hotelId/members/:userId`
- `GET /api/v1/hotels/:hotelId`
- `GET /api/v1/hotels/:hotelId/members`
- `DELETE /api/v1/hotels/:hotelId`
- `GET /api/v1/hotels`

Create hotel:

- Set `ownerId = currentUser`.
- Tạo luôn `HotelMember` cho owner.
- Nếu có images thì tạo `HotelImage`.
- Include owner/members/images trong response.

Get my hotels:

- Hotel chưa soft-delete.
- User là owner hoặc member.
- Sort `createdAt desc`.

Update hotel:

- Chỉ update hotel chưa deleted.
- Nếu payload có `images`, diff theo id:
  - Image id hiện có: update URL.
  - Image mới: create.
  - Image DB không còn trong payload: delete.

Member management:

- Add member:
  - Hotel phải tồn tại và chưa deleted.
  - Tất cả userIds phải tồn tại.
  - Upsert `HotelMember` để tránh duplicate.
- Remove member: delete theo composite key `[hotelId, userId]`.

Delete hotel:

- Soft delete bằng `deletedAt`.
- Chỉ owner hoặc role `ADMIN`.

Admin/member hotel list:

- Nếu user là `ADMIN`, thấy tất cả.
- Nếu không phải admin, chỉ thấy hotel mình là member.
- Mặc định loại deleted, trừ khi `includeDeleted`.
- Filter ownerId/city/name/q.
- Include images, owner, commission package, member count.

Public hotel list:

- Chỉ hotel `deletedAt = null`.
- Chỉ `status = ACTIVE`.
- Phải có ít nhất một room type chưa deleted.
- Filter q/city.
- Filter minPrice/maxPrice theo room type price.
- Filter date bằng inventory có available > 0, stopSell false, deletedAt null.
- Sort price asc/desc bằng cách lấy tất cả hotel match, tính min price trong memory, sort rồi paginate.

Lưu ý:

- Date availability ở public hotel list chỉ yêu cầu có inventory record available trong các ngày, chưa đảm bảo đủ mọi ngày như booking service.

### 4.5 Amenity

Endpoints:

- `POST /api/v1/amenities`
- `GET /api/v1/amenities`
- `GET /api/v1/amenities/:id`
- `PATCH /api/v1/amenities/:id`
- `DELETE /api/v1/amenities/:id`

Logic:

- Create trim `key`, `label`.
- `key` unique, lỗi Prisma P2002 thành BadRequest.
- List filter q theo key/label, filter `isActive`, order `sortOrder desc`, `createdAt desc`.
- Update trim field nếu có.
- Delete thực tế là disable: set `isActive = false`.

### 4.6 Room type

Endpoints:

- `GET /api/v1/room-types`
- `POST /api/v1/hotels/:hotelId/room-types`
- `GET /api/v1/hotels/:hotelId/room-types`
- `GET /api/v1/hotels/:hotelId/room-types/available`
- `GET /api/v1/hotels/:hotelId/room-types/:id`
- `PATCH /api/v1/hotels/:hotelId/room-types/:id`
- `DELETE /api/v1/hotels/:hotelId/room-types/:id`

Access:

- Owner hoặc hotel member mới được quản trị.
- Endpoint `available` public.
- Endpoint `room-types` public list all.

Create:

- Check hotel access.
- Amenity ids phải tồn tại và active.
- Name trim và unique trong hotel, case-insensitive, chỉ xét room type chưa deleted.
- Giá chuyển sang `Prisma.Decimal`.
- Tạo room type, images, amenity mappings trong transaction.

List:

- Filter q theo name/description.
- Pagination.
- Include amenities/images.

Available:

- Nhận `from`, `to`.
- Lấy room types chưa deleted.
- Lấy inventories trong khoảng `date >= from`, `date <= to`.
- Nếu có `stopSell`: available = 0.
- Nếu thiếu inventory record cho đủ số ngày: available = 0.
- Nếu đủ: availableRooms = min availableRooms trong khoảng.

Update:

- Check access và tồn tại.
- Nếu đổi name, check unique.
- Diff images tương tự hotel.
- Diff amenities: create mới và delete removed.

Remove:

- Soft delete bằng `deletedAt`.

Lưu ý:

- Availability dùng khoảng ngày inclusive `[from, to]`; booking service dùng checkout exclusive `[checkIn, checkOut)`. Có nguy cơ lệch một ngày.

### 4.7 Room

Endpoints:

- `POST /api/v1/hotels/:hotelId/rooms`
- `GET /api/v1/hotels/:hotelId/rooms`
- `GET /api/v1/hotels/:hotelId/rooms/:id`
- `PATCH /api/v1/hotels/:hotelId/rooms/:id`
- `DELETE /api/v1/hotels/:hotelId/rooms/:id`

Logic:

- User phải là owner/member của hotel chưa deleted.
- RoomType khi tạo phải thuộc hotel.
- `code` unique trong hotel với room chưa deleted.
- List filter roomTypeId, search code/note/floor.
- Update check duplicate code nếu đổi code.
- Delete là soft delete:
  - Set `deletedAt`.
  - Set `status = INACTIVE`.

Lưu ý:

- Booking không trừ theo `Room.status`; booking trừ theo `Inventory`.

### 4.8 Inventory

Endpoints:

- `GET /api/v1/hotels/:hotelId/inventories`
- `POST /api/v1/hotels/:hotelId/inventories/bulk`
- `PATCH /api/v1/hotels/:hotelId/inventories/:id`
- `DELETE /api/v1/hotels/:hotelId/inventories/:id`

Access:

- Owner/member.

List:

- Required `from`, `to`.
- Parse date-only UTC.
- `from <= to`.
- Filter hotelId, date range, optional roomTypeId.
- Mặc định ẩn `stopSell`, trừ khi `includeStopped`.
- Include roomType name.
- Return `{ from, to, items }`.

Bulk set:

- Check access.
- Check `from <= to`.
- RoomType phải thuộc hotel.
- Tạo danh sách ngày inclusive `[from, to]`.
- Upsert theo composite unique `[roomTypeId, hotelId, date]`.
- Create/update `totalRooms`, `availableRooms`, `stopSell`.
- Nếu record từng soft-delete, update set `deletedAt: null`.

Update one:

- Check tồn tại và chưa deleted.
- Update partial `totalRooms`, `availableRooms`, `stopSell`.

Soft delete:

- Set `deletedAt`.

Lưu ý:

- Backend không enforce `availableRooms <= totalRooms`; frontend validator có rule này.

### 4.9 Booking

Endpoints:

- `GET /api/v1/bookings/me`
- `GET /api/v1/bookings/me/:id`
- `POST /api/v1/hotels/:hotelId/bookings`
- `GET /api/v1/hotels/:hotelId/bookings`
- `GET /api/v1/hotels/:hotelId/bookings/:id`
- `PATCH /api/v1/hotels/:hotelId/bookings/:id/cancel`
- `PATCH /api/v1/hotels/:hotelId/bookings/:id/status`
- `POST /api/v1/bookings/:id/check-in`
- `GET /api/v1/bookings/:id/check-in`

Create booking:

1. Parse `checkIn`, `checkOut` bằng date-only UTC.
2. Bắt buộc `checkIn < checkOut`.
3. Số đêm là từng ngày trong khoảng `[checkIn, checkOut)`.
4. Mỗi `roomTypeId` trong items phải thuộc hotel.
5. Load giá `price_per_night`.
6. Load hotel commission package active nếu có.
7. Validate `commissionRate` trong khoảng 0..1.
8. Trong transaction:
   - Với từng item/từng đêm:
     - Inventory phải tồn tại.
     - Không `stopSell`.
     - `availableRooms >= quantity`.
   - Trừ tồn bằng `updateMany` với điều kiện `availableRooms >= quantity` để chống race.
   - Tính `lineTotal = unitPrice * quantity * nightsCount`.
   - Tính `totalAmount`.
   - Nếu có promotion code, validate và tính discount.
   - Tính `finalTotal = totalAmount - discountAmount`.
   - Tăng `promotion.usedCount`.
   - Tính `commissionAmount = finalTotal * commissionRate`, làm tròn 0 chữ số.
   - Tạo booking status `PENDING`, items, discount, promotionId, commission snapshot.
9. Sau transaction, gửi notification `NEW_BOOKING` cho owner và members.

Promotion trong booking:

- Code phải tồn tại.
- Promotion active.
- `now` nằm trong `startAt/endAt`.
- Nếu promotion có hotelId, phải đúng hotel.
- `totalUsageLimit`: `usedCount < totalUsageLimit`.
- `perUserLimit`: user phải login; đếm booking của user dùng promotion này và status không CANCELLED.
- `minBookingAmount`: total trước giảm phải đủ.
- `PERCENT`: discount = total * percent, áp `maxDiscountAmount` nếu có.
- `FIXED`: discount = số tiền cố định.
- Discount không vượt total.

Cancel booking:

- Tìm booking theo id/hotelId, include items.
- Nếu đã `CANCELLED`, trả booking.
- Với từng item/từng đêm, cộng lại `availableRooms`.
- Update status `CANCELLED`.

List hotel bookings:

- Filter status, from/to theo checkIn, search q theo guestName/guestEmail.
- Pagination.
- Include items.

My bookings:

- Filter theo userId và optional status.
- Include hotel info, items/roomType, payments summary.

Booking detail:

- Hotel detail include items/roomType và payments.
- My detail include hotel, items/roomType, payments.

Status transition:

- Terminal states: `CANCELLED`, `NO_SHOW`, `COMPLETED`.
- Allowed:
  - `PENDING -> CONFIRMED | CANCELLED`
  - `CONFIRMED -> CANCELLED | CHECKED_IN | NO_SHOW`
  - `CHECKED_IN -> COMPLETED`
- Nếu status không đổi, trả booking hiện tại.
- Update status yêu cầu hotel access.

Cron auto-cancel:

- Chạy mỗi phút.
- PENDING quá 15 phút (`PENDING_TTL_MINUTES = 15`).
- Không có payment `SUCCEEDED`.
- Lấy tối đa 100 booking mỗi lần.
- Transaction:
  - Update status sang CANCELLED nếu vẫn PENDING.
  - Trả tồn từng item/từng đêm.
- Log số booking auto-cancel.

Check-in:

- Actor phải là owner/member của hotel chứa booking.
- Không cho check-in booking `CANCELLED`.
- Không cho check-in booking `COMPLETED`.
- Normalize guests:
  - Primary + companions.
  - Deduplicate theo `userId`, nếu không có thì theo `fullName|idNumber|email`.
- Transaction:
  - Upsert `CheckIn`.
  - Delete toàn bộ `BookingGuest` cũ.
  - CreateMany guests mới.
  - Update booking status `CHECKED_IN`.
- `getCheckIn` trả `{ checkIn, guests }`.

Lưu ý:

- Booking giữ tồn ngay khi `PENDING`, chưa chờ thanh toán.
- Nếu cron không chạy, tồn có thể bị giữ lâu.
- Hủy booking trả tồn, nhưng không thấy decrement `Promotion.usedCount`.
- Promotion `usedCount` tăng khi tạo booking, không chờ thanh toán thành công.

### 4.10 Payment VNPAY

Endpoints:

- `POST /api/v1/bookings/:bookingId/payments/vnpay`
- `GET /api/v1/payments/vnpay/return`
- `GET /api/v1/payments/vnpay/ipn`

Create VNPAY URL:

- Tìm booking theo id.
- Chỉ cho thanh toán nếu booking status `PENDING`.
- Lấy config `VNPAY_TMN_CODE`, `VNPAY_HASH_SECRET`, `VNPAY_URL`, `VNPAY_RETURN_URL`.
- Tạo `merchantTxnRef = BK_${booking.id}_${Date.now()}`.
- Tạo payment:
  - provider `VNPAY`
  - status `INIT`
  - amount = booking.totalAmount
  - secureHashAlg `sha512`
- Build params VNPAY:
  - version `2.1.0`
  - command `pay`
  - currCode `VND`
  - amount = totalAmount * 100
  - locale default `vn`
  - optional bankCode
- Sort params, ký HMAC SHA512.
- Trả `paymentUrl`.
- Update payment status `PENDING`.

VNPAY return:

- Verify secure hash.
- Tìm payment theo `vnp_TxnRef`.
- Log `PaymentEvent` type `RETURN`.
- Nếu chữ ký sai: không update.
- Nếu payment không còn `INIT/PENDING`: coi là idempotent, không ghi đè.
- Nếu `vnp_ResponseCode === '00'`:
  - Update payment `SUCCEEDED` và lưu audit fields.
  - Update booking `CONFIRMED`.
  - Gửi mail success một lần.
- Nếu response khác `00`:
  - Update payment `FAILED`.
- Return data cho controller redirect frontend `/payment-result?payment_status=success|failed&booking_id=...`.

VNPAY IPN:

- Verify checksum, sai trả `RspCode 97`.
- Không tìm thấy payment trả `01`.
- Check amount: `vnp_Amount / 100` phải bằng payment.amount, sai trả `04`.
- Nếu payment đã xử lý, trả `02`.
- Log `PaymentEvent` type `IPN`.
- Nếu response `00`:
  - Payment `SUCCEEDED`.
  - Booking `CONFIRMED`.
- Nếu fail:
  - Payment `FAILED`.
- Xử lý hợp lệ trả `RspCode 00`.

Mail success:

- Check đã có event `MAIL_PAYMENT_SUCCEEDED` chưa.
- Load payment + booking.
- Email ưu tiên `booking.guestEmail`, fallback user.email.
- Gửi mail.
- Tạo event success/fail để tránh gửi lặp.

Lưu ý:

- `createVnpayPaymentUrl` nhận `userId` nhưng không check booking thuộc user đó.
- Return idempotent branch có thể trả thiếu `bookingId` nếu IPN đã xử lý trước.

### 4.11 Review

Endpoints:

- `GET /api/v1/hotels/:hotelId/reviews`
- `GET /api/v1/hotels/:hotelId/reviews/moderation`
- `POST /api/v1/hotels/:hotelId/reviews`
- `GET /api/v1/users/me/reviews`
- `PATCH /api/v1/reviews/:id`
- `PATCH /api/v1/hotels/:hotelId/reviews/:id/moderate`
- `DELETE /api/v1/hotels/:hotelId/reviews/:id`

Create review:

- Booking phải tồn tại, thuộc hotel, thuộc user.
- Booking status phải `COMPLETED`.
- `bookingId` unique ngăn review lặp.
- Nếu có `imageIds`:
  - Ảnh phải thuộc gallery của user.
  - Lưu `secureUrl || url` vào `ReviewImage`.
- Tạo review trong transaction.

Public list:

- Chỉ `deletedAt = null`.
- Chỉ `isHidden = false`.
- Search title/content.
- Include user/avatar/images.

Moderation:

- Owner/member hotel.
- List không lấy deleted, nhưng thấy hidden.
- Moderate update `isHidden`.
- Delete là soft delete `deletedAt`.

User:

- List review của chính mình.
- Update review của chính mình nếu chưa deleted.

### 4.12 Promotion

Endpoints:

- `POST /api/v1/promotions`
- `GET /api/v1/promotions`
- `GET /api/v1/promotions/public`
- `GET /api/v1/promotions/:id`
- `PATCH /api/v1/promotions/:id`
- `DELETE /api/v1/promotions/:id`

Create:

- Check code unique.
- Tạo promotion với discount fields, limits, start/end, isActive.
- Lưu ý: DTO có `hotelId`, nhưng service create hiện không set `hotelId`, nên promotion tạo qua API đang thành global promotion.

Admin list:

- Search code/name.
- Filter `isActive`.
- Pagination.
- Include hotel.

Public list:

- Chỉ `isActive = true`.
- `startAt <= now`, `endAt >= now`.
- Optional search.
- Include hotel.

Update/delete:

- Nếu promotion gắn hotel:
  - User phải admin/owner/member của hotel.
- Nếu promotion global:
  - Chỉ admin.

### 4.13 Commission package

Endpoints:

- Base `/api/v1/admin/commission-packages`
- `GET /`
- `GET /revenue/chart`
- `GET /:id`
- `POST /`
- `PATCH /:id`
- `PATCH /:id/deactivate`
- `PATCH /:hotelId/commission-package`

Logic:

- CRUD package đơn giản.
- `commissionRate` validate trong DTO từ 0 đến 1.
- Deactivate set `isActive = false`.
- Set commission package update `Hotel.commissionPackageId`.
- Booking creation snapshot rate và amount vào booking.
- Revenue chart chỉ tính booking `COMPLETED` có `commissionAmount != null`.
- Query `year`: trả mảng 12 tháng.
- Query `from/to`: trả từng booking `{ date, revenue }`.
- Default current year.

### 4.14 Dashboard

Endpoints:

- `GET /api/v1/dashboard/stats`
- `GET /api/v1/dashboard/revenue-chart`
- `GET /api/v1/dashboard/latest-reviews`
- `GET /api/v1/dashboard/newest-bookings`

Stats:

- Nếu có hotelId:
  - totalUsers = distinct userId từ booking của hotel.
  - totalBookings theo hotel.
  - revenue = sum totalAmount của booking `COMPLETED` theo hotel.
  - activeHotels = 1 nếu hotel ACTIVE.
- Nếu không có hotelId:
  - totalUsers = count users.
  - totalBookings = count bookings.
  - revenue = sum booking completed.
  - activeHotels = count hotel ACTIVE.

Revenue chart:

- Filter booking `COMPLETED`.
- Có thể theo hotelId.
- Nếu groupBy month và không from/to, init 12 tháng.
- Nếu group day/week hiện logic đều group theo date string.

Latest reviews/newest bookings:

- Lấy mới nhất theo createdAt, optional hotelId, limit.

### 4.15 Policy

Endpoints:

- `GET /api/v1/hotels/:hotelId/policies`
- `GET /api/v1/admin/hotels/:hotelId/policies`
- `GET /api/v1/admin/hotels/:hotelId/policies/:id`
- `POST /api/v1/admin/hotels/:hotelId/policies`
- `PATCH /api/v1/admin/hotels/:hotelId/policies/:id`
- `DELETE /api/v1/admin/hotels/:hotelId/policies/:id`

Logic:

- Public list chỉ `enabled = true`, order asc.
- Admin endpoints yêu cầu owner/member.
- Create:
  - Check `order` không trùng trong hotel.
  - Schema còn unique `[hotelId, type]`, nên mỗi type chỉ có một policy.
- Update:
  - Nếu đổi order, check không trùng policy khác.
- Delete hard delete.

### 4.16 News

Endpoints:

- `GET /api/v1/news`
- `GET /api/v1/news/:slug`
- `POST /api/v1/admin/news`
- `GET /api/v1/admin/news`
- `GET /api/v1/admin/news/id/:id`
- `PATCH /api/v1/admin/news/:id`
- `DELETE /api/v1/admin/news/:id`

Logic:

- Slugify title:
  - Lowercase.
  - Normalize/remove accent.
  - Non alphanumeric thành `-`.
  - Nếu trùng slug, append timestamp.
- Create:
  - Status mặc định DRAFT.
  - Nếu PUBLISHED, set `publishedAt = now`.
  - Image ids phải thuộc gallery của user.
  - Tạo news + images.
- Public list/detail:
  - Chỉ `status = PUBLISHED`, `deletedAt = null`.
- Admin list/detail:
  - Có thể filter status/q.
- Update:
  - Nếu có status PUBLISHED, update `publishedAt = now`; nếu không published thì null.
  - Nếu truyền imageIds, replace toàn bộ images.
- Remove:
  - Soft delete bằng `deletedAt`.

### 4.17 Banner

Endpoints:

- `GET /api/v1/banners`
- `POST /api/v1/admin/banners`
- `GET /api/v1/admin/banners`
- `PATCH /api/v1/admin/banners/:id`
- `DELETE /api/v1/admin/banners/:id`

Logic:

- Create:
  - Nếu có startAt/endAt, startAt <= endAt.
  - Position không được trùng.
  - Images tối thiểu qua DTO.
  - Lưu createdById.
- Update:
  - Check banner tồn tại.
  - Check date range.
  - Nếu đổi position, không được trùng.
  - Nếu truyền images, replace toàn bộ images.
- Public list:
  - `isActive = true`.
  - startAt null hoặc <= now.
  - endAt null hoặc >= now.
  - order position asc.
- Delete hard delete banner, images cascade.

### 4.18 Contact

Endpoints:

- `POST /api/v1/contact`
- `GET /api/v1/admin/contacts`
- `GET /api/v1/admin/contacts/:id`
- `PATCH /api/v1/admin/contacts/:id`

Create contact:

- Bắt buộc có email hoặc phone.
- Lưu name/email/phone/subject/message, ip, userAgent.
- Gửi mail support/admin.
- Tạo notification `SYSTEM` cho user có role `ADMIN`, `OWNER`, `STAFF`.
- Trả `{ id, ok: true }`.

Admin list:

- Filter status.
- Search name/email/phone/subject/message.
- Pagination.
- Include handledBy.

Update:

- Update status, handledById, note.

Lưu ý:

- Comment nói mail best-effort, nhưng đoạn create không bọc try/catch quanh `sendContactNotification`, nên lỗi mail có thể làm request fail.

### 4.19 Notification

Endpoints:

- `GET /api/v1/notifications`
- `GET /api/v1/notifications/unread-count`
- `PATCH /api/v1/notifications/read-all`
- `PATCH /api/v1/notifications/:id/read`
- `DELETE /api/v1/notifications/:id`

Logic:

- Mọi thao tác user-facing đều filter theo `userId`.
- List phân trang, order newest first.
- `markAsRead` check ownership trước.
- `markAllAsRead` update toàn bộ unread của user.
- `remove` delete notification của user.

### 4.20 Cloudinary/Gallery/Avatar

Cloudinary endpoints:

- `POST /api/v1/upload`
- `GET /api/v1/upload/folders`
- `GET /api/v1/upload/folders/:folderName`
- `POST /api/v1/upload/create-folder`
- `POST /api/v1/upload/image/:folderName`
- `GET /api/v1/upload/db-folders`
- `GET /api/v1/upload/db-folders/:folderId/images`

Logic:

- Generic upload vào folder `stayra`.
- DB folder tạo `FolderGallery` theo user.
- Upload image to folder:
  - Tạo folder DB nếu chưa có.
  - Upload Cloudinary.
  - Tạo `ImageGallery` với publicId/url/secureUrl/userId/folderId.
- DB folders trả folder của user và count ảnh của user.
- Get images trong folder filter userId + folderId.

Avatar:

- `POST /api/v1/users/me/avatar`: upload Cloudinary, xóa avatar cũ nếu có, tạo `ImageAsset`, gán `user.avatarId`.
- `DELETE /api/v1/users/me/avatar`: destroy Cloudinary, set avatarId null, xóa ImageAsset.

## 5. Frontend business logic

### 5.1 Route groups

Public routes:

- `/`: trang chủ.
- `/hotels`: danh sách khách sạn public.
- `/hotels/[hotel_id]`: chi tiết hotel, gallery, room availability, reviews, policies.
- `/booking`: xác nhận booking từ query params.
- `/payment-result`: kết quả thanh toán.
- `/login`, `/register`, `/forgot-password`, `/auth/reset`, `/auth/verify-email`, `/auth/callback`.
- `/me`: profile.
- `/me/my-bookings`, `/me/my-bookings/[booking_id]`.
- `/me/my-reviews`.
- `/news`, `/news/[news_id]`.
- `/contact`, `/partner`.

Admin routes:

- `/admin`: dashboard/admin home.
- `/admin/dashboard/[hotel_id]`.
- `/admin/hotels`, `/admin/hotels/[id]`.
- `/admin/member-hotels`.
- `/admin/room-types`, `/admin/room-types/[hotel_id]`, `/admin/room-types/[hotel_id]/manage/[type_id]`, room detail route.
- `/admin/inventory`.
- `/admin/bookings`, `/admin/bookings/[hotel_id]`, booking detail route.
- `/admin/reviews`, `/admin/reviews/[hotel_id]`.
- `/admin/promotions`, `/admin/promotions/[id]`.
- `/admin/commissions`, `/admin/commissions/[commission_id]`, `/admin/commissions/hotels`.
- `/admin/users`, `/admin/users/roles`, `/admin/users/permissions`, `/admin/users/actions`.
- `/admin/amenities`, `/admin/amenities/[id]`.
- `/admin/news`, `/admin/news/[news_id]`.
- `/admin/contacts`, `/admin/contacts/[contact_id]`.
- `/admin/policies`, `/admin/policies/[hotel_id]`, `/admin/policies/[hotel_id]/policy/[policy_id]`.
- `/admin/settings` dùng cho banner/settings.

### 5.2 AuthProvider và axios

`AuthProvider`:

- `loadUser`: nếu có `accessToken`, gọi `GET /users/me`.
- `login`: gọi `/auth/login`, lưu access token, load user, redirect `/me`.
- `register`: gọi `/auth/register`, redirect `/login`.
- `logout`: gọi `/auth/logout`, clear access token, redirect login.
- `forgotPassword`, `resetPassword`: gọi API tương ứng.

`PermissionProvider`:

- Dựa vào `user.allowedActions`.
- Expose `can`, `canAny`, `canAll`.
- Không render children khi auth loading.

`AdminRoute`:

- Chỉ yêu cầu user tồn tại và `roles.length > 0`.
- Không check role name cụ thể.

### 5.3 Public hotel search/booking flow

Luồng tìm và chọn phòng:

1. User vào `/hotels`.
2. `HotelSearch` gọi `GET /hotels/public` với filters như city, date, price, q, sort.
3. User vào `/hotels/[hotel_id]`.
4. Page gọi:
   - `GET /hotels/:hotelId`
   - `GET /hotels/:hotelId/room-types/available?from=&to=`
   - `GET /hotels/:hotelId/reviews`
   - `GET /hotels/:hotelId/policies`
5. User chọn ngày và số lượng room type.
6. Frontend không cho quantity vượt `availableRooms`.
7. Bấm Book Now tạo URL:
   - `/booking?hotel_id=...&check_in=...&check_out=...&total_price=...&rooms=roomTypeId:qty,...`

Luồng xác nhận booking:

1. `/booking` parse query params.
2. Gọi lại hotel detail và room-types available để xác nhận dữ liệu.
3. Form nhập guestName, guestPhone, guestEmail, note, promotionCode.
4. Promotion search gọi `GET /promotions/public?search=...`.
5. Frontend tự tính discount preview:
   - PERCENT/FIXED.
   - minBookingAmount.
   - maxDiscountAmount.
   - discount không vượt rawTotal.
6. Submit gọi `POST /hotels/:hotelId/bookings` với:
   - checkIn/checkOut.
   - guest info.
   - promotionCode.
   - totalAmount frontend tính.
   - items.
7. Backend vẫn tự tính total/discount thật; frontend totalAmount không phải nguồn tin cậy.
8. Sau success, frontend alert và redirect `/`, chưa tự chuyển sang payment.

### 5.4 Payment/account flow

My bookings:

- `/me/my-bookings` gọi `GET /bookings/me`.
- `/me/my-bookings/[booking_id]` gọi `GET /bookings/me/:bookingId`.

Nếu booking `PENDING`, user có thể:

- Hủy booking:
  - `PATCH /hotels/:hotelId/bookings/:bookingId/cancel`.
- Tạo thanh toán VNPAY:
  - `POST /bookings/:bookingId/payments/vnpay`.
  - Payload mặc định `{ locale: 'vn', bankCode: 'NCB' }`.
  - Redirect `window.location.href = paymentUrl`.

Payment result:

- `/payment-result` đọc query:
  - `payment_status=success|failed`
  - `booking_id`
- Gọi `GET /bookings/me/:bookingId`.
- Nếu failed và booking còn `PENDING`, cho retry bằng cách quay về booking detail.

Profile:

- `/me` update profile `PATCH /users/me`.
- Change password `POST /users/me/change-password`.
- Upload avatar `POST /users/me/avatar`.

Review:

- `/me/my-reviews` gọi `GET users/me/reviews`.
- Update review `PATCH reviews/:id`.
- Booking `COMPLETED` mới có nút review ở UI.

### 5.5 Admin workflows

Admin navigation:

- Sidebar lọc menu theo action key từ `allowedActions`.
- Các action chính:
  - `dashboard.read`
  - `hotels.admin.list`
  - `inventories.list`
  - `room-types.list`
  - `amenities.list`
  - `bookings.list`
  - `news.read`
  - `reviews.moderate`
  - `promotions.list`
  - `commission-packages.list`
  - `users.list`
  - `roles.list`
  - `permissions.list`
  - `actions.list`
  - `contacts.read`
  - `policies.read`
  - `banners.read`

Hotel/room/inventory:

- Hotel CRUD dùng `/hotels`.
- Members dùng `/hotels/:hotelId/members`.
- Room types dùng `/hotels/:hotelId/room-types`.
- Rooms dùng `/hotels/:hotelId/rooms`.
- Inventory dùng:
  - `GET /hotels/:hotelId/inventories`
  - `POST /hotels/:hotelId/inventories/bulk`
  - `PATCH /hotels/:hotelId/inventories/:id`
- Frontend inventory validator có rule `availableRooms <= totalRooms`.
- API wrapper inventory hiện chưa có delete wrapper dù backend có endpoint delete.

Bookings:

- `/admin/bookings` trước tiên list hotels bằng `GET /hotels`.
- `/admin/bookings/[hotel_id]` gọi `GET /hotels/:hotelId/bookings` với filter.
- Detail gọi `GET /hotels/:hotelId/bookings/:bookingId`.
- Update status theo frontend transitions:
  - `PENDING -> CONFIRMED | CANCELLED`
  - `CONFIRMED -> CHECKED_IN | CANCELLED`
  - `CHECKED_IN -> COMPLETED`
  - Terminal: `COMPLETED`, `CANCELLED`, `NO_SHOW`
- Check-in mở form khách:
  - Primary guest bắt buộc fullName.
  - Companions optional.
  - Gọi `POST /bookings/:bookingId/check-in`.
- Xem check-in gọi `GET /bookings/:bookingId/check-in`.

RBAC/admin users:

- Users list: `GET /users`.
- Frontend có update/delete user wrapper nhưng backend endpoint chưa tương ứng.
- Roles CRUD và assign permissions.
- Permissions CRUD.
- Actions list và assign permissions.
- Assign role to user: `POST /roles/assign-to-user`.

Content/support:

- Amenities CRUD.
- Reviews moderation.
- Promotions CRUD/public search.
- Commission packages CRUD/revenue/assign.
- Contact list/detail/update.
- News CRUD/public.
- Policies CRUD/public.
- Banners CRUD/public.
- Gallery folders/images.
- Notifications list/unread/mark/delete; unread count refetch mỗi 30s.

### 5.6 Frontend validation đáng chú ý

Auth:

- Email hợp lệ.
- Password tối thiểu 8 ký tự, có thường, hoa, số, ký tự đặc biệt.
- Confirm password phải trùng.

Booking:

- `guestName`, `guestPhone` bắt buộc.
- `guestEmail` optional nhưng nếu có phải email.
- `note`, `promotionCode` optional.

Check-in:

- `primary.fullName` bắt buộc.
- Email optional nhưng phải hợp lệ nếu có.
- Gender `MALE | FEMALE | OTHER`.
- Companions là mảng guest tương tự.

Hotel:

- name/address/description/city/country bắt buộc ở form.
- Status `DRAFT | ACTIVE | SUSPENDED | ARCHIVED`.
- Images optional, URL hợp lệ.

Room type:

- name, price_per_night, description bắt buộc.
- `max_guests >= 1`.
- amenities/images optional.

Room:

- code bắt buộc.
- Status `ACTIVE | INACTIVE | MAINTENANCE`.
- Clean status `CLEAN | DIRTY | INSPECT`.

Inventory:

- from/to format `YYYY-MM-DD`.
- roomTypeId bắt buộc.
- totalRooms/availableRooms integer >= 0.
- availableRooms không vượt totalRooms.

Promotion:

- code uppercase.
- Percent không quá 100.
- `endAt > startAt`.
- usage limit >= 1.

Banner:

- images tối thiểu 1 URL.
- position >= 0.
- startAt <= endAt nếu có.

Policy:

- Type thuộc enum.
- title/content bắt buộc.

Contact:

- name/message bắt buộc.
- Phải có email hoặc phone.

Review:

- rating 1..5.
- bookingId bắt buộc khi tạo.

## 6. Các luồng nghiệp vụ end-to-end

### 6.1 Khách đặt phòng

1. Khách tìm hotel public theo địa điểm/ngày/giá.
2. Hotel public phải ACTIVE, chưa deleted, có room type.
3. Khách vào detail, chọn ngày và room type còn available.
4. Frontend giới hạn quantity theo `availableRooms`.
5. Khách submit booking.
6. Backend kiểm tra lại mọi thứ trong transaction:
   - date range.
   - room type thuộc hotel.
   - inventory đủ từng đêm.
   - stopSell false.
   - promotion hợp lệ.
7. Backend trừ tồn ngay và tạo booking `PENDING`.
8. Owner/member nhận notification new booking.
9. Khách vào booking detail để thanh toán.
10. VNPAY success thì payment `SUCCEEDED`, booking `CONFIRMED`.
11. Nếu quá 15 phút chưa payment success, cron cancel booking và trả tồn.

### 6.2 Vận hành lưu trú

1. Owner/member xem danh sách booking theo hotel.
2. Booking PENDING có thể confirm/cancel.
3. Booking CONFIRMED có thể cancel hoặc check-in.
4. Check-in lưu thông tin primary guest + companions.
5. Check-in set booking `CHECKED_IN`.
6. Sau lưu trú, admin/staff chuyển `CHECKED_IN -> COMPLETED`.
7. Booking COMPLETED mới được user review.

### 6.3 Quản trị khách sạn

1. User tạo hotel và trở thành owner/member.
2. Owner/member cập nhật thông tin hotel, ảnh, members.
3. Tạo room types, gắn amenities/images.
4. Tạo rooms vật lý để quản trị vận hành.
5. Bulk set inventory theo room type và ngày.
6. Public booking chỉ dựa vào inventory, không dựa trực tiếp vào số lượng room records.
7. Owner/member quản lý policies, reviews moderation, bookings, rooms, inventory.

### 6.4 RBAC/action permission

1. Admin tạo permission.
2. Admin tạo role.
3. Admin gán permission cho role.
4. Admin seed/upsert action.
5. Admin gán permissions required cho action.
6. User được gán role.
7. `/users/me` trả `allowedActions`.
8. Frontend ẩn/hiện menu theo actions.
9. Backend route có `ActionGuard` enforce quyền theo action policies.

### 6.5 Promotion và commission

Promotion:

1. Admin tạo promotion.
2. Public booking form search promotion active.
3. Frontend tính preview discount.
4. Backend validate lại promotion và tính discount thật.
5. Booking lưu `discountAmount`, `promotionId`.
6. `usedCount` tăng ngay khi booking được tạo.

Commission:

1. Admin tạo commission package.
2. Gán package cho hotel.
3. Khi booking tạo, nếu package active:
   - Lưu `commissionRateSnapshot`.
   - Tính `commissionAmount`.
4. Revenue chart commission chỉ tính booking COMPLETED.

## 7. API mapping chính

Base URL frontend: `NEXT_PUBLIC_API_BASE_URL || http://localhost:8080/api/v1`.

Auth:

- `/auth/login`
- `/auth/register`
- `/auth/logout`
- `/auth/refresh`
- `/auth/forgot-password`
- `/auth/reset-password`
- `/auth/google`
- `/auth/verify-email`
- `/auth/resend`

User/RBAC:

- `/users`, `/users/:id`, `/users/me`, `/users/me/change-password`, `/users/me/avatar`
- `/roles`, `/roles/:id`, `/roles/:id/permissions`, `/roles/assign-to-user`
- `/permissions`, `/permissions/:id`
- `/actions`, `/actions/:id/permissions`

Hotels:

- `/hotels`
- `/hotels/public`
- `/hotels/:id`
- `/hotels/:hotelId/members`
- `/hotels/:hotelId/members/:userId`

Room/inventory:

- `/room-types`
- `/hotels/:hotelId/room-types`
- `/hotels/:hotelId/room-types/available`
- `/hotels/:hotelId/room-types/:id`
- `/hotels/:hotelId/rooms`
- `/hotels/:hotelId/rooms/:roomId`
- `/hotels/:hotelId/inventories`
- `/hotels/:hotelId/inventories/bulk`
- `/hotels/:hotelId/inventories/:id`

Booking/payment/check-in:

- `/bookings/me`
- `/bookings/me/:bookingId`
- `/bookings/:bookingId/payments/vnpay`
- `/bookings/:bookingId/check-in`
- `/hotels/:hotelId/bookings`
- `/hotels/:hotelId/bookings/:bookingId`
- `/hotels/:hotelId/bookings/:bookingId/status`
- `/hotels/:hotelId/bookings/:bookingId/cancel`
- `/payments/vnpay/return`
- `/payments/vnpay/ipn`

Review/promotion/policy:

- `/hotels/:hotelId/reviews`
- `/hotels/:hotelId/reviews/moderation`
- `/hotels/:hotelId/reviews/:id/moderate`
- `/hotels/:hotelId/reviews/:id`
- `/reviews/:id`
- `/promotions`
- `/promotions/public`
- `/promotions/:id`
- `/admin/hotels/:hotelId/policies`
- `/admin/hotels/:hotelId/policies/:policyId`
- `/hotels/:hotelId/policies`

CMS/support/dashboard:

- `/news`, `/news/:slug`
- `/admin/news`, `/admin/news/id/:id`, `/admin/news/:id`
- `/banners`, `/admin/banners`, `/admin/banners/:id`
- `/contact`, `/admin/contacts`, `/admin/contacts/:id`
- `/dashboard/stats`
- `/dashboard/revenue-chart`
- `/dashboard/latest-reviews`
- `/dashboard/newest-bookings`
- `/admin/commission-packages`
- `/admin/commission-packages/:id`
- `/admin/commission-packages/:id/deactivate`
- `/admin/commission-packages/:hotelId/commission-package`
- `/admin/commission-packages/revenue/chart`

Upload/notification:

- `/upload`
- `/upload/folders`
- `/upload/folders/:folderName`
- `/upload/create-folder`
- `/upload/image/:folderName`
- `/upload/db-folders`
- `/upload/db-folders/:folderId/images`
- `/notifications`
- `/notifications/unread-count`
- `/notifications/read-all`
- `/notifications/:id/read`

## 8. Business invariants và điểm cần lưu ý

Các invariant quan trọng:

- Booking chỉ hợp lệ nếu `checkIn < checkOut`.
- Booking tính đêm theo `[checkIn, checkOut)`.
- Booking trừ inventory trong transaction, từng room type/từng ngày.
- Inventory là nguồn chống overbooking, không phải `Room.status`.
- Booking PENDING giữ tồn trong 15 phút.
- Payment success chuyển booking sang CONFIRMED.
- Check-in chuyển booking sang CHECKED_IN.
- Chỉ booking COMPLETED được review.
- Một booking chỉ có một review.
- Public hotel phải ACTIVE và chưa deleted.
- Room type name unique trong hotel.
- Room code unique trong hotel.
- Promotion discount không vượt tổng tiền.
- Commission amount snapshot tại thời điểm tạo booking.

Các điểm lệch/rủi ro trong code hiện tại:

- `schema.prisma` mới hơn migrations, cần tạo migration đầy đủ.
- `logout` chỉ clear cookie, không revoke session DB.
- `logout-all` dùng `req.user.sub` trong khi strategy trả `id`.
- `resendVerificationEmail` gửi token thay vì verify URL đầy đủ.
- `UsersController` có `@Action('users.list')` nhưng không gắn `ActionGuard`.
- `RolesController`, `PermissionsController`, `ActionsController` có nơi action/permission metadata chưa enforce thật vì thiếu guard phù hợp.
- `PermissionsGuard` không có tác dụng nếu route không gắn `@Permissions`.
- Frontend admin route chỉ cần user có ít nhất một role, không check role ADMIN cụ thể.
- Frontend menu permission chỉ ẩn/hiện UI, không thay thế backend authorization.
- Frontend có wrapper update/delete user nhưng backend chưa thấy endpoint tương ứng.
- `Payment.createVnpayPaymentUrl` không kiểm booking thuộc user đang gọi.
- VNPAY return idempotent branch có thể thiếu `bookingId`.
- Promotion `usedCount` tăng khi booking tạo, không chờ payment success.
- Hủy booking không thấy decrement promotion `usedCount`.
- `Promotion.create` không lưu `hotelId` dù DTO có field.
- `RoomType.getAvailableRoomTypes` dùng date range inclusive `[from, to]`, booking dùng checkout exclusive.
- `Hotel.listPublicHotels` date filter chưa đảm bảo đủ availability cho mọi ngày.
- Backend inventory không enforce `availableRooms <= totalRooms`.
- `Policy.remove` hard delete, khác style soft delete của nhiều domain khác.
- `ListUsersQuery.sortBy = fullName` có thể lỗi vì DB không có field này.
- Contact mail comment là best-effort nhưng không có try/catch rõ trong create flow.

