---
status: draft
dependencies:
  - 3_2_1_7_usecase_quan_ly_khach_san.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.19"
title: "Sơ đồ hoạt động thêm khách sạn mới"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.67: Sơ đồ hoạt động thêm khách sạn mới


- Sơ đồ hoạt động cập nhật khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Cập nhật khách sạn

|Admin|
start
:Chọn chức năng "Chỉnh sửa"\ntại khách sạn cần cập nhật;
:Thay đổi các thông tin mong muốn\n(Tên, Mô tả, Tiện ích, Ảnh...);
:Nhấn nút "Lưu thay đổi";

|System|
:Kiểm tra quyền sở hữu (Check Owner);
if (Là chủ sở hữu?) then ([True])
  :Kiểm tra khách sạn tồn tại;
  if (Khách sạn tồn tại?) then ([True])
    if (Có URL hình ảnh hợp lệ?) then ([True])
      :Lưu thông tin mới vào cơ sở dữ liệu;
      :Hiển thị thông báo "Cập nhật thành công";
      stop
    else ([False (Thiếu ảnh)])
      :Hiển thị lỗi\n"Vui lòng tải lên ít nhất một hình ảnh";
      stop
    endif
  else ([False])
    :Hiển thị lỗi hệ thống;
    stop
  endif
else ([False])
  :Hiển thị cảnh báo\n"Bạn không có quyền chỉnh sửa khách sạn này";
  stop
endif
@enduml
```
