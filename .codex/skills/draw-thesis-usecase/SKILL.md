---
name: draw-thesis-usecase
description: Generate PlantUML Use Case diagrams for the thesis folder using the user's mandatory Vietnamese prompt and UML layout rules. Use when asked to draw, create, revise, or validate use case diagrams for thesis or PlantUML use case outputs.
---

# Draw Thesis Use Case

## Workflow

Use this skill when the user asks to create, update, or review a Use Case Diagram for `thesis/`.

1. Read the relevant materials in `thesis/` first. Prefer `thesis/AI_INSTRUCTIONS.md`, `thesis/THESIS_MEMORY.md`, `thesis/compiled_thesis.md`, and the specific chapter or note mentioned by the user.
2. Identify the system/module name, actors, main/base use cases, child/specialized use cases, include use cases, extend use cases, and any system boundary groups.
3. Produce complete PlantUML only, unless the user asks for explanation too.
4. Follow the canonical prompt below exactly. Do not weaken, rename, reorder, or reinterpret its rules.
5. Keep the final diagram scoped. If the thesis context contains many modules, create separate diagrams instead of one giant diagram.
6. If business details are missing, make the smallest reasonable assumption and state it briefly before the PlantUML.

## Canonical Prompt

Use the following prompt exactly as the required drawing standard:

```text
PROMPT
"Hãy đóng vai trò là một Kiến trúc sư phần mềm (Software Architect). Nhiệm vụ của bạn là viết mã PlantUML để vẽ Biểu đồ Use Case (Use Case Diagram) chuẩn UML cho hệ thống/module: [TÊN HỆ THỐNG / MODULE CẦN VẼ - Ví dụ: Quản lý Kho].
YÊU CẦU CHI TIẾT VÀ QUY TẮC VẼ (BẮT BUỘC TUÂN THỦ):
1. Giao diện & Hướng biểu đồ (Theme & Layout):

Bắt buộc phải sử dụng dòng !theme plain ở ngay đầu đoạn mã.
Bắt buộc phải sử dụng từ khóa left to right direction ngay dưới phần khai báo theme để dàn trang cơ bản.
Tuyệt đối KHÔNG sử dụng skinparam actorStyle awesome hay bất kỳ skinparam nào khác làm thay đổi style mặc định của biểu đồ.
2. Cấu trúc & Gom nhóm:

Không vẽ gộp tất cả vào một diagram khổng lồ.
Chỉ sử dụng từ khóa rectangle để thể hiện ranh giới hệ thống (System Boundary) hoặc gom nhóm các cụm chức năng logic có liên quan.
Tuyệt đối KHÔNG sử dụng từ khóa package, và bên trong rectangle không được chứa bất kỳ package nào.
3. Quy tắc không lồng ghép (No nesting):

Tuyệt đối KHÔNG vẽ lồng Use Case con bên trong Use Case cha.
Tất cả các Use Case phải được định nghĩa độc lập và liên kết với nhau bằng các mũi tên quan hệ.
4. Mối quan hệ chuẩn UML (Rất quan trọng về hướng mũi tên):

<<include>>: Thể hiện quy trình bắt buộc. Hướng mũi tên chuẩn: Base Use Case ..> Included Use Case : <<include>>.
<<extend>>: Thể hiện quy trình mở rộng, tùy chọn hoặc ngoại lệ. Hướng mũi tên chuẩn: Extended Use Case .> Base Use Case : <<extend>>. (Mẹo: Bắt buộc sử dụng mũi tên trỏ lên .up.> nếu muốn ép các Use Case thông báo/ngoại lệ rơi xuống vị trí dưới cùng của biểu đồ).
Generalization (Kế thừa): Dùng khi Use case con là một trường hợp cụ thể của Use case cha. Bắt buộc sử dụng hướng mũi tên trỏ lên: Child Use Case -up-|> Parent Use Case. Việc này cực kỳ quan trọng để ép Use Case cha neo ở vị trí trên cùng, giúp các Use Case con tự động dàn dọc ngay ngắn xuống bên dưới.
5. Actor:

Actor kết nối trực tiếp (-->) với các Use Case chính (Base Use Case) mà họ tham gia thực hiện.
6. Thứ tự bố cục và luồng hoạt động (Layout & Flow Order):

Vị trí hiển thị bắt buộc: Actor và Use Case chính/cha phải nằm ở góc trên cùng bên trái của biểu đồ. Các Use Case con phải được xếp tuần tự dọc xuống bên dưới. Các Use Case phụ trợ (Include, Extend) tản ra phía bên phải hoặc sát đáy.
Mẹo cho code: Để PlantUML render đúng bố cục này:
Hãy khai báo code theo thứ tự logic: Khai báo Actor trước -> Khai báo Use Case chính -> Khai báo các Use Case con -> Khai báo các Use Case phụ trợ.
Phải tuân thủ tuyệt đối việc dùng -up-|> cho quan hệ kế thừa để giữ cụm Use Case cha + Actor ở trên cao nhất.
KỊCH BẢN CẦN VẼ: Dựa trên các quy tắc trên, hãy phân tích và vẽ biểu đồ cho các thông tin sau:

Các Actor tham gia: [LIỆT KÊ CÁC ACTOR - Ví dụ: Thủ kho, Quản lý].
Yêu cầu nghiệp vụ / Danh sách Use Case: [MÔ TẢ CHI TIẾT LUỒNG NGHIỆP VỤ HOẶC DANH SÁCH CHỨC NĂNG Ở ĐÂY. Nêu rõ chức năng nào include chức năng nào, chức năng nào extend từ đâu...].
Hãy cung cấp code PlantUML hoàn chỉnh và có logic phân bổ rõ ràng."
```

## Output Checklist

Before responding, verify that the PlantUML:

- Starts with `@startuml`, then `!theme plain`, then `left to right direction`.
- Does not contain `package`, `skinparam actorStyle awesome`, or unrelated `skinparam` overrides.
- Uses `rectangle` only for system boundaries or logical function groups.
- Defines every use case independently.
- Uses `Base ..> Included : <<include>>`.
- Uses `Extended .> Base : <<extend>>`, or `.up.>` when forcing extension/notification use cases toward the bottom.
- Uses `Child -up-|> Parent` for generalization.
- Connects actors directly to base use cases with `-->`.
