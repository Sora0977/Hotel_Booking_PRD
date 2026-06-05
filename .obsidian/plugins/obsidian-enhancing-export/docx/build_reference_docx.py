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


def set_run_font(run, size_pt, bold=False, italic=False, underline=False, all_caps=False):
    run.font.name = FONT_NAME
    run.font.size = Pt(size_pt)
    run.font.color.rgb = BLACK
    run.font.bold = bold
    run.font.italic = italic
    run.font.underline = underline
    run.font.all_caps = all_caps
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = rpr._add_rFonts()
    for key in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(f"{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{key}", FONT_NAME)
    set_times_new_roman_rpr(rpr, size_pt=size_pt)


def configure_paragraph_format(style, size_pt, bold=False, italic=False, underline=False, all_caps=False, alignment=None):
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


def set_table_grid_borders(document):
    table_grid = document.styles["Table Grid"]
    tbl_pr = get_or_add(table_grid._element, "w:tblPr")
    tbl_borders = get_or_add(tbl_pr, "w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        replace_border(tbl_borders, edge)


def set_document_defaults(document):
    styles_element = document.styles.element
    doc_defaults = get_or_add(styles_element, "w:docDefaults")
    rpr_default = get_or_add(doc_defaults, "w:rPrDefault")
    rpr = get_or_add(rpr_default, "w:rPr")
    set_times_new_roman_rpr(rpr, size_pt=BODY_SIZE_PT)


def get_or_add_style(document, name, style_type=WD_STYLE_TYPE.PARAGRAPH):
    try:
        return document.styles[name]
    except KeyError:
        return document.styles.add_style(name, style_type)


def build_reference_docx(output_path):
    document = Document()

    configure_paragraph_format(document.styles["Normal"], BODY_SIZE_PT)
    configure_paragraph_format(document.styles["Body Text"], BODY_SIZE_PT)
    configure_paragraph_format(document.styles["Title"], 18, bold=True, all_caps=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    configure_paragraph_format(document.styles["Heading 1"], 24, bold=True, all_caps=True, alignment=WD_ALIGN_PARAGRAPH.RIGHT)
    configure_paragraph_format(document.styles["Heading 2"], 15, bold=True, all_caps=True)
    configure_paragraph_format(document.styles["Heading 3"], 14, bold=True)
    configure_paragraph_format(document.styles["Heading 4"], 13, underline=True)
    configure_paragraph_format(document.styles["Heading 5"], 13, bold=False)
    configure_paragraph_format(document.styles["Caption"], 13, bold=True, underline=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)

    toc_title = get_or_add_style(document, "TOC Title")
    configure_paragraph_format(toc_title, 18, bold=True, all_caps=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)

    figure_style = get_or_add_style(document, "Figure")
    configure_paragraph_format(figure_style, BODY_SIZE_PT, alignment=WD_ALIGN_PARAGRAPH.CENTER)

    for style_name in ("Header", "Footer"):
        configure_paragraph_format(document.styles[style_name], BODY_SIZE_PT, italic=True)

    set_document_defaults(document)
    set_table_grid_borders(document)

    document.add_paragraph("Reference DOCX for Obsidian Enhancing Export.", style="Normal")
    sample_table = document.add_table(rows=1, cols=1)
    sample_table.style = "Table Grid"
    sample_table.cell(0, 0).text = "Table Grid"
    document.save(output_path)


if __name__ == "__main__":
    build_reference_docx("reference.docx")
