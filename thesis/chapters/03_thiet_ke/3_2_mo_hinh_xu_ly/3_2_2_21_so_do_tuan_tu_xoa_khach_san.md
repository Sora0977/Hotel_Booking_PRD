---
status: draft
dependencies:
  - 3_2_1_7_usecase_quan_ly_khach_san.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.21"
title: "Sơ đồ tuần tự xóa khách sạn"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.33: Sơ đồ tuần tự xóa khách sạn


- Sơ đồ tuần tự xem danh sách khách sạn của tôi

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem danh sách khách sạn của tôi

actor Admin
boundary MyHotelListView
control HotelService
entity HotelDB

Admin -> MyHotelListView: 1 Chọn menu "Khách sạn của tôi"
MyHotelListView -> HotelService: 2 Yêu cầu lấy danh sách khách sạn sở hữu
HotelService -> HotelService: 3 Kiểm tra quyền Admin (Check Role)

alt [Không phải Admin]
    HotelService --> MyHotelListView: 4 Từ chối truy cập
    MyHotelListView --> Admin: 5 Hiển thị lỗi phân quyền
else [Admin hợp lệ]
    HotelService -> HotelService: 6 Lấy ID Admin từ Context
    HotelService -> HotelDB: 7 Truy vấn Hotel với điều kiện (owner_id == admin_id)
    HotelDB --> HotelService: 8 Trả về danh sách khách sạn

    alt [Danh sách trống (Chưa có khách sạn nào)]
        HotelService --> MyHotelListView: 9 Trả về thông báo "Bạn chưa có khách sạn nào"
        MyHotelListView --> Admin: 10 Hiển thị thông báo & Gợi ý tạo mới
    else [Có dữ liệu (Success)]
        HotelService --> MyHotelListView: 11 Trả về danh sách khách sạn của tôi
        MyHotelListView --> Admin: 12 Hiển thị danh sách lên giao diện
    end
end

@enduml
```
