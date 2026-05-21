# Product Requirements Document - Hotel Booking

## 1. Metadata

| Field | Value |
| --- | --- |
| Document type | PRD |
| Product | Hotel Booking |
| Language | Vietnamese |
| Scope | Product requirements only |
| Tech Spec status | Pending user approval |
| Primary roles | Customer, Admin |

## 2. Tổng Quan Dự Án

### 2.1 Mục Tiêu Cốt Lõi

- Xây dựng hệ thống web đặt phòng khách sạn cho phép khách hàng:
  - Tìm kiếm khách sạn và phòng theo địa điểm, ngày lưu trú, sức chứa.
  - Xem chi tiết khách sạn, phòng, hình ảnh, tiện ích.
  - Tạo booking, nhận mã đặt phòng, xem lịch sử đặt phòng.
  - Tra cứu booking theo mã xác nhận.
  - Hủy booking theo điều kiện hợp lệ.
- Cung cấp khu vực quản trị cho Admin để:
  - Quản lý tài khoản người dùng.
  - Quản lý khách sạn, phòng, hình ảnh, tiện ích.
  - Quản lý booking, check-in, check-out, hủy booking.
  - Gán số phòng thực tế khi khách nhận phòng.

### 2.2 Phạm Vi MVP

| Scope ID | Included | Description |
| --- | --- | --- |
| MVP-001 | Yes | Đăng ký, đăng nhập, đăng xuất, đổi mật khẩu, quản lý thông tin cá nhân |
| MVP-002 | Yes | Tìm kiếm khách sạn/phòng, xem danh sách, xem chi tiết |
| MVP-003 | Yes | Kiểm tra phòng trống theo ngày, sức chứa, số lượng còn lại |
| MVP-004 | Yes | Tạo booking, sinh mã booking, lưu trạng thái `BOOKED` |
| MVP-005 | Yes | Xem lịch sử booking, tra cứu booking theo mã |
| MVP-006 | Yes | Hủy booking, ghi nhận lý do hủy |
| MVP-007 | Yes | Admin quản lý user, hotel, room, amenity, booking |
| MVP-008 | Partial | Thanh toán chỉ ở mức mô phỏng/xác nhận thủ công nếu có |
| MVP-009 | No | Quên mật khẩu |
| MVP-010 | No | Thống kê doanh thu |
| MVP-011 | No | Gợi ý cá nhân hóa, AI recommendation |
| MVP-012 | No | Review, policy engine, thanh toán thật qua VNPAY/MoMo/ngân hàng |
| MVP-013 | No | Chấm điểm/xử phạt đối tác, cơ chế chống gian lận, commission/hoa hồng marketplace |
| MVP-014 | No | Chatbot/FAQ tự động, hỗ trợ khách hàng đa kênh, SLA hỗ trợ |
| MVP-015 | No | Khuyến mãi, loyalty/tích điểm, ưu đãi thành viên |

### 2.3 Benchmark Và Product Direction Từ Hệ Thống Tương Tự

Nguồn chương 2 phân tích Booking.com và Traveloka như hai hệ thống marketplace tiêu biểu. SDD dùng phần này để giữ lại reasoning sản phẩm, không mặc định đưa toàn bộ vào MVP.

| Benchmark Insight | Ý nghĩa cho MVP hiện tại | Roadmap/Open Policy |
| --- | --- | --- |
| Booking.com mạnh ở danh mục lưu trú lớn, bộ lọc theo giá/tiện nghi/rating/vị trí và công cụ quản lý đối tác. | MVP ưu tiên search theo location/date/capacity, quản lý hotel/room/booking cho Admin, và cấu trúc dữ liệu đủ mở rộng filter. | Bổ sung filter `priceMin/priceMax`, `amenityIds`, `starRating`, `reviewScore`, sort theo giá/rating/vị trí khi có dữ liệu review/location chuẩn. |
| Booking.com có chính sách đặt/hủy linh hoạt và các rate plan khác nhau. | MVP chỉ có state machine hủy cơ bản: owner/Admin được hủy khi booking chưa hoàn tất/chưa hủy. | Nếu thêm policy engine, cần mô hình `cancellation_policy`, `rate_plan`, non-refundable/free-cancellation/pay-at-property và tác động refund/payment. |
| Traveloka mạnh ở địa phương hóa Đông Nam Á, ví điện tử, chuyển khoản, khuyến mãi và trải nghiệm tối giản. | MVP chưa xử lý thanh toán thật; UI cần giữ luồng đặt phòng đơn giản và thông báo lỗi rõ. | Payment/localization roadmap gồm VietQR, MoMo, ví điện tử, chuyển khoản ngân hàng, thanh toán tại nơi lưu trú, promotion và loyalty. |
| Cả hai hệ thống đều có nhu cầu kiểm soát chất lượng đối tác và chống gian lận. | MVP chỉ kiểm soát owner checks, trạng thái active và Admin operations. | Cần partner quality score, audit log, xử lý đối tác tự ý hủy đơn, tạm khóa hotel/partner, chính sách khiếu nại. |
| Hệ thống lớn thường cần support/chăm sóc khách hàng đa kênh. | MVP chưa có workflow support riêng. | Roadmap có FAQ/chính sách, chatbot hỗ trợ tự động, kênh chat/phone/email và SLA phản hồi. |

