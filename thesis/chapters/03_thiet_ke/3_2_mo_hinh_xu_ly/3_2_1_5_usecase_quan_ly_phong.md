---
status: draft
dependencies:
  - 3_2_1_use_case_chi_tiet.md
last_updated: 2026-05-21
chapter: "03 - Thiết kế"
parent_chunk: "3.2 Mô hình xử lý"
chunk: "3.2.1.5"
title: "3.2.1.5 Usecase quản lý phòng"
source_file: "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"
related_memory: ../../../THESIS_MEMORY.md
school_rules: ../../../SCHOOL_RULES.md
---
<!-- Mảnh Level-3 được tạo từ mục 3.2. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này. Không tự ý chỉnh sửa PlantUML/code fence nếu tác vụ không yêu cầu. -->

#### 3.2.1.5 Usecase quản lý phòng

```plantuml
@startuml
!theme plain
left to right direction

actor "Quản trị viên (Admin)" as Admin

rectangle "Hệ thống Quản lý Phòng" {
  usecase "Quản lý Phòng" as RoomManage
  usecase "Thêm phòng mới" as AddRoom
  usecase "Cập nhật thông tin phòng" as UpdateRoom
  usecase "Xóa phòng" as DeleteRoom
  usecase "Xác thực phiên Admin" as VerifyAdminSession
  usecase "Kiểm tra quyền sở hữu Khách sạn" as CheckHotelOwner
  usecase "Kiểm tra phòng tồn tại" as CheckRoom
  usecase "Upload hình ảnh\n(Cloudinary)" as UploadImage
  usecase "Thêm tiện ích cho phòng" as AddAmenity
  usecase "Thông báo phòng không tìm thấy" as RoomNotFound
  usecase "Thông báo lỗi định dạng ảnh" as ImageError
  usecase "Thông báo lỗi không có quyền" as PermissionError
}

Admin --> RoomManage
AddRoom -up-|> RoomManage
UpdateRoom -up-|> RoomManage
DeleteRoom -up-|> RoomManage
RoomManage ..> VerifyAdminSession : <<include>>
AddRoom ..> CheckHotelOwner : <<include>>
AddRoom ..> UploadImage : <<include>>
AddRoom ..> AddAmenity : <<include>>
UpdateRoom ..> CheckHotelOwner : <<include>>
UpdateRoom ..> CheckRoom : <<include>>
UpdateRoom ..> UploadImage : <<include>>
DeleteRoom ..> CheckRoom : <<include>>
RoomNotFound .up.> UpdateRoom : <<extend>>\n[Phòng không tồn tại]
RoomNotFound .up.> DeleteRoom : <<extend>>\n[Phòng không tồn tại]
ImageError .up.> AddRoom : <<extend>>\n[File ảnh không hợp lệ]
ImageError .up.> UpdateRoom : <<extend>>\n[File ảnh không hợp lệ]
PermissionError .up.> AddRoom : <<extend>>\n[Không phải chủ sở hữu]
PermissionError .up.> UpdateRoom : <<extend>>\n[Không phải chủ sở hữu]
@enduml
```

> Hình 3.5: Usecase quản lý phòng


Đặc tả Usecase thêm phòng mới

