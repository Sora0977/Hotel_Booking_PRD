---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.25"
title: "Sơ đồ tuần tự tìm kiếm khách sạn"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.37: Sơ đồ tuần tự tìm kiếm khách sạn


- Sơ đồ tuần tự xem danh sách phòng của khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem danh sách phòng của khách sạn

actor "Guest/User" as GuestUser
boundary HotelDetailView
control HotelService
entity HotelDB

GuestUser -> HotelDetailView: 1 Cuộn tới phần "Danh sách phòng" (hoặc nhấn Xem phòng)
HotelDetailView -> HotelService: 2 Gửi yêu cầu lấy danh sách phòng(hotelId)
HotelService -> HotelDB: 3 Kiểm tra khách sạn tồn tại (Check Hotel ID)
HotelDB --> HotelService: 4 Kết quả (Tồn tại/Không)

alt [Khách sạn không tồn tại (Invalid ID)]
    HotelService --> HotelDetailView: 5 Trả về lỗi "Không tìm thấy khách sạn" (404)
    HotelDetailView --> GuestUser: 6 Hiển thị thông báo lỗi hoặc chuyển hướng
else [Khách sạn hợp lệ (Success)]
    HotelService -> HotelDB: 7 Truy vấn các phòng có hotel_id khớp
    HotelDB --> HotelService: 8 Trả về danh sách phòng (List<Room>)
    HotelService --> HotelDetailView: 9 Trả về dữ liệu danh sách phòng
    HotelDetailView --> GuestUser: 10 Hiển thị danh sách các phòng kèm giá và tình trạng
end

@enduml
```
