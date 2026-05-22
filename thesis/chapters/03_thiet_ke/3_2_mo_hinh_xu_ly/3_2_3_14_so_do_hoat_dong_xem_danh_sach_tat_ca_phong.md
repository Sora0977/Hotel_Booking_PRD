---
status: draft
dependencies:
  - 3_2_1_5_usecase_quan_ly_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.14"
title: "Sơ đồ hoạt động xem danh sách tất cả phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.62: Sơ đồ hoạt động xem danh sách tất cả phòng


- Sơ đồ hoạt động tìm phòng trống theo ngày

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Tìm phòng trống theo ngày

|Guest/User|
start
:Truy cập giao diện tìm kiếm;

repeat
  :Chọn ngày Check-in và Check-out;
  :Nhấn nút "Tìm kiếm";

  |System|
  :Kiểm tra tính hợp lệ ngày tháng;

  if (Ngày hợp lệ?) then ([True])
  else ([False])
    :Hiển thị cảnh báo
"Ngày không hợp lệ";

    |Guest/User|
    :[Yêu cầu chọn lại];
  endif
repeat while (Chọn lại?) is ([Yêu cầu chọn lại])

|System|
:Truy vấn DB (Lọc phòng đã đặt);

if (Có phòng trống?) then ([True])
  :Hiển thị danh sách phòng trống phù hợp;
else ([False (Hết phòng)])
  :Hiển thị thông báo
"Không còn phòng trống trong khoảng thời gian này";
endif

stop

@enduml
```