| Mục                                               | Nội dung                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tên Use case                                      | Thêm phòng mới                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Actor                                             | Quản trị viên (Admin)                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Mô tả                                             | Admin tạo và thêm một phòng mới vào khách sạn mà mình quản lý. Quá trình này bao gồm nhập thông tin chi tiết, tải lên hình ảnh và gán các tiện ích cho phòng.                                                                                                                                                                                                                                                                                           |
| Pre-conditions                                    | - Actor đã đăng nhập và có quyền Admin.<br>- Actor phải là chủ sở hữu của khách sạn mà phòng sẽ được thêm vào.                                                                                                                                                                                                                                                                                                                                          |
| Post-conditions                                   | Success: Phòng mới được tạo và lưu vào cơ sở dữ liệu với đầy đủ thông tin, ảnh và tiện ích.<br>Fail: Hệ thống báo lỗi và không tạo phòng (do lỗi quyền hoặc dữ liệu).                                                                                                                                                                                                                                                                                   |
| Luồng sự kiện chính                               | 1. Actor chọn chức năng "Thêm phòng mới" trong giao diện quản lý khách sạn.<br><br>2. Actor nhập các thông tin cơ bản (Tên phòng, Loại phòng, Giá, Mô tả...).<br>3. Actor thực hiện Upload hình ảnh.<br>4. Actor chọn danh sách tiện ích và thực hiện Thêm tiện ích cho phòng.<br>5. Actor nhấn nút "Lưu".<br>6. Hệ thống thực hiện Kiểm tra quyền sở hữu Khách sạn.<br>7. Nếu hợp lệ, hệ thống lưu dữ liệu phòng và thông báo "Thêm phòng thành công". |
| Luồng sự kiện phụ                                 | - Nếu Actor không phải là chủ sở hữu khách sạn: Hệ thống thực hiện Thông báo lỗi không có quyền.<br>- Nếu file ảnh upload bị lỗi hoặc sai định dạng: Hệ thống thực hiện Thông báo lỗi định dạng ảnh.                                                                                                                                                                                                                                                    |
| <Include Use Case><br>Quy trình Nghiệp vụ         | - Kiểm tra quyền sở hữu Khách sạn: Hệ thống xác minh ID của người đang thực hiện có khớp với chủ sở hữu (Owner) của khách sạn hay không.<br>- Upload hình ảnh: Hệ thống xử lý việc tải ảnh lên Cloudinary và lấy về URL.<br>- Thêm tiện ích cho phòng: Hệ thống liên kết các tiện ích (Amenities) đã chọn vào bản ghi của phòng mới.                                                                                                                    |
| <Extend Use Case><br>Thông báo lỗi không có quyền | Điều kiện: Khi quy trình kiểm tra quyền sở hữu trả về False.<br>Hành động:<br>- Hệ thống hiển thị thông báo: "Bạn không có quyền thêm phòng vào khách sạn này".<br>- Hệ thống chặn hành động lưu.                                                                                                                                                                                                                                                       |
| <Extend Use Case><br>Thông báo lỗi định dạng ảnh  | Điều kiện: Khi file tải lên không phải là ảnh hoặc kích thước quá lớn.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo: "Định dạng ảnh không hợp lệ hoặc file quá lớn".                                                                                                                                                                                                                                                                                   |

Đặc tả Usecase cập nhật thông tin phòng

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Cập nhật thông tin phòng |
| Actor | Quản trị viên (Admin) |
| Mô tả | Admin thay đổi các thông tin chi tiết của một phòng đã tồn tại trong hệ thống (như giá cả, mô tả, loại phòng hoặc hình ảnh) để đảm bảo dữ liệu luôn chính xác. |
| Pre-conditions | - Actor đã đăng nhập và có quyền Admin.<br>- Phòng cần cập nhật phải đang tồn tại trong hệ thống. |
| Post-conditions | Success: Thông tin phòng được cập nhật mới trong cơ sở dữ liệu.<br>Fail: Hệ thống giữ nguyên thông tin cũ và báo lỗi (nếu phòng không tồn tại hoặc lỗi dữ liệu). |
| Luồng sự kiện chính | 1. Actor chọn chức năng "Chỉnh sửa" tại một phòng cụ thể trong danh sách.<br>2. Actor thay đổi các thông tin cần thiết (Giá, Mô tả...).<br>3. (Tùy chọn) Actor tải lên hình ảnh mới thay thế ảnh cũ.<br>4. Actor nhấn nút "Lưu thay đổi".<br>5. Hệ thống thực hiện kiểm tra phòng tồn tại.<br>6. (Nếu có ảnh mới) Hệ thống thực hiện upload hình ảnh.<br>7. Hệ thống lưu thông tin mới và thông báo cập nhật thành công. |
| Luồng sự kiện phụ | - Nếu ID phòng không tìm thấy trong DB: Hệ thống thực hiện thông báo phòng không tìm thấy.<br>- Nếu ảnh tải lên bị lỗi định dạng: Hệ thống thực hiện thông báo lỗi định dạng ảnh. |
| <Include Use Case><br>Quy trình Nghiệp vụ | - Kiểm tra phòng tồn tại: Hệ thống truy vấn cơ sở dữ liệu để đảm bảo ID phòng đang thao tác là hợp lệ trước khi cho phép sửa.<br>- Upload hình ảnh: Nếu người dùng thay đổi ảnh, hệ thống thực hiện tải ảnh mới lên Cloud server và cập nhật lại đường dẫn ảnh. |
| <Extend Use Case><br>Thông báo phòng không tìm thấy | Điều kiện: Khi quy trình kiểm tra sự tồn tại của phòng trả về kết quả rỗng (có thể do phòng vừa bị xóa bởi người khác).<br>Hành động:<br>- Hệ thống hiển thị lỗi: "Phòng này không còn tồn tại".<br>- Hệ thống đưa người dùng quay lại danh sách phòng. |
| <Extend Use Case><br>Thông báo lỗi định dạng ảnh | Điều kiện: Khi file ảnh mới tải lên không đúng định dạng cho phép.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo và yêu cầu chọn file khác. |

