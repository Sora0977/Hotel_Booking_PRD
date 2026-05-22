---
status: draft
dependencies:
  - 3_2_1_3_usecase_quan_ly_thong_tin_ca_nhan.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.04"
title: "Sơ đồ hoạt động đổi mật khẩu"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.52: Sơ đồ hoạt động đổi mật khẩu


- Sơ đồ hoạt động xem thông tin Profile

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem thông tin Profile

|User|
start
:Chọn menu "Hồ sơ cá nhân";

|System|
:Lấy thông tin User từ Context;

if (Lấy được thông tin User?) then ([True])
  :Truy xuất dữ liệu chi tiết từ cơ sở dữ liệu;
  :Hiển thị giao diện thông tin profile
(Họ tên, Email, SĐT, Avatar...);
  stop
else ([False (Lỗi phiên)])
  :Chuyển hướng về trang đăng nhập;
  stop
endif

@enduml
```
