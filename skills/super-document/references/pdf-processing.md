# PDF 处理参考指南

## 库对比

| 库 | 优势 | 劣势 | 适用场景 |
|----|------|------|---------|
| pypdf | 纯 Python，无需外部依赖 | 文本提取质量一般 | 合并/拆分/加密 |
| pdfplumber | 文本/表格提取质量高 | 内存占用较大 | 提取文本和表格 |
| PyMuPDF (fitz) | 速度快，功能全面 | 文档较少 | 复杂 PDF 操作 |
| reportlab | 创建 PDF 功能强大 | 只能创建，不能修改 | 生成 PDF 报告 |
| pdf2image | 图片转换质量高 | 需要安装 poppler | PDF 转图片 |

## 安装

```bash
# Python 库
pip install pypdf pdfplumber reportlab PyMuPDF pdf2image

# 系统工具
# macOS
brew install poppler qpdf

# Windows
choco install poppler qpdf

# Linux
sudo apt install poppler-utils qpdf
```

## 文本提取

### pdfplumber（推荐）

```python
import pdfplumber

# 基础提取
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)

# 保留布局
with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text(layout=True)

# 指定区域
with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]
    # 只提取上半部分
    top_half = page.crop((0, 0, page.width, page.height / 2))
    text = top_half.extract_text()
```

### pypdf

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"
```

### PyMuPDF

```python
import fitz  # PyMuPDF

doc = fitz.open("document.pdf")
for page in doc:
    text = page.get_text()
    print(text)
```

## 表格提取

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("report.pdf") as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    
    for i, table in enumerate(tables):
        # table 是二维数组，第一行通常是表头
        if len(table) > 1:
            df = pd.DataFrame(table[1:], columns=table[0])
            df.to_excel(f"table_{i}.xlsx", index=False)
```

## 图片提取

### 使用 PyMuPDF

```python
import fitz

doc = fitz.open("document.pdf")
for page_num, page in enumerate(doc):
    images = page.get_images()
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        
        with open(f"page{page_num}_img{img_index}.png", "wb") as f:
            f.write(image_bytes)
```

### 使用命令行

```bash
# pdfimages（poppler-utils）
pdfimages -j document.pdf output_prefix

# 输出：output_prefix-000.jpg, output_prefix-001.jpg, ...
```

## 合并与拆分

### 合并

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
files = ["part1.pdf", "part2.pdf", "part3.pdf"]

for file in files:
    reader = PdfReader(file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as f:
    writer.write(f)
```

```bash
# 命令行
qpdf --empty --pages part1.pdf part2.pdf part3.pdf -- merged.pdf
```

### 拆分

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")

# 按页拆分
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        writer.write(f)

# 按范围拆分
writer1 = PdfWriter()
for i in range(0, 5):  # 第 1-5 页
    writer1.add_page(reader.pages[i])
with open("part1.pdf", "wb") as f:
    writer1.write(f)
```

```bash
# 命令行
qpdf input.pdf --pages . 1-5 -- part1.pdf
qpdf input.pdf --pages . 6-10 -- part2.pdf
```

## 加密与解密

### 加密

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# 设置密码
writer.encrypt(
    user_password="user123",    # 打开密码
    owner_password="owner123",  # 权限密码
    permissions=0b0100          # 只允许打印
)

with open("encrypted.pdf", "wb") as f:
    writer.write(f)
```

### 解密

```python
from pypdf import PdfReader

reader = PdfReader("encrypted.pdf")

if reader.is_encrypted:
    reader.decrypt("password")

for page in reader.pages:
    print(page.extract_text())
```

## 水印

```python
from pypdf import PdfReader, PdfWriter

# 创建水印 PDF（或使用现有水印）
watermark = PdfReader("watermark.pdf").pages[0]

reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as f:
    writer.write(f)
```

## OCR

```python
import pytesseract
from pdf2image import convert_from_path

# 转换为图片
images = convert_from_path("scanned.pdf")

# OCR
for i, image in enumerate(images):
    text = pytesseract.image_to_string(
        image,
        lang="chi_sim+eng"  # 中英文
    )
    print(f"--- Page {i+1} ---")
    print(text)
```

## 创建 PDF

### reportlab

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table

doc = SimpleDocTemplate("output.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

# 标题
story.append(Paragraph("报告标题", styles["Title"]))
story.append(Spacer(1, 12))

# 正文
story.append(Paragraph("这是一段正文内容。", styles["Normal"]))
story.append(Spacer(1, 12))

# 表格
data = [
    ["姓名", "年龄", "城市"],
    ["张三", "25", "北京"],
    ["李四", "30", "上海"]
]
table = Table(data)
story.append(table)

doc.build(story)
```

## PDF 转图片

```python
from pdf2image import convert_from_path

# 转换所有页
images = convert_from_path("document.pdf", dpi=300)

for i, image in enumerate(images):
    image.save(f"page_{i+1}.png", "PNG")

# 转换指定页
images = convert_from_path("document.pdf", first_page=1, last_page=5)
```

## 常见问题

### 中文乱码

```python
# pdfplumber 通常能正确处理中文
import pdfplumber

with pdfplumber.open("chinese.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    print(text)  # 通常正常显示
```

### 提取质量差

```python
# 1. 使用 layout 模式
text = page.extract_text(layout=True)

# 2. 使用 PyMuPDF
import fitz
doc = fitz.open("document.pdf")
text = doc[0].get_text()

# 3. OCR 扫描件
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf")
text = pytesseract.image_to_string(images[0], lang="chi_sim+eng")
```

### 加密 PDF 解密失败

```python
# 尝试 qpdf 解密
# qpdf --password=xxx --decrypt input.pdf output.pdf

import subprocess
subprocess.run(["qpdf", "--password=xxx", "--decrypt", 
                "input.pdf", "output.pdf"])
```

## 性能优化

```python
# 大文件流式处理
import pdfplumber

# 不要一次性打开所有页
with pdfplumber.open("large.pdf") as pdf:
    for page in pdf.pages:
        # 逐页处理
        text = page.extract_text()
        # 处理后立即释放
        page.flush_cache()
```

## 最佳实践

1. **文本提取** → 优先使用 `pdfplumber`
2. **合并/拆分** → 优先使用 `qpdf` 命令行
3. **表格提取** → `pdfplumber` + `pandas`
4. **扫描件** → `pdf2image` + `pytesseract`
5. **创建 PDF** → `reportlab` 或直接转 Markdown 用 pandoc