# Update Logic

Tài liệu này trình bày logic nghiệp vụ theo hướng: mỗi actor có thể thực hiện những chức năng nào và khi actor thao tác thì hệ thống xử lý ra sao.

## 1. Actor Người dùng

Người dùng là actor tổng quát của hệ thống. Các actor Khách hàng, Doanh nghiệp, Quản lý và Quản trị viên đều kế thừa các chức năng chung này tùy theo quyền truy cập.

### Người dùng có thể đăng ký tài khoản

- Người dùng mới cung cấp họ tên, email, số điện thoại, ngày/năm sinh và mật khẩu.
- Trước khi tạo tài khoản, hệ thống kiểm tra email và số điện thoại trong cơ sở dữ liệu để tránh trùng lặp.
- Mật khẩu được mã hóa bằng BCrypt trước khi lưu trữ.
- Tài khoản mới được gán vai trò mặc định là `CUSTOMER` và trạng thái hoạt động là `ACTIVE`.
- Nếu người dùng đăng ký với mục đích trở thành doanh nghiệp/đối tác khách sạn, tài khoản vẫn được tạo trước, sau đó phải thực hiện luồng đăng ký doanh nghiệp riêng để được cấp quyền `BUSINESS`.

### Người dùng có thể đăng nhập

- Người dùng nhập email và mật khẩu.
- Hệ thống tìm tài khoản theo email, kiểm tra trạng thái tài khoản và từ chối đăng nhập nếu tài khoản bị khóa hoặc đã bị vô hiệu hóa bởi Quản trị viên.
- Nếu tài khoản hợp lệ, hệ thống so khớp mật khẩu đã mã hóa.
- Sau khi đăng nhập thành công, hệ thống xác định vai trò của người dùng để điều hướng đến đúng giao diện: Khách hàng, Doanh nghiệp, Quản lý hoặc Quản trị viên.

### Người dùng có thể yêu cầu khôi phục mật khẩu

- Người dùng yêu cầu khôi phục mật khẩu bằng email đã đăng ký.
- Hệ thống kiểm tra email tồn tại và gửi liên kết hoặc mã xác thực đặt lại mật khẩu.
- Mã khôi phục chỉ có hiệu lực trong một khoảng thời gian giới hạn và bị vô hiệu hóa sau khi sử dụng.

### Người dùng có thể đổi mật khẩu

- Người dùng đã đăng nhập có thể đổi mật khẩu từ trang hồ sơ cá nhân.
- Hệ thống yêu cầu nhập mật khẩu hiện tại, mật khẩu mới và xác nhận mật khẩu mới.
- Mật khẩu mới chỉ được cập nhật khi mật khẩu hiện tại hợp lệ và mật khẩu mới thỏa mãn quy định bảo mật.
- Sau khi đổi mật khẩu thành công, hệ thống lưu mật khẩu mới đã mã hóa và có thể yêu cầu người dùng đăng nhập lại trên các phiên khác.

### Người dùng có thể tìm kiếm và lọc khách sạn

- Người dùng có thể tìm kiếm khách sạn theo địa điểm lưu trú, ngày nhận phòng, ngày trả phòng, số lượng khách và số lượng phòng.
- Hệ thống chỉ hiển thị các khách sạn đang ở trạng thái được phép hoạt động và đã được Quản trị viên phê duyệt.
- Bộ lọc nâng cao có thể bao gồm mức giá, hạng sao, tiện nghi, chính sách hủy, điểm đánh giá và khoảng cách vị trí.
- Hệ thống loại bỏ các khách sạn không còn phòng phù hợp trong khoảng thời gian tìm kiếm.

### Người dùng có thể xem thông tin khách sạn

- Người dùng có thể xem trang chi tiết khách sạn từ kết quả tìm kiếm.
- Hệ thống hiển thị thông tin tổng quan gồm tên khách sạn, địa chỉ, mô tả, hình ảnh, tiện nghi, điểm đánh giá, chính sách và danh sách phòng còn khả dụng.
- Nếu khách sạn bị khóa hoặc chưa được phê duyệt, hệ thống không cho phép truy cập từ phía khách hàng.

