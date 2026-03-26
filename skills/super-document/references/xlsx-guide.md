# Excel 表格处理指南

## 库选择

| 库 | 优势 | 劣势 | 适用场景 |
|----|------|------|---------|
| openpyxl | 格式化、公式、完整功能 | 大文件性能差 | 创建格式化表格 |
| pandas | 数据分析强大 | 格式控制弱 | 数据处理分析 |
| xlsxwriter | 性能好，功能全 | 不能读取现有文件 | 创建大型表格 |
| xlrd/xlwt | 支持 .xls 格式 | 旧格式，功能少 | 处理旧版 Excel |

## 安装

```bash
pip install openpyxl pandas xlsxwriter
```

## 基础读写

### 读取

```python
import pandas as pd
from openpyxl import load_workbook

# pandas 方式（推荐用于数据分析）
df = pd.read_excel("data.xlsx")
print(df.head())

# 指定工作表
df = pd.read_excel("data.xlsx", sheet_name="Sheet2")

# 读取多个工作表
all_sheets = pd.read_excel("data.xlsx", sheet_name=None)
for name, df in all_sheets.items():
    print(f"Sheet: {name}")
    print(df.head())

# openpyxl 方式（用于读取格式/公式）
wb = load_workbook("data.xlsx")
ws = wb.active

# 读取单元格
value = ws['A1'].value
print(value)

# 遍历所有行
for row in ws.iter_rows(values_only=True):
    print(row)
```

### 写入

```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

# pandas 方式
df = pd.DataFrame({
    'Name': ['张三', '李四'],
    'Age': [25, 30]
})
df.to_excel("output.xlsx", index=False)

# openpyxl 方式
wb = Workbook()
ws = wb.active
ws['A1'] = "姓名"
ws['B1'] = "年龄"
ws['A2'] = "张三"
ws['B2'] = 25
wb.save("output.xlsx")
```

## 格式化

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active

# 字体
bold_font = Font(bold=True, size=14, color="FF0000")
ws['A1'].font = bold_font

# 填充
yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
ws['A1'].fill = yellow_fill

# 对齐
center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws['A1'].alignment = center_align

# 边框
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
ws['A1'].border = thin_border

# 行高/列宽
ws.row_dimensions[1].height = 30
ws.column_dimensions['A'].width = 20

# 条件格式
from openpyxl.formatting.rule import FormulaRule

red_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
ws.conditional_formatting.add('A2:A10', 
    FormulaRule(formula=['$A2<0'], fill=red_fill))

wb.save("formatted.xlsx")
```

## 公式

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# 数据
data = [
    ['项目', '数量', '单价', '金额'],
    ['苹果', 10, 5, '=B2*C2'],
    ['香蕉', 20, 3, '=B3*C3'],
    ['橙子', 15, 4, '=B4*C4'],
    ['合计', '=SUM(B2:B4)', '', '=SUM(D2:D4)']
]

for row in data:
    ws.append(row)

wb.save("formulas.xlsx")

# 注意：openpyxl 不会计算公式，只存储公式
# 如果需要获取计算结果：
# 1. 用 LibreOffice 重算：libreoffice --calc --convert-to xlsx formulas.xlsx
# 2. 用 pandas 读取 data_only=True
```

## 图表

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, LineChart, Reference

wb = Workbook()
ws = wb.active

# 数据
data = [
    ['月份', '销售额'],
    ['1月', 1000],
    ['2月', 1500],
    ['3月', 2000],
    ['4月', 1800],
]

for row in data:
    ws.append(row)

# 柱状图
chart = BarChart()
chart.title = "月度销售额"
chart.x_axis.title = "月份"
chart.y_axis.title = "销售额"

data = Reference(ws, min_col=2, min_row=1, max_row=5)
cats = Reference(ws, min_col=1, min_row=2, max_row=5)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

ws.add_chart(chart, "D2")

wb.save("chart.xlsx")
```

## 数据分析

```python
import pandas as pd

# 读取数据
df = pd.read_excel("sales.xlsx")

# 基础统计
print(df.describe())
print(df.info())

# 筛选
high_sales = df[df['销售额'] > 10000]
print(high_sales)

# 排序
sorted_df = df.sort_values('销售额', ascending=False)

# 分组统计
summary = df.groupby('地区').agg({
    '销售额': ['sum', 'mean', 'count']
})
print(summary)

# 数据透视表
pivot = pd.pivot_table(
    df, 
    values='销售额',
    index='地区',
    columns='产品',
    aggfunc='sum'
)
print(pivot)

# 导出
summary.to_excel("summary.xlsx")
```

## 多工作表操作

```python
from openpyxl import Workbook

wb = Workbook()

# 重命名默认工作表
ws1 = wb.active
ws1.title = "数据"

