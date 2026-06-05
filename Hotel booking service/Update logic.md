# Update Logic

Tài liệu này trình bày logic nghiệp vụ theo hướng: mỗi actor có thể thực hiện những chức năng nào và khi actor thao tác thì hệ thống xử lý ra sao.

## 1. Actor Người dùng

Người dùng là actor tổng quát của hệ thống. Các actor Khách hàng, Doanh nghiệp, Quản lý và Quản trị viên đều kế thừa các chức năng chung này tùy theo quyền truy cập.

### Người dùng có thể đăng ký tài khoản

- Người dùng mới có thể đăng ký tài khoản khách hàng bằng cách cung cấp họ tên, email, số điện thoại, ngày/năm sinh, mật khẩu và xác nhận mật khẩu.
- Trước khi tạo tài khoản, hệ thống kiểm tra email và số điện thoại trong cơ sở dữ liệu để tránh trùng lặp.
- Mật khẩu được mã hóa bằng BCrypt trước khi lưu trữ.
- Tài khoản khách hàng mới được gán vai trò mặc định là `CUSTOMER` và trạng thái hoạt động là `ACTIVE`.
- Người dùng có thể đăng ký tài khoản doanh nghiệp/đối tác bằng cách cung cấp thông tin tài khoản, thông tin bảo mật, thông tin người đại diện và thông tin pháp lý của doanh nghiệp.
- Hồ sơ doanh nghiệp gồm tên doanh nghiệp, mã số thuế, địa chỉ đăng ký kinh doanh, người đại diện, chức vụ, số điện thoại và email liên hệ.
- Sau khi đăng ký doanh nghiệp, hệ thống lưu tài khoản và hồ sơ đối tác ở trạng thái chờ xét duyệt. Quyền `BUSINESS` chỉ được cấp sau khi Quản trị viên phê duyệt hồ sơ hợp lệ.

### Người dùng có thể đăng nhập

- Người dùng nhập email và mật khẩu.
- Hệ thống tìm tài khoản theo email, kiểm tra trạng thái tài khoản và từ chối đăng nhập nếu tài khoản bị khóa hoặc đã bị vô hiệu hóa bởi Quản trị viên.
- Nếu tài khoản hợp lệ, hệ thống so khớp mật khẩu đã mã hóa.
- Sau khi đăng nhập thành công, hệ thống xác định vai trò của người dùng để điều hướng đến đúng giao diện: Khách hàng, Doanh nghiệp, Quản lý hoặc Quản trị viên.

### Người dùng có thể yêu cầu khôi phục mật khẩu

- Người dùng yêu cầu khôi phục mật khẩu bằng email đã đăng ký.
- Hệ thống kiểm tra email tồn tại và gửi liên kết hoặc mã xác thực đặt lại mật khẩu.
- Mã khôi phục chỉ có hiệu lực trong một khoảng thời gian giới hạn và bị vô hiệu hóa sau khi sử dụng.
- Sau khi xác thực hợp lệ, hệ thống cho phép người dùng thiết lập mật khẩu mới đã được mã hóa trước khi lưu.

### Người dùng có thể đổi mật khẩu

- Người dùng đã đăng nhập có thể đổi mật khẩu từ trang hồ sơ cá nhân.
- Hệ thống yêu cầu nhập mật khẩu hiện tại, mật khẩu mới và xác nhận mật khẩu mới.
- Mật khẩu mới chỉ được cập nhật khi mật khẩu hiện tại hợp lệ và mật khẩu mới thỏa mãn quy định bảo mật.
- Sau khi đổi mật khẩu thành công, hệ thống lưu mật khẩu mới đã mã hóa và có thể yêu cầu người dùng đăng nhập lại trên các phiên khác.

### Người dùng có thể đăng xuất

- Người dùng đã đăng nhập có thể đăng xuất để chấm dứt phiên làm việc hiện tại.
- Hệ thống hủy hoặc vô hiệu hóa phiên/token đăng nhập tương ứng.
- Sau khi đăng xuất, người dùng phải đăng nhập lại nếu muốn truy cập các chức năng yêu cầu xác thực.
- Việc đăng xuất giúp bảo vệ tài khoản khi người dùng thao tác trên thiết bị dùng chung.

### Người dùng có thể tìm kiếm và lọc khách sạn

