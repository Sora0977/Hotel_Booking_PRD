# Toàn bộ nghiệp vụ bằng lời - hotel-booking-web

Tài liệu này diễn giải các nghiệp vụ đang có trong source code `Clone/hotel-booking-web` bằng lời tự nhiên. Nội dung bên dưới mô tả hệ thống theo hành vi nghiệp vụ: người dùng làm gì, hệ thống kiểm tra gì, dữ liệu nào được tạo hoặc cập nhật, trạng thái chuyển như thế nào, và các quy tắc quan trọng nằm trong code.

Đây là mô tả theo code hiện tại, không phải bản thiết kế mong muốn. Vì vậy các điểm chưa nhất quán, endpoint thiếu guard, hoặc rule có vẻ chưa hoàn thiện vẫn được ghi lại như một phần của nghiệp vụ thực tế.

## 1. Bức tranh nghiệp vụ tổng thể

Hệ thống là một nền tảng đặt phòng khách sạn. Phần public phục vụ khách xem khách sạn, tìm phòng, đặt phòng, thanh toán, xem tin tức, gửi liên hệ và quản lý tài khoản cá nhân. Phần admin phục vụ người quản trị hệ thống, chủ khách sạn hoặc nhân sự khách sạn quản lý khách sạn, phòng, tồn kho, đơn đặt phòng, check-in, đánh giá, khuyến mãi, chính sách, hoa hồng, tin tức, banner, liên hệ, người dùng và phân quyền.

Backend dùng NestJS, Prisma và PostgreSQL. API có prefix `api/v1`. Frontend dùng Next.js App Router, React Query, axios, React Hook Form và Zod. Dữ liệu nghiệp vụ chính nằm trong Prisma schema, còn các quy tắc xử lý nằm trong các service của backend và một phần trong validator/flow của frontend.

Các nhóm tác nhân chính gồm:

- Khách vãng lai: xem khách sạn, xem phòng, xem review, xem news/banner/policy, gửi contact, đăng ký tài khoản.
- Người dùng đã đăng nhập: đặt phòng, xem booking của mình, thanh toán, hủy booking còn chờ, cập nhật hồ sơ, đổi mật khẩu, upload avatar, tạo hoặc sửa review của mình.
- Chủ khách sạn hoặc thành viên khách sạn: quản lý hotel, room type, room, inventory, booking của khách sạn, check-in, chính sách, review moderation và các nội dung có phạm vi hotel.
- Admin hệ thống: quản lý user, role, permission, action policy, hotel, commission package, promotion global, news, banner, contact và các dashboard tổng hợp.
- Hệ thống nền: tự hủy booking `PENDING` quá hạn, gửi email, tạo notification, ghi log payment event.

## 2. Nghiệp vụ tài khoản và định danh

### 2.1 Đăng ký tài khoản local

Khi khách đăng ký bằng email và mật khẩu, hệ thống chuẩn hóa email bằng cách trim và lowercase. Sau đó service tạo user local với `passwordHash` được hash bằng argon2. User mới mặc định chưa xác thực email, vì vậy chưa thể đăng nhập thành công ngay.

Sau khi tạo user, backend tạo một token xác thực email dạng raw token. Token raw chỉ gửi cho người dùng qua email, còn database chỉ lưu hash SHA-256 của token, thời điểm hết hạn và trạng thái đã dùng hay chưa. Token xác thực email có thời hạn 30 phút. Link xác thực được tạo dựa trên `PUBLIC_WEB_URL` và trỏ về trang `/auth/verify-email?token=...`.

Nghiệp vụ này có ý nghĩa là tài khoản chỉ được kích hoạt sau khi người dùng sở hữu email đó bấm vào link xác thực. Nếu email trùng với tài khoản đã tồn tại thì service tạo user local sẽ báo lỗi.

### 2.2 Xác thực email

Khi user mở link xác thực, frontend gửi token về backend. Backend hash lại token raw và tìm bản ghi `EmailVerifyToken`. Token chỉ hợp lệ khi tồn tại, chưa được dùng và chưa hết hạn.

Nếu token hợp lệ, backend chạy transaction để đánh dấu `user.emailVerified = true` và set `usedAt` cho token. Từ sau bước này user mới được phép login bằng email/password.

Nếu token sai, đã dùng hoặc hết hạn, hệ thống trả lỗi. Điều này ngăn việc reuse link cũ hoặc xác thực lại bằng token đã tiêu thụ.

### 2.3 Gửi lại email xác thực

User có thể yêu cầu gửi lại email xác thực. Service tìm user theo email, kiểm tra user chưa xác thực, kiểm tra token gần nhất để tránh spam gửi lại quá nhanh, sau đó xóa token cũ chưa dùng và tạo token mới.

Code hiện tại gửi token cho mail service ở luồng resend. Ở luồng register, mail service nhận verify URL đầy đủ; ở resend, giá trị truyền vào có vẻ là token raw chứ không phải URL đầy đủ. Đây là điểm lệch cần chú ý nếu kiểm thử chức năng gửi lại email.

### 2.4 Đăng nhập bằng email và mật khẩu

Khi đăng nhập local, backend tìm user bằng email. User phải tồn tại, phải có `passwordHash`, mật khẩu nhập vào phải verify được với argon2, và `emailVerified` phải bằng true.

Nếu tất cả điều kiện đúng, backend tạo một cặp token gồm access token và refresh token. Access token dùng cho các request API. Refresh token được đặt vào cookie HTTP-only tên `refresh_token`. Backend cũng tạo một bản ghi `AuthSession` với `jti`, hash của refresh token, provider, userAgent, ip và thời điểm hết hạn.

Frontend sau khi login lưu access token vào cookie `accessToken`, gọi lại `/users/me` để lấy thông tin user và chuyển user về `/me`.

### 2.5 Quản lý phiên đăng nhập và refresh token

Mỗi lần đăng nhập hoặc Google OAuth tạo một session. Session gắn với `jti`. Refresh token được ký riêng, payload có `type = refresh`. Database không lưu refresh token raw mà lưu hash để nếu DB lộ cũng không dùng được token.

Khi access token hết hạn và API trả 401, frontend axios interceptor tự gọi `/auth/refresh`. Backend đọc refresh token từ cookie, verify chữ ký, kiểm tra payload là refresh token, tìm session theo `jti`, kiểm tra session chưa bị revoke, rồi verify hash.

Nếu hash không khớp, backend xem đây là dấu hiệu reuse refresh token và revoke toàn bộ session của user. Nếu hash khớp, backend revoke session cũ với lý do rotated, tạo session mới và trả access token mới cùng refresh cookie mới. Đây là cơ chế refresh token rotation.

### 2.6 Logout và logout all

