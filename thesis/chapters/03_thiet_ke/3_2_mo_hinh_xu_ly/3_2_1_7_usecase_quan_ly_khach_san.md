---
status: draft
dependencies:
  - 3_2_1_use_case_chi_tiet.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.1.7"
title: "3.2.1.7 Usecase quản lý khách sạn"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

#### 3.2.1.7 Usecase quản lý khách sạn

```plantuml
@startuml
!theme plain
left to right direction

actor "Quản trị viên (Admin)" as Admin

rectangle "Hệ thống Quản lý Khách sạn" {
  usecase "Quản lý Khách sạn" as HotelManage
  usecase "Kiểm tra quyền Admin" as CheckAdmin
  usecase "Xóa khách sạn" as DeleteHotel
  usecase "Kiểm tra khách sạn tồn tại" as CheckHotelExists
  usecase "Cập nhật khách sạn" as UpdateHotel
  usecase "Kiểm tra quyền sở hữu\n(Check Owner)" as CheckOwner
  usecase "Thông báo lỗi không có quyền" as PermissionError
  usecase "Đăng nhập hệ thống" as LoginSystem
  usecase "Xem danh sách khách sạn của tôi" as MyHotels
  usecase "Thêm khách sạn mới" as AddHotel
  usecase "Kiểm tra trùng tên & địa điểm" as CheckDuplicate
  usecase "Upload hình ảnh (Cloudinary)" as UploadImage
  usecase "Thông báo trùng lặp" as DuplicateError
  usecase "Thông báo thiếu ảnh" as MissingImage
}

Admin --> HotelManage

DeleteHotel -up-|> HotelManage
UpdateHotel -up-|> HotelManage
MyHotels -up-|> HotelManage
AddHotel -up-|> HotelManage

HotelManage ..> CheckAdmin : <<include>>
HotelManage ..> LoginSystem : <<include>>

DeleteHotel ..> CheckHotelExists : <<include>>
DeleteHotel ..> CheckOwner : <<include>>
UpdateHotel ..> CheckHotelExists : <<include>>
UpdateHotel ..> CheckOwner : <<include>>
AddHotel ..> CheckDuplicate : <<include>>
AddHotel ..> UploadImage : <<include>>

PermissionError .up.> UpdateHotel : <<extend>>
PermissionError .up.> DeleteHotel : <<extend>>
DuplicateError .up.> AddHotel : <<extend>>
MissingImage .up.> AddHotel : <<extend>>
@enduml
```

> Hình 3.7: Usecase quản lý khách sạn


Đặc tả Usecase thêm khách sạn mới

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Thêm khách sạn mới |
| Actor | Quản trị viên (Admin) |
| Mô tả | Admin tạo và đăng ký một khách sạn mới vào hệ thống. Quá trình này bao gồm nhập thông tin định danh, địa chỉ và tải lên hình ảnh đại diện cho khách sạn. |
| Pre-conditions | - Actor đã đăng nhập vào hệ thống.<br>- Actor có quyền Admin. |
| Post-conditions | Success: Khách sạn mới được lưu vào cơ sở dữ liệu và gán quyền sở hữu cho Admin tạo ra nó.<br>Fail: Hệ thống báo lỗi trùng lặp hoặc lỗi dữ liệu (thiếu ảnh). |
| Luồng sự kiện chính | 1. Actor chọn chức năng "Thêm khách sạn".<br>2. Actor nhập thông tin (Tên, Địa chỉ, Thành phố, Mô tả...).<br>3. Actor thực hiện upload hình ảnh (Cloudinary).<br>4. Actor nhấn nút "Tạo mới".<br>5. Hệ thống thực hiện đăng nhập (kiểm tra session).<br>6. Hệ thống thực hiện kiểm tra quyền Admin.<br>7. Hệ thống thực hiện kiểm tra trùng tên & địa điểm.<br>8. Nếu hợp lệ, hệ thống lưu thông tin khách sạn mới.<br>9. Hệ thống hiển thị thông báo "Thêm khách sạn thành công". |
| Luồng sự kiện phụ | - Nếu tên hoặc địa chỉ khách sạn đã tồn tại: Hệ thống thực hiện thông báo trùng lặp.<br>- Nếu người dùng không tải ảnh lên: Hệ thống thực hiện thông báo thiếu ảnh. |
| <Include Use Case><br>Quy trình Nghiệp vụ | - Kiểm tra quyền Admin: Hệ thống xác minh vai trò của tài khoản để đảm bảo chỉ quản trị viên mới được tạo khách sạn.<br>- Upload hình ảnh: Hệ thống xử lý việc tải file ảnh lên server lưu trữ đám mây và trả về đường dẫn URL.<br>- Kiểm tra trùng tên & địa điểm: Hệ thống so sánh thông tin nhập vào với dữ liệu hiện có để tránh việc tạo các bản ghi khách sạn trùng lặp (Duplicate). |
| <Extend Use Case><br>Thông báo trùng lặp | Điều kiện: Khi quy trình kiểm tra trùng lặp phát hiện dữ liệu tương tự đã tồn tại.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo: "Khách sạn với tên và địa chỉ này đã tồn tại".<br>- Hệ thống yêu cầu sửa lại thông tin. |
| <Extend Use Case><br>Thông báo thiếu ảnh | Điều kiện: Khi người dùng cố gắng lưu mà chưa có URL hình ảnh hợp lệ.<br>Hành động:<br>- Hệ thống hiển thị lỗi: "Vui lòng tải lên ít nhất một hình ảnh cho khách sạn". |

