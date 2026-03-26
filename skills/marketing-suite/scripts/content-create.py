#!/usr/bin/env python3
"""
营销内容创作脚本
支持多平台内容生成与适配
"""

import argparse
import json
from datetime import datetime
from typing import Optional

# 平台配置
PLATFORM_CONFIG = {
    "xiaohongshu": {
        "name": "小红书",
        "max_title": 20,
        "max_content": 1000,
        "style": "种草风、真实分享、emoji丰富",
        "hashtags": 5,
        "emoji_density": "high"
    },
    "douyin": {
        "name": "抖音",
        "max_title": 30,
        "max_content": 500,
        "style": "短平快、悬念开头、节奏感强",
        "hashtags": 3,
        "emoji_density": "medium"
    },
    "weibo": {
        "name": "微博",
        "max_title": 50,
        "max_content": 2000,
        "style": "话题引导、互动性强",
        "hashtags": 2,
        "emoji_density": "low"
    },
    "wechat": {
        "name": "微信公众号",
        "max_title": 30,
        "max_content": 5000,
        "style": "深度内容、价值输出、专业感",
        "hashtags": 0,
        "emoji_density": "low"
    }
}

# 风格模板
STYLE_TEMPLATES = {
    "casual": "轻松活泼、口语化、亲切感",
    "professional": "专业权威、数据支撑、理性分析",
    "emotional": "情感共鸣、故事化、温暖治愈",
    "funny": "幽默风趣、网络梗、娱乐化",
    "storytelling": "故事叙述、场景描绘、代入感"
}


def create_content(
    platform: str,
    topic: str,
    style: str = "casual",
    keywords: Optional[list] = None,
    output_format: str = "markdown"
) -> dict:
    """
    创建营销内容
    
    Args:
        platform: 目标平台
        topic: 内容主题
        style: 内容风格
        keywords: 关键词列表
        output_format: 输出格式
    
    Returns:
        生成的内容字典
    """
    config = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG["xiaohongshu"])
    style_desc = STYLE_TEMPLATES.get(style, STYLE_TEMPLATES["casual"])
    
    # 构建内容框架
    content = {
        "platform": config["name"],
        "platform_code": platform,
        "topic": topic,
        "style": style_desc,
        "created_at": datetime.now().isoformat(),
        "content": {
            "title": f"[待填写] {topic}",
            "body": f"[待填写正文内容，风格：{style_desc}]",
            "highlights": ["核心卖点1", "核心卖点2", "核心卖点3"],
            "cta": "[待填写行动号召]",
            "hashtags": []
        },
        "guidelines": {
            "max_title_length": config["max_title"],
            "max_content_length": config["max_content"],
            "recommended_hashtags": config["hashtags"],
            "emoji_suggestion": config["emoji_density"]
        }
    }
    
    # 添加关键词
    if keywords:
        content["keywords"] = keywords
        content["content"]["hashtags"] = [f"#{kw}" for kw in keywords[:config["hashtags"]]]
    
    return content


def generate_all_platforms(topic: str, style: str = "casual") -> dict:
    """生成全平台适配内容"""
    results = {}
    for platform in PLATFORM_CONFIG:
        results[platform] = create_content(platform, topic, style)
    return results


def format_output(content: dict, output_format: str = "markdown") -> str:
    """格式化输出"""
    if output_format == "json":
        return json.dumps(content, ensure_ascii=False, indent=2)
    
    # Markdown 格式
    md = f"""# 营销内容创作

## 平台：{content['platform']}
## 主题：{content['topic']}
## 风格：{content['style']}

---

### 标题
{content['content']['title']}

### 正文
{content['content']['body']}

### 核心卖点
"""
    for h in content['content']['highlights']:
        md += f"- {h}\n"
    
    md += f"""
### 行动号召
{content['content']['cta']}

### 话题标签
{' '.join(content['content']['hashtags'])}

---

## 创作指南
- 标题字数限制：{content['guidelines']['max_title_length']}字
- 正文字数限制：{content['guidelines']['max_content_length']}字
- 推荐标签数：{content['guidelines']['recommended_hashtags']}个
- Emoji 建议：{content['guidelines']['emoji_suggestion']}

---
创建时间：{content['created_at']}
"""
    return md


def main():
    parser = argparse.ArgumentParser(description="营销内容创作工具")
    parser.add_argument("--platform", "-p", default="xiaohongshu",
                        choices=list(PLATFORM_CONFIG.keys()) + ["all"],
                        help="目标平台")
    parser.add_argument("--topic", "-t", required=True, help="内容主题")
    parser.add_argument("--style", "-s", default="casual",
                        choices=list(STYLE_TEMPLATES.keys()),
                        help="内容风格")
    parser.add_argument("--keywords", "-k", nargs="+", help="关键词列表")
    parser.add_argument("--format", "-f", default="markdown",
                        choices=["markdown", "json"],
                        help="输出格式")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 生成内容
    if args.platform == "all":
        result = generate_all_platforms(args.topic, args.style)
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        content = create_content(args.platform, args.topic, args.style, args.keywords)
        output = format_output(content, args.format)
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"内容已保存到：{args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()