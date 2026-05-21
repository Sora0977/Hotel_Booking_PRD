---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.28"
title: "Sơ đồ hoạt động cập nhật trạng thái booking"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.76: Sơ đồ hoạt động cập nhật trạng thái booking


- Sơ đồ hoạt động tạo Booking mới

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Tạo Booking mới

|User|
start
:Truy cập trang chi tiết phòng\nhoặc giao diện đặt phòng;

repeat
  :Chọn ngày Check-in, Check-out\nvà số lượng phòng cần đặt;
  :Nhấn nút "Đặt phòng";

  |System|
  :Kiểm tra tính hợp lệ ngày đặt;
  if (Ngày hợp lệ?) then ([True])
    :Kiểm tra phòng trống (Availability)\nvà Số lượng còn lại (Capacity Check);
    if (Còn phòng trống?) then ([True])
    else ([False (Hết chỗ)])
      :Hiển thị thông báo\n"Phòng đã hết chỗ trong khoảng thời gian này";
      |User|
      :[Chọn lại thông tin];
    endif
  else ([False])
    :Hiển thị lỗi "Ngày đặt không hợp lệ";
    |User|
    :[Chọn lại thông tin];
  endif
repeat while (Thông tin hợp lệ?) is ([False]) not ([True])

|System|
fork
  :Tính tổng giá tiền;
fork again
  :Sinh mã đặt phòng;
end fork
:Lưu thông tin đơn hàng vào DB;
:Hiển thị thông báo "Đặt phòng thành công";
stop
@enduml
```
