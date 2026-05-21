---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.33"
title: "Sơ đồ hoạt động cập nhật tiện ích"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.81: Sơ đồ hoạt động cập nhật tiện ích


- Sơ đồ hoạt động xóa tiện ích hệ thống

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Xóa tiện ích hệ thống

|Admin|
start
:Nhấn nút "Xóa" tại dòng tiện ích;

|System|
:Hiển thị hộp thoại xác nhận xóa;

|Admin|
:Nhấn nút "Đồng ý";

|System|
:Kiểm tra sự tồn tại (ID);
if (ID tiện ích còn tồn tại?) then ([Tồn tại])
  :Kiểm tra đang sử dụng (In Use);
  if (Tiện ích đang được sử dụng?) then ([Đang sử dụng])
    :Hiển thị cảnh báo\n"Không thể xóa tiện ích này vì đang được sử dụng\nbởi các khách sạn/phòng";
    :Hệ thống hủy bỏ lệnh xóa;
    stop
  else ([Không sử dụng])
    fork
      :Xóa tiện ích khỏi cơ sở dữ liệu (DB);
    fork again
      :Ghi log hành động hệ thống (System Log);
    end fork
    :Hiển thị thông báo\n"Đã xóa tiện ích thành công";
    stop
  endif
else ([Không tìm thấy])
  :Hiển thị thông báo\n"Tiện ích không tìm thấy";
  stop
endif
@enduml
```
