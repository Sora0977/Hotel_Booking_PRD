---
status: imported_chunk
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.2.02"
title: "Sơ đồ tuần tự đăng ký"
source_file: "../3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

> Hình 3.14: Sơ đồ tuần tự đăng ký


- Sơ đồ tuần tự cập nhật thông tin cá nhân

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
hide footbox
autoactivate on
title Sequence Diagram: Cập nhật thông tin cá nhân

actor User
boundary ProfileForm
control ProfileService
entity UserDB

User -> ProfileForm : 1 Chọn "Cập nhật thông tin" & Nhập dữ liệu mới
User -> ProfileForm : 2 Nhấn nút "Lưu thay đổi"
ProfileForm -> ProfileService : 3 Gửi yêu cầu cập nhật(data)
ProfileService -> ProfileService : 4 Lấy thông tin User từ Context (Session/Token)
ProfileService -> ProfileService : 5 Kiểm tra tính hợp lệ dữ liệu (Validate Form)

alt Dữ liệu không hợp lệ (Sai định dạng/Thiếu trường...)
    ProfileService --> ProfileForm : 6 Trả về lỗi Validation
    ProfileForm --> User : 7 Hiển thị thông báo lỗi & Yêu cầu nhập lại
else Dữ liệu hợp lệ
    ProfileService -> UserDB : 8 Cập nhật thông tin User
    UserDB --> ProfileService : 9 Xác nhận cập nhật thành công
    ProfileService --> ProfileForm : 10 Trả về thông báo "Cập nhật thành công"
    ProfileForm --> User : 11 Hiển thị thông báo thành công
end
@enduml
```
