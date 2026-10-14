# -*- coding: utf-8 -*-
import json, os

os.chdir(r"C:\Users\Administrator\Doubao\chats\2026-10-14\new-chat\legado-sources")

with open("bookSources/legado/all.json", "r", encoding="utf-8") as f:
    all_sources = json.load(f)

print(f"总书源: {len(all_sources)} 条")

# 按类型分类
fiction = [s for s in all_sources if s.get("bookSourceType", 0) == 0]
comics = [s for s in all_sources if s.get("bookSourceType", 0) == 2]
audio = [s for s in all_sources if s.get("bookSourceType", 0) == 1]
other = [s for s in all_sources if s.get("bookSourceType", 0) == 3]

print(f"文本小说: {len(fiction)} 条")
print(f"漫画: {len(comics)} 条")
print(f"有声书: {len(audio)} 条")
print(f"文件类: {len(other)} 条")

# 按分组统计小说
from collections import Counter
groups = Counter(s.get("bookSourceGroup", "未分组") for s in fiction)
print(f"\n小说分组数: {len(groups)}")
print("前20个分组:")
for g, c in groups.most_common(20):
    print(f"  {g}: {c} 条")

# 保存各类型文件
def save_file(data, filename):
    path = f"bookSources/legado/{filename}"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    size = os.path.getsize(path)
    print(f"  {filename}: {len(data)} 条, {size/1024/1024:.1f} MB")

print("\n生成文件:")
save_file(fiction, "fiction.json")
save_file(comics, "comics.json")
save_file(audio + other, "audio-other.json")

# 如果小说太大，按首字母分两个
if len(fiction) > 4000:
    # 按书源名称首字符分
    fiction_sorted = sorted(fiction, key=lambda x: x.get("bookSourceName", ""))
    mid = len(fiction_sorted) // 2
    fiction_a = fiction_sorted[:mid]
    fiction_b = fiction_sorted[mid:]
    print("\n小说进一步分割:")
    save_file(fiction_a, "fiction-part1.json")
    save_file(fiction_b, "fiction-part2.json")

print("\n完成!")
