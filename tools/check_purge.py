# -*- coding: utf-8 -*-
import json
from urllib.request import Request, urlopen

url = "https://legado.aoaostar.com/sources/3f067eb2.json"
headers = {"User-Agent": "Mozilla/5.0"}
req = Request(url, headers=headers)
with urlopen(req, timeout=60) as resp:
    content = resp.read().decode("utf-8")

data = json.loads(content)
if isinstance(data, dict):
    for k in ("data", "sources", "list", "purgeSources"):
        if k in data and isinstance(data[k], list):
            data = data[k]
            break

print(f"总数: {len(data)}")
if data:
    print(f"第1条字段: {list(data[0].keys())}")
    print(f"第1条内容: {json.dumps(data[0], ensure_ascii=False)[:800]}")
    print()
    print(f"第2条字段: {list(data[1].keys()) if len(data)>1 else 'N/A'}")
