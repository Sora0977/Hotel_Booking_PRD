# BÁO CÁO PHÂN TÍCH CHUYÊN Sâu: ĐỐI CHIẾU YÊU CẦU THIẾT KẾ (PRD) VÀ HIỆN TRẠNG MÃ NGUỒN (CODE)

Tài liệu này cung cấp một bản phân tích cực kỳ chi tiết, diễn giải bằng văn bản đầy đủ về sự khác biệt giữa hai văn bản:
1. **Thiết kế (Update logic.md)**: Đại diện cho yêu cầu nghiệp vụ lý tưởng, nhắm tới mô hình kinh doanh B2B chuyên nghiệp, có quản lý đối tác, chuỗi khách sạn và chính sách giữ chân khách hàng (Loyalty).
2. **Hiện trạng Code (toàn bộ nghiệp vụ bằng lời.md)**: Đại diện cho những gì hệ thống phần mềm đã thực sự được lập trình và đang vận hành (luồng dữ liệu, database, cronjob).

---

## 1. MÔ HÌNH TÀI KHOẢN VÀ QUY TRÌNH DOANH NGHIỆP (B2B)

### 1.1. Đăng ký và Định danh Doanh nghiệp
- **Theo Thiết Kế (PRD):** Phân chia rõ ràng giữa tài khoản "Khách hàng" và "Doanh nghiệp". Doanh nghiệp muốn lên sàn bắt buộc phải thực hiện quy trình Onboarding: cung cấp thông tin pháp nhân, mã số thuế, địa chỉ kinh doanh, người đại diện. Hồ sơ này được chuyển vào trạng thái "Chờ xét duyệt". Chỉ khi Quản trị viên (Admin) xem xét giấy tờ hợp lệ và phê duyệt, tài khoản mới được cấp quyền kinh doanh (`BUSINESS`).
- **Thực tế trong Code:** Không hề tồn tại khái niệm "Tài khoản Doanh nghiệp" với quy trình duyệt hồ sơ pháp nhân. Mọi người dùng (User) sau khi đăng ký và xác thực email đều có cơ hội tạo khách sạn. Khi một user tạo khách sạn thành công, hệ thống tự động lưu trữ bản ghi `HotelMember` và biến user đó thành "Chủ khách sạn" (Owner). 
- **Đánh giá:** Code đang đi theo hướng B2C tự do (như các nền tảng đăng tin) thay vì B2B kiểm soát chặt chẽ hợp đồng như PRD yêu cầu.

### 1.2. Phân Quyền Nhân Sự Nội Bộ Khách Sạn
- **Theo Thiết Kế (PRD):** Doanh nghiệp (tổ chức cấp cao) có quyền tạo tài khoản nhân sự, phân công nhân viên làm "Quản lý" tại từng chi nhánh khách sạn. Doanh nghiệp có thể thăng chức, giáng chức hoặc luân chuyển công tác của nhân sự từ khách sạn này sang khách sạn khác trong cùng một chuỗi.
- **Thực tế trong Code:** Cấu trúc cơ sở dữ liệu chỉ có bảng `HotelMember` (kết nối giữa User và Hotel). Dù mã nguồn có định nghĩa một danh sách các chức vụ (`HotelMemberRole`), nhưng lại **không tạo cột (field) để lưu trữ** chức vụ này vào Database. Do đó, tất cả thành viên trong khách sạn hiện tại đều bình đẳng ngang nhau về mặt dữ liệu. Không có tính năng phân cấp nhân sự, cũng như không có tính năng luân chuyển nhân sự giữa các khách sạn.

---

## 2. QUẢN LÝ KHÁCH SẠN VÀ ĐỊA ĐIỂM LƯU TRÚ