## 3. Đối Tượng Người Dùng

| Persona ID | Role | Description | Primary Goals |
| --- | --- | --- | --- |
| PER-001 | Customer | Người dùng tìm và đặt phòng khách sạn. Bao gồm trạng thái chưa đăng nhập khi chỉ xem/tìm kiếm và trạng thái đã đăng nhập khi đặt/hủy/quản lý booking. | Tìm phòng phù hợp, đặt phòng nhanh, theo dõi/hủy booking, quản lý hồ sơ cá nhân |
| PER-002 | Admin | Người quản trị vận hành hệ thống và quản lý dữ liệu khách sạn/phòng/booking. Trong tài liệu hiện tại, Admin vừa có quyền quản trị hệ thống vừa có quyền quản lý khách sạn thuộc sở hữu của mình. | Quản lý dữ liệu vận hành, đảm bảo booking đúng trạng thái, tránh trùng phòng, quản lý tài khoản |

## 4. Vai Trò Và Quyền Truy Cập

| Module | Customer | Admin | Notes |
| --- | --- | --- | --- |
| Đăng ký | Create own account | Not required | Account mới mặc định role `CUSTOMER` |
| Đăng nhập | Yes | Yes | Login trả JWT và thông tin user |
| Profile | View/update own profile | View/update own profile | Không xem/sửa profile người khác trừ module quản lý user |
| Đổi mật khẩu | Own account | Own account | Bắt buộc nhập đúng mật khẩu cũ |
| Khách sạn | View/search/detail | CRUD owned hotels | Admin phải có quyền sở hữu khi sửa/xóa |
| Phòng | View/search/detail/book | CRUD rooms in owned hotels | Admin phải có quyền sở hữu hotel chứa phòng |
| Booking | Create/view/cancel own booking | View all, update status, cancel | Customer chỉ thao tác booking của mình |
| User management | No | View/list, lock, unlock | Bắt buộc quyền Admin |
| Amenity | View assigned amenities | CRUD catalog, assign/remove | Không xóa amenity đang được sử dụng |

## 5. Yêu Cầu Chức Năng

### 5.1 Customer Requirements