- Người dùng có thể tìm kiếm khách sạn theo địa điểm lưu trú, ngày nhận phòng, ngày trả phòng, số lượng khách và số lượng phòng.
- Hệ thống chỉ hiển thị các khách sạn đang ở trạng thái được phép hoạt động và đã được Quản trị viên phê duyệt.
- Bộ lọc nâng cao có thể bao gồm mức giá, hạng sao, tiện nghi, chính sách hủy, điểm đánh giá và khoảng cách vị trí.
- Người dùng có thể sắp xếp kết quả theo giá, điểm đánh giá, mức độ phù hợp hoặc các tiêu chí hiển thị khác.
- Hệ thống loại bỏ các khách sạn không còn phòng phù hợp trong khoảng thời gian tìm kiếm.

### Người dùng có thể xem thông tin khách sạn và phòng

- Người dùng có thể xem trang chi tiết khách sạn từ kết quả tìm kiếm.
- Hệ thống hiển thị thông tin tổng quan gồm tên khách sạn, địa chỉ, mô tả, hình ảnh, tiện nghi, điểm đánh giá, chính sách và danh sách phòng còn khả dụng.
- Người dùng có thể chọn một phòng hoặc loại phòng để xem thông tin chi tiết.
- Hệ thống hiển thị sức chứa, diện tích, tiện nghi trong phòng, hình ảnh, giá, số lượng còn trống và điều kiện hủy.
- Nếu khách sạn bị khóa hoặc chưa được phê duyệt, hệ thống không cho phép truy cập từ phía khách hàng.
- Trước khi cho phép đặt phòng, hệ thống kiểm tra lại tình trạng phòng theo ngày nhận/trả phòng hiện tại để tránh dữ liệu cũ.

### Người dùng có thể quản lý hồ sơ cá nhân

- Người dùng phải đăng nhập trước khi truy cập khu vực quản lý hồ sơ.
- Người dùng có thể xem thông tin cá nhân hiện tại của mình trên hệ thống.
- Người dùng có thể cập nhật họ tên, số điện thoại, ngày sinh, ảnh đại diện và các thông tin liên hệ khác.
- Email dùng để đăng nhập chỉ được thay đổi khi hệ thống xác thực lại danh tính hoặc gửi xác nhận đến email mới.
- Hệ thống kiểm tra định dạng dữ liệu và không cho phép cập nhật thông tin trùng với tài khoản khác nếu trường đó cần duy nhất.

### Hệ thống kiểm tra phòng trống khi Người dùng tìm kiếm hoặc xem phòng

- Tất cả phòng thuộc khách sạn được kiểm tra theo khoảng thời gian người dùng chọn.
- Hệ thống loại bỏ những phòng đã nằm trong đơn đặt phòng có trạng thái `BOOKED`, `CHECKED_IN` hoặc đang được giữ chỗ tạm thời mà thời gian lưu trú giao nhau với thời gian tìm kiếm.
- Phòng chỉ được xem là hợp lệ khi còn số lượng trống, đáp ứng sức chứa và thuộc khách sạn đang hoạt động.
- Kết quả trả về gồm khách sạn, loại phòng, giá theo đêm, tiện nghi nổi bật và chính sách hủy áp dụng.

## 2. Actor Khách hàng

Khách hàng là người dùng đã đăng nhập và thực hiện các nghiệp vụ tìm khách sạn, lưu khách sạn yêu thích, đặt phòng, thanh toán, theo dõi lịch sử, hủy đặt phòng, yêu cầu hoàn tiền và đánh giá khách sạn.

### Khách hàng có thể quản lý khách sạn yêu thích

- Khách hàng phải đăng nhập trước khi quản lý danh sách yêu thích.
- Khách hàng có thể thêm khách sạn hoặc phòng quan tâm vào danh sách yêu thích để lưu trữ và xem lại sau.
- Mỗi khách sạn chỉ xuất hiện một lần trong danh sách yêu thích của cùng một khách hàng.
- Khách hàng có thể xem danh sách các khách sạn đã được lưu vào mục yêu thích.
- Khách hàng có thể xóa khách sạn khỏi danh sách yêu thích khi không còn nhu cầu theo dõi.
- Nếu khách sạn bị khóa hoặc ngừng hoạt động, hệ thống có thể ẩn khách sạn đó khỏi danh sách hiển thị nhưng vẫn giữ dữ liệu lịch sử.

