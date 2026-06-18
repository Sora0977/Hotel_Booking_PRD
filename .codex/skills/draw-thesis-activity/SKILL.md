---
name: draw-thesis-activity
description: Generate or insert PlantUML Activity Diagrams for thesis materials using the user's mandatory Vietnamese prompt and formatting rules. Use when asked to draw, recreate, revise, validate, or add activity diagrams for thesis, markdown thesis files, screenshots, UML images, workflows, swimlanes, decisions, loops, or fork/join flows.
---

# Draw Thesis Activity

## Workflow

Use this skill when the user asks to create, update, recreate, or validate an Activity Diagram for `thesis/`.

1. Read the relevant materials in `thesis/` first. Prefer `thesis/AI_INSTRUCTIONS.md`, `thesis/THESIS_MEMORY.md`, `thesis/compiled_thesis.md`, and the specific chapter, markdown file, image, workflow, or note mentioned by the user.
2. If the task is to recreate an existing diagram from markdown or an image, preserve the original image and caption. Insert the PlantUML block directly below the caption or image as requested.
3. Identify swimlanes/partitions, actions, decisions, True/False labels, error/success branches, loops, fork/join flows, start, and end.
4. Preserve the source flow exactly. Do not add new steps, rename labels, or simplify branches unless the source explicitly supports it.
5. Return only a complete `plantuml` block unless the user explicitly asks for explanation or file edits.
6. Follow the canonical prompt below exactly. Do not weaken, rename, reorder, or reinterpret its rules.

## Canonical Prompt

Use the following prompt exactly as the required drawing standard:

````text
PROMPT
"Bạn là chuyên gia vẽ lại sơ đồ UML bằng PlantUML.

Nhiệm vụ:
Hãy đọc kỹ hình sơ đồ UML được cung cấp và vẽ lại bằng code PlantUML sao cho giống hình gốc nhất có thể.

Yêu cầu bắt buộc:
1. Không được thay đổi nội dung, luồng xử lý, tên actor/swimlane, action, điều kiện, nhánh True/False, nhánh lỗi, nhánh thành công, fork/join, start/end so với hình gốc.
2. Vẽ đúng loại sơ đồ trong hình:
   - Nếu là activity diagram thì dùng activity syntax của PlantUML.
   - Nếu có swimlane/partition như Guest, User, Admin, System thì phải giữ đúng.
   - Nếu có decision node thì dùng `if/else/endif`.
   - Nếu có vòng lặp nhập lại/chọn lại/upload lại thì thể hiện bằng `repeat/repeat while` hoặc cấu trúc tương đương.
   - Nếu có xử lý song song thì dùng `fork/fork again/end fork`.
3. Format phải là trắng đen, dùng theme plain.
4. Mỗi sơ đồ phải có đầy đủ:
   - `@startuml`
   - `!theme plain`
   - `skinparam monochrome true`
   - `skinparam shadowing false`
   - `title ...`
   - nội dung sơ đồ
   - `@enduml`
5. Giữ nguyên tiếng Việt và dấu câu trong hình. Không tự ý sửa câu chữ, không thêm bước mới nếu hình không có.
6. Ưu tiên bố cục giống hình gốc: actor/swimlane bên trái, System bên phải, các nhánh lỗi/thành công đúng hướng logic.
7. Chỉ trả về code PlantUML trong fenced code block `plantuml`, không giải thích dài dòng.

Mẫu output:

```plantuml
@startuml
!theme plain
skinparam monochrome true
skinparam shadowing false
title Activity Diagram: [Tên quy trình]

|[Actor/User/Admin/Guest]|
start
:[Hành động đầu tiên];

|System|
:[Hành động hệ thống];

if ([Điều kiện?]) then ([True])
  :[Luồng thành công];
  stop
else ([False])
  :[Luồng lỗi];
  stop
endif

@enduml."
````

## Output Checklist

Before responding or editing a markdown file, verify that the PlantUML:

- Is inside a fenced `plantuml` block when returning diagram code.
- Starts with `@startuml`, `!theme plain`, `skinparam monochrome true`, and `skinparam shadowing false`.
- Includes `title Activity Diagram: <tên quy trình>` or the exact title required by the source.
- Uses PlantUML activity syntax for activity diagrams.
- Preserves swimlane/partition names, actions, conditions, True/False labels, error/success branches, fork/join, start, and end from the source.
- Uses `if`/`else`/`endif` for decision nodes.
- Uses `repeat`/`repeat while` or an equivalent structure for repeat loops.
- Uses `fork`/`fork again`/`end fork` for parallel processing.
- Ends with `@enduml`.
