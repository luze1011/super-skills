#!/usr/bin/env python3
"""
文本润色工具 - Super Writing Assistant

用法：
    python polish-text.py --input <文件> [--check-all] [--output <文件>]

参数：
    --input     输入文件路径
    --check-all 执行所有检查
    --output    输出文件路径（可选，默认打印到控制台）
"""

import argparse
import re
from pathlib import Path
from typing import List, Tuple


# 润色规则
POLISH_RULES = [
    {
        "name": "删除冗余形容词",
        "pattern": r"(非常重要的|关键的|核心的|主要的|基本的)",
        "replacement": "",
        "example": "这是一个非常重要的关键功能 → 该功能"
    },
    {
        "name": "删除空洞开头",
        "pattern": r"在当今(快速发展的)?(技术领域|社会|市场)中[，,]?",
        "replacement": "",
        "example": "在当今快速发展的技术领域中 → （删除）"
    },
    {
        "name": "简化动词",
        "pattern": r"可以帮助(用户)?(实现|完成|达到)",
        "replacement": "帮助实现",
        "example": "可以帮助用户实现 → 帮助实现"
    },
    {
        "name": "删除营销废话",
        "pattern": r"(革命性的|创新性的|颠覆性的|突破性的)[，,]?",
        "replacement": "",
        "example": "革命性的技术 → 技术"
    },
    {
        "name": "具体化模糊表达",
        "pattern": r"大幅(提升|提高|改善|优化)",
        "replacement": "提升（请补充具体数据）",
        "example": "大幅提升效率 → 提升（请补充具体数据）"
    }
]


# 检查规则
CHECK_RULES = [
    {
        "name": "句子重复检查",
        "check": "每句话有独特价值，无重复信息",
        "severity": "高"
    },
    {
        "name": "形容词检查",
        "check": "无冗余形容词/副词",
        "severity": "中"
    },
    {
        "name": "句式变化检查",
        "check": "句式有变化，不单调",
        "severity": "中"
    },
    {
        "name": "术语准确性检查",
        "check": "专业术语使用准确",
        "severity": "高"
    },
    {
        "name": "具体性检查",
        "check": "用具体数字/案例替代模糊描述",
        "severity": "高"
    },
    {
        "name": "营销废话检查",
        "check": "无'革命性'、'创新'等空洞词汇",
        "severity": "中"
    }
]


def polish_text(text: str) -> Tuple[str, List[dict]]:
    """润色文本，返回润色后的文本和修改记录"""
    changes = []
    polished = text
    
    for rule in POLISH_RULES:
        pattern = rule["pattern"]
        replacement = rule["replacement"]
        
        matches = re.findall(pattern, polished)
        if matches:
            before = polished
            polished = re.sub(pattern, replacement, polished)
            if before != polished:
                changes.append({
                    "rule": rule["name"],
                    "count": len(matches),
                    "example": rule["example"]
                })
    
    return polished, changes


def generate_checklist(text: str) -> List[dict]:
    """生成检查清单"""
    results = []
    
    for rule in CHECK_RULES:
        results.append({
            "name": rule["name"],
            "check": rule["check"],
            "severity": rule["severity"],
            "status": "待检查"
        })
    
    return results


def format_polish_report(original: str, polished: str, changes: List[dict], checks: List[dict]) -> str:
    """格式化润色报告"""
    report = """# 润色报告

## 自动润色结果

"""
    
    if changes:
        report += "### 应用的规则：\n\n"
        for change in changes:
            report += f"- **{change['rule']}** ({change['count']}处)\n"
            report += f"  - 示例：{change['example']}\n\n"
    else:
        report += "✅ 未发现需要自动润色的问题\n\n"
    
    report += """## 润色后文本

---
"""
    report += polished
    report += "\n---\n"
    
    report += """
## 质量检查清单

"""
    for check in checks:
        report += f"- [ ] **{check['name']}** ({check['severity']}优先级)\n"
        report += f"  - {check['check']}\n\n"
    
    report += """
## 手动检查建议

1. **阅读润色后文本**：确认自动修改是否合适
2. **逐项检查清单**：确保每项都已满足
3. **补充具体数据**：为模糊表达补充具体数字
4. **删除重复信息**：确保每句话有独特价值
5. **验证术语准确**：确保专业术语使用正确

---
*由 Super Writing Assistant 生成*
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="文本润色工具")
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--check-all", action="store_true", help="执行所有检查")
    parser.add_argument("--output", help="输出文件路径（可选）")
    
    args = parser.parse_args()
    
    # 读取输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {args.input}")
    
    original_text = input_path.read_text(encoding='utf-8')
    
    # 润色文本
    polished_text, changes = polish_text(original_text)
    
    # 生成检查清单
    checks = generate_checklist(polished_text)
    
    # 生成报告
    report = format_polish_report(original_text, polished_text, changes, checks)
    
    # 输出
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding='utf-8')
        print(f"✅ 润色报告已保存到: {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()