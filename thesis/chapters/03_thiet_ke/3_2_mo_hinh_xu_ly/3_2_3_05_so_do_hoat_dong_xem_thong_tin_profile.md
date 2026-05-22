---
status: draft
dependencies:
  - 3_2_1_3_usecase_quan_ly_thong_tin_ca_nhan.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.05"
title: "Sơ đồ hoạt động xem thông tin profile"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.53: Sơ đồ hoạt động xem thông tin profile


- Sơ đồ hoạt động xóa tài khoản cá nhân

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xóa tài khoản cá nhân

|User|
start
:Chọn chức năng "Xóa tài khoản"
trong phần cài đặt;

|System|
:Hiển thị cảnh báo và yêu cầu xác nhận;

|User|
if (Xác nhận xóa?) then ([Đồng ý (Confirm)])
  |System|
  :Lấy thông tin User từ Context;
  :Chuyển trạng thái tài khoản sang "Đã xóa"
(Soft Delete/Inactive);

  fork
    :Thực hiện đăng xuất người dùng;
  fork again
    :Chuyển hướng về trang chủ;
  end fork

  stop
else ([Hủy bỏ])
  :Quay lại màn hình cài đặt;
  stop
endif

@enduml
```
