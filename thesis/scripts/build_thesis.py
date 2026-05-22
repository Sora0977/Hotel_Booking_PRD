import hashlib
import re
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urldefrag
from urllib.request import Request, urlopen


THESIS_ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = THESIS_ROOT / "chapters"
OUTPUT_FILE = THESIS_ROOT / "compiled_thesis.md"
READONLY_OUTPUT_FILE = THESIS_ROOT / "compiled_thesis_readonly.md"
GENERATED_FIGURES_DIR = THESIS_ROOT / "figures" / "generated"
SEPARATOR = "\n\n"
PLANTUML_SERVER_URL = "http://www.plantuml.com/plantuml/png"
PLANTUML_TIMEOUT_SECONDS = 20

NATURAL_SPLIT_RE = re.compile(r"(\d+)")
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)")
HTTP_LINK_RE = re.compile(r"^https?://", re.IGNORECASE)
EXTERNAL_LINK_RE = re.compile(r"^(?:https?://|mailto:|tel:|ftp://|data:)", re.IGNORECASE)
PLANTUML_BLOCK_RE = re.compile(r"```plantuml[^\n]*\n(.*?)(?:\n```|```)", re.DOTALL | re.IGNORECASE)
YAML_FRONTMATTER_RE = re.compile(r"^\s*---\n.*?\n---\n", re.DOTALL)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


@dataclass(frozen=True)
class Chunk:
    path: Path
    content: str
    anchor: str


@dataclass(frozen=True)
class BuildStats:
    chunk_count: int
    diagram_count: int
    warning_count: int


def natural_sort_key(value: str) -> tuple[tuple[int, object], ...]:
    parts: list[tuple[int, object]] = []
    for token in NATURAL_SPLIT_RE.split(value.lower()):
        if not token:
            continue
        if token.isdigit():
            parts.append((1, int(token)))
        else:
            parts.append((0, token))
    return tuple(parts)


def sort_key(path: Path) -> tuple[tuple[tuple[int, object], ...], ...]:
    return tuple(natural_sort_key(part) for part in path.relative_to(CHAPTERS_DIR).parts)


def warn(warnings: list[str], message: str) -> None:
    warnings.append(message)
    safe_print(f"Warning: {message}")


def safe_print(message: str) -> None:
    """In UTF-8 an toàn trên Windows console có codepage hẹp như cp1252."""
    try:
        print(message)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(f"{message}\n".encode("utf-8", errors="replace"))


def is_backup(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".bak") or ".bak." in name


def is_index(path: Path) -> bool:
    return path.name.lower() == "index.md"


def is_legacy_aggregate(path: Path) -> bool:
    """Skip a top-level chapter file when a same-stem chunk directory exists."""
    return path.parent == CHAPTERS_DIR and (CHAPTERS_DIR / path.stem).is_dir()


def should_skip_markdown(path: Path) -> bool:
    return is_index(path) or is_backup(path) or is_legacy_aggregate(path)


def normalize_image_target(target: str) -> str:
    value = target.strip()
    if HTTP_LINK_RE.match(value):
        return target

    title_suffix = ""
    if " " in value and not value.startswith("<"):
        value, title_suffix = value.split(maxsplit=1)
        title_suffix = f" {title_suffix}"

    has_angle_brackets = value.startswith("<") and value.endswith(">")
    image_path = value[1:-1] if has_angle_brackets else value
    image_path = image_path.replace("\\", "/")
    image_path = re.sub(r"^(?:\.\./)+", "", image_path)
    image_path = re.sub(r"^\./+", "", image_path)

    figures_index = image_path.find("figures/")
    if figures_index >= 0:
        image_path = image_path[figures_index:]

    if has_angle_brackets:
        image_path = f"<{image_path}>"
    return f"{image_path}{title_suffix}"


