---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.27"
title: "Sơ đồ tuần tự xem danh sách tất cả booking"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.39: Sơ đồ tuần tự xem danh sách tất cả booking


- Sơ đồ tuần tự cập nhật trạng thái booking

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Cập nhật trạng thái Booking

actor Admin
boundary BookingManagementView
control BookingService
entity BookingDB

Admin -> BookingManagementView: 1 Chọn Booking, nhập số phòng (nếu Check-in)
Admin -> BookingManagementView: 2 Nhấn nút "Cập nhật"
BookingManagementView -> BookingService: 3 Gửi yêu cầu cập nhật(bookingId, status, roomNumber)
BookingService -> BookingDB: 4 Tìm Booking theo ID
BookingDB --> BookingService: 5 Kết quả (Booking hoặc Null)

alt [Booking không tồn tại]
    BookingService --> BookingManagementView: 6 Trả về lỗi "Booking không tồn tại"
    BookingManagementView --> Admin: 7 Hiển thị thông báo lỗi & Quay lại danh sách
else [Booking tồn tại (Valid)]
    BookingService -> BookingDB: 8 Kiểm tra phòng đang có khách (Check Occupied)
    BookingDB --> BookingService: 9 Kết quả (Trống/Có người)

    alt [Phòng đang có người ở (Occupied)]
        BookingService --> BookingManagementView: 10 Trả về lỗi "Phòng này đang có người ở hoặc không khả dụng"
        BookingManagementView --> Admin: 11 Hiển thị cảnh báo & Yêu cầu chọn phòng khác
    else [Phòng trống (Hợp lệ)]
        BookingService -> BookingService: 12 Gán số phòng (Assign Room Number)
        BookingService -> BookingDB: 13 Cập nhật trạng thái mới & số phòng vào DB
        BookingDB --> BookingService: 14 Xác nhận cập nhật thành công
        BookingService --> BookingManagementView: 15 Thông báo "Cập nhật thành công"
        BookingManagementView --> Admin: 16 Hiển thị thông báo thành công
    end
end

@enduml
```
