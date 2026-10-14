#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从指定 URL 列表下载书源，校验、去重后合并输出。
用法: python3 tools/fetch_merge.py <url1> <url2> ... -o output.json
"""
import json
import sys
import os
import hashlib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

URLS = [
    "https://www.yck2026.fun/yuedu/shuyuans/json/id/1293.json",
    "https://www.yck2026.fun/yuedu/shuyuans/json/id/1304.json",
    "https://www.yck2026.fun/yuedu/shuyuans/json/id/1276.json",
    "https://www.yck2026.fun/yuedu/shuyuans/json/id/1254.json",
    "https://www.yck2026.fun/yuedu/shuyuans/json/id/1264.json",
    "https://www.yck2026.fun/yuedu/shuyuans/json/id/1240.json",
    "https://www.yck2026.fun/yuedu/shuyuans/json/id/1303.json",
]

def fetch(url, timeout=30):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json,*/*',
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        print(f"  [FAIL] {url}: {e}")
        return None

def parse_json(content):
    if not content:
        return None
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for k in ('data', 'sources', 'list', 'bookSources'):
                if k in data and isinstance(data[k], list):
                    return data[k]
        return None
    except json.JSONDecodeError:
        # 尝试提取数组部分
        start = content.find('[')
        end = content.rfind(']')
        if start >= 0 and end > start:
            try:
                data = json.loads(content[start:end+1])
                if isinstance(data, list):
                    return data
            except Exception:
                pass
        return None

def get_key(item):
    url = str(item.get('bookSourceUrl', '')).strip().rstrip('/')
    name = str(item.get('bookSourceName', '')).strip()
    return f"{url}|{name}"

def is_valid_book_source(item):
    if not isinstance(item, dict):
        return False
    required = ['bookSourceName', 'bookSourceUrl']
    for f in required:
        if f not in item or not item[f]:
            return False
    return True

def main():
    all_sources = []
    seen = set()
    stats = []

    for i, url in enumerate(URLS, 1):
        print(f"[{i}/{len(URLS)}] 下载: {url}")
        content = fetch(url)
        if content is None:
            stats.append((url, 0, 0, 0))
            continue

        items = parse_json(content)
        if items is None:
            print(f"  [FAIL] JSON 解析失败")
            stats.append((url, 0, 0, 0))
            continue

        raw_count = len(items)
        valid_count = 0
        added_count = 0
        dup_count = 0

        for item in items:
            if not is_valid_book_source(item):
                continue
            valid_count += 1
            key = get_key(item)
            if key in seen:
                dup_count += 1
                continue
            seen.add(key)
            all_sources.append(item)
            added_count += 1

        print(f"  [OK] 原始 {raw_count} 条，有效 {valid_count} 条，新增 {added_count} 条，重复 {dup_count} 条")
        stats.append((url, raw_count, valid_count, added_count))

    print()
    print(f"=== 合并完成 ===")
    print(f"总书源数: {len(all_sources)}")

    # 按类型统计
    type_count = {}
    for s in all_sources:
        t = s.get('bookSourceType', 0)
        type_name = {0: '文本小说', 1: '音频', 2: '图片(漫画)', 3: '文件'}.get(t, f'未知({t})')
        type_count[type_name] = type_count.get(type_name, 0) + 1
    for t, c in type_count.items():
        print(f"  {t}: {c} 条")

    # 输出
    output_dir = "bookSources/legado"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "all.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_sources, f, ensure_ascii=False, indent=2)
    print(f"\n已输出: {output_path} ({os.path.getsize(output_path):,} bytes)")

    # 同时按类型分类输出
    fiction = [s for s in all_sources if s.get('bookSourceType', 0) == 0]
    comics = [s for s in all_sources if s.get('bookSourceType', 0) == 2]
    audio = [s for s in all_sources if s.get('bookSourceType', 0) == 1]

    for name, data in [('fiction', fiction), ('comics', comics), ('audiobooks', audio)]:
        if data:
            path = os.path.join(output_dir, name, "merged.json")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  分类输出: {path} ({len(data)} 条)")

if __name__ == '__main__':
    main()