Logout bình thường ở controller hiện clear cookie refresh. Phần revoke session hiện tại trong code bị comment, nên nghiệp vụ thực tế là phía client mất cookie/token, nhưng DB session có thể vẫn chưa bị revoke.

Logout all gọi service revoke toàn bộ session của user rồi clear cookie. Tuy nhiên controller dùng `req.user.sub` trong khi JWT strategy trả user object có field `id`. Vì vậy có rủi ro logout all không revoke đúng user nếu request user không có `sub`.

### 2.7 Quên mật khẩu và đặt lại mật khẩu

Ở luồng forgot password, user nhập email. Nếu email không tồn tại, backend không báo lỗi rõ để tránh lộ thông tin email nào đã đăng ký. Nếu email tồn tại, backend xóa các password reset token cũ của user, tạo token mới, lưu hash SHA-256, đặt hạn 30 phút và gửi link reset qua email.

Ở luồng reset password, backend kiểm tra token tồn tại, chưa dùng và chưa hết hạn. Nếu hợp lệ, backend hash mật khẩu mới, cập nhật `passwordHash`, đánh dấu token đã dùng và xóa toàn bộ auth session của user. Việc xóa session buộc user đăng nhập lại bằng mật khẩu mới trên mọi thiết bị.

### 2.8 Đổi mật khẩu khi đã đăng nhập

Người dùng đã đăng nhập có thể đổi mật khẩu. Hệ thống kiểm tra mật khẩu mới và xác nhận mật khẩu phải trùng nhau, user phải là tài khoản có mật khẩu local, mật khẩu hiện tại phải đúng. Sau khi đổi, backend cập nhật hash mới và xóa toàn bộ session hiện có.

Điều này giúp bảo vệ tài khoản nếu mật khẩu cũ bị lộ: sau khi đổi, các phiên cũ không còn hợp lệ.

### 2.9 Đăng nhập bằng Google

Google OAuth dùng Google strategy để lấy thông tin profile. Nếu email Google trùng với tài khoản local đã tồn tại, backend không tự động gộp tài khoản mà từ chối và yêu cầu login bằng password hoặc link Google sau. Nếu provider khác không khớp cũng bị từ chối.

Nếu hợp lệ, backend upsert user theo `providerId`, set provider là `GOOGLE`, set `emailVerified = true`, tạo auth session provider Google, trả access token và refresh token. Callback redirect về frontend `/auth/callback#access_token=...`.

Một điểm cần chú ý là strategy map `firstName` và `lastName` từ Google profile có vẻ bị đảo giữa familyName và givenName.

### 2.10 Hồ sơ cá nhân và avatar

Người dùng có thể xem `/users/me`. Response không chỉ trả thông tin public user, roles và avatar, mà còn tính thêm `allowedActions` để frontend biết user được phép thấy menu/tính năng nào.

Người dùng có thể cập nhật hồ sơ cá nhân, đổi mật khẩu, upload avatar hoặc xóa avatar. Avatar được upload lên Cloudinary trong folder theo user. Khi upload avatar mới, hệ thống xóa avatar cũ trên Cloudinary nếu có, xóa `ImageAsset` cũ, tạo `ImageAsset` mới và gắn `avatarId` vào user. Khi xóa avatar, backend destroy ảnh trên Cloudinary, set `avatarId = null` và xóa asset.

## 3. Nghiệp vụ phân quyền hệ thống

### 3.1 Role, permission và user role

Hệ thống dùng mô hình RBAC. User có nhiều role. Role có nhiều permission. Role name unique, permission name unique. Khi gán role cho user hoặc gán permission cho role, code dùng kiểu replace-all: danh sách cũ bị xóa rồi tạo danh sách mới.

Khi set permission cho role, hệ thống trim id, không cho danh sách rỗng, không cho duplicate, và kiểm tra tất cả permission id phải tồn tại. Nếu thiếu id nào thì báo lỗi. Khi xóa permission, code xóa các liên kết `RolePermission` trước rồi mới xóa permission. (Lưu ý: Hiện tại hệ thống đang bị sót việc xóa liên kết với các `ApiAction`, nên nếu bạn cố xóa một quyền đang được gán cho một hành động nào đó, hệ thống sẽ báo lỗi và không cho phép xóa).

### 3.2 ApiAction và action policy

Ngoài RBAC truyền thống, code có thêm lớp `ApiAction`. Mỗi action đại diện cho một hành động nghiệp vụ như `hotels.create`, `bookings.cancel`, `roles.list`, `promotions.list`. Action có key unique, trạng thái enabled và mode `ANY` hoặc `ALL`.

Một `ApiAction` có thể gắn nhiều permission thông qua `ApiActionPolicy`. Nếu mode là `ANY`, user chỉ cần có ít nhất một permission trong policy. Nếu mode là `ALL`, user phải có đủ toàn bộ permission trong policy. Việc gán quyền cho Action cũng tuân thủ quy tắc cực kỳ nghiêm ngặt giống như gán quyền cho Role: danh sách quyền mới sẽ ghi đè hoàn toàn danh sách cũ, không cho phép để trống, không được trùng lặp, và mọi quyền được gán đều phải tồn tại.

Tuy nhiên, hiện tại trên giao diện quản trị (Frontend) vẫn chưa có tính năng để tạo mới hay chỉnh sửa các Action này, dù hệ thống lõi (Backend) đã hỗ trợ sẵn chức năng này.

File `actions.sql` seed nhiều action nghiệp vụ cho amenities, bookings, commission packages, hotels, inventories, news, reviews, rooms, room types và các module quản trị.

### 3.3 Tính allowed actions cho frontend

Khi frontend gọi `/users/me`, backend gom tất cả permission của user từ các role, lấy danh sách action enabled, rồi tính xem action nào user được phép thực hiện theo mode `ANY` hoặc `ALL`. Danh sách key được trả về dưới dạng `allowedActions`.

Frontend `PermissionProvider` chuyển danh sách này thành `Set` và cung cấp hàm `can`, `canAny`, `canAll`. Sidebar admin dùng các action key để ẩn hiện menu. Component `Can` dùng action key để ẩn hiện nút hoặc vùng UI.

Đây là logic hiển thị phía client. Nó không thay thế kiểm tra quyền ở backend.

### 3.4 Guard kiểm tra action ở backend

`ActionGuard` đọc metadata `@Action('...')` trên route. Nếu route public thì bỏ qua. Nếu route không public mà không có user thì trả 401. Nếu route không khai báo action thì trả 403. Nếu action không tồn tại, disabled hoặc không có policy phù hợp thì trả 403. Nếu user có đủ permission theo mode của action thì request được đi tiếp.

Guard này có hỗ trợ cache Redis nếu cấu hình Redis, TTL 60 giây. Tuy nhiên trong code hiện tại không phải controller nào có `@Action` cũng gắn `ActionGuard`, nên một số metadata action chỉ có tác dụng mô tả chứ chưa thật sự enforce.

