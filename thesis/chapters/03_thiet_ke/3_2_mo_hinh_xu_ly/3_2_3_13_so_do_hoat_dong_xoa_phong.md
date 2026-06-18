---
status: draft
dependencies:
  - 3_2_1_5_usecase_quan_ly_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.13"
title: "Sơ đồ hoạt động xóa phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.61: Sơ đồ hoạt động xóa phòng


- Sơ đồ hoạt động xem danh sách tất cả phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem danh sách tất cả phòng

|Guest/User|
start
:Chọn menu "Phòng" hoặc "Danh sách phòng";

|System|
:Truy vấn cơ sở dữ liệu để lấy danh sách phòng;

if (Có dữ liệu phòng?) then ([True])
  :Hiển thị danh sách phòng lên giao diện
(Hình ảnh, Tên, Giá...);
  stop
else ([False (Danh sách trống)])
  :Hiển thị thông báo
"Chưa có phòng nào được cập nhật";
  stop
endif

@enduml
```
