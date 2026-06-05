## Logic Nghiệp Vụ Hệ Thống **Actor (Tác nhân):** Người dùng

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


Dựa trên biểu đồ Use Case từ tệp `image_c51e65.png`, dưới đây là các luồng nghiệp vụ (business logic) mô tả chi tiết những gì **Người dùng** có thể thực hiện trên hệ thống:


### 4. Đăng nhập

**Người dùng** có thể truy cập vào hệ thống thông qua chức năng **Đăng nhập**. Tùy thuộc vào vai trò, người dùng có thể tùy chọn:

- **Đăng nhập tài khoản khách hàng:** Truy cập bằng tư cách người dùng cá nhân.
    
- **Đăng nhập tài khoản doanh nghiệp:** Truy cập bằng tư cách tổ chức hoặc công ty.
    

### 5. Đăng ký

Nếu chưa có tài khoản, **Người dùng** có thể thiết lập tài khoản mới thông qua chức năng **Đăng ký**. Người dùng có hai hướng để tạo tài khoản với các yêu cầu thông tin đi kèm:

- **Đăng ký tài khoản khách hàng:** Để hoàn tất, **Người dùng** cần nhập các thông tin cơ bản:
    
    - Email.
        
    - Mật khẩu và xác nhận mật khẩu.
        
- **Đăng ký tài khoản doanh nghiệp:** Phức tạp hơn, **Người dùng** cần cung cấp đầy đủ 4 nhóm thông tin chính:
    
    - **Thông tin tài khoản:** Cung cấp Email.
        
    - **Bảo mật:** Thiết lập Mật khẩu và xác nhận mật khẩu.
        
    - **Người đại diện:** Cập nhật thông tin của người chịu trách nhiệm, bao gồm: Họ tên, Chức vụ, Số điện thoại và Email.
        
    - **Thông tin pháp lý và doanh nghiệp:** Cung cấp các chứng từ pháp lý bao gồm: Tên doanh nghiệp, Mã số thuế và Địa chỉ đăng ký kinh doanh (Địa chỉ trụ sở chính).
        

### 6. Đăng xuất

Sau khi đã xác thực và sử dụng xong hệ thống, **Người dùng** có thể thực hiện **Đăng xuất** để chấm dứt phiên làm việc và bảo vệ tài khoản.



## Logic Nghiệp Vụ Hệ Thống **Actor (Tác nhân):** Khách hàng

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


## Logic Nghiệp Vụ Hệ Thống **Actor (Tác nhân):** Quản lý 

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


### 6. Nhóm chức năng: Quản lý đặt phòng

- **Actor:** Quản lý.
    
- **Luồng nghiệp vụ:**
    
    - Để bắt đầu thao tác, Quản lý bắt buộc phải Đăng nhập tài khoản quản lý và Xem danh sách đơn đặt phòng.
        
    - Tại danh sách này, Quản lý có thể Xem chi tiết đơn đặt phòng.
        
    - Quản lý có chức năng Lọc/Tìm đơn để dễ dàng tra cứu.
        
    - Quản lý có thể Sắp xếp đơn theo nhu cầu.
        
    - Quản lý có quyền Huỷ đơn đặt phòng.
        
    - Khi tiến hành huỷ đơn, hệ thống có thể hỗ trợ các thao tác đi kèm là Hoàn tiền theo chính sách và Gửi email thông báo kèm lý do huỷ.
        
    - Quản lý có thể Cập nhật trạng thái đơn.
        
    - Các trạng thái có thể được cập nhật bao gồm: Cancel, Check-out, Check-in, hoặc No-show.
        

### 7. Nhóm chức năng: Quản lý phòng

- **Actor:** Quản lý.
    
- **Luồng nghiệp vụ:**
    
    - Quản lý bắt buộc phải Đăng nhập và Xem danh sách loại phòng để quản lý.
        
    - Quản lý có quyền Thêm loại phòng mới vào hệ thống.
        
    - Trong quá trình thêm loại phòng mới, hệ thống bắt buộc Quản lý phải thiết lập đầy đủ các thông tin: Giá, Hình ảnh, Mô tả, Sức chứa, và Số lượng phòng.
        
    - Quản lý có thể Cập nhật thông tin loại phòng hiện có.
        
    - Quản lý có quyền Ẩn/Xoá loại phòng khỏi hệ thống.
        

### 8. Nhóm chức năng: Quản lý thông tin hồ sơ

- **Actor:** Quản lý.
    
