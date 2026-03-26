# Super Search - 超级搜索技能

> 多搜索引擎整合、新闻聚合、社交研究、智能信息提取的一站式搜索解决方案

## 概述

超级搜索技能整合了多种搜索能力，帮助用户快速获取全面的信息：

- **多搜索引擎** - 同时查询 Google、Bing、DuckDuckGo、百度等多个搜索引擎
- **新闻聚合** - 从多个新闻源聚合最新资讯
- **社交研究** - 搜索微博、知乎、小红书等社交平台
- **信息提取** - 智能提取网页内容、生成摘要

## 安装依赖

```bash
pip install requests beautifulsoup4 feedparser readability-lxml jieba
```

## 使用方法

### 1. 多搜索引擎

```bash
python scripts/multi-search.py "搜索关键词" --engines google,bing,duckduckgo,baidu
```

**参数说明**：
- `query`: 搜索关键词（必填）
- `--engines`: 指定搜索引擎，默认全部
- `--max-results`: 每个引擎最大结果数，默认 10
- `--output`: 输出格式（json/markdown/table），默认 markdown

**示例**：
```bash
# 基础搜索
python scripts/multi-search.py "AI Agent 开发"

# 指定引擎和结果数
python scripts/multi-search.py "大模型应用" --engines google,bing --max-results 20

# 输出 JSON 格式
python scripts/multi-search.py "GPT-5 发布时间" --output json
```

### 2. 新闻聚合

```bash
python scripts/news-aggregate.py "关键词" --days 3 --sources all
```

**参数说明**：
- `keyword`: 新闻关键词（必填）
- `--days`: 最近几天，默认 7
- `--sources`: 新闻源（all/tech/finance/social），默认 all
- `--output`: 输出文件路径（可选）

**示例**：
```bash
# 搜索最近 3 天的科技新闻
python scripts/news-aggregate.py "OpenAI" --days 3 --sources tech

# 搜索财经新闻并保存
python scripts/news-aggregate.py "美联储加息" --sources finance --output news.md
```

### 3. 社交研究

```bash
python scripts/social-research.py "关键词" --platforms weibo,zhihu --limit 50
```

**参数说明**：
- `keyword`: 搜索关键词（必填）
- `--platforms`: 平台（weibo/zhihu/xiaohongshu/douban），默认全部
- `--limit`: 每个平台最大结果数，默认 30
- `--sort`: 排序方式（time/hot/relevant），默认 relevant

**示例**：
```bash
# 微博热搜研究
python scripts/social-research.py "AI绘画" --platforms weibo --sort hot

# 多平台综合研究
python scripts/social-research.py "大模型落地" --platforms weibo,zhihu --limit 50
```

## 支持的搜索引擎

| 引擎 | 特点 | 适用场景 |
|------|------|---------|
| Google | 全球最大，结果全面 | 国际资讯、技术资料 |
| Bing | 微软搜索，AI 增强 | 学术搜索、图片搜索 |
| DuckDuckGo | 隐私优先，无追踪 | 敏感搜索、隐私保护 |
| Baidu | 中文优化，本土化 | 中文内容、国内资讯 |
| Sogou | 微信内容整合 | 微信公众号文章 |

## RSS 新闻源配置

RSS 源配置文件位于 `assets/rss-sources.json`，可以自定义添加：

```json
{
  "tech": [
    {"name": "36氪", "url": "https://36kr.com/feed", "type": "rss"},
    {"name": "虎嗅", "url": "https://www.huxiu.com/rss/0.xml", "type": "rss"}
  ],
  "finance": [
    {"name": "财新网", "url": "https://rsshub.app/caixin/finance", "type": "rss"}
  ]
}
```

## 信息提取能力

支持从网页中提取：

- **正文内容** - 智能识别主要内容
- **标题摘要** - 自动生成标题和摘要
- **关键信息** - 提取日期、作者、来源
- **结构化数据** - 表格、列表、代码块

## 输出格式

### Markdown 格式

```markdown
# 搜索结果：AI Agent 开发

## Google (10 条)

1. [AI Agent 开发指南](https://example.com/1)
   > 详细介绍 AI Agent 的开发流程...

2. [构建智能 Agent 系统](https://example.com/2)
   > 从零开始构建企业级 Agent...

## Bing (8 条)

...
```

### JSON 格式

```json
{
  "query": "AI Agent 开发",
  "timestamp": "2026-03-26T15:00:00+08:00",
  "results": {
    "google": [
      {"title": "...", "url": "...", "snippet": "..."}
    ]
  }
}
```

## 高级功能

### 结果去重

自动合并多个搜索引擎的重复结果，智能合并标题和摘要。

### 相关性排序

使用关键词匹配和语义相似度对结果重新排序。

### 实时热点

结合微博热搜、知乎热榜，识别当前热点话题。

## 注意事项

1. **频率限制** - 部分搜索引擎有访问频率限制，建议间隔 1-2 秒
2. **代理配置** - 访问 Google 等需要配置代理
3. **Cookie 失效** - 社交平台搜索可能需要定期更新 Cookie

## 更新日志

- **2026-03-26**: 初始版本发布
  - 多搜索引擎整合
  - RSS 新闻聚合
  - 社交平台研究
  - 智能信息提取