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




### 1. Nhóm chức năng: Quản lý thông tin khách sạn

- **Actor:** Quản lý
    
- **Luồng nghiệp vụ:** * Để bắt đầu, Quản lý bắt buộc phải **Đăng nhập** vào hệ thống.
    
    - Khi truy cập vào chức năng quản lý thông tin khách sạn, Quản lý có thể thực hiện các thao tác sau:
        
        - Thêm các thông tin mô tả, phần giới thiệu và hình ảnh của khách sạn.
            
        - Cập nhật, chỉnh sửa lại thông tin của khách sạn.
            
        - Thêm các tiện nghi mới cho khách sạn.
            
        - Cập nhật và chỉnh sửa thông tin của các tiện nghi hiện tại.
            

### 2. Nhóm chức năng: Quản lý phòng

- **Actor:** Quản lý
    
- **Luồng nghiệp vụ:**
    
    - Quản lý bắt buộc phải **Đăng nhập** và hệ thống sẽ yêu cầu **Xem danh sách loại phòng** để tiến hành quản lý.
        
    - Tại đây, Quản lý có thể thực hiện các thao tác:
        
        - **Thêm loại phòng mới:** Khi thực hiện hành động này, hệ thống bắt buộc Quản lý phải nhập đầy đủ các thông tin đi kèm bao gồm: thêm hình ảnh, mô tả, giá, sức chứa và số lượng phòng.
            
        - **Cập nhật thông tin loại phòng:** Tương tự như khi thêm mới, khi cập nhật, Quản lý cũng bắt buộc phải làm việc với các trường dữ liệu: cập nhật hình ảnh, mô tả, giá, sức chứa và số lượng phòng.
            
        - **Ẩn/xoá loại phòng:** Quản lý có quyền ẩn hoặc xoá bỏ một loại phòng khỏi hệ thống.
            

### 3. Nhóm chức năng: Quản lý đặt phòng

- **Actor:** Quản lý
    
- **Luồng nghiệp vụ:**
    
    - Quản lý bắt buộc phải **Đăng nhập** và **Xem danh sách đơn đặt phòng** để thao tác.
        
    - Trong quá trình quản lý đơn đặt phòng, Quản lý có quyền:
        
        - Xem chi tiết thông tin của một đơn đặt phòng cụ thể.
            
        - Lọc hoặc tìm kiếm các đơn đặt phòng theo nhu cầu.
            
        - Sắp xếp sản phẩm (sắp xếp các đơn/phòng).
            
        - Huỷ đơn đặt phòng.
            
        - **Cập nhật trạng thái đơn:** Khi cập nhật, Quản lý có thể thay đổi trạng thái của đơn thành các mốc cụ thể như: _No-show_ (Khách không đến), _Check-in_ (Nhận phòng), _Check-out_ (Trả phòng), hoặc _Cancel_ (Huỷ).
            

### 4. Nhóm chức năng: Quản lý đánh giá khách sạn

- **Actor:** Quản lý
    
- **Luồng nghiệp vụ:**
    
    - Quản lý bắt buộc phải **Đăng nhập** và **Xem đánh giá từ khách hàng**.
        
    - Đối với các đánh giá này, Quản lý có thể thực hiện các tác vụ:
        
        - Lọc các đánh giá.
            
        - Sắp xếp các đánh giá để dễ dàng theo dõi.
            
        - Phản hồi lại các đánh giá của khách hàng.
            
        - Ẩn đi các đánh giá có nội dung vi phạm.
            

### 5. Nhóm chức năng: Quản lý chính sách và điều khoản 

- **Actor:** Quản lý
    
- **Luồng nghiệp vụ:**
    
    - Quản lý bắt buộc phải **Đăng nhập** và **Xem danh sách chính sách và điều khoản** hiện có của hệ thống.
        
    - Tại màn hình quản lý này, Quản lý có quyền:
        
        - Thiết lập các chính sách liên quan đến việc đặt phòng, huỷ phòng và hoàn tiền.
            
        - Thêm các điều khoản về việc xử lý sự cố hoặc thiệt hại tài sản.
            
        - Chỉnh sửa lại nội dung các chính sách, điều khoản hiện tại của khách sạn cho phù hợp.



