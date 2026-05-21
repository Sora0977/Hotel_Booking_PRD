# AI Instructions

File này quy định cách AI agent làm việc với project luận văn.

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