### Người dùng có thể xem thông tin chi tiết phòng khách sạn

- Người dùng chọn một phòng hoặc loại phòng để xem thông tin chi tiết.
- Hệ thống hiển thị sức chứa, diện tích, tiện nghi trong phòng, hình ảnh, giá, số lượng còn trống và điều kiện hủy.
- Trước khi cho phép đặt phòng, hệ thống kiểm tra lại tình trạng phòng theo ngày nhận/trả phòng hiện tại để tránh dữ liệu cũ.

### Hệ thống kiểm tra phòng trống khi Người dùng tìm kiếm hoặc xem phòng

- Tất cả phòng thuộc khách sạn được kiểm tra theo khoảng thời gian người dùng chọn.
- Hệ thống loại bỏ những phòng đã nằm trong đơn đặt phòng có trạng thái `BOOKED`, `CHECKED_IN` hoặc đang được giữ chỗ tạm thời mà thời gian lưu trú giao nhau với thời gian tìm kiếm.
- Phòng chỉ được xem là hợp lệ khi còn số lượng trống, đáp ứng sức chứa và thuộc khách sạn đang hoạt động.
- Kết quả trả về gồm khách sạn, loại phòng, giá theo đêm, tiện nghi nổi bật và chính sách hủy áp dụng.

## 2. Actor Khách hàng

Khách hàng là người dùng đã đăng nhập và thực hiện các nghiệp vụ đặt phòng, quản lý thông tin cá nhân, theo dõi lịch sử, hủy đặt phòng và đánh giá khách sạn.

### Khách hàng có thể quản lý thông tin hồ sơ

- Khách hàng có thể cập nhật họ tên, số điện thoại, ngày sinh, ảnh đại diện và các thông tin liên hệ khác.
- Email dùng để đăng nhập chỉ được thay đổi khi hệ thống xác thực lại danh tính hoặc gửi xác nhận đến email mới.
- Hệ thống kiểm tra định dạng dữ liệu và không cho phép cập nhật thông tin trùng với tài khoản khác nếu trường đó cần duy nhất.

### Khách hàng có thể quản lý khách sạn yêu thích

- Khách hàng có thể thêm hoặc xóa khách sạn khỏi danh sách yêu thích.
- Mỗi khách sạn chỉ xuất hiện một lần trong danh sách yêu thích của cùng một khách hàng.
- Nếu khách sạn bị khóa hoặc ngừng hoạt động, hệ thống có thể ẩn khách sạn đó khỏi danh sách hiển thị nhưng vẫn giữ dữ liệu lịch sử.

### Khách hàng có thể đặt phòng khách sạn và thanh toán

- Khách hàng phải đăng nhập trước khi đặt phòng.
- Khách hàng chọn khách sạn, phòng, ngày nhận phòng, ngày trả phòng, số lượng khách và thông tin người lưu trú.
- Hệ thống kiểm tra ngày nhận phòng không được ở quá khứ và ngày trả phòng phải sau ngày nhận phòng.
- Tại thời điểm khách hàng nhấn đặt phòng, hệ thống kích hoạt cơ chế giữ chỗ tạm thời để hạn chế đặt trùng phòng.
- Hệ thống kiểm tra lại số lượng phòng còn trống trong khoảng thời gian lưu trú trước khi tạo giao dịch thanh toán.
- Nếu phòng không còn đủ số lượng, hệ thống từ chối yêu cầu và yêu cầu khách hàng chọn phương án khác.
- Nếu phòng hợp lệ, hệ thống tính tổng tiền dựa trên giá phòng, số đêm, số lượng phòng, thuế/phí nếu có và các ưu đãi hợp lệ.
- Khách hàng được chuyển sang cổng thanh toán điện tử như VNPay hoặc SePay trong thời gian giữ chỗ giới hạn.
- Khi thanh toán thành công, hệ thống tạo đơn đặt phòng với trạng thái `BOOKED`, chuyển giữ chỗ tạm thời thành đặt phòng chính thức và gửi email xác nhận cho khách hàng.
- Nếu thanh toán thất bại, hết thời gian hoặc bị hủy, hệ thống giải phóng giữ chỗ và không ghi nhận đơn đặt phòng thành công.
- Thông báo thời gian thực được gửi đến màn hình quản lý của khách sạn để Quản lý nắm được đơn mới.