### Actor: Doanh nghiệp

**1. Nhóm nghiệp vụ Đăng ký khách sạn mới**

- **Đăng nhập hệ thống:** Đây là thao tác bắt buộc đầu tiên để Doanh nghiệp bắt đầu quy trình.
    
- **Tạo đơn đăng ký:** Doanh nghiệp tiến hành tạo lập đơn đăng ký cho một khách sạn mới thuộc chuỗi của mình.
    
- **Cung cấp thông tin pháp nhân:** Doanh nghiệp bắt buộc phải điền đầy đủ các thông tin pháp nhân bao gồm tên, mã số thuế và địa điểm.
    
- **Chỉnh sửa thông tin pháp nhân:** Trong quá trình thực hiện, Doanh nghiệp có quyền thay đổi hoặc cập nhật lại các thông tin pháp lý này nếu cần thiết.
    
- **Chuyển hồ sơ:** Sau khi hoàn tất thông tin, Doanh nghiệp gửi hồ sơ lên quản trị viên (Admin) để tiến hành xét duyệt.
    

**2. Nhóm nghiệp vụ Quản lý danh mục khách sạn**

- **Xác thực tài khoản:** Doanh nghiệp bắt buộc phải đăng nhập để truy cập vào không gian quản lý danh mục.
    
- **Theo dõi danh sách khách sạn:** Doanh nghiệp có thể xem toàn bộ danh sách các khách sạn hiện đang thuộc sở hữu/quản lý của mình.
    
- **Mở rộng chuỗi:** Từ giao diện quản lý, Doanh nghiệp có thể trực tiếp kích hoạt lại quy trình đăng ký thêm một khách sạn mới.
    

**3. Nhóm nghiệp vụ Quản lý nhân viên**

- **Xác thực tài khoản:** Doanh nghiệp cần đăng nhập để thao tác với phân hệ nhân sự.
    
- **Xem danh sách nhân sự:** Doanh nghiệp có thể theo dõi danh sách toàn bộ nhân viên đang hoạt động trong hệ thống của mình.
    
- **Thêm nhân viên mới:** Doanh nghiệp có quyền tạo thêm tài khoản cho nhân sự mới.
    
- **Gán quyền hạn:** Khi thực hiện thêm nhân viên mới, Doanh nghiệp bắt buộc phải thiết lập vai trò và gán quyền tương ứng (ví dụ: cấp quyền quản lý hoặc quyền nhân viên thông thường).
    
- **Bảo mật và kiểm soát:** Doanh nghiệp có quyền thu hồi các quyền đã cấp hoặc vô hiệu hóa hoàn toàn tài khoản của nhân viên khi có sự thay đổi về mặt nhân sự.
    

**4. Nhóm nghiệp vụ Thống kê báo cáo**

- **Xác thực tài khoản:** Doanh nghiệp bắt buộc đăng nhập để xem các dữ liệu nhạy cảm về tài chính và hoạt động.
    
- **Xem số liệu tổng quan:** Doanh nghiệp có thể xem số liệu về tổng doanh thu và tổng lợi nhuận của toàn chuỗi.
    
- **Xem số liệu chi tiết:** Cung cấp khả năng xem doanh thu chi tiết bóc tách cho từng khách sạn cụ thể.
    
- **Theo dõi lượng đơn:** Doanh nghiệp có thể kiểm tra tổng số lượng đơn (đặt phòng/dịch vụ) đã phát sinh.
    
- **Kiểm soát chi phí:** Cho phép Doanh nghiệp xem chi tiết các khoản chi phí hoa hồng cần trả cho nền tảng.
    
- **Sử dụng bộ lọc:** Doanh nghiệp có thể tùy chỉnh lọc dữ liệu doanh thu theo từng khoảng thời gian cụ thể để phục vụ việc phân tích.