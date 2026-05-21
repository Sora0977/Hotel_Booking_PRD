---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.09"
title: "Sơ đồ hoạt động khóa tài khoản người dùng"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.57: Sơ đồ hoạt động khóa tài khoản người dùng


- Sơ đồ hoạt động mở khóa tài khoản người dùng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Mở khóa tài khoản người dùng

|Admin|
start
:Tìm kiếm và chọn người dùng bị khóa
từ danh sách;
:Nhấn nút "Mở khóa tài khoản";

|System|
:Tìm User theo ID trong cơ sở dữ liệu;

if (Tìm thấy User?) then ([True])
  :Cập nhật trạng thái Activate thành True (Hoạt động);
  :Hiển thị thông báo
"Đã mở khóa tài khoản thành công";
  stop
else ([False (Không tồn tại)])
  :Hiển thị thông báo "User không tồn tại";
  stop
endif

@enduml
```
