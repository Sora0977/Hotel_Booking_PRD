---
status: draft
dependencies:
  - 3_2_1_use_case_chi_tiet.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3"
title: "3.2.3 Sơ đồ hoạt động (activity)"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

### 3.2.3 Sơ đồ hoạt động (activity)

- Sơ đồ hoạt động đăng nhập

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Đăng nhập

|Guest|
start
:Truy cập trang đăng nhập;

repeat
  :Nhập Email và Mật khẩu;
  :Nhấn nút "Đăng nhập";

  |System|
  :Kiểm tra Email tồn tại trong DB;

  if (Email tồn tại?) then ([True])
    :Kiểm tra Mật khẩu (So sánh Hash);

    if (Mật khẩu trùng khớp?) then ([True])
      :Kiểm tra trạng thái khóa (Activate);

      if (Activate == True?) then ([True (Hoạt động)])
        fork
          :Tạo JWT Token;
        fork again
          :Ghi log đăng nhập;
        end fork

        :Hiển thị thông báo thành công;
        :Chuyển hướng về trang chủ;
        stop
      else ([False (Bị khóa)])
        :Hiển thị thông báo "Tài khoản bị khóa";
        stop
      endif
    else ([False])
      :Hiển thị lỗi "Sai thông tin";
      :Xóa trường mật khẩu;
    endif
  else ([False])
    :Hiển thị lỗi "Sai thông tin";
    :Xóa trường mật khẩu;
  endif

  |Guest|
  :[Yêu cầu nhập lại];
repeat while (Yêu cầu nhập lại?) is ([Yêu cầu nhập lại])

@enduml
```
