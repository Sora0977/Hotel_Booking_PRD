---
status: draft
dependencies:
  - 3_2_1_12_usecase_quan_ly_tien_ich.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.32"
title: "Sơ đồ hoạt động tạo tiện ích mới"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.80: Sơ đồ hoạt động tạo tiện ích mới


- Sơ đồ hoạt động cập nhật tiện ích

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Cập nhật tiện ích

|Admin|
start
:Chọn chức năng "Chỉnh sửa" tại dòng tiện ích;

repeat
  :Thay đổi các thông tin mong muốn\n(Tên, hình ảnh...);
  :Nhấn nút "Lưu thay đổi";

  |System|
  :Kiểm tra sự tồn tại (ID)\n(Truy vấn DB);
  if (ID tiện ích còn tồn tại?) then ([Tồn tại])
    :Kiểm tra trùng tên\n(So sánh với các tiện ích khác);
    if (Tên mới bị trùng?) then ([Trùng tên])
      :Hiển thị cảnh báo\n"Tên tiện ích đã được sử dụng";
      :Giữ nguyên thông tin cũ;
      |Admin|
      :[Yêu cầu nhập lại];
    else ([Hợp lệ])
      |System|
    endif
  else ([Không tìm thấy/Đã bị xóa])
    :Hiển thị lỗi\n"Tiện ích không tồn tại hoặc đã bị xóa";
    :Quay lại danh sách tiện ích;
    stop
  endif
repeat while (Dữ liệu hợp lệ?) is ([False]) not ([True])

|System|
fork
  :Cập nhật thông tin mới vào cơ sở dữ liệu (DB);
fork again
  :Ghi log hành động hệ thống (System Log);
end fork
:Hiển thị thông báo\n"Cập nhật tiện ích thành công";
stop
@enduml
```
