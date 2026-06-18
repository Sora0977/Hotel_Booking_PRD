---
status: draft
dependencies:
  - 3_2_1_7_usecase_quan_ly_khach_san.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.24"
title: "Sơ đồ tuần tự xem chi tiết khách sạn"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.36: Sơ đồ tuần tự xem chi tiết khách sạn


- Sơ đồ tuần tự tìm kiếm khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Tìm kiếm khách sạn

actor "Guest/User" as GuestUser
boundary SearchHotelForm
control HotelService
entity HotelDB

GuestUser -> SearchHotelForm: 1 Nhập Địa điểm, Ngày Check-in, Check-out
GuestUser -> SearchHotelForm: 2 Nhấn nút "Tìm kiếm"
SearchHotelForm -> HotelService: 3 Gửi yêu cầu tìm kiếm(location, checkIn, checkOut)
HotelService -> HotelService: 4 Kiểm tra Logic ngày (Check-in >= Today && Check-out > Check-in)

alt [Ngày không hợp lệ (Lỗi Logic)]
    HotelService --> SearchHotelForm: 5 Trả về lỗi "Ngày chọn không hợp lệ (Ngày trả phải sau ngày nhận)"
    SearchHotelForm --> GuestUser: 6 Hiển thị cảnh báo & Yêu cầu chọn lại ngày
else [Ngày hợp lệ (Valid Date)]
    HotelService -> HotelDB: 7 Truy vấn khách sạn theo Địa điểm & Thời gian
    HotelDB --> HotelService: 8 Trả về danh sách khách sạn phù hợp
    HotelService --> SearchHotelForm: 9 Trả về danh sách kết quả tìm kiếm
    SearchHotelForm --> GuestUser: 10 Hiển thị danh sách khách sạn lên giao diện
end

@enduml
```