### Khách hàng có thể đặt phòng khách sạn và thanh toán

- Khách hàng phải đăng nhập trước khi đặt phòng.
- Khách hàng chọn khách sạn, phòng, ngày nhận phòng, ngày trả phòng, số lượng khách, số lượng phòng và thông tin người lưu trú.
- Khách hàng có thể ghi chú thêm các yêu cầu đặc biệt nếu có.
- Hệ thống kiểm tra ngày nhận phòng không được ở quá khứ và ngày trả phòng phải sau ngày nhận phòng.
- Tại thời điểm khách hàng nhấn đặt phòng, hệ thống kích hoạt cơ chế giữ chỗ tạm thời để hạn chế đặt trùng phòng.
- Hệ thống kiểm tra lại số lượng phòng còn trống trong khoảng thời gian lưu trú trước khi tạo giao dịch thanh toán.
- Nếu phòng không còn đủ số lượng, hệ thống từ chối yêu cầu và yêu cầu khách hàng chọn phương án khác.
- Nếu phòng hợp lệ, hệ thống tính tổng tiền dựa trên giá phòng, số đêm, số lượng phòng, thuế/phí nếu có và các ưu đãi hợp lệ.
- Khách hàng chọn phương thức thanh toán và được chuyển sang cổng thanh toán điện tử như VNPay hoặc SePay trong thời gian giữ chỗ giới hạn.
- Khi thanh toán thành công, hệ thống tạo đơn đặt phòng với trạng thái `BOOKED`, chuyển giữ chỗ tạm thời thành đặt phòng chính thức và gửi email xác nhận cho khách hàng.
- Nếu thanh toán thất bại, hết thời gian hoặc bị hủy, hệ thống giải phóng giữ chỗ và không ghi nhận đơn đặt phòng thành công.
- Thông báo thời gian thực được gửi đến màn hình quản lý của khách sạn để Quản lý nắm được đơn mới.

### Khách hàng có thể xem lịch sử đặt phòng

- Khách hàng phải đăng nhập trước khi xem lịch sử đặt phòng.
- Khách hàng có thể xem danh sách các đơn đặt phòng đã tạo.
- Hệ thống phân loại lịch sử theo trạng thái như `BOOKED`, `CHECKED_IN`, `CHECKED_OUT`, `CANCELLED` và `NO_SHOW`.
- Mỗi đơn hiển thị mã đặt phòng, khách sạn, phòng, ngày lưu trú, tổng tiền, trạng thái thanh toán và chính sách hủy.
- Khách hàng có thể xem thông tin chi tiết của một đơn đặt phòng cụ thể.
- Khách hàng có thể chuyển sang bước đánh giá khách sạn trực tiếp từ lịch sử đơn hàng nếu đơn đủ điều kiện.

### Khách hàng có thể hủy đặt phòng và yêu cầu hoàn tiền

- Khách hàng có thể yêu cầu hủy đơn nếu đơn đang ở trạng thái cho phép hủy theo chính sách của khách sạn.
- Hệ thống kiểm tra thời điểm hủy so với ngày nhận phòng và điều khoản hủy đã áp dụng khi đặt phòng.
- Nếu đủ điều kiện hủy miễn phí hoặc hoàn tiền một phần, hệ thống ghi nhận yêu cầu hoàn tiền theo tỷ lệ chính sách.
- Nếu quá hạn hủy, hệ thống có thể từ chối hủy hoặc cho hủy nhưng không hoàn tiền tùy điều khoản.
- Sau khi hủy thành công, trạng thái đơn chuyển thành `CANCELLED`, phòng được trả lại kho khả dụng và thông báo được gửi cho khách hàng cùng Quản lý khách sạn.
- Hệ thống xử lý hoàn tiền theo chính sách áp dụng cho đơn đặt phòng và trạng thái giao dịch thanh toán.

### Khách hàng có thể đánh giá khách sạn

