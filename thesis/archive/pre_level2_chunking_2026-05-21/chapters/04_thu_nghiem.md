---
status: outline
last_updated: 2026-05-21
chapter: "04 - Thử nghiệm"
related_memory: THESIS_MEMORY.md
school_rules: ../SCHOOL_RULES.md
---

# Chương 4 — Thử nghiệm

<!-- Rules.md khuyến khích bổ sung chương thử nghiệm nếu có thời gian. Báo cáo cũ chưa có chương thử nghiệm riêng, vì vậy chương này được tạo theo khung của trường và cần được điền bằng dữ liệu kiểm thử thực tế. -->

## 4.1 Các kịch bản thử nghiệm

| Mã kịch bản | Chức năng / yêu cầu | Điều kiện tiền đề | Dữ liệu thử nghiệm | Kết quả mong đợi | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| TC-01 | Đăng ký tài khoản | Chưa có tài khoản trùng email | [Bổ sung] | Người dùng đăng ký thành công hoặc nhận thông báo lỗi phù hợp | [Cần kiểm thử] |
| TC-02 | Đăng nhập tài khoản | Tài khoản đã tồn tại và đang hoạt động | [Bổ sung] | Người dùng đăng nhập thành công và nhận token hợp lệ | [Cần kiểm thử] |
| TC-03 | Tìm kiếm khách sạn | Có dữ liệu khách sạn/phòng trong hệ thống | [Bổ sung] | Hệ thống trả về danh sách phù hợp tiêu chí tìm kiếm | [Cần kiểm thử] |
| TC-04 | Đặt phòng | Phòng còn khả dụng trong khoảng ngày chọn | [Bổ sung] | Đơn đặt phòng được tạo, dữ liệu phòng không bị đặt trùng | [Cần kiểm thử] |
| TC-05 | Hủy đặt phòng | Người dùng có đơn đặt phòng hợp lệ | [Bổ sung] | Đơn được hủy theo chính sách và ghi nhận lý do hủy | [Cần kiểm thử] |
| TC-06 | Quản lý khách sạn/phòng | Tài khoản quản trị viên hợp lệ | [Bổ sung] | Quản trị viên thêm, sửa, xóa hoặc cập nhật dữ liệu thành công | [Cần kiểm thử] |

## 4.2 Kết quả thử nghiệm các kịch bản

[Bổ sung bảng kết quả sau khi thực hiện kiểm thử. Cần ghi rõ đạt/không đạt, mô tả lỗi nếu có và minh chứng tương ứng.]

## 4.3 Xử lý các trường hợp ngoại lệ

Các trường hợp ngoại lệ cần kiểm tra tối thiểu gồm:

- Email đăng ký đã tồn tại.
- Đăng nhập sai email hoặc mật khẩu.
- Tài khoản bị khóa.
- Tìm kiếm không có khách sạn phù hợp.
- Đặt phòng khi phòng đã hết hoặc khoảng ngày không hợp lệ.
- Hủy đặt phòng ngoài điều kiện chính sách.
- Người dùng không có quyền truy cập chức năng quản trị.

## Ghi chú cho AI agent

- Không tự bịa kết quả kiểm thử.
- Nếu chưa có dữ liệu kiểm thử, giữ trạng thái [Cần kiểm thử] và cập nhật TODO.md.
- Khi bổ sung kết quả, cần đối chiếu với mục 1.4 và chương 5.1.