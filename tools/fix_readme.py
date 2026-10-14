# -*- coding: utf-8 -*-
import os

os.chdir(r"C:\Users\Administrator\Doubao\chats\2026-10-14\new-chat\legado-sources")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# 1. 修复书源表格分隔行
content = content.replace(
    "|------|------|--------|-------------------|",
    "|------|------|--------|---------------|-------------------|---------------------|"
)

# 2. 替换净化源部分
old_purge = """**Legado 净化源：**
```
https://raw.githubusercontent.com/Lcfyn/legado-sources/main/purgeSources/legado/all.json
```"""

purge_github = "https://raw.githubusercontent.com/Lcfyn/legado-sources/main/purgeSources/legado/all.json"
new_purge = f"""**Legado 净化源：**

| 类型 | GitHub | 镜像① wget.la | 镜像② gh-proxy.org | 镜像③ gh.catmak.name |
|------|--------|---------------|-------------------|---------------------|
| 净化源 | [导入]({purge_github}) | [导入](https://wget.la/{purge_github}) | [导入](https://gh-proxy.org/{purge_github}) | [导入](https://gh.catmak.name/{purge_github}) |"""

content = content.replace(old_purge, new_purge)

# 3. 替换替换规则部分
old_rules = """**Legado 替换规则（20条）：**
```
https://raw.githubusercontent.com/Lcfyn/legado-sources/main/rules/replace-rules.json
```"""

rules_github = "https://raw.githubusercontent.com/Lcfyn/legado-sources/main/rules/replace-rules.json"
new_rules = f"""**Legado 替换规则（20条）：**

| 类型 | GitHub | 镜像① wget.la | 镜像② gh-proxy.org | 镜像③ gh.catmak.name |
|------|--------|---------------|-------------------|---------------------|
| 替换规则 | [导入]({rules_github}) | [导入](https://wget.la/{rules_github}) | [导入](https://gh-proxy.org/{rules_github}) | [导入](https://gh.catmak.name/{rules_github}) |"""

content = content.replace(old_rules, new_rules)

# 4. 删除旧的Gitee推荐文字
content = content.replace("\n国内用户推荐使用 Gitee 加速链接。\n", "\n")

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README修复完成")
