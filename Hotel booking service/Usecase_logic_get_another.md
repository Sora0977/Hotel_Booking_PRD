# Logic Nghiệp Vụ Hệ Thống Theo Actor

Tài liệu này mô tả các chức năng nghiệp vụ theo hướng: mỗi actor có thể thực hiện những hành động nào trên hệ thống. Các chức năng trùng lặp đã được gộp lại để nội dung dễ đọc và tránh lặp ý.

## 1. Actor Người dùng

Người dùng là actor tổng quát của hệ thống. Các actor Khách hàng, Doanh nghiệp, Quản lý và Quản trị viên đều có thể kế thừa các thao tác xác thực cơ bản tùy theo quyền truy cập.

### Người dùng có thể đăng ký tài khoản

- Người dùng có thể đăng ký tài khoản mới nếu chưa có tài khoản trên hệ thống.
- Người dùng có thể đăng ký tài khoản khách hàng bằng cách nhập email, mật khẩu và xác nhận mật khẩu.
- Người dùng có thể đăng ký tài khoản doanh nghiệp bằng cách cung cấp đầy đủ các nhóm thông tin sau:
  - Thông tin tài khoản gồm email đăng nhập.
  - Thông tin bảo mật gồm mật khẩu và xác nhận mật khẩu.
  - Thông tin người đại diện gồm họ tên, chức vụ, số điện thoại và email.
  - Thông tin pháp lý và doanh nghiệp gồm tên doanh nghiệp, mã số thuế và địa chỉ đăng ký kinh doanh.
- Sau khi đăng ký, hệ thống lưu thông tin tài khoản và phân loại tài khoản theo vai trò phù hợp.

### Người dùng có thể đăng nhập

- Người dùng có thể đăng nhập vào hệ thống bằng tài khoản đã có.
- Người dùng có thể đăng nhập bằng tài khoản khách hàng để truy cập hệ thống với tư cách người dùng cá nhân.
- Người dùng có thể đăng nhập bằng tài khoản doanh nghiệp để truy cập hệ thống với tư cách tổ chức hoặc công ty.
- Sau khi đăng nhập thành công, hệ thống điều hướng người dùng đến đúng giao diện theo vai trò.

### Người dùng có thể khôi phục mật khẩu

- Người dùng có thể sử dụng chức năng quên mật khẩu để khôi phục quyền truy cập.
- Hệ thống yêu cầu người dùng cung cấp thông tin tài khoản cần khôi phục.
- Sau khi xác thực hợp lệ, hệ thống hỗ trợ người dùng thiết lập lại mật khẩu hoặc lấy lại quyền truy cập.

### Người dùng có thể đổi mật khẩu

- Người dùng đã đăng nhập có thể đổi mật khẩu để tăng cường bảo mật tài khoản.
- Hệ thống yêu cầu người dùng cung cấp thông tin mật khẩu cần thiết trước khi cập nhật.
- Sau khi đổi mật khẩu thành công, người dùng sử dụng mật khẩu mới cho các lần đăng nhập sau.

### Người dùng có thể đăng xuất

- Sau khi sử dụng xong hệ thống, người dùng có thể đăng xuất để chấm dứt phiên làm việc.
- Việc đăng xuất giúp bảo vệ tài khoản, đặc biệt khi người dùng thao tác trên thiết bị dùng chung.

### Người dùng có thể tìm kiếm và lọc khách sạn

- Người dùng có thể nhập thông tin lọc/tìm kiếm để xác định tiêu chí như địa điểm, thời gian và mức giá.
- Người dùng có thể kích hoạt chức năng tìm kiếm/lọc để hệ thống trả về danh sách khách sạn hoặc phòng phù hợp.
- Người dùng có thể sắp xếp kết quả lọc/tìm kiếm để dễ so sánh và lựa chọn.

### Người dùng có thể xem thông tin khách sạn và phòng

- Người dùng có thể xem thông tin chi tiết khách sạn từ danh sách kết quả tìm kiếm.
- Người dùng có thể xem thông tin chi tiết phòng khách sạn đối với các kết quả cụ thể mà họ quan tâm.
- Các thông tin hiển thị có thể bao gồm mô tả, hình ảnh, tiện nghi, giá, sức chứa, số lượng phòng và các điều kiện liên quan.

### Người dùng có thể quản lý hồ sơ cá nhân

- Người dùng phải đăng nhập trước khi truy cập khu vực quản lý hồ sơ.
- Người dùng có thể xem thông tin cá nhân hiện tại của mình trên hệ thống.
- Người dùng có thể cập nhật thông tin cá nhân khi có thay đổi.
- Người dùng có thể đổi mật khẩu từ khu vực hồ sơ để bảo vệ tài khoản.

## 2. Actor Khách hàng