| FR ID | Use Case | Requirement | Acceptance Criteria | Priority |
| --- | --- | --- | --- | --- |
| FR-CUS-AUTH-001 | Đăng ký tài khoản | Customer có thể tạo tài khoản bằng họ tên, email, số điện thoại, ngày sinh, mật khẩu. | Email không được trùng; dữ liệu bắt buộc phải hợp lệ; mật khẩu được hash; tài khoản mới có role `CUSTOMER`; tài khoản ở trạng thái active sau khi tạo. | Must |
| FR-CUS-AUTH-002 | Đăng nhập | Customer có thể đăng nhập bằng email và mật khẩu. | Hệ thống kiểm tra email tồn tại, mật khẩu đúng, tài khoản active; nếu hợp lệ trả JWT và user info; nếu sai hiển thị lỗi; nếu bị khóa hiển thị lỗi tài khoản bị khóa. | Must |
| FR-CUS-AUTH-003 | Đăng xuất | Customer có thể đăng xuất khỏi hệ thống. | Token/session phía client bị xóa; người dùng được chuyển về trạng thái chưa đăng nhập. | Must |
| FR-CUS-PROFILE-001 | Xem profile | Customer có thể xem thông tin cá nhân. | Hệ thống lấy user từ JWT/context và hiển thị đúng thông tin của tài khoản hiện tại. | Must |
| FR-CUS-PROFILE-002 | Cập nhật profile | Customer có thể cập nhật thông tin cá nhân. | Hệ thống validate dữ liệu; cập nhật thành công khi hợp lệ; giữ dữ liệu cũ và hiển thị lỗi khi không hợp lệ. | Must |
| FR-CUS-PROFILE-003 | Đổi mật khẩu | Customer có thể đổi mật khẩu. | Bắt buộc nhập đúng mật khẩu cũ; mật khẩu mới không trùng mật khẩu cũ; mật khẩu mới được hash trước khi lưu. | Must |
| FR-CUS-PROFILE-004 | Xóa tài khoản cá nhân | Customer có thể yêu cầu xóa hoặc vô hiệu hóa tài khoản. | Hệ thống yêu cầu xác nhận; sau khi xử lý tài khoản bị vô hiệu hóa/xóa theo chính sách; người dùng bị đăng xuất. | Should |
| FR-CUS-HOTEL-001 | Xem danh sách khách sạn | Customer có thể xem danh sách khách sạn. | Danh sách hiển thị thông tin tóm tắt gồm tên, địa điểm, ảnh đại diện, rating nếu có; hỗ trợ trạng thái danh sách trống. | Must |
| FR-CUS-HOTEL-002 | Xem chi tiết khách sạn | Customer có thể xem chi tiết một khách sạn. | Hiển thị thông tin khách sạn, ảnh, mô tả, liên hệ, sao, tiện ích, danh sách phòng; nếu ID không tồn tại trả lỗi 404 hoặc màn hình không tìm thấy. | Must |
| FR-CUS-HOTEL-003 | Tìm kiếm khách sạn | Customer có thể tìm khách sạn theo địa điểm và ngày check-in/check-out. | Hệ thống validate ngày; ngày check-out phải sau check-in; kết quả chỉ trả khách sạn phù hợp; nếu không có kết quả hiển thị trạng thái rỗng. | Must |
| FR-CUS-ROOM-001 | Xem danh sách phòng | Customer có thể xem danh sách phòng trong hệ thống hoặc theo khách sạn. | Hiển thị ảnh, tên phòng, loại phòng, giá, sức chứa, mô tả ngắn; hỗ trợ phân trang hoặc trạng thái danh sách trống. | Must |
| FR-CUS-ROOM-002 | Xem chi tiết phòng | Customer có thể xem chi tiết phòng. | Hiển thị ảnh, tên, loại phòng, giá, sức chứa, số lượng, mô tả, tiện ích, form đặt phòng; nếu phòng không tồn tại trả 404. | Must |
| FR-CUS-ROOM-003 | Tìm phòng theo từ khóa | Customer có thể tìm phòng bằng từ khóa. | Hệ thống lọc theo tên/mô tả hoặc trường liên quan; nếu không có kết quả hiển thị thông báo phù hợp. | Should |
| FR-CUS-ROOM-004 | Tìm phòng trống theo ngày | Customer có thể kiểm tra phòng trống theo check-in, check-out, số khách, số lượng phòng. | Hệ thống loại trừ booking trạng thái `BOOKED` hoặc `CHECKED_IN` có khoảng ngày giao nhau; chỉ trả phòng đủ sức chứa và còn số lượng. | Must |
| FR-CUS-BOOK-001 | Tạo booking mới | Customer có thể tạo booking từ trang chi tiết phòng hoặc form đặt phòng. | Bắt buộc đăng nhập; validate ngày; kiểm tra hotel/room hợp lệ; kiểm tra còn phòng; tính tổng tiền; sinh mã booking duy nhất; lưu booking trạng thái `BOOKED`; hiển thị thông tin booking sau khi tạo. | Must |
| FR-CUS-BOOK-002 | Xem booking success | Customer thấy màn hình đặt phòng thành công sau khi tạo booking. | Hiển thị mã booking, thông tin phòng/khách sạn, ngày lưu trú, tổng tiền, trạng thái. | Must |
| FR-CUS-BOOK-003 | Xem lịch sử booking | Customer có thể xem danh sách booking của chính mình. | Danh sách được lọc theo current user; hiển thị mã booking, ngày, khách sạn/phòng, trạng thái; nếu trống hiển thị thông báo. | Must |
| FR-CUS-BOOK-004 | Tra cứu booking theo mã | Customer có thể tìm booking bằng mã xác nhận. | Nếu mã tồn tại và có quyền xem, hiển thị chi tiết booking; nếu mã không tồn tại hiển thị lỗi. | Must |
| FR-CUS-BOOK-005 | Xem chi tiết booking | Customer có thể xem chi tiết một booking. | Hiển thị mã booking, trạng thái, ngày check-in/check-out, phòng, khách sạn, tổng tiền, số khách, yêu cầu đặc biệt, lý do hủy nếu có. | Must |
| FR-CUS-BOOK-006 | Hủy booking | Customer có thể hủy booking của chính mình khi còn hợp lệ. | Chỉ chủ booking hoặc Admin được hủy; không cho hủy booking `CHECKED_OUT` hoặc `CANCELLED`; ghi nhận lý do hủy; cập nhật trạng thái `CANCELLED`; giải phóng khả dụng phòng. | Must |

### 5.2 Admin Requirements

