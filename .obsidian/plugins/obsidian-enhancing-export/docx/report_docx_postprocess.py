import argparse
import re

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor


FONT_NAME = "Times New Roman"
BLACK = RGBColor(0, 0, 0)
BLACK_HEX = "000000"
BODY_SIZE_PT = 13
LINE_SPACING = 1.3
SPACING_BEFORE_PT = 6
SPACING_AFTER_PT = 0
DEFAULT_TOPIC = "ỨNG DỤNG TRA CỨU VÀ LƯU TRỮ CÔNG THỨC NẤU ĂN"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def w_tag(name):
    return f"{{{W_NS}}}{name}"


def get_or_add(parent, child_tag):
    child = parent.find(qn(child_tag))
    if child is None:
        child = OxmlElement(child_tag)
        parent.append(child)
    return child


def set_times_new_roman_rpr(rpr, size_pt=None):
    rfonts = get_or_add(rpr, "w:rFonts")
    for key in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(qn(f"w:{key}"), FONT_NAME)
    for key in ("asciiTheme", "hAnsiTheme", "csTheme", "cstheme", "eastAsiaTheme"):
        theme_attr = qn(f"w:{key}")
        if theme_attr in rfonts.attrib:
            del rfonts.attrib[theme_attr]

    color = get_or_add(rpr, "w:color")
    color.set(qn("w:val"), BLACK_HEX)

    if size_pt is not None:
        half_points = str(int(size_pt * 2))
        size = get_or_add(rpr, "w:sz")
        size.set(qn("w:val"), half_points)
        complex_size = get_or_add(rpr, "w:szCs")
        complex_size.set(qn("w:val"), half_points)


def set_style_xml_font(style, size_pt):
    rpr = get_or_add(style._element, "w:rPr")
    set_times_new_roman_rpr(rpr, size_pt=size_pt)


def set_run_font(run, size_pt=BODY_SIZE_PT, bold=None, italic=None, underline=None, all_caps=None):
    run.font.name = FONT_NAME
    run.font.size = Pt(size_pt)
    run.font.color.rgb = BLACK
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if underline is not None:
        run.font.underline = underline
    if all_caps is not None:
        run.font.all_caps = all_caps
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = rpr._add_rFonts()
    for key in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(w_tag(key), FONT_NAME)
    set_times_new_roman_rpr(rpr, size_pt=size_pt)


def configure_style(style, size_pt, bold=False, italic=False, underline=False, all_caps=False, alignment=None):
    font = style.font
    font.name = FONT_NAME
    font.size = Pt(size_pt)
    font.color.rgb = BLACK
    font.bold = bold
    font.italic = italic
    font.underline = underline
    font.all_caps = all_caps
    set_style_xml_font(style, size_pt)

    paragraph_format = style.paragraph_format
    paragraph_format.space_before = Pt(SPACING_BEFORE_PT)
    paragraph_format.space_after = Pt(SPACING_AFTER_PT)
    paragraph_format.line_spacing = LINE_SPACING
    if alignment is not None:
        paragraph_format.alignment = alignment


def get_or_add_style(document, name, style_type=WD_STYLE_TYPE.PARAGRAPH):
    try:
        return document.styles[name]
    except KeyError:
        return document.styles.add_style(name, style_type)