### Khách hàng có thể xem lịch sử đặt phòng

- Khách hàng có thể xem danh sách các đơn đặt phòng đã tạo.
- Hệ thống phân loại lịch sử theo trạng thái như `BOOKED`, `CHECKED_IN`, `CHECKED_OUT`, `CANCELLED` và `NO_SHOW`.
- Mỗi đơn hiển thị mã đặt phòng, khách sạn, phòng, ngày lưu trú, tổng tiền, trạng thái thanh toán và chính sách hủy.

### Khách hàng có thể hủy đặt phòng khách sạn

- Khách hàng có thể yêu cầu hủy đơn nếu đơn đang ở trạng thái cho phép hủy theo chính sách của khách sạn.
- Hệ thống kiểm tra thời điểm hủy so với ngày nhận phòng và điều khoản hủy đã áp dụng khi đặt phòng.
- Nếu đủ điều kiện hủy miễn phí hoặc hoàn tiền một phần, hệ thống ghi nhận yêu cầu hoàn tiền theo tỷ lệ chính sách.
- Nếu quá hạn hủy, hệ thống có thể từ chối hủy hoặc cho hủy nhưng không hoàn tiền tùy điều khoản.
- Sau khi hủy thành công, trạng thái đơn chuyển thành `CANCELLED`, phòng được trả lại kho khả dụng và thông báo được gửi cho khách hàng cùng Quản lý khách sạn.

### Khách hàng có thể đánh giá khách sạn

- Khách hàng chỉ được đánh giá khách sạn sau khi có đơn đặt phòng tại khách sạn đó và đơn đã chuyển sang trạng thái `CHECKED_OUT`.
- Mỗi đơn đặt phòng chỉ được dùng để tạo một đánh giá hợp lệ.
- Nội dung đánh giá gồm số sao, nhận xét và có thể có hình ảnh minh họa nếu hệ thống hỗ trợ.
- Khi khách hàng viết đánh giá hợp lệ, hệ thống có thể tặng điểm thưởng hoặc ưu đãi dùng cho các đơn đặt phòng tương lai.
- Điểm thưởng của khách hàng chỉ được sử dụng theo điều kiện khuyến mãi và không được quy đổi trực tiếp thành tiền mặt nếu hệ thống không cho phép.

## 3. Actor Doanh nghiệp

Doanh nghiệp là actor đại diện đối tác khách sạn. Doanh nghiệp quản lý danh mục khách sạn thuộc quyền sở hữu và phân quyền nhân sự vận hành.

### Doanh nghiệp có thể đăng ký khách sạn mới

- Người dùng đại diện doanh nghiệp tạo hồ sơ đăng ký đối tác bằng thông tin pháp nhân như tên doanh nghiệp, mã số thuế, người đại diện, thông tin liên hệ và tài khoản ngân hàng.
- Hồ sơ được gửi đến Quản trị viên để kiểm duyệt.
- Nếu được chấp thuận, tài khoản được cấp vai trò `BUSINESS` và có quyền tạo hồ sơ khách sạn.
- Doanh nghiệp tạo khách sạn mới bằng cách cung cấp tên khách sạn, địa chỉ, mô tả, hình ảnh, tiện nghi, chính sách và thông tin liên hệ.
- Khách sạn mới ở trạng thái `PENDING_APPROVAL` và chỉ được hiển thị công khai sau khi Quản trị viên phê duyệt.

