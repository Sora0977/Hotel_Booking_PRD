---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.35"
title: "Sơ đồ hoạt động gỡ tiện ích khỏi khách sạn"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.83: Sơ đồ hoạt động gỡ tiện ích khỏi khách sạn


- Sơ đồ hoạt động gỡ tiện ích khỏi Phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Gỡ tiện ích khỏi Phòng

|Admin|
start
:Truy cập vào trang cấu hình tiện ích của một phòng cụ thể;
:Nhấn nút "Gỡ bỏ" tại dòng tiện ích muốn xóa;

|System|
:Hiển thị hộp thoại xác nhận;

|Admin|
:Nhấn nút "Đồng ý";

|System|
:Kiểm tra quyền sở hữu Phòng\n(Xác minh Admin là chủ khách sạn chứa phòng);
if (Có quyền sở hữu?) then ([Hợp lệ])
  fork
    :Xóa liên kết giữa tiện ích và phòng khỏi DB\n(Không xóa tiện ích gốc);
  fork again
    :Ghi log hành động hệ thống;
  end fork
  :Hiển thị thông báo\n"Đã gỡ tiện ích khỏi phòng thành công";
  stop
else ([Không phải chủ sở hữu])
  :Hiển thị cảnh báo\n"Bạn không có quyền thay đổi tiện ích của phòng này";
  :Hủy bỏ thao tác;
  stop
endif
@enduml
```
