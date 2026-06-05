# Báo cáo So sánh Chi tiết: Thiết kế (PRD) vs Code thực tế (Clone)

Tài liệu này cung cấp một cái nhìn đối chiếu **chuyên sâu và chi tiết** giữa hai tài liệu:
- **Thiết kế (PRD) - `Update logic.md`**: Bức tranh nghiệp vụ lý tưởng, tập trung vào mô hình kinh doanh B2B, vận hành chuỗi khách sạn và trải nghiệm khách hàng tiêu chuẩn.
- **Code thực tế - `toàn bộ nghiệp vụ bằng lời.md`**: Tình trạng source code hiện tại, cấu trúc database, các flow kỹ thuật (cronjob, token) và những hạn chế/chênh lệch đang tồn tại.

---

## 1. So sánh về Quản lý Tài khoản & Định danh

| Tiêu chí | Thiết kế (PRD) | Code thực tế (Clone) | Phân tích chênh lệch |
| :--- | :--- | :--- | :--- |
| **Phân loại Tài khoản** | Chia rõ: Khách hàng và Doanh nghiệp (đối tác). Doanh nghiệp cần nộp hồ sơ pháp nhân, MST. | Không chia cứng. Mọi User đều có thể là Khách vãng lai, Đăng nhập, hoặc Owner (khi tự tạo khách sạn). | Code thiếu quy trình định danh Doanh nghiệp B2B bài bản. Ai cũng có thể đóng vai trò "chủ khách sạn" nếu tạo khách sạn mới. |
| **Quy trình Duyệt Doanh nghiệp** | Hồ sơ doanh nghiệp ở trạng thái chờ duyệt. Admin phê duyệt xong mới có quyền `BUSINESS`. | Không có trạng thái chờ duyệt tài khoản doanh nghiệp. Quyền kiểm soát dựa trên RBAC (`Role`, `Permission`) và `Action Policy`. | Tính năng B2B onboarding chưa được implement trong code. |
| **Xác thực Đăng nhập** | Đăng nhập email/pass cơ bản. Có quên mật khẩu bằng mã/link. | Dùng JWT (Access/Refresh Token). Bắt buộc **Verify Email** trước khi login lần đầu. Có Google OAuth. | Code chi tiết và bảo mật hơn về mặt kỹ thuật (Token rotation, Hash argon2), nhưng PRD tập trung vào luồng người dùng. |

## 2. So sánh về Quản lý Khách sạn & Chuỗi

| Tiêu chí | Thiết kế (PRD) | Code thực tế (Clone) | Phân tích chênh lệch |
| :--- | :--- | :--- | :--- |
| **Đăng ký Khách sạn** | Doanh nghiệp gửi hồ sơ -> Khách sạn `PENDING_APPROVAL` -> Admin duyệt -> `ACTIVE`. | User gọi API tạo Khách sạn -> Tự động thành Owner (`HotelMember`). Thiếu flow chờ duyệt cứng ngắc. | Code cho phép tạo nhanh chóng, chưa có cơ chế block/kiểm duyệt hồ sơ khách sạn gắt gao từ Admin như PRD. |
| **Quản lý Địa điểm** | Admin thêm/sửa/xóa Tỉnh/Thành phố, Phường/Xã để khách sạn chọn. | Địa điểm (`city`, `country`) chỉ là chuỗi string lưu tự do. Không có DB Table quản lý Location. | Dữ liệu địa điểm trong code dễ bị phân mảnh (VD: "HCM", "Ho Chi Minh" khác nhau), khác với tính chuẩn hóa của PRD. |
| **Điểm Uy tín Khách sạn** | Tự động cộng điểm uy tín khi đơn hoàn tất. Dùng để ranking kết quả tìm kiếm. | Hoàn toàn **không có** trường lưu điểm uy tín hay logic tự động cộng điểm. Sort public chỉ theo giá. | Tính năng ranking thông minh dựa trên độ uy tín chưa được code. |
| **Nhân sự & Luân chuyển** | Doanh nghiệp gán vai trò (Quản lý), thăng chức, giáng chức, luân chuyển công tác chi nhánh. | Chỉ có `HotelMember` (quan hệ Có/Không). Database chưa có field phân vai trò nội bộ trong khách sạn. Không có chức năng luân chuyển. | Code chưa giải quyết bài toán quản trị nhân sự khách sạn phức tạp (Hierarchy), chỉ mới ở mức "Ai có trong danh sách thì có quyền". |

