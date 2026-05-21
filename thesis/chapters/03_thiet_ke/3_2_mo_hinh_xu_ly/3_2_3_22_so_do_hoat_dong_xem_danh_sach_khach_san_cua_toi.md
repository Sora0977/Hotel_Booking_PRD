---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.22"
title: "Sơ đồ hoạt động xem danh sách khách sạn của tôi"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.70: Sơ đồ hoạt động xem danh sách khách sạn của tôi


- Sơ đồ hoạt động xem danh sách tất cả khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem danh sách tất cả khách sạn

|Guest/User|
start
:Chọn menu "Danh sách Khách sạn";

|System|
:Truy vấn cơ sở dữ liệu để lấy danh sách khách sạn;
if (Có dữ liệu khách sạn?) then ([True])
  :Hiển thị danh sách khách sạn lên giao diện\n(có thể phân trang);
  stop
else ([False (Danh sách trống)])
  :Hiển thị thông báo\n"Chưa có khách sạn nào trong hệ thống";
  stop
endif
@enduml
```
