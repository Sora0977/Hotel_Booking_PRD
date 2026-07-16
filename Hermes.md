## Có — cấu trúc hiện tại của bạn rất phù hợp với Hermes Agent

Sau khi xem file Repomix bạn gửi, mình đánh giá **nên sử dụng Hermes Agent**. Thậm chí cách bạn tổ chức báo cáo hiện tại phù hợp với agent hơn nhiều so với việc chỉnh trực tiếp một file DOCX lớn.

File XML bạn gửi không phải bản báo cáo để chỉnh trực tiếp; nó là bản đóng gói toàn bộ repository bằng Repomix. Bên trong project, báo cáo thực tế đã được chia thành nhiều file Markdown theo chương, mục và use case; đồng thời có `build_thesis.py`, `compiled_thesis.md`, `compiled_thesis.docx`, `THESIS_MEMORY.md`, `STYLE_GUIDE.md`, `SCHOOL_RULES.md`, `OUTLINE.md` và `AI_INSTRUCTIONS.md`. Đây gần như là cấu trúc được thiết kế sẵn để AI agent làm việc.

## Vì sao Hermes phù hợp với project này?

Quy trình của bạn là:

```text
Source code
    ↓
Phân tích chức năng thực tế
    ↓
Cập nhật từng file Markdown nhỏ
    ↓
Gộp thành compiled_thesis.md
    ↓
Chuyển Markdown thành DOCX
```

Hermes phù hợp ở ba khâu giữa:

1. Đọc source code và tìm bằng chứng kỹ thuật.
    
2. Đối chiếu code với các file báo cáo hiện có.
    
3. Chỉnh sửa trực tiếp từng file Markdown và chạy script kiểm tra.
    

Hermes có công cụ đọc/chỉnh sửa file, chạy terminal và làm việc trực tiếp trong thư mục project. Nó cũng tự động đọc context file cấp project như `.hermes.md` hoặc `AGENTS.md`, phù hợp với bộ quy tắc luận văn mà bạn đã xây dựng. ([Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files?utm_source=chatgpt.com "Context Files | Hermes Agent - nous research"))

## Điểm quan trọng: Hermes chưa tự đọc `AI_INSTRUCTIONS.md`

Project của bạn hiện có:

```text
AI_INSTRUCTIONS.md
THESIS_MEMORY.md
STYLE_GUIDE.md
SCHOOL_RULES.md
OUTLINE.md
TODO.md
```

Nhưng theo tài liệu hiện tại, Hermes ưu tiên context file theo thứ tự:

```text
.hermes.md
AGENTS.md
CLAUDE.md
.cursorrules
```