### 2.1. Phê Duyệt Khách Sạn
- **Theo Thiết Kế (PRD):** Khách sạn mới được tạo sẽ nằm ở trạng thái `PENDING_APPROVAL`. Không có một khách sạn nào được phép xuất hiện trên danh sách tìm kiếm công khai nếu Admin chưa kiểm tra và đổi trạng thái sang `ACTIVE`.
- **Thực tế trong Code:** Khách sạn do Owner tạo ra chỉ cần có Status = `ACTIVE`, chưa bị xóa (Soft-delete) và có ít nhất 1 loại phòng là sẽ lập tức xuất hiện trên trang public. Flow "Admin duyệt khách sạn" chưa được lập trình dưới dạng một rào cản kỹ thuật bắt buộc.

### 2.2. Quản Lý Khu Vực / Địa Điểm
- **Theo Thiết Kế (PRD):** Admin phải có quyền quản lý danh mục "Tỉnh/Thành phố", "Phường/Xã". Điều này giúp chuẩn hóa dữ liệu tìm kiếm, khách sạn chỉ được chọn các địa điểm đã có trong hệ thống.
- **Thực tế trong Code:** Dữ liệu địa điểm như `city`, `country` của khách sạn được thiết kế là các trường văn bản tự do (String). Hệ thống không có bất kỳ bảng dữ liệu riêng nào để quản lý hay chuẩn hóa Tỉnh/Thành. Điều này có thể dẫn đến rủi ro rác dữ liệu (ví dụ: người nhập "Hồ Chí Minh", người nhập "HCM").

### 2.3. Hệ Thống Điểm Uy Tín Khách Sạn
- **Theo Thiết Kế (PRD):** Hệ thống có thuật toán riêng: mỗi khi một đơn đặt phòng hoàn tất (Checked-out), khách sạn sẽ tự động được cộng "Điểm uy tín". Thuật toán hiển thị tìm kiếm ưu tiên những khách sạn có điểm uy tín cao.
- **Thực tế trong Code:** Hoàn toàn **trắng** logic này. Trong Database không có bất cứ trường dữ liệu nào tên là "Uy tín" (Reputation Score). Khi user tìm kiếm public, hệ thống chỉ lọc bằng ngày trống phòng, khoảng giá và sắp xếp theo thông số kỹ thuật, không hề có ưu tiên hiển thị theo "Điểm uy tín".

---

## 3. QUY TRÌNH ĐẶT PHÒNG (BOOKING) VÀ TỒN KHO

### 3.1. Cơ Chế Chống Đặt Trùng (Overbooking Prevention)
- **Theo Thiết Kế (PRD):** Nhắc đến khái niệm "Giữ chỗ tạm thời" ngay tại thời điểm khách hàng click chọn phòng và bắt đầu điền thông tin trước khi thanh toán.
- **Thực tế trong Code:** Cách xử lý của Code rất mạnh mẽ và mang tính kỹ thuật cao. Code không dùng bảng "Giữ chỗ" riêng, mà thiết kế một bảng `Inventory` (Tồn kho theo từng ngày). Khi khách bấm Đặt phòng, backend mở một Transaction (Giao dịch nguyên tử) để trừ thẳng số phòng trong `availableRooms`. Nếu trừ thành công, booking được tạo với trạng thái `PENDING`. 

### 3.2. Vòng Đời Đơn Đặt Phòng (Hủy tự động)
- **Theo Thiết Kế (PRD):** Nếu thanh toán thất bại hoặc quá giờ, giải phóng giữ chỗ.
- **Thực tế trong Code:** Sử dụng **Cron Job**. Hệ thống có một con bot chạy ngầm cứ **mỗi 1 phút 1 lần**, đi tìm tất cả các đơn hàng `PENDING` được tạo ra quá 15 phút mà chưa thanh toán. Con bot này sẽ tự động chuyển trạng thái đơn sang `CANCELLED` và lập tức cộng trả lại số lượng phòng vào kho `Inventory` để khách khác có thể đặt.

### 3.3. Tên Gọi Các Trạng Thái (Status Naming)
- **PRD dùng:** `BOOKED` (Đã đặt) -> `CHECKED_IN` -> `CHECKED_OUT`
- **Code dùng:** `PENDING` (Đang chờ thanh toán) -> `CONFIRMED` (Đã thanh toán/Xác nhận) -> `CHECKED_IN` -> `COMPLETED`. Mặc dù tên gọi khác nhau, nhưng bản chất máy trạng thái (State Machine) là tương đồng và đang hoạt động đúng logic.

