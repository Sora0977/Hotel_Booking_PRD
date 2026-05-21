# Thesis Memory

## Tên đề tài luận văn

Hệ thống đặt phòng khách sạn trực tuyến (Hotel Booking System) [cần xác nhận tên đề tài chính thức].

## Chủ đề nghiên cứu

Phân tích, thiết kế, xây dựng và đánh giá hệ thống web đặt phòng khách sạn trực tuyến.

## Vấn đề nghiên cứu chính

Người dùng có nhu cầu tìm kiếm, so sánh, đặt phòng và thanh toán trực tuyến thuận tiện, trong khi các đơn vị lưu trú nhỏ lẻ cần một nền tảng số để quản lý phòng, đặt chỗ, tài khoản và doanh thu hiệu quả hơn.

## Mục tiêu nghiên cứu

- Mục tiêu 1: Xây dựng hệ thống web cho phép khách hàng tìm kiếm và đặt phòng khách sạn trực tuyến.
- Mục tiêu 2: Phát triển giao diện thân thiện, dễ sử dụng và tương thích trên nhiều thiết bị.
- Mục tiêu 3: Cung cấp công cụ quản lý cho quản trị viên để quản lý khách sạn, phòng, tài khoản, đặt phòng và báo cáo doanh thu.
- Mục tiêu 4: Đảm bảo hệ thống đáp ứng các yêu cầu cơ bản về hiệu suất, bảo mật và khả năng mở rộng.

## Câu hỏi nghiên cứu

- Câu hỏi 1: Làm thế nào để xây dựng một hệ thống web hỗ trợ tìm kiếm và đặt phòng khách sạn trực tuyến đáp ứng nhu cầu của người dùng?
- Câu hỏi 2: Hệ thống cần những chức năng và mô hình dữ liệu nào để quản lý khách sạn, phòng, tài khoản, đặt phòng và hủy phòng?
- Câu hỏi 3: Mức độ đáp ứng của hệ thống so với các mục tiêu chức năng và phi chức năng đã đặt ra là gì?

## Luận điểm chính / giả thuyết / tuyên bố trung tâm

Một hệ thống đặt phòng khách sạn trực tuyến được thiết kế theo hướng web-based, có phân quyền người dùng, mô hình dữ liệu rõ ràng và quy trình nghiệp vụ đầy đủ có thể hỗ trợ hiệu quả cả nhu cầu đặt phòng của khách hàng và nhu cầu quản lý vận hành của quản trị viên.

## Phạm vi nghiên cứu

Hệ thống web, chưa phát triển ứng dụng di động. Cơ sở dữ liệu sử dụng MySQL. Chức năng thanh toán được xem xét ở mức mô phỏng hoặc sandbox, chưa triển khai dòng tiền thực tế.

## Đối tượng và khách thể nghiên cứu

Đối tượng sử dụng chính gồm khách hàng và quản trị viên. Khách thể nghiên cứu là quy trình tìm kiếm, đặt phòng, quản lý phòng, quản lý khách sạn, quản lý tài khoản và các nghiệp vụ liên quan trong hệ thống đặt phòng khách sạn trực tuyến.

## Phương pháp thực hiện

Phân tích hệ thống tương tự, phân tích yêu cầu, thiết kế cơ sở dữ liệu, thiết kế use case, thiết kế quy trình xử lý, xây dựng hệ thống web và đối chiếu kết quả triển khai với mục tiêu ban đầu.

## Dữ liệu / trường hợp nghiên cứu / tài liệu sử dụng

- Báo cáo luận văn hiện có tại `Hotel booking service/Thesis-report/` đã được nhập vào `thesis/chapters/` ngày 2026-05-21.
- Tài liệu đặc tả phát triển phần mềm tại `SDD/`.
- Hình ảnh minh họa từ `Hotel booking service/Thesis-report/images/` đã được sao chép sang `thesis/figures/imported/`.
- Bản lưu nguyên văn các chương cũ nằm tại `thesis/archive/original_chapters/`.

## Khái niệm và thuật ngữ chính

- Hệ thống đặt phòng khách sạn trực tuyến:
  - Ý nghĩa: Hệ thống web hỗ trợ người dùng tìm kiếm, đặt phòng và quản lý các nghiệp vụ lưu trú.
  - Cách dùng thống nhất trong luận văn: Dùng thống nhất với cụm “hệ thống đặt phòng khách sạn trực tuyến”; có thể ghi kèm “Hotel Booking System” ở lần xuất hiện đầu tiên.