## 3. So sánh về Phòng & Tồn kho (Inventory)

| Tiêu chí | Thiết kế (PRD) | Code thực tế (Clone) | Phân tích chênh lệch |
| :--- | :--- | :--- | :--- |
| **Đóng bán phòng** | Quản lý đóng bán phòng theo ngày (bảo trì, ngưng nhận khách). | Dùng tính năng `stopSell` trong bảng `Inventory` để khóa từng ngày cụ thể. | **Khớp nhau.** Code đã support tốt nghiệp vụ này qua bảng Inventory. |
| **Xóa phòng/Hạng phòng** | Không cho phép xóa nếu ảnh hưởng đơn đặt phòng trong tương lai. | Dùng cơ chế **Soft Delete** (`deletedAt`). Code chưa block chặt chẽ việc xóa nếu có đơn tương lai. | Rủi ro ở Code: nếu soft delete hạng phòng, booking tương lai có thể gặp lỗi khi render hoặc lấy thông tin. |

## 4. So sánh về Đặt phòng & Giữ chỗ (Booking Prevention)

| Tiêu chí | Thiết kế (PRD) | Code thực tế (Clone) | Phân tích chênh lệch |
| :--- | :--- | :--- | :--- |
| **Chống Overbooking** | Kích hoạt cơ chế "giữ chỗ tạm thời" ngay khi user nhấn đặt phòng. | Dùng **Inventory Transaction**: Trừ trực tiếp `availableRooms` khi tạo booking (`PENDING`). | Về bản chất là giống nhau, nhưng code dùng cách trừ tồn thực tế thay vì bảng giữ chỗ riêng (Reservation Lock). |
| **Hủy giữ chỗ tự động** | Giải phóng giữ chỗ nếu thanh toán thất bại hoặc hết thời gian. | Có **Cron Job** chạy mỗi phút để tìm booking `PENDING` quá 15 phút, tự động `CANCELLED` và trả phòng. | **Khớp nhau.** Code đã giải quyết rất tốt bài toán này bằng Background Task (Cronjob). |
| **Trạng thái Đặt phòng** | `BOOKED`, `CHECKED_IN`, `CHECKED_OUT`, `CANCELLED`, `NO_SHOW`. | `PENDING`, `CONFIRMED` (thay cho BOOKED), `CHECKED_IN`, `COMPLETED` (thay cho CHECKED_OUT), `CANCELLED`, `NO_SHOW`. | Khác biệt về naming convention (tên trạng thái) giữa thiết kế và DB, nhưng workflow (state machine) là tương đương. |

## 5. So sánh về Thanh toán & Hoàn tiền

| Tiêu chí | Thiết kế (PRD) | Code thực tế (Clone) | Phân tích chênh lệch |
| :--- | :--- | :--- | :--- |
| **Cổng thanh toán** | Hỗ trợ VNPay, SePay. | Chỉ hỗ trợ **VNPAY**. | Code chưa mở rộng cho SePay. |
| **Hoàn tiền (Refund)** | Hệ thống xử lý hoàn tiền theo tỷ lệ chính sách hủy (hỗ trợ hoàn tiền). | Không thấy logic gọi API hoàn tiền tự động (VNPAY Refund) trong code. Nếu khách hủy, booking chuyển `CANCELLED`, nhưng tiền phải xử lý thủ công. | Tính năng Refund tự động qua ví/cổng thanh toán chưa được implement trong code. |

## 6. So sánh về Đánh giá (Review) & Ưu đãi