### Doanh nghiệp có thể quản lý danh mục khách sạn

- Doanh nghiệp có thể xem danh sách các khách sạn thuộc quyền sở hữu của mình.
- Doanh nghiệp có thể cập nhật thông tin cơ bản, gửi lại hồ sơ chờ duyệt, tạm ngưng kinh doanh hoặc yêu cầu mở lại khách sạn.
- Những thay đổi quan trọng như giấy tờ pháp lý, địa chỉ hoặc trạng thái hoạt động có thể cần Quản trị viên xét duyệt lại.
- Doanh nghiệp không được chỉnh sửa dữ liệu đặt phòng hoặc giao dịch ngoài phạm vi khách sạn mình sở hữu.

### Doanh nghiệp có thể quản lý nhân sự

- Doanh nghiệp có thể tạo tài khoản nhân sự hoặc gán người dùng hiện có làm Quản lý cho từng khách sạn cụ thể.
- Mỗi Quản lý chỉ được thao tác trên khách sạn được phân quyền.
- Doanh nghiệp có thể thu hồi quyền Quản lý khi nhân sự nghỉ việc hoặc đổi nhiệm vụ.
- Hệ thống ghi nhận lịch sử phân quyền để phục vụ kiểm tra và truy vết.

### Doanh nghiệp có thể xem thống kê báo cáo và đối soát

- Doanh nghiệp xem báo cáo theo phạm vi các khách sạn thuộc quyền sở hữu.
- Báo cáo gồm doanh thu, số lượng đơn, tỷ lệ lấp phòng, số đơn hủy, số đơn no-show và điểm đánh giá trung bình.
- Dữ liệu báo cáo được tổng hợp từ các đơn đã thanh toán và trạng thái vận hành thực tế.
- Doanh nghiệp thanh toán hoa hồng cho nền tảng theo bảng đối soát định kỳ thay vì theo từng đơn riêng lẻ.

## 4. Actor Quản lý

Quản lý là actor được Doanh nghiệp phân quyền để vận hành một hoặc nhiều khách sạn cụ thể.

### Quản lý có thể quản lý thông tin khách sạn

- Quản lý được phân quyền có thể cập nhật mô tả, hình ảnh, thông tin liên hệ, giờ nhận/trả phòng và tiện nghi của khách sạn.
- Các thay đổi ảnh hưởng đến tính pháp lý hoặc trạng thái công khai có thể cần Doanh nghiệp hoặc Quản trị viên phê duyệt.
- Khách sạn chỉ được nhận đặt phòng khi đang ở trạng thái hoạt động và có ít nhất một loại phòng hợp lệ.

### Quản lý có thể quản lý phòng

- Quản lý tạo và cập nhật loại phòng, số lượng phòng, sức chứa, tiện nghi, hình ảnh và giá bán.
- Hệ thống không cho phép xóa phòng hoặc giảm số lượng phòng nếu thao tác đó làm ảnh hưởng đến các đơn đã đặt trong tương lai.
- Khi cập nhật giá hoặc chính sách, thay đổi chỉ áp dụng cho các lượt đặt mới, không tự động thay đổi đơn đã thanh toán.
- Quản lý có thể đóng bán phòng theo ngày nếu phòng bảo trì hoặc khách sạn tạm ngưng nhận khách.

### Quản lý có thể quản lý đặt phòng

- Quản lý xem danh sách đơn đặt phòng của khách sạn mình phụ trách.
- Khi khách đến nhận phòng, Quản lý xác nhận check-in và chuyển trạng thái đơn từ `BOOKED` sang `CHECKED_IN`.
- Khi khách trả phòng, Quản lý xác nhận check-out và chuyển trạng thái đơn sang `CHECKED_OUT`.
- Nếu khách không đến, Quản lý có thể đánh dấu `NO_SHOW` theo quy định của khách sạn.
- Quản lý không được tạo trạng thái mâu thuẫn, ví dụ check-out khi đơn chưa check-in hoặc xử lý đơn không thuộc khách sạn mình quản lý.
- Mỗi đơn đặt phòng chuyển sang trạng thái `CHECKED_OUT` sẽ tự động cộng điểm uy tín cho khách sạn.