Khách hàng là người dùng sử dụng hệ thống để tìm khách sạn, lưu khách sạn yêu thích, đặt phòng, thanh toán, theo dõi lịch sử đặt phòng và đánh giá khách sạn.

### Khách hàng có thể quản lý khách sạn yêu thích

- Khách hàng phải đăng nhập trước khi quản lý danh sách yêu thích.
- Khách hàng có thể thêm khách sạn hoặc phòng quan tâm vào danh sách yêu thích để lưu trữ và xem lại sau.
- Khách hàng có thể xem danh sách các khách sạn đã được lưu vào mục yêu thích.
- Khách hàng có thể xóa khách sạn khỏi danh sách yêu thích khi không còn nhu cầu theo dõi.

### Khách hàng có thể đặt phòng và thanh toán

- Khách hàng phải đăng nhập trước khi đặt phòng.
- Khách hàng có thể nhập thông tin điều kiện để tìm kiếm và lọc các phòng/khách sạn phù hợp.
- Khách hàng có thể xem thông tin chi tiết của phòng khách sạn trước khi đặt.
- Khách hàng có thể chọn phòng muốn đặt.
- Khách hàng có thể nhập thông tin cá nhân để ghi nhận trên đơn đặt phòng.
- Khách hàng có thể ghi chú thêm các yêu cầu đặc biệt nếu có.
- Khách hàng có thể chọn phương thức thanh toán và hoàn tất giao dịch.

### Khách hàng có thể xem lịch sử đặt phòng

- Khách hàng phải đăng nhập trước khi xem lịch sử đặt phòng.
- Khách hàng có thể xem danh sách tổng hợp tất cả các đơn đặt phòng của mình.
- Khách hàng có thể xem thông tin chi tiết của một đơn đặt phòng cụ thể.
- Khách hàng có thể chuyển sang bước đánh giá khách sạn trực tiếp từ lịch sử đơn hàng nếu đơn đủ điều kiện.

### Khách hàng có thể hủy đặt phòng và yêu cầu hoàn tiền

- Khách hàng có thể thực hiện thao tác hủy đặt phòng từ lịch sử đơn hàng.
- Khách hàng có thể gửi yêu cầu hoàn tiền cho các đơn hàng hợp lệ.
- Hệ thống xử lý việc hủy đơn và hoàn tiền theo chính sách áp dụng cho đơn đặt phòng.

### Khách hàng có thể đánh giá khách sạn

- Khách hàng phải đăng nhập trước khi đánh giá khách sạn.
- Khách hàng có thể xem lại lịch sử các đơn đặt phòng ở trạng thái đã hoàn tất hoặc đã checkout.
- Khách hàng có thể viết và gửi đánh giá cho khách sạn mà mình đã trải nghiệm.

## 3. Actor Quản lý

Quản lý là actor được phân quyền để vận hành thông tin khách sạn, phòng, đơn đặt phòng, đánh giá, chính sách và hồ sơ cá nhân trong phạm vi khách sạn được giao.

### Quản lý có thể quản lý thông tin khách sạn

- Quản lý bắt buộc phải đăng nhập trước khi thao tác.
- Quản lý có thể thêm thông tin mô tả, phần giới thiệu và hình ảnh của khách sạn.
- Quản lý có thể cập nhật, chỉnh sửa lại thông tin của khách sạn.
- Quản lý có thể thêm các tiện nghi mới cho khách sạn.
- Quản lý có thể cập nhật và chỉnh sửa thông tin của các tiện nghi hiện tại.

### Quản lý có thể quản lý phòng

- Quản lý bắt buộc phải đăng nhập và xem danh sách loại phòng trước khi quản lý.
- Quản lý có thể thêm loại phòng mới vào hệ thống.
- Khi thêm loại phòng mới, hệ thống yêu cầu Quản lý nhập đầy đủ giá, hình ảnh, mô tả, sức chứa và số lượng phòng.
- Quản lý có thể cập nhật thông tin loại phòng hiện có.
- Khi cập nhật loại phòng, Quản lý có thể cập nhật hình ảnh, mô tả, giá, sức chứa và số lượng phòng.
- Quản lý có thể ẩn hoặc xóa loại phòng khỏi hệ thống.

### Quản lý có thể quản lý đặt phòng

- Quản lý bắt buộc phải đăng nhập và xem danh sách đơn đặt phòng trước khi thao tác.
- Quản lý có thể xem chi tiết thông tin của một đơn đặt phòng cụ thể.
- Quản lý có thể lọc hoặc tìm kiếm đơn đặt phòng theo nhu cầu.
- Quản lý có thể sắp xếp danh sách đơn đặt phòng để dễ theo dõi.
- Quản lý có thể hủy đơn đặt phòng.
- Khi hủy đơn, hệ thống có thể hỗ trợ hoàn tiền theo chính sách và gửi email thông báo kèm lý do hủy.
- Quản lý có thể cập nhật trạng thái đơn đặt phòng.
- Các trạng thái có thể được cập nhật gồm `Cancel`, `Check-in`, `Check-out` và `No-show`.

