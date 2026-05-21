---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.06"
title: "Sơ đồ hoạt động xóa tài khoản cá nhân"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.54: Sơ đồ hoạt động xóa tài khoản cá nhân


- Sơ đồ hoạt động xem lịch sử đặt phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem lịch sử đặt phòng

|User|
start
:Chọn mục "Lịch sử đặt phòng";

|System|
:Lấy thông tin User từ Context;
:Truy vấn danh sách Booking gắn với ID người dùng;

if (Danh sách trống?) then ([True])
  :Hiển thị thông báo
"Bạn chưa có lịch sử đặt phòng nào";
  stop
else ([False (Có dữ liệu)])
  :Sắp xếp danh sách theo thời gian;
  :Hiển thị danh sách các đơn hàng
(Ngày đặt, Khách sạn, Trạng thái...);
  stop
endif

@enduml
```