---

## 4. THANH TOÁN VÀ CHÍNH SÁCH HOÀN TIỀN

### 4.1. Cổng Thanh Toán
- **Theo Thiết Kế (PRD):** Đề xuất hệ thống kết nối với nhiều cổng thanh toán như VNPay, SePay...
- **Thực tế trong Code:** Mã nguồn hiện tại mới chỉ được lập trình tích hợp duy nhất với cổng **VNPAY**. Các luồng mã hóa bảo mật tạo URL, nhận Return URL, và nhận IPN từ VNPAY về cơ bản đã hoàn thiện.

### 4.2. Hoàn Tiền (Refund)
- **Theo Thiết Kế (PRD):** Khách hàng có thể hủy đơn theo chính sách (hủy trước N ngày). Hệ thống hỗ trợ xử lý hoàn tiền một phần hoặc toàn bộ số tiền một cách tự động.
- **Thực tế trong Code:** Khi hủy đơn hợp lệ, code cập nhật trạng thái đơn thành `CANCELLED` và trả lại phòng vào kho. Tuy nhiên, **logic gọi API hoàn tiền trực tiếp qua VNPAY chưa được code**. Việc hoàn tiền lại cho khách hiện tại chỉ mang tính chất ghi nhận trên hệ thống, còn dòng tiền thực tế phải do Kế toán thao tác thủ công ngoài đời thực.

---

## 5. ĐÁNH GIÁ (REVIEW) VÀ ĐIỂM THƯỞNG KHÁCH HÀNG

### 5.1. Hệ Thống Khuyến Khích Đánh Giá (Loyalty)
- **Theo Thiết Kế (PRD):** Nhằm giữ chân người dùng (Retention), khi khách hàng viết một đánh giá hợp lệ, hệ thống sẽ tự động tặng "Điểm thưởng" hoặc gửi mã ưu đãi vào tài khoản để dùng cho lần đặt phòng tiếp theo.
- **Thực tế trong Code:** Hoàn toàn **không có** hệ thống điểm thưởng hay ví điểm (Loyalty Points) trong Database. Logic đánh giá hiện tại chỉ thuần túy là: Kiểm tra đơn đã hoàn tất (`COMPLETED`) -> Cho phép viết Review (Lưu số sao và nội dung) -> Hiển thị công khai.

### 5.2. Quản Trị Đánh Giá (Review Moderation)
- **Theo Thiết Kế (PRD):** Quản lý khách sạn có quyền "Phản hồi" (Reply) lại đánh giá của khách để chăm sóc khách hàng, đồng thời có thể "Ẩn" những đánh giá vi phạm từ ngữ hoặc tiêu chuẩn.
- **Thực tế trong Code:** Chức năng Ẩn đánh giá đã được làm tốt (chuyển cờ `isHidden = true`). Tuy nhiên, cơ sở dữ liệu và API hiện tại chưa hỗ trợ chức năng "Phản hồi đánh giá".

---

## 6. ĐỐI SOÁT DOANH THU VÀ HOA HỒNG TỰ ĐỘNG

### 6.1. Logic Tính Hoa Hồng
- **Cả PRD và Code** đều thống nhất việc nền tảng sẽ thu hoa hồng trên các giao dịch thành công.
- **Điểm sáng của Code:** Code xử lý việc này rất thông minh bằng kỹ thuật "Snapshot" (Chụp nhanh). Lúc booking được tạo, code lấy mức hoa hồng (`commissionRate`) hiện tại của khách sạn lưu cứng vào trong lòng booking đó. Nhờ vậy, nếu 3 tháng sau khách sạn đổi hợp đồng tăng/giảm phần trăm hoa hồng, các booking cũ vẫn tính đúng số tiền hoa hồng của 3 tháng trước.

