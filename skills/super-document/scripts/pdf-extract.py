#!/usr/bin/env python3
"""
PDF 提取工具
支持文本、表格、图片提取，以及合并/拆分 PDF
"""

import argparse
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("请安装 pdfplumber: pip install pdfplumber")
    sys.exit(1)

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("请安装 pypdf: pip install pypdf")
    sys.exit(1)


def extract_text(pdf_path: str, output_path: str = None, layout: bool = False):
    """提取 PDF 文本"""
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            if layout:
                text = page.extract_text(layout=True)
            else:
                text = page.extract_text()
            texts.append(f"--- Page {i} ---\n{text}\n")
    
    content = "\n".join(texts)
    if output_path:
        Path(output_path).write_text(content, encoding="utf-8")
        print(f"✓ 文本已保存到: {output_path}")
    else:
        print(content)
    return content


def extract_tables(pdf_path: str, output_path: str = None, format: str = "csv"):
    """提取 PDF 表格"""
    try:
        import pandas as pd
    except ImportError:
        print("请安装 pandas: pip install pandas")
        sys.exit(1)
    
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            for table_num, table in enumerate(tables, 1):
                if table and len(table) > 1:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df["_page"] = page_num
                    df["_table"] = table_num
                    all_tables.append(df)
    
    if not all_tables:
        print("未找到表格")
        return None
    
    result = pd.concat(all_tables, ignore_index=True)
    
    if output_path:
        if format == "xlsx" or output_path.endswith(".xlsx"):
            result.to_excel(output_path, index=False)
        else:
            result.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"✓ 表格已保存到: {output_path}")
    else:
        print(result.to_string())
    
    return result


def extract_images(pdf_path: str, output_dir: str):
    """提取 PDF 图片（需要 pdfimages 命令）"""
    import subprocess
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 使用 pdfimages 提取图片
    output_prefix = output_dir / "image"
    result = subprocess.run(
        ["pdfimages", "-j", pdf_path, str(output_prefix)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        images = list(output_dir.glob("image-*"))
        print(f"✓ 提取了 {len(images)} 张图片到: {output_dir}")
        return images
    else:
        print(f"提取失败: {result.stderr}")
        print("请确保已安装 poppler-utils (pdfimages)")
        return None


def merge_pdfs(pdf_files: list, output_path: str):
    """合并多个 PDF"""
    writer = PdfWriter()
    
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)
    
    with open(output_path, "wb") as f:
        writer.write(f)
    
    print(f"✓ 已合并 {len(pdf_files)} 个文件到: {output_path}")


def split_pdf(pdf_path: str, output_dir: str, pages: str = None):
    """拆分 PDF"""
    reader = PdfReader(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if pages:
        # 解析页面范围，如 "1-5,7,9-10"
        page_list = parse_page_range(pages, len(reader.pages))
        for i in page_list:
            writer = PdfWriter()
            writer.add_page(reader.pages[i - 1])  # 转为 0-indexed
            output_file = output_dir / f"page_{i}.pdf"
            with open(output_file, "wb") as f:
                writer.write(f)
        print(f"✓ 已拆分 {len(page_list)} 页到: {output_dir}")
    else:
        # 拆分所有页
        for i, page in enumerate(reader.pages, 1):
            writer = PdfWriter()
            writer.add_page(page)
            output_file = output_dir / f"page_{i}.pdf"
            with open(output_file, "wb") as f:
                writer.write(f)
        print(f"✓ 已拆分 {len(reader.pages)} 页到: {output_dir}")


def parse_page_range(pages: str, max_page: int) -> list:
    """解析页面范围字符串"""
    result = []
    for part in pages.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            result.extend(range(start, min(end + 1, max_page + 1)))
        else:
            page = int(part)
            if 1 <= page <= max_page:
                result.append(page)
    return sorted(set(result))


def ocr_pdf(pdf_path: str, output_path: str = None, lang: str = "chi_sim+eng"):
    """OCR 扫描件 PDF"""
    try:
        import pytesseract
        from pdf2image import convert_from_path
    except ImportError:
        print("请安装: pip install pytesseract pdf2image")
        sys.exit(1)
    
    images = convert_from_path(pdf_path)
    texts = []
    
    for i, image in enumerate(images, 1):
        text = pytesseract.image_to_string(image, lang=lang)
        texts.append(f"--- Page {i} ---\n{text}\n")
    
    content = "\n".join(texts)
    
    if output_path:
        Path(output_path).write_text(content, encoding="utf-8")
        print(f"✓ OCR 结果已保存到: {output_path}")
    else:
        print(content)
    
    return content


def main():
    parser = argparse.ArgumentParser(description="PDF 提取工具")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 提取文本
    text_parser = subparsers.add_parser("text", help="提取文本")
    text_parser.add_argument("pdf", help="PDF 文件路径")
    text_parser.add_argument("-o", "--output", help="输出文件路径")
    text_parser.add_argument("--layout", action="store_true", help="保留布局")
    
    # 提取表格
    table_parser = subparsers.add_parser("tables", help="提取表格")
    table_parser.add_argument("pdf", help="PDF 文件路径")
    table_parser.add_argument("-o", "--output", help="输出文件路径")
    table_parser.add_argument("-f", "--format", choices=["csv", "xlsx"], default="csv")
    
    # 提取图片
    image_parser = subparsers.add_parser("images", help="提取图片")
    image_parser.add_argument("pdf", help="PDF 文件路径")
    image_parser.add_argument("-o", "--output", required=True, help="输出目录")
    
    # 合并 PDF
    merge_parser = subparsers.add_parser("merge", help="合并 PDF")
    merge_parser.add_argument("pdfs", nargs="+", help="PDF 文件列表")
    merge_parser.add_argument("-o", "--output", required=True, help="输出文件")
    
    # 拆分 PDF
    split_parser = subparsers.add_parser("split", help="拆分 PDF")
    split_parser.add_argument("pdf", help="PDF 文件路径")
    split_parser.add_argument("-o", "--output", required=True, help="输出目录")
    split_parser.add_argument("-p", "--pages", help="页面范围，如 '1-5,7,9-10'")
    
    # OCR
    ocr_parser = subparsers.add_parser("ocr", help="OCR 扫描件")
    ocr_parser.add_argument("pdf", help="PDF 文件路径")
    ocr_parser.add_argument("-o", "--output", help="输出文件路径")
    ocr_parser.add_argument("-l", "--lang", default="chi_sim+eng", help="OCR 语言")
    
    args = parser.parse_args()
    
    if args.command == "text":
        extract_text(args.pdf, args.output, args.layout)
    elif args.command == "tables":
        extract_tables(args.pdf, args.output, args.format)
    elif args.command == "images":
        extract_images(args.pdf, args.output)
    elif args.command == "merge":
        merge_pdfs(args.pdfs, args.output)
    elif args.command == "split":
        split_pdf(args.pdf, args.output, args.pages)
    elif args.command == "ocr":
        ocr_pdf(args.pdf, args.output, args.lang)


if __name__ == "__main__":
    main()