- **Luồng nghiệp vụ:**
    
    - Quản lý bắt buộc phải Đăng nhập và Xem thông tin tài khoản của mình.
        
    - Khi xem thông tin tài khoản, Quản lý có thể xem được các thông tin chi tiết về: Mã nhân viên, Vai trò, và Địa điểm công tác.
        
    - Quản lý có thể thực hiện chức năng Đổi mật khẩu tài khoản.
        
    - Quản lý có quyền Cập nhật thông tin hồ sơ của bản thân.
        
    - Khi thực hiện cập nhật thông tin, Quản lý có thể chỉnh sửa các dữ liệu bao gồm: Họ tên, Số điện thoại, Ngày tháng năm sinh, và Giới tính.



## Logic Nghiệp Vụ Hệ Thống **Actor (Tác nhân):** Doanh Nghiệp 

**1. Nhóm nghiệp vụ Đăng ký khách sạn mới**

- **Đăng nhập hệ thống:** Đây là thao tác bắt buộc đầu tiên để Doanh nghiệp bắt đầu quy trình.
    
- **Tạo đơn đăng ký:** Doanh nghiệp tiến hành tạo lập đơn đăng ký cho một khách sạn mới thuộc chuỗi của mình.
    
- **Cung cấp thông tin pháp nhân:** Doanh nghiệp bắt buộc phải điền đầy đủ các thông tin pháp nhân bao gồm tên, mã số thuế và địa điểm.
    
- **Chỉnh sửa thông tin pháp nhân:** Trong quá trình thực hiện, Doanh nghiệp có quyền thay đổi hoặc cập nhật lại các thông tin pháp lý này nếu cần thiết.
    
- **Chuyển hồ sơ:** Sau khi hoàn tất thông tin, Doanh nghiệp gửi hồ sơ lên quản trị viên (Admin) để tiến hành xét duyệt.
    


**2. Nhóm nghiệp vụ Quản lý danh mục khách sạn**

- **Xác thực tài khoản:** Doanh nghiệp bắt buộc phải đăng nhập thành công mới có thể truy cập vào giao diện quản lý danh mục khách sạn.
    
- **Theo dõi danh sách khách sạn:** Từ giao diện quản lý, Doanh nghiệp có thể lựa chọn xem danh sách toàn bộ các khách sạn hiện đang thuộc sở hữu của mình.
    
- **Đăng ký khách sạn mới:** Doanh nghiệp có thể mở rộng chuỗi bằng cách kích hoạt quy trình đăng ký thêm một khách sạn mới ngay từ trong phần quản lý danh mục. Khi thực hiện nghiệp vụ này, Doanh nghiệp bắt buộc phải hoàn thành các bước sau:
    
    - **Đăng ký địa điểm:** Cung cấp thông tin vị trí, địa chỉ cụ thể cho khách sạn mới.
        
    - **Đăng ký tên khách sạn:** Cung cấp và xác nhận tên gọi mới cho khách sạn vừa được tạo.
    

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

    
**5. Nhóm nghiệp vụ Quản lý phân công** 

- **Xác thực tài khoản:** Doanh nghiệp bắt buộc phải đăng nhập vào tài khoản doanh nghiệp để tiến hành phân công nhân sự.
    
- **Phân bổ nơi làm việc:** Khi thực hiện nghiệp vụ phân công, Doanh nghiệp bắt buộc phải chỉ định và phân công nơi làm việc hoặc nơi công tác cụ thể cho nhân viên.
    
- **Quản lý vai trò:** Đây là một khâu bắt buộc trong việc phân công. Doanh nghiệp phải gán một vai trò/chức vụ cụ thể cho nhân viên. Trong quá trình vận hành, Doanh nghiệp có thể cập nhật lại vai trò này bằng các quyết định thăng chức hoặc giáng chức nhân viên.
    
- **Luân chuyển nhân sự:** Doanh nghiệp có quyền quyết định luân chuyển công tác của nhân viên qua lại giữa các chi nhánh khách sạn khác nhau trong chuỗi.
    
- **Tra cứu danh sách:** Để hỗ trợ cho việc phân công, Doanh nghiệp có thể mở xem danh sách nhân viên hiện tại, kết hợp với các công cụ sắp xếp và lọc để tìm kiếm nhân sự phù hợp.
    

**6. Nhóm nghiệp vụ Quản lý thông tin hồ sơ** 

- **Xác thực tài khoản:** Doanh nghiệp bắt buộc phải đăng nhập hệ thống để quản lý hồ sơ.
    
