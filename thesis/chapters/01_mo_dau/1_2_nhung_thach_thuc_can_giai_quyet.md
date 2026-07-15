---
status: imported_chunk
last_updated: 2026-05-21
chapter: "01 - Giới thiệu"
chunk: "1.2"
source_file: "../01_mo_dau.md"
related_memory: ../../THESIS_MEMORY.md
school_rules: ../../SCHOOL_RULES.md
---
<!-- Mảnh file được tạo từ 01_mo_dau.md. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này, không chỉnh file chương gốc. -->

## 1.2 NHỮNG THÁCH THỨC CẦN GIẢI QUYẾT

Quản lý dữ liệu phức tạp: Dữ liệu liên quan đến nhiều bảng (khách sạn, phòng, đặt phòng, hủy phòng, đánh giá). Việc đảm bảo tính toàn vẹn và hiệu suất truy vấn là một thách thức.

Tìm kiếm và lọc dữ liệu: Cần tối ưu truy vấn để đảm bảo kết quả tìm kiếm trả về nhanh (≤ 3 giây) khi có nhiều tiêu chí tìm kiếm đồng thời.

Quản lý phân quyền người dùng: Cần xây dựng cơ chế phân quyền rõ ràng cho ba vai trò: Khách hàng, Quản trị viên.

Tính thân thiện với người dùng: Thiết kế giao diện trực quan dễ sử dụng, trải nghiệm nhất quán trên cả desktop, tablet và mobile.

Tối ưu hóa tìm kiếm khách sạn : Xử lý truy vấn phức tạp với khối lượng dữ liệu lớn trong thời gian thực, đòi hỏi thiết kế cơ sở dữ liệu hiệu quả và thuật toán tìm kiếm tối ưu.

Đồng bộ dữ liệu tồn kho : Quản lý số lượng phòng trống để tránh tình trạng đặt trùng phòng (overbooking), yêu cầu cơ chế khóa giao dịch.
