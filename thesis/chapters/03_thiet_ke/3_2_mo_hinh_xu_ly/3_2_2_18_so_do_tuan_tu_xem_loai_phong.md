---
status: draft
dependencies:
  - 3_2_1_6_usecase_tra_cuu_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.18"
title: "Sơ đồ tuần tự xem loại phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.30: Sơ đồ tuần tự xem loại phòng


- Sơ đồ tuần tự thêm khách sạn mới

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Thêm khách sạn mới

actor Admin
boundary AddHotelForm
control HotelService
participant CloudinaryService
entity HotelDB

Admin -> AddHotelForm : 1 Nhập thông tin (Tên, Địa chỉ...) & Chọn ảnh
Admin -> AddHotelForm : 2 Nhấn nút "Tạo mới"
AddHotelForm -> HotelService : 3 Gửi yêu cầu thêm khách sạn(data, image)
HotelService -> HotelService : 4 Kiểm tra quyền Admin (Check Role)

alt Không có ảnh hoặc Upload lỗi
    HotelService --> AddHotelForm : 5 Trả về lỗi "Vui lòng tải lên ít nhất một hình ảnh"
    AddHotelForm --> Admin : 6 Hiển thị cảnh báo thiếu ảnh
else Upload thành công
    HotelService -> CloudinaryService : 7 Upload hình ảnh
    CloudinaryService --> HotelService : 8 Trả về URL ảnh
    HotelService -> HotelDB : 9 Kiểm tra trùng lặp (Check Duplicate)
    HotelDB --> HotelService : 10 Trả về kết quả (Có/Không)
    alt Dữ liệu trùng lặp (Duplicate)
        HotelService --> AddHotelForm : 11 Trả về lỗi "Khách sạn với tên và địa chỉ này đã tồn tại"
        AddHotelForm --> Admin : 12 Hiển thị thông báo & Yêu cầu sửa lại
    else Dữ liệu hợp lệ (Success)
        HotelService -> HotelService : 13 Gán quyền sở hữu (OwnerID = CurrentAdminID)
        HotelService -> HotelDB : 14 Lưu khách sạn mới vào DB
        HotelDB --> HotelService : 15 Xác nhận lưu thành công
        HotelService --> AddHotelForm : 16 Thông báo "Thêm khách sạn thành công"
        AddHotelForm --> Admin : 17 Hiển thị thông báo thành công
    end
end
@enduml
```
