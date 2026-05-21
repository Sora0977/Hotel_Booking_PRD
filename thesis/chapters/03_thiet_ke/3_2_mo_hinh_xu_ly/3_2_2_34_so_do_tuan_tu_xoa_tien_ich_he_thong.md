---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.34"
title: "Sơ đồ tuần tự xóa tiện ích hệ thống"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.46: Sơ đồ tuần tự xóa tiện ích hệ thống


- Sơ đồ tuần tự gỡ tiện ích khỏi khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Gỡ tiện ích khỏi Khách sạn

actor Admin
boundary EditHotelView
control HotelService
entity HotelDB

Admin -> EditHotelView: 1 Nhấn nút "Xóa" (icon X) trên tiện ích đang có
EditHotelView -> HotelService: 2 Gửi yêu cầu gỡ tiện ích(hotelId, amenityId)
HotelService -> HotelService: 3 Kiểm tra quyền sở hữu (Check Owner)

alt [Không có quyền (Unauthorized)]
    HotelService --> EditHotelView: 4 Trả về lỗi "Bạn không có quyền sửa đổi khách sạn này"
    EditHotelView --> Admin: 5 Hiển thị cảnh báo
else [Quyền hợp lệ (Authorized)]
    HotelService -> HotelDB: 6 Kiểm tra xem tiện ích có đang gắn với KS không?
    HotelDB --> HotelService: 7 Kết quả (Có/Không)

    alt [Liên kết không tồn tại (Not Found)]
        HotelService --> EditHotelView: 8 Trả về thông báo "Tiện ích này đã được gỡ trước đó"
        EditHotelView --> Admin: 9 Cập nhật lại giao diện (tự động ẩn tiện ích)
    else [Liên kết tồn tại (Valid)]
        HotelService -> HotelDB: 10 Xóa dòng trong bảng liên kết (Delete Relation)
        HotelDB --> HotelService: 11 Xác nhận xóa liên kết thành công
        HotelService --> EditHotelView: 12 Thông báo "Đã gỡ tiện ích thành công"
        EditHotelView --> Admin: 13 Loại bỏ tiện ích khỏi danh sách hiển thị
    end
end

@enduml
```
