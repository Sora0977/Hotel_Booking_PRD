---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.21"
title: "Sơ đồ hoạt động xóa khách sạn"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.69: Sơ đồ hoạt động xóa khách sạn


- Sơ đồ hoạt động xem danh sách khách sạn của tôi

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Xem danh sách khách sạn của tôi

|Admin|
start
:Chọn menu "Khách sạn của tôi";

|System|
:Kiểm tra quyền Admin;
if (Là Admin?) then ([True])
  :Truy vấn DB lấy danh sách khách sạn theo Owner ID;
  if (Danh sách trống?) then ([True])
    :Hiển thị thông báo\n"Bạn chưa có khách sạn nào. Hãy tạo mới ngay!";
    stop
  else ([False])
    :Hiển thị danh sách khách sạn lên giao diện\n(Tên, Địa chỉ, Ảnh...);
    stop
  endif
else ([False])
  :Hiển thị cảnh báo "Không có quyền truy cập";
  stop
endif
@enduml
```
