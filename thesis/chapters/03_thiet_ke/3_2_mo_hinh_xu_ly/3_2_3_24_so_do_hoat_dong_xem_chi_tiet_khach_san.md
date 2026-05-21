---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.24"
title: "Sơ đồ hoạt động xem chi tiết khách sạn"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.72: Sơ đồ hoạt động xem chi tiết khách sạn


- Sơ đồ hoạt động tìm kiếm khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Tìm kiếm khách sạn

|Guest/User|
start
:Truy cập trang chủ hoặc giao diện tìm kiếm;

repeat
  :Nhập địa điểm cần tìm\nvà chọn ngày Check-in, Check-out;
  :Nhấn nút "Tìm kiếm";

  |System|
  :Kiểm tra tính hợp lệ ngày tháng;
  if (Ngày hợp lệ?) then ([True])
  else ([False])
    :Hiển thị cảnh báo\n"Ngày chọn không hợp lệ (Ngày trả phòng phải sau ngày nhận)";
    :Yêu cầu chọn lại ngày;
    |Guest/User|
    :[Chọn lại];
  endif
repeat while (Ngày hợp lệ?) is ([False]) not ([True])

|System|
:Truy vấn danh sách khách sạn trong DB;
if (Tìm thấy kết quả?) then ([True])
  :Hiển thị danh sách kết quả tìm kiếm lên giao diện;
  stop
else ([False (Không có dữ liệu)])
  :Hiển thị thông báo\n"Không tìm thấy khách sạn phù hợp với tiêu chí";
  stop
endif
@enduml
```
