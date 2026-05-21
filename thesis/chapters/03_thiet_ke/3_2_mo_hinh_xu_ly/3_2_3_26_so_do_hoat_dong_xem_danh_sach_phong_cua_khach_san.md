---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.26"
title: "Sơ đồ hoạt động xem danh sách phòng của khách sạn"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.74: Sơ đồ hoạt động xem danh sách phòng của khách sạn


- Sơ đồ hoạt động xem danh sách tất cả Booking

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem danh sách tất cả Booking

|Admin|
start
:Chọn chức năng "Quản lý Đặt phòng"\ntrên menu;

|System|
:Kiểm tra quyền Admin;
if (Là Admin?) then ([True])
  :Truy vấn dữ liệu các đơn đặt phòng;
  :Hiển thị danh sách Booking lên giao diện\n(Khách hàng, Phòng, Ngày, Trạng thái...);
  stop
else ([False (Không có quyền)])
  :Từ chối truy cập;
  :Hiển thị thông báo lỗi;
  stop
endif
@enduml
```
