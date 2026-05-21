---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.29"
title: "Sơ đồ hoạt động tạo booking mới"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.77: Sơ đồ hoạt động tạo booking mới


- Sơ đồ hoạt động tra cứu Booking theo mã

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Tra cứu Booking theo mã

|Guest/User|
start
:Truy cập trang "Tra cứu đơn hàng" (Tracking);

repeat
  :Nhập Mã đặt phòng (Booking Code);
  :Nhấn nút "Tra cứu";

  |System|
  :Truy vấn cơ sở dữ liệu theo Mã Code;
  if (Tìm thấy đơn hàng?) then ([True])
    :Tải thông tin chi tiết đơn hàng;
    :Hiển thị trạng thái và thông tin Booking\n(Ngày, Phòng, Giá tiền...);
    stop
  else ([False])
    :Hiển thị thông báo lỗi\n"Mã đặt phòng không tồn tại hoặc đã bị hủy";
    |Guest/User|
    :[Nhập lại mã khác];
  endif
repeat while (Tìm thấy đơn hàng?) is ([False]) not ([True])
@enduml
```
