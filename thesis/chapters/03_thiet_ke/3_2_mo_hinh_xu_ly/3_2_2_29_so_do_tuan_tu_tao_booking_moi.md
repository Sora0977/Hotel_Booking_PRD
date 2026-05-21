---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.29"
title: "Sơ đồ tuần tự tạo booking mới"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.41: Sơ đồ tuần tự tạo booking mới


- Sơ đồ tuần tự tra cứu booking theo mã

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Tra cứu Booking theo mã

actor "Customer/Admin" as User
boundary LookupView
control BookingService
entity BookingDB

User -> LookupView: 1 Truy cập trang tra cứu & Nhập mã đặt phòng (Ref Code)
User -> LookupView: 2 Nhấn nút "Tìm kiếm"
LookupView -> BookingService: 3 Gửi yêu cầu tra cứu(refCode)
BookingService -> BookingDB: 4 Truy vấn Booking theo Reference Code
BookingDB --> BookingService: 5 Kết quả (Booking hoặc Null)

alt [Mã đặt phòng không tồn tại (Not Found)]
    BookingService --> LookupView: 6 Trả về lỗi "Mã đặt phòng không tồn tại"
    LookupView --> User: 7 Hiển thị thông báo lỗi & Yêu cầu nhập lại
else [Mã hợp lệ (Success)]
    BookingService -> BookingService: 8 Kiểm tra quyền truy cập (Check Ownership/Admin)
    BookingService --> LookupView: 9 Trả về thông tin chi tiết Booking
    LookupView --> User: 10 Hiển thị thông tin đơn đặt phòng
end

@enduml
```
