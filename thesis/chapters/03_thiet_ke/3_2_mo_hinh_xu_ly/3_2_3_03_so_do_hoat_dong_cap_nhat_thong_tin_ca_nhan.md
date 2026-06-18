---
status: draft
dependencies:
  - 3_2_1_3_usecase_quan_ly_thong_tin_ca_nhan.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.03"
title: "Sơ đồ hoạt động cập nhật thông tin cá nhân"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.51: Sơ đồ hoạt động cập nhật thông tin cá nhân


- Sơ đồ hoạt động đổi mật khẩu

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Đổi mật khẩu

|User|
start
:Chọn chức năng "Đổi mật khẩu";

repeat
  :Nhập Mật khẩu cũ, Mật khẩu mới
và Xác nhận mật khẩu mới;
  :Nhấn nút "Đổi mật khẩu";

  |System|
  :Xác thực mật khẩu cũ
(So sánh Hash trong DB);

  if (Mật khẩu cũ chính xác?) then ([True])
    :Kiểm tra trùng mật khẩu cũ
(So sánh Pass cũ vs Pass mới);

    if (Mật khẩu mới khác mật khẩu cũ?) then ([True (Hợp lệ)])
      :Mã hóa mật khẩu mới;
      :Cập nhật mật khẩu mới vào DB;
      :Vô hiệu hóa các phiên đăng nhập cũ
(Tùy chọn chính sách);
      :Hiển thị thông báo thành công;
      stop
    else ([False (Trùng)])
      :Hiển thị cảnh báo
"Mật khẩu mới phải khác mật khẩu cũ";
    endif
  else ([False])
    :Hiển thị lỗi "Mật khẩu hiện tại không đúng";
    :Xóa các trường mật khẩu;
  endif

  |User|
  :[Yêu cầu nhập lại];
repeat while (Yêu cầu nhập lại?) is ([Yêu cầu nhập lại])

@enduml
```