| FR ID | Use Case | Requirement | Acceptance Criteria | Priority |
| --- | --- | --- | --- | --- |
| FR-ADM-AUTH-001 | Đăng nhập Admin | Admin có thể đăng nhập vào khu vực quản trị. | Hệ thống xác thực email/password, trạng thái active và role Admin; nếu hợp lệ chuyển vào dashboard quản trị. | Must |
| FR-ADM-DASH-001 | Dashboard quản trị | Admin có dashboard truy cập nhanh các module quản trị. | Dashboard có các module: quản lý tài khoản, khách sạn, phòng, tiện nghi, đặt phòng. | Should |
| FR-ADM-USER-001 | Xem danh sách người dùng | Admin có thể xem danh sách user. | Chỉ Admin được truy cập; danh sách hiển thị thông tin user và trạng thái active/locked. | Must |
| FR-ADM-USER-002 | Khóa tài khoản | Admin có thể khóa tài khoản user. | Hệ thống tìm user theo ID; nếu tồn tại chuyển trạng thái active sang false; user bị khóa không đăng nhập được. | Must |
| FR-ADM-USER-003 | Mở khóa tài khoản | Admin có thể mở khóa tài khoản user. | Hệ thống tìm user theo ID; nếu tồn tại chuyển trạng thái active sang true; user có thể đăng nhập lại. | Must |
| FR-ADM-HOTEL-001 | Xem khách sạn của tôi | Admin có thể xem danh sách khách sạn mình sở hữu. | Hệ thống lọc theo owner/current admin; nếu chưa có khách sạn hiển thị trạng thái trống. | Must |
| FR-ADM-HOTEL-002 | Thêm khách sạn | Admin có thể tạo khách sạn mới. | Bắt buộc quyền Admin; nhập tên, địa chỉ/location, mô tả, liên hệ, sao; bắt buộc ảnh; upload ảnh lên Cloudinary hoặc storage tương đương; chống trùng tên và địa điểm; gán owner là Admin tạo. | Must |
| FR-ADM-HOTEL-003 | Cập nhật khách sạn | Admin có thể cập nhật khách sạn mình sở hữu. | Hệ thống kiểm tra khách sạn tồn tại và quyền sở hữu; cập nhật thông tin hợp lệ; từ chối nếu không phải owner. | Must |
| FR-ADM-HOTEL-004 | Xóa khách sạn | Admin có thể xóa khách sạn mình sở hữu. | Hệ thống yêu cầu xác nhận; kiểm tra tồn tại và owner; xóa hoặc vô hiệu hóa khách sạn theo chính sách dữ liệu. | Must |
| FR-ADM-ROOM-001 | Xem phòng theo khách sạn | Admin có thể xem danh sách phòng của khách sạn mình quản lý. | Hệ thống kiểm tra quyền sở hữu khách sạn; hiển thị danh sách phòng và trạng thái dữ liệu. | Must |
| FR-ADM-ROOM-002 | Thêm phòng | Admin có thể thêm phòng vào khách sạn mình sở hữu. | Nhập tên, loại phòng, giá, số lượng, sức chứa, mô tả; upload ảnh; chọn tiện ích; kiểm tra owner của khách sạn; lưu room thành công. | Must |
| FR-ADM-ROOM-003 | Cập nhật phòng | Admin có thể cập nhật phòng thuộc khách sạn mình sở hữu. | Kiểm tra phòng tồn tại và quyền sở hữu hotel; cập nhật giá, mô tả, loại phòng, số lượng, sức chứa, ảnh, tiện ích khi hợp lệ. | Must |
| FR-ADM-ROOM-004 | Xóa phòng | Admin có thể xóa phòng thuộc khách sạn mình sở hữu. | Hệ thống yêu cầu xác nhận; kiểm tra phòng tồn tại; xóa hoặc vô hiệu hóa theo chính sách dữ liệu; danh sách phòng được cập nhật. | Must |
| FR-ADM-BOOK-001 | Xem toàn bộ booking | Admin có thể xem và tìm kiếm danh sách booking. | Chỉ Admin được truy cập; hiển thị booking với khách hàng, phòng, ngày, trạng thái, mã booking. | Must |
| FR-ADM-BOOK-002 | Cập nhật trạng thái booking | Admin có thể chuyển trạng thái booking sang check-in/check-out. | Booking phải tồn tại; khi check-in phải gán số phòng cụ thể; hệ thống kiểm tra số phòng không đang có khách; cập nhật trạng thái thành công khi hợp lệ. | Must |
| FR-ADM-BOOK-003 | Gán số phòng khi check-in | Admin có thể gán room number thực tế cho khách. | Không cho gán số phòng đang được dùng bởi booking `CHECKED_IN` khác trong cùng thời điểm; nếu trùng hiển thị lỗi phòng đang có khách. | Must |
| FR-ADM-BOOK-004 | Hủy booking | Admin có thể hủy booking khi còn hợp lệ. | Không cho hủy booking `CHECKED_OUT` hoặc `CANCELLED`; ghi nhận lý do hủy; cập nhật trạng thái `CANCELLED`. | Must |
| FR-ADM-AMENITY-001 | Tạo tiện ích | Admin có thể tạo tiện ích hệ thống. | Bắt buộc quyền Admin; tên tiện ích không trùng; lưu name, type, mô tả/icon nếu có. | Must |
| FR-ADM-AMENITY-002 | Cập nhật tiện ích | Admin có thể sửa tiện ích hệ thống. | Kiểm tra tiện ích tồn tại; tên mới không trùng tiện ích khác; lưu cập nhật khi hợp lệ. | Must |
| FR-ADM-AMENITY-003 | Xóa tiện ích | Admin có thể xóa tiện ích hệ thống khi chưa được sử dụng. | Kiểm tra tiện ích tồn tại; nếu đang được gán cho hotel/room thì chặn xóa; nếu không được sử dụng thì xóa thành công. | Must |
| FR-ADM-AMENITY-004 | Gán tiện ích cho khách sạn/phòng | Admin có thể gán tiện ích từ danh mục cho khách sạn hoặc phòng. | Kiểm tra quyền sở hữu khách sạn/phòng; tạo liên kết tiện ích; không tạo liên kết trùng. | Must |
| FR-ADM-AMENITY-005 | Gỡ tiện ích khỏi khách sạn/phòng | Admin có thể gỡ tiện ích khỏi khách sạn hoặc phòng. | Chỉ xóa liên kết; không xóa tiện ích gốc; kiểm tra quyền sở hữu trước khi thao tác. | Must |

