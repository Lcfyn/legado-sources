# -*- coding: utf-8 -*-
import json, os
from urllib.request import Request, urlopen

os.chdir(r"C:\Users\Administrator\Doubao\chats\2026-10-14\new-chat\legado-sources")

url = "https://legado.aoaostar.com/sources/3f067eb2.json"
print(f"下载净化规则: {url}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json,*/*",
}

req = Request(url, headers=headers)
with urlopen(req, timeout=60) as resp:
    content = resp.read().decode("utf-8")

try:
    new_purges = json.loads(content)
    if isinstance(new_purges, dict):
        for k in ("data", "sources", "list", "purgeSources"):
            if k in new_purges and isinstance(new_purges[k], list):
                new_purges = new_purges[k]
                break
except Exception:
    start = content.find("[")
    end = content.rfind("]")
    new_purges = json.loads(content[start:end+1])

print(f"下载到: {len(new_purges)} 条净化规则")

# 读取现有净化源
with open("purgeSources/legado/all.json", "r", encoding="utf-8") as f:
    existing = json.load(f)
print(f"现有: {len(existing)} 条")

def get_key(item):
    name = str(item.get("sourceName", "")).strip()
    url_val = str(item.get("url", "")).strip()
    return f"{name}|{url_val}"

existing_keys = {get_key(s) for s in existing}
added = 0
dup = 0
for s in new_purges:
    if not isinstance(s, dict):
        continue
    if "sourceName" not in s:
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

# 写入
with open("purgeSources/legado/all.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)
size = os.path.getsize("purgeSources/legado/all.json")
print(f"已写入 all.json ({size:,} bytes)")

# 列出前几条名称
print("\n净化规则列表:")
for i, s in enumerate(existing[:10], 1):
    print(f"  {i}. {s.get('sourceName', '未知')}")
if len(existing) > 10:
    print(f"  ... 共 {len(existing)} 条")
