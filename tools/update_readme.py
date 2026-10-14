# -*- coding: utf-8 -*-
import os, re

os.chdir(r"C:\Users\Administrator\Doubao\chats\2026-10-14\new-chat\legado-sources")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# 定义文件路径映射
files = {
    "fiction-part1": "bookSources/legado/fiction-part1.json",
    "fiction-part2": "bookSources/legado/fiction-part2.json",
    "comics": "bookSources/legado/comics.json",
    "audio-other": "bookSources/legado/audio-other.json",
}

# 书源表格 - 替换为三镜像列
old_table_header = "| 类型 | 条数 | GitHub | 镜像加速（国内可用） |"
new_table_header = "| 类型 | 条数 | GitHub | 镜像① wget.la | 镜像② gh-proxy.org | 镜像③ gh.catmak.name |"

old_table_sep = "|------|------|--------|---------------------|"
new_table_sep = "|------|------|--------|---------------|-------------------|---------------------|"

content = content.replace(old_table_header, new_table_header)
content = content.replace(old_table_sep, new_table_sep)

# 替换每一行的镜像链接为三个镜像链接
for key, path in files.items():
    github_url = f"https://raw.githubusercontent.com/Lcfyn/legado-sources/main/{path}"
    wget_url = f"https://wget.la/{github_url}"
    ghproxy_url = f"https://gh-proxy.org/{github_url}"
    catmak_url = f"https://gh.catmak.name/{github_url}"
    
    # 匹配当前行（包含wget.la链接的行）
    # 格式: | 小说 A-M | 3185 | [导入](github) | [导入](wget.la) |
    pattern = re.compile(
        r'(\| [^|]+ \| \d+ \| \[导入\]\(' + re.escape(github_url) + r'\) \|) \[导入\]\(' + re.escape(wget_url) + r'\) \|'
    )
    replacement = rf'\1 [导入]({wget_url}) | [导入]({ghproxy_url}) | [导入]({catmak_url}) |'
    content = pattern.sub(replacement, content)

# 净化源表格
old_purge_header = "| 平台 | 导入地址 |"
new_purge_header = "| 类型 | GitHub | 镜像① wget.la | 镜像② gh-proxy.org | 镜像③ gh.catmak.name |"
old_purge_sep = "|------|---------|"
new_purge_sep = "|------|--------|---------------|-------------------|---------------------|"

content = content.replace(old_purge_header, new_purge_header)
content = content.replace(old_purge_sep, new_purge_sep)

# 净化源行
purge_github = "https://raw.githubusercontent.com/Lcfyn/legado-sources/main/purgeSources/legado/all.json"
purge_wget = f"https://wget.la/{purge_github}"
purge_ghproxy = f"https://gh-proxy.org/{purge_github}"
purge_catmak = f"https://gh.catmak.name/{purge_github}"

old_purge_row = f"| GitHub | [导入]({purge_github}) |\n| Gitee（国内加速） | [导入]({purge_wget}) |"
# 实际可能是不同的格式，让我用更灵活的方式
content = content.replace(
    f"| GitHub | [导入]({purge_github}) |",
    f"| 净化源 | [导入]({purge_github}) | [导入]({purge_wget}) | [导入]({purge_ghproxy}) | [导入]({purge_catmak}) |"
)
# 删除Gitee那一行
content = content.replace(f"\n| 镜像加速（国内可用） | [导入]({purge_wget}) |", "")
content = content.replace(f"\n| Gitee（国内加速） | [导入]({purge_wget}) |", "")

# 替换规则行
rules_github = "https://raw.githubusercontent.com/Lcfyn/legado-sources/main/rules/replace-rules.json"
rules_wget = f"https://wget.la/{rules_github}"
rules_ghproxy = f"https://gh-proxy.org/{rules_github}"
rules_catmak = f"https://gh.catmak.name/{rules_github}"

content = content.replace(
    f"| GitHub | [导入]({rules_github}) |",
    f"| 替换规则 | [导入]({rules_github}) | [导入]({rules_wget}) | [导入]({rules_ghproxy}) | [导入]({rules_catmak}) |"
)
content = content.replace(f"\n| 镜像加速（国内可用） | [导入]({rules_wget}) |", "")
content = content.replace(f"\n| Gitee（国内加速） | [导入]({rules_wget}) |", "")

# 删除之前的镜像源说明（因为已经直接列在表格里了）
old_note = """> **镜像源说明**：如果 wget.la 访问慢或不可用，可将链接前缀替换为以下任意一个：
> - `https://gh-proxy.org/https://raw.githubusercontent.com/...`
> - `https://gh.catmak.name/https://raw.githubusercontent.com/...`"""
content = content.replace(old_note, "")

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README已更新，三个镜像源已添加到表格中")
