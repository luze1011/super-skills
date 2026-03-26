---
name: super-document
description: "统一文档处理技能 - 一站式处理 PDF、Word、Excel、PowerPoint 和 Markdown 格式转换。当用户需要：读取/创建/编辑 Office 文档、PDF 操作（提取/合并/拆分/OCR）、表格数据处理、演示文稿制作、格式转换时使用。支持 Python 库和命令行工具。"
---

# 超级文档处理技能

## 概述

统一处理五大文档格式的完整解决方案：
- 📄 **PDF** - 文本/表格/图片提取、合并/拆分/加密、OCR
- 📝 **Word** - 创建/读取/编辑 DOCX、模板操作、格式化
- 📊 **Excel** - 创建/读取 XLSX、公式处理、数据分析
- 🎯 **PowerPoint** - 创建/编辑 PPTX、模板使用、幻灯片操作
- 📋 **Markdown** - 格式转换、HTML/Markdown 互转

---

## 快速决策表

| 用户需求 | 推荐工具 | 章节 |
|---------|---------|------|
| 读取 PDF 内容 | `pdfplumber` / `markitdown` | [PDF 处理](#pdf-处理) |
| 合并/拆分 PDF | `pypdf` / `qpdf` | [PDF 处理](#pdf-处理) |
| 创建 Word 文档 | `docx-js` (Node.js) | [Word 文档](#word-文档) |
| 编辑现有 Word | 解包 → 编辑 XML → 打包 | [Word 文档](#word-文档) |
| 创建 Excel | `openpyxl` (Python) | [Excel 表格](#excel-表格) |
| 分析 Excel 数据 | `pandas` (Python) | [Excel 表格](#excel-表格) |
| 创建演示文稿 | `pptxgenjs` (Node.js) | [PowerPoint](#powerpoint) |
| 编辑演示文稿 | 解包 → 编辑 XML → 打包 | [PowerPoint](#powerpoint) |
| 文档转 Markdown | `markitdown` (CLI) | [Markdown 转换](#markdown-转换) |
| Markdown 转 Word | `pandoc` | [Markdown 转换](#markdown-转换) |

---

# PDF 处理

## Python 库速查

| 库 | 用途 | 安装 |
|----|------|------|
| `pypdf` | 合并/拆分/旋转/加密 | `pip install pypdf` |
| `pdfplumber` | 文本/表格提取 | `pip install pdfplumber` |
| `reportlab` | 创建 PDF | `pip install reportlab` |
| `pytesseract` | OCR 扫描件 | `pip install pytesseract pdf2image` |

## 常用操作

### 1. 读取 PDF

```python
# 方法一：pdfplumber（推荐）
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

```python
# 方法二：pypdf（基础）
from pypdf import PdfReader

reader = PdfReader("document.pdf")
for page in reader.pages:
    print(page.extract_text())
```

```bash
# 方法三：命令行（最快）
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt  # 保留排版
```

### 2. 提取表格

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("report.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            df.to_excel("output.xlsx", index=False)
```

### 3. 合并 PDF

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for file in ["part1.pdf", "part2.pdf", "part3.pdf"]:
    reader = PdfReader(file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as f:
    writer.write(f)
```

```bash
# 命令行方式
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
```

### 4. 拆分 PDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")

# 按页拆分
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        writer.write(f)
```

```bash
# 命令行方式
qpdf input.pdf --pages . 1-5 -- part1.pdf
qpdf input.pdf --pages . 6-10 -- part2.pdf
```

### 5. 提取图片

```bash
# 使用 pdfimages（poppler-utils）
pdfimages -j input.pdf output_prefix
# 生成 output_prefix-000.jpg, output_prefix-001.jpg, ...
```

### 6. OCR 扫描件

```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
for i, image in enumerate(images):
    text = pytesseract.image_to_string(image, lang='chi_sim+eng')
    print(f"--- Page {i+1} ---\n{text}")
```

### 7. 加密 PDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt("user_password", "owner_password")

with open("encrypted.pdf", "wb") as f:
    writer.write(f)
```

### 8. 添加水印

```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as f:
    writer.write(f)
```

### 9. 创建 PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

c.drawString(100, height - 100, "Hello World!")
c.save()
```

---

# Word 文档

## 工具选择

| 任务 | 工具 |
|------|------|
| 创建新文档 | `docx-js` (Node.js) |
| 读取内容 | `pandoc` 或解包查看 XML |
| 编辑现有文档 | 解包 → 编辑 XML → 打包 |
| 转换格式 | `pandoc` 或 LibreOffice |

## 创建 Word 文档

### 安装

```bash
npm install -g docx
```

### 基础示例

```javascript
const { Document, Packer, Paragraph, TextRun } = require('docx');
const fs = require('fs');

const doc = new Document({
    sections: [{
        properties: {
            page: {
                size: { width: 12240, height: 15840 }, // US Letter
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        children: [
            new Paragraph({
                children: [new TextRun({ text: "标题", bold: true, size: 32 })]
            }),
            new Paragraph({
                children: [new TextRun("正文内容")]
            })
        ]
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync("document.docx", buffer);
});
```

### 添加表格

```javascript
const { Table, TableRow, TableCell, BorderStyle, WidthType } = require('docx');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [4680, 4680],
    rows: [
        new TableRow({
            children: [
                new TableCell({
                    borders,
                    width: { size: 4680, type: WidthType.DXA },
                    children: [new Paragraph("单元格1")]
                }),
                new TableCell({
                    borders,
                    width: { size: 4680, type: WidthType.DXA },
                    children: [new Paragraph("单元格2")]
                })
            ]
        })
    ]
})
```

### 添加图片

```javascript
const { ImageRun } = require('docx');

new Paragraph({
    children: [new ImageRun({
        type: "png",
        data: fs.readFileSync("image.png"),
        transformation: { width: 200, height: 150 }
    })]
})
```

## 读取 Word 文档

```bash
# 转为 Markdown
pandoc document.docx -o output.md

# 带修订痕迹
pandoc --track-changes=all document.docx -o output.md
```

## 编辑现有 Word 文档

### 三步流程

1. **解包**
```bash
python scripts/office/unpack.py document.docx unpacked/
```

2. **编辑 XML**（在 `unpacked/word/document.xml` 中修改）

3. **打包**
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

### 添加修订

```xml
<!-- 插入内容 -->
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>新增文字</w:t></w:r>
</w:ins>

<!-- 删除内容 -->
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>被删除的文字</w:delText></w:r>
</w:del>
```

---

# Excel 表格

## 库选择

| 库 | 用途 | 安装 |
|----|------|------|
| `openpyxl` | 格式化、公式、复杂操作 | `pip install openpyxl` |
| `pandas` | 数据分析、批量处理 | `pip install pandas openpyxl` |

## 创建 Excel

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active
sheet.title = "数据表"

# 设置表头
headers = ["姓名", "年龄", "城市"]
for col, header in enumerate(headers, 1):
    cell = sheet.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor="D5E8F0")

# 添加数据
data = [
    ["张三", 25, "北京"],
    ["李四", 30, "上海"],
    ["王五", 28, "广州"]
]
for row_idx, row_data in enumerate(data, 2):
    for col_idx, value in enumerate(row_data, 1):
        sheet.cell(row=row_idx, column=col_idx, value=value)

# 添加公式
sheet['D1'] = "备注"
sheet['D2'] = '=CONCAT(A2, "住在", C2)'

# 设置列宽
sheet.column_dimensions['A'].width = 15
sheet.column_dimensions['B'].width = 10
sheet.column_dimensions['C'].width = 15

wb.save("output.xlsx")
```

## 读取 Excel

```python
# 方法一：pandas（推荐）
import pandas as pd

df = pd.read_excel('data.xlsx')
print(df.head())
print(df.describe())

# 方法二：openpyxl
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
sheet = wb.active
for row in sheet.iter_rows(values_only=True):
    print(row)
```

## 公式处理

```python
from openpyxl import Workbook

wb = Workbook()
sheet = wb.active

# 数据
sheet['A1'] = 10
sheet['A2'] = 20
sheet['A3'] = 30

# 公式
sheet['B1'] = '=SUM(A1:A3)'      # 求和
sheet['B2'] = '=AVERAGE(A1:A3)'  # 平均值
sheet['B3'] = '=MAX(A1:A3)'      # 最大值
sheet['B4'] = '=IF(A1>15, "大", "小")'  # 条件

wb.save("formulas.xlsx")

# 重新计算公式值
# python scripts/recalc.py formulas.xlsx
```

## 格式化

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# 字体
bold_font = Font(bold=True, color="0000FF")

# 填充
yellow_fill = PatternFill("solid", fgColor="FFFF00")

# 对齐
center_align = Alignment(horizontal="center", vertical="center")

# 边框
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# 应用
sheet['A1'].font = bold_font
sheet['A1'].fill = yellow_fill
sheet['A1'].alignment = center_align
sheet['A1'].border = thin_border
```

## 数据分析

```python
import pandas as pd

df = pd.read_excel('sales.xlsx')

# 筛选
high_sales = df[df['销售额'] > 10000]

# 分组统计
summary = df.groupby('地区').agg({
    '销售额': ['sum', 'mean', 'count']
})

# 导出
summary.to_excel('summary.xlsx')
```

---

# PowerPoint

## 工具选择

| 任务 | 工具 |
|------|------|
| 创建演示文稿 | `pptxgenjs` (Node.js) |
| 读取内容 | `markitdown` |
| 编辑现有演示文稿 | 解包 → 编辑 XML → 打包 |

## 创建演示文稿

### 安装

```bash
npm install -g pptxgenjs
```

### 基础示例

```javascript
const PptxGenJS = require('pptxgenjs');
const pptx = new PptxGenJS();

// 设置主题
pptx.layout = 'LAYOUT_16x9';
pptx.title = '演示文稿标题';

// 幻灯片 1 - 标题页
let slide1 = pptx.addSlide();
slide1.addText('演示文稿标题', {
    x: 0.5, y: 2, w: 9, h: 1,
    fontSize: 44, bold: true, align: 'center'
});
slide1.addText('副标题', {
    x: 0.5, y: 3.5, w: 9, h: 0.5,
    fontSize: 24, align: 'center'
});

// 幻灯片 2 - 内容页
let slide2 = pptx.addSlide();
slide2.addText('章节标题', {
    x: 0.5, y: 0.5, w: 9, h: 0.8,
    fontSize: 32, bold: true
});
slide2.addText([
    { text: '要点一\n', options: { bullet: true } },
    { text: '要点二\n', options: { bullet: true } },
    { text: '要点三', options: { bullet: true } }
], {
    x: 0.5, y: 1.5, w: 9, h: 4,
    fontSize: 20
});

// 保存
pptx.writeFile('presentation.pptx');
```

### 添加图片

```javascript
slide.addImage({
    path: 'image.png',
    x: 1, y: 1, w: 4, h: 3
});
```

### 添加表格

```javascript
slide.addTable([
    [{ text: 'Header 1', options: { bold: true } }, 'Header 2'],
    ['Row 1, Col 1', 'Row 1, Col 2'],
    ['Row 2, Col 1', 'Row 2, Col 2']
], {
    x: 0.5, y: 1, w: 9, h: 3,
    border: { pt: 1, color: '000000' }
});
```

### 添加图表

```javascript
slide.addChart(pptx.charts.BAR, [
    {
        name: 'Series 1',
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        values: [13, 25, 36, 29]
    }
], {
    x: 1, y: 1, w: 8, h: 4
});
```

## 读取演示文稿

```bash
# 提取文本
python -m markitdown presentation.pptx

# 生成缩略图
python scripts/thumbnail.py presentation.pptx
```

## 编辑现有演示文稿

1. **解包**
```bash
python scripts/office/unpack.py presentation.pptx unpacked/
```

2. **编辑 XML**

3. **打包**
```bash
python scripts/office/pack.py unpacked/ output.pptx --original presentation.pptx
```

## 设计建议

### 配色方案

| 主题 | 主色 | 辅色 | 强调色 |
|------|------|------|--------|
| 商务蓝 | `1E2761` | `CADCFC` | `FFFFFF` |
| 森林绿 | `2C5F2D` | `97BC62` | `F5F5F5` |
| 活力橙 | `F96167` | `F9E795` | `2F3C7E` |
| 极简灰 | `36454F` | `F2F2F2` | `212121` |

### 字体规范

| 元素 | 大小 |
|------|------|
| 标题 | 36-44pt |
| 小标题 | 20-24pt |
| 正文 | 14-16pt |
| 注释 | 10-12pt |

---

# Markdown 转换

## 工具

| 工具 | 用途 |
|------|------|
| `markitdown` | 文档 → Markdown |
| `pandoc` | 通用格式转换 |

## 安装

```bash
# markitdown（无需安装，直接运行）
uvx markitdown --help

# pandoc
# macOS: brew install pandoc
# Windows: choco install pandoc
```

## 文档转 Markdown

```bash
# PDF
uvx markitdown document.pdf -o output.md

# Word
uvx markitdown report.docx > report.md

# Excel
uvx markitdown data.xlsx > data.md

# PowerPoint
uvx markitdown slides.pptx -o slides.md

# HTML
uvx markitdown webpage.html -o webpage.md

# 从标准输入
cat document.pdf | uvx markitdown -x .pdf > output.md
```

## Markdown 转其他格式

```bash
# 转 Word
pandoc input.md -o output.docx

# 转 PDF
pandoc input.md -o output.pdf

# 转 HTML
pandoc input.md -o output.html

# 转 PowerPoint
pandoc input.md -o output.pptx
```

## 高级选项

```bash
# 指定模板
pandoc input.md --reference-doc=template.docx -o output.docx

# 生成目录
pandoc input.md --toc -o output.pdf

# 使用 Azure Document Intelligence（提升 PDF 提取质量）
uvx markitdown scan.pdf -d -e "https://your-resource.cognitiveservices.azure.com/"
```

---

# 命令速查表

## PDF

```bash
# 提取文本
pdftotext input.pdf output.txt

# 合并
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# 拆分
qpdf input.pdf --pages . 1-5 -- part1.pdf

# 提取图片
pdfimages -j input.pdf output_prefix

# 转 Markdown
uvx markitdown input.pdf -o output.md
```

## Word

```bash
# 读取
pandoc document.docx -o output.md

# 创建
node create-docx.js  # 使用 docx-js

# 编辑
python scripts/office/unpack.py document.docx unpacked/
# 编辑 XML
python scripts/office/pack.py unpacked/ output.docx

# 格式转换
pandoc input.md -o output.docx
```

## Excel

```bash
# 读取
python -c "import pandas as pd; print(pd.read_excel('data.xlsx'))"

# 公式重算
python scripts/recalc.py workbook.xlsx

# 转 Markdown
uvx markitdown data.xlsx > data.md
```

## PowerPoint

```bash
# 读取
python -m markitdown presentation.pptx

# 创建
node create-pptx.js  # 使用 pptxgenjs

# 缩略图
python scripts/thumbnail.py presentation.pptx

# 转 Markdown
uvx markitdown presentation.pptx -o slides.md
```

## Markdown

```bash
# 文档 → Markdown
uvx markitdown document.pdf -o output.md
uvx markitdown document.docx -o output.md
uvx markitdown document.xlsx -o output.md
uvx markitdown document.pptx -o output.md

# Markdown → 文档
pandoc input.md -o output.docx
pandoc input.md -o output.pdf
pandoc input.md -o output.pptx
```

---

# 常见问题

## PDF 中文乱码

```python
# 使用 pdfplumber 并指定编码
import pdfplumber

with pdfplumber.open("chinese.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

## Excel 公式不计算

```bash
# 使用 LibreOffice 重算
python scripts/recalc.py workbook.xlsx
```

## Word 修订痕迹丢失

```bash
# 使用 pandoc 保留修订
pandoc --track-changes=all document.docx -o output.md
```

## 演示文稿字体太小

- 标题使用 36-44pt
- 正文使用 14-16pt
- 最小不低于 12pt

## Markdown 转换图片丢失

```bash
# 使用 pandoc 提取图片
pandoc input.md --extract-media=./images -o output.docx
```

---

# 依赖安装

## Python

```bash
pip install pypdf pdfplumber reportlab pytesseract pdf2image
pip install openpyxl pandas
pip install "markitdown[pptx]" Pillow
```

## Node.js

```bash
npm install -g docx pptxgenjs
```

## 系统工具

```bash
# macOS
brew install poppler qpdf pandoc libreoffice tesseract

# Ubuntu/Debian
sudo apt install poppler-utils qpdf pandoc libreoffice tesseract-ocr

# Windows
choco install poppler qpdf pandoc libreoffice tesseract
```

---

# 最佳实践

## 1. 选择正确的工具

- **简单任务** → 命令行工具（pandoc、qpdf、pdftotext）
- **复杂操作** → Python 库（openpyxl、pdfplumber）
- **创建文档** → Node.js 库（docx-js、pptxgenjs）

## 2. 性能优化

- 大文件使用流式处理
- 批量操作减少 I/O
- 缓存常用模板

## 3. 错误处理

```python
try:
    with pdfplumber.open("document.pdf") as pdf:
        # 处理
except Exception as e:
    print(f"Error: {e}")
```

## 4. 编码规范

- 统一使用 UTF-8 编码
- 路径使用原始字符串或 Path 对象
- 异常情况提供友好提示

---

**技能版本**: 1.0.0  
**更新日期**: 2025-01-01  
**维护者**: 太子工作区