- Khách hàng chỉ được đánh giá khách sạn sau khi có đơn đặt phòng tại khách sạn đó và đơn đã chuyển sang trạng thái `CHECKED_OUT`.
- Mỗi đơn đặt phòng chỉ được dùng để tạo một đánh giá hợp lệ.
- Nội dung đánh giá gồm số sao, nhận xét và có thể có hình ảnh minh họa nếu hệ thống hỗ trợ.
- Khi khách hàng viết đánh giá hợp lệ, hệ thống có thể tặng điểm thưởng hoặc ưu đãi dùng cho các đơn đặt phòng tương lai.
- Điểm thưởng của khách hàng chỉ được sử dụng theo điều kiện khuyến mãi và không được quy đổi trực tiếp thành tiền mặt nếu hệ thống không cho phép.

## 3. Actor Quản lý

Quản lý là actor được Doanh nghiệp phân quyền để vận hành thông tin khách sạn, phòng, đơn đặt phòng, đánh giá, chính sách, báo cáo và hồ sơ cá nhân trong phạm vi khách sạn được giao.

### Quản lý có thể quản lý thông tin khách sạn

- Quản lý bắt buộc phải đăng nhập trước khi thao tác.
- Quản lý được phân quyền có thể cập nhật mô tả, phần giới thiệu, hình ảnh, thông tin liên hệ, giờ nhận/trả phòng và tiện nghi của khách sạn.
- Quản lý có thể thêm các tiện nghi mới cho khách sạn hoặc cập nhật tiện nghi hiện tại.
- Các thay đổi ảnh hưởng đến tính pháp lý hoặc trạng thái công khai có thể cần Doanh nghiệp hoặc Quản trị viên phê duyệt.
- Khách sạn chỉ được nhận đặt phòng khi đang ở trạng thái hoạt động và có ít nhất một loại phòng hợp lệ.

### Quản lý có thể quản lý phòng

- Quản lý bắt buộc phải đăng nhập và xem danh sách loại phòng trước khi quản lý.
- Quản lý có thể thêm loại phòng mới vào hệ thống.
- Khi thêm loại phòng mới, hệ thống yêu cầu Quản lý nhập đầy đủ giá, hình ảnh, mô tả, sức chứa, số lượng phòng, tiện nghi và chính sách áp dụng.
- Quản lý có thể cập nhật thông tin loại phòng hiện có như hình ảnh, mô tả, giá, sức chứa và số lượng phòng.
- Khi cập nhật giá hoặc chính sách, thay đổi chỉ áp dụng cho các lượt đặt mới, không tự động thay đổi đơn đã thanh toán.
- Hệ thống không cho phép xóa phòng hoặc giảm số lượng phòng nếu thao tác đó làm ảnh hưởng đến các đơn đã đặt trong tương lai.
- Quản lý có thể ẩn, đóng bán hoặc xóa loại phòng khỏi hệ thống khi thao tác không ảnh hưởng đến đơn hợp lệ.
- Quản lý có thể đóng bán phòng theo ngày nếu phòng bảo trì hoặc khách sạn tạm ngưng nhận khách.

### Quản lý có thể quản lý đặt phòng

- Quản lý bắt buộc phải đăng nhập và chỉ được xem danh sách đơn đặt phòng của khách sạn mình phụ trách.
- Quản lý có thể xem chi tiết thông tin của một đơn đặt phòng cụ thể.
- Quản lý có thể lọc, tìm kiếm và sắp xếp danh sách đơn đặt phòng để dễ theo dõi.
- Khi khách đến nhận phòng, Quản lý xác nhận check-in và chuyển trạng thái đơn từ `BOOKED` sang `CHECKED_IN`.
- Khi khách trả phòng, Quản lý xác nhận check-out và chuyển trạng thái đơn sang `CHECKED_OUT`.
- Nếu khách không đến, Quản lý có thể đánh dấu `NO_SHOW` theo quy định của khách sạn.
- Quản lý có thể hủy đơn đặt phòng nếu đơn thuộc phạm vi khách sạn được giao và đáp ứng chính sách hủy.
- Khi hủy đơn, hệ thống có thể hỗ trợ hoàn tiền theo chính sách và gửi email thông báo kèm lý do hủy.
- Quản lý không được tạo trạng thái mâu thuẫn, ví dụ check-out khi đơn chưa check-in hoặc xử lý đơn không thuộc khách sạn mình quản lý.
- Mỗi đơn đặt phòng chuyển sang trạng thái `CHECKED_OUT` sẽ tự động cộng điểm uy tín cho khách sạn.