Nó không mặc định coi `AI_INSTRUCTIONS.md` là context file chính. Vì vậy, bạn nên tạo thêm `AGENTS.md` ở thư mục gốc. Hermes chỉ tự chọn một loại project context file theo thứ tự ưu tiên, nên không cần tạo cả `.hermes.md` lẫn `AGENTS.md`. ([Hermes Agent](https://hermes-agent.nousresearch.com/docs/guides/tips?utm_source=chatgpt.com "Tips & Best Practices | Hermes Agent - nous research"))

Nội dung đề xuất:

# Vai trò

Bạn là AI agent hỗ trợ cập nhật báo cáo luận văn dựa trên source code thực tế của hệ thống.

# Tài liệu bắt buộc phải đọc

Trước khi chỉnh sửa báo cáo, đọc lần lượt:

1. `AI_INSTRUCTIONS.md`
    
2. `THESIS_MEMORY.md`
    
3. `SCHOOL_RULES.md`
    
4. `OUTLINE.md`
    
5. `STYLE_GUIDE.md`
    
6. `TODO.md`
    
7. File Markdown của mục đang được chỉnh sửa
    
8. Những file source code liên quan
    

# Nguyên tắc làm việc

- Source code hiện tại là nguồn bằng chứng chính cho các chức năng của hệ thống.
    
- Không tự suy đoán chức năng khi không tìm thấy bằng chứng trong code.
    
- Không tự tạo số liệu kiểm thử, hiệu năng, bảo mật hoặc kết quả đánh giá.
    
- Không sửa toàn bộ luận văn trong một lần.
    
- Chỉ chỉnh sửa những file thuộc phạm vi công việc hiện tại.
    
- Không chỉnh trực tiếp `compiled_thesis.md` nếu file này được sinh tự động.
    
- Không chỉnh trực tiếp file DOCX đầu ra.
    
- Không sửa các file trong `archive/`.
    
- Không sửa source code trừ khi có yêu cầu rõ ràng.
    
- Giữ nguyên citation key trong Markdown.
    
- Không tự tạo nguồn tham khảo.
    
- Nội dung không xác minh được phải được đánh dấu `[CẦN XÁC NHẬN]`.
    
- Mọi thay đổi quan trọng phải được ghi vào `THESIS_MEMORY.md`.
    
- Những công việc chưa hoàn thành phải được ghi vào `TODO.md`.
    

# Quy trình cập nhật một mục

1. Đọc nội dung báo cáo hiện tại.
    
2. Xác định các nhận định kỹ thuật trong nội dung.
    
3. Tìm bằng chứng tương ứng trong source code.
    
4. Lập danh sách:
    
    - Nội dung còn chính xác.
        
    - Nội dung đã lỗi thời.
        
    - Nội dung còn thiếu.
        
    - Nội dung không có bằng chứng.
        
5. Chỉnh sửa tối thiểu file Markdown liên quan.
    
6. Kiểm tra sự nhất quán với các chương khác.
    
7. Chạy script build báo cáo.
    
8. Kiểm tra lỗi build, liên kết hình, heading và citation.
    
9. Báo cáo danh sách file đã thay đổi và bằng chứng code đã sử dụng.
    

# Yêu cầu truy vết

Khi hoàn thành một nhiệm vụ, cung cấp bảng:

|Nội dung cập nhật|File báo cáo|Bằng chứng source code|Mức độ chắc chắn|
|---|---|---|---|

# Lệnh build

Sử dụng script có sẵn của project để tạo bản Markdown tổng hợp và DOCX.

Không chỉnh sửa file đầu ra để thay thế cho việc chỉnh sửa các file nguồn trong `chapters/`, `front_matter/` hoặc `appendices/`.

## Nên cho Hermes làm việc trên repository thật, không phải chỉ trên file XML

File XML Repomix phù hợp để:

- Tìm hiểu tổng quan repository.
    
- Gửi code cho một AI không truy cập được thư mục project.
    
- Lưu snapshot để đối chiếu.
    
- Phân tích read-only.
    

Nhưng nó không phải bề mặt chỉnh sửa tốt nhất. Ngay phần hướng dẫn trong file cũng xác định bản Repomix nên được coi là read-only và thay đổi phải thực hiện trên repository gốc.

Cấu trúc làm việc nên là:

```text
workspace/
├── application/
│   ├── apps/
│   ├── packages/
│   ├── prisma/
│   └── ...
│
├── thesis/
│   ├── AGENTS.md
│   ├── AI_INSTRUCTIONS.md
│   ├── THESIS_MEMORY.md
│   ├── SCHOOL_RULES.md
│   ├── STYLE_GUIDE.md
│   ├── OUTLINE.md
│   ├── TODO.md
│   ├── chapters/
│   ├── figures/
│   ├── scripts/
│   └── references.bib
│
└── evidence/
    └── code-report-mapping.md
```

Khởi chạy Hermes tại `workspace/` hoặc vị trí mà nó nhìn thấy được cả source code lẫn thư mục luận văn. Hermes hỗ trợ chạy terminal cục bộ, Docker, SSH và một số môi trường sandbox khác; với luận văn và source code quan trọng, Docker hoặc Git worktree sẽ an toàn hơn chạy không giới hạn trực tiếp trên thư mục chính. ([GitHub](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/configuration.md?utm_source=chatgpt.com "hermes-agent/website/docs/user-guide/configuration.md ..."))

## Không nên yêu cầu cập nhật cả luận văn trong một prompt

Project của bạn đã phân mảnh rất sâu, chẳng hạn riêng mục `3.2` đã có các file riêng cho từng use case, sơ đồ tuần tự và sơ đồ hoạt động. Đây là lợi thế lớn, vì agent chỉ cần đọc phần có liên quan thay vì nạp toàn bộ báo cáo vào context.

Hãy giao việc theo đơn vị nhỏ:

```text
Kiểm tra và cập nhật:
chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/
3_2_1_4_usecase_quan_tri_nguoi_dung.md

Đối chiếu với toàn bộ controller, service, guard,
permission và giao diện admin trong source code.

Không sửa những file khác, ngoại trừ:
- THESIS_MEMORY.md
- TODO.md
- evidence/code-report-mapping.md
```

Sau đó lần lượt xử lý:

```text
1. Phân quyền và người dùng
2. Khách sạn
3. Loại phòng và phòng
4. Booking
5. Thanh toán
6. Khuyến mãi
7. Đánh giá
8. Dashboard và báo cáo
9. Kiểm thử
10. Kết luận
```

## Quy trình thực tế nên áp dụng

### Giai đoạn 1: Kiểm kê source code

Chưa sửa báo cáo ngay. Yêu cầu Hermes tạo:

```text
evidence/
├── architecture-inventory.md
├── roles-and-permissions.md
├── features-inventory.md
├── api-inventory.md
├── database-inventory.md
├── frontend-pages-inventory.md
└── test-inventory.md
```

Mỗi chức năng phải có đường dẫn đến controller, service, schema, route và màn hình tương ứng.

### Giai đoạn 2: Đối chiếu báo cáo

Tạo bảng:

|Mục báo cáo|Nội dung cũ|Code hiện tại|Kết luận|
|---|---|---|---|
|Công nghệ backend|Spring Boot|NestJS|Phải viết lại|
|Database|MySQL|Kiểm tra Prisma datasource|Cần xác minh|
|Quản lý khuyến mãi|Chưa có|Có module promotion|Cần bổ sung|
|Dashboard|Nội dung chưa đầy đủ|Có stats và revenue chart|Cần cập nhật|

Điều này đặc biệt quan trọng vì trong nội dung báo cáo cũ của bạn vẫn có mô tả Java, Spring Boot và MySQL, trong khi snapshot source code khác đã xuất hiện cấu trúc NestJS, Prisma và frontend hiện đại. Do đó, không nên chỉ “viết đẹp lại”; cần thực hiện kiểm toán kỹ thuật trước.

### Giai đoạn 3: Cập nhật từng mục Markdown

Hermes chỉ sửa file nguồn nhỏ, không sửa:

```text
compiled_thesis.md
compiled_thesis.docx
compiled_thesis_rules.docx
```

Các file này nên được xem là output.

### Giai đoạn 4: Build và kiểm tra

Sau mỗi nhóm thay đổi:

```bash
python scripts/build_thesis.py
```

Sau đó kiểm tra:

- Script có chạy thành công không.
    
- Heading có đúng cấp không.
    
- Hình có tồn tại không.
    
- Caption có đúng không.
    
- PlantUML có render được không.
    
- Citation key có trong `references.bib` không.
    
- `compiled_thesis.md` có đúng thứ tự không.
    
- DOCX có giữ đúng style của trường không.
    

### Giai đoạn 5: Git review

Mỗi nhiệm vụ nên ở một branch hoặc một commit:

```bash
git checkout -b thesis/update-admin-permissions
git diff
git add chapters/ THESIS_MEMORY.md TODO.md evidence/
git commit -m "docs: update admin permissions from current implementation"
```

Bạn phải xem `git diff` trước khi chấp nhận thay đổi.

## Cấu hình quyền nên giới hạn

Cho Hermes quyền:

```text
Đọc toàn bộ source code
Đọc và sửa thư mục thesis/
Chạy script build
Chạy test hoặc lệnh kiểm tra read-only
Sử dụng git diff và git status
```

Không nên mặc định cho phép:

```text
Xóa hàng loạt file
Push lên remote
Merge branch
Sửa database production
Chạy migration production
Truy cập file .env
Đọc secret hoặc API key
Tự động commit toàn bộ repository
```

## Kết luận

**Với cấu trúc hiện tại, bạn nên dùng Hermes Agent.**

Lý do không chỉ vì báo cáo được viết bằng Markdown, mà vì project của bạn đã có đầy đủ các thành phần phù hợp với agent:

- Báo cáo được chia nhỏ theo chương và mục.
    
- Có bộ nhớ luận văn.
    
- Có quy định trường.
    
- Có style guide.
    
- Có instruction dành cho AI.
    
- Có TODO.
    
- Có archive.
    
- Có script build.
    
- Có Markdown tổng hợp và DOCX đầu ra.
    
- Có thể dùng Git để kiểm tra từng thay đổi.
    

Lựa chọn tốt nhất là:

> **Hermes đọc repository thật, tạo bảng bằng chứng, cập nhật từng file Markdown nhỏ, chạy script build và để bạn duyệt Git diff.**

Không nên sử dụng theo cách:

> **Đưa hai file XML lớn rồi yêu cầu Hermes tự viết lại toàn bộ luận văn trong một lần.**

Bước cần làm ngay là thêm `AGENTS.md`, đặt source code và thư mục luận văn trong cùng workspace, rồi bắt đầu bằng nhiệm vụ **kiểm kê sự khác biệt giữa công nghệ/chức năng trong báo cáo cũ và source code hiện tại**.