### 3.5 Phân quyền theo phạm vi khách sạn

Ngoài RBAC toàn hệ thống, nhiều nghiệp vụ khách sạn tự kiểm tra user có quan hệ với hotel hay không. Quy tắc phổ biến là user được phép nếu là owner của hotel hoặc có bản ghi trong `HotelMember`.

Một số guard có tồn tại như `HotelMemberGuard`, `HotelMemberWithAdminGuard`, `HotelContextGuard`, `HotelRoleGuard`. Luồng chính trong service thường tự gọi `assertHotelAccess`. `HotelMemberWithAdminGuard` cho phép role `ADMIN` đi qua, còn nhiều service thuần hotel lại chỉ kiểm owner/member.

## 4. Nghiệp vụ quản lý người dùng

Admin có thể list user với filter theo từ khóa, role và trạng thái xác thực email. Từ khóa có thể tìm trên email, firstName, lastName. Danh sách có phân trang và sort theo query.

Khi xem public profile của user khác, service che email nếu requester không phải chính user đó và không có quyền admin/manager. Điều này tách dữ liệu cá nhân khỏi thông tin public.

Frontend có wrapper cho update/delete user theo id, nhưng backend users controller hiện không thấy endpoint update/delete user tương ứng. Vì vậy nghiệp vụ quản trị user trong code backend chủ yếu là list, xem detail, xem/me, update me, đổi mật khẩu, avatar và gán role qua roles module.

Một điểm cần chú ý là query sort user cho phép `fullName`, nhưng Prisma model không có field `fullName`; nếu sort field này được truyền xuống Prisma có thể lỗi.

## 5. Nghiệp vụ khách sạn

### 5.1 Tạo khách sạn

Người dùng đăng nhập có thể tạo khách sạn. Khi tạo, hotel được gán `ownerId` là user hiện tại. Đồng thời hệ thống tạo luôn một bản ghi `HotelMember` cho chính owner để owner xuất hiện trong danh sách thành viên. Nếu payload có ảnh, hệ thống tạo các bản ghi `HotelImage`.

Hotel có các thông tin như tên, mô tả, địa chỉ, city, country, status, owner, members, images, room types, rooms, bookings, reviews, policies, promotions, inventories, notifications và optional commission package.

### 5.2 Xem khách sạn của tôi

Người dùng có thể xem danh sách khách sạn mình quản lý. Điều kiện là hotel chưa soft delete và user là owner hoặc member. Danh sách được sort theo `createdAt desc`.

### 5.3 Cập nhật khách sạn

Khi cập nhật hotel, code chỉ xử lý hotel chưa bị soft delete. Phần thông tin thường được update trực tiếp. Phần ảnh được xử lý theo kiểu diff:

- Ảnh gửi lên có id trùng ảnh hiện có thì update URL.
- Ảnh gửi lên không có id thì tạo mới.
- Ảnh đang có trong DB nhưng không còn trong payload thì xóa.

Logic này làm cho payload ảnh khi update đại diện cho trạng thái ảnh mong muốn sau cùng.

### 5.4 Thành viên khách sạn

Owner hoặc người có quyền tương ứng có thể thêm thành viên vào khách sạn. Backend kiểm tra hotel tồn tại và chưa bị xóa, kiểm tra tất cả user id được gửi lên có tồn tại, rồi upsert `HotelMember` để tránh duplicate.

Xóa thành viên là xóa bản ghi theo khóa kép `hotelId_userId`. Schema có enum `HotelMemberRole`, nhưng model `HotelMember` hiện không có field role, nên nghiệp vụ member trong code chỉ là có hoặc không có quan hệ với hotel, chưa có phân vai nội bộ theo owner/staff/manager trong bảng member.

### 5.5 Xóa khách sạn

Xóa hotel là soft delete bằng cách set `deletedAt`. Chỉ owner hoặc user có role `ADMIN` được xóa. Hotel bị soft delete sẽ bị loại khỏi các list chính nếu không truyền `includeDeleted`.

### 5.6 Danh sách khách sạn admin

Danh sách admin có logic phân quyền theo role. Nếu user là `ADMIN`, user thấy tất cả khách sạn. Nếu không phải admin, user chỉ thấy khách sạn mà mình là member. Query hỗ trợ filter ownerId, city, name/q và includeDeleted. Response include images, owner, commission package và số lượng member.

### 5.7 Danh sách khách sạn public

Danh sách public chỉ trả hotel chưa xóa, status `ACTIVE`, và có ít nhất một room type chưa xóa. User có thể lọc theo q/city, khoảng giá và ngày.

Khoảng giá dựa trên `price_per_night` của room type. Nếu sort theo giá, code không sort trực tiếp bằng Prisma mà lấy các hotel match, tính min price của room type trong memory, sort rồi mới paginate.

Filter theo ngày dùng inventory để tìm khách sạn có room type còn phòng, `availableRooms > 0`, `stopSell = false`, `deletedAt = null`. Tuy nhiên filter public này chỉ đảm bảo có availability record phù hợp ở mức tương đối; nghiệp vụ booking phía sau mới kiểm từng ngày và từng item nghiêm ngặt hơn.

## 6. Nghiệp vụ tiện nghi

Amenity là danh mục tiện nghi gắn vào room type, ví dụ wifi, bữa sáng, hồ bơi. Khi tạo amenity, code trim key và label. `key` unique. Nếu trùng key, lỗi Prisma P2002 được chuyển thành BadRequest.

Danh sách amenity hỗ trợ search theo key/label, filter `isActive`, sort theo `sortOrder desc` rồi `createdAt desc`. Update trim field nếu có.

Xóa amenity thực tế là disable bằng cách set `isActive = false`. Room type chỉ nhận amenity active khi create/update.

## 7. Nghiệp vụ hạng phòng

### 7.1 Tạo hạng phòng

Room type thuộc về một hotel. Owner hoặc member của hotel mới được tạo. Khi tạo, backend kiểm tra quyền hotel, kiểm tra amenity ids nếu có phải tồn tại và active, kiểm tra tên room type không trùng trong cùng hotel, rồi tạo room type trong transaction.

Room type lưu tên, mô tả, `price_per_night`, `max_guests`, ảnh và tiện nghi. Giá được lưu bằng Decimal. Tên room type unique theo hotel ở mức nghiệp vụ và schema. (Lưu ý: Hệ thống quản lý tính duy nhất rất chặt ở tầng cơ sở dữ liệu. Vì vậy, nếu bạn tạo một hạng phòng với cái tên đã từng được dùng nhưng sau đó bị xóa, hệ thống sẽ văng lỗi hệ thống và không cho tạo).

### 7.2 Danh sách và chi tiết hạng phòng

