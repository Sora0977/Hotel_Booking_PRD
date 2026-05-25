---
name: draw-thesis-sequence
description: Generate or insert PlantUML Sequence Diagrams for thesis materials using the user's mandatory Vietnamese prompt and formatting rules. Use when asked to draw, recreate, revise, validate, or add sequence diagrams for thesis, markdown thesis files, source code flows, screenshots, or UML sequence outputs.
---

# Draw Thesis Sequence

## Workflow

Use this skill when the user asks to create, update, recreate, or validate a Sequence Diagram for `thesis/`.

1. Read the relevant materials in `thesis/` first. Prefer `thesis/AI_INSTRUCTIONS.md`, `thesis/THESIS_MEMORY.md`, `thesis/compiled_thesis.md`, and the specific chapter, markdown file, code reference, image, or note mentioned by the user.
2. If the task is to recreate an existing diagram from markdown or an image, preserve the original image and caption. Insert the PlantUML block directly below the caption or image as requested.
3. Identify lifelines from left to right, including actors, boundaries, controls, participants, and entities.
4. Preserve message order, message numbering, returns, self-calls, `alt`/`else` branches, and `opt` blocks from the source. Do not add new steps that are not supported by the source.
5. Return only a complete `plantuml` block unless the user explicitly asks for explanation or file edits.
6. Follow the canonical prompt below exactly. Do not weaken, rename, reorder, or reinterpret its rules.

## Canonical Prompt

Use the following prompt exactly as the required drawing standard:

```text
PROMPT
"Bạn là chuyên gia vẽ lại sơ đồ UML bằng PlantUML.

Nhiệm vụ: đọc kỹ sơ đồ gốc hoặc code/ảnh được cung cấp, sau đó viết lại bằng PlantUML sao cho giống nội dung, thứ tự, actor/participant, message, nhánh điều kiện và format nhất có thể.

Yêu cầu bắt buộc:
1. Chỉ dùng PlantUML, đặt trong block ```plantuml.
2. Luôn dùng format trắng đen:
   @startuml
   !theme plain
   skinparam monochrome true
   skinparam shadowing false
   hide footbox
   autoactivate on
3. Nếu là sơ đồ tuần tự:
   - Actor dùng `actor`.
   - Màn hình/Form/View dùng `boundary`.
   - Service/Controller/Control dùng `control`.
   - Dịch vụ ngoài như Cloudinary/Payment/Email dùng `participant`.
   - Database/DB/kho dữ liệu bắt buộc dùng `entity`, không dùng `database`.
   - Giữ đúng thứ tự lifeline từ trái sang phải như hình gốc.
   - Giữ đúng số thứ tự message nếu hình có đánh số.
   - Message gọi xử lý dùng `->`, message trả về dùng `-->`.
   - Có self-call thì dùng `A -> A : nội dung`.
   - Nếu hình có nhánh điều kiện thì dùng đúng `alt`, `else`, `end`.
   - Nếu hình có bước tùy chọn thì dùng `opt`.
   - Không tự thêm bước mới nếu hình/code gốc không có.
4. Title đặt theo mẫu:
   title Sequence Diagram: <tên sơ đồ>
5. Nội dung chữ phải giữ sát hình/code gốc, đặc biệt tên actor, form, service, DB, điều kiện trong alt/else và thông báo lỗi/thành công.
6. Nếu đang chỉnh file markdown:
   - Không xóa hình gốc.
   - Không xóa caption gốc.
   - Chèn block PlantUML ngay dưới caption hoặc ngay dưới hình theo yêu cầu.
7. Trước khi trả lời, tự kiểm tra:
   - Có đủ `@startuml` và `@enduml`.
   - Không còn keyword `database`.
   - Mỗi DB đã là `entity`.
   - Có `autoactivate on`.
   - Mỗi `alt/opt` đều có `end`.
   - Không thiếu message so với hình gốc.

Đầu ra: chỉ trả về code PlantUML hoàn chỉnh, không giải thích dài dòng."
```

## Output Checklist

Before responding or editing a markdown file, verify that the PlantUML:

- Is inside a fenced `plantuml` block when returning diagram code.
- Starts with `@startuml`, `!theme plain`, `skinparam monochrome true`, `skinparam shadowing false`, `hide footbox`, and `autoactivate on`.
- Uses `actor`, `boundary`, `control`, `participant`, and `entity` according to the canonical prompt.
- Does not contain the `database` keyword.
- Preserves lifeline order, message order, message numbering, return arrows, self-calls, `alt`/`else`, and `opt`.
- Uses `title Sequence Diagram: <tên sơ đồ>`.
- Ends every `alt` and `opt` with `end`.
- Ends with `@enduml`.
