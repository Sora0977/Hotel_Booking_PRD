---
status: draft
dependencies:
  - 3_2_1_3_usecase_quan_ly_thong_tin_ca_nhan.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.04"
title: "Sơ đồ tuần tự đổi mật khẩu"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.16: Sơ đồ tuần tự đổi mật khẩu


- Sơ đồ tuần tự xem thông tin profile

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Xem thông tin Profile

actor User
boundary ProfileView
control ProfileService
entity UserDB

User -> ProfileView : 1 Chọn menu "Hồ sơ cá nhân"
ProfileView -> ProfileService : 2 Yêu cầu lấy thông tin Profile
ProfileService -> ProfileService : 3 Lấy User ID từ Context (Session/Token)

alt Không lấy được Context (Lỗi phiên/Hết hạn)
    ProfileService --> ProfileView : 4 Yêu cầu đăng nhập lại
    ProfileView --> User : 5 Chuyển hướng về trang Đăng nhập
else Context hợp lệ (Success)
    ProfileService -> UserDB : 6 Truy vấn thông tin chi tiết theo ID
    UserDB --> ProfileService : 7 Trả về dữ liệu User (Họ tên, SĐT, Avatar...)
    ProfileService --> ProfileView : 8 Trả về dữ liệu Profile
    ProfileView --> User : 9 Hiển thị giao diện thông tin chi tiết
end
@enduml
```
