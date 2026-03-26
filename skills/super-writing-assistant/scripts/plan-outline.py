#!/usr/bin/env python3
"""
大纲规划工具 - Super Writing Assistant

用法：
    python plan-outline.py --type <类型> --topic "<主题>" [--output <文件>]

参数：
    --type    内容类型：营销|技术|技能|计划
    --topic   写作主题
    --output  输出文件路径（可选，默认打印到控制台）
"""

import argparse
import json
from pathlib import Path


# 结构模板
STRUCTURES = {
    "营销": {
        "name": "营销文案结构",
        "sections": [
            "标题（价值主张）",
            "副标题（具体化）",
            "CTA（主要行动号召）",
            "社会证明",
            "痛点描述",
            "解决方案/收益",
            "工作原理",
            "异议处理",
            "最终CTA"
        ],
        "questions": [
            "页面类型？（首页/落地页/详情页）",
            "目标行动？（注册/购买/下载）",
            "受众画像？（年龄/职业/痛点）",
            "核心痛点是什么？",
            "独特卖点是什么？"
        ]
    },
    "技术": {
        "name": "技术文档结构",
        "sections": [
            "概述（1-2句说明）",
            "前置条件",
            "核心概念",
            "实现步骤（带代码示例）",
            "常见问题",
            "进阶话题"
        ],
        "questions": [
            "读者技术水平？（初学者/中级/高级）",
            "使用的技术栈？",
            "要解决什么问题？",
            "需要代码示例吗？",
            "预期产出是什么？"
        ]
    },
    "技能": {
        "name": "技能文档结构",
        "sections": [
            "name（技能标识）",
            "description（触发条件）",
            "概述（核心原则）",
            "When to Use（触发场景）",
            "Core Pattern（Before/After）",
            "Quick Reference（速查表）",
            "Implementation（实现）",
            "Common Mistakes（常见错误）"
        ],
        "questions": [
            "触发场景是什么？",
            "核心原则是什么？",
            "需要什么工具/依赖？",
            "常见错误有哪些？",
            "如何测试验证？"
        ]
    },
    "计划": {
        "name": "实施计划结构",
        "sections": [
            "目标陈述",
            "架构概述",
            "技术栈",
            "文件清单",
            "任务分解（每步2-5分钟）",
            "验证步骤",
            "提交节点"
        ],
        "questions": [
            "技术栈是什么？",
            "文件结构是什么？",
            "任务粒度？（粗粒度/细粒度）",
            "如何验证？",
            "提交节点有哪些？"
        ]
    }
}


def generate_outline(content_type: str, topic: str) -> dict:
    """生成大纲"""
    if content_type not in STRUCTURES:
        raise ValueError(f"未知的内容类型: {content_type}。支持的类型: {list(STRUCTURES.keys())}")
    
    template = STRUCTURES[content_type]
    
    outline = {
        "type": content_type,
        "topic": topic,
        "structure": template["name"],
        "sections": template["sections"],
        "questions_to_answer": template["questions"],
        "estimated_sections": len(template["sections"])
    }
    
    return outline


def format_outline_markdown(outline: dict) -> str:
    """格式化为 Markdown"""
    md = f"""# {outline['topic']} - 大纲规划

## 内容类型
{outline['structure']}

## 结构大纲

"""
    for i, section in enumerate(outline['sections'], 1):
        md += f"{i}. **{section}**\n   - [ ] 待填写\n\n"
    
    md += f"""## 需要回答的问题

"""
    for q in outline['questions_to_answer']:
        md += f"- {q}\n"
    
    md += f"""
## 预计段落数
{outline['estimated_sections']} 个主要部分

---
*由 Super Writing Assistant 生成*
"""
    return md


def main():
    parser = argparse.ArgumentParser(description="大纲规划工具")
    parser.add_argument("--type", required=True, choices=list(STRUCTURES.keys()), help="内容类型")
    parser.add_argument("--topic", required=True, help="写作主题")
    parser.add_argument("--output", help="输出文件路径（可选）")
    
    args = parser.parse_args()
    
    # 生成大纲
    outline = generate_outline(args.type, args.topic)
    
    # 格式化输出
    md_content = format_outline_markdown(outline)
    
    # 输出
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(md_content, encoding='utf-8')
        print(f"✅ 大纲已保存到: {output_path}")
    else:
        print(md_content)


if __name__ == "__main__":
    main()