# 创建新工作表
ws2 = wb.create_sheet("分析")
ws3 = wb.create_sheet("汇总", 0)  # 插入到第一位

# 删除工作表
wb.remove(ws3)

# 复制工作表
ws_copy = wb.copy_worksheet(ws1)
ws_copy.title = "数据副本"

# 引用其他工作表
ws2['A1'] = "=数据!A1"

wb.save("multi_sheets.xlsx")
```

## 合并单元格

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# 合并单元格
ws.merge_cells('A1:C1')
ws['A1'] = "合并后的标题"

# 合并多行
ws.merge_cells('A3:B5')
ws['A3'] = "大单元格"

# 取消合并
# ws.unmerge_cells('A1:C1')

wb.save("merged.xlsx")
```

## 数据验证

```python
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
ws = wb.active

# 下拉列表
dv = DataValidation(type="list", formula1='"选项1,选项2,选项3"', allow_blank=True)
dv.error = "请从列表中选择"
dv.errorTitle = "输入错误"
ws.add_data_validation(dv)
dv.add('A1:A10')

# 数字范围
dv2 = DataValidation(type="whole", operator="between", formula1=0, formula2=100)
dv2.error = "请输入0-100之间的整数"
ws.add_data_validation(dv2)
dv2.add('B1:B10')

# 日期范围
dv3 = DataValidation(type="date", operator="greaterThan", formula1="2026-01-01")
ws.add_data_validation(dv3)
dv3.add('C1:C10')

wb.save("validation.xlsx")
```

## 批量处理

```python
import pandas as pd
from pathlib import Path

# 合并多个 Excel
files = list(Path(".").glob("*.xlsx"))
dfs = [pd.read_excel(f) for f in files]
merged = pd.concat(dfs, ignore_index=True)
merged.to_excel("merged.xlsx", index=False)

# 拆分 Excel
df = pd.read_excel("data.xlsx")
for region in df['地区'].unique():
    region_df = df[df['地区'] == region]
    region_df.to_excel(f"{region}.xlsx", index=False)

# 批量修改
from openpyxl import load_workbook

for file in Path(".").glob("*.xlsx"):
    wb = load_workbook(file)
    ws = wb.active
    ws['A1'] = "Modified"
    wb.save(file)
```

## 性能优化

```python
# 大文件处理
from openpyxl import load_workbook

# 只读模式
wb = load_workbook("large.xlsx", read_only=True)
ws = wb.active
for row in ws.iter_rows(values_only=True):
    # 处理行
    pass
wb.close()

# 只写模式
from openpyxl import Workbook

wb = Workbook(write_only=True)
ws = wb.create_sheet()
for i in range(100000):
    ws.append([i, f"Item {i}"])
wb.save("large_output.xlsx")

# 使用 xlsxwriter 提高写入性能
import xlsxwriter

wb = xlsxwriter.Workbook('fast.xlsx')
ws = wb.add_worksheet()
for i in range(100000):
    ws.write_row(i, 0, [i, f"Item {i}"])
wb.close()
```

## 与数据库交互

```python
import pandas as pd
import sqlite3

# Excel → 数据库
df = pd.read_excel("data.xlsx")
conn = sqlite3.connect("data.db")
df.to_sql("mytable", conn, if_exists="replace", index=False)

# 数据库 → Excel
df = pd.read_sql("SELECT * FROM mytable", conn)
df.to_excel("from_db.xlsx", index=False)

conn.close()
```

## 常见问题

### 公式不计算

```python
# openpyxl 不会自动计算公式
# 解决方法：
# 1. 用 Excel 打开后保存
# 2. 用 LibreOffice 重算
import subprocess
subprocess.run(["libreoffice", "--calc", "--convert-to", "xlsx", "file.xlsx"])
```

### 大文件内存溢出

```python
# 使用 read_only 和 write_only 模式
wb = load_workbook("large.xlsx", read_only=True)
# 或使用 pandas 分块读取
for chunk in pd.read_excel("large.xlsx", chunksize=10000):
    process(chunk)
```

### 日期格式问题

```python
import pandas as pd

# 读取时指定日期列
df = pd.read_excel("data.xlsx", parse_dates=['日期'])

# 写入时指定日期格式
from openpyxl.styles import numbers
ws['A1'].number_format = 'YYYY-MM-DD'
```

### 中文乱码

```python
# 使用 utf-8-sig 编码
df.to_csv("output.csv", encoding="utf-8-sig")

# openpyxl 通常能正确处理中文
```

## 最佳实践

1. **数据分析** → 使用 `pandas`
2. **格式化输出** → 使用 `openpyxl`
3. **大型文件** → 使用 `xlsxwriter` 或 `read_only/write_only` 模式
4. **公式处理** → 注意公式不会自动计算
5. **批量操作** → 使用路径模式和循环