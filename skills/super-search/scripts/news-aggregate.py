#!/usr/bin/env python3
"""
新闻聚合脚本

从多个 RSS 源聚合新闻，支持关键词过滤和时间范围筛选。
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import feedparser
import jieba

# 默认 RSS 源配置文件
DEFAULT_RSS_CONFIG = Path(__file__).parent.parent / "assets" / "rss-sources.json"


class NewsAggregator:
    """新闻聚合器"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path or str(DEFAULT_RSS_CONFIG)
        self.sources = self._load_sources()

    def _load_sources(self) -> dict:
        """加载 RSS 源配置"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return self._get_default_sources()

    def _get_default_sources(self) -> dict:
        """获取默认 RSS 源"""
        return {
            "tech": [
                {"name": "36氪", "url": "https://36kr.com/feed", "type": "rss"},
                {"name": "虎嗅", "url": "https://www.huxiu.com/rss/0.xml", "type": "rss"},
                {"name": "极客公园", "url": "https://www.geekpark.net/rss", "type": "rss"},
                {"name": "爱范儿", "url": "https://www.ifanr.com/feed", "type": "rss"},
            ],
            "finance": [
                {"name": "财新网", "url": "https://rsshub.app/caixin/finance", "type": "rss"},
                {"name": "华尔街见闻", "url": "https://wallstreetcn.com/news/global", "type": "rss"},
            ],
            "social": [
                {"name": "微博热搜", "url": "https://rsshub.app/weibo/search/hot", "type": "rss"},
                {"name": "知乎热榜", "url": "https://rsshub.app/zhihu/hotlist", "type": "rss"},
            ],
        }

    def fetch_feed(self, source: dict) -> list:
        """获取单个 RSS 源的内容"""
        articles = []

        try:
            feed = feedparser.parse(source["url"])

            for entry in feed.entries:
                article = {
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "summary": entry.get("summary", ""),
                    "source": source["name"],
                    "published": entry.get("published", ""),
                }

                # 解析发布时间
                if entry.get("published_parsed"):
                    article["timestamp"] = datetime(*entry.published_parsed[:6])
                else:
                    article["timestamp"] = datetime.now()

                articles.append(article)

        except Exception as e:
            print(f"获取 {source['name']} 失败: {e}")

        return articles

    def filter_by_keyword(self, articles: list, keyword: str) -> list:
        """按关键词过滤文章"""
        if not keyword:
            return articles

        # 使用 jieba 分词
        keyword_words = set(jieba.cut(keyword))
        filtered = []

        for article in articles:
            text = f"{article['title']} {article['summary']}"
            article_words = set(jieba.cut(text))

            # 计算关键词匹配度
            overlap = keyword_words & article_words
            if overlap:
                article["relevance"] = len(overlap) / len(keyword_words)
                filtered.append(article)

        # 按相关性排序
        filtered.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        return filtered

    def filter_by_time(self, articles: list, days: int) -> list:
        """按时间范围过滤文章"""
        if days <= 0:
            return articles

        cutoff = datetime.now() - timedelta(days=days)
        return [a for a in articles if a.get("timestamp", datetime.min) >= cutoff]

    def aggregate(
        self,
        keyword: str = None,
        days: int = 7,
        sources: str = "all"
    ) -> list:
        """聚合新闻"""
        all_articles = []

        # 确定要获取的源
        if sources == "all":
            source_categories = list(self.sources.keys())
        else:
            source_categories = [s.strip() for s in sources.split(",")]

        # 获取所有文章
        for category in source_categories:
            if category in self.sources:
                for source in self.sources[category]:
                    articles = self.fetch_feed(source)
                    all_articles.extend(articles)

        # 过滤
        all_articles = self.filter_by_time(all_articles, days)
        if keyword:
            all_articles = self.filter_by_keyword(all_articles, keyword)

        # 按时间排序
        all_articles.sort(key=lambda x: x.get("timestamp", datetime.min), reverse=True)

        return all_articles


def format_output(articles: list, format_type: str = "markdown") -> str:
    """格式化输出"""
    if format_type == "json":
        # 转换时间对象为字符串
        for article in articles:
            if "timestamp" in article:
                article["timestamp"] = article["timestamp"].isoformat()
        return json.dumps(articles, ensure_ascii=False, indent=2)

    # Markdown 格式
    lines = ["# 新闻聚合结果\n"]
    lines.append(f"共 {len(articles)} 条新闻\n")
    lines.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for i, article in enumerate(articles, 1):
        lines.append(f"## {i}. {article['title']}\n")
        lines.append(f"**来源**: {article['source']}")
        if article.get("published"):
            lines.append(f" | **时间**: {article['published']}")
        lines.append(f"\n[阅读原文]({article['url']})\n")
        if article.get("summary"):
            summary = article["summary"][:200] + "..." if len(article["summary"]) > 200 else article["summary"]
            lines.append(f"> {summary}\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="新闻聚合工具")
    parser.add_argument("keyword", nargs="?", default="", help="搜索关键词")
    parser.add_argument("--days", "-d", type=int, default=7,
                       help="最近几天的新闻，默认 7 天")
    parser.add_argument("--sources", "-s", default="all",
                       help="新闻源分类（all/tech/finance/social）")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--format", "-f", choices=["json", "markdown"],
                       default="markdown", help="输出格式")
    parser.add_argument("--config", "-c", help="RSS 源配置文件路径")

    args = parser.parse_args()

    # 聚合新闻
    aggregator = NewsAggregator(config_path=args.config)
    articles = aggregator.aggregate(
        keyword=args.keyword,
        days=args.days,
        sources=args.sources
    )

    # 格式化输出
    output = format_output(articles, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"结果已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()