---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.23"
title: "Sơ đồ hoạt động danh sách tất cả khách sạn"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.71: Sơ đồ hoạt động danh sách tất cả khách sạn


- Sơ đồ hoạt động xem chi tiết khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem chi tiết khách sạn

|Guest/User|
start
:Nhấn vào tên hoặc hình ảnh\ncủa một khách sạn trong danh sách;

|System|
:Thực hiện tìm khách sạn trong DB\n(theo ID);
if (Tìm thấy khách sạn?) then ([True])
  :Tải thông tin chi tiết\n(Info, Images, Amenities);
  :Hiển thị giao diện chi tiết khách sạn;
  stop
else ([False (Không tồn tại)])
  :Hiển thị thông báo lỗi 404\n"Không tìm thấy khách sạn yêu cầu";
  :Cung cấp nút quay lại danh sách;
  stop
endif
@enduml
```