### 6.2. Tạo Bảng Đối Soát Định Kỳ
- **Theo Thiết Kế (PRD):** Hệ thống được tự động hóa vào đầu mỗi tháng: Tổng hợp tất cả giao dịch tháng trước, chốt số doanh thu, trừ hoa hồng và sinh ra một "Bảng đối soát thanh toán" gửi cho Doanh nghiệp để làm căn cứ chuyển tiền (Payout).
- **Thực tế trong Code:** Hệ thống chưa được lập trình module "Bảng đối soát hàng tháng". Hiện tại Admin và Owner chỉ có các API Dashboard để xem biểu đồ thống kê tổng tiền (`revenue`) chứ không có tài liệu/hóa đơn hệ thống sinh ra tự động để chốt sổ công nợ giữa Nền tảng và Chủ khách sạn.

---

## 7. NHỮNG TÍNH NĂNG CODE ĐÃ LÀM NHƯNG PRD KHÔNG NHẮC ĐẾN

Vì PRD tập trung vào luồng khách hàng & booking, tác giả PRD đã bỏ qua rất nhiều công sức vận hành "vô hình" mà Dev thực tế phải code để một website hoạt động. Các tính năng này đã có sẵn trong source code:

1. **Hệ thống Quản Trị Nội Dung (CMS - Tin tức & Banner):** Code đã có sẵn phân hệ cho phép Admin đăng tin tức blog (News) có hỗ trợ Slug URL tự động, Lưu nháp (Draft), và đăng Banner quảng cáo có cài đặt thời gian bắt đầu/kết thúc (`startAt`, `endAt`).
2. **Hệ thống Upload và Thư viện Ảnh (Gallery):** Code được tích hợp sâu với **Cloudinary**. Mỗi User có một thư mục Gallery riêng, quản lý ảnh cá nhân. Các bức ảnh này sau đó có thể được dùng lại để làm Avatar, viết Review, hoặc thêm vào bài viết News.
3. **Luồng Liên Hệ Hỗ Trợ (Contact Form):** Khách hàng gửi biểu mẫu liên hệ ngoài trang chủ -> Code lưu vào Database -> Tự động bắn Notification Notification nội bộ cho toàn bộ Admin/Staff -> Đồng thời gọi API Mail Service gửi Email cảnh báo.
4. **Bảo Mật Bằng Phân Quyền Cấp API (Action Policy):** Tầng backend của Code đang sở hữu một hệ thống RBAC nâng cao kết hợp Action Guard (`ApiAction`). Hệ thống này kiểm tra quyền đến từng endpoint chi tiết (Chế độ ANY/ALL) mà trong tài liệu thiết kế nghiệp vụ không thể hiện được độ phức tạp này.

---

## TỔNG KẾT VÀ ĐỀ XUẤT MỞ RỘNG

* **Điểm mạnh của hệ thống hiện tại:** Đã hoàn thiện toàn bộ xương sống lõi (Core Engine) cực kỳ vững chắc, bao gồm luồng Tìm phòng -> Đặt phòng -> Xử lý tồn kho theo ngày chống trùng phòng -> Tích hợp thanh toán VNPAY -> Hủy phòng tự động bằng CronJob.
* **Những tính năng cần phát triển thêm để đạt 100% chuẩn PRD (B2B):**
   1. Bổ sung module Đăng ký hồ sơ Doanh nghiệp B2B và quy trình Admin phê duyệt.
   2. Nâng cấp bảng `HotelMember` để có tính năng phân chức vụ nội bộ và luân chuyển nhân sự.
   3. Viết thêm logic tích điểm thưởng (Loyalty) cho khách hàng sau khi review.
   4. Phát triển Module Hệ thống Đối soát tự động sinh Hóa đơn/Báo cáo công nợ đầu tháng giữa Admin và Khách sạn.
   5. Chuẩn hóa lại bảng quản trị Địa điểm (Tỉnh/Thành/Phường/Xã) vào cơ sở dữ liệu thay vì nhập tay tự do.
