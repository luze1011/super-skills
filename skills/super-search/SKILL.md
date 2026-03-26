# Super Search - 超级搜索技能

统一的智能搜索解决方案，集成多搜索引擎、AI 增强、新闻聚合、社交媒体研究和信息提取。

---

## 🎯 核心能力

| 模块 | 功能 | 工具 |
|------|------|------|
| **多搜索引擎** | DuckDuckGo/Google/Bing 搜索聚合 | `web_search` |
| **AI 搜索增强** | Google AI Mode 智能摘要 | `google-ai-mode-skill` |
| **新闻聚合** | 多源新闻抓取、RSS、分类过滤 | `news-aggregator-skill` |
| **社交研究** | TikTok 研究、趋势分析 | `tiktok-research` |
| **信息提取** | 网页内容提取、结构化输出 | `web_fetch` |

---

## 📋 使用场景决策

```
用户需求 → 判断场景 → 选择工具

┌─ 简单查询（< 3 条结果）
│  └→ web_search (DuckDuckGo)
│
├─ 深度研究（需 AI 总结）
│  └→ google-ai-mode-skill
│
├─ 新闻/热点追踪
│  └→ news-aggregator-skill
│
├─ 社交媒体内容研究
│  └→ tiktok-research
│
├─ 提取网页内容
│  └→ web_fetch
│
└─ 综合搜索（多源聚合）
   └→ 调用多个工具 + 结果整合
```

---

## 🔧 核心命令参考

### 1. 多搜索引擎集成

#### DuckDuckGo 搜索（推荐首选）

```python
# 工具：web_search
# 特点：无需 API Key，速度快，隐私友好

# 基础搜索
web_search(query="关键词", count=10)

# 指定地区
web_search(query="关键词", region="zh-cn", count=10)

# 安全搜索模式
web_search(query="关键词", safeSearch="strict")  # strict/moderate/off
```

#### Google 搜索（通过 AI Mode）

```python
# 工具：google-ai-mode-skill
# 特点：AI 增强搜索，智能摘要，语义理解

# AI 搜索
read("~/.agents/skills/google-ai-mode-skill/SKILL.md")
# 然后使用浏览器自动化访问 Google AI Mode
```

#### Bing 搜索

```python
# 通过 browser 工具访问
browser(action="open", url="https://www.bing.com")
browser(action="act", kind="type", selector="input[type='search']", text="关键词")
browser(action="act", kind="press", key="Enter")
```

#### 搜索结果聚合

```python
# 并行调用多个搜索引擎
# 使用 sessions_spawn 异步处理

# 示例：聚合 DuckDuckGo + 新闻
results_ddg = web_search(query="AI 趋势", count=5)
results_news = read_skill("news-aggregator-skill")
# 合并去重后返回
```

---

### 2. AI 搜索增强

#### Google AI Mode 智能搜索

```python
# 读取技能说明
read("~/.agents/skills/google-ai-mode-skill/SKILL.md")

# 使用浏览器自动化
browser(action="open", url="https://www.google.com")
browser(action="snapshot")
# 在搜索框输入问题
browser(action="act", kind="type", selector="textarea[name='q']", text="你的问题")
browser(action="act", kind="press", key="Enter")
# 等待 AI Mode 响应
browser(action="snapshot")
```

#### 智能摘要流程

```
1. web_search 获取结果列表
2. web_fetch 提取前 3-5 篇文章内容
3. 合并内容后使用 AI 总结要点
4. 返回结构化摘要
```

#### 语义搜索示例

```python
# 使用 AI Mode 进行语义理解搜索
# 输入自然语言问题，而非关键词
query = "最近 AI 领域有哪些重要的技术突破？"
# AI Mode 会理解问题意图，返回相关答案
```

---

### 3. 新闻聚合

#### 多源新闻抓取

```python
# 读取新闻聚合技能
read("~/.agents/skills/news-aggregator-skill/SKILL.md")

# 或使用 news-aggregator-skill
# 自动抓取多个新闻源
```

#### RSS 订阅管理

```python
# RSS 源配置示例
RSS_SOURCES = {
    "科技": [
        "https://www.36kr.com/feed",
        "https://techcrunch.com/feed/",
    ],
    "财经": [
        "https://www.ft.com/rss/home",
    ],
    "AI": [
        "https://openai.com/blog/rss.xml",
    ]
}

# 使用 web_fetch 抓取 RSS
web_fetch(url="https://example.com/feed.xml", extractMode="text")
```

