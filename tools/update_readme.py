# -*- coding: utf-8 -*-
import os

os.chdir(r"C:\Users\Administrator\Doubao\chats\2026-10-14\new-chat\legado-sources")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

old = "> 书源涵盖文本小说、漫画、有声书等类型，已自动去重并校验格式。替换规则需在 Legado「我的 → 替换规则」中导入。"

new = """> 书源涵盖文本小说、漫画、有声书等类型，已自动去重并校验格式。替换规则需在 Legado「我的 → 替换规则」中导入。

> **镜像源说明**：如果 wget.la 访问慢或不可用，可将链接前缀替换为以下任意一个：
> - `https://gh-proxy.org/https://raw.githubusercontent.com/...`
> - `https://gh.catmak.name/https://raw.githubusercontent.com/...`"""

if old in content:
    content = content.replace(old, new)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("已添加镜像源说明")
else:
    print("未找到目标文本，可能已更新过")