def fix_image_paths(content: str) -> str:
    def replace(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        target = match.group(2)
        return f"![{alt_text}]({normalize_image_target(target)})"

    return MARKDOWN_IMAGE_RE.sub(replace, content)


def strip_yaml_frontmatter(content: str) -> str:
    return YAML_FRONTMATTER_RE.sub("", content, count=1)


def strip_html_comments(content: str) -> str:
    return HTML_COMMENT_RE.sub("", content)


def split_inline_link_target(raw_target: str) -> tuple[str, str]:
    """Tách path và title trong cú pháp Markdown link để giữ nguyên title nếu có."""
    value = raw_target.strip()
    if value.startswith("<"):
        closing_index = value.find(">")
        if closing_index >= 0:
            target = value[1:closing_index]
            return target, value[closing_index + 1 :]

    if " " in value:
        target, title = value.split(maxsplit=1)
        if title.startswith(('"', "'", "(")):
            return target, f" {title}"

    return value, ""


def resolve_markdown_target(source_path: Path, raw_target: str) -> Path | None:
    target, _title = split_inline_link_target(raw_target)
    target_without_fragment, _fragment = urldefrag(target)
    if not target_without_fragment or EXTERNAL_LINK_RE.match(target_without_fragment):
        return None

    normalized_target = unquote(target_without_fragment).replace("\\", "/")
    if Path(normalized_target).suffix.lower() != ".md":
        return None
    return (source_path.parent / normalized_target).resolve()


def iter_index_targets(index_path: Path) -> list[Path]:
    content = index_path.read_text(encoding="utf-8")
    targets: list[Path] = []
    for match in MARKDOWN_LINK_RE.finditer(content):
        resolved = resolve_markdown_target(index_path, match.group(2))
        if resolved is not None:
            targets.append(resolved)
    return targets


def find_relocated_target(missing_target: Path) -> Path | None:
    """Tìm target đã bị di chuyển để index cũ vẫn giữ được thứ tự logic."""
    parent_name = missing_target.parent.name.lower()
    candidates: list[Path] = []

    for candidate in CHAPTERS_DIR.rglob(missing_target.name):
        if not candidate.exists():
            continue
        if candidate.parent.name.lower() == parent_name:
            candidates.append(candidate.resolve())

    if not candidates and missing_target.name.lower() != "index.md":
        candidates = [candidate.resolve() for candidate in CHAPTERS_DIR.rglob(missing_target.name)]

    if not candidates:
        return None

    return sorted(candidates, key=sort_key)[0]


def iter_markdown_files(warnings: list[str]) -> list[Path]:
    """Ưu tiên thứ tự trong index.md, sau đó bổ sung các file còn thiếu theo cây thư mục."""
    files: list[Path] = []
    seen_files: set[Path] = set()
    visited_indexes: set[Path] = set()

    def add_file(path: Path) -> None:
        resolved = path.resolve()
        if resolved in seen_files or should_skip_markdown(resolved):
            return
        seen_files.add(resolved)
        files.append(resolved)

    def visit_index(index_path: Path) -> None:
        resolved_index = index_path.resolve()
        if resolved_index in visited_indexes:
            return
        visited_indexes.add(resolved_index)

        if not resolved_index.exists():
            warn(warnings, f"Không tìm thấy index target: {index_path}")
            return

        for target in iter_index_targets(resolved_index):
            if not target.exists():
                relocated_target = find_relocated_target(target)
                if relocated_target is None:
                    warn(warnings, f"Không tìm thấy markdown target trong index: {target}")
                    continue
                warn(warnings, f"Index target đã di chuyển, dùng target mới: {relocated_target}")
                target = relocated_target
            if is_index(target):
                visit_index(target)
            else:
                add_file(target)

    root_index = CHAPTERS_DIR / "index.md"
    if root_index.exists():
        visit_index(root_index)

    for path in sorted(CHAPTERS_DIR.rglob("*.md"), key=sort_key):
        add_file(path)

    return files


def clean_chunk_content(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    content = strip_yaml_frontmatter(content)
    content = strip_html_comments(content)
    content = fix_image_paths(content.strip())
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()


def extract_first_heading(content: str, path: Path) -> str:
    match = HEADING_RE.search(content)
    if match:
        return match.group(1).strip()
    return path.stem.replace("_", " ")


def slugify_heading(heading: str) -> str:
    """Tạo anchor kiểu GitHub/Pandoc, giữ dấu tiếng Việt để link dễ đọc."""
    text = re.sub(r"`([^`]*)`", r"\1", heading)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[_\s-]+", "-", text, flags=re.UNICODE).strip("-")
    return text or "section"


def unique_anchor(base_anchor: str, used_anchors: dict[str, int]) -> str:
    count = used_anchors.get(base_anchor, 0)
    used_anchors[base_anchor] = count + 1
    if count == 0:
        return base_anchor
    return f"{base_anchor}-{count}"


def prepare_chunks(paths: list[Path]) -> list[Chunk]:
    chunks: list[Chunk] = []
    used_anchors: dict[str, int] = {}

    for path in paths:
        content = clean_chunk_content(path)
        if not content:
            continue

        heading = extract_first_heading(content, path)
        anchor = unique_anchor(slugify_heading(heading), used_anchors)
        chunks.append(Chunk(path=path, content=content, anchor=anchor))

    return chunks


def rewrite_internal_links(content: str, source_path: Path, path_to_anchor: dict[Path, str]) -> str:
    """Đổi link .md tương đối sang anchor để file gộp không bị gãy link."""
    def replace(match: re.Match[str]) -> str:
        label = match.group(1)
        raw_target = match.group(2)
        target, title_suffix = split_inline_link_target(raw_target)
        target_without_fragment, fragment = urldefrag(target)

        if not target_without_fragment or EXTERNAL_LINK_RE.match(target_without_fragment):
            return match.group(0)

        normalized_target = unquote(target_without_fragment).replace("\\", "/")
        if Path(normalized_target).suffix.lower() != ".md":
            return match.group(0)

        resolved_target = (source_path.parent / normalized_target).resolve()
        if resolved_target not in path_to_anchor:
            return match.group(0)

        anchor = slugify_heading(unquote(fragment)) if fragment else path_to_anchor[resolved_target]
        return f"[{label}](#{anchor}{title_suffix})"

    return MARKDOWN_LINK_RE.sub(replace, content)


def encode_6bit(value: int) -> str:
    return PLANTUML_ALPHABET[value & 0x3F]


def append_3_bytes(byte_1: int, byte_2: int, byte_3: int) -> str:
    char_1 = byte_1 >> 2
    char_2 = ((byte_1 & 0x3) << 4) | (byte_2 >> 4)
    char_3 = ((byte_2 & 0xF) << 2) | (byte_3 >> 6)
    char_4 = byte_3 & 0x3F
    return "".join(encode_6bit(value) for value in (char_1, char_2, char_3, char_4))


def plantuml_encode(source: str) -> str:
    """Nén PlantUML bằng raw deflate và bảng mã 6-bit của PlantUML server."""
    compressed = zlib.compress(source.encode("utf-8"))[2:-4]
    encoded_parts: list[str] = []

    for index in range(0, len(compressed), 3):
        byte_1 = compressed[index]
        byte_2 = compressed[index + 1] if index + 1 < len(compressed) else 0
        byte_3 = compressed[index + 2] if index + 2 < len(compressed) else 0
        encoded_parts.append(append_3_bytes(byte_1, byte_2, byte_3))

    return "".join(encoded_parts)


def diagram_filename(source_path: Path, diagram_index: int, plantuml_source: str) -> str:
    digest = hashlib.sha1(plantuml_source.encode("utf-8")).hexdigest()[:12]
    short_stem = re.sub(r"[^A-Za-z0-9_-]+", "_", source_path.stem)[:48].strip("_")
    return f"{short_stem}_{diagram_index:02d}_{digest}.png"


def render_plantuml_png(plantuml_source: str, output_path: Path) -> None:
    encoded_diagram = plantuml_encode(plantuml_source)
    request = Request(
        f"{PLANTUML_SERVER_URL}/{encoded_diagram}",
        headers={"User-Agent": "thesis-build/1.0"},
    )

    with urlopen(request, timeout=PLANTUML_TIMEOUT_SECONDS) as response:
        image_data = response.read()

    if not image_data.startswith(b"\x89PNG"):
        raise RuntimeError("PlantUML API không trả về dữ liệu PNG hợp lệ")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = output_path.with_suffix(".tmp")
    temporary_output.write_bytes(image_data)
    temporary_output.replace(output_path)


def inject_plantuml_images(content: str, source_path: Path, warnings: list[str]) -> tuple[str, int]:
    """Render từng block PlantUML và chèn ảnh ngay dưới code block trong bản build."""
    diagram_counter = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal diagram_counter
        diagram_counter += 1

        plantuml_source = match.group(1).strip()
        if not plantuml_source:
            return match.group(0)

        image_path = GENERATED_FIGURES_DIR / diagram_filename(source_path, diagram_counter, plantuml_source)
        if not image_path.exists():
            try:
                render_plantuml_png(plantuml_source, image_path)
            except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as exc:
                warn(warnings, f"Không render được PlantUML trong {source_path.name}: {exc}")
                return match.group(0)

        relative_image_path = image_path.relative_to(THESIS_ROOT).as_posix()
        return f"{match.group(0)}\n\n![Diagram]({relative_image_path})"

    content_with_images = PLANTUML_BLOCK_RE.sub(replace, content)
    return content_with_images, diagram_counter


def build() -> BuildStats:
    if not CHAPTERS_DIR.exists():
        raise FileNotFoundError(f"Chapters directory not found: {CHAPTERS_DIR}")

    warnings: list[str] = []
    chunks = prepare_chunks(iter_markdown_files(warnings))
    path_to_anchor = {chunk.path.resolve(): chunk.anchor for chunk in chunks}

    compiled_chunks: list[str] = []
    diagram_count = 0
    for chunk in chunks:
        content = rewrite_internal_links(chunk.content, chunk.path, path_to_anchor)
        content, chunk_diagram_count = inject_plantuml_images(content, chunk.path, warnings)
        content = re.sub(r"\n{3,}", "\n\n", content).strip()
        if content:
            compiled_chunks.append(content)
            diagram_count += chunk_diagram_count

    compiled_content = SEPARATOR.join(compiled_chunks) + "\n"
    OUTPUT_FILE.write_text(compiled_content, encoding="utf-8")
    READONLY_OUTPUT_FILE.write_text(compiled_content, encoding="utf-8")

    return BuildStats(
        chunk_count=len(compiled_chunks),
        diagram_count=diagram_count,
        warning_count=len(warnings),
    )


if __name__ == "__main__":
    stats = build()
    safe_print(
        f"Compiled {stats.chunk_count} Markdown files into {OUTPUT_FILE} "
        f"and {READONLY_OUTPUT_FILE}"
    )
    safe_print(f"Processed {stats.diagram_count} PlantUML block(s) with {stats.warning_count} warning(s)")