**Dành cho quản trị:** Owner/member có thể xem danh sách hạng phòng trong khách sạn của mình. Danh sách này bỏ qua các hạng phòng đã bị xóa, hỗ trợ tìm kiếm và kèm theo thông tin tiện nghi, hình ảnh. Xem chi tiết cũng yêu cầu quyền quản lý và chỉ lấy hạng phòng thuộc đúng khách sạn đó.

**Dành cho hệ thống (Public):** Hệ thống có một danh sách mở (ẩn), cho phép lấy toàn bộ hạng phòng của *tất cả khách sạn* trên toàn hệ thống mà không cần đăng nhập hay lọc theo khách sạn cụ thể nào.

### 7.3 Cập nhật hạng phòng

Update room type kiểm tra quyền hotel, room type thuộc đúng hotel và chưa xóa. Nếu đổi tên, tên mới không được trùng room type khác trong cùng hotel.

Ảnh được xử lý theo diff giống hotel: update ảnh cũ, tạo ảnh mới, xóa ảnh không còn trong payload. Amenities cũng được xử lý theo diff: amenity mới thì create relation, amenity cũ không còn thì delete relation. Giá nếu được truyền thì convert sang Decimal.

### 7.4 Xóa hạng phòng

Xóa room type là soft delete bằng `deletedAt`. API trả `{ deleted: true }`. Room type đã xóa sẽ không xuất hiện trong list quản trị, list public và booking availability.

### 7.5 Hạng phòng còn trống cho đặt phòng

Endpoint available được thiết kế public để phục vụ booking. Khi có from/to, hệ thống lấy các room type của hotel chưa xóa, lấy inventory trong range ngày, rồi tính `availableRooms` là số nhỏ nhất trong các ngày. Nếu thiếu inventory cho một ngày hoặc min available không dương, room type được trả về với `availableRooms = 0`.

Code hiện tại tính range availability theo kiểu inclusive từ `from` đến `to`, trong khi booking dùng checkout exclusive `[checkIn, checkOut)`. Đây là điểm lệch cần chú ý khi so sánh số phòng trên UI và khả năng đặt thật.

## 8. Nghiệp vụ phòng vật lý

Room là phòng vật lý cụ thể trong khách sạn, ví dụ mã phòng 101 hoặc A203. Room thuộc một hotel và một room type.

Khi tạo room, owner/member phải có quyền hotel. Backend kiểm tra room type thuộc hotel. Lưu ý là mã phòng (code) không được trùng với bất kỳ phòng nào trong khách sạn, kể cả những phòng đã bị xóa trước đó (nếu nhập trùng mã phòng đã xóa, hệ thống sẽ báo lỗi). Sau đó hệ thống tạo room với status, cleanStatus, floor và note.

Danh sách room lọc theo hotel, bỏ room đã soft delete, có thể filter roomTypeId và q theo code/note. Update room kiểm tra room tồn tại, thuộc hotel, chưa xóa; nếu đổi code thì code mới không được trùng room khác trong hotel.

Xóa room là soft delete bằng `deletedAt` và set status thành `INACTIVE`. Nghiệp vụ public booking không dựa trực tiếp vào số lượng `Room` đang active mà dựa vào `Inventory`.

## 9. Nghiệp vụ tồn kho phòng

Inventory là nguồn sự thật để chống overbooking. Mỗi bản ghi tồn kho đại diện cho số lượng phòng của một room type trong một hotel tại một ngày cụ thể. Schema unique theo `roomTypeId`, `hotelId`, `date`.

Owner/member có thể xem inventory theo khoảng ngày. Query chuyển chuỗi `YYYY-MM-DD` thành date-only, lọc theo hotel, `deletedAt = null`, date từ from đến to, optional roomTypeId, và mặc định loại `stopSell` nếu không bật `includeStopped`.

Bulk set inventory cho phép cập nhật hoặc tạo inventory cho nhiều ngày trong một khoảng. Backend kiểm tra room type thuộc hotel, tạo danh sách ngày, rồi upsert từng ngày. Khi upsert, nếu bản ghi cũ đã soft delete thì set `deletedAt = null` trở lại. Các field có thể set gồm totalRooms, availableRooms và stopSell.

Update một inventory record chỉ update các field được truyền. Delete inventory là soft delete bằng `deletedAt`.

Frontend validator có rule `availableRooms <= totalRooms`, nhưng backend service hiện không enforce rõ rule này. Vì vậy nếu gọi API trực tiếp, vẫn cần kiểm tra lại nếu muốn đảm bảo invariant.

## 10. Nghiệp vụ tìm kiếm và chọn phòng public

Khách vào trang danh sách khách sạn public để tìm nơi lưu trú. Frontend gọi `/hotels/public` với filter q, city, date, minPrice, maxPrice và sort. Kết quả chỉ gồm hotel active, chưa xóa và có room type.

Khi khách vào chi tiết hotel, frontend lấy thông tin hotel, room types available theo ngày, reviews public và policies public. Khách chọn ngày check-in/check-out và chọn số lượng ở từng room type. UI không cho chọn quantity vượt `availableRooms` mà endpoint available trả về.

Khi bấm đặt phòng, frontend tạo URL `/booking` kèm hotel id, check-in, check-out, tổng tiền tạm tính và danh sách room type/quantity. Sang trang booking, frontend gọi lại hotel detail và availability để xác nhận lại dữ liệu hiển thị trước khi submit.

Tổng tiền và giảm giá ở frontend chỉ là preview. Backend luôn tính lại tổng tiền, discount, hoa hồng và tồn kho trong transaction.

## 11. Nghiệp vụ đặt phòng

### 11.1 Tạo booking

Tạo booking là nghiệp vụ quan trọng nhất của hệ thống. User gửi hotelId, checkIn, checkOut, thông tin khách đại diện, note, promotionCode nếu có, và danh sách item gồm roomTypeId/quantity.

Backend chuyển checkIn/checkOut thành date-only và yêu cầu `checkIn < checkOut`. Số đêm được tính theo khoảng `[checkIn, checkOut)`, tức gồm ngày check-in và các ngày giữa, không gồm ngày check-out.

Trong transaction, backend kiểm từng item và từng ngày:

- Inventory cho room type/hotel/ngày phải tồn tại.
- Inventory không được `stopSell`.
- Inventory chưa soft delete.
- `availableRooms` phải đủ quantity yêu cầu.
- Room type phải thuộc hotel và chưa bị xóa.

Sau khi kiểm đủ, backend dùng `updateMany` với điều kiện `availableRooms >= quantity` để trừ tồn. Điều kiện này chống race condition khi nhiều request đặt cùng lúc. Nếu update không thành công, request bị lỗi vì inventory đã thay đổi.

### 11.2 Tính tiền booking

Backend không tin `totalAmount` từ frontend. Với từng item, backend lấy `price_per_night` của room type, nhân số lượng và số đêm để ra line total. Tổng booking là tổng các line total.

