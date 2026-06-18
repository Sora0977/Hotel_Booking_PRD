---
status: draft
dependencies:
  - 3_2_1_11_usecase_tra_cuu_va_huy_don_dat_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.31"
title: "Sơ đồ hoạt động hủy đặt phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.79: Sơ đồ hoạt động hủy đặt phòng


- Sơ đồ hoạt động tạo tiện ích mới

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Tạo tiện ích mới

|Admin|
start
:Nhấn nút "Thêm tiện ích mới";

repeat
  :Nhập thông tin tiện ích\n(Tên, Mô tả, Icon/Hình ảnh);
  :Nhấn nút "Lưu";

  |System|
  :Kiểm tra quyền Admin\n(Include Use Case);
  if (Có quyền Admin?) then ([Có])
    :Kiểm tra dữ liệu đầu vào\n(Check Image & Duplicate Name);
    if (Hình ảnh/URL hợp lệ?) then ([Hợp lệ])
      if (Tên tiện ích đã tồn tại?) then ([Đã tồn tại])
        :Hiển thị cảnh báo\n"Tên tiện ích này đã tồn tại";
        :Yêu cầu nhập tên khác;
        |Admin|
        :[Yêu cầu nhập lại];
      else ([Hợp lệ])
        |System|
      endif
    else ([Không hợp lệ/Thiếu])
      :Hiển thị lỗi\n"Vui lòng tải lên ít nhất một hình ảnh";
      |Admin|
      :[Yêu cầu nhập lại];
    endif
  else ([Không])
    :Hiển thị thông báo lỗi quyền;
    stop
  endif
repeat while (Dữ liệu hợp lệ?) is ([False]) not ([True])

|System|
fork
  :Lưu tiện ích mới vào cơ sở dữ liệu (DB);
fork again
  :Ghi log hành động hệ thống (System Log);
end fork
:Hiển thị thông báo\n"Thêm tiện ích thành công";
stop
@enduml
```
