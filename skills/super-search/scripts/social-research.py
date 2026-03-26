#!/usr/bin/env python3
"""
社交平台研究脚本

支持微博、知乎、小红书、豆瓣等平台的搜索和热点分析。
"""

import argparse
import json
import re
import time
from datetime import datetime
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

# 社交平台配置
PLATFORMS = {
    "weibo": {
        "name": "微博",
        "search_url": "https://s.weibo.com/weibo?q={query}",
        "hot_url": "https://s.weibo.com/top/summary",
        "requires_login": False,
    },
    "zhihu": {
        "name": "知乎",
        "search_url": "https://www.zhihu.com/search?type=content&q={query}",
        "hot_url": "https://www.zhihu.com/api/v3/feed/topstory/hot-list?limit=50",
        "requires_login": False,
    },
    "xiaohongshu": {
        "name": "小红书",
        "search_url": "https://www.xiaohongshu.com/search_result?keyword={query}",
        "hot_url": "https://www.xiaohongshu.com/explore",
        "requires_login": True,
    },
    "douban": {
        "name": "豆瓣",
        "search_url": "https://www.douban.com/search?q={query}",
        "hot_url": "https://www.douban.com/group/explore",
        "requires_login": False,
    },
}


class SocialResearcher:
    """社交平台研究器"""

    def __init__(self, cookies: dict = None):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        if cookies:
            self.session.cookies.update(cookies)

    def search_weibo(self, query: str, limit: int = 30) -> list:
        """搜索微博"""
        results = []

        try:
            url = PLATFORMS["weibo"]["search_url"].format(query=quote_plus(query))
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for card in soup.select("div.card-wrap")[:limit]:
                try:
                    # 提取微博内容
                    content_elem = card.select_one("p[node-type='feed_list_content']")
                    if not content_elem:
                        continue

                    content = content_elem.get_text(strip=True)

                    # 提取作者
                    author_elem = card.select_one("a.name")
                    author = author_elem.get_text(strip=True) if author_elem else "未知"

                    # 提取链接
                    link_elem = card.select_one("a[action-type='feed_list_item_date']")
                    link = f"https://weibo.com{link_elem['href']}" if link_elem else ""

                    # 提取互动数据
                    stats = {}
                    for stat in card.select("div.card-act li"):
                        text = stat.get_text(strip=True)
                        if "转发" in text:
                            stats["reposts"] = self._parse_count(text)
                        elif "评论" in text:
                            stats["comments"] = self._parse_count(text)
                        elif "赞" in text:
                            stats["likes"] = self._parse_count(text)

                    results.append({
                        "platform": "微博",
                        "author": author,
                        "content": content[:200] + "..." if len(content) > 200 else content,
                        "url": link,
                        "stats": stats,
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"微博搜索失败: {e}")

        return results

    def search_zhihu(self, query: str, limit: int = 30) -> list:
        """搜索知乎"""
        results = []

        try:
            url = PLATFORMS["zhihu"]["search_url"].format(query=quote_plus(query))
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.select("div.List-item")[:limit]:
                try:
                    # 提取标题
                    title_elem = item.select_one("h2.ContentItem-title a")
                    title = title_elem.get_text(strip=True) if title_elem else ""

                    # 提取链接
                    link = f"https://www.zhihu.com{title_elem['href']}" if title_elem else ""

                    # 提取摘要
                    excerpt_elem = item.select_one("div.RichContent-inner")
                    excerpt = excerpt_elem.get_text(strip=True)[:200] if excerpt_elem else ""

                    # 提取作者
                    author_elem = item.select_one("a.AuthorInfo-name")
                    author = author_elem.get_text(strip=True) if author_elem else "匿名"

                    # 提取互动数据
                    stats = {}
                    vote_elem = item.select_one("button.VoteButton--up")
                    if vote_elem:
                        stats["votes"] = self._parse_count(vote_elem.get_text(strip=True))

                    comment_elem = item.select_one("button.ContentItem-action button")
                    if comment_elem:
                        stats["comments"] = self._parse_count(comment_elem.get_text(strip=True))

                    results.append({
                        "platform": "知乎",
                        "author": author,
                        "title": title,
                        "content": excerpt,
                        "url": link,
                        "stats": stats,
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"知乎搜索失败: {e}")

        return results

    def get_weibo_hot(self, limit: int = 50) -> list:
        """获取微博热搜"""
        results = []

        try:
            url = PLATFORMS["weibo"]["hot_url"]
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.select("td.td-02")[:limit]:
                try:
                    link_elem = item.select_one("a")
                    if link_elem:
                        title = link_elem.get_text(strip=True)
                        link = f"https://s.weibo.com{link_elem['href']}"

                        # 热度值
                        hot_elem = item.select_one("span")
                        hot = hot_elem.get_text(strip=True) if hot_elem else ""

                        results.append({
                            "rank": len(results) + 1,
                            "title": title,
                            "url": link,
                            "hot": hot,
                        })

                except Exception:
                    continue

        except Exception as e:
            print(f"获取微博热搜失败: {e}")

        return results

    def get_zhihu_hot(self, limit: int = 50) -> list:
        """获取知乎热榜"""
        results = []

        try:
            url = PLATFORMS["zhihu"]["hot_url"]
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            for item in data.get("data", [])[:limit]:
                try:
                    target = item.get("target", {})
                    results.append({
                        "rank": len(results) + 1,
                        "title": target.get("title", ""),
                        "url": f"https://www.zhihu.com/question/{target.get('id', '')}",
                        "hot": item.get("detail_text", ""),
                        "excerpt": target.get("excerpt", ""),
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"获取知乎热榜失败: {e}")

        return results

    def _parse_count(self, text: str) -> int:
        """解析数量字符串"""
        text = text.strip()
        if "万" in text:
            return int(float(re.sub(r"[^0-9.]", "", text)) * 10000)
        elif "亿" in text:
            return int(float(re.sub(r"[^0-9.]", "", text)) * 100000000)
        else:
            nums = re.findall(r"\d+", text)
            return int(nums[0]) if nums else 0

    def research(
        self,
        keyword: str,
        platforms: list = None,
        limit: int = 30,
        sort: str = "relevant"
    ) -> dict:
        """综合研究"""
        if platforms is None:
            platforms = list(PLATFORMS.keys())

        results = {}

        for platform in platforms:
            if platform == "weibo":
                results["weibo"] = self.search_weibo(keyword, limit)
            elif platform == "zhihu":
                results["zhihu"] = self.search_zhihu(keyword, limit)
            elif platform == "xiaohongshu":
                print("小红书需要登录，暂时不支持")
                results["xiaohongshu"] = []
            elif platform == "douban":
                print("豆瓣搜索暂时不支持")
                results["douban"] = []

            time.sleep(1)  # 避免频率限制

        return results

    def get_hot(self, platforms: list = None, limit: int = 50) -> dict:
        """获取各平台热搜/热榜"""
        if platforms is None:
            platforms = ["weibo", "zhihu"]

        results = {}

        if "weibo" in platforms:
            results["weibo"] = self.get_weibo_hot(limit)
        if "zhihu" in platforms:
            results["zhihu"] = self.get_zhihu_hot(limit)

        return results


def format_output(results: dict, format_type: str = "markdown") -> str:
    """格式化输出"""
    if format_type == "json":
        return json.dumps(results, ensure_ascii=False, indent=2)

    lines = ["# 社交平台研究结果\n"]

    for platform, items in results.items():
        platform_name = PLATFORMS.get(platform, {}).get("name", platform)
        lines.append(f"## {platform_name} ({len(items)} 条)\n")

        for i, item in enumerate(items, 1):
            if "title" in item:
                lines.append(f"{i}. **{item['title']}**")
            else:
                lines.append(f"{i}. {item.get('author', '未知')}")
                if item.get("content"):
                    lines.append(f"   > {item['content'][:100]}...")

            if item.get("url"):
                lines.append(f"   [查看原文]({item['url']})")

            if item.get("stats"):
                stats = item["stats"]
                stats_str = " | ".join(f"{k}: {v}" for k, v in stats.items() if v)
                if stats_str:
                    lines.append(f"   📊 {stats_str}")

            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="社交平台研究工具")
    parser.add_argument("keyword", nargs="?", default="", help="搜索关键词")
    parser.add_argument("--platforms", "-p", default="all",
                       help="平台（weibo/zhihu/xiaohongshu/douban），逗号分隔")
    parser.add_argument("--limit", "-l", type=int, default=30,
                       help="每个平台最大结果数")
    parser.add_argument("--sort", "-s", choices=["time", "hot", "relevant"],
                       default="relevant", help="排序方式")
    parser.add_argument("--hot", action="store_true",
                       help="获取热搜/热榜")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--format", "-f", choices=["json", "markdown"],
                       default="markdown", help="输出格式")

    args = parser.parse_args()

    researcher = SocialResearcher()

    # 解析平台列表
    if args.platforms == "all":
        platforms = list(PLATFORMS.keys())
    else:
        platforms = [p.strip().lower() for p in args.platforms.split(",")]

    if args.hot:
        # 获取热搜
        results = researcher.get_hot(platforms)
    else:
        # 搜索
        if not args.keyword:
            print("请提供搜索关键词")
            return
        results = researcher.research(args.keyword, platforms, args.limit, args.sort)

    # 格式化输出
    output = format_output(results, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"结果已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()