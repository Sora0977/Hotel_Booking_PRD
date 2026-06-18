---
status: draft
dependencies:
  - 3_2_1_2_usecase_dang_ky.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.02"
title: "Sơ đồ hoạt động đăng ký tài khoản"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.50: Sơ đồ hoạt động đăng ký tài khoản


- Sơ đồ hoạt động cập nhật thông tin cá nhân

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Cập nhật thông tin cá nhân

|User|
start
:Chọn chức năng "Cập nhật thông tin";

|System|
:Lấy thông tin User từ Context;

|User|
repeat
  :Chỉnh sửa các trường thông tin
(Họ tên, SĐT, Địa chỉ...);
  :Nhấn nút "Lưu thay đổi";

  |System|
  :Kiểm tra tính hợp lệ dữ liệu
(Validate Form);

  if (Dữ liệu hợp lệ?) then ([True])
    :Lưu thông tin mới vào cơ sở dữ liệu;
    :Hiển thị thông báo "Cập nhật thành công";
    stop
  else ([False])
    :Hiển thị thông báo lỗi Validation;
    :Giữ nguyên dữ liệu cũ trên Form;
  endif

  |User|
  :[Yêu cầu nhập lại];
repeat while (Yêu cầu nhập lại?) is ([Yêu cầu nhập lại])

@enduml
```