- **Xem thông tin đăng ký:** Ngay khi truy cập, Doanh nghiệp mặc định sẽ xem được toàn bộ thông tin đã đăng ký của tổ chức.
    
- **Đổi mật khẩu:** Doanh nghiệp có quyền thực hiện đổi mật khẩu để bảo đảm an toàn cho tài khoản.
    
- **Cập nhật thông tin:** Doanh nghiệp có thể tiến hành chỉnh sửa hồ sơ. Quá trình này cho phép cập nhật chi tiết về thông tin người đại diện hợp pháp và thông tin pháp lý của doanh nghiệp.
    

**7. Nhóm nghiệp vụ Quản lý nhân sự** 

- **Xác thực tài khoản:** Doanh nghiệp bắt buộc đăng nhập để thao tác với dữ liệu nhân sự.
    
- **Xem danh sách nhân viên:** Doanh nghiệp có thể theo dõi danh sách toàn bộ nhân viên, có thể sử dụng thêm tính năng sắp xếp và lọc dữ liệu để quản lý dễ dàng hơn.
    
- **Thêm nhân viên mới:** Doanh nghiệp có quyền tạo lập hồ sơ cho nhân sự mới. Khi thêm mới, Doanh nghiệp bắt buộc phải khai báo đầy đủ các trường thông tin: Họ tên, Giới tính, Năm sinh, Số điện thoại và Trạng thái hoạt động.
    
- **Vô hiệu hoá tài khoản:** Doanh nghiệp có quyền khóa hoặc vô hiệu hóa tài khoản của các nhân viên không còn làm việc hoặc vi phạm quy định.


## Logic Nghiệp Vụ Hệ Thống **Actor (Tác nhân):** Admin (Quản )

**1. Trong nghiệp vụ "Quản lý đăng ký khách sạn từ đối tác"**

Admin có thể:

- Đăng nhập vào hệ thống.
    
- Xem danh sách các đăng ký khách sạn được gửi từ đối tác.
    
- Duyệt các yêu cầu đăng ký hợp lệ.
    
- Từ chối các yêu cầu đăng ký và ghi kèm theo lý do từ chối.
    
- Ẩn khách sạn trên nền tảng.
    

**2. Trong nghiệp vụ "Quản lý giao dịch và hoa hồng"**

Admin có thể:

- Đăng nhập vào hệ thống.
    
- Xem nhật ký của các giao dịch.
    
- Xem chi tiết từng giao dịch cụ thể.
    
- Lọc và tìm kiếm các giao dịch.
    
- Tính toán và lưu vết doanh thu hoa hồng thu được từ các đối tác.
    

**3. Trong nghiệp vụ "Quản lý hoạt động khách sạn"**

Admin có thể:

- Đăng nhập vào hệ thống.
    
- Xem danh sách các khách sạn hiện đang hoạt động.
    
- Lọc và tìm kiếm các khách sạn.
    
- Đình chỉ hoạt động của một khách sạn cụ thể.
    
- Ẩn hoặc vô hiệu hoá khách sạn trên nền tảng.
    

**4. Trong nghiệp vụ "Quản lý người dùng"**

Admin có thể:

- Đăng nhập vào hệ thống.
    
- Xem danh sách người dùng.
    
- Lọc và tìm kiếm người dùng.
    
- Vô hiệu hoá tài khoản của người dùng.
    

**5. Trong nghiệp vụ "Quản lý tiện nghi / Đánh giá khách sạn"** 

Admin có thể:

- Đăng nhập vào hệ thống.
    
- Xem danh sách các tiện nghi.
    
- Thêm tiện nghi mới.
    
- Cập nhật thông tin tiện nghi.
    
- Xoá tiện nghi.
    

**6. Trong nghiệp vụ "Thống kê báo cáo"**

Admin có thể:

- Đăng nhập vào hệ thống.
    
- Lọc các chỉ số thống kê theo thời gian.
    
- So sánh doanh thu theo các mốc thời gian: tháng/quý/năm.
    
- Xem tổng số lượng đơn đặt phòng.
    
- Xem tổng doanh thu của toàn bộ nền tảng.
    
- Xem tổng lợi nhuận của đối tác.


**7. Trong nghiệp vụ "Quản lý địa điểm"**

Admin có thể:

- Đăng nhập vào hệ thống.
    
- Xem danh sách các tỉnh/thành phố, phường/xã.
    
- Thêm tỉnh/thành phố, phường/xã.
    
- Cập nhật thông tin tỉnh/thành phố, phường/xã.
    
- Xoá tỉnh/thành phố, phường/xã.