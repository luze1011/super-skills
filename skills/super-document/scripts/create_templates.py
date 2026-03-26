#!/usr/bin/env python3
"""创建模板文件"""

import zipfile
import os
import shutil
from pathlib import Path

def create_docx_template(output_path: str):
    """创建 Word 模板"""
    temp_dir = Path(output_path).parent / "temp_docx"
    temp_dir.mkdir(exist_ok=True)
    
    # [Content_Types].xml
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''
    
    # _rels/.rels
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    
    # word/_rels/document.xml.rels
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    
    # word/document.xml
    document = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
<w:p>
<w:pPr><w:jc w:val="center"/></w:pPr>
<w:r><w:rPr><w:b/><w:sz w:val="48"/></w:rPr><w:t>文档模板</w:t></w:r>
</w:p>
<w:p>
<w:pPr><w:jc w:val="right"/></w:pPr>
<w:r><w:t>日期: {{date}}</w:t></w:r>
</w:p>
<w:p><w:r><w:t>{{content}}</w:t></w:r></w:p>
</w:body>
</w:document>'''
    
    # word/styles.xml
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'''
    
    # 写入文件
    (temp_dir / "[Content_Types].xml").write_text(content_types, encoding="utf-8")
    
    (temp_dir / "_rels").mkdir(exist_ok=True)
    (temp_dir / "_rels" / ".rels").write_text(rels, encoding="utf-8")
    
    (temp_dir / "word").mkdir(exist_ok=True)
    (temp_dir / "word" / "document.xml").write_text(document, encoding="utf-8")
    (temp_dir / "word" / "styles.xml").write_text(styles, encoding="utf-8")
    
    (temp_dir / "word" / "_rels").mkdir(exist_ok=True)
    (temp_dir / "word" / "_rels" / "document.xml.rels").write_text(doc_rels, encoding="utf-8")
    
    # 创建 ZIP
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in temp_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(temp_dir)
                zf.write(file, arcname)
    
    # 清理
    shutil.rmtree(temp_dir)
    print(f"Word template created: {output_path}")


def create_xlsx_template(output_path: str):
    """创建 Excel 模板"""
    temp_dir = Path(output_path).parent / "temp_xlsx"
    temp_dir.mkdir(exist_ok=True)
    
    # [Content_Types].xml
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>'''
    
    # _rels/.rels
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''
    
    # xl/_rels/workbook.xml.rels
    wb_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    
    # xl/workbook.xml
    workbook = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheets>
<sheet name="Sheet1" sheetId="1" r:id="rId1" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
</sheets>
</workbook>'''
    
    # xl/worksheets/sheet1.xml
    sheet1 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>
<row r="1">
<c r="A1" t="str"><v>ID</v></c>
<c r="B1" t="str"><v>名称</v></c>
<c r="C1" t="str"><v>数量</v></c>
<c r="D1" t="str"><v>金额</v></c>
<c r="E1" t="str"><v>备注</v></c>
</row>
<row r="2">
<c r="A2" t="str"><v>{{id}}</v></c>
<c r="B2" t="str"><v>{{name}}</v></c>
<c r="C2" t="str"><v>{{quantity}}</v></c>
<c r="D2" t="str"><v>{{amount}}</v></c>
<c r="E2" t="str"><v>{{remark}}</v></c>
</row>
</sheetData>
</worksheet>'''
    
    # xl/styles.xml
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="1">
<font><sz val="11"/><name val="Calibri"/></font>
</fonts>
<fills count="1">
<fill><patternFill patternType="none"/></fill>
</fills>
<borders count="1">
<border/>
</borders>
<cellStyleXfs count="1">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
</cellStyleXfs>
<cellXfs count="1">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
</cellXfs>
</styleSheet>'''
    
    # 写入文件
    (temp_dir / "[Content_Types].xml").write_text(content_types, encoding="utf-8")
    
    (temp_dir / "_rels").mkdir(exist_ok=True)
    (temp_dir / "_rels" / ".rels").write_text(rels, encoding="utf-8")
    
    (temp_dir / "xl").mkdir(exist_ok=True)
    (temp_dir / "xl" / "workbook.xml").write_text(workbook, encoding="utf-8")
    (temp_dir / "xl" / "styles.xml").write_text(styles, encoding="utf-8")
    
    (temp_dir / "xl" / "_rels").mkdir(exist_ok=True)
    (temp_dir / "xl" / "_rels" / "workbook.xml.rels").write_text(wb_rels, encoding="utf-8")
    
    (temp_dir / "xl" / "worksheets").mkdir(exist_ok=True)
    (temp_dir / "xl" / "worksheets" / "sheet1.xml").write_text(sheet1, encoding="utf-8")
    
    # 创建 ZIP
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in temp_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(temp_dir)
                zf.write(file, arcname)
    
    # 清理
    shutil.rmtree(temp_dir)
    print(f"Excel template created: {output_path}")


if __name__ == "__main__":
    assets_dir = Path(__file__).parent.parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    create_docx_template(assets_dir / "docx-template.docx")
    create_xlsx_template(assets_dir / "xlsx-template.xlsx")