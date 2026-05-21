---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.23"
title: "Sơ đồ tuần tự xem danh sách tất cả khách sạn"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.35: Sơ đồ tuần tự xem danh sách tất cả khách sạn


- Sơ đồ tuần tự xem chi tiết khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem chi tiết khách sạn

actor "Guest/User" as GuestUser
boundary HotelDetailView
control HotelService
entity HotelDB

GuestUser -> HotelDetailView: 1 Nhấn vào tên hoặc hình ảnh khách sạn
HotelDetailView -> HotelService: 2 Gửi yêu cầu xem chi tiết(hotelId)
HotelService -> HotelDB: 3 Tìm khách sạn theo ID
HotelDB --> HotelService: 4 Trả về kết quả (Hotel hoặc Null)

alt [Không tìm thấy khách sạn (Result Null)]
    HotelService --> HotelDetailView: 5 Trả về lỗi "Không tìm thấy khách sạn bạn yêu cầu" (404)
    HotelDetailView --> GuestUser: 6 Hiển thị thông báo lỗi & Nút quay lại danh sách
else [Tìm thấy khách sạn (Success)]
    HotelService -> HotelDB: 7 Tải thông tin chi tiết (Info, Images, Amenities)
    HotelDB --> HotelService: 8 Trả về dữ liệu đầy đủ
    HotelService --> HotelDetailView: 9 Trả về dữ liệu chi tiết khách sạn
    HotelDetailView --> GuestUser: 10 Hiển thị giao diện chi tiết (Ảnh, Tiện ích, Mô tả...)
end

@enduml
```