#### 新闻分类与过滤

```python
# 按关键词过滤新闻
def filter_news(news_list, keywords):
    return [n for n in news_list 
            if any(kw in n['title'] or kw in n['content'] 
                   for kw in keywords)]

# 按时间过滤
def filter_by_date(news_list, start_date, end_date):
    # 解析时间戳并过滤
    pass

# 按来源过滤
def filter_by_source(news_list, sources):
    return [n for n in news_list if n['source'] in sources]
```

---

### 4. 社交媒体研究

#### TikTok 研究

```python
# 读取 TikTok 研究技能
read("~/.agents/skills/tiktok-research/SKILL.md")

# 功能：
# - 热门视频分析
# - 趋势标签发现
# - 内容表现统计
```

#### 内容分析流程

```
1. 搜索目标内容
2. 提取关键指标（点赞、评论、分享）
3. 分析内容模式
4. 生成报告
```

#### 趋势发现

```python
# 使用 TikTok Research API
# 或通过浏览器自动化抓取热门内容

browser(action="open", url="https://www.tiktok.com/trending")
browser(action="snapshot")
# 分析热门视频数据
```

---

### 5. 信息提取

#### 网页内容提取

```python
# 工具：web_fetch
# 提取网页正文内容

# Markdown 格式（推荐）
web_fetch(url="https://example.com/article", extractMode="markdown")

# 纯文本格式
web_fetch(url="https://example.com/article", extractMode="text")

# 限制字符数
web_fetch(url="https://example.com", maxChars=5000)
```

#### 数据清洗

```python
import re

def clean_text(text):
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:，。！？；：]', '', text)
    return text.strip()

def extract_urls(text):
    return re.findall(r'https?://[^\s]+', text)

def extract_emails(text):
    return re.findall(r'[\w.-]+@[\w.-]+\.\w+', text)
```

#### 结构化输出

```python
# 提取文章信息
def extract_article_info(url):
    content = web_fetch(url=url, extractMode="markdown")
    
    return {
        "url": url,
        "title": extract_title(content),
        "author": extract_author(content),
        "date": extract_date(content),
        "summary": extract_summary(content),
        "keywords": extract_keywords(content),
    }
```

---

## 🚀 CLI 使用示例

### 快速搜索

```bash
# DuckDuckGo 搜索（通过 agent 对话）
> 搜索 "OpenAI 最新动态"

# AI 增强搜索
> 用 Google AI Mode 搜索 "AI Agent 发展趋势"

# 新闻聚合
> 查看今天的科技新闻
```

### 深度研究

```bash
# 综合研究流程
> 帮我研究一下 "Claude 3.5 Sonnet" 的能力
# 自动执行：
# 1. web_search 搜索
# 2. web_fetch 提取相关文章
# 3. AI 总结要点
```

### 内容提取

```bash
# 提取网页内容
> 提取 https://example.com/article 的内容
# 返回 Markdown 格式正文
```

---

## 📊 Python 使用示例

### 综合搜索函数

```python
async def super_search(query, mode="quick"):
    """
    超级搜索统一接口
    
    Args:
        query: 搜索关键词
        mode: 搜索模式
            - quick: 快速搜索（DuckDuckGo）
            - deep: 深度搜索（AI Mode + 多源）
            - news: 新闻搜索
            - social: 社交媒体搜索
    
    Returns:
        搜索结果（结构化数据）
    """
    
    if mode == "quick":
        # DuckDuckGo 搜索
        results = web_search(query=query, count=10)
        return results
    
    elif mode == "deep":
        # AI Mode 搜索
        ai_results = use_skill("google-ai-mode-skill", query)
        # 补充 DuckDuckGo 结果
        ddg_results = web_search(query=query, count=5)
        # 合并返回
        return merge_results(ai_results, ddg_results)
    
    elif mode == "news":
        # 新闻聚合
        return use_skill("news-aggregator-skill", query)
    
    elif mode == "social":
        # TikTok 研究
        return use_skill("tiktok-research", query)
```

### 信息提取函数

```python
async def extract_info(url, output_format="markdown"):
    """
    提取网页信息
    
    Args:
        url: 目标网址
        output_format: 输出格式
            - markdown: Markdown 格式
            - text: 纯文本
            - structured: 结构化数据
    
    Returns:
        提取的内容
    """
    
    if output_format in ["markdown", "text"]:
        return web_fetch(url=url, extractMode=output_format)
    
    elif output_format == "structured":
        content = web_fetch(url=url, extractMode="markdown")
        return {
            "url": url,
            "content": content,
            "extracted_at": datetime.now().isoformat()
        }
```

