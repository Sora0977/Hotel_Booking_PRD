---
status: draft
dependencies:
  - 3_2_1_7_usecase_quan_ly_khach_san.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.20"
title: "Sơ đồ tuần tự cập nhật khách sạn"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.32: Sơ đồ tuần tự cập nhật khách sạn


- Sơ đồ tuần tự xóa khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xóa khách sạn

actor Admin
boundary HotelManagementView
control HotelService
entity HotelDB

Admin -> HotelManagementView : 1 Nhấn nút "Xóa" tại khách sạn cần xóa
HotelManagementView --> Admin : 2 Hiển thị hộp thoại xác nhận xóa
Admin -> HotelManagementView : 3 Nhấn nút "Đồng ý" (Confirm)
HotelManagementView -> HotelService : 4 Gửi yêu cầu xóa khách sạn(hotelId)
HotelService -> HotelService : 5 Kiểm tra quyền sở hữu (Check Owner)

alt Không có quyền (Not Owner)
    HotelService --> HotelManagementView : 6 Trả về lỗi "Bạn không có quyền xóa khách sạn này"
    HotelManagementView --> Admin : 7 Hiển thị cảnh báo bảo mật & Hủy thao tác
else Quyền hợp lệ (Owner Verified)
    HotelService -> HotelDB : 8 Kiểm tra khách sạn tồn tại (Check Exists)
    HotelDB --> HotelService : 9 Trả về kết quả (True/False)
    alt Khách sạn không tồn tại (Not Found)
        HotelService --> HotelManagementView : 10 Trả về lỗi "Khách sạn không tồn tại"
        HotelManagementView --> Admin : 11 Hiển thị thông báo lỗi
    else Khách sạn tồn tại (Valid)
        HotelService -> HotelDB : 12 Xóa dữ liệu khách sạn
        HotelDB --> HotelService : 13 Xác nhận xóa thành công
        HotelService --> HotelManagementView : 14 Thông báo "Đã xóa khách sạn thành công"
        HotelManagementView --> Admin : 15 Hiển thị thông báo & Cập nhật danh sách
    end
end
@enduml
```