Đặc tả Usecase cập nhật khách sạn

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Cập nhật khách sạn |
| Actor | Quản trị viên (Admin) |
| Mô tả | Admin thay đổi các thông tin chi tiết của một khách sạn đã tồn tại trong hệ thống (như tên, mô tả, tiện ích, hoặc ảnh đại diện) để cập nhật dữ liệu mới nhất. |
| Pre-conditions | - Actor đã đăng nhập và có quyền Admin.<br>- Khách sạn cần cập nhật phải tồn tại.<br>- Actor phải là người sở hữu (Owner) của khách sạn đó. |
| Post-conditions | Success: Thông tin khách sạn được cập nhật vào cơ sở dữ liệu.<br>Fail: Hệ thống giữ nguyên thông tin cũ và báo lỗi (nếu không có quyền hoặc khách sạn không tồn tại). |
| Luồng sự kiện chính | 1. Actor chọn chức năng "Chỉnh sửa" tại khách sạn cần cập nhật.<br>2. Actor thay đổi các thông tin mong muốn (Tên, Mô tả, v.v.).<br>3. Actor nhấn nút "Lưu thay đổi".<br>4. Hệ thống thực hiện kiểm tra quyền sở hữu.<br>5. Hệ thống thực hiện kiểm tra khách sạn tồn tại.<br>6. Nếu hợp lệ, hệ thống lưu thông tin mới.<br>7. Hệ thống hiển thị thông báo "Cập nhật thành công". |
| Luồng sự kiện phụ | - Nếu Actor cố tình sửa khách sạn không thuộc quyền quản lý của mình: Hệ thống thực hiện thông báo lỗi không có quyền. |
| <Include Use Case><br>Quy trình Nghiệp vụ | - Kiểm tra quyền sở hữu: Hệ thống đối chiếu ID của Admin đang đăng nhập với ID chủ sở hữu (OwnerID) của khách sạn để đảm bảo tính bảo mật.<br>- Kiểm tra khách sạn tồn tại: Hệ thống xác minh xem ID khách sạn có còn hợp lệ trong cơ sở dữ liệu hay không (tránh trường hợp vừa bị xóa). |
| <Extend Use Case><br>Thông báo lỗi không có quyền | Điều kiện: Khi quy trình kiểm tra quyền sở hữu trả về kết quả False (không khớp).<br>Hành động:<br>- Hệ thống hiển thị cảnh báo: "Bạn không có quyền chỉnh sửa khách sạn này".<br><br>- Hệ thống từ chối lưu thay đổi. |
| <Extend Use Case><br>Thông báo thiếu ảnh | Điều kiện: Khi người dùng cố gắng lưu mà chưa có URL hình ảnh hợp lệ.<br>Hành động:<br>- Hệ thống hiển thị lỗi: "Vui lòng tải lên ít nhất một hình ảnh cho khách sạn". |