## 6. Use Case Map

| Use Case ID | Role | Use Case Name | Related FR IDs |
| --- | --- | --- | --- |
| UC-001 | Customer, Admin | Đăng nhập | FR-CUS-AUTH-002, FR-ADM-AUTH-001 |
| UC-002 | Customer | Đăng ký | FR-CUS-AUTH-001 |
| UC-003 | Customer | Quản lý thông tin cá nhân | FR-CUS-PROFILE-001, FR-CUS-PROFILE-002, FR-CUS-PROFILE-003, FR-CUS-PROFILE-004 |
| UC-004 | Admin | Quản trị người dùng | FR-ADM-USER-001, FR-ADM-USER-002, FR-ADM-USER-003 |
| UC-005 | Admin | Quản lý phòng | FR-ADM-ROOM-001, FR-ADM-ROOM-002, FR-ADM-ROOM-003, FR-ADM-ROOM-004 |
| UC-006 | Customer | Tra cứu phòng | FR-CUS-ROOM-001, FR-CUS-ROOM-002, FR-CUS-ROOM-003, FR-CUS-ROOM-004 |
| UC-007 | Admin | Quản lý khách sạn | FR-ADM-HOTEL-001, FR-ADM-HOTEL-002, FR-ADM-HOTEL-003, FR-ADM-HOTEL-004 |
| UC-008 | Customer | Tra cứu khách sạn | FR-CUS-HOTEL-001, FR-CUS-HOTEL-002, FR-CUS-HOTEL-003 |
| UC-009 | Admin | Quản lý đặt phòng | FR-ADM-BOOK-001, FR-ADM-BOOK-002, FR-ADM-BOOK-003, FR-ADM-BOOK-004 |
| UC-010 | Customer | Đặt phòng | FR-CUS-BOOK-001, FR-CUS-BOOK-002 |
| UC-011 | Customer, Admin | Tra cứu và hủy booking | FR-CUS-BOOK-004, FR-CUS-BOOK-005, FR-CUS-BOOK-006, FR-ADM-BOOK-004 |
| UC-012 | Admin | Quản lý tiện ích | FR-ADM-AMENITY-001, FR-ADM-AMENITY-002, FR-ADM-AMENITY-003, FR-ADM-AMENITY-004, FR-ADM-AMENITY-005 |

## 7. Business Rules

### 7.1 Authentication Rules

| Rule ID | Rule |
| --- | --- |
| BR-AUTH-001 | Email là định danh đăng nhập và không được trùng. |
| BR-AUTH-002 | Mật khẩu phải được hash trước khi lưu. |
| BR-AUTH-003 | Account bị khóa hoặc inactive không được đăng nhập. |
| BR-AUTH-004 | Account mới đăng ký được gán role mặc định `CUSTOMER`. |
| BR-AUTH-005 | API yêu cầu đăng nhập phải xác thực bằng JWT hoặc cơ chế tương đương. |

### 7.2 Booking And Availability Rules

| Rule ID | Rule |
| --- | --- |
| BR-BOOK-001 | `checkin_date` không được nằm trong quá khứ. |
| BR-BOOK-002 | `checkout_date` phải sau `checkin_date`. |
| BR-BOOK-003 | Booking mới chỉ được tạo khi room/hotel tồn tại và còn hoạt động. |
| BR-BOOK-004 | Booking conflict nếu booking hiện có ở trạng thái `BOOKED` hoặc `CHECKED_IN` và khoảng ngày giao nhau với yêu cầu mới. |
| BR-BOOK-005 | Công thức giao ngày: `existing_checkin < new_checkout AND existing_checkout > new_checkin`. |
| BR-BOOK-006 | Số lượng phòng đặt mới cộng số lượng đã được giữ/đặt không được vượt quá `room.amount`. |
| BR-BOOK-007 | Sức chứa phòng phải đáp ứng tổng số khách theo yêu cầu. |
| BR-BOOK-008 | Tổng tiền booking được tính theo giá phòng, số đêm lưu trú và số lượng phòng. |
| BR-BOOK-009 | Mã booking phải duy nhất và có thể dùng để tra cứu. |
| BR-BOOK-010 | Booking mới có trạng thái mặc định `BOOKED`. |

