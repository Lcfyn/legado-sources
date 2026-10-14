#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legado-sources 书源格式校验工具

用法:
    python3 validate.py <文件或目录路径>
    python3 validate.py bookSources/legado/fiction/
    python3 validate.py bookSources/legado/fiction/example.json

校验内容:
    - JSON 语法是否合法
    - 是否为数组格式
    - 每条书源的必填字段是否存在
    - 字段类型是否正确
    - URL 格式是否合理
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any

# 颜色输出
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Legado 书源必填字段及类型
LEGADO_REQUIRED_FIELDS = {
    'bookSourceName': str,
    'bookSourceUrl': str,
    'bookSourceType': int,
    'searchUrl': str,
    'ruleSearch': dict,
    'ruleBookInfo': dict,
    'ruleToc': dict,
    'ruleContent': dict,
}

# Legado 书源可选字段及类型
LEGADO_OPTIONAL_FIELDS = {
    'bookSourceGroup': str,
    'bookSourceComment': str,
    'enabled': bool,
    'enabledExplore': bool,
    'enabledCookieJar': bool,
    'exploreUrl': str,
    'lastUpdateTime': int,
    'customOrder': int,
    'variableComment': str,
}

# 有效的书源类型
VALID_SOURCE_TYPES = {0, 1, 2, 3}

# 净化源必填字段
PURGE_REQUIRED_FIELDS = {
    'sourceName': str,
    'url': str,
    'replaceRegex': list,
}

# 订阅源必填字段
SUBSCRIBE_REQUIRED_FIELDS = {
    'sourceName': str,
    'url': str,
}


def is_valid_url(url: str) -> bool:
    """简单的 URL 格式校验"""
    if not url or not isinstance(url, str):
        return False
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def detect_source_type(data: List[Dict]) -> str:
    """根据数据结构判断源类型"""
    if not data or not isinstance(data, list):
        return 'unknown'
    first = data[0]
    if not isinstance(first, dict):
        return 'unknown'
    if 'bookSourceName' in first:
        return 'legado_book'
    if 'sourceName' in first and 'replaceRegex' in first:
        return 'legado_purge'
    if 'sourceName' in first:
        return 'legado_subscribe'
    if 'name' in first and 'searchUrl' in first:
        return 'xiaomi_book'
    return 'unknown'


def validate_legado_book_source(item: Dict, index: int) -> List[str]:
    """校验单条 Legado 书源，返回错误列表"""
    errors = []
    warnings = []

    # 必填字段检查
    for field, expected_type in LEGADO_REQUIRED_FIELDS.items():
        if field not in item:
            errors.append(f"第 {index} 条: 缺少必填字段 '{field}'")
        elif not isinstance(item[field], expected_type):
            errors.append(
                f"第 {index} 条: 字段 '{field}' 类型错误，"
                f"期望 {expected_type.__name__}，实际 {type(item[field]).__name__}"
            )

    # 可选字段类型检查
    for field, expected_type in LEGADO_OPTIONAL_FIELDS.items():
        if field in item and not isinstance(item[field], expected_type):
            warnings.append(
                f"第 {index} 条: 字段 '{field}' 类型不匹配，"
                f"期望 {expected_type.__name__}，实际 {type(item[field]).__name__}"
            )

    # 书源类型检查
    if 'bookSourceType' in item and isinstance(item['bookSourceType'], int):
        if item['bookSourceType'] not in VALID_SOURCE_TYPES:
            errors.append(
                f"第 {index} 条: bookSourceType={item['bookSourceType']} 不在有效范围 {VALID_SOURCE_TYPES}"
            )

    # URL 格式检查
    if 'bookSourceUrl' in item and isinstance(item['bookSourceUrl'], str):
        if not is_valid_url(item['bookSourceUrl']):
            warnings.append(f"第 {index} 条: bookSourceUrl 格式可能不正确: {item['bookSourceUrl']}")

    # 子规则字段检查
    if 'ruleSearch' in item and isinstance(item['ruleSearch'], dict):
        if 'bookList' not in item['ruleSearch']:
            warnings.append(f"第 {index} 条: ruleSearch 缺少 'bookList' 字段")
    if 'ruleContent' in item and isinstance(item['ruleContent'], dict):
        if 'content' not in item['ruleContent']:
            warnings.append(f"第 {index} 条: ruleContent 缺少 'content' 字段")

    return errors, warnings


def validate_purge_source(item: Dict, index: int) -> Tuple[List[str], List[str]]:
    """校验单条净化源"""
    errors = []
    warnings = []

    for field, expected_type in PURGE_REQUIRED_FIELDS.items():
        if field not in item:
            errors.append(f"第 {index} 条: 缺少必填字段 '{field}'")
        elif not isinstance(item[field], expected_type):
            errors.append(
                f"第 {index} 条: 字段 '{field}' 类型错误，"
                f"期望 {expected_type.__name__}，实际 {type(item[field]).__name__}"
            )

    if 'replaceRegex' in item and isinstance(item['replaceRegex'], list):
        for i, rule in enumerate(item['replaceRegex']):
            if isinstance(rule, dict):
                if 'regex' not in rule:
                    errors.append(f"第 {index} 条: replaceRegex[{i}] 缺少 'regex' 字段")
            elif not isinstance(rule, str):
                errors.append(f"第 {index} 条: replaceRegex[{i}] 应为字符串或对象")

    return errors, warnings