Nếu không có promotion, discount bằng 0. Nếu có promotion, backend kiểm tra promotion trước rồi mới tính discount. Tổng cuối cùng là `totalAmount - discountAmount`, và discount không được vượt quá tổng tiền.

Booking được tạo với status `PENDING`, lưu guestName, guestPhone, guestEmail, note, checkIn, checkOut, totalAmount sau giảm, discountAmount, promotionId, items và snapshot hoa hồng.

### 11.3 Áp dụng khuyến mãi trong booking

Nếu user nhập promotion code, backend tìm promotion theo code. Promotion phải active, nằm trong thời gian hiệu lực, chưa vượt tổng usage limit, hợp lệ với hotel nếu promotion có hotelId, và đạt minBookingAmount nếu có.

Nếu promotion có `perUserLimit`, user bắt buộc phải đăng nhập. Backend đếm số booking không bị `CANCELLED` của user với promotion đó. Nếu vượt giới hạn thì từ chối.

Discount có hai kiểu. Nếu là percent, discount bằng tổng tiền nhân phần trăm và bị chặn bởi maxDiscountAmount nếu có. Nếu là fixed, discount bằng giá trị cố định. Sau đó discount bị chặn để không vượt tổng tiền. Khi booking được tạo, `usedCount` của promotion tăng ngay.

Điểm cần chú ý: usedCount tăng khi booking được tạo, không chờ payment thành công. Khi booking bị hủy, code không thấy giảm usedCount.

### 11.4 Ghi nhận hoa hồng khi booking

Khi tạo booking, backend lấy commission package đang gắn với hotel. Nếu package active, lấy `commissionRate`; nếu không có package active thì rate là 0. Rate phải nằm trong khoảng 0 đến 1.

Booking lưu `commissionRateSnapshot` và `commissionAmount`. Đây là snapshot tại thời điểm booking. Nếu sau này khách sạn đổi gói hoa hồng, booking cũ vẫn giữ số hoa hồng đã tính lúc tạo.

### 11.5 Notification khi có booking mới

Sau khi booking tạo thành công, hệ thống tạo notification `NEW_BOOKING` cho owner của hotel và các hotel members. Nếu owner cũng nằm trong members, tập recipient được dedupe bằng Set.

Notification giúp phần admin biết có booking mới mà không cần refresh thủ công liên tục.

### 11.6 Hủy booking

Booking có thể bị hủy qua endpoint cancel. Nếu booking đã `CANCELLED`, service trả lại booking hiện tại. Nếu chưa hủy, backend tính các đêm của booking và trả lại inventory bằng cách cộng `availableRooms` theo từng item/ngày, rồi set status `CANCELLED`.

Cancel được dùng cho user hủy booking của mình khi còn chờ, admin/member hủy booking trong vận hành, và cron tự hủy booking quá hạn.

### 11.7 Tự hủy booking PENDING quá hạn

Booking service có cron chạy mỗi phút. Cron tìm các booking `PENDING` được tạo quá 15 phút. Với từng booking quá hạn, hệ thống transaction set status `CANCELLED` nếu booking vẫn còn `PENDING`, sau đó trả lại inventory cho từng item/ngày.

Mục đích là giữ phòng tạm thời cho khách trong 15 phút chờ thanh toán. Nếu khách không thanh toán thành công trong khoảng này, phòng được trả lại để người khác đặt.

### 11.8 Xem booking

User có thể xem booking của chính mình qua `/bookings/me` và `/bookings/me/:bookingId`. Admin/owner/member có thể xem danh sách booking theo hotel, filter theo status/date và xem detail booking thuộc hotel.

Các response thường include hotel, items, room type, payment, review, guests và check-in tùy endpoint.

### 11.9 Chuyển trạng thái booking

Code có state machine cho booking status:

- `PENDING` có thể chuyển sang `CONFIRMED` hoặc `CANCELLED`.
- `CONFIRMED` có thể chuyển sang `CHECKED_IN` hoặc `CANCELLED`.
- `CHECKED_IN` có thể chuyển sang `COMPLETED`.
- `COMPLETED`, `CANCELLED` và `NO_SHOW` là trạng thái cuối hoặc gần cuối, không có nhiều chuyển tiếp trong service.

Payment success tự chuyển booking sang `CONFIRMED`. Check-in tự chuyển booking sang `CHECKED_IN`. Sau khi khách hoàn tất lưu trú, admin/staff chuyển sang `COMPLETED`, và chỉ booking `COMPLETED` mới được review.

## 12. Nghiệp vụ thanh toán VNPAY

### 12.1 Tạo URL thanh toán

Khi user muốn thanh toán booking `PENDING`, frontend gọi API tạo VNPAY payment URL. Backend tìm booking, tạo `merchantTxnRef` dạng `BK_{bookingId}_{timestamp}`, tạo bản ghi `Payment` provider `VNPAY`, status ban đầu, amount theo booking, rồi ký params VNPAY để tạo URL redirect.

Frontend nhận `paymentUrl` và gán `window.location.href` để chuyển user sang cổng thanh toán.

Điểm cần chú ý: service tạo URL thanh toán hiện không kiểm rõ booking thuộc user đang gọi. Nếu endpoint không có check quyền ở controller/service, đây là rủi ro truy cập booking của người khác.

### 12.2 Return từ VNPAY

Sau khi thanh toán, VNPAY redirect về return URL. Backend verify chữ ký, lấy `vnp_TxnRef`, tìm payment theo `merchantTxnRef`, ghi `PaymentEvent` type `RETURN` để audit.

Nếu checksum sai, thiếu transaction ref hoặc không tìm thấy payment, backend trả kết quả failed. Nếu payment đã ở trạng thái cuối thì logic idempotent không ghi đè lung tung.

Nếu VNPAY báo thành công, backend cập nhật payment `SUCCEEDED`, lưu transaction no, bank code, pay date, response code, transaction status và chuyển booking sang `CONFIRMED`. Sau đó gửi email payment success một lần. Nếu không thành công, payment chuyển `FAILED`.

### 12.3 IPN từ VNPAY

IPN cũng verify checksum, tìm payment theo transaction ref, kiểm amount gửi về có khớp amount của payment không, kiểm trạng thái cuối để idempotent, ghi `PaymentEvent` type `IPN`, rồi cập nhật payment/booking tương tự return.

Nếu success, booking được `CONFIRMED`. Nếu failed, payment `FAILED`. IPN trả mã theo chuẩn VNPAY như checksum failed, order not found, amount invalid hoặc success.

### 12.4 Email sau thanh toán

Khi payment success, hệ thống gửi email thành công cho guestEmail hoặc email user liên quan. Trước khi gửi, service kiểm tra đã có `PaymentEvent` type `MAIL_PAYMENT_SUCCEEDED` chưa để tránh gửi lặp. Nếu gửi thất bại, event failed cũng được ghi lại.