### 7.3 Booking Status Rules

| Current Status | Action | Actor | Next Status | Conditions |
| --- | --- | --- | --- | --- |
| None | Create booking | Customer, Admin | `BOOKED` | Room available, valid dates, authenticated user |
| `BOOKED` | Check-in | Admin | `CHECKED_IN` | Assign room number, room number not occupied |
| `CHECKED_IN` | Check-out | Admin | `CHECKED_OUT` | Booking exists and current status is checked-in |
| `BOOKED` | Cancel | Customer, Admin | `CANCELLED` | Actor is owner or Admin |
| `CHECKED_IN` | Cancel | Admin | Not allowed | Blocked by default until policy is explicitly approved; system shows cannot-cancel error |
| `CHECKED_OUT` | Cancel | Customer, Admin | Not allowed | System shows cannot-cancel error |
| `CANCELLED` | Cancel again | Customer, Admin | Not allowed | System shows cannot-cancel error |

### 7.4 Ownership And Permission Rules

| Rule ID | Rule |
| --- | --- |
| BR-PERM-001 | Customer chỉ được xem/cập nhật profile của chính mình. |
| BR-PERM-002 | Customer chỉ được xem/hủy booking của chính mình, trừ trường hợp tra cứu công khai được xác nhận sau. |
| BR-PERM-003 | Admin được xem và xử lý danh sách booking trong hệ thống. |
| BR-PERM-004 | Admin chỉ được sửa/xóa khách sạn thuộc quyền sở hữu của mình. |
| BR-PERM-005 | Admin chỉ được thêm/sửa/xóa phòng trong khách sạn thuộc quyền sở hữu của mình. |
| BR-PERM-006 | Admin chỉ được gỡ/gán tiện ích vào khách sạn/phòng thuộc quyền sở hữu của mình. |

### 7.5 Data Format, Validation, And Defaults

| Data | Product Rule |
| --- | --- |
| Account registration | Email normalize lowercase; phone theo regex VN trong API Contract; account mới default role `CUSTOMER` và active. |
| Password | Min length `8`, max length `72`, có ít nhất một chữ và một số; password chỉ được lưu sau khi hash. |
| Booking dates | Customer nhập date-only `YYYY-MM-DD`; `checkout_date` phải sau `checkin_date`; `checkin_date` không ở quá khứ theo UTC+7. |
| Booking guests | `adult_amount` tối thiểu `1`; `children_amount` tối thiểu `0` và default `0` nếu form không nhập. |
| Booking status | Booking mới default `BOOKED`; trạng thái chỉ đổi qua state machine. |
| Booking quantity | Room quantity đặt phải `> 0`; tổng khách phải phù hợp capacity theo quantity. |
| Money | Giá, tổng tiền, refund dùng decimal scale 2; backend là nguồn tính tiền duy nhất. |
| Image URL | Chỉ lưu HTTPS URL từ Cloudinary/storage; không lưu base64 hoặc local path trong DB. |
| Hotel/room active state | Search/booking chỉ hiển thị và cho đặt hotel/room active. |

## 8. Screen Inventory

