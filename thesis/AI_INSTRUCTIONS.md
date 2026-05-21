# AI Instructions

File này quy định cách AI agent làm việc với project luận văn.

## MEGA-DOCUMENT PROTOCOL

Dự án này là một luận văn quy mô lớn, dự kiến khoảng 300-400 trang. AI agent phải làm việc theo cơ chế phân mảnh cấp độ 2 và cấp độ 3 (Level-2 & Level-3 Chunking) và truy xuất cục bộ (Local Retrieval) để tránh tràn ngữ cảnh, giảm rủi ro làm hỏng nội dung và bảo vệ các khối sơ đồ/mã nguồn.

### 1. Cấu trúc Phân mảnh (Level-2 & Level-3 Chunking)

- Các chương trong `chapters/` phải được chia thành thư mục chương.
- Mỗi thư mục chương chứa các mảnh file tương ứng với từng heading cấp 2, ví dụ `3.1_mo_hinh_du_lieu.md`, `3.2_mo_hinh_xu_ly.md`.
- Mỗi thư mục chương phải có `index.md` để liệt kê và mô tả các mảnh file con.
- Khi chỉnh sửa nội dung, làm việc trên mảnh file cục bộ, không thao tác trực tiếp trên file chương gộp lớn trừ khi người dùng yêu cầu rõ ràng.
- Các file chương gốc chỉ được dùng như bản tham chiếu/nguồn nhập hoặc phục vụ xuất bản, không phải bề mặt chỉnh sửa mặc định.
- Nếu một mảnh cấp độ 2 vẫn quá lớn, đặc biệt là các mục chứa nhiều PlantUML, phải tách tiếp thành thư mục cấp độ 3 theo heading cấp 3/cấp 4 hoặc theo cụm sơ đồ/caption an toàn.
- Mỗi thư mục phân mảnh cấp độ 3 cũng phải có `index.md`.
- Sau khi phân mảnh cấp độ 3, file mảnh cấp độ 2 gốc phải được đổi thành `_OLD.md.bak` hoặc lưu vào `archive/`, không xóa hẳn nếu chưa có bản dự phòng.

### 2. Giao thức đọc ngữ cảnh

Trước khi viết, sửa hoặc tái cấu trúc:

1. Đọc `THESIS_MEMORY.md` và `OUTLINE.md` để nắm bản đồ tổng thể.
2. Định vị đúng thư mục chương và mảnh file cần sửa bằng `index.md` hoặc tìm kiếm theo từ khóa.
3. Chỉ đọc mảnh file liên quan trực tiếp đến tác vụ.
4. Không tự ý đọc toàn bộ chương hoặc toàn bộ luận văn nếu không cần thiết.
5. Nếu cần tìm khái niệm, thuật ngữ, định nghĩa hoặc citation ở chương khác, ưu tiên dùng tìm kiếm (`rg`) với từ khóa cụ thể thay vì mở hàng loạt file.
6. Chỉ đọc `STYLE_GUIDE.md` khi bắt đầu viết nội dung mới hoặc chỉnh văn phong.
7. Chỉ đọc `SCHOOL_RULES.md` khi thao tác liên quan đến cấu trúc heading, định dạng, mục lục, hình ảnh hoặc quy định của trường.

### 3. Giao thức chỉnh sửa

- Chỉnh sửa bằng patch/diff hoặc thay thế khối nhỏ.
- Không in lại toàn bộ nội dung file dài trong phản hồi.
- Khi cần mô tả thay đổi, chỉ nêu file, mục và đoạn đã thay đổi.
- Nếu cần thay thế nội dung thủ công, ghi rõ đoạn cần thay và nội dung thay thế.
- Luôn bảo vệ citation key, bảng, heading và cấu trúc tài liệu nếu không có lý do rõ ràng để thay đổi.
- **Bảo vệ Encoding (UTF-8):** TẤT CẢ các lệnh thao tác ghi (write/patch) lên hệ thống file BẮT BUỘC phải sử dụng chuẩn mã hóa `UTF-8`. AI tuyệt đối không được ghi ra các file làm vỡ font chữ tiếng Việt thành các ký tự dấu `?`.

#### Quy tắc xuất ảnh PlantUML

Mỗi khi sửa xong mã code PlantUML, bạn phải BẮT BUỘC nhắc User cập nhật/export file ảnh `.png` tương ứng lưu vào thư mục `thesis/figures/`. Đồng thời, đảm bảo file markdown chứa mã PlantUML đó phải có một thẻ nhúng ảnh, ví dụ `![Sơ đồ](../../figures/ten_anh.png)`, nằm ngay bên dưới khối code.

### 4. Vùng bất khả xâm phạm

- Không tự ý thay đổi, xóa hoặc định dạng lại các khối PlantUML, Mermaid, code fence hoặc sơ đồ.
- Nếu tác vụ bắt buộc phải sửa sơ đồ, phải nêu rõ phạm vi sửa và chỉ sửa khối liên quan.
- Không tự tạo kết quả thử nghiệm, dữ liệu, tài liệu tham khảo hoặc minh chứng.

### 5. Diagnostic Report

Sau mỗi tác vụ lớn liên quan đến tái cấu trúc, nhập nội dung, xuất bản hoặc chỉnh sửa nhiều mảnh file, báo cáo phải có các mục:

- Phạm vi xử lý.
- File/thư mục đã thay đổi.
- Chunk đã tạo hoặc đã chỉnh sửa.
- File gốc có bị xóa hay không.
- Kiểm tra an toàn đã thực hiện.
- Citation.
- Bộ nhớ luận văn và TODO.
- Vấn đề còn lại.
- Cam kết thao tác tiếp theo theo Level-2/Level-3 Chunking.

## Vai trò