### Quản lý có thể quản lý đánh giá khách hàng

- Quản lý xem danh sách đánh giá thuộc khách sạn mình phụ trách.
- Quản lý có thể phản hồi đánh giá để giải thích hoặc chăm sóc khách hàng.
- Quản lý khách sạn được xem và phản hồi đánh giá, nhưng không được tự ý sửa điểm đánh giá của khách hàng.
- Nếu đánh giá có nội dung vi phạm, Quản lý gửi yêu cầu xử lý đến Quản trị viên thay vì tự ý xóa đánh giá.

### Quản lý có thể quản lý chính sách và điều khoản khách sạn

- Quản lý cấu hình chính sách hủy phòng, phụ thu, giờ nhận/trả phòng, quy định trẻ em, vật nuôi và các điều khoản lưu trú khác.
- Chính sách được gắn vào đơn tại thời điểm đặt phòng để đảm bảo khách hàng và khách sạn cùng tham chiếu một điều khoản cố định.
- Khi chính sách thay đổi, hệ thống chỉ áp dụng cho các đơn mới sau thời điểm cập nhật.

### Quản lý có thể xem thống kê báo cáo

- Quản lý xem báo cáo theo phạm vi khách sạn mình được phân quyền.
- Báo cáo gồm doanh thu, số lượng đơn, tỷ lệ lấp phòng, số đơn hủy, số đơn no-show và điểm đánh giá trung bình.
- Dữ liệu báo cáo được tổng hợp từ các đơn đã thanh toán và trạng thái vận hành thực tế.

## 5. Actor Quản trị viên

Quản trị viên là actor quản lý toàn bộ hệ thống, bao gồm danh mục dùng chung, người dùng, khách sạn, giao dịch, hoa hồng và hồ sơ hợp tác đối tác.

### Quản trị viên có thể quản lý tiện nghi

- Quản trị viên quản lý danh mục tiện nghi dùng chung cho toàn hệ thống.
- Tiện nghi có thể được thêm, cập nhật, ẩn hoặc ngừng sử dụng.
- Khi tiện nghi bị ẩn, các khách sạn đã sử dụng tiện nghi đó không bị mất dữ liệu lịch sử nhưng tiện nghi không còn xuất hiện trong lựa chọn mới.

### Quản trị viên có thể quản lý giao dịch và hoa hồng

- Quản trị viên theo dõi các giao dịch thanh toán, trạng thái hoàn tiền và doanh thu phát sinh từ đặt phòng.
- Hệ thống tính hoa hồng nền tảng dựa trên các đơn thành công, đơn no-show có thu tiền và chính sách thương mại áp dụng cho từng đối tác.
- Vào đầu mỗi tháng, hệ thống tổng hợp giao dịch tháng trước để tạo bảng đối soát cho Doanh nghiệp.
- Quản trị viên dùng bảng đối soát để theo dõi phần hoa hồng nền tảng và phần lợi nhuận đối tác.

### Quản trị viên có thể quản lý tất cả người dùng

- Quản trị viên xem và quản lý toàn bộ tài khoản người dùng trong hệ thống.
- Quản trị viên có thể khóa, mở khóa, cập nhật vai trò hoặc vô hiệu hóa tài khoản theo quy định.
- Hệ thống không cho phép thao tác làm mất tài khoản quản trị cuối cùng còn hoạt động.
- Mọi thay đổi vai trò và trạng thái tài khoản được ghi log để phục vụ kiểm tra.