Đặc tả Usecase xóa phòng

| Mục | Nội dung |
| --- | --- |
| Tên Use case | Xóa phòng |
| Actor | Quản trị viên (Admin) |
| Mô tả | Admin thực hiện xóa vĩnh viễn một phòng khỏi danh sách phòng của khách sạn. Hành động này thường yêu cầu xác nhận kỹ lưỡng để tránh mất dữ liệu. |
| Pre-conditions | - Actor đã đăng nhập và có quyền Admin.<br>- Phòng cần xóa đang hiện hữu trong danh sách quản lý. |
| Post-conditions | Success: Dữ liệu phòng bị xóa khỏi cơ sở dữ liệu.<br>Fail: Hệ thống giữ nguyên dữ liệu và báo lỗi (nếu phòng không tìm thấy). |
| Luồng sự kiện chính | 1. Actor nhấn nút "Xóa" tại dòng thông tin của phòng cần xóa.<br>2. Hệ thống hiển thị hộp thoại yêu cầu xác nhận hành động.<br>3. Actor nhấn nút "Đồng ý" (Confirm).<br>4. Hệ thống thực hiện kiểm tra phòng tồn tại.<br>5. Nếu phòng hợp lệ, hệ thống thực hiện xóa dữ liệu phòng.<br>6. Hệ thống hiển thị thông báo "Đã xóa phòng thành công" và cập nhật lại danh sách. |
| Luồng sự kiện phụ | - Nếu trong quá trình xử lý, phòng không còn tồn tại trong DB (ví dụ: đã bị xóa bởi admin khác): Hệ thống thực hiện thông báo phòng không tìm thấy. |
| <Include Use Case><br>Quy trình Nghiệp vụ | - Kiểm tra phòng tồn tại: Hệ thống truy vấn cơ sở dữ liệu theo ID của phòng để đảm bảo đối tượng cần xóa là hợp lệ trước khi thực thi lệnh xóa. |
| <Extend Use Case><br>Thông báo phòng không tìm thấy | Điều kiện: Khi quy trình kiểm tra trả về kết quả rằng ID phòng không tồn tại.<br>Hành động:<br>- Hệ thống hiển thị thông báo lỗi: "Phòng này không tồn tại hoặc đã bị xóa".<br>- Hệ thống tự động làm mới danh sách phòng để phản ánh dữ liệu thực tế. |
| <Extend Use Case><br>Thông báo lỗi định dạng ảnh | Điều kiện: Khi file ảnh mới tải lên không đúng định dạng cho phép.<br>Hành động:<br>- Hệ thống hiển thị cảnh báo và yêu cầu chọn file khác. |
