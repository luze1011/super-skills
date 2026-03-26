# Word 文档处理指南

## 工具选择

| 任务 | 推荐工具 | 说明 |
|------|---------|------|
| 创建新文档 | `python-docx` 或 `docx` (JS) | 功能完善，易于使用 |
| 读取内容 | `pandoc` | 转换为 Markdown 最方便 |
| 编辑现有文档 | 解包 → 编辑 XML → 打包 | 最灵活的方式 |
| 格式转换 | `pandoc` 或 LibreOffice | 支持多种格式 |

## 安装

```bash
# Python
pip install python-docx

# Node.js
npm install docx

# 命令行工具
# macOS: brew install pandoc
# Windows: choco install pandoc
# Linux: sudo apt install pandoc
```

## 创建文档

### python-docx（Python）

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 创建文档
doc = Document()

# 标题
doc.add_heading("文档标题", level=1)

# 段落
para = doc.add_paragraph("这是正文内容。")
para.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 加粗/斜体
run = para.add_run("这是加粗文本。")
run.bold = True

# 添加图片
doc.add_picture("image.png", width=Inches(4))

# 添加表格
table = doc.add_table(rows=3, cols=3)
for i, row in enumerate(table.rows):
    for j, cell in enumerate(row.cells):
        cell.text = f"Cell {i},{j}"

# 保存
doc.save("output.docx")
```

### docx（Node.js）

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell } = require('docx');
const fs = require('fs');

const doc = new Document({
    sections: [{
        properties: {},
        children: [
            new Paragraph({
                children: [new TextRun({ text: "标题", bold: true, size: 32 })]
            }),
            new Paragraph({
                children: [new TextRun("正文内容")]
            }),
            new Table({
                rows: [
                    new TableRow({
                        children: [
                            new TableCell({ children: [new Paragraph("单元格1")] }),
                            new TableCell({ children: [new Paragraph("单元格2")] })
                        ]
                    })
                ]
            })
        ]
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync("output.docx", buffer);
});
```

## 读取文档

### pandoc（推荐）

```bash
# 转为 Markdown
pandoc document.docx -o output.md

# 保留修订痕迹
pandoc --track-changes=all document.docx -o output.md

# 提取图片
pandoc document.docx --extract-media=./images -o output.md
```

### python-docx

```python
from docx import Document

doc = Document("document.docx")

# 读取段落
for para in doc.paragraphs:
    print(para.text)

# 读取表格
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
```

## 编辑现有文档

### 三步流程

1. **解包 DOCX**

```bash
# DOCX 是 ZIP 文件
unzip document.docx -d unpacked/
```

2. **编辑 XML**

主要文件：
- `word/document.xml` - 文档内容
- `word/styles.xml` - 样式定义
- `word/numbering.xml` - 列表编号

```xml
<!-- document.xml 示例 -->
<w:p>
  <w:r>
    <w:t>段落文本</w:t>
  </w:r>
</w:p>
```

3. **重新打包**

```bash
cd unpacked/
zip -r ../output.docx *
```

### 添加修订

```xml
<!-- 插入内容 -->
<w:ins w:id="1" w:author="Claude" w:date="2026-03-26T00:00:00Z">
  <w:r>
    <w:t>新增文字</w:t>
  </w:r>
</w:ins>

<!-- 删除内容 -->
<w:del w:id="2" w:author="Claude" w:date="2026-03-26T00:00:00Z">
  <w:r>
    <w:delText>被删除的文字</w:delText>
  </w:r>
</w:del>
```

## 样式处理

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# 设置中文字体
def set_chinese_font(run, font_name="微软雅黑", size=11):
    run.font.size = Pt(size)
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)

doc = Document()
para = doc.add_paragraph()
run = para.add_run("中文文本")
set_chinese_font(run, "宋体", 14)
```

## 表格操作

```python
from docx import Document
from docx.shared import Inches
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# 创建表格
table = doc.add_table(rows=4, cols=3)
table.style = "Table Grid"
table.alignment = WD_TABLE_ALIGNMENT.CENTER

# 填充数据
headers = ["姓名", "年龄", "城市"]
data = [
    ["张三", "25", "北京"],
    ["李四", "30", "上海"],
    ["王五", "28", "广州"]
]

# 表头
for i, header in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = header
    # 设置加粗
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True

# 数据
for row_idx, row_data in enumerate(data):
    for col_idx, value in enumerate(row_data):
        table.rows[row_idx + 1].cells[col_idx].text = value