### Quản trị viên có thể quản lý trạng thái hoạt động của tất cả khách sạn

- Quản trị viên xét duyệt khách sạn mới, khóa khách sạn vi phạm hoặc mở lại khách sạn sau khi khắc phục.
- Trạng thái khách sạn có thể gồm `PENDING_APPROVAL`, `ACTIVE`, `INACTIVE`, `SUSPENDED` và `REJECTED`.
- Khách sạn chỉ xuất hiện trong tìm kiếm và được nhận đặt phòng khi ở trạng thái `ACTIVE`.
- Khi khách sạn bị khóa, hệ thống không cho phép phát sinh đơn mới nhưng vẫn giữ dữ liệu đơn đặt phòng và giao dịch cũ.

### Quản trị viên có thể quản lý hồ sơ hợp tác khách sạn từ đối tác

- Quản trị viên tiếp nhận và kiểm tra hồ sơ hợp tác từ đối tác/doanh nghiệp.
- Hệ thống lưu thông tin hợp đồng, thời hạn hợp tác, tỷ lệ hoa hồng, trạng thái hiệu lực và tài liệu pháp lý liên quan.
- Chỉ những đối tác có hồ sơ hợp lệ mới được phép đưa khách sạn lên hệ thống.
- Khi hợp đồng hết hạn hoặc bị chấm dứt, hệ thống có thể tạm ngưng quyền đăng khách sạn mới hoặc khóa trạng thái hoạt động theo quy định.

### Quản trị viên có thể xử lý đánh giá vi phạm

- Quản trị viên có quyền ẩn hoặc xử lý đánh giá vi phạm quy định hệ thống.
- Quản trị viên xử lý các yêu cầu báo cáo đánh giá vi phạm do Quản lý khách sạn gửi lên.
- Việc xử lý đánh giá không làm mất dữ liệu lịch sử cần thiết cho kiểm tra và truy vết.

### Quản trị viên có thể xem thống kê báo cáo toàn hệ thống

- Quản trị viên xem báo cáo toàn hệ thống hoặc lọc theo khách sạn, doanh nghiệp, thời gian và trạng thái đơn.
- Báo cáo gồm doanh thu, số lượng đơn, tỷ lệ lấp phòng, số đơn hủy, số đơn no-show, điểm đánh giá trung bình, hoa hồng nền tảng và payout cho đối tác.
- Dữ liệu báo cáo được dùng để kiểm tra vận hành, đối soát doanh thu và đánh giá chất lượng khách sạn.

## 6. Logic tự động của hệ thống đi kèm các actor

### Hệ thống tự động bảo vệ dữ liệu đặt phòng

- Hệ thống dùng cơ chế giữ chỗ tạm thời khi Khách hàng bắt đầu đặt phòng để hạn chế overbooking.
- Hệ thống tự động giải phóng giữ chỗ nếu thanh toán thất bại, hết thời gian hoặc bị hủy.
- Hệ thống không cho phép tạo đơn mới cho khách sạn không ở trạng thái `ACTIVE`.
- Hệ thống không cho phép thao tác quản lý ảnh hưởng đến các đơn đã đặt trong tương lai.

### Hệ thống tự động cập nhật uy tín và ưu đãi

- Mỗi đơn đặt phòng chuyển sang trạng thái `CHECKED_OUT` sẽ tự động cộng điểm uy tín cho khách sạn.
- Thuật toán hiển thị khách sạn dựa trên điểm uy tín, điểm đánh giá trung bình, tỷ lệ hoàn tất đơn và mức độ vi phạm chính sách.
- Đánh giá tích cực giúp tăng độ hiển thị của khách sạn; đánh giá tiêu cực hoặc vi phạm vận hành có thể làm giảm độ ưu tiên hiển thị.
- Khi Khách hàng viết đánh giá hợp lệ, hệ thống có thể tặng điểm thưởng hoặc ưu đãi dùng cho các đơn đặt phòng tương lai.