### Quản lý có thể quản lý đánh giá khách sạn

- Quản lý bắt buộc phải đăng nhập và chỉ được xem đánh giá thuộc khách sạn mình phụ trách.
- Quản lý có thể lọc và sắp xếp các đánh giá để dễ theo dõi.
- Quản lý có thể phản hồi đánh giá để giải thích hoặc chăm sóc khách hàng.
- Quản lý được xem và phản hồi đánh giá, nhưng không được tự ý sửa điểm đánh giá của khách hàng.
- Nếu đánh giá có nội dung vi phạm, Quản lý có thể ẩn đánh giá khỏi khu vực hiển thị công khai và hệ thống vẫn giữ dữ liệu lịch sử để kiểm tra, truy vết.

### Quản lý có thể quản lý chính sách và điều khoản khách sạn

- Quản lý bắt buộc phải đăng nhập và xem danh sách chính sách, điều khoản hiện có.
- Quản lý cấu hình chính sách hủy phòng, hoàn tiền, phụ thu, giờ nhận/trả phòng, quy định trẻ em, vật nuôi và các điều khoản lưu trú khác.
- Chính sách được gắn vào đơn tại thời điểm đặt phòng để đảm bảo khách hàng và khách sạn cùng tham chiếu một điều khoản cố định.
- Khi chính sách thay đổi, hệ thống chỉ áp dụng cho các đơn mới sau thời điểm cập nhật.
- Quản lý có thể thêm các điều khoản về xử lý sự cố hoặc thiệt hại tài sản.

### Quản lý có thể quản lý thông tin hồ sơ cá nhân

- Quản lý bắt buộc phải đăng nhập và xem thông tin tài khoản của mình.
- Quản lý có thể xem các thông tin chi tiết như mã nhân viên, vai trò và địa điểm công tác.
- Quản lý có thể đổi mật khẩu tài khoản.
- Quản lý có thể cập nhật họ tên, số điện thoại, ngày tháng năm sinh và giới tính.
- Hệ thống kiểm tra quyền và định dạng dữ liệu trước khi lưu thay đổi hồ sơ.

### Quản lý có thể xem thống kê báo cáo

- Quản lý xem báo cáo theo phạm vi khách sạn mình được phân quyền.
- Báo cáo gồm doanh thu, số lượng đơn, tỷ lệ lấp phòng, số đơn hủy, số đơn no-show và điểm đánh giá trung bình.
- Dữ liệu báo cáo được tổng hợp từ các đơn đã thanh toán và trạng thái vận hành thực tế.

## 4. Actor Doanh nghiệp

Doanh nghiệp là actor đại diện cho đối tác hoặc tổ chức sở hữu khách sạn. Doanh nghiệp có thể đăng ký khách sạn, quản lý danh mục khách sạn, nhân sự, phân công, hồ sơ và báo cáo.

### Doanh nghiệp có thể đăng ký khách sạn mới

- Doanh nghiệp bắt buộc phải đăng nhập trước khi bắt đầu quy trình.
- Doanh nghiệp có thể tạo đơn đăng ký cho một khách sạn mới thuộc chuỗi của mình.
- Doanh nghiệp bắt buộc phải cung cấp thông tin pháp nhân gồm tên doanh nghiệp, mã số thuế, địa điểm, người đại diện, thông tin liên hệ và tài khoản ngân hàng nếu cần đối soát.
- Doanh nghiệp có thể chỉnh sửa hoặc cập nhật lại thông tin pháp nhân trong quá trình thực hiện nếu cần.
- Doanh nghiệp tạo khách sạn mới bằng cách cung cấp tên khách sạn, địa chỉ, mô tả, hình ảnh, tiện nghi, chính sách và thông tin liên hệ.
- Khách sạn mới ở trạng thái `PENDING_APPROVAL` và chỉ được hiển thị công khai sau khi Quản trị viên phê duyệt.
- Sau khi hoàn tất thông tin, Doanh nghiệp gửi hồ sơ lên Quản trị viên để xét duyệt.

### Doanh nghiệp có thể quản lý danh mục khách sạn