# 合并单元格
table.cell(1, 0).merge(table.cell(1, 1))
```

## 图片操作

```python
from docx import Document
from docx.shared import Inches

doc = Document()

# 添加图片
doc.add_picture("image.png", width=Inches(4))

# 图片对齐
last_paragraph = doc.paragraphs[-1]
last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 设置图片环绕（需要操作 XML）
from docx.oxml import OxmlElement

def set_image_wrap(paragraph, wrap_type="inline"):
    # wrap_type: inline, square, tight, through, top_and_bottom
    # 需要更复杂的 XML 操作
    pass
```

## 页眉页脚

```python
from docx import Document
from docx.shared import Pt

doc = Document()

# 页眉
header = doc.sections[0].header
header_para = header.paragraphs[0]
header_para.text = "页眉文本"

# 页脚
footer = doc.sections[0].footer
footer_para = footer.paragraphs[0]
footer_para.text = "页脚文本"

# 添加页码
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_page_number(paragraph):
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    
    instrText = OxmlElement('w:instrText')
    instrText.text = "PAGE"
    
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
```

## 目录

```python
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()

# 添加目录字段
paragraph = doc.add_paragraph()
run = paragraph.add_run()

fldChar = OxmlElement('w:fldChar')
fldChar.set(qn('w:fldCharType'), 'begin')
run._r.append(fldChar)

instrText = OxmlElement('w:instrText')
instrText.set(qn('xml:space'), 'preserve')
instrText.text = ' TOC \\o "1-3" \\h \\z \\u '
run._r.append(instrText)

fldChar2 = OxmlElement('w:fldChar')
fldChar2.set(qn('w:fldCharType'), 'separate')
run._r.append(fldChar2)

fldChar3 = OxmlElement('w:fldChar')
fldChar3.set(qn('w:fldCharType'), 'end')
run._r.append(fldChar3)
```

## 批注和修订

```python
from docx import Document
from docx.shared import RGBColor

doc = Document("document.docx")

# 添加批注（需要操作 XML）
# python-docx 不直接支持，需要使用更底层的方法

# 追踪修订
# Word 的修订追踪需要在 Word 中开启
# pandoc 可以保留修订痕迹：
# pandoc --track-changes=all document.docx -o output.md
```

## 格式转换

```bash
# DOCX → Markdown
pandoc document.docx -o output.md

# Markdown → DOCX
pandoc input.md -o output.docx

# DOCX → PDF
pandoc document.docx -o output.pdf

# DOCX → HTML
pandoc document.docx -o output.html

# 使用模板
pandoc input.md --reference-doc=template.docx -o output.docx
```

## 模板系统

```python
from docx import Document

def fill_template(template_path, output_path, replacements):
    """
    使用字典替换模板中的占位符
    
    模板中使用 {{placeholder}} 格式
    """
    doc = Document(template_path)
    
    # 替换段落中的占位符
    for para in doc.paragraphs:
        for key, value in replacements.items():
            placeholder = "{{" + key + "}}"
            if placeholder in para.text:
                para.text = para.text.replace(placeholder, value)
    
    # 替换表格中的占位符
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for key, value in replacements.items():
                        placeholder = "{{" + key + "}}"
                        if placeholder in para.text:
                            para.text = para.text.replace(placeholder, value)
    
    doc.save(output_path)

# 使用示例
fill_template(
    "template.docx",
    "output.docx",
    {
        "name": "张三",
        "date": "2026年3月26日",
        "title": "报告标题"
    }
)
```

## 常见问题

### 中文字体不生效

```python
# 需要同时设置 w:eastAsia
from docx.oxml.ns import qn

run.font.name = "宋体"
run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
```

### 表格样式不生效

```python
# 确保样式名称正确
table.style = "Table Grid"  # 不是 "TableGrid"
```

### 图片无法居中

```python
# 图片居中需要设置段落对齐
paragraph = doc.add_paragraph()
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = paragraph.add_run()
run.add_picture("image.png", width=Inches(4))
```

## 最佳实践

1. **创建文档** → 使用 `python-docx` 或 `docx` (JS)
2. **读取内容** → 使用 `pandoc` 转 Markdown
3. **批量处理** → 先解包，批量修改 XML，再打包
4. **模板填充** → 使用占位符替换
5. **格式转换** → `pandoc` 是最佳选择