---
status: draft
dependencies:
  - 3_2_1_6_usecase_tra_cuu_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.16"
title: "Sơ đồ hoạt động xem chi tiết phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.64: Sơ đồ hoạt động xem chi tiết phòng


- Sơ đồ hoạt động tìm kiếm phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Tìm kiếm phòng theo từ khóa

|Guest/User|
start
:Nhập từ khóa vào ô tìm kiếm\n(ví dụ: "Deluxe", "Sea View");
:Nhấn nút "Tìm kiếm";

|System|
:Truy vấn cơ sở dữ liệu;
if (Tìm thấy kết quả?) then ([True])
  :Hiển thị danh sách kết quả tìm được;
  stop
else ([False (Không có dữ liệu)])
  :Hiển thị thông báo\n"Không tìm thấy kết quả nào phù hợp";
  stop
endif
@enduml
```