- Doanh nghiệp bắt buộc phải đăng nhập thành công mới có thể truy cập giao diện quản lý danh mục khách sạn.
- Doanh nghiệp có thể xem danh sách toàn bộ các khách sạn hiện đang thuộc sở hữu của mình.
- Doanh nghiệp có thể mở rộng chuỗi bằng cách kích hoạt quy trình đăng ký thêm khách sạn mới từ phần quản lý danh mục.
- Doanh nghiệp có thể cập nhật thông tin cơ bản, gửi lại hồ sơ chờ duyệt, tạm ngưng kinh doanh hoặc yêu cầu mở lại khách sạn.
- Những thay đổi quan trọng như giấy tờ pháp lý, địa chỉ hoặc trạng thái hoạt động có thể cần Quản trị viên xét duyệt lại.
- Doanh nghiệp không được chỉnh sửa dữ liệu đặt phòng hoặc giao dịch ngoài phạm vi khách sạn mình sở hữu.

### Doanh nghiệp có thể quản lý nhân sự và phân công

- Doanh nghiệp bắt buộc phải đăng nhập để thao tác với phân hệ nhân sự.
- Doanh nghiệp có thể xem danh sách toàn bộ nhân viên đang hoạt động trong hệ thống của mình.
- Doanh nghiệp có thể sử dụng tính năng sắp xếp và lọc dữ liệu để quản lý hoặc tìm kiếm nhân sự phù hợp.
- Doanh nghiệp có thể tạo tài khoản nhân sự hoặc gán người dùng hiện có làm Quản lý cho từng khách sạn cụ thể.
- Khi thêm nhân viên mới, Doanh nghiệp bắt buộc khai báo họ tên, giới tính, năm sinh, số điện thoại và trạng thái hoạt động.
- Khi thêm hoặc phân công nhân viên, Doanh nghiệp phải thiết lập vai trò và gán quyền tương ứng.
- Mỗi Quản lý chỉ được thao tác trên khách sạn được phân quyền.
- Doanh nghiệp có thể phân bổ nơi làm việc hoặc nơi công tác cụ thể cho nhân viên.
- Doanh nghiệp có thể cập nhật vai trò/chức vụ của nhân viên thông qua thăng chức hoặc giáng chức.
- Doanh nghiệp có thể luân chuyển công tác của nhân viên giữa các chi nhánh khách sạn khác nhau trong chuỗi.
- Doanh nghiệp có thể thu hồi quyền đã cấp hoặc vô hiệu hóa tài khoản nhân viên khi có thay đổi nhân sự hoặc khi nhân viên vi phạm quy định.
- Hệ thống ghi nhận lịch sử phân quyền để phục vụ kiểm tra và truy vết.

### Doanh nghiệp có thể xem thống kê báo cáo và đối soát

- Doanh nghiệp bắt buộc đăng nhập để xem dữ liệu nhạy cảm về tài chính và hoạt động.
- Doanh nghiệp xem báo cáo theo phạm vi các khách sạn thuộc quyền sở hữu.
- Báo cáo gồm tổng doanh thu, tổng lợi nhuận, doanh thu theo từng khách sạn, số lượng đơn, tỷ lệ lấp phòng, số đơn hủy, số đơn no-show, điểm đánh giá trung bình và chi phí hoa hồng cần trả cho nền tảng.
- Doanh nghiệp có thể lọc dữ liệu doanh thu theo từng khoảng thời gian cụ thể để phục vụ việc phân tích.
- Dữ liệu báo cáo được tổng hợp từ các đơn đã thanh toán và trạng thái vận hành thực tế.
- Doanh nghiệp thanh toán hoa hồng cho nền tảng theo bảng đối soát định kỳ thay vì theo từng đơn riêng lẻ.

### Doanh nghiệp có thể quản lý thông tin hồ sơ

- Doanh nghiệp bắt buộc phải đăng nhập để quản lý hồ sơ.
- Doanh nghiệp có thể xem toàn bộ thông tin đã đăng ký của tổ chức.
- Doanh nghiệp có thể đổi mật khẩu để bảo đảm an toàn cho tài khoản.
- Doanh nghiệp có thể cập nhật thông tin hồ sơ.
- Khi cập nhật hồ sơ, Doanh nghiệp có thể chỉnh sửa thông tin người đại diện hợp pháp, thông tin liên hệ và thông tin pháp lý của doanh nghiệp.
- Những thay đổi quan trọng về pháp nhân có thể cần Quản trị viên kiểm tra lại trước khi có hiệu lực trên hệ thống.

