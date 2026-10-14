#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""过滤无效书源，只保留有完整必填字段的。"""
import json
import os

INPUT = "bookSources/legado/all.json"

REQUIRED = ['bookSourceName', 'bookSourceUrl', 'searchUrl',
            'ruleSearch', 'ruleBookInfo', 'ruleToc', 'ruleContent']

def is_valid(item):
    if not isinstance(item, dict):
        return False
    for f in REQUIRED:
        if f not in item or not item[f]:
            return False
    # ruleSearch 需要有 bookList 或 list 字段
    rs = item.get('ruleSearch', {})
    if isinstance(rs, dict):
        if not any(k in rs for k in ('bookList', 'list', 'booklist')):
            return False
    # ruleContent 需要有 content 字段
    rc = item.get('ruleContent', {})
    if isinstance(rc, dict):
        if 'content' not in rc:
            return False
    return True

with open(INPUT, 'r', encoding='utf-8') as f:
    data = json.load(f)

valid = [item for item in data if is_valid(item)]
invalid = len(data) - len(valid)

print(f"原始: {len(data)} 条")
print(f"有效: {len(valid)} 条")
print(f"过滤: {invalid} 条 (缺少必填字段)")

# 按类型统计
type_count = {}
for s in valid:
    t = s.get('bookSourceType', 0)
    type_count[t] = type_count.get(t, 0) + 1
type_names = {0: '文本小说', 1: '音频', 2: '图片(漫画)', 3: '文件'}
for t, c in sorted(type_count.items()):
    print(f"  {type_names.get(t, f'类型{t}')}: {c} 条")

# 重新去重（按 bookSourceUrl + name）
seen = set()
deduped = []
for item in valid:
    url = str(item.get('bookSourceUrl', '')).strip().rstrip('/')
    name = str(item.get('bookSourceName', '')).strip()
    key = f"{url}|{name}"
    if key not in seen:
        seen.add(key)
        deduped.append(item)

print(f"\n去重后: {len(deduped)} 条 (移除 {len(valid) - len(deduped)} 条重复)")

# 输出 all.json
with open(INPUT, 'w', encoding='utf-8') as f:
    json.dump(deduped, f, ensure_ascii=False, indent=2)
print(f"已写入: {INPUT} ({os.path.getsize(INPUT):,} bytes)")

# 分类输出
output_dir = "bookSources/legado"
for type_id, type_name in [(0, 'fiction'), (2, 'comics'), (1, 'audiobooks')]:
    subset = [s for s in deduped if s.get('bookSourceType', 0) == type_id]
    if subset:
        path = os.path.join(output_dir, type_name, "merged.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(subset, f, ensure_ascii=False, indent=2)
        print(f"  {type_name}: {len(subset)} 条 -> {path}")
