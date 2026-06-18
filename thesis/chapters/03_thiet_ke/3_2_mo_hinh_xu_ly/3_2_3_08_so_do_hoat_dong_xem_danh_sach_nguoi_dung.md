---
status: draft
dependencies:
  - 3_2_1_4_usecase_quan_tri_nguoi_dung.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.08"
title: "Sơ đồ hoạt động xem danh sách người dùng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.56: Sơ đồ hoạt động xem danh sách người dùng


- Sơ đồ hoạt động khóa tài khoản người dùng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Khóa tài khoản người dùng

|Admin|
start
:Tìm kiếm và chọn người dùng
cần khóa từ danh sách;
:Nhấn nút "Khóa tài khoản";

|System|
:Tìm User theo ID trong cơ sở dữ liệu;

if (Tìm thấy User?) then ([True])
  :Cập nhật trạng thái Activate thành False (Locked);
  :Hiển thị thông báo
"Đã khóa tài khoản thành công";
  stop
else ([False (Không tồn tại)])
  :Hiển thị thông báo "User không tồn tại";
  stop
endif

@enduml
```