Đặc tả Usecase xóa khách sạn

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Xóa khách sạn |
| Actor | Quản trị viên (Admin) |
| Mô tả | Admin thực hiện xóa vĩnh viễn một khách sạn khỏi hệ thống. Hành động này yêu cầu quyền sở hữu đối với khách sạn đó và thường đi kèm bước xác nhận để tránh sai sót. |
| Pre-conditions | - Actor đã đăng nhập và có quyền Admin.<br>- Khách sạn cần xóa đang tồn tại trong danh sách quản lý của Admin. |
| Post-conditions | Success: Dữ liệu khách sạn (và các phòng liên quan) bị xóa khỏi cơ sở dữ liệu.<br>Fail: Hệ thống giữ nguyên dữ liệu và báo lỗi (nếu không có quyền hoặc khách sạn không tồn tại). |
| Luồng sự kiện chính | 1. Actor chọn nút "Xóa" tại khách sạn mong muốn trong danh sách.<br>2. Hệ thống hiển thị hộp thoại xác nhận.<br>3. Actor nhấn nút "Đồng ý" để xác nhận xóa.<br>4. Hệ thống thực hiện kiểm tra quyền sở hữu.<br>5. Hệ thống thực hiện kiểm tra khách sạn tồn tại.<br>6. Nếu hợp lệ, hệ thống xóa dữ liệu khách sạn.<br>7. Hệ thống hiển thị thông báo "Đã xóa khách sạn thành công". |
| Luồng sự kiện phụ | - Nếu Actor không phải là chủ sở hữu của khách sạn này: Hệ thống thực hiện thông báo lỗi không có quyền. |
| <Include Use Case><br>Quy trình Nghiệp vụ | - Kiểm tra quyền sở hữu: Hệ thống xác minh Admin hiện tại có phải là người tạo/sở hữu khách sạn này không (Owner Check).<br>- Kiểm tra khách sạn tồn tại: Hệ thống đảm bảo ID khách sạn vẫn còn trong DB trước khi thực hiện lệnh xóa. |
| <Extend Use Case><br>Thông báo lỗi không có quyền | Điều kiện: Khi quy trình kiểm tra quyền sở hữu thất bại.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo: "Bạn không có quyền xóa khách sạn này".<br>- Hệ thống hủy bỏ thao tác xóa. |
| <Extend Use Case><br>Thông báo lỗi trùng tên | Điều kiện: Khi quy trình kiểm tra tên phát hiện sự trùng lặp.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo: "Tên tiện ích đã được sử dụng". |

Đặc tả Usecase xem danh sách khách sạn của tôi

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Xem danh sách khách sạn của tôi (View My Hotels) |
| Actor | Quản trị viên (Admin) |
| Mô tả | Admin xem danh sách toàn bộ các khách sạn mà mình đang sở hữu và quản lý. Tính năng này giúp Admin có cái nhìn tổng quan về tài sản của mình trên hệ thống. |
| Pre-conditions | - Actor đã đăng nhập vào hệ thống.<br>- Actor có quyền Admin. |
| Post-conditions | Success: Hệ thống hiển thị danh sách các khách sạn do Admin này tạo/sở hữu.<br>Fail: Hệ thống hiển thị danh sách trống (nếu chưa có khách sạn nào). |
| Luồng sự kiện chính | 1. Actor chọn menu "Khách sạn của tôi".<br>2. Hệ thống thực hiện kiểm tra quyền Admin.<br>3. Hệ thống truy vấn cơ sở dữ liệu để lấy danh sách khách sạn theo ID của Admin.<br>4. Hệ thống hiển thị danh sách khách sạn lên giao diện. |
| Luồng sự kiện phụ | - Nếu Admin chưa tạo khách sạn nào: Hệ thống hiển thị thông báo "Bạn chưa có khách sạn nào. Hãy tạo mới ngay!". |
| <Include Use Case><br>Quy trình Nghiệp vụ | - Kiểm tra quyền Admin: Hệ thống xác minh vai trò của tài khoản để đảm bảo người dùng có quyền truy cập vào khu vực quản lý.<br>- Truy vấn theo Owner ID: (Ngầm định) Hệ thống lọc dữ liệu khách sạn trong DB với điều kiện owner_id == current_user_id. |
| <Extend Use Case><br>Thông báo lỗi không có quyền | Điều kiện: Khi quy trình kiểm tra quyền sở hữu trả về kết quả False (không khớp).<br>Hành động:<br>- Hệ thống hiển thị cảnh báo: "Bạn không có quyền chỉnh sửa khách sạn này".<br>- Hệ thống từ chối lưu thay đổi. |
| <Extend Use Case><br>Thông báo thiếu ảnh | Điều kiện: Khi người dùng cố gắng lưu mà chưa có URL hình ảnh hợp lệ.<br>Hành động:<br>- Hệ thống hiển thị lỗi: "Vui lòng tải lên ít nhất một hình ảnh cho khách sạn". |
