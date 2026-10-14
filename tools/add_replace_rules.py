# -*- coding: utf-8 -*-
import json, os
from urllib.request import Request, urlopen

os.chdir(r"C:\Users\Administrator\Doubao\chats\2026-10-14\new-chat\legado-sources")

url = "https://legado.aoaostar.com/sources/3f067eb2.json"
headers = {"User-Agent": "Mozilla/5.0"}
req = Request(url, headers=headers)
with urlopen(req, timeout=60) as resp:
    content = resp.read().decode("utf-8")

data = json.loads(content)
if isinstance(data, dict):
    for k in ("data", "sources", "list"):
        if k in data and isinstance(data[k], list):
            data = data[k]
            break

print(f"下载到 {len(data)} 条替换规则")

# 按 group 分类
groups = {}
for item in data:
    g = item.get("group", "未分类")
    if g not in groups:
        groups[g] = []
    groups[g].append(item)

print("分类统计:")
for g, items in groups.items():
    print(f"  {g}: {len(items)} 条")

# 保存全量替换规则
os.makedirs("rules", exist_ok=True)
with open("rules/replace-rules.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
size = os.path.getsize("rules/replace-rules.json")
print(f"\n已保存: rules/replace-rules.json ({size:,} bytes)")

# 同时尝试转换成净化源格式（把所有规则合并成一个净化源）
purge_source = {
    "sourceName": "aoaostar 通用净化规则",
    "sourceGroup": "通用规则",
    "enabled": True,
    "url": ".*",
    "replaceRegex": [],
    "comment": f"从 aoaostar 3f067eb2 转换，共 {len(data)} 条替换规则",
    "lastUpdateTime": int(__import__("time").time() * 1000)
}

for item in data:
    if not item.get("isEnabled", True):
        continue
    pattern = item.get("pattern", "")
    replacement = item.get("replacement", "")
    if not pattern:
        continue
    # 替换规则中的 @js: 前缀需要特殊处理，这里简化为普通正则
    if replacement.startswith("@js:"):
        # JS 替换规则无法直接转为正则，跳过
        continue
    purge_source["replaceRegex"].append({
        "regex": pattern,
        "replacement": replacement
    })

print(f"转换为净化源: {len(purge_source['replaceRegex'])} 条正则规则 (跳过JS规则)")

# 读取现有净化源并合并
with open("purgeSources/legado/all.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

# 检查是否已存在同名净化源
exists = any(s.get("sourceName") == purge_source["sourceName"] for s in existing)
if not exists:
    existing.append(purge_source)
    print(f"已添加净化源: {purge_source['sourceName']}")
else:
    print(f"净化源已存在，跳过")

with open("purgeSources/legado/all.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"\n净化源总数: {len(existing)} 条")
for s in existing:
    print(f"  - {s.get('sourceName', '未知')}")
