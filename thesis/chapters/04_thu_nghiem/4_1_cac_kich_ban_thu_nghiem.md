---
status: imported_chunk
last_updated: 2026-05-21
chapter: "04 - Thử nghiệm"
chunk: "4.1"
source_file: "../04_thu_nghiem.md"
related_memory: ../../THESIS_MEMORY.md
school_rules: ../../SCHOOL_RULES.md
---
<!-- Mảnh file được tạo từ 04_thu_nghiem.md. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này, không chỉnh file chương gốc. -->

## 4.1 Các kịch bản thử nghiệm

| Mã kịch bản | Chức năng / yêu cầu | Điều kiện tiền đề | Dữ liệu thử nghiệm | Kết quả mong đợi | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| TC-01 | Đăng ký tài khoản | Chưa có tài khoản trùng email | [Bổ sung] | Người dùng đăng ký thành công hoặc nhận thông báo lỗi phù hợp | [Cần kiểm thử] |
| TC-02 | Đăng nhập tài khoản | Tài khoản đã tồn tại và đang hoạt động | [Bổ sung] | Người dùng đăng nhập thành công và nhận token hợp lệ | [Cần kiểm thử] |
| TC-03 | Tìm kiếm khách sạn | Có dữ liệu khách sạn/phòng trong hệ thống | [Bổ sung] | Hệ thống trả về danh sách phù hợp tiêu chí tìm kiếm | [Cần kiểm thử] |
| TC-04 | Đặt phòng | Phòng còn khả dụng trong khoảng ngày chọn | [Bổ sung] | Đơn đặt phòng được tạo, dữ liệu phòng không bị đặt trùng | [Cần kiểm thử] |
| TC-05 | Hủy đặt phòng | Người dùng có đơn đặt phòng hợp lệ | [Bổ sung] | Đơn được hủy theo chính sách và ghi nhận lý do hủy | [Cần kiểm thử] |
| TC-06 | Quản lý khách sạn/phòng | Tài khoản quản trị viên hợp lệ | [Bổ sung] | Quản trị viên thêm, sửa, xóa hoặc cập nhật dữ liệu thành công | [Cần kiểm thử] |