## 5. Actor Quản trị viên

Quản trị viên là actor quản lý toàn bộ hệ thống, bao gồm đăng ký khách sạn từ đối tác, giao dịch, hoa hồng, trạng thái hoạt động khách sạn, người dùng, tiện nghi, báo cáo và địa điểm.

### Quản trị viên có thể quản lý đăng ký khách sạn từ đối tác

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem danh sách các đăng ký khách sạn được gửi từ đối tác.
- Quản trị viên tiếp nhận và kiểm tra hồ sơ hợp tác từ đối tác/doanh nghiệp.
- Quản trị viên có thể duyệt các yêu cầu đăng ký hợp lệ.
- Quản trị viên có thể từ chối các yêu cầu đăng ký và ghi kèm lý do từ chối.
- Sau khi phê duyệt, khách sạn hoặc hồ sơ đối tác được chuyển sang trạng thái phù hợp để tiếp tục vận hành.

### Quản trị viên có thể quản lý giao dịch và hoa hồng

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem nhật ký của các giao dịch.
- Quản trị viên có thể xem chi tiết từng giao dịch cụ thể.
- Quản trị viên có thể lọc và tìm kiếm các giao dịch.
- Quản trị viên theo dõi trạng thái thanh toán, hoàn tiền và doanh thu phát sinh từ đặt phòng.
- Hệ thống tính hoa hồng nền tảng dựa trên các đơn thành công, đơn no-show có thu tiền và chính sách thương mại áp dụng cho từng đối tác.
- Vào đầu mỗi tháng, hệ thống tổng hợp giao dịch tháng trước để tạo bảng đối soát cho Doanh nghiệp.
- Quản trị viên dùng bảng đối soát để theo dõi phần hoa hồng nền tảng và phần lợi nhuận đối tác.

### Quản trị viên có thể quản lý hoạt động khách sạn

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem danh sách các khách sạn hiện đang hoạt động.
- Quản trị viên có thể lọc và tìm kiếm các khách sạn.
- Quản trị viên xét duyệt khách sạn mới, khóa khách sạn vi phạm hoặc mở lại khách sạn sau khi khắc phục.
- Trạng thái khách sạn có thể gồm `PENDING_APPROVAL`, `ACTIVE`, `INACTIVE`, `SUSPENDED` và `REJECTED`.
- Khách sạn chỉ xuất hiện trong tìm kiếm và được nhận đặt phòng khi ở trạng thái `ACTIVE`.
- Khi khách sạn bị khóa, hệ thống không cho phép phát sinh đơn mới nhưng vẫn giữ dữ liệu đơn đặt phòng và giao dịch cũ.
- Quản trị viên có thể ẩn hoặc vô hiệu hóa khách sạn trên nền tảng khi cần thiết.

### Quản trị viên có thể quản lý người dùng

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên xem và quản lý toàn bộ tài khoản người dùng trong hệ thống.
- Quản trị viên có thể lọc và tìm kiếm người dùng.
- Quản trị viên có thể khóa, mở khóa, cập nhật vai trò hoặc vô hiệu hóa tài khoản theo quy định.
- Hệ thống không cho phép thao tác làm mất tài khoản quản trị cuối cùng còn hoạt động.
- Mọi thay đổi vai trò và trạng thái tài khoản được ghi log để phục vụ kiểm tra.

### Quản trị viên có thể quản lý tiện nghi

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên quản lý danh mục tiện nghi dùng chung cho toàn hệ thống.
- Quản trị viên có thể xem danh sách các tiện nghi.
- Quản trị viên có thể thêm tiện nghi mới.
- Quản trị viên có thể cập nhật thông tin tiện nghi.
- Quản trị viên có thể xóa, ẩn hoặc ngừng sử dụng tiện nghi.
- Khi tiện nghi bị ẩn, các khách sạn đã sử dụng tiện nghi đó không bị mất dữ liệu lịch sử nhưng tiện nghi không còn xuất hiện trong lựa chọn mới.

### Quản trị viên có thể xem thống kê báo cáo toàn hệ thống

