# 数据提取参考文档

## 网页内容提取

### 核心库

#### BeautifulSoup
- **用途**: HTML/XML 解析
- **优势**: 简单易用，支持多种解析器
- **安装**: `pip install beautifulsoup4`

#### Readability
- **用途**: 提取网页正文
- **优势**: 智能识别主要内容
- **安装**: `pip install readability-lxml`

#### Trafilatura
- **用途**: 新闻文章提取
- **优势**: 提取质量高，支持元数据
- **安装**: `pip install trafilatura`

### 正文提取

```python
from readability import Document
from bs4 import BeautifulSoup
import requests

def extract_content(url: str) -> dict:
    """提取网页正文"""
    response = requests.get(url)
    doc = Document(response.text)
    
    return {
        "title": doc.title(),
        "content": doc.summary(),
        "short_title": doc.short_title(),
    }
```

### 新闻文章提取

```python
import trafilatura

def extract_news(url: str) -> dict:
    """提取新闻文章"""
    downloaded = trafilatura.fetch_url(url)
    
    return {
        "title": trafilatura.extract_metadata(downloaded).title,
        "text": trafilatura.extract(downloaded),
        "comments": trafilatura.extract(downloaded, include_comments=True),
    }
```

## RSS/Atom 解析

### Feedparser

```python
import feedparser

def parse_rss(url: str) -> list:
    """解析 RSS 源"""
    feed = feedparser.parse(url)
    
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "summary": entry.get("summary", ""),
            "author": entry.get("author", ""),
            "published": entry.get("published", ""),
            "tags": [tag.term for tag in entry.get("tags", [])],
        })
    
    return articles
```

### RSSHub

RSSHub 是一个开源的 RSS 生成器，可以为各种网站生成 RSS 源。

**常用 RSS 源**:
- 微博热搜: `https://rsshub.app/weibo/search/hot`
- 知乎热榜: `https://rsshub.app/zhihu/hotlist`
- 36氪: `https://rsshub.app/36kr/newsflashes`
- 虎嗅: `https://rsshub.app/huxiu/article`

## 结构化数据提取

### JSON-LD

```python
from bs4 import BeautifulSoup
import json

def extract_jsonld(html: str) -> list:
    """提取 JSON-LD 结构化数据"""
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    
    data = []
    for script in scripts:
        try:
            data.append(json.loads(script.string))
        except:
            continue
    
    return data
```

### Open Graph

```python
from bs4 import BeautifulSoup

def extract_og(html: str) -> dict:
    """提取 Open Graph 元数据"""
    soup = BeautifulSoup(html, "html.parser")
    
    og_data = {}
    for meta in soup.find_all("meta", property=lambda x: x and x.startswith("og:")):
        prop = meta.get("property", "").replace("og:", "")
        og_data[prop] = meta.get("content", "")
    
    return og_data
```

### Twitter Cards

```python
def extract_twitter_cards(html: str) -> dict:
    """提取 Twitter Cards 元数据"""
    soup = BeautifulSoup(html, "html.parser")
    
    tc_data = {}
    for meta in soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")}):
        name = meta.get("name", "").replace("twitter:", "")
        tc_data[name] = meta.get("content", "")
    
    return tc_data
```

## 关键信息提取

### 发布时间

```python
import re
from datetime import datetime

def extract_publish_time(html: str) -> datetime:
    """提取发布时间"""
    soup = BeautifulSoup(html, "html.parser")
    
    # 尝试多种时间格式
    time_patterns = [
        r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",
        r"(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2})",
        r"(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2})",
    ]
    
    # 查找 time 标签
    time_elem = soup.find("time")
    if time_elem:
        datetime_str = time_elem.get("datetime") or time_elem.get_text()
        for pattern in time_patterns:
            match = re.search(pattern, datetime_str)
            if match:
                return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
    
    # 查找 meta 标签
    for meta in soup.find_all("meta"):
        if meta.get("property") in ["article:published_time", "og:published_time"]:
            return datetime.fromisoformat(meta.get("content").replace("Z", "+00:00"))
    
    return None
```

### 作者信息

```python
def extract_author(html: str) -> str:
    """提取作者信息"""
    soup = BeautifulSoup(html, "html.parser")
    
    # 尝试多种选择器
    selectors = [
        "meta[name='author']",
        "span.author",
        "div.author-name",
        "a[rel='author']",
    ]
    
    for selector in selectors:
        elem = soup.select_one(selector)
        if elem:
            if elem.name == "meta":
                return elem.get("content", "")
            return elem.get_text(strip=True)
    
    return ""
```

## 内容清洗

### HTML 清洗

```python
import re

def clean_html(html: str) -> str:
    """清洗 HTML 内容"""
    # 移除脚本和样式
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    
    # 移除注释
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    
    # 移除多余空白
    html = re.sub(r"\s+", " ", html)
    
    return html.strip()
```

### 文本清洗

```python
def clean_text(text: str) -> str:
    """清洗文本内容"""
    # 移除 HTML 实体
    import html
    text = html.unescape(text)
    
    # 移除特殊字符
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)
    
    # 规范化空白
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()
```

## 中文分词

### Jieba

```python
import jieba
import jieba.analyse

def tokenize(text: str) -> list:
    """中文分词"""
    return list(jieba.cut(text))

def extract_keywords(text: str, top_k: int = 10) -> list:
    """提取关键词"""
    return jieba.analyse.extract_tags(text, topK=top_k)

def extract_summary(text: str, top_k: int = 5) -> list:
    """提取摘要关键词"""
    return jieba.analyse.textrank(text, topK=top_k)
```

## 最佳实践

1. **编码处理**: 统一使用 UTF-8 编码
2. **异常处理**: 处理网络超时、解析错误
3. **延迟控制**: 避免频繁请求同一网站
4. **结果验证**: 验证提取的数据完整性
5. **缓存策略**: 缓存已提取的内容