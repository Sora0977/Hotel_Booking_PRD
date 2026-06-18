---
status: draft
dependencies:
  - 3_2_1_7_usecase_quan_ly_khach_san.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.19"
title: "Sơ đồ tuần tự thêm khách sạn mới"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.31: Sơ đồ tuần tự thêm khách sạn mới


- Sơ đồ tuần tự cập nhật khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Cập nhật khách sạn

actor Admin
boundary EditHotelForm
control HotelService
entity HotelDB

Admin -> EditHotelForm : 1 Chọn chức năng "Chỉnh sửa" & Thay đổi thông tin
Admin -> EditHotelForm : 2 Nhấn nút "Lưu thay đổi"
EditHotelForm -> HotelService : 3 Gửi yêu cầu cập nhật(hotelId, newData)
HotelService -> HotelService : 4 Kiểm tra quyền sở hữu (Check Owner)

alt Không có quyền (Not Owner)
    HotelService --> EditHotelForm : 5 Trả về lỗi "Bạn không có quyền chỉnh sửa khách sạn này"
    EditHotelForm --> Admin : 6 Hiển thị cảnh báo bảo mật & Chặn hành động
else Quyền hợp lệ (Owner Verified)
    HotelService -> HotelDB : 7 Kiểm tra khách sạn tồn tại (Check Exists)
    HotelDB --> HotelService : 8 Trả về kết quả (True/False)
    alt Khách sạn không tồn tại (Deleted)
        HotelService --> EditHotelForm : 9 Trả về lỗi "Khách sạn không tồn tại"
        EditHotelForm --> Admin : 10 Hiển thị thông báo lỗi
    else Khách sạn tồn tại (Valid)
        HotelService -> HotelDB : 11 Lưu thông tin mới vào DB
        HotelDB --> HotelService : 12 Xác nhận cập nhật thành công
        HotelService --> EditHotelForm : 13 Thông báo "Cập nhật thành công"
        EditHotelForm --> Admin : 14 Hiển thị thông báo thành công
    end
end
@enduml
```