## 13. Nghiệp vụ check-in và lưu trú

Check-in chỉ dành cho người có quyền quản lý hotel của booking. Service tìm booking, kiểm quyền hotel thông qua booking, và không cho check-in booking đã `CANCELLED`.

Payload check-in gồm primary guest và companions. Service normalize danh sách khách, trong đó primary guest là bắt buộc ở frontend, companions là optional. Dữ liệu guest có fullName, email, phone, dateOfBirth, gender, idNumber và nationality.

Khi check-in, backend upsert bản ghi `CheckIn` theo bookingId. Nếu đã có check-in record thì cập nhật; nếu chưa có thì tạo mới. Sau đó xóa danh sách `BookingGuest` cũ và tạo lại danh sách guest theo payload mới. Booking được chuyển sang `CHECKED_IN`.

Admin/member có thể xem thông tin check-in của booking, gồm check-in record và danh sách guest. Sau lưu trú, booking được chuyển tiếp sang `COMPLETED` bằng luồng update status.

## 14. Nghiệp vụ đánh giá

### 14.1 Tạo review

User chỉ được review booking của chính mình, thuộc đúng hotel, và booking phải có status `COMPLETED`. Mỗi booking chỉ có một review vì `Review.bookingId` unique.

Nếu user chọn ảnh, backend chỉ chấp nhận ảnh nằm trong gallery của chính user. Nếu có imageId không thuộc user hoặc không tồn tại, request bị từ chối.

Review lưu hotelId, userId, bookingId, rating, title, content và các ảnh review. Nếu booking đã có review, lỗi unique được chuyển thành BadRequest với thông báo booking đã được review.

### 14.2 Review public

Danh sách review public của hotel chỉ hiển thị review chưa soft delete và `isHidden = false`. Danh sách có phân trang, sort mới nhất trước và include thông tin user public cùng ảnh review.

### 14.3 Review của tôi

User có trang xem đánh giá của chính mình. Danh sách chỉ lấy các đánh giá của user đó, bỏ qua các đánh giá đã xóa, và kèm theo thông tin khách sạn. (Lưu ý: Dù theo logic cần có thông tin đơn đặt phòng liên quan, nhưng hiện tại hệ thống chưa trả về dữ liệu đơn đặt phòng trong danh sách này).

User có thể update review của chính mình. Service kiểm tra review thuộc user và chưa bị xóa rồi update rating/title/content.

### 14.4 Kiểm duyệt đánh giá (Moderation review)

Chủ khách sạn hoặc nhân viên có thể xem danh sách toàn bộ đánh giá để kiểm duyệt. Danh sách này bao gồm cả những đánh giá đang bị ẩn, và cho phép tìm kiếm theo tiêu đề hoặc nội dung. (Lưu ý: Hiện tại chức năng lọc danh sách theo số sao đánh giá hay theo trạng thái ẩn/hiện vẫn chưa được hỗ trợ trong hệ thống). Moderator có thể cập nhật trạng thái `isHidden` để ẩn hoặc hiện đánh giá ra công chúng.

Owner/member cũng có thể remove review theo hotel. Remove là soft delete bằng `deletedAt`.

## 15. Nghiệp vụ khuyến mãi

Promotion có code unique, kiểu giảm giá percent hoặc fixed, giá trị giảm, max discount, min booking amount, total usage limit, per user limit, thời gian start/end, isActive và optional hotelId.

Admin có thể tạo promotion. Code hiện tại có comment về việc kiểm quyền theo hotel hoặc global, nhưng phần create thực tế không enforce userId và cũng không lưu `hotelId` từ DTO vào data create. Vì vậy promotion tạo ra có xu hướng là global theo code hiện tại.

Danh sách admin có filter/search/pagination. Danh sách public chỉ trả promotion active, đang trong thời gian hiệu lực, chưa vượt usage limit và có thể search theo code. Phần filter hotelId trong public hiện bị comment.

Update promotion kiểm tra nếu promotion có hotelId thì user phải là owner/member của hotel; nếu promotion global thì user phải là admin. Remove cũng kiểm tra tương tự. Điều này tạo ra khác biệt: create đang lỏng hơn update/remove.

Khi booking dùng promotion, backend mới validate đầy đủ hotel, thời gian, usage, per user limit, min amount và tính discount thật.

## 16. Nghiệp vụ gói hoa hồng

Commission package mô tả mức hoa hồng hệ thống thu từ hotel. Package có code unique, name, commissionRate, packageType, billingCycle, isActive. Rate là số từ 0 đến 1.

Admin có thể tạo, list, xem detail, update, deactivate và gán package cho hotel. Khi gán package cho hotel, hotel lưu `commissionPackageId`.

Khi booking được tạo, hệ thống snapshot rate từ package active của hotel vào booking. `commissionAmount` được tính bằng final total nhân rate. Dashboard hoa hồng/revenue chart chỉ tính booking `COMPLETED`.

Điểm quan trọng là hoa hồng không tính động theo package hiện tại khi báo cáo booking cũ, mà dựa trên snapshot trong booking.

## 17. Nghiệp vụ dashboard

Dashboard cung cấp thống kê cho admin hoặc người quản lý hotel. Các API dashboard lấy số liệu booking, doanh thu, review mới nhất, booking mới nhất và biểu đồ doanh thu.

Khi có hotelId, số liệu được scope theo hotel. Khi không có hotelId, tùy quyền và endpoint, số liệu có thể là toàn hệ thống hoặc theo danh sách hotel user được quản lý.

Doanh thu và hoa hồng có xu hướng dựa trên booking đã hoàn thành hoặc thanh toán thành công tùy service cụ thể. Phần commission revenue chart tính booking `COMPLETED`.

## 18. Nghiệp vụ chính sách khách sạn

Hotel policy là các chính sách hiển thị trên trang chi tiết hotel và quản trị trong admin. Policy có type, title, content, enabled và order. Schema unique theo hotelId/type, nên mỗi hotel chỉ có một policy cho mỗi loại type.

Public list chỉ trả policy enabled, sort theo order tăng dần. Admin list trả tất cả policy của hotel, cũng sort theo order.

Tạo, cập nhật, xem detail và xóa policy yêu cầu user là owner/member của hotel. Khi tạo, order mặc định là 0 nếu không truyền. Code kiểm tra order không được trùng với policy khác trong cùng hotel. Khi update nếu đổi order, order mới cũng không được trùng.

Xóa policy hiện là hard delete, khác với nhiều domain khác đang dùng soft delete.

## 19. Nghiệp vụ tin tức

News phục vụ CMS tin tức/blog. Admin tạo news với title, content, summary, status và imageIds. Backend slugify title bằng cách lowercase, bỏ dấu, đổi ký tự không phải chữ số thành `-`. Nếu slug trùng, append timestamp.

