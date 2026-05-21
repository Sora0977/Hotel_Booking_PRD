import re
from pathlib import Path


THESIS_ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = THESIS_ROOT / "chapters"
OUTPUT_FILE = THESIS_ROOT / "compiled_thesis.md"
SEPARATOR = "\n\n"
NATURAL_SPLIT_RE = re.compile(r"(\d+)")
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HTTP_LINK_RE = re.compile(r"^https?://", re.IGNORECASE)
PLANTUML_BLOCK_RE = re.compile(r"```plantuml.*?```", re.DOTALL | re.IGNORECASE)
YAML_FRONTMATTER_RE = re.compile(r"^\s*---\n.*?\n---\n", re.DOTALL)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


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


def is_backup(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".bak") or ".bak." in name


def is_index(path: Path) -> bool:
    return path.name.lower() == "index.md"


def is_legacy_aggregate(path: Path) -> bool:
    """Skip a top-level chapter file when a same-stem chunk directory exists."""
    return path.parent == CHAPTERS_DIR and (CHAPTERS_DIR / path.stem).is_dir()


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


def strip_plantuml_blocks(content: str) -> str:
    return PLANTUML_BLOCK_RE.sub("", content)


def strip_yaml_frontmatter(content: str) -> str:
    return YAML_FRONTMATTER_RE.sub("", content, count=1)


def strip_html_comments(content: str) -> str:
    return HTML_COMMENT_RE.sub("", content)


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(CHAPTERS_DIR.rglob("*.md"), key=sort_key):
        if is_index(path) or is_backup(path) or is_legacy_aggregate(path):
            continue
        files.append(path)
    return files


def build() -> int:
    if not CHAPTERS_DIR.exists():
        raise FileNotFoundError(f"Chapters directory not found: {CHAPTERS_DIR}")

    chunks = []
    for path in iter_markdown_files():
        content = path.read_text(encoding="utf-8")
        content = strip_yaml_frontmatter(content)
        content = strip_html_comments(content)
        content = content.strip()

        if content:
            content = fix_image_paths(content)
            # content = strip_plantuml_blocks(content)

            content = content.strip()
            content = re.sub(r"\n{3,}", "\n\n", content)

            if content:
                chunks.append(content)

    OUTPUT_FILE.write_text(SEPARATOR.join(chunks) + "\n", encoding="utf-8")
    return len(chunks)


if __name__ == "__main__":
    count = build()
    print(f"Compiled {count} Markdown files into {OUTPUT_FILE}")
