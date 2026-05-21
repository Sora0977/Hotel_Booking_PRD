---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.3.11"
title: "Sơ đồ hoạt động thêm phòng mới"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.59: Sơ đồ hoạt động thêm phòng mới


- Sơ đồ hoạt động cập nhật thông tin phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: Quy trình Cập nhật thông tin phòng

|Admin|
start
:Chọn chức năng "Chỉnh sửa" tại một phòng cụ thể;
:Thay đổi các thông tin cần thiết
(Giá, Mô tả, Loại phòng...);

if (Có tải ảnh mới?) then ([Có])
  :Chọn file hình ảnh mới thay thế;
else ([Không])
endif

:Nhấn nút "Lưu thay đổi";

|System|
:Kiểm tra phòng tồn tại (Check ID);

if (Phòng tồn tại?) then ([True])
  if (Có file ảnh mới?) then ([True])
    :Thực hiện Upload hình ảnh mới;

    if (Upload thành công?) then ([True])
      :Cập nhật URL ảnh mới;
    else ([False (Lỗi định dạng)])
      :Hiển thị cảnh báo lỗi định dạng ảnh;
      stop
    endif
  else ([False])
    :Giữ nguyên URL ảnh cũ;
  endif

  :Lưu thông tin mới vào cơ sở dữ liệu;
  :Hiển thị thông báo "Cập nhật thành công";
  stop
else ([False (Không tìm thấy)])
  :Hiển thị lỗi "Phòng này không còn tồn tại";
  :Đưa người dùng quay lại danh sách phòng;
  stop
endif

@enduml
```