| Screen ID   | Role     | Screen                                 | Source Image                                               |
| ----------- | -------- | -------------------------------------- | ---------------------------------------------------------- |
| SCR-CUS-001 | Customer | Đăng nhập                              | `Hotel booking service/Thesis-report/images/image-096.png` |
| SCR-CUS-002 | Customer | Đăng ký                                | `Hotel booking service/Thesis-report/images/image-097.png` |
| SCR-CUS-003 | Customer | Trang chủ                              | `Hotel booking service/Thesis-report/images/image-098.png` |
| SCR-CUS-004 | Customer | Xem tất cả khách sạn                   | `Hotel booking service/Thesis-report/images/image-099.png` |
| SCR-CUS-005 | Customer | Chi tiết khách sạn                     | `Hotel booking service/Thesis-report/images/image-100.png` |
| SCR-CUS-006 | Customer | Danh sách phòng của khách sạn          | `Hotel booking service/Thesis-report/images/image-101.png` |
| SCR-CUS-007 | Customer | Chi tiết phòng và form đặt phòng       | `Hotel booking service/Thesis-report/images/image-102.png` |
| SCR-CUS-008 | Customer | Đặt phòng thành công                   | `Hotel booking service/Thesis-report/images/image-103.png` |
| SCR-CUS-009 | Customer | Lịch sử đặt phòng và tìm kiếm          | `Hotel booking service/Thesis-report/images/image-104.png` |
| SCR-CUS-010 | Customer | Chi tiết booking                       | `Hotel booking service/Thesis-report/images/image-105.png` |
| SCR-CUS-011 | Customer | Xác nhận hủy booking                   | `Hotel booking service/Thesis-report/images/image-106.png` |
| SCR-CUS-012 | Customer | Thông tin cá nhân và đổi mật khẩu      | `Hotel booking service/Thesis-report/images/image-107.png` |
| SCR-ADM-001 | Admin    | Trang chính quản trị                   | `Hotel booking service/Thesis-report/images/image-108.png` |
| SCR-ADM-002 | Admin    | Quản lý tài khoản                      | `Hotel booking service/Thesis-report/images/image-109.png` |
| SCR-ADM-003 | Admin    | Quản lý khách sạn                      | `Hotel booking service/Thesis-report/images/image-110.png` |
| SCR-ADM-004 | Admin    | Quản lý một khách sạn cụ thể           | `Hotel booking service/Thesis-report/images/image-111.png` |
| SCR-ADM-005 | Admin    | Quản lý phòng của khách sạn            | `Hotel booking service/Thesis-report/images/image-112.png` |
| SCR-ADM-006 | Admin    | Thêm phòng mới                         | `Hotel booking service/Thesis-report/images/image-113.png` |
| SCR-ADM-007 | Admin    | Chỉnh sửa phòng                        | `Hotel booking service/Thesis-report/images/image-114.png` |
| SCR-ADM-008 | Admin    | Xác nhận xóa phòng                     | `Hotel booking service/Thesis-report/images/image-115.png` |
| SCR-ADM-009 | Admin    | Thêm khách sạn                         | `Hotel booking service/Thesis-report/images/image-116.png` |
| SCR-ADM-010 | Admin    | Chỉnh sửa khách sạn                    | `Hotel booking service/Thesis-report/images/image-117.png` |
| SCR-ADM-011 | Admin    | Xác nhận xóa khách sạn                 | `Hotel booking service/Thesis-report/images/image-118.png` |
| SCR-ADM-012 | Admin    | Quản lý và tìm kiếm booking            | `Hotel booking service/Thesis-report/images/image-119.png` |
| SCR-ADM-013 | Admin    | Chuyển booking sang đã nhận phòng      | `Hotel booking service/Thesis-report/images/image-120.png` |
| SCR-ADM-014 | Admin    | Quản lý tiện nghi                      | `Hotel booking service/Thesis-report/images/image-121.png` |
| SCR-ADM-015 | Admin    | Thêm tiện nghi                         | `Hotel booking service/Thesis-report/images/image-122.png` |
| SCR-ADM-016 | Admin    | Chỉnh sửa tiện nghi                    | `Hotel booking service/Thesis-report/images/image-123.png` |
| SCR-ADM-017 | Admin    | Xác nhận xóa tiện nghi                 | `Hotel booking service/Thesis-report/images/image-124.png` |
| SCR-ADM-018 | Admin    | Xem tiện nghi theo cấp khách sạn/phòng | `Hotel booking service/Thesis-report/images/image-125.png` |

### 8.1 Screen Coverage Notes

| Note ID | Note |
| --- | --- |
| SCR-NOTE-001 | Chapter 3 labels two final screenshots as `Hình 3.113`; SDD disambiguates them as `SCR-ADM-017` and `SCR-ADM-018`. |
| SCR-NOTE-002 | Logout is treated as a header/profile/admin-layout action, not a standalone screen in Chapter 3. |
| SCR-NOTE-003 | Check-out and Admin cancel booking are operations inside `SCR-ADM-012` unless a future UI adds dedicated dialogs/screens. |
| SCR-NOTE-004 | Amenity assignment/removal can be implemented inside edit hotel/edit room screens or `SCR-ADM-018`; add a separate screen only if UI introduces a dedicated dialog. |

## 9. Yêu Cầu Phi Chức Năng

### 9.1 Performance

| NFR ID | Requirement | Target |
| --- | --- | --- |
| NFR-PERF-001 | Thời gian phản hồi tìm kiếm khách sạn/phòng | `<= 3s` |
| NFR-PERF-002 | Thời gian tải trang chính và trang chi tiết khách sạn | `<= 2s` |
| NFR-PERF-003 | Thời gian xác nhận giao dịch thanh toán nếu bật online payment | `5-7s` |

### 9.2 Security

| NFR ID | Requirement | Target |
| --- | --- | --- |
| NFR-SEC-001 | Mật khẩu lưu trữ an toàn | Hash bằng BCrypt hoặc thuật toán tương đương |
| NFR-SEC-002 | API bảo vệ bằng xác thực | JWT hoặc OAuth2 |
| NFR-SEC-003 | Phân quyền | Role-based access control cho Customer/Admin |
| NFR-SEC-004 | Kiểm tra sở hữu dữ liệu | Bắt buộc cho hotel, room, booking, amenity mapping |
| NFR-SEC-005 | Truyền tải an toàn | HTTPS/SSL-TLS cho môi trường production |
| NFR-SEC-006 | Thông tin thanh toán | Không xử lý tiền thật trong MVP nếu chưa tích hợp cổng thanh toán đạt chuẩn |

### 9.3 Data Integrity