### 新闻监控函数

```python
async def monitor_news(keywords, sources=None):
    """
    监控新闻关键词
    
    Args:
        keywords: 关键词列表
        sources: 新闻源列表（可选）
    
    Returns:
        匹配的新闻列表
    """
    
    # 获取最新新闻
    all_news = use_skill("news-aggregator-skill")
    
    # 按关键词过滤
    filtered = []
    for news in all_news:
        if any(kw in news['title'] or kw in news.get('content', '') 
               for kw in keywords):
            filtered.append(news)
    
    # 按来源过滤
    if sources:
        filtered = [n for n in filtered if n.get('source') in sources]
    
    return filtered
```

---

## 🎓 常用操作速查

### 场景 1：快速查询

```
用户：搜索一下 Python 异步编程最佳实践
→ web_search(query="Python 异步编程最佳实践", count=5)
→ 返回前 5 条结果
```

### 场景 2：深度研究

```
用户：帮我研究一下 RAG 技术
→ web_search(query="RAG 技术 原理", count=10)
→ web_fetch 提取前 3 篇文章
→ AI 总结要点
→ 返回结构化报告
```

### 场景 3：新闻追踪

```
用户：最近有什么 AI 大新闻？
→ news-aggregator-skill 获取最新新闻
→ 按 AI 关键词过滤
→ 返回相关新闻列表
```

### 场景 4：竞品分析

```
用户：分析一下竞争对手的抖音内容
→ tiktok-research 搜索竞品账号
→ 提取热门视频数据
→ 分析内容模式
→ 生成分析报告
```

### 场景 5：内容提取

```
用户：提取这篇文章的内容 https://...
→ web_fetch(url, extractMode="markdown")
→ 数据清洗
→ 返回结构化内容
```

---

## 🔗 相关技能

| 技能 | 路径 | 用途 |
|------|------|------|
| `google-ai-mode-skill` | `~/.openclaw/workspace-taizi/skills/google-ai-mode-skill/` | Google AI 搜索 |
| `news-aggregator-skill` | `~/.openclaw/workspace-taizi/skills/news-aggregator-skill/` | 新闻聚合 |
| `tiktok-research` | `~/.agents/skills/tiktok-research/` | TikTok 研究 |
| `multi-search-engine` | `~/.agents/skills/multi-search-engine/` | 多搜索引擎 |
| `web-clipper` | `~/.agents/skills/web-clipper/` | 网页剪藏 |

---

## 💡 最佳实践

### 1. 选择合适的搜索工具

| 需求 | 推荐工具 | 理由 |
|------|---------|------|
| 快速查询 | `web_search` | 无需 API Key，速度快 |
| 深度研究 | `google-ai-mode-skill` | AI 增强，智能摘要 |
| 新闻追踪 | `news-aggregator-skill` | 多源聚合，实时更新 |
| 社交分析 | `tiktok-research` | 专业社交数据分析 |

### 2. 异步处理大型搜索

```python
# 预计耗时 > 1 分钟的任务
# 使用 sessions_spawn 异步处理

sessions_spawn(
    task="深度研究任务",
    skill="super-search",
    params={"query": "...", "mode": "deep"}
)
```

### 3. 结果缓存

```python
# 对重复搜索进行缓存
# 避免浪费 API 调用

cache_key = f"search:{query}:{mode}"
if cached := get_cache(cache_key):
    return cached

results = perform_search(query, mode)
set_cache(cache_key, results, ttl=3600)
```

---

## 🚨 注意事项

1. **API 限制**：`web_search` 无限制，其他工具可能有 API 限流
2. **隐私安全**：DuckDuckGo 注重隐私，Google/Bing 会记录搜索历史
3. **结果质量**：AI Mode 适合复杂问题，简单查询用 DuckDuckGo 更快
4. **异步处理**：大型搜索任务（> 1 分钟）必须使用异步模式
5. **数据清洗**：提取的内容可能需要清洗才能使用

---

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-03-26 | 1.0.0 | 初始版本，集成多搜索引擎、AI 增强、新闻聚合、社交研究、信息提取 |

---

*Super Search - 统一智能搜索解决方案*