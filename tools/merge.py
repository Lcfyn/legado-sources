#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legado-sources 书源合并工具

将目录下所有 JSON 书源文件合并为单个文件，便于批量导入阅读 APP。

用法:
    python3 merge.py <输入目录> -o <输出文件>
    python3 merge.py bookSources/legado/ -o bookSources/legado/all.json
    python3 merge.py bookSources/legado/ -o all.json --pretty --dedup

选项:
    -o, --output    输出文件路径（默认: merged.json）
    --pretty        格式化输出（缩进 2 空格）
    --dedup         按关键字段去重
    --quiet         静默模式，不输出详细信息
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def collect_json_files(directory: str) -> List[str]:
    """收集目录下所有 JSON 文件（排除 all.json 和 merged 开头的文件）"""
    json_files = []
    for root, dirs, files in os.walk(directory):
        for f in sorted(files):
            if f.endswith('.json') and not f.startswith('.'):
                # 排除合并产物自身，避免循环
                if f in ('all.json', 'merged.json') or f.startswith('merged_'):
                    continue
                json_files.append(os.path.join(root, f))
    return sorted(json_files)


def load_json_file(filepath: str) -> List[Dict]:
    """加载单个 JSON 文件，返回列表"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            print(f"  {Colors.YELLOW}⚠ 跳过 {filepath}: 根元素不是数组{Colors.RESET}")
            return []
    except json.JSONDecodeError as e:
        print(f"  {Colors.RED}✗ 跳过 {filepath}: JSON 语法错误 - {e}{Colors.RESET}")
        return []
    except Exception as e:
        print(f"  {Colors.RED}✗ 跳过 {filepath}: 读取失败 - {e}{Colors.RESET}")
        return []


def get_dedup_key(item: Dict) -> str:
    """获取去重关键字"""
    # Legado 书源
    if 'bookSourceUrl' in item:
        return f"book:{item.get('bookSourceUrl', '')}"
    # 净化源 / 订阅源
    if 'url' in item and 'sourceName' in item:
        return f"source:{item.get('sourceName', '')}:{item.get('url', '')}"
    # 小米阅读
    if 'url' in item and 'name' in item:
        return f"xiaomi:{item.get('name', '')}:{item.get('url', '')}"
    # 兜底
    return json.dumps(item, sort_keys=True, ensure_ascii=False)


def merge_sources(
    input_dir: str,
    output_file: str,
    pretty: bool = False,
    dedup: bool = False,
    quiet: bool = False
) -> Dict[str, Any]:
    """执行合并操作，返回统计信息"""
    json_files = collect_json_files(input_dir)

    if not json_files:
        print(f"{Colors.RED}错误: 目录下未找到 JSON 文件 - {input_dir}{Colors.RESET}")
        sys.exit(1)

    if not quiet:
        print(f"{Colors.BOLD}{Colors.CYAN}=== 书源合并 ==={Colors.RESET}")
        print(f"输入目录: {input_dir}")
        print(f"输出文件: {output_file}")
        print(f"发现文件: {len(json_files)} 个")
        print(f"去重: {'开启' if dedup else '关闭'}")
        print()

    all_sources = []
    file_stats = []
    seen_keys = set()
    duplicate_count = 0

    for filepath in json_files:
        rel_path = os.path.relpath(filepath, input_dir)
        sources = load_json_file(filepath)
        file_stats.append((rel_path, len(sources)))

        if not quiet and sources:
            print(f"  {Colors.GREEN}✓{Colors.RESET} {rel_path} ({len(sources)} 条)")

        for item in sources:
            if not isinstance(item, dict):
                continue

            if dedup:
                key = get_dedup_key(item)
                if key in seen_keys:
                    duplicate_count += 1
                    continue
                seen_keys.add(key)

            all_sources.append(item)

    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 写入输出文件
    indent = 2 if pretty else None
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_sources, f, ensure_ascii=False, indent=indent)

    stats = {
        'input_files': len(json_files),
        'total_sources': sum(c for _, c in file_stats),
        'output_sources': len(all_sources),
        'duplicates_removed': duplicate_count,
        'output_file': output_file,
        'file_stats': file_stats,
    }

    if not quiet:
        print()
        print(f"{Colors.BOLD}=== 合并完成 ==={Colors.RESET}")
        print(f"输入文件数:   {stats['input_files']}")
        print(f"原始源总数:   {stats['total_sources']}")
        if dedup:
            print(f"移除重复:     {Colors.YELLOW}{duplicate_count}{Colors.RESET}")
        print(f"输出源总数:   {Colors.GREEN}{stats['output_sources']}{Colors.RESET}")
        print(f"输出文件:     {output_file}")
        print(f"文件大小:     {os.path.getsize(output_file):,} bytes")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='legado-sources 书源合并工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 merge.py bookSources/legado/ -o all.json
  python3 merge.py bookSources/legado/ -o all.json --pretty --dedup
  python3 merge.py purgeSources/legado/ -o purge-all.json --dedup
        """
    )
    parser.add_argument('input_dir', help='输入目录路径')
    parser.add_argument('-o', '--output', default='merged.json', help='输出文件路径 (默认: merged.json)')
    parser.add_argument('--pretty', action='store_true', help='格式化输出（缩进 2 空格）')
    parser.add_argument('--dedup', action='store_true', help='按关键字段去重')
    parser.add_argument('--quiet', action='store_true', help='静默模式')

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"{Colors.RED}错误: 输入路径不是目录 - {args.input_dir}{Colors.RESET}")
        sys.exit(1)

    merge_sources(
        input_dir=args.input_dir,
        output_file=args.output,
        pretty=args.pretty,
        dedup=args.dedup,
        quiet=args.quiet,
    )


if __name__ == '__main__':
    main()