def validate_subscribe_source(item: Dict, index: int) -> Tuple[List[str], List[str]]:
    """校验单条订阅源"""
    errors = []
    warnings = []

    for field, expected_type in SUBSCRIBE_REQUIRED_FIELDS.items():
        if field not in item:
            errors.append(f"第 {index} 条: 缺少必填字段 '{field}'")
        elif not isinstance(item[field], expected_type):
            errors.append(
                f"第 {index} 条: 字段 '{field}' 类型错误，"
                f"期望 {expected_type.__name__}，实际 {type(item[field]).__name__}"
            )

    return errors, warnings


def validate_file(filepath: str) -> Tuple[bool, int, List[str], List[str]]:
    """校验单个 JSON 文件，返回 (是否通过, 书源数量, 错误列表, 警告列表)"""
    all_errors = []
    all_warnings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, 0, [f"JSON 语法错误: {e}"], []
    except Exception as e:
        return False, 0, [f"文件读取失败: {e}"], []

    if not isinstance(data, list):
        return False, 0, ["文件根元素必须是 JSON 数组"], []

    if len(data) == 0:
        all_warnings.append("文件为空数组")
        return True, 0, all_errors, all_warnings

    source_type = detect_source_type(data)

    for i, item in enumerate(data, 1):
        if not isinstance(item, dict):
            all_errors.append(f"第 {i} 条: 不是 JSON 对象")
            continue

        if source_type == 'legado_book':
            errors, warnings = validate_legado_book_source(item, i)
        elif source_type == 'legado_purge':
            errors, warnings = validate_purge_source(item, i)
        elif source_type == 'legado_subscribe':
            errors, warnings = validate_subscribe_source(item, i)
        elif source_type == 'xiaomi_book':
            # 小米阅读格式校验较宽松
            errors, warnings = [], []
            if 'name' not in item:
                errors.append(f"第 {i} 条: 缺少 'name' 字段")
            if 'searchUrl' not in item:
                errors.append(f"第 {i} 条: 缺少 'searchUrl' 字段")
        else:
            warnings = [f"第 {i} 条: 无法识别的源格式，跳过详细校验"]
            errors = []

        all_errors.extend(errors)
        all_warnings.extend(warnings)

    return len(all_errors) == 0, len(data), all_errors, all_warnings


def collect_json_files(path: str) -> List[str]:
    """收集路径下所有 JSON 文件"""
    if os.path.isfile(path):
        return [path] if path.endswith('.json') else []

    json_files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.json') and not f.startswith('.'):
                json_files.append(os.path.join(root, f))
    return sorted(json_files)


def main():
    if len(sys.argv) < 2:
        print(f"{Colors.RED}用法: python3 validate.py <文件或目录路径>{Colors.RESET}")
        sys.exit(1)

    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"{Colors.RED}错误: 路径不存在 - {target}{Colors.RESET}")
        sys.exit(1)

    json_files = collect_json_files(target)
    if not json_files:
        print(f"{Colors.YELLOW}未找到任何 JSON 文件{Colors.RESET}")
        sys.exit(0)

    print(f"{Colors.BOLD}{Colors.CYAN}=== legado-sources 书源校验 ==={Colors.RESET}")
    print(f"校验目标: {target}")
    print(f"发现文件: {len(json_files)} 个")
    print()

    total_files = 0
    total_sources = 0
    passed_files = 0
    failed_files = 0
    total_errors = 0
    total_warnings = 0

    for filepath in json_files:
        rel_path = os.path.relpath(filepath, target) if os.path.isdir(target) else filepath
        passed, count, errors, warnings = validate_file(filepath)

        total_files += 1
        total_sources += count

        if passed:
            passed_files += 1
            status = f"{Colors.GREEN}[OK]  {Colors.RESET}"
        else:
            failed_files += 1
            status = f"{Colors.RED}[FAIL]{Colors.RESET}"

        print(f"{status} {rel_path} ({count} 条源)")

        for err in errors:
            print(f"       {Colors.RED}✗ {err}{Colors.RESET}")
            total_errors += 1
        for warn in warnings:
            print(f"       {Colors.YELLOW}⚠ {warn}{Colors.RESET}")
            total_warnings += 1

    print()
    print(f"{Colors.BOLD}=== 校验结果汇总 ==={Colors.RESET}")
    print(f"文件总数:   {total_files}")
    print(f"书源总数:   {total_sources}")
    print(f"通过文件:   {Colors.GREEN}{passed_files}{Colors.RESET}")
    print(f"失败文件:   {Colors.RED if failed_files else ''}{failed_files}{Colors.RESET}")
    print(f"错误总数:   {Colors.RED if total_errors else ''}{total_errors}{Colors.RESET}")
    print(f"警告总数:   {Colors.YELLOW if total_warnings else ''}{total_warnings}{Colors.RESET}")
    print()

    if failed_files > 0:
        print(f"{Colors.RED}校验未通过，请修复上述错误后再提交。{Colors.RESET}")
        sys.exit(1)
    else:
        print(f"{Colors.GREEN}全部文件校验通过！{Colors.RESET}")
        if total_warnings > 0:
            print(f"{Colors.YELLOW}（有 {total_warnings} 条警告，建议检查但不阻塞提交）{Colors.RESET}")
        sys.exit(0)


if __name__ == '__main__':
    main()
