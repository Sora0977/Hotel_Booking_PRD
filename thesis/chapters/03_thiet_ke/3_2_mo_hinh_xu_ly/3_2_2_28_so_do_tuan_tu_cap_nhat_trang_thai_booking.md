---
status: draft
dependencies:
  - 3_2_1_9_usecase_quan_ly_dat_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.28"
title: "Sơ đồ tuần tự cập nhật trạng thái booking"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.40: Sơ đồ tuần tự cập nhật trạng thái booking


- Sơ đồ tuần tự tạo booking mới

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Tạo Booking mới

actor Customer
boundary BookingForm
control BookingService
entity Database

Customer -> BookingForm: 1 Chọn ngày Check-in, Check-out, Số lượng phòng
Customer -> BookingForm: 2 Nhấn nút "Đặt phòng"
BookingForm -> BookingService: 3 Gửi yêu cầu đặt phòng(bookingData)
BookingService -> BookingService: 4 Kiểm tra tính hợp lệ ngày đặt (Validate Date)

alt [Ngày đặt không hợp lệ]
    BookingService --> BookingForm: 5 Trả về lỗi "Ngày đặt không hợp lệ"
    BookingForm --> Customer: 6 Hiển thị yêu cầu chọn lại ngày
else [Ngày hợp lệ]
    BookingService -> Database: 7 Truy vấn kiểm tra phòng trống
    Database --> BookingService: 8 Kết quả (Trống/Đã có khách)

    alt [Phòng không còn trống (Availability = False)]
        BookingService --> BookingForm: 9 Trả về lỗi "Phòng đã hết chỗ trong thời gian này"
        BookingForm --> Customer: 10 Hiển thị thông báo hết phòng
    else [Phòng khả dụng]
        BookingService -> Database: 11 Kiểm tra sức chứa (Check Capacity)
        Database --> BookingService: 12 Kết quả số lượng (Đủ/Thiếu)

        alt [Số lượng phòng không đủ]
            BookingService --> BookingForm: 13 Trả về lỗi "Số lượng phòng còn lại không đủ"
            BookingForm --> Customer: 14 Hiển thị thông báo lỗi số lượng
        else [Số lượng đáp ứng (Success)]
            BookingService -> BookingService: 15 Tính tổng giá tiền (Calculate Price)
            BookingService -> BookingService: 16 Sinh mã đặt phòng (Generate Reference Code)
            BookingService -> Database: 17 Lưu đơn đặt phòng mới vào DB
            Database --> BookingService: 18 Xác nhận lưu thành công
            BookingService --> BookingForm: 19 Thông báo "Đặt phòng thành công" (kèm Mã)
            BookingForm --> Customer: 20 Hiển thị thông báo & Chuyển hướng
        end
    end
end

@enduml
```