- Quản trị viên:
  - Ý nghĩa: Vai trò có quyền quản lý tài khoản, khách sạn, phòng, tiện nghi, đặt phòng và các chức năng quản trị.
  - Cách dùng thống nhất trong luận văn: Dùng “quản trị viên”, hạn chế thay thế bằng “Admin” trong phần văn bản học thuật, trừ khi nói về vai trò hệ thống.
- Overbooking:
  - Ý nghĩa: Tình trạng đặt trùng hoặc đặt vượt quá số lượng phòng còn khả dụng.
  - Cách dùng thống nhất trong luận văn: Dùng “đặt trùng phòng (overbooking)” ở lần xuất hiện đầu tiên.
- Marketplace:
  - Ý nghĩa: Mô hình nền tảng kết nối khách hàng với nhà cung cấp dịch vụ lưu trú.
  - Cách dùng thống nhất trong luận văn: Có thể giữ thuật ngữ tiếng Anh nếu đang so sánh với Booking.com hoặc Traveloka.

## Cấu trúc chương

### Chương 1 — Giới thiệu

Theo `Rules.md`, chương này mang tên “Giới thiệu”. Nội dung gồm đặt vấn đề và mục tiêu luận văn, những thách thức cần giải quyết, nội dung/phạm vi thực hiện và bảng kết quả cần đạt.

### Chương 2 — Phương pháp thực hiện

Theo `Rules.md`, chương này gồm các hệ thống tương tự, cơ sở lý thuyết nếu cần, công nghệ sử dụng và phân tích yêu cầu. Nội dung từ các file 2 cũ và 3 cũ đã được tái phân bổ vào `chapters/02_phuong_phap_thuc_hien.md`.

### Chương 3 — Thiết kế

Theo `Rules.md`, chương này gồm mô hình dữ liệu, mô hình xử lý, hệ thống màn hình và hệ thống báo biểu nếu có. Nội dung thiết kế từ chương 3 cũ đã được chuyển sang `chapters/03_thiet_ke.md`.

### Chương 4 — Thử nghiệm

Chương thử nghiệm được tạo mới theo `Rules.md`, gồm các kịch bản thử nghiệm, kết quả thử nghiệm và xử lý trường hợp ngoại lệ. Hiện chương này đang ở trạng thái outline, chưa có kết quả kiểm thử thực tế.

### Chương 5 — Kết luận

Theo `Rules.md`, chương này gồm kết quả đối chiếu với mục tiêu, các vấn đề còn tồn đọng và hướng phát triển. Nội dung từ chương kết luận cũ đã được chuyển sang `chapters/05_ket_luan.md`.

### Phụ lục — Hướng dẫn sử dụng

Đã tạo `appendices/huong_dan_su_dung.md` theo yêu cầu tối thiểu của `Rules.md`. Cần bổ sung hướng dẫn sử dụng cho ít nhất một quy trình chính của ứng dụng.

## Quyết định viết quan trọng

- Sử dụng thuật ngữ nhất quán trong toàn bộ luận văn.
- Không tự tạo nguồn tham khảo giả.
- Giữ văn phong tiếng Việt học thuật.
- Giữ nguyên citation key dạng [@authorYear].
- Ưu tiên câu rõ ràng, trực tiếp, tránh diễn đạt mơ hồ.
- Không tự ý thay đổi mục tiêu, câu hỏi nghiên cứu, phương pháp hoặc luận điểm chính nếu chưa được yêu cầu.
- Ưu tiên cấu trúc và quy định định dạng trong `Rules.md` và `SCHOOL_RULES.md`.
- Cấu trúc chương hiện hành là 5 chương theo mẫu của trường, không dùng cấu trúc 6 chương của template cũ.
- Áp dụng MEGA-DOCUMENT PROTOCOL: nội dung chương phải được chỉnh sửa mặc định qua các mảnh file trong thư mục chương, không chỉnh trực tiếp file chương gộp lớn nếu không có yêu cầu rõ ràng.
- Các file chương gốc trong `thesis/chapters/*.md` hiện vẫn được giữ lại để đối chiếu và chỉ xóa hoặc di chuyển khi người dùng xác nhận.
- Mục `3.2 Mô hình xử lý` đã được phân mảnh cấp độ 3 tại `chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/`; file cấp 2 cũ được giữ dưới tên `3_2_mo_hinh_xu_ly_OLD.md.bak`.

