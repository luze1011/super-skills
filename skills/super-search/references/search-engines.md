# 搜索引擎参考文档

## 支持的搜索引擎

### 国际搜索引擎

#### Google
- **网址**: https://www.google.com
- **特点**: 全球最大的搜索引擎，搜索结果全面
- **适用场景**: 国际资讯、技术文档、学术论文
- **注意事项**: 国内需要代理访问

#### Bing
- **网址**: https://www.bing.com
- **特点**: 微软旗下搜索引擎，与 ChatGPT 集成
- **适用场景**: 学术搜索、图片搜索、视频搜索
- **API**: Bing Web Search API

#### DuckDuckGo
- **网址**: https://duckduckgo.com
- **特点**: 隐私优先，不追踪用户
- **适用场景**: 敏感搜索、隐私保护场景
- **优势**: 无需代理，无搜索历史

### 中文搜索引擎

#### 百度
- **网址**: https://www.baidu.com
- **特点**: 中文优化，国内使用最广
- **适用场景**: 中文内容、国内资讯
- **注意事项**: 广告较多，需要筛选

#### 搜狗
- **网址**: https://www.sogou.com
- **特点**: 微信内容整合
- **适用场景**: 搜索微信公众号文章
- **优势**: 微信生态内容覆盖

#### 360搜索
- **网址**: https://www.so.com
- **特点**: 安全搜索
- **适用场景**: 常规搜索
- **注意事项**: 结果质量一般

## 搜索语法技巧

### 通用搜索语法

| 语法 | 作用 | 示例 |
|------|------|------|
| `""` | 精确匹配 | `"AI Agent"` |
| `site:` | 限定网站 | `site:github.com AI` |
| `filetype:` | 限定文件类型 | `filetype:pdf 机器学习` |
| `-` | 排除关键词 | `AI -人工智能` |
| `OR` | 或运算 | `AI OR 人工智能` |
| `intitle:` | 标题包含 | `intitle:教程` |
| `inurl:` | URL包含 | `inurl:blog` |

### Google 高级搜索

```
# 搜索最近一年的内容
AI Agent after:2023-01-01

# 搜索指定时间范围
机器学习 before:2023-12-31 after:2023-01-01

# 搜索相关网站
related:openai.com
```

### 百度高级搜索

```
# 限定网站
site:zhihu.com AI

# 限定文件类型
filetype:pdf 深度学习

# 限定标题
intitle:人工智能
```

## API 接入

### Google Custom Search API

```python
import requests

api_key = "YOUR_API_KEY"
search_engine_id = "YOUR_SEARCH_ENGINE_ID"
query = "AI Agent"

url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
response = requests.get(url)
results = response.json()
```

### Bing Web Search API

```python
import requests

api_key = "YOUR_API_KEY"
query = "AI Agent"

url = f"https://api.bing.microsoft.com/v7.0/search?q={query}"
headers = {"Ocp-Apim-Subscription-Key": api_key}
response = requests.get(url, headers=headers)
results = response.json()
```

## 搜索结果解析

### HTML 选择器参考

#### Google
```css
/* 搜索结果容器 */
div.g

/* 标题 */
h3

/* 链接 */
div.yuRUbf > a

/* 摘要 */
div[data-sncf]
```

#### Bing
```css
/* 搜索结果容器 */
li.b_algo

/* 标题 */
h2

/* 链接 */
h2 > a

/* 摘要 */
p, div.b_caption
```

#### 百度
```css
/* 搜索结果容器 */
div.result

/* 标题 */
h3

/* 链接 */
h3 > a

/* 摘要 */
div.c-abstract
```

## 频率限制

| 搜索引擎 | 限制 | 建议 |
|---------|------|------|
| Google | 严格 | 使用 API，间隔 1-2 秒 |
| Bing | 中等 | 间隔 1 秒 |
| DuckDuckGo | 宽松 | 间隔 0.5 秒 |
| 百度 | 中等 | 间隔 1 秒，避免触发验证码 |

## 最佳实践

1. **并发控制**: 避免同时请求多个搜索引擎
2. **延迟策略**: 每次请求间隔 1-2 秒
3. **代理轮换**: 使用代理池避免 IP 封禁
4. **结果缓存**: 缓存搜索结果，避免重复请求
5. **错误处理**: 处理验证码、超时等异常情况