- Quản trị viên phải đăng nhập trước khi xem báo cáo.
- Quản trị viên xem báo cáo toàn hệ thống hoặc lọc theo khách sạn, doanh nghiệp, thời gian và trạng thái đơn.
- Quản trị viên có thể so sánh doanh thu theo tháng, quý hoặc năm.
- Báo cáo gồm doanh thu, số lượng đơn đặt phòng, tỷ lệ lấp phòng, số đơn hủy, số đơn no-show, điểm đánh giá trung bình, hoa hồng nền tảng, tổng lợi nhuận của đối tác và payout cho đối tác.
- Dữ liệu báo cáo được dùng để kiểm tra vận hành, đối soát doanh thu và đánh giá chất lượng khách sạn.

### Quản trị viên có thể quản lý địa điểm

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem danh sách các tỉnh/thành phố và phường/xã.
- Quản trị viên có thể thêm tỉnh/thành phố hoặc phường/xã.
- Quản trị viên có thể cập nhật thông tin tỉnh/thành phố hoặc phường/xã.
- Quản trị viên có thể xóa tỉnh/thành phố hoặc phường/xã nếu địa điểm đó chưa phát sinh ràng buộc dữ liệu quan trọng.
- Nếu địa điểm đã được khách sạn hoặc đơn đặt phòng sử dụng, hệ thống có thể chỉ cho phép ẩn/ngừng sử dụng để giữ toàn vẹn dữ liệu lịch sử.

### Quản trị viên có thể quản lý hồ sơ hợp tác khách sạn từ đối tác

- Quản trị viên tiếp nhận và kiểm tra hồ sơ hợp tác từ đối tác/doanh nghiệp.
- Hệ thống lưu thông tin hợp đồng, thời hạn hợp tác, tỷ lệ hoa hồng, trạng thái hiệu lực và tài liệu pháp lý liên quan.
- Chỉ những đối tác có hồ sơ hợp lệ mới được phép đưa khách sạn lên hệ thống.
- Khi hợp đồng hết hạn hoặc bị chấm dứt, hệ thống có thể tạm ngưng quyền đăng khách sạn mới hoặc khóa trạng thái hoạt động theo quy định.

### Quản trị viên có thể xử lý đánh giá vi phạm

- Quản trị viên có quyền ẩn hoặc xử lý đánh giá vi phạm quy định hệ thống.
- Quản trị viên có thể xử lý các yêu cầu báo cáo đánh giá vi phạm do Quản lý khách sạn gửi lên nếu hệ thống có quy trình duyệt vi phạm tập trung.
- Việc xử lý đánh giá không làm mất dữ liệu lịch sử cần thiết cho kiểm tra và truy vết.

## 6. Logic tự động của hệ thống đi kèm các actor

### Hệ thống tự động bảo vệ dữ liệu đặt phòng

- Hệ thống dùng cơ chế giữ chỗ tạm thời khi Khách hàng bắt đầu đặt phòng để hạn chế overbooking.
- Hệ thống tự động giải phóng giữ chỗ nếu thanh toán thất bại, hết thời gian hoặc bị hủy.
- Hệ thống không cho phép tạo đơn mới cho khách sạn không ở trạng thái `ACTIVE`.
- Hệ thống không cho phép thao tác quản lý ảnh hưởng đến các đơn đã đặt trong tương lai.
- Chính sách đặt phòng, hủy phòng và hoàn tiền được gắn vào đơn tại thời điểm đặt để tránh thay đổi ngược lên đơn đã thanh toán.

### Hệ thống tự động cập nhật uy tín và ưu đãi

- Mỗi đơn đặt phòng chuyển sang trạng thái `CHECKED_OUT` sẽ tự động cộng điểm uy tín cho khách sạn.
- Thuật toán hiển thị khách sạn dựa trên điểm uy tín, điểm đánh giá trung bình, tỷ lệ hoàn tất đơn và mức độ vi phạm chính sách.
- Đánh giá tích cực giúp tăng độ hiển thị của khách sạn; đánh giá tiêu cực hoặc vi phạm vận hành có thể làm giảm độ ưu tiên hiển thị.
- Khi Khách hàng viết đánh giá hợp lệ, hệ thống có thể tặng điểm thưởng hoặc ưu đãi dùng cho các đơn đặt phòng tương lai.