### Quản lý có thể quản lý đánh giá khách sạn

- Quản lý bắt buộc phải đăng nhập và xem đánh giá từ khách hàng.
- Quản lý có thể lọc các đánh giá.
- Quản lý có thể sắp xếp các đánh giá để dễ theo dõi.
- Quản lý có thể phản hồi lại các đánh giá của khách hàng.
- Quản lý có thể ẩn các đánh giá có nội dung vi phạm.

### Quản lý có thể quản lý chính sách và điều khoản

- Quản lý bắt buộc phải đăng nhập và xem danh sách chính sách, điều khoản hiện có.
- Quản lý có thể thiết lập các chính sách liên quan đến đặt phòng, hủy phòng và hoàn tiền.
- Quản lý có thể thêm các điều khoản về xử lý sự cố hoặc thiệt hại tài sản.
- Quản lý có thể chỉnh sửa nội dung các chính sách, điều khoản hiện tại của khách sạn cho phù hợp.

### Quản lý có thể quản lý thông tin hồ sơ cá nhân

- Quản lý bắt buộc phải đăng nhập và xem thông tin tài khoản của mình.
- Quản lý có thể xem các thông tin chi tiết như mã nhân viên, vai trò và địa điểm công tác.
- Quản lý có thể đổi mật khẩu tài khoản.
- Quản lý có thể cập nhật thông tin hồ sơ của bản thân.
- Khi cập nhật hồ sơ, Quản lý có thể chỉnh sửa họ tên, số điện thoại, ngày tháng năm sinh và giới tính.

## 4. Actor Doanh nghiệp

Doanh nghiệp là actor đại diện cho đối tác hoặc tổ chức sở hữu khách sạn. Doanh nghiệp có thể đăng ký khách sạn, quản lý danh mục khách sạn, nhân sự, phân công, hồ sơ và báo cáo.

### Doanh nghiệp có thể đăng ký khách sạn mới

- Doanh nghiệp bắt buộc phải đăng nhập trước khi bắt đầu quy trình.
- Doanh nghiệp có thể tạo đơn đăng ký cho một khách sạn mới thuộc chuỗi của mình.
- Doanh nghiệp bắt buộc phải cung cấp thông tin pháp nhân gồm tên doanh nghiệp, mã số thuế và địa điểm.
- Doanh nghiệp có thể chỉnh sửa hoặc cập nhật lại thông tin pháp nhân trong quá trình thực hiện nếu cần.
- Doanh nghiệp có thể đăng ký địa điểm và địa chỉ cụ thể cho khách sạn mới.
- Doanh nghiệp có thể đăng ký và xác nhận tên khách sạn mới.
- Sau khi hoàn tất thông tin, Doanh nghiệp gửi hồ sơ lên Quản trị viên để xét duyệt.

### Doanh nghiệp có thể quản lý danh mục khách sạn

- Doanh nghiệp bắt buộc phải đăng nhập thành công mới có thể truy cập giao diện quản lý danh mục khách sạn.
- Doanh nghiệp có thể xem danh sách toàn bộ các khách sạn hiện đang thuộc sở hữu của mình.
- Doanh nghiệp có thể mở rộng chuỗi bằng cách kích hoạt quy trình đăng ký thêm khách sạn mới từ phần quản lý danh mục.

### Doanh nghiệp có thể quản lý nhân sự và phân công

- Doanh nghiệp bắt buộc phải đăng nhập để thao tác với phân hệ nhân sự.
- Doanh nghiệp có thể xem danh sách toàn bộ nhân viên đang hoạt động trong hệ thống của mình.
- Doanh nghiệp có thể sử dụng tính năng sắp xếp và lọc dữ liệu để quản lý hoặc tìm kiếm nhân sự phù hợp.
- Doanh nghiệp có thể thêm nhân viên mới.
- Khi thêm nhân viên mới, Doanh nghiệp bắt buộc khai báo họ tên, giới tính, năm sinh, số điện thoại và trạng thái hoạt động.
- Khi thêm hoặc phân công nhân viên, Doanh nghiệp phải thiết lập vai trò và gán quyền tương ứng.
- Doanh nghiệp có thể phân bổ nơi làm việc hoặc nơi công tác cụ thể cho nhân viên.
- Doanh nghiệp có thể cập nhật vai trò/chức vụ của nhân viên thông qua thăng chức hoặc giáng chức.
- Doanh nghiệp có thể luân chuyển công tác của nhân viên giữa các chi nhánh khách sạn khác nhau trong chuỗi.
- Doanh nghiệp có thể thu hồi quyền đã cấp hoặc vô hiệu hóa tài khoản nhân viên khi có thay đổi nhân sự hoặc khi nhân viên vi phạm quy định.