AI agent có nhiệm vụ hỗ trợ:

- Lập dàn ý.
- Viết nháp.
- Viết lại.
- Rà soát lập luận.
- Kiểm tra logic.
- Kiểm tra thuật ngữ.
- Kiểm tra citation.
- Cập nhật bộ nhớ luận văn.
- Quản lý TODO.
- Hỗ trợ chuẩn bị bản nháp hoàn chỉnh.

## Quy trình bắt buộc khi nhận yêu cầu

Khi tôi yêu cầu viết, viết lại, mở rộng, rút gọn, rà soát hoặc chỉnh sửa bất kỳ phần nào của luận văn, hãy làm theo quy trình sau:

### Bước 1 — Đọc bộ nhớ

Đọc các file sau:

1. THESIS_MEMORY.md
2. OUTLINE.md
3. STYLE_GUIDE.md
4. AI_INSTRUCTIONS.md
5. SCHOOL_RULES.md
6. File chương hoặc mục liên quan

Nếu cần kiểm tra chi tiết quy định của trường, đọc thêm `../Rules.md`.

### Bước 2 — Truy xuất ngữ cảnh liên quan

Tìm trong các chương khác những nội dung liên quan đến:

- Thuật ngữ chính.
- Câu hỏi nghiên cứu.
- Luận điểm.
- Phương pháp.
- Citation.
- Định nghĩa.
- Kết quả đã trình bày.
- Các đoạn có khả năng bị lặp ý.

Không được chỉ dựa vào trí nhớ trong chat.

### Bước 2.5 — Đối chiếu quy định của trường

Trước khi viết mới, tái cấu trúc hoặc chỉnh sửa các phần lớn, phải kiểm tra nội dung có phù hợp với:

- Cấu trúc 5 chương trong `SCHOOL_RULES.md`.
- Dàn ý trong `OUTLINE.md`.
- Quy định định dạng, heading, hình ảnh, mục lục, header/footer trong `STYLE_GUIDE.md`.

Nếu có mâu thuẫn giữa template cũ và quy định trường, ưu tiên `SCHOOL_RULES.md` và ghi nhận trong `THESIS_MEMORY.md` hoặc `TODO.md`.

### Bước 3 — Xác định phạm vi công việc

Trước khi chỉnh sửa, xác định:

- File cần sửa.
- Mục cần sửa.
- Mục tiêu chỉnh sửa.
- Những phần không được thay đổi.

Chỉ làm việc trong phạm vi tôi yêu cầu.

### Bước 4 — Chỉnh sửa tối thiểu

- Thực hiện thay đổi nhỏ nhất cần thiết.
- Không viết lại toàn bộ file nếu không được yêu cầu.
- Không xóa nội dung quan trọng nếu chưa hỏi.
- Không thay đổi citation key nếu không cần.
- Không đổi thuật ngữ chính nếu chưa cập nhật THESIS_MEMORY.md.

### Bước 5 — Bảo toàn citation

- Giữ citation key dạng [@authorYear].
- Không bịa nguồn.
- Không tạo citation mới nếu chưa có trong references.bib.
- Nếu cần nguồn nhưng chưa có, ghi [citation needed].
- Nếu thiếu BibTeX, thêm việc cần làm vào TODO.md.

### Bước 6 — Cập nhật bộ nhớ

Sau khi chỉnh sửa, cập nhật THESIS_MEMORY.md nếu có thay đổi quan trọng về:

- Tên đề tài.
- Chủ đề nghiên cứu.
- Vấn đề nghiên cứu.
- Mục tiêu nghiên cứu.
- Câu hỏi nghiên cứu.
- Luận điểm chính.
- Phương pháp thực hiện.
- Dữ liệu hoặc trường hợp nghiên cứu.
- Thuật ngữ chính.
- Tóm tắt chương.
- Quyết định viết quan trọng.
- Vấn đề còn mở.
- Cấu trúc chương theo quy định của trường.

Không cập nhật THESIS_MEMORY.md cho các thay đổi nhỏ về câu chữ nếu ý nghĩa không đổi.

### Bước 7 — Cập nhật TODO

Nếu còn vấn đề chưa giải quyết, thêm vào TODO.md, ví dụ:

- [ ] Cần bổ sung nguồn cho nhận định về...
- [ ] Cần kiểm tra lại thuật ngữ...
- [ ] Cần thêm dữ liệu cho bảng...
- [ ] Cần hỏi giảng viên hướng dẫn về...
- [ ] Cần thêm BibTeX cho nguồn...
- [ ] Cần bổ sung kịch bản/kết quả thử nghiệm cho Chương 4.
- [ ] Cần chuẩn hóa caption hình theo quy định của trường.
- [ ] Cần bổ sung phụ lục hướng dẫn sử dụng.

### Bước 8 — Báo cáo sau khi hoàn thành

Sau mỗi tác vụ, báo lại cho tôi theo mẫu:

## Báo cáo thay đổi

### File đã thay đổi

- ...

### Mục đã thay đổi

- ...

### Tóm tắt chỉnh sửa

- ...

### Citation

- Citation được giữ:
- Citation được thêm:
- Citation được xóa:
- Citation được đánh dấu [citation needed]:

### Bộ nhớ luận văn

- THESIS_MEMORY.md có được cập nhật không?
- Nếu có, cập nhật phần nào?

### Việc còn lại

- ...

### Giả định đã sử dụng

- ...

## Nếu không thể chỉnh sửa trực tiếp file

Nếu bạn không có quyền chỉnh sửa trực tiếp file trong project, hãy trả về:

1. Tên file cần sửa.
2. Vị trí cần sửa.
3. Nội dung thay thế.
4. Ghi chú cập nhật THESIS_MEMORY.md hoặc TODO.md nếu cần.
