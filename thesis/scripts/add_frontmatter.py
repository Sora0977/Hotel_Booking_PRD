from __future__ import annotations

import re
from pathlib import Path


THESIS_ROOT = Path(__file__).resolve().parents[1]
LEVEL3_DIR = THESIS_ROOT / "chapters" / "03_thiet_ke" / "3_2_mo_hinh_xu_ly"
FRONTMATTER_RE = re.compile(r"^---\s*\n", re.MULTILINE)
ALLOWED_STATUS = {"draft", "reviewing", "completed"}
ARCHIVED_SOURCE_FILE = "../../../archive/3_2_mo_hinh_xu_ly_OLD.md.bak"

USECASE_BY_RANGE: tuple[tuple[range, str], ...] = (
    (range(1, 2), "3_2_1_1_usecase_dang_nhap.md"),
    (range(2, 3), "3_2_1_2_usecase_dang_ky.md"),
    (range(3, 8), "3_2_1_3_usecase_quan_ly_thong_tin_ca_nhan.md"),
    (range(8, 11), "3_2_1_4_usecase_quan_tri_nguoi_dung.md"),
    (range(11, 15), "3_2_1_5_usecase_quan_ly_phong.md"),
    (range(15, 19), "3_2_1_6_usecase_tra_cuu_phong.md"),
    (range(19, 25), "3_2_1_7_usecase_quan_ly_khach_san.md"),
    (range(25, 27), "3_2_1_8_usecase_tra_cuu_khach_san.md"),
    (range(27, 29), "3_2_1_9_usecase_quan_ly_dat_phong.md"),
    (range(29, 30), "3_2_1_10_usecase_dat_phong.md"),
    (range(30, 32), "3_2_1_11_usecase_tra_cuu_va_huy_don_dat_phong.md"),
    (range(32, 37), "3_2_1_12_usecase_quan_ly_tien_ich.md"),
)


def has_frontmatter(content: str) -> bool:
    return bool(FRONTMATTER_RE.match(content))


def dependency_for(path: Path) -> str:
    """Suy luận dependency chính để AI biết file nào cần đối chiếu khi chỉnh chunk."""
    stem = path.stem
    numbered_diagram = re.match(r"3_2_[23]_(\d{2})_", stem)
    if numbered_diagram:
        number = int(numbered_diagram.group(1))
        for number_range, usecase_file in USECASE_BY_RANGE:
            if number in number_range:
                return usecase_file

    if stem.startswith("3_2_1_") and "usecase" in stem:
        return "3_2_1_use_case_chi_tiet.md"
    if stem in {"3_2_2_so_do_tuan_tu", "3_2_3_so_do_hoat_dong_activity"}:
        return "3_2_1_use_case_chi_tiet.md"
    if stem == "3_2_1_use_case_chi_tiet":
        return "3_2_0_gioi_thieu_mo_hinh_xu_ly.md"
    return "index.md"


def build_frontmatter(path: Path) -> str:
    dependency = dependency_for(path)
    return f"---\nstatus: draft\ndependencies:\n  - {dependency}\n---\n\n"


def split_frontmatter(content: str) -> tuple[str | None, str]:
    if not has_frontmatter(content):
        return None, content

    lines = content.splitlines(keepends=True)
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    return None, content


def ensure_frontmatter(content: str, path: Path) -> str | None:
    """Thêm hoặc chuẩn hóa metadata tối thiểu mà không đụng phần nội dung chính."""
    frontmatter, body = split_frontmatter(content)
    if frontmatter is None:
        return build_frontmatter(path) + body.lstrip()

    lines = frontmatter.splitlines()
    updated = False

    status_index = next((index for index, line in enumerate(lines) if line.startswith("status:")), None)
    if status_index is None:
        lines.insert(0, "status: draft")
        updated = True
    else:
        status_value = lines[status_index].split(":", 1)[1].strip()
        if status_value not in ALLOWED_STATUS:
            lines[status_index] = "status: draft"
            updated = True

    has_dependencies = any(line.startswith("dependencies:") for line in lines)
    if not has_dependencies:
        status_index = next(index for index, line in enumerate(lines) if line.startswith("status:"))
        lines[status_index + 1 : status_index + 1] = [
            "dependencies:",
            f"  - {dependency_for(path)}",
        ]
        updated = True

    for index, line in enumerate(lines):
        if line.startswith("source_file:") and "3_2_mo_hinh_xu_ly_OLD.md.bak" in line:
            archived_source = f'source_file: "{ARCHIVED_SOURCE_FILE}"'
            if line != archived_source:
                lines[index] = archived_source
                updated = True

    if not updated:
        return None

    normalized_frontmatter = "\n".join(lines).rstrip()
    return f"---\n{normalized_frontmatter}\n---\n{body}"


def add_frontmatter() -> list[Path]:
    if not LEVEL3_DIR.exists():
        raise FileNotFoundError(f"Level-3 directory not found: {LEVEL3_DIR}")

    updated_files: list[Path] = []
    for path in sorted(LEVEL3_DIR.glob("*.md")):
        if path.name.lower() == "index.md":
            continue

        content = path.read_text(encoding="utf-8")
        updated_content = ensure_frontmatter(content, path)
        if updated_content is None:
            continue

        path.write_text(updated_content, encoding="utf-8")
        updated_files.append(path)

    return updated_files


if __name__ == "__main__":
    updated = add_frontmatter()
    print(f"Updated {len(updated)} file(s).")
    for path in updated:
        print(path.relative_to(THESIS_ROOT).as_posix())
