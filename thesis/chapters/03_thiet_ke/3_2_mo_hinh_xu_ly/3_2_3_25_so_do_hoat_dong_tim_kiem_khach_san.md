---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.25"
title: "Sơ đồ hoạt động tìm kiếm khách sạn"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.73: Sơ đồ hoạt động tìm kiếm khách sạn


- Sơ đồ hoạt động xem danh sách phòng của khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem danh sách phòng của khách sạn

|Guest/User|
start
:Đang ở trang chi tiết khách sạn;
:Cuộn xuống phần "Danh sách phòng"\nhoặc nhấn nút "Xem phòng trống";

|System|
:Thực hiện tìm khách sạn trong DB\n(Validation ID);
if (ID Khách sạn hợp lệ?) then ([True])
  :Truy vấn danh sách các bản ghi Phòng (Room)\ncó hotel_id trùng khớp;
  if (Danh sách phòng trống?) then ([True])
    :Hiển thị thông báo\n"Khách sạn này chưa có phòng nào";
    stop
  else ([False])
    :Hiển thị danh sách các phòng thuộc khách sạn\n(kèm giá, loại phòng, tình trạng...);
    stop
  endif
else ([False])
  :Hiển thị thông báo lỗi (404)\nhoặc chuyển hướng về danh sách;
  stop
endif
@enduml
```
