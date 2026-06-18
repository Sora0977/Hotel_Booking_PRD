---
status: draft
dependencies:
  - 3_2_1_4_usecase_quan_tri_nguoi_dung.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.10"
title: "Sơ đồ hoạt động mở khóa tài khoản người dùng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.58: Sơ đồ hoạt động mở khóa tài khoản người dùng


- Sơ đồ hoạt động thêm phòng mới

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Thêm phòng mới

|Admin|
start
:Chọn chức năng "Thêm phòng mới"
trong giao diện quản lý;
:Nhập các thông tin cơ bản
(Tên phòng, Loại phòng, Giá, Mô tả...);

repeat
  :Thực hiện Upload hình ảnh;

  |System|
  :Xử lý tải ảnh lên Cloudinary;

  if (Ảnh hợp lệ?) then ([True])
    :Lấy về URL hình ảnh;
  else ([False (Sai định dạng/Quá lớn)])
    :Hiển thị cảnh báo "Lỗi định dạng ảnh";

    |Admin|
    :[Upload lại];
  endif
repeat while (Upload lại?) is ([Upload lại])

|Admin|
:Chọn danh sách tiện ích cho phòng;
:Nhấn nút "Lưu";

|System|
:Kiểm tra quyền sở hữu Khách sạn
(Check Owner);

if (Là chủ sở hữu?) then ([True])
  fork
    :Lưu dữ liệu phòng mới vào DB;
  fork again
    :Liên kết các tiện ích đã chọn vào phòng;
  end fork

  :Hiển thị thông báo "Thêm phòng thành công";
  stop
else ([False])
  :Hiển thị thông báo
"Bạn không có quyền thêm phòng";
  stop
endif

@enduml
```
