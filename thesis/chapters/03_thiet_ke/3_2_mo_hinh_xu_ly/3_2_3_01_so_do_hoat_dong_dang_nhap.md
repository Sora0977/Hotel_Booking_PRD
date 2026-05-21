---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.01"
title: "Sơ đồ hoạt động đăng nhập"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.49: Sơ đồ hoạt động đăng nhập


- Sơ đồ hoạt động đăng ký

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Đăng ký tài khoản

|Guest|
start
:Truy cập trang đăng ký;

repeat
  :Nhập thông tin đăng ký
(Email, Mật khẩu, Họ tên);
  :Nhấn nút "Đăng ký";

  |System|
  :Kiểm tra định dạng dữ liệu
(Validate Form);

  if (Dữ liệu đúng định dạng?) then ([True])
    :Kiểm tra Email đã tồn tại trong DB;

    if (Email chưa tồn tại?) then ([True (Hợp lệ)])
      fork
        :Mã hóa mật khẩu;
      fork again
        :Gán quyền mặc định (Customer);
      end fork

      :Lưu thông tin tài khoản mới vào DB;
      :Hiển thị thông báo đăng ký thành công;
      stop
    else ([False (Đã tồn tại)])
      :Hiển thị lỗi "Email đã được sử dụng";
    endif
  else ([False])
    :Hiển thị lỗi Validation
(Sai định dạng/Mật khẩu yếu);
  endif

  |Guest|
  :[Yêu cầu nhập lại];
repeat while (Yêu cầu nhập lại?) is ([Yêu cầu nhập lại])

@enduml
```
