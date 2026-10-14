# -*- coding: utf-8 -*-
import os

os.chdir(r"C:\Users\Administrator\Doubao\chats\2026-10-14\new-chat\legado-sources")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# 替换书源导入部分
old_section = """**Legado 书源（全量 6667+ 条）：**
```
https://raw.githubusercontent.com/Lcfyn/legado-sources/main/bookSources/legado/all.json
```

**Legado 净化源：**
```
https://raw.githubusercontent.com/Lcfyn/legado-sources/main/purgeSources/legado/all.json
```

> 书源涵盖文本小说、漫画、有声书等类型，已自动去重并校验格式。"""

new_section = """**Legado 书源（按类型分离，推荐）：**

| 类型 | 条数 | GitHub | Gitee（国内加速） |
|------|------|--------|-------------------|
| 小说 A-M | 3185 | [导入](https://raw.githubusercontent.com/Lcfyn/legado-sources/main/bookSources/legado/fiction-part1.json) | [导入](https://gitee.com/Lcfyn/legado-sources/raw/main/bookSources/legado/fiction-part1.json) |
| 小说 N-Z | 3185 | [导入](https://raw.githubusercontent.com/Lcfyn/legado-sources/main/bookSources/legado/fiction-part2.json) | [导入](https://gitee.com/Lcfyn/legado-sources/raw/main/bookSources/legado/fiction-part2.json) |
| 漫画 | 155 | [导入](https://raw.githubusercontent.com/Lcfyn/legado-sources/main/bookSources/legado/comics.json) | [导入](https://gitee.com/Lcfyn/legado-sources/raw/main/bookSources/legado/comics.json) |
| 有声书+其他 | 142 | [导入](https://raw.githubusercontent.com/Lcfyn/legado-sources/main/bookSources/legado/audio-other.json) | [导入](https://gitee.com/Lcfyn/legado-sources/raw/main/bookSources/legado/audio-other.json) |

**全量书源（6667+ 条，37MB，不推荐）：**
```
https://raw.githubusercontent.com/Lcfyn/legado-sources/main/bookSources/legado/all.json
```

**Legado 净化源：**
```
https://raw.githubusercontent.com/Lcfyn/legado-sources/main/purgeSources/legado/all.json
```

**Legado 替换规则（20条）：**
```
https://raw.githubusercontent.com/Lcfyn/legado-sources/main/rules/replace-rules.json
```

> 书源涵盖文本小说、漫画、有声书等类型，已自动去重并校验格式。替换规则需在 Legado「我的 → 替换规则」中导入。国内用户推荐使用 Gitee 加速链接。"""

if old_section in content:
    content = content.replace(old_section, new_section)
    print("书源导入部分已更新")
else:
    print("未找到旧的书源导入部分，尝试其他方式...")
    # 打印相关区域帮助调试
    idx = content.find("Legado 书源")
    if idx >= 0:
        print(repr(content[idx:idx+300]))

# 更新方式二本地导入的说明
old_local = "选择 `bookSources/legado/all.json`"
new_local = "选择 `bookSources/legado/` 下的 JSON 文件"
content = content.replace(old_local, new_local)

# 更新方式三
old_way3 = """### 方式三：按分类导入

如需按类型单独导入，可将 `all.json` 按 `bookSourceType` 字段筛选后导入。"""
new_way3 = """### 方式三：GitCode 镜像

也可使用 GitCode 镜像站导入：
```
https://gitcode.com/Lcfyn/legado-sources/-/raw/main/bookSources/legado/fiction-part1.json
```"""
content = content.replace(old_way3, new_way3)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README 更新完成")
