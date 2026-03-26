#!/usr/bin/env python3
"""
初稿撰写工具 - Super Writing Assistant

用法：
    python write-draft.py --outline <大纲文件> --style <风格> [--output <文件>]

参数：
    --outline  大纲文件路径
    --style    写作风格：正式|轻松|技术|营销
    --output   输出文件路径（可选）
"""

import argparse
import json
from pathlib import Path


# 风格指南
STYLE_GUIDES = {
    "正式": {
        "name": "正式风格",
        "characteristics": [
            "使用完整句子",
            "避免口语化表达",
            "使用专业术语",
            "保持客观中立"
        ],
        "avoid": [
            "网络用语",
            "表情符号",
            "过于口语化的表达"
        ]
    },
    "轻松": {
        "name": "轻松风格",
        "characteristics": [
            "使用口语化表达",
            "适当使用比喻",
            "句式简洁明快",
            "可以适度幽默"
        ],
        "avoid": [
            "过于正式的词汇",
            "长难句",
            "过于严肃的语气"
        ]
    },
    "技术": {
        "name": "技术风格",
        "characteristics": [
            "直接切入技术内容",
            "使用同行对话语气",
            "解释'为什么'而非'是什么'",
            "提供完整可运行示例"
        ],
        "avoid": [
            "泛泛介绍",
            "教科书式语气",
            "代码片段不完整",
            "滥用形容词"
        ]
    },
    "营销": {
        "name": "营销风格",
        "characteristics": [
            "清晰胜于聪明",
            "收益胜于功能",
            "具体胜于模糊",
            "使用用户语言"
        ],
        "avoid": [
            "功能堆砌",
            "空洞的形容词",
            "公司术语",
            "模糊的价值主张"
        ]
    }
}


# 标题公式
TITLE_FORMULAS = {
    "营销": [
        "{达成结果} 无需 {痛点}",
        "为{受众}打造的{品类}",
        "再也不用{不愉快经历}",
        "{直击痛点的问题}"
    ],
    "技术": [
        "如何{实现目标}",
        "{技术}实践指南",
        "理解{概念}",
        "从{起点}到{终点}"
    ],
    "技能": [
        "{技能名} - {一句话描述}",
        "{触发场景}处理指南",
        "{核心功能}最佳实践"
    ],
    "计划": [
        "{项目名}实施计划",
        "构建{系统}的技术方案",
        "{目标}实现路线图"
    ]
}


# CTA公式
CTA_FORMULAS = [
    "开始{行动}",
    "获取{收益}",
    "{动词} + {得到什么} + {限定词}"
]


def load_outline(outline_path: str) -> dict:
    """加载大纲（支持 JSON 或 Markdown）"""
    path = Path(outline_path)
    
    if not path.exists():
        raise FileNotFoundError(f"大纲文件不存在: {outline_path}")
    
    content = path.read_text(encoding='utf-8')
    
    # 简单解析 Markdown 大纲
    if path.suffix == '.md':
        sections = []
        for line in content.split('\n'):
            if line.strip().startswith('- [ ]') or line.strip().startswith('1.'):
                section = line.replace('- [ ]', '').replace('- [x]', '').strip()
                section = section.lstrip('0123456789.').strip()
                if section.startswith('**') and section.endswith('**'):
                    section = section[2:-2]
                if section:
                    sections.append(section)
        
        return {
            "sections": sections,
            "raw_content": content
        }
    
    # JSON 格式
    return json.loads(content)


def generate_draft_prompt(outline: dict, style: str) -> str:
    """生成撰写提示"""
    style_guide = STYLE_GUIDES.get(style, STYLE_GUIDES["正式"])
    
    prompt = f"""# 撰写初稿

## 写作风格
**{style_guide['name']}**

### 特点：
"""
    for char in style_guide['characteristics']:
        prompt += f"- {char}\n"
    
    prompt += "\n### 避免：\n"
    for avoid in style_guide['avoid']:
        prompt += f"- {avoid}\n"
    
    prompt += f"""
## 大纲结构

"""
    for i, section in enumerate(outline.get('sections', []), 1):
        prompt += f"{i}. {section}\n"
    
    prompt += """
## 撰写要求

1. **每句话有独特价值**：避免重复信息
2. **具体胜于模糊**：用具体数字/案例替代模糊描述
3. **句式有变化**：避免单调重复的句式
4. **术语准确**：确保专业术语使用正确

---
请根据以上大纲和风格要求，撰写初稿内容。
"""
    return prompt


def main():
    parser = argparse.ArgumentParser(description="初稿撰写工具")
    parser.add_argument("--outline", required=True, help="大纲文件路径")
    parser.add_argument("--style", required=True, choices=list(STYLE_GUIDES.keys()), help="写作风格")
    parser.add_argument("--output", help="输出文件路径（可选）")
    
    args = parser.parse_args()
    
    # 加载大纲
    outline = load_outline(args.outline)
    
    # 生成撰写提示
    prompt = generate_draft_prompt(outline, args.style)
    
    # 输出
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(prompt, encoding='utf-8')
        print(f"✅ 撰写提示已保存到: {output_path}")
    else:
        print(prompt)


if __name__ == "__main__":
    main()