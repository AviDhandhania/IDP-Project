"""
Converts Report-2 Markdown into Report-2-Crypto-Agility-Copilot.docx
using Report-1-Crypto-Agility-Copilot.docx as a template archive.
"""

import re
import os
import zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def make_run(text: str, bold=False, italic=False, code=False) -> str:
    """Generates a <w:r> element with formatting."""
    if not text:
        return ""
    rPr = []
    if bold:
        rPr.append("<w:b/>")
    if italic:
        rPr.append("<w:i/>")
    if code:
        rPr.append('<w:rStyle w:val="VerbatimChar"/><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>')
    rPr_str = f"<w:rPr>{''.join(rPr)}</w:rPr>" if rPr else ""
    escaped_text = escape(text)
    return f'<w:r>{rPr_str}<w:t xml:space="preserve">{escaped_text}</w:t></w:r>'


def parse_inline(text: str) -> str:
    """Parses basic markdown bold, italic, code spans into Word runs."""
    tokens = re.split(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)", text)
    runs = []
    for token in tokens:
        if not token:
            continue
        if token.startswith("`") and token.endswith("`") and len(token) >= 2:
            runs.append(make_run(token[1:-1], code=True))
        elif token.startswith("**") and token.endswith("**") and len(token) >= 4:
            runs.append(make_run(token[2:-2], bold=True))
        elif token.startswith("*") and token.endswith("*") and len(token) >= 2:
            runs.append(make_run(token[1:-1], italic=True))
        else:
            runs.append(make_run(token))
    return "".join(runs)


def make_p(content_runs: str, style: str = "BodyText", jc: str = None) -> str:
    """Creates a <w:p> paragraph with specified style."""
    pPr_items = [f'<w:pStyle w:val="{style}"/>']
    if jc:
        pPr_items.append(f'<w:jc w:val="{jc}"/>')
    pPr_str = f"<w:pPr>{''.join(pPr_items)}</w:pPr>"
    return f"<w:p>{pPr_str}{content_runs}</w:p>"


def make_table(rows: list) -> str:
    """Generates a WordprocessingML <w:tbl> table."""
    tbl_xml = [
        '<w:tbl>',
        '<w:tblPr>',
        '<w:tblStyle w:val="Table"/>',
        '<w:tblW w:type="pct" w:w="0.0"/>',
        '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="0" w:val="0020"/>',
        '</w:tblPr>'
    ]
    for row_idx, row in enumerate(rows):
        tbl_xml.append('<w:tr>')
        for cell in row:
            tbl_xml.append('<w:tc>')
            # Table cell paragraph
            runs = parse_inline(cell)
            if row_idx == 0:
                # Header row: bold
                runs = parse_inline(f"**{cell}**")
            tbl_xml.append(f'<w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr>{runs}</w:p>')
            tbl_xml.append('</w:tc>')
        tbl_xml.append('</w:tr>')
    tbl_xml.append('</w:tbl>')
    return "".join(tbl_xml)


def convert_md_to_docx_body(md_text: str) -> str:
    """Converts full Markdown string into body elements XML string."""
    lines = md_text.splitlines()
    body_elements = []

    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # 1. Code blocks
        if stripped.startswith("```"):
            if in_code_block:
                # End code block
                in_code_block = False
                for cl in code_lines:
                    body_elements.append(make_p(make_run(cl, code=True), style="SourceCode"))
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # 2. Tables
        if "|" in line:
            # Check if separator row (e.g. |---|---|)
            if re.match(r"^\|?\s*[-:]+[-| :]*$", stripped):
                continue
            # Parse table row
            cells = [c.strip() for c in stripped.split("|")]
            # Strip empty first/last if leading/trailing pipe
            if stripped.startswith("|") and len(cells) > 0 and cells[0] == "":
                cells = cells[1:]
            if stripped.endswith("|") and len(cells) > 0 and cells[-1] == "":
                cells = cells[:-1]
            if cells:
                in_table = True
                table_rows.append(cells)
                continue
        else:
            if in_table:
                body_elements.append(make_table(table_rows))
                in_table = False
                table_rows = []

        if not stripped:
            continue

        # 3. Horizontal rules
        if stripped in ["---", "***", "___"]:
            body_elements.append(make_p(make_run(" "), style="BodyText"))
            continue

        # 4. Headings
        if stripped.startswith("#### "):
            body_elements.append(make_p(parse_inline(stripped[5:]), style="Heading4"))
        elif stripped.startswith("### "):
            body_elements.append(make_p(parse_inline(stripped[4:]), style="Heading3"))
        elif stripped.startswith("## "):
            body_elements.append(make_p(parse_inline(stripped[3:]), style="Heading2"))
        elif stripped.startswith("# "):
            body_elements.append(make_p(parse_inline(stripped[2:]), style="Heading1"))
        # 5. Lists
        elif stripped.startswith("- ") or stripped.startswith("* "):
            body_elements.append(make_p(make_run("• ") + parse_inline(stripped[2:]), style="Compact"))
        elif re.match(r"^\d+\.\s+", stripped):
            m = re.match(r"^(\d+\.)\s+(.*)$", stripped)
            body_elements.append(make_p(make_run(m.group(1) + " ") + parse_inline(m.group(2)), style="Compact"))
        # 6. Regular paragraphs
        else:
            body_elements.append(make_p(parse_inline(stripped), style="BodyText"))

    if in_table and table_rows:
        body_elements.append(make_table(table_rows))

    # Add section properties
    body_elements.append('<w:sectPr/>')

    return "".join(body_elements)


def generate_docx(input_md: str, template_docx: str, output_docx: str):
    print(f"Reading markdown from {input_md}...")
    with open(input_md, "r", encoding="utf-8") as f:
        md_text = f.read()

    print("Converting markdown elements to WordprocessingML body...")
    body_xml_content = convert_md_to_docx_body(md_text)

    # Wrap in complete document.xml
    full_document_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<w:body>{body_xml_content}</w:body>'
        '</w:document>'
    )

    print(f"Packaging new DOCX from template {template_docx}...")
    with zipfile.ZipFile(template_docx, 'r') as zin:
        with zipfile.ZipFile(output_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/document.xml':
                    zout.writestr('word/document.xml', full_document_xml.encode('utf-8'))
                else:
                    zout.writestr(item, zin.read(item.filename))

    file_size = os.path.getsize(output_docx)
    print(f"✅ Successfully created {output_docx} ({file_size:,} bytes).")


if __name__ == "__main__":
    import sys
    md_file = sys.argv[1] if len(sys.argv) > 1 else "Report-2-Crypto-Agility-Copilot.md"
    template_file = sys.argv[2] if len(sys.argv) > 2 else "Report-1-Crypto-Agility-Copilot.docx"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "Report-2-Crypto-Agility-Copilot.docx"
    generate_docx(md_file, template_file, output_file)
