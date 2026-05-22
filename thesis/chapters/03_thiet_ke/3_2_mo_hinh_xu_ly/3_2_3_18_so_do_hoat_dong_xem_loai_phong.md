---
status: draft
dependencies:
  - 3_2_1_6_usecase_tra_cuu_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.18"
title: "Sơ đồ hoạt động xem loại phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.66: Sơ đồ hoạt động xem loại phòng


- Sơ đồ hoạt động thêm khách sạn mới

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Thêm khách sạn mới

|Admin|
start
:Chọn chức năng "Thêm khách sạn";

repeat
  :Nhập thông tin khách sạn\n(Tên, Địa chỉ, Thành phố, Mô tả...);
  :Thực hiện Upload hình ảnh (Cloudinary);
  :Nhấn nút "Tạo mới";

  |System|
  :Kiểm tra quyền Admin;
  if (Là Admin?) then ([True])
    :Kiểm tra dữ liệu hình ảnh;
    if (Có URL hình ảnh?) then ([True])
      :Kiểm tra trùng tên & địa điểm;
      if (Dữ liệu trùng lặp?) then ([False (Hợp lệ)])
      else ([True])
        :Hiển thị cảnh báo\n"Khách sạn đã tồn tại";
        |Admin|
        :[Yêu cầu nhập lại];
      endif
    else ([False (Thiếu ảnh)])
      :Hiển thị lỗi "Vui lòng tải lên hình ảnh";
      |Admin|
      :[Yêu cầu nhập lại];
    endif
  else ([False])
    :Hiển thị lỗi: "Không có quyền truy cập";
    stop
  endif
repeat while (Dữ liệu hợp lệ?) is ([False]) not ([True])

|System|
:Lưu thông tin khách sạn mới vào DB;
:Hiển thị thông báo "Thêm khách sạn thành công";
stop
@enduml
```
