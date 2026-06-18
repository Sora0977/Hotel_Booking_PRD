---
status: draft
dependencies:
  - 3_2_1_3_usecase_quan_ly_thong_tin_ca_nhan.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.07"
title: "Sơ đồ hoạt động xem lịch sử đặt phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.55: Sơ đồ hoạt động xem lịch sử đặt phòng


- Sơ đồ hoạt động xem danh sách người dùng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem danh sách người dùng

|Admin|
start
:Chọn chức năng "Quản lý người dùng"
trên thanh menu;

|System|
:Kiểm tra quyền Admin của tài khoản;

if (Là Admin?) then ([True (Hợp lệ)])
  :Truy vấn danh sách người dùng từ DB;
  :Hiển thị danh sách người dùng lên giao diện
(ID, Tên, Email, Trạng thái...);
  stop
else ([False (Không có quyền)])
  :Từ chối truy cập;
  :Hiển thị thông báo lỗi hoặc
chuyển hướng về trang chủ;
  stop
endif

@enduml
```
