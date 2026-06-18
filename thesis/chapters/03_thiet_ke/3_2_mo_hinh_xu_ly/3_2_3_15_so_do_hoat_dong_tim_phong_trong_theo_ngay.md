---
status: draft
dependencies:
  - 3_2_1_6_usecase_tra_cuu_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.15"
title: "Sơ đồ hoạt động tìm phòng trống theo ngày"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.63: Sơ đồ hoạt động tìm phòng trống theo ngày


- Sơ đồ hoạt động xem chi tiết phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem chi tiết phòng

|Guest/User|
start
:Nhấn vào hình ảnh hoặc tên\ncủa một phòng trong danh sách;

|System|
:Truy vấn DB theo ID phòng;
if (Dữ liệu tồn tại?) then ([True])
  :Tải thông tin chi tiết\n(Info, Images, Amenities);
  :Hiển thị trang chi tiết phòng\nđầy đủ thông tin;
  stop
else ([False (Null)])
  :Hiển thị trang lỗi 404\n"Không tìm thấy phòng bạn yêu cầu";
  :Cung cấp nút quay lại danh sách;
  stop
endif
@enduml
```
