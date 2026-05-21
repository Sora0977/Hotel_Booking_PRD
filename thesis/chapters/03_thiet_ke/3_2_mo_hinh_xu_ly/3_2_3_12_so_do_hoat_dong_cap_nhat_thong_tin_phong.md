---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.12"
title: "Sơ đồ hoạt động cập nhật thông tin phòng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.60: Sơ đồ hoạt động cập nhật thông tin phòng


- Sơ đồ hoạt động xóa phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xóa phòng

|Admin|
start
:Nhấn nút "Xóa" tại dòng thông tin của phòng cần xóa;

|System|
:Hiển thị hộp thoại yêu cầu xác nhận hành động;

|Admin|
if (Xác nhận xóa?) then ([Đồng ý (Confirm)])
  |System|
  :Kiểm tra phòng tồn tại trong DB;

  if (Phòng tồn tại?) then ([True])
    :Thực hiện xóa dữ liệu phòng khỏi DB;
    :Hiển thị thông báo "Đã xóa phòng thành công";
    :Cập nhật lại danh sách hiển thị;
    stop
  else ([False (Không tìm thấy)])
    :Hiển thị thông báo
"Phòng này không tồn tại hoặc đã bị xóa";
    :Tự động làm mới danh sách phòng;
    stop
  endif
else ([Hủy bỏ])
  stop
endif

@enduml
```
