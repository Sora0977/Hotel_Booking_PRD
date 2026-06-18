---
status: draft
dependencies:
  - 3_2_1_9_usecase_quan_ly_dat_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.27"
title: "Sơ đồ hoạt động xem danh sách tất cả Booking"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.75: Sơ đồ hoạt động xem danh sách tất cả Booking


- Sơ đồ hoạt động cập nhật trạng thái Booking

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Cập nhật trạng thái Booking

|Admin|
start
:Chọn một Booking cụ thể và\nnhấn "Cập nhật" (hoặc Check-in/Check-out);

if (Là hành động Check-in?) then ([Đúng])
  repeat
    :Nhập/Chọn số phòng (Room Number);

    |System|
    :Kiểm tra phòng đang có khách\n(Room Availability);
    if (Phòng trống?) then ([True])
      :Gán số phòng (Room Number) vào Booking;
    else ([False (Có khách)])
      :Hiển thị cảnh báo\n"Phòng này đang có người ở";
      |Admin|
      :[Chọn lại phòng];
    endif
  repeat while (Phòng trống?) is ([False]) not ([True])
else ([Sai (Check-out/Khác)])
endif

|System|
:Thực hiện tìm Booking trong DB;
if (Booking tồn tại?) then ([True])
  :Lưu trạng thái mới cho Booking\n(Cập nhật xuống DB);
  :Hiển thị thông báo "Cập nhật thành công";
  stop
else ([False])
  :Hiển thị lỗi "Booking không tồn tại";
  stop
endif
@enduml
```