## Vấn đề còn mở

- [ ] Thiếu nguồn: Các nhận định về Booking.com, Traveloka, công nghệ sử dụng và tiêu chí phi chức năng cần được bổ sung nguồn học thuật hoặc tài liệu chính thức.
- [ ] Cần làm rõ: Tên đề tài chính thức và yêu cầu cụ thể của giảng viên hướng dẫn nếu khác với `Rules.md`.
- [ ] Cần phản hồi từ giảng viên hướng dẫn: Có giữ Chương 4 — Thử nghiệm hay chỉ xem là phần khuyến khích.
- [ ] Cần kiểm tra lại thuật ngữ: Thống nhất cách dùng “quản trị viên/Admin”, “hệ thống đặt phòng khách sạn trực tuyến”, “Marketplace”, “overbooking”.
- [ ] Cần bổ sung dữ liệu hoặc minh chứng: Kết quả kiểm thử hiệu suất, bảo mật, responsive, xác thực API và các chức năng chưa đạt.
- [ ] Cần bổ sung phụ lục hướng dẫn sử dụng cho tối thiểu một quy trình chính.
- [ ] Cần chuẩn hóa caption hình theo quy định đánh số hình của trường.
- [ ] Cần quyết định xử lý các file chương gốc sau khi đã phân mảnh cấp độ 2.
- [x] Đã phân mảnh sâu mục `3.2 Mô hình xử lý` để tránh xử lý file quá lớn khi chỉnh use case, sơ đồ tuần tự và sơ đồ hoạt động.

## Nhật ký thay đổi

- Ngày: 2026-05-21
  - Thay đổi: Khởi tạo bộ nhớ dài hạn của luận văn theo template mặc định.
  - File liên quan: THESIS_MEMORY.md
- Ngày: 2026-05-21
  - Thay đổi: Ghi nhận nội dung luận văn hiện có tại `Hotel booking service/Thesis-report/` và tài liệu SDD làm nguồn tham chiếu cho project `thesis/`.
  - File liên quan: THESIS_MEMORY.md, TODO.md, notes/ghi_chu_nguon.md
- Ngày: 2026-05-21
  - Thay đổi: Gộp các chương cũ từ `Hotel booking service/Thesis-report/chapters/` vào cấu trúc `thesis/chapters/`, sao chép 31 ảnh sang `thesis/figures/imported/`, và lưu bản gốc tại `thesis/archive/original_chapters/`.
  - File liên quan: chapters/, figures/imported/, archive/original_chapters/, THESIS_MEMORY.md, TODO.md
- Ngày: 2026-05-21
  - Thay đổi: Cập nhật project theo `Rules.md` của trường; chuyển cấu trúc từ 6 chương sang 5 chương gồm Giới thiệu, Phương pháp thực hiện, Thiết kế, Thử nghiệm và Kết luận; tạo `SCHOOL_RULES.md`, `front_matter/` và `appendices/huong_dan_su_dung.md`.
  - File liên quan: Rules.md, SCHOOL_RULES.md, OUTLINE.md, STYLE_GUIDE.md, AI_INSTRUCTIONS.md, README.md, chapters/, front_matter/, appendices/, TODO.md
- Ngày: 2026-05-21
  - Thay đổi: Bổ sung MEGA-DOCUMENT PROTOCOL vào `AI_INSTRUCTIONS.md` và phân mảnh cấp độ 2 các chương 1-5 thành thư mục chunk có `index.md`.
  - File liên quan: AI_INSTRUCTIONS.md, chapters/index.md, chapters/01_mo_dau/, chapters/02_phuong_phap_thuc_hien/, chapters/03_thiet_ke/, chapters/04_thu_nghiem/, chapters/05_ket_luan/, TODO.md
- Ngày: 2026-05-21
  - Thay đổi: Phân mảnh cấp độ 3 mục `3.2 Mô hình xử lý`; tách use case, sơ đồ tuần tự và sơ đồ hoạt động thành các file nhỏ trong `chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/`.
  - File liên quan: chapters/03_thiet_ke/index.md, chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/, chapters/03_thiet_ke/3_2_mo_hinh_xu_ly_OLD.md.bak, AI_INSTRUCTIONS.md, TODO.md
