#!/usr/bin/env python3
"""
多搜索引擎整合搜索脚本

支持 Google、Bing、DuckDuckGo、百度、搜狗等多个搜索引擎，
可同时搜索并合并去重结果。
"""

import argparse
import json
import time
from datetime import datetime
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

# 搜索引擎配置
ENGINES = {
    "google": {
        "name": "Google",
        "search_url": "https://www.google.com/search?q={query}&num={num}",
        "result_selector": "div.g",
        "title_selector": "h3",
        "link_selector": "a",
        "snippet_selector": "div[data-sncf]",
        "requires_proxy": True,
    },
    "bing": {
        "name": "Bing",
        "search_url": "https://www.bing.com/search?q={query}&count={num}",
        "result_selector": "li.b_algo",
        "title_selector": "h2",
        "link_selector": "a",
        "snippet_selector": "p",
        "requires_proxy": False,
    },
    "duckduckgo": {
        "name": "DuckDuckGo",
        "search_url": "https://html.duckduckgo.com/html/?q={query}",
        "result_selector": "div.result",
        "title_selector": "a.result__a",
        "link_selector": "a.result__a",
        "snippet_selector": "a.result__snippet",
        "requires_proxy": False,
    },
    "baidu": {
        "name": "百度",
        "search_url": "https://www.baidu.com/s?wd={query}&rn={num}",
        "result_selector": "div.result",
        "title_selector": "h3",
        "link_selector": "a",
        "snippet_selector": "div.c-abstract",
        "requires_proxy": False,
    },
    "sogou": {
        "name": "搜狗",
        "search_url": "https://www.sogou.com/web?query={query}&num={num}",
        "result_selector": "div.vrwrap",
        "title_selector": "h3",
        "link_selector": "a",
        "snippet_selector": "p.str-text-info",
        "requires_proxy": False,
    },
}


class MultiSearcher:
    """多搜索引擎整合器"""

    def __init__(self, proxy=None, timeout=10):
        self.proxy = proxy
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def search_engine(self, engine_name: str, query: str, max_results: int = 10) -> list:
        """使用单个搜索引擎搜索"""
        if engine_name not in ENGINES:
            print(f"未知的搜索引擎: {engine_name}")
            return []

        engine = ENGINES[engine_name]
        results = []

        try:
            url = engine["search_url"].format(
                query=quote_plus(query),
                num=max_results
            )

            proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None

            response = self.session.get(
                url,
                proxies=proxies,
                timeout=self.timeout
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.select(engine["result_selector"])[:max_results]:
                try:
                    title_elem = item.select_one(engine["title_selector"])
                    link_elem = item.select_one(engine["link_selector"])
                    snippet_elem = item.select_one(engine["snippet_selector"])

                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem.get("href", "")
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                        if title and link:
                            results.append({
                                "title": title,
                                "url": link,
                                "snippet": snippet,
                                "engine": engine["name"],
                            })
                except Exception:
                    continue

        except Exception as e:
            print(f"{engine['name']} 搜索失败: {e}")

        return results

    def search_all(
        self,
        query: str,
        engines: list = None,
        max_results: int = 10,
        delay: float = 1.0
    ) -> dict:
        """使用所有指定的搜索引擎搜索"""
        if engines is None:
            engines = list(ENGINES.keys())

        all_results = {}

        for engine in engines:
            print(f"正在搜索 {ENGINES.get(engine, {}).get('name', engine)}...")
            results = self.search_engine(engine, query, max_results)
            all_results[engine] = results

            # 避免频率限制
            if engine != engines[-1]:
                time.sleep(delay)

        return all_results

    def merge_and_deduplicate(self, results: dict) -> list:
        """合并并去重结果"""
        seen_urls = set()
        merged = []

        for engine, items in results.items():
            for item in items:
                url = item.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    merged.append(item)

        return merged


def format_markdown(query: str, results: dict) -> str:
    """格式化为 Markdown"""
    lines = [f"# 搜索结果：{query}\n"]
    lines.append(f"搜索时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for engine, items in results.items():
        engine_name = ENGINES.get(engine, {}).get("name", engine)
        lines.append(f"## {engine_name} ({len(items)} 条)\n")

        for i, item in enumerate(items, 1):
            lines.append(f"{i}. [{item['title']}]({item['url']})")
            if item.get("snippet"):
                lines.append(f"   > {item['snippet'][:100]}...")
            lines.append("")

    return "\n".join(lines)


def format_table(query: str, results: dict) -> str:
    """格式化为表格"""
    lines = [f"# 搜索结果：{query}\n"]
    lines.append("| 序号 | 标题 | 来源 |")
    lines.append("|------|------|------|")

    count = 1
    for engine, items in results.items():
        for item in items:
            title = item["title"][:30] + "..." if len(item["title"]) > 30 else item["title"]
            lines.append(f"| {count} | [{title}]({item['url']}) | {item['engine']} |")
            count += 1

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="多搜索引擎整合搜索")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--engines", "-e", default="all",
                       help="搜索引擎，逗号分隔，默认 all")
    parser.add_argument("--max-results", "-n", type=int, default=10,
                       help="每个引擎最大结果数")
    parser.add_argument("--output", "-o", choices=["json", "markdown", "table"],
                       default="markdown", help="输出格式")
    parser.add_argument("--proxy", "-p", help="代理地址")
    parser.add_argument("--merge", "-m", action="store_true",
                       help="合并去重结果")

    args = parser.parse_args()

    # 解析引擎列表
    if args.engines == "all":
        engines = list(ENGINES.keys())
    else:
        engines = [e.strip().lower() for e in args.engines.split(",")]

    # 执行搜索
    searcher = MultiSearcher(proxy=args.proxy)
    results = searcher.search_all(args.query, engines, args.max_results)

    # 输出结果
    if args.output == "json":
        output = json.dumps({
            "query": args.query,
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, ensure_ascii=False, indent=2)
    elif args.output == "table":
        output = format_table(args.query, results)
    else:
        output = format_markdown(args.query, results)

    print(output)

    if args.merge:
        merged = searcher.merge_and_deduplicate(results)
        print(f"\n--- 合并去重后共 {len(merged)} 条结果 ---")


if __name__ == "__main__":
    main()