News mặc định status `DRAFT`. Nếu tạo hoặc update sang `PUBLISHED`, backend set `publishedAt = now`. Nếu status không published thì `publishedAt = null`.

Ảnh của news lấy từ gallery của user hiện tại. Backend kiểm imageIds phải thuộc user, sau đó lưu URL vào `NewsImage`. Khi update nếu truyền imageIds, toàn bộ ảnh cũ bị replace.

Public list/detail chỉ hiển thị news `PUBLISHED` và chưa soft delete. Admin list/detail có thể xem cả draft/archived và filter status/q. Xóa news là soft delete bằng `deletedAt`.

## 20. Nghiệp vụ banner

Banner phục vụ nội dung quảng bá trên frontend. Banner có title, subtitle, linkType, linkUrl hoặc link target, position, isActive, startAt, endAt và images.

Khi tạo banner, backend kiểm nếu có startAt/endAt thì startAt phải nhỏ hơn hoặc bằng endAt. Position không được trùng với banner khác. Nếu không truyền position, mặc định là 0. Images được tạo từ danh sách URL trong payload.

Update banner cũng kiểm date range và position unique nếu đổi position. Nếu payload có images, toàn bộ ảnh banner cũ bị replace bằng danh sách mới.

Public banner chỉ trả banner active, startAt null hoặc đã bắt đầu, endAt null hoặc chưa kết thúc, sort theo position tăng dần. Admin list trả tất cả banner sort mới nhất trước. Xóa banner là hard delete, ảnh banner bị xóa theo quan hệ.

## 21. Nghiệp vụ liên hệ hỗ trợ

Trang contact public cho phép khách gửi thông tin liên hệ. Payload bắt buộc có name/message và phải có ít nhất email hoặc phone. Backend lưu contact message với status ban đầu, ip, userAgent, subject, message và thông tin liên hệ.

Sau khi lưu, backend gửi mail notification cho support/admin. Sau đó tìm user có role `ADMIN`, `OWNER`, `STAFF` và tạo notification type `SYSTEM` cho họ với nội dung có contact message mới.

Admin có thể list contact theo status, search theo name/email/phone/subject/message, xem detail và update status, handledById, note. Status gồm `NEW`, `IN_PROGRESS`, `RESOLVED`, `SPAM`.

Điểm cần chú ý: comment nói mail là best-effort, nhưng code create gọi mail trực tiếp không bọc try/catch rõ ràng, nên lỗi gửi mail có thể làm request contact fail.

## 22. Nghiệp vụ notification

Notification là thông báo nội bộ cho user. Mỗi notification gắn userId, optional hotelId/bookingId, type, title, message, isRead và readAt.

User có thể list notification của chính mình, xem unread count, mark một notification là read, mark all read và delete notification. Tất cả thao tác đều filter theo userId, nghĩa là user không thể đọc hoặc xóa notification của người khác nếu gọi API đúng controller.

Các nghiệp vụ tự tạo notification gồm booking mới cho owner/member và contact mới cho nhóm admin/owner/staff.

Frontend có khu vực notification, unread count được refetch định kỳ khoảng 30 giây.

## 23. Nghiệp vụ upload, gallery và ảnh

Cloudinary module xử lý upload file lên Cloudinary. Upload generic vào folder `stayra`. User có thể tạo folder gallery trong DB, upload ảnh vào folder, xem danh sách folder DB và xem ảnh theo folder.

Khi upload image vào folder, backend tạo folder DB nếu chưa có, upload ảnh lên Cloudinary, rồi tạo `ImageGallery` với publicId, url, secureUrl, userId và folderId. Khi lấy DB folders hoặc images, backend filter theo userId, nghĩa là user chỉ thấy gallery của mình.

Gallery được dùng lại trong news và review. News/review không upload ảnh trực tiếp mà nhận imageIds từ gallery, sau đó backend xác nhận ảnh thuộc user hiện tại.

Ngoài gallery chung còn có ảnh domain riêng: `HotelImage`, `RoomTypeImage`, `NewsImage`, `BannerImage`, `ReviewImage`, và `ImageAsset` cho avatar.

## 24. Nghiệp vụ nội dung public

Trang chủ và các trang public dùng banner, hotel public, news public, review public và policy public để hiển thị nội dung cho khách.

Trang news public chỉ thấy bài published. Trang banner public chỉ thấy banner active trong thời gian hiệu lực. Trang hotel detail chỉ nên hiển thị hotel chưa xóa, room type chưa xóa, review không bị ẩn và policy enabled.

Trang partner là trang public giới thiệu đối tác, không thấy nghiệp vụ backend riêng ngoài điều hướng public.

## 25. Nghiệp vụ frontend

### 25.1 AuthProvider và axios

Frontend giữ access token trong cookie `accessToken`. Axios request interceptor đọc cookie này và gắn `Authorization: Bearer ...` cho request. Nếu API trả 401, axios tự gọi `/auth/refresh`. Nếu refresh thành công, access token mới được lưu lại và request ban đầu có thể tiếp tục. Nếu refresh thất bại, frontend xóa token và redirect về login.

Nếu API trả 403, frontend hiển thị toast lỗi quyền và redirect `/forbidden`.

`AuthProvider` chịu trách nhiệm load user từ `/users/me`, login, register, logout, forgot password, reset password và update state user.

### 25.2 Route guard frontend

`proxy.ts` chặn `/admin` và `/me` nếu thiếu `accessToken`. Nếu user đã login mà vào login page, frontend redirect về `/me`.

`AdminRoute` trong layout admin chỉ kiểm user tồn tại và `roles.length > 0`, chưa kiểm role name cụ thể như ADMIN. Menu admin được lọc bằng `allowedActions`, nhưng route guard admin vẫn khá rộng.

### 25.3 Luồng đặt phòng trên frontend

Frontend public hotel detail cho user chọn ngày, số phòng và room type. Khi sang trang booking, query string giữ danh sách phòng. Trang booking fetch lại hotel và availability, hiển thị form guestName, guestPhone, guestEmail, note, promotionCode.

Promotion public search được gọi khi user nhập code. Frontend tính discount preview theo percent/fixed, minBookingAmount và maxDiscountAmount. Khi submit, frontend gửi booking request. Sau khi booking thành công, frontend hiện alert và redirect `/`; hiện chưa tự chuyển ngay sang trang thanh toán.

User vào `/me/my-bookings` để thấy booking của mình. Nếu booking còn `PENDING`, user có thể hủy hoặc tạo payment URL VNPAY.

### 25.4 Luồng payment result trên frontend

Trang `/payment-result` đọc query `payment_status` và `booking_id`. Sau đó gọi `/bookings/me/:bookingId` để hiển thị booking. Nếu payment failed và booking vẫn `PENDING`, UI cho retry bằng cách quay lại booking detail để thanh toán lại.

