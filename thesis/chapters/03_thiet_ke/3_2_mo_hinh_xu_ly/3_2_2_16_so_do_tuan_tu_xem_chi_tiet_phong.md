---
status: draft
dependencies:
  - 3_2_1_6_usecase_tra_cuu_phong.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.16"
title: "Sơ đồ tuần tự xem chi tiết phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.28: Sơ đồ tuần tự xem chi tiết phòng


- Sơ đồ tuần tự tìm kiếm phòng

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Tìm kiếm phòng theo từ khóa

actor "Guest/User" as GuestUser
boundary SearchForm
control RoomService
entity RoomDB

GuestUser -> SearchForm : 1 Nhập từ khóa (Ví dụ: "Deluxe", "Sea View")
GuestUser -> SearchForm : 2 Nhấn nút "Tìm kiếm"
SearchForm -> RoomService : 3 Gửi yêu cầu tìm kiếm(keyword)
RoomService -> RoomDB : 4 Truy vấn theo từ khóa (LIKE %keyword%)
RoomDB --> RoomService : 5 Trả về danh sách kết quả (List)

alt Không tìm thấy kết quả (List Empty)
    RoomService --> SearchForm : 6 Trả về thông báo "Không tìm thấy kết quả nào phù hợp"
    SearchForm --> GuestUser : 7 Hiển thị thông báo trống
else Tìm thấy kết quả (Success)
    RoomService --> SearchForm : 8 Trả về danh sách phòng tìm được
    SearchForm --> GuestUser : 9 Hiển thị danh sách kết quả tìm kiếm
end
@enduml
```