| Tiêu chí | Thiết kế (PRD) | Code thực tế (Clone) | Phân tích chênh lệch |
| :--- | :--- | :--- | :--- |
| **Điều kiện đánh giá** | Đơn phải ở trạng thái `CHECKED_OUT`. | Đơn phải ở trạng thái `COMPLETED` và chỉ 1 review/booking. | **Khớp nhau** (chỉ khác tên trạng thái). |
| **Kiểm duyệt Đánh giá** | Quản lý có thể phản hồi và "ẩn" đánh giá vi phạm. | Có field `isHidden`, Quản lý có thể set để ẩn đánh giá khỏi public. Không thấy nhắc đến luồng "Phản hồi đánh giá". | Tính năng reply review của Quản lý chưa có trong code. |
| **Điểm thưởng/Loyalty** | Viết đánh giá hợp lệ sẽ được cộng điểm thưởng / ưu đãi cho đơn sau. | Hoàn toàn **không có** hệ thống điểm thưởng (Loyalty points) cho khách hàng trong DB và Code. | Tính năng giữ chân khách hàng (Retention) bằng điểm thưởng chưa được phát triển. |

## 7. So sánh về Báo cáo, Đối soát & Hoa hồng

| Tiêu chí | Thiết kế (PRD) | Code thực tế (Clone) | Phân tích chênh lệch |
| :--- | :--- | :--- | :--- |
| **Tính Hoa hồng** | Hoa hồng nền tảng dựa trên đơn thành công và đơn no-show có thu tiền. | Chụp nhanh (Snapshot) `commissionRate` từ Package active của hotel vào booking lúc tạo. | Code đảm bảo tính toàn vẹn (đổi gói hoa hồng sau này không ảnh hưởng booking cũ). Rất tốt. |
| **Đối soát định kỳ** | Hệ thống tạo "Bảng đối soát định kỳ" (đầu tháng) để thanh toán cho Doanh nghiệp. | Code chỉ có API Dashboard tổng hợp doanh thu/hoa hồng (`commissionAmount`). Không có cronjob hay logic sinh Bảng Đối Soát riêng. | Code thiếu module Payout/Reconciliation chuyên nghiệp để Admin và Doanh nghiệp chốt số và chuyển tiền thực tế. |

## 8. Các Tính năng Tồn tại trong Code nhưng PRD KHÔNG đề cập

Có những khía cạnh kỹ thuật thực tế được xây dựng trong code để hệ thống chạy được, nhưng PRD bỏ qua vì mang tính "kỹ thuật ngầm":

1. **Upload & Gallery (Cloudinary)**: Code có cả một hệ thống để user quản lý thư mục ảnh (Gallery) của riêng mình, từ đó dùng ảnh này cho Avatar, Review, News.
2. **Hệ thống News (Blog) & Banner**: Code có tính năng quản trị tin tức, banner quảng cáo hiển thị public (có date range, isActive). PRD không nhắc đến nội dung marketing này.
3. **Liên hệ & Hỗ trợ (Contact)**: Code xử lý khách gửi form liên hệ, bắn notification nội bộ và gửi email cho Admin. 
4. **Hệ thống Policy/Action cực kỳ nghiêm ngặt**: Backend code sử dụng `ApiActionPolicy` với các mode `ANY` / `ALL` để cấp quyền tới từng Endpoint API rất phức tạp, nhưng Frontend lại thiếu UI tạo/sửa các Action này.
5. **Khuyến mãi (Promotion)**: Code mô tả rất kỹ việc áp mã giảm giá (Percent/Fixed), có giới hạn lượt dùng (`usedCount`), giới hạn từng user. PRD chỉ lướt qua.

## Tóm lược đánh giá độ "Chênh"

- **Mức độ hoàn thiện cốt lõi (Core Booking)**: Đạt **90%** so với PRD. Các luồng chọn phòng, trừ tồn kho, thanh toán và hủy phòng đều khớp chặt chẽ giữa thiết kế và code thực tế.
- **Mức độ hoàn thiện kinh doanh B2B (Doanh nghiệp & Đối soát)**: Đạt **30%**. Code thiếu hẳn quy trình duyệt hồ sơ doanh nghiệp B2B, quản lý nhân sự đa cấp (chỉ có Owner/Member ngang hàng), và module Đối soát thanh toán (Reconciliation) hàng tháng.
- **Mức độ hoàn thiện giữ chân khách hàng (Loyalty/Review)**: Đạt **50%**. Có đánh giá nhưng thiếu tính năng cộng điểm thưởng, thiếu hệ thống điểm uy tín để ranking khách sạn. 

*(Tài liệu này dùng để team Dev và Product đối chiếu, lên kế hoạch cho các Sprint tiếp theo nhằm bù đắp những khoảng trống tính năng giữa Code và PRD).*