### 25.5 Luồng admin trên frontend

Admin sidebar hiển thị menu theo action key. Các nhóm màn hình admin gồm dashboard, hotels, member hotels, room types, rooms, inventory, bookings, reviews, promotions, commissions, users, roles, permissions, actions, amenities, news, contacts, policies và settings/banner.

Các màn hình admin dùng React Query queries/mutations theo từng feature. Form dùng Zod validator. Nhiều validator frontend chặt hơn backend, ví dụ inventory check `availableRooms <= totalRooms`, promotion percent không quá 100, banner bắt buộc ít nhất một ảnh, contact phải có email hoặc phone.

## 26. Các quy tắc nghiệp vụ cốt lõi

Các rule quan trọng nhất đang được code thể hiện:

- Email local phải được verify trước khi login.
- Refresh token luôn gắn với session và được rotate.
- User có quyền admin UI dựa trên `allowedActions`.
- Quyền thật ở backend chỉ chắc chắn khi route có guard phù hợp.
- Hotel public phải active, chưa xóa và có room type.
- User quản lý hotel khi là owner hoặc member.
- Room type name unique trong một hotel.
- Room code unique trong một hotel.
- Inventory theo từng ngày là nguồn chống overbooking.
- Booking chỉ hợp lệ khi `checkIn < checkOut`.
- Số đêm booking tính theo `[checkIn, checkOut)`.
- Booking tạo ra giữ tồn ngay khi status `PENDING`.
- Booking `PENDING` quá 15 phút bị cron tự hủy và trả tồn.
- Payment success chuyển booking sang `CONFIRMED`.
- Check-in chuyển booking sang `CHECKED_IN`.
- Booking `CHECKED_IN` có thể chuyển sang `COMPLETED`.
- Chỉ booking `COMPLETED` mới được review.
- Một booking chỉ có một review.
- Review hidden không hiển thị public.
- Promotion discount không được vượt tổng tiền.
- Promotion per user limit yêu cầu user đăng nhập.
- Commission được snapshot lúc booking tạo.
- News public chỉ hiển thị `PUBLISHED`.
- Banner public chỉ hiển thị active và trong thời gian hiệu lực.
- Notification user-facing luôn scope theo userId.

## 27. Các điểm lệch và rủi ro nghiệp vụ trong code hiện tại

Một số điểm dưới đây không nhất thiết là lỗi đã xảy ra, nhưng là hành vi hoặc rủi ro đọc được từ code:

- `schema.prisma` giàu hơn migrations, nhiều model mới chưa được migration cũ bao phủ đầy đủ.
- Logout bình thường chỉ clear cookie, phần revoke session DB đang bị comment.
- Logout all dùng `req.user.sub` trong khi JWT strategy trả `id`.
- Resend verification email truyền token raw cho mail service, khác luồng register truyền verify URL đầy đủ.
- Một số controller có `@Action` nhưng không gắn `ActionGuard`, nên action permission có thể chưa enforce.
- `PermissionsGuard` chỉ có tác dụng nếu route gắn `@Permissions`.
- Frontend admin route chỉ yêu cầu user có ít nhất một role, không kiểm role cụ thể.
- Frontend allowedActions chỉ ẩn/hiện UI, không bảo vệ API nếu backend thiếu guard.
- Frontend có wrapper update/delete user nhưng backend chưa thấy endpoint tương ứng.
- `Payment.createVnpayPaymentUrl` không thấy kiểm rõ booking thuộc user đang gọi.
- VNPAY return ở nhánh idempotent có thể thiếu `bookingId` trong response.
- Promotion `usedCount` tăng khi booking tạo, không chờ thanh toán thành công.
- Cancel booking không thấy decrement promotion `usedCount`.
- `Promotion.create` không lưu `hotelId` dù DTO có field và update/remove có logic phân quyền theo hotel/global.
- `RoomType.getAvailableRoomTypes` dùng date range inclusive, còn booking dùng checkout exclusive.
- `Hotel.listPublicHotels` filter theo date chưa nghiêm bằng booking transaction, có thể chỉ là filter sơ bộ.
- Backend inventory chưa enforce rõ `availableRooms <= totalRooms`, frontend có enforce.
- `Policy.remove` hard delete, khác với soft delete ở hotel, room type, room, inventory, review, news.
- `ListUsersQuery.sortBy = fullName` có thể lỗi vì DB không có field `fullName`.
- Contact service gọi gửi mail trực tiếp, nên nếu mail lỗi có thể làm tạo contact lỗi.
- Schema có `HotelMemberRole` nhưng model `HotelMember` chưa có field role, nên phân vai nội bộ khách sạn chưa thật sự tồn tại trong DB.

## 28. Tóm tắt theo hành trình end-to-end

### 28.1 Khách đặt phòng

Khách tìm hotel public, chọn hotel active, chọn ngày và room type còn phòng. Frontend hiển thị số phòng còn dựa trên inventory. Khách nhập thông tin đại diện và mã khuyến mãi nếu có. Backend kiểm tra lại ngày, tồn kho, room type, promotion, tính tiền thật, trừ tồn, tạo booking `PENDING`, snapshot hoa hồng và gửi notification cho khách sạn. Nếu khách thanh toán VNPAY thành công trong 15 phút, booking thành `CONFIRMED`. Nếu không, cron tự hủy và trả phòng.

### 28.2 Khách lưu trú

Sau khi booking confirmed, owner/member khách sạn xem booking trong admin. Khi khách đến, nhân sự check-in bằng cách nhập primary guest và companions. Hệ thống lưu check-in record, danh sách khách lưu trú và chuyển booking sang `CHECKED_IN`. Khi hoàn tất lưu trú, booking chuyển `COMPLETED`. Từ lúc đó user mới có thể review.

### 28.3 Quản trị khách sạn

User tạo hotel và trở thành owner/member. Owner/member cấu hình thông tin hotel, ảnh, members, amenities dùng cho room type, room types, rooms vật lý, inventory theo ngày, policies, review moderation và booking operation. Hotel muốn xuất hiện public cần active, chưa xóa và có room type. Khả năng đặt phòng thực tế phụ thuộc inventory.

### 28.4 Quản trị hệ thống

Admin quản lý role, permission, action policy, user roles, hotels, commission packages, promotions global, news, banners, contacts và dashboard tổng hợp. Frontend admin menu dựa trên action permissions; backend chỉ enforce chắc chắn ở những route có guard phù hợp.

### 28.5 Nội dung và hỗ trợ

Admin tạo news published để hiển thị public, tạo banner active trong thời gian hiệu lực, xử lý contact message từ khách và nhận notification nội bộ. User có gallery riêng để tái sử dụng ảnh cho avatar, news và review.