| NFR ID | Requirement | Target |
| --- | --- | --- |
| NFR-DATA-001 | Ngăn overbooking | Kiểm tra conflict booking trước khi tạo booking |
| NFR-DATA-002 | Booking reference | Mã booking phải duy nhất |
| NFR-DATA-003 | Delete constraints | Không xóa amenity đang được gán cho hotel/room |
| NFR-DATA-004 | Status consistency | Booking chỉ chuyển trạng thái theo rule được định nghĩa |
| NFR-DATA-005 | Duplicate prevention | Không tạo khách sạn trùng tên và địa điểm |

### 9.4 Usability

| NFR ID | Requirement | Target |
| --- | --- | --- |
| NFR-UX-001 | Responsive UI | Hỗ trợ desktop, tablet, mobile |
| NFR-UX-002 | Error feedback | Form validation hiển thị lỗi rõ ràng tại thao tác liên quan |
| NFR-UX-003 | Empty states | Danh sách rỗng phải có thông báo phù hợp |
| NFR-UX-004 | Confirmation dialogs | Hành động xóa/hủy phải có xác nhận trước khi thực thi |
| NFR-UX-005 | Navigation clarity | Breadcrumb chưa thuộc MVP hiện tại, cần xác nhận nếu đưa vào scope |

### 9.5 Maintainability And Operations

| NFR ID | Requirement | Target |
| --- | --- | --- |
| NFR-OPS-001 | Modular design | Tách module theo auth, user, hotel, room, booking, amenity |
| NFR-OPS-002 | Maintenance window | Bảo trì ngoài giờ cao điểm và có thông báo trước |
| NFR-OPS-003 | Admin action logging | Nên ghi log cho hành động tạo/sửa/xóa quan trọng trong admin |

## 10. Open Questions

| Question ID | Question | Impact |
| --- | --- | --- |
| OQ-001 | Admin là system admin duy nhất hay có thêm hotel owner/partner role riêng? | Ảnh hưởng permission model và owner checks |
| OQ-002 | Tra cứu booking theo mã có cho guest chưa đăng nhập hay bắt buộc đăng nhập? | Ảnh hưởng bảo mật dữ liệu booking |
| OQ-003 | Có cần mở chính sách hủy booking ở trạng thái `CHECKED_IN` trong phiên bản sau không? | MVP mặc định chặn và trả `BOOKING_CANNOT_CANCEL`; chỉ thay đổi khi có policy mới |
| OQ-004 | Xóa hotel/room là hard delete hay soft delete? | Ảnh hưởng lịch sử booking và toàn vẹn dữ liệu |
| OQ-005 | Thanh toán thật có thuộc scope phiên bản tiếp theo không? | Ảnh hưởng payment domain, bảo mật, luồng booking |
| OQ-006 | Review, policy, promotion có thuộc roadmap gần không? | Ảnh hưởng database và màn hình mới |
| OQ-007 | Marketplace có tách Hotel Partner khỏi Admin hệ thống và có commission/hoa hồng không? | Ảnh hưởng role model, payout/reporting và quyền quản lý hotel |
| OQ-008 | Có cần partner quality score, audit log hoặc xử phạt khi đối tác vi phạm chính sách không? | Ảnh hưởng schema, admin workflow và compliance |
| OQ-009 | Có cần chatbot/support workflow trong roadmap gần không? | Ảnh hưởng use case hỗ trợ khách hàng, SLA và màn hình support |
| OQ-010 | Có cần rate plan/cancellation policy như free cancellation, non-refundable, pay-at-property không? | Ảnh hưởng pricing, cancellation, refund và payment domain |

## 11. Source References

| Source ID | Path                                                                                                                        | Used For                                                                                    |
| --------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| SRC-001   | `Hotel booking service/Thesis-report/chapters/chuong-1-gioi-thieu.md`                                                       | Mục tiêu, tiêu chí phi chức năng, scope đạt/chưa đạt                                        |
| SRC-002   | `Hotel booking service/Thesis-report/chapters/chuong-2-phuong-phap-thuc-hien.md`                                            | Quy trình nghiệp vụ auth, hotel/room, availability, booking, vận hành                       |
| SRC-003   | `Hotel booking service/Thesis-report/chapters/chuong-3-thiet-ke.md`                                                         | Use case chi tiết, screen inventory, activity/sequence diagrams                             |
| SRC-004   | `Hotel booking service/Thesis-report/chapters/chuong-4-ket-luan.md`                                                         | Gaps: quên mật khẩu, thanh toán thật, thống kê doanh thu, HTTPS, recommendation, breadcrumb |
| SRC-005   | `graphify-out/wiki/index.md`                                                                                                | Điều hướng knowledge graph                                                                  |
| SRC-006   | `graphify-out/wiki/3.2.1_Use_case_chi_tiết_-_3.2.1.10_Usecase_đặt_phòng_-_3.2.1.11_Usecase_tra_cứu_và_hủy_đơn_đặt_phòng.md` | Use case map                                                                                |