### Doanh nghiệp có thể xem thống kê báo cáo

- Doanh nghiệp bắt buộc đăng nhập để xem dữ liệu nhạy cảm về tài chính và hoạt động.
- Doanh nghiệp có thể xem số liệu tổng quan về tổng doanh thu và tổng lợi nhuận của toàn chuỗi.
- Doanh nghiệp có thể xem doanh thu chi tiết bóc tách theo từng khách sạn cụ thể.
- Doanh nghiệp có thể kiểm tra tổng số lượng đơn đặt phòng hoặc dịch vụ đã phát sinh.
- Doanh nghiệp có thể xem chi tiết các khoản chi phí hoa hồng cần trả cho nền tảng.
- Doanh nghiệp có thể lọc dữ liệu doanh thu theo từng khoảng thời gian cụ thể để phục vụ việc phân tích.

### Doanh nghiệp có thể quản lý thông tin hồ sơ

- Doanh nghiệp bắt buộc phải đăng nhập để quản lý hồ sơ.
- Doanh nghiệp có thể xem toàn bộ thông tin đã đăng ký của tổ chức.
- Doanh nghiệp có thể đổi mật khẩu để bảo đảm an toàn cho tài khoản.
- Doanh nghiệp có thể cập nhật thông tin hồ sơ.
- Khi cập nhật hồ sơ, Doanh nghiệp có thể chỉnh sửa thông tin người đại diện hợp pháp và thông tin pháp lý của doanh nghiệp.

## 5. Actor Quản trị viên

Quản trị viên là actor quản lý toàn hệ thống, bao gồm đăng ký khách sạn từ đối tác, giao dịch, hoa hồng, trạng thái hoạt động khách sạn, người dùng, tiện nghi, báo cáo và địa điểm.

### Quản trị viên có thể quản lý đăng ký khách sạn từ đối tác

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem danh sách các đăng ký khách sạn được gửi từ đối tác.
- Quản trị viên có thể duyệt các yêu cầu đăng ký hợp lệ.
- Quản trị viên có thể từ chối các yêu cầu đăng ký và ghi kèm lý do từ chối.
- Quản trị viên có thể ẩn khách sạn trên nền tảng khi cần thiết.

### Quản trị viên có thể quản lý giao dịch và hoa hồng

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem nhật ký của các giao dịch.
- Quản trị viên có thể xem chi tiết từng giao dịch cụ thể.
- Quản trị viên có thể lọc và tìm kiếm các giao dịch.
- Quản trị viên có thể tính toán và lưu vết doanh thu hoa hồng thu được từ các đối tác.

### Quản trị viên có thể quản lý hoạt động khách sạn

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem danh sách các khách sạn hiện đang hoạt động.
- Quản trị viên có thể lọc và tìm kiếm các khách sạn.
- Quản trị viên có thể đình chỉ hoạt động của một khách sạn cụ thể.
- Quản trị viên có thể ẩn hoặc vô hiệu hóa khách sạn trên nền tảng.

### Quản trị viên có thể quản lý người dùng

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem danh sách người dùng.
- Quản trị viên có thể lọc và tìm kiếm người dùng.
- Quản trị viên có thể vô hiệu hóa tài khoản của người dùng.

### Quản trị viên có thể quản lý tiện nghi

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem danh sách các tiện nghi.
- Quản trị viên có thể thêm tiện nghi mới.
- Quản trị viên có thể cập nhật thông tin tiện nghi.
- Quản trị viên có thể xóa tiện nghi.

### Quản trị viên có thể xem thống kê báo cáo

- Quản trị viên phải đăng nhập trước khi xem báo cáo.
- Quản trị viên có thể lọc các chỉ số thống kê theo thời gian.
- Quản trị viên có thể so sánh doanh thu theo tháng, quý hoặc năm.
- Quản trị viên có thể xem tổng số lượng đơn đặt phòng.
- Quản trị viên có thể xem tổng doanh thu của toàn bộ nền tảng.
- Quản trị viên có thể xem tổng lợi nhuận của đối tác.

### Quản trị viên có thể quản lý địa điểm

- Quản trị viên phải đăng nhập trước khi thao tác.
- Quản trị viên có thể xem danh sách các tỉnh/thành phố và phường/xã.
- Quản trị viên có thể thêm tỉnh/thành phố hoặc phường/xã.
- Quản trị viên có thể cập nhật thông tin tỉnh/thành phố hoặc phường/xã.
- Quản trị viên có thể xóa tỉnh/thành phố hoặc phường/xã.
