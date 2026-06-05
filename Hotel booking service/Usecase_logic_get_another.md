## Khả năng tương tác của Actor: Người dùng

Dưới đây là các luồng nghiệp vụ (business logic) mô tả những gì **Người dùng** có thể thực hiện trên hệ thống, được chia theo từng nhóm chức năng:

### 1. Quản lý Tài khoản và Xác thực

Đối với nhóm chức năng này, **Người dùng** có thể thực hiện việc **Xác thực** để truy cập và sử dụng hệ thống. Cụ thể, người dùng có thể:

- **Đăng nhập** vào hệ thống bằng tài khoản đã có.
    
- **Đăng ký** một tài khoản mới.
    
- Khôi phục quyền truy cập thông qua chức năng **Quên mật khẩu**.
    

### 2. Tìm kiếm và Xem Thông tin Khách sạn

Trong quá trình tìm phòng, **Người dùng** có quyền **Xem khách sạn và phòng**. Để quá trình này diễn ra hiệu quả, người dùng có thể thực hiện các hành động bổ trợ sau:

- **Nhập thông tin lọc/tìm kiếm** để xác định các tiêu chí (ví dụ: địa điểm, thời gian, mức giá).
    
- Kích hoạt tính năng **Tìm kiếm/Lọc** để hệ thống trả về danh sách phù hợp.
    
- **Sắp xếp kết quả lọc/tìm kiếm** để dễ dàng so sánh và lựa chọn hơn.
    
- **Xem thông tin chi tiết khách sạn và phòng khách sạn** đối với các kết quả cụ thể mà họ quan tâm.
    
- **Thêm vào danh sách yêu thích** những khách sạn hoặc phòng mà họ ưng ý để tiện lưu trữ và xem lại sau.
    

### 3. Quản lý Hồ sơ Cá nhân

Để kiểm soát thông tin tài khoản của mình, **Người dùng** có thể **Quản lý thông tin hồ sơ**. Quá trình này bắt buộc người dùng phải thực hiện bước **Đăng nhập** trước. Sau khi vào khu vực quản lý, người dùng có thể:

- **Xem thông tin cá nhân** hiện tại của mình trên hệ thống.
    
- **Cập nhật thông tin cá nhân** khi có bất kỳ thay đổi nào.
    
- **Đổi mật khẩu** để tăng cường tính bảo mật cho tài khoản.



## Logic Nghiệp Vụ Hệ Thống

**Actor (Tác nhân):** Khách hàng

### 1. Đánh giá khách sạn

Khách hàng có quyền để lại nhận xét và đánh giá về khách sạn mà họ đã trải nghiệm. Để hoàn tất quy trình này, khách hàng có thể:

- Đăng nhập vào hệ thống.
    
- Xem lại lịch sử các đơn đặt phòng ở trạng thái đã hoàn tất (đã checkout).
    
- Thực hiện viết và gửi đánh giá cho khách sạn.
    

### 2. Đặt phòng và thanh toán

Khách hàng có thể tìm kiếm, lựa chọn và hoàn tất giao dịch thuê phòng khách sạn thông qua các hành động sau:

- Đăng nhập vào hệ thống.
    
- Nhập thông tin điều kiện để tìm kiếm và lọc các phòng/khách sạn phù hợp.
    
- Xem thông tin chi tiết của phòng khách sạn.
    
- Chọn phòng muốn đặt.
    
- Nhập thông tin cá nhân để ghi nhận trên đơn đặt phòng.
    
- Ghi chú thêm các yêu cầu đặc biệt (nếu có).
    
- Tiến hành thanh toán bằng cách chọn phương thức thanh toán và hoàn tất giao dịch.
    

### 3. Xem lịch sử đặt phòng

Khách hàng có thể quản lý, theo dõi tình trạng và xử lý các vấn đề liên quan đến đơn đặt phòng của mình:

- Đăng nhập vào hệ thống.
    
- Xem danh sách tổng hợp tất cả các đơn đặt phòng.
    
- Xem thông tin chi tiết của một đơn đặt phòng cụ thể.
    
- Thực hiện thao tác huỷ đặt phòng.
    
- Gửi yêu cầu hoàn tiền cho các đơn hàng hợp lệ.
    
- Chuyển sang bước đánh giá khách sạn trực tiếp từ lịch sử đơn hàng.
    

### 4. Quản lý khách sạn yêu thích

Khách hàng có thể lưu trữ và tuỳ chỉnh danh sách các khách sạn mà mình quan tâm:

- Đăng nhập vào hệ thống.
    
- Xem danh sách các khách sạn đã được lưu vào mục yêu thích.
    
- Thực hiện xoá khách sạn ra khỏi danh sách yêu thích khi không còn nhu cầu theo dõi.