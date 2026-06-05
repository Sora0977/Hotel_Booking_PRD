# Báo cáo so sánh Nghiệp vụ: Thiết kế (PRD) vs Code thực tế (Clone)

Tài liệu này tổng hợp các điểm khác biệt giữa hai tài liệu:
1. **[Hotel booking service/Update logic.md]**: Đại diện cho thiết kế lý thuyết, luồng nghiệp vụ tiêu chuẩn và mong muốn (PRD).
2. **[Clone/toàn bộ nghiệp vụ bằng lời.md]**: Đại diện cho tình trạng code thực tế đang chạy, bao gồm cả những ràng buộc kỹ thuật và các phần chưa hoàn thiện.

---

## 1. Cấu trúc và Góc nhìn tài liệu
- **Thiết kế (PRD):** Lấy **Actor** làm trung tâm (Người dùng, Khách hàng, Doanh nghiệp, Quản lý, Admin). Các hành vi được mô tả theo quyền hạn của từng loại tài khoản.
- **Code thực tế:** Lấy **Module / Chức năng** làm trung tâm (Auth, Khách sạn, Phòng, Booking, Thanh toán...). Mô tả theo dòng chảy luồng code (Flow), cách DB lưu trữ (Schema, Transaction), phân quyền theo Role/Permission/Action.

## 2. Quy trình Đăng ký Khách sạn và Phân quyền Doanh nghiệp
- **Thiết kế (PRD):** 
  - Tách biệt rõ ràng luồng "Đăng ký tài khoản Doanh nghiệp". Cần có thông tin pháp nhân, mã số thuế... 
  - Đăng ký xong phải **chờ Admin duyệt** mới có quyền Doanh nghiệp.
  - Khách sạn tạo ra cũng ở trạng thái `PENDING_APPROVAL`, chờ Admin duyệt mới lên `ACTIVE`.
- **Code thực tế:**
  - Không có module đăng ký Doanh nghiệp chuyên biệt. User bình thường tạo khách sạn thì hệ thống tự động gán user đó thành `Owner` (chủ khách sạn) qua bảng `HotelMember`.
  - Khách sạn tạo xong không có flow chờ Admin duyệt bài bản (hoặc ít nhất không bị chặn cứng bởi logic chờ duyệt như PRD mô tả).

## 3. Quản lý Nhân sự trong Khách sạn
- **Thiết kế (PRD):**
  - Doanh nghiệp có thể phân quyền chi tiết: gán chức vụ, thăng chức, giáng chức, luân chuyển công tác giữa các chi nhánh khách sạn.
- **Code thực tế:**
  - Code chỉ có mô hình thành viên khách sạn (`HotelMember`).
  - Dù DB có enum `HotelMemberRole`, nhưng model lại không có field này. Do đó, hiện tại không có phân vai nội bộ (staff/manager) mà chỉ có quan hệ Có/Không là thành viên khách sạn. 
  - Không có chức năng luân chuyển nhân sự giữa các khách sạn.

## 4. Quản lý Địa điểm (Tỉnh/Thành phố)
- **Thiết kế (PRD):** Admin có quyền quản lý cấu trúc Địa điểm (thêm/sửa/xóa Tỉnh, Thành phố, Phường, Xã).
- **Code thực tế:** Hoàn toàn không có module Quản lý địa điểm riêng. Các trường như City, Country trong Khách sạn chỉ là chuỗi văn bản (String) nhập tự do.

## 5. Điểm uy tín, Điểm thưởng và Đánh giá (Review)
- **Thiết kế (PRD):**
  - Khách sạn được tự động cộng "điểm uy tín" khi có đơn hoàn tất. Hệ thống dùng điểm này để ưu tiên hiển thị.
  - Khách hàng review hợp lệ sẽ được cộng "điểm thưởng" hoặc ưu đãi.
- **Code thực tế:**
  - Chưa triển khai hệ thống điểm uy tín cho khách sạn, cũng không có điểm thưởng cho khách hàng. 
  - Việc sort/hiển thị public chỉ dựa trên giá, thành phố, ngày trống phòng... chứ không ưu tiên theo mức độ uy tín một cách tự động.

## 6. Cơ chế Giữ chỗ (Overbooking Prevention)
- **Thiết kế (PRD):** Nhắc đến "Giữ chỗ tạm thời" ngay khi user bắt đầu quá trình đặt phòng trước khi chuyển sang cổng thanh toán.
- **Code thực tế:** Trình bày chi tiết cơ chế kỹ thuật cho việc này:
  - Khi tạo booking, status là `PENDING`, hệ thống chạy Transaction **trừ trực tiếp** vào kho phòng (`availableRooms`).
  - Có một **Cron Job** chạy mỗi phút để tìm các booking `PENDING` quá 15 phút. Nếu khách không thanh toán kịp, Cron tự hủy booking và cộng trả lại phòng vào tồn kho.

## 7. Cổng thanh toán
- **Thiết kế (PRD):** Hỗ trợ nhiều cổng thanh toán điện tử như VNPay hoặc SePay.
- **Code thực tế:** Hiện tại code chỉ mới tích hợp duy nhất cổng **VNPAY**.

## 8. Đối soát Doanh thu & Báo cáo
- **Thiết kế (PRD):** Admin và Doanh nghiệp có hệ thống tạo "bảng đối soát định kỳ" (thường vào đầu tháng) để thanh toán tiền và hoa hồng nền tảng.
- **Code thực tế:** 
  - Có các dashboard báo cáo doanh thu và hoa hồng dựa trên các booking đã hoàn thành (COMPLETED).
  - Hoa hồng nền tảng (`commissionRate`) được "snapshot" (lưu cứng) vào đơn lúc đặt để không bị thay đổi nếu sau này khách sạn đổi gói hoa hồng.
  - Tuy nhiên, chưa có quy trình/màn hình riêng lẻ cho việc sinh "Bảng đối soát định kỳ đầu tháng" tự động như PRD nhắc đến.

## 9. Các sai số / Điểm chưa hoàn thiện trong Code so với Lý thuyết
Code thực tế còn chứa một số bug hoặc thiết kế chưa đồng nhất (mà trong PRD không mô tả vì PRD là bản thiết kế hoàn hảo):
- Validator ở frontend (Zod) đang check chặt chẽ hơn backend (VD: tồn kho, % khuyến mãi, ...).
- API logout chỉ xóa cookie ở frontend chứ chưa revoke session trong DB (commented out code).
- Thao tác xóa chính sách (Policy) bị hard-delete thay vì soft-delete như các object khác (hotel, room).
- Cơ chế Role/Permission frontend phụ thuộc vào `allowedActions` để ẩn/hiện UI, nhưng backend đôi khi thiếu Guard bảo vệ API thật.

## Tổng kết
Tài liệu **Update logic** là bản phác thảo mục tiêu kinh doanh đầy đủ, có sự tham gia của đối tác/doanh nghiệp chuyên nghiệp, quản lý địa lý, và cơ chế retention user (điểm thưởng).
Tài liệu **Toàn bộ nghiệp vụ bằng lời** cho thấy source code hiện tại đã hoàn thiện cốt lõi việc đặt phòng (tìm kiếm, trừ tồn kho, thanh toán VNPAY, gửi mail), nhưng các module phục vụ B2B (đối soát, đăng ký doanh nghiệp, phân quyền nhân sự khách sạn) hoặc các cấu trúc nâng cao (điểm uy tín) thì **chưa được implement** hoặc implement chưa đầy đủ so với PRD.
