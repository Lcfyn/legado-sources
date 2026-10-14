# -*- coding: utf-8 -*-
import json, os
from urllib.request import Request, urlopen

os.chdir(r"C:\Users\Administrator\Doubao\chats\2026-10-14\new-chat\legado-sources")

url = "https://legado.aoaostar.com/sources/2a1f129b.json"
print(f"下载: {url}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json,*/*",
}

req = Request(url, headers=headers)
with urlopen(req, timeout=60) as resp:
    content = resp.read().decode("utf-8")

try:
    new_sources = json.loads(content)
    if isinstance(new_sources, dict):
        for k in ("data", "sources", "list", "bookSources"):
            if k in new_sources and isinstance(new_sources[k], list):
                new_sources = new_sources[k]
                break
except Exception:
    start = content.find("[")
    end = content.rfind("]")
    new_sources = json.loads(content[start:end+1])

print(f"下载到: {len(new_sources)} 条")

# 读取现有
with open("bookSources/legado/all.json", "r", encoding="utf-8") as f:
    existing = json.load(f)
print(f"现有: {len(existing)} 条")

def get_key(item):
    u = str(item.get("bookSourceUrl", "")).strip().rstrip("/")
    n = str(item.get("bookSourceName", "")).strip()
    return f"{u}|{n}"

existing_keys = {get_key(s) for s in existing}
added = 0
dup = 0
for s in new_sources:
    if not isinstance(s, dict):
        continue
    if "bookSourceName" not in s or "bookSourceUrl" not in s:
        continue
    key = get_key(s)
    if key in existing_keys:
        dup += 1
        continue
    existing_keys.add(key)
    existing.append(s)
    added += 1

print(f"新增: {added} 条，重复: {dup} 条")
print(f"合并后: {len(existing)} 条")

# 过滤无效
REQUIRED = ["bookSourceName", "bookSourceUrl", "searchUrl", "ruleSearch", "ruleBookInfo", "ruleToc", "ruleContent"]
def is_valid(item):
    for f in REQUIRED:
        if f not in item or not item[f]:
            return False
    rs = item.get("ruleSearch", {})
    if isinstance(rs, dict) and not any(k in rs for k in ("bookList", "list", "booklist")):
        return False
    rc = item.get("ruleContent", {})
    if isinstance(rc, dict) and "content" not in rc:
        return False
    if item.get("bookSourceType", 0) not in (0, 1, 2, 3):
        return False
    return True

valid = [s for s in existing if is_valid(s)]
print(f"过滤无效后: {len(valid)} 条 (移除 {len(existing)-len(valid)})")

with open("bookSources/legado/all.json", "w", encoding="utf-8") as f:
    json.dump(valid, f, ensure_ascii=False, indent=2)
size = os.path.getsize("bookSources/legado/all.json")
print(f"已写入 all.json ({size:,} bytes, {size/1024/1024:.1f} MB)")

from collections import Counter
types = Counter(s.get("bookSourceType", 0) for s in valid)
names = {0: "文本小说", 1: "音频", 2: "漫画", 3: "文件"}
for t, c in sorted(types.items()):
    print(f"  {names.get(t, t)}: {c} 条")
