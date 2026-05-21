---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.30"
title: "Sơ đồ hoạt động tra cứu booking theo mã"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.78: Sơ đồ hoạt động tra cứu booking theo mã


- Sơ đồ hoạt động hủy đặt phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Hủy đặt phòng

|Guest/User|
start
:Nhấn nút "Hủy đặt phòng"\ntại giao diện chi tiết đơn hàng;

|System|
:Hiển thị hộp thoại yêu cầu xác nhận hành động;

|Guest/User|
if (Xác nhận hủy?) then ([Đồng ý])
  |System|
  :Kiểm tra điều kiện hủy (Validation);
  if (Đủ điều kiện hủy?) then ([True])
    :Cập nhật trạng thái Booking\nthành "CANCELLED";
    fork
      :Giải phóng phòng (Restore Availability);
    fork again
      :Gửi email thông báo hủy thành công;
    end fork
    :Hiển thị thông báo\n"Đã hủy đặt phòng thành công";
    stop
  else ([False])
    :Hiển thị thông báo lỗi\n"Không thể hủy đơn hàng này (Đã check-in hoặc quá hạn)";
    stop
  endif
else ([Không/Hủy bỏ])
  stop
endif
@enduml
```
