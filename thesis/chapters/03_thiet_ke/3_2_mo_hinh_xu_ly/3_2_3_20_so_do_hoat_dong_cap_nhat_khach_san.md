---
status: draft
dependencies:
  - 3_2_1_7_usecase_quan_ly_khach_san.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.20"
title: "Sơ đồ hoạt động cập nhật khách sạn"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.68: Sơ đồ hoạt động cập nhật khách sạn


- Sơ đồ hoạt động xóa khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xóa khách sạn

|Admin|
start
:Chọn nút "Xóa" tại khách sạn mong muốn;

|System|
:Hiển thị hộp thoại xác nhận;

|Admin|
if (Xác nhận xóa?) then ([Đồng ý])
  |System|
  :Kiểm tra quyền sở hữu (Owner Check);
  if (Là chủ sở hữu?) then ([True])
    :Kiểm tra khách sạn tồn tại;
    if (Khách sạn tồn tại?) then ([True])
      :Xóa dữ liệu khách sạn khỏi DB;
      :Hiển thị thông báo\n"Đã xóa khách sạn thành công";
      stop
    else ([False])
      :Hiển thị lỗi hệ thống;
      stop
    endif
  else ([False])
    :Hủy bỏ thao tác Xóa;
    :Hiển thị cảnh báo\n"Bạn không có quyền xóa khách sạn này";
    stop
  endif
else ([Hủy bỏ])
  stop
endif
@enduml
```
