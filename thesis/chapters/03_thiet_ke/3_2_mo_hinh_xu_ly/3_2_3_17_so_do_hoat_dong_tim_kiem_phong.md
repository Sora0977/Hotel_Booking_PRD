---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.17"
title: "Sơ đồ hoạt động tìm kiếm phòng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.65: Sơ đồ hoạt động tìm kiếm phòng


- Sơ đồ hoạt động xem loại phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem loại phòng

|Guest/User|
start
:Chọn menu "Loại phòng"\nhoặc bộ lọc theo hạng phòng;

|System|
:Truy vấn dữ liệu loại phòng từ DB;
if (Có dữ liệu?) then ([True])
  :Hiển thị danh sách các loại phòng\nkèm mô tả đặc trưng;
  stop
else ([False (Danh sách trống)])
  :Hiển thị thông báo\n"Chưa có dữ liệu loại phòng";
  stop
endif
@enduml
```
