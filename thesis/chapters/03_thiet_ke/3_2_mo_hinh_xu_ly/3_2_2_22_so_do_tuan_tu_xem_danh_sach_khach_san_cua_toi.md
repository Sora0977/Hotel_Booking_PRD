---
status: draft
dependencies:
  - 3_2_1_7_usecase_quan_ly_khach_san.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.22"
title: "Sơ đồ tuần tự xem danh sách khách sạn của tôi"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.34: Sơ đồ tuần tự xem danh sách khách sạn của tôi


- Sơ đồ tuần tự xem danh sách tất cả khách sạn

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem danh sách tất cả khách sạn

actor "Guest/User" as GuestUser
boundary HotelListView
control HotelService
entity HotelDB

GuestUser -> HotelListView: 1 Chọn menu "Danh sách Khách sạn"
HotelListView -> HotelService: 2 Yêu cầu lấy toàn bộ danh sách khách sạn
HotelService -> HotelDB: 3 Truy vấn dữ liệu khách sạn (Select All)
HotelDB --> HotelService: 4 Trả về danh sách khách sạn (List<Hotel>)

alt [Danh sách trống (Empty List)]
    HotelService --> HotelListView: 5 Trả về thông báo "Chưa có khách sạn nào trong hệ thống"
    HotelListView --> GuestUser: 6 Hiển thị thông báo dữ liệu trống
else [Có dữ liệu (Success)]
    HotelService --> HotelListView: 7 Trả về danh sách (Tên, Địa chỉ, Ảnh đại diện...)
    HotelListView --> GuestUser: 8 Hiển thị danh sách khách sạn lên giao diện
end

@enduml
```