def ensure_styles(document):
    configure_style(document.styles["Normal"], BODY_SIZE_PT)
    configure_style(document.styles["Body Text"], BODY_SIZE_PT)
    configure_style(document.styles["Title"], 18, bold=True, all_caps=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    configure_style(document.styles["Heading 1"], 24, bold=True, all_caps=True, alignment=WD_ALIGN_PARAGRAPH.RIGHT)
    configure_style(document.styles["Heading 2"], 15, bold=True, all_caps=True)
    configure_style(document.styles["Heading 3"], 14, bold=True)
    configure_style(document.styles["Heading 4"], 13, underline=True)
    configure_style(document.styles["Heading 5"], 13)
    configure_style(document.styles["Caption"], 13, bold=True, underline=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    configure_style(get_or_add_style(document, "TOC Title"), 18, bold=True, all_caps=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    configure_style(get_or_add_style(document, "Figure"), BODY_SIZE_PT, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    for heading_level in range(6, 10):
        configure_style(document.styles[f"Heading {heading_level}"], BODY_SIZE_PT)
    configure_style(document.styles["Header"], BODY_SIZE_PT, italic=True)
    configure_style(document.styles["Footer"], BODY_SIZE_PT, italic=True)
    set_document_defaults(document)


def heading_style_for_text(text):
    stripped = text.strip()
    if re.match(r"^(mục lục|danh mục)", stripped, flags=re.IGNORECASE):
        return "TOC Title"
    if re.match(r"^(tài liệu tham khảo|kết luận|phụ lục)", stripped, flags=re.IGNORECASE):
        return "Heading 1"
    if re.match(r"^(chương|phần)\s+\S+", stripped, flags=re.IGNORECASE):
        return "Heading 1"
    if re.match(r"^\d+\.\s+\S+", stripped):
        return "Heading 1"
    if re.match(r"^\d+\.\d+\.?\s+\S+", stripped):
        return "Heading 2"
    if re.match(r"^\d+\.\d+\.\d+\.?\s+\S+", stripped):
        return "Heading 3"
    if re.match(r"^\d+\.\d+\.\d+\.\d+\.?\s+\S+", stripped):
        return "Heading 4"
    return None


def is_heading_style(paragraph):
    return paragraph.style and paragraph.style.name.startswith("Heading")


def paragraph_has_drawing(paragraph):
    return bool(paragraph._p.findall(".//w:drawing", NS) or paragraph._p.findall(".//w:pict", NS))


def restyle_caption(paragraph):
    text = paragraph.text.strip()
    paragraph.clear()
    paragraph.style = "Caption"
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    match = re.match(r"^(Hình\s+[0-9]+(?:[-.][0-9]+)*\s*:)(.*)$", text, flags=re.IGNORECASE)
    if match:
        label, rest = match.groups()
        label_run = paragraph.add_run(label)
        set_run_font(label_run, bold=True, italic=True, underline=True)
        rest_run = paragraph.add_run(rest)
        set_run_font(rest_run, bold=True, italic=False, underline=True)
    else:
        run = paragraph.add_run(text)
        set_run_font(run, bold=True, italic=True, underline=True)


def direct_format_for_style(style_name):
    style_formats = {
        "Title": {"size_pt": 18, "bold": True, "all_caps": True},
        "TOC Title": {"size_pt": 18, "bold": True, "all_caps": True},
        "Heading 1": {"size_pt": 24, "bold": True, "all_caps": True},
        "Heading 2": {"size_pt": 15, "bold": True, "all_caps": True},
        "Heading 3": {"size_pt": 14, "bold": True},
        "Heading 4": {"size_pt": 13, "underline": True},
        "Heading 5": {"size_pt": 13},
        "Heading 6": {"size_pt": 13},
        "Heading 7": {"size_pt": 13},
        "Heading 8": {"size_pt": 13},
        "Heading 9": {"size_pt": 13},
        "Caption": {"size_pt": 13, "bold": True, "underline": True},
    }
    return style_formats.get(style_name, {"size_pt": BODY_SIZE_PT})


def apply_direct_run_format(paragraph):
    style_name = paragraph.style.name if paragraph.style else ""
    run_format = direct_format_for_style(style_name)
    for run in paragraph.runs:
        set_run_font(run, **run_format)


def border_element(name):
    element = OxmlElement(f"w:{name}")
    element.set(qn("w:val"), "single")
    element.set(qn("w:sz"), "4")
    element.set(qn("w:space"), "0")
    element.set(qn("w:color"), BLACK_HEX)
    return element


def replace_border(parent, name):
    existing = parent.find(qn(f"w:{name}"))
    if existing is not None:
        parent.remove(existing)
    parent.append(border_element(name))


def set_table_all_borders(table):
    try:
        table.style = "Table Grid"
    except KeyError:
        pass

    tbl_pr = table._tbl.tblPr
    if tbl_pr is None:
        tbl_pr = OxmlElement("w:tblPr")
        table._tbl.insert(0, tbl_pr)

    tbl_borders = tbl_pr.find(qn("w:tblBorders"))
    if tbl_borders is None:
        tbl_borders = OxmlElement("w:tblBorders")
        tbl_pr.append(tbl_borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        replace_border(tbl_borders, edge)


def set_cell_all_borders(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = tc_pr.find(qn("w:tcBorders"))
    if tc_borders is None:
        tc_borders = OxmlElement("w:tcBorders")
        tc_pr.append(tc_borders)
    for edge in ("top", "left", "bottom", "right"):
        replace_border(tc_borders, edge)


def set_document_defaults(document):
    styles_element = document.styles.element
    doc_defaults = get_or_add(styles_element, "w:docDefaults")
    rpr_default = get_or_add(doc_defaults, "w:rPrDefault")
    rpr = get_or_add(rpr_default, "w:rPr")
    set_times_new_roman_rpr(rpr, size_pt=BODY_SIZE_PT)


def ensure_table_grid_style(document):
    try:
        table_grid = document.styles["Table Grid"]
    except KeyError:
        return
    tbl_pr = get_or_add(table_grid._element, "w:tblPr")
    tbl_borders = get_or_add(tbl_pr, "w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        replace_border(tbl_borders, edge)


def normalize_paragraphs(document):
    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        style_name = heading_style_for_text(text)

        if style_name and (is_heading_style(paragraph) or style_name == "TOC Title"):
            paragraph.style = style_name
        elif index == 0 and is_heading_style(paragraph):
            paragraph.style = "Title"
        elif text.lower().startswith("hình "):
            restyle_caption(paragraph)
        elif paragraph_has_drawing(paragraph):
            paragraph.style = "Figure"
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        paragraph.paragraph_format.space_before = Pt(SPACING_BEFORE_PT)
        paragraph.paragraph_format.space_after = Pt(SPACING_AFTER_PT)
        paragraph.paragraph_format.line_spacing = LINE_SPACING
        apply_direct_run_format(paragraph)


def normalize_tables(document):
    ensure_table_grid_style(document)
    for table in document.tables:
        set_table_all_borders(table)
        for row in table.rows:
            for cell in row.cells:
                set_cell_all_borders(cell)
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.space_before = Pt(SPACING_BEFORE_PT)
                    paragraph.paragraph_format.space_after = Pt(SPACING_AFTER_PT)
                    paragraph.paragraph_format.line_spacing = LINE_SPACING
                    for run in paragraph.runs:
                        set_run_font(run)


def prepare_document(docx_path):
    document = Document(docx_path)
    ensure_styles(document)
    normalize_paragraphs(document)
    normalize_tables(document)
    document.save(docx_path)


def main():
    parser = argparse.ArgumentParser(description="Apply LVTN DOCX formatting after Pandoc export.")
    parser.add_argument("docx_path")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help=argparse.SUPPRESS)
    args = parser.parse_args()

    prepare_document(args.docx_path)


if __name__ == "__main__":
    main()
