# legado-sources

全网阅读 APP 书源、净化源、订阅源聚合仓库。持续收集、整理、校验各类阅读资源配置，支持 Legado（阅读）、小米阅读及更多主流阅读 APP。

> ⚠️ **免责声明**：本仓库仅收集和整理第三方公开的阅读源配置文件，不存储任何书籍内容。所有书源均指向互联网公开网站，版权归原网站及作者所有。如有侵权请提交 Issue，我们将在 24 小时内移除相关内容。请支持正版阅读。

---

## 📋 目录

- [支持的 APP](#支持的-app)
- [目录结构](#目录结构)
- [快速开始](#快速开始)
- [书源格式说明](#书源格式说明)
- [工具使用](#工具使用)
- [贡献指南](#贡献指南)
- [常见问题](#常见问题)
- [免责声明](#免责声明)

---

## 支持的 APP

| APP | 书源 | 净化源 | 订阅源 | 格式 |
|-----|------|--------|--------|------|
| **Legado / 阅读** (3.0+) | ✅ | ✅ | ✅ | JSON |
| **小米阅读** | ✅ | ✅ | ❌ | JSON |
| **其他 APP** | 🔄 | 🔄 | ❌ | 见各子目录 |

> 🔄 = 持续补充中，欢迎 PR 贡献

---

## 目录结构

```
legado-sources/
├── bookSources/              # 书源
│   ├── legado/               #   Legado 格式
│   │   ├── fiction/          #     小说类
│   │   ├── comics/           #     漫画类
│   │   └── audiobooks/       #     有声书类
│   ├── xiaomi/               #   小米阅读格式
│   └── other/                #   其他 APP 格式
├── purgeSources/             # 净化源（广告过滤规则）
│   ├── legado/
│   └── xiaomi/
├── subscribeSources/         # 订阅源 / 发现源
│   ├── legado/
│   └── xiaomi/
├── rules/                    # 替换规则、正文净化规则
├── templates/                # 各格式模板文件
├── tools/                    # 工具脚本
│   ├── validate.py           #   书源格式校验
│   └── merge.py              #   多文件合并
├── docs/                     # 文档
│   ├── contribution.md       #   贡献指南
│   └── format-spec.md        #   格式规范详解
├── LICENSE
├── .gitignore
└── README.md
```

---

## 快速开始

### 方式一：网络导入（推荐）

将以下链接复制到阅读 APP 的「网络导入」中：

**Legado 书源（全量）：**
```
https://raw.githubusercontent.com/你的用户名/legado-sources/main/bookSources/legado/all.json
```

**Legado 净化源：**
```
https://raw.githubusercontent.com/你的用户名/legado-sources/main/purgeSources/legado/all.json
```

> 推送至 GitHub 后，将 `你的用户名` 替换为实际的 GitHub 用户名。

### 方式二：本地导入

1. 下载本仓库（`git clone` 或下载 ZIP）
2. 打开阅读 APP → 我的 → 书源管理
3. 点击右上角「导入」→ 选择本地 JSON 文件
4. 导入完成后启用需要的书源

### 方式三：订阅源自动更新

1. 复制订阅源链接
2. 阅读 APP → 我的 → 订阅源 → 添加
3. 开启自动更新，书源将定期同步最新版本

---

## 书源格式说明

### Legado 书源字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookSourceName` | string | ✅ | 书源名称 |
| `bookSourceGroup` | string | ❌ | 书源分组 |
| `bookSourceUrl` | string | ✅ | 书源主页 URL |
| `bookSourceType` | int | ✅ | 0=文本, 1=音频, 2=图片, 3=文件 |
| `bookSourceComment` | string | ❌ | 书源备注 |
| `enabled` | boolean | ❌ | 是否启用，默认 true |
| `enabledExplore` | boolean | ❌ | 是否启用发现页 |
| `enabledCookieJar` | boolean | ❌ | 是否启用 Cookie |
| `searchUrl` | string | ✅ | 搜索 URL 规则 |
| `ruleSearch` | object | ✅ | 搜索结果解析规则 |
| `ruleBookInfo` | object | ✅ | 书籍详情解析规则 |
| `ruleToc` | object | ✅ | 目录解析规则 |
| `ruleContent` | object | ✅ | 正文解析规则 |
| `lastUpdateTime` | long | ❌ | 最后更新时间戳 |

完整字段说明请参考 [docs/format-spec.md](docs/format-spec.md)。

### 小米阅读书源字段

小米阅读使用简化版 JSON 格式，模板见 `templates/xiaomi-book-source.json`。

---

## 工具使用

### 书源校验

校验指定目录下所有 JSON 文件的格式是否合法：

```bash
python3 tools/validate.py bookSources/legado/fiction/
```

输出示例：
```
[OK]   biquge.json (12 条书源)
[FAIL] example.json: 第 3 条缺少 bookSourceUrl 字段
[WARN] test.json: 第 1 条 bookSourceType 不在有效范围
```

### 书源合并

将目录下所有 JSON 合并为单个文件，便于批量导入：

```bash
python3 tools/merge.py bookSources/legado/ -o bookSources/legado/all.json
```

常用参数：
- `-o, --output`：输出文件路径
- `--pretty`：格式化输出（缩进 2 空格）
- `--dedup`：按 `bookSourceUrl` 去重

---

## 贡献指南

我们欢迎所有形式的贡献！详细流程请阅读 [docs/contribution.md](docs/contribution.md)。

### 快速贡献流程

1. **Fork** 本仓库
2. 创建分支：`git checkout -b feature/new-source`
3. 添加书源文件到对应目录
4. 运行校验：`python3 tools/validate.py <你的文件>`
5. 提交 PR，标题格式：`[书源类型] 书源名称 - 简要说明`

### 提交规范

- 每个 JSON 文件建议包含同一网站或同一主题的多个书源
- 文件名使用小写英文，如 `biquge.json`、`qidian.json`
- 书源名称建议包含站点标识，便于区分
- 提交前务必运行 `validate.py` 确保格式正确
- 失效书源请提交 Issue 或 PR 标记移除

---

## 常见问题

**Q: 导入后书源搜索不到结果？**
A: 可能原因：① 书源已失效（网站改版或关闭）；② 需要登录/Cookie；③ 网络问题。请尝试切换书源或提交 Issue。

**Q: 如何添加需要登录的书源？**
A: 在书源配置中启用 `enabledCookieJar`，并在 APP 内登录对应网站后自动获取 Cookie。

**Q: 净化源和书源有什么区别？**
A: 书源负责从网站抓取书籍内容，净化源负责对抓取到的正文进行二次过滤（去除广告、修正排版等）。两者配合使用效果最佳。

**Q: 为什么有些书源加载很慢？**
A: 书源速度取决于目标网站的响应速度和你的网络环境，与本仓库无关。建议同时启用多个书源自动切换。

---

## 免责声明

1. 本仓库所有内容均收集自互联网公开渠道，仅供学习交流使用
2. 本仓库不存储、不修改、不传播任何书籍内容
3. 使用者应遵守所在国家/地区的法律法规，尊重知识产权
4. 如本仓库内容侵犯了您的合法权益，请通过 Issue 联系，我们将及时处理
5. 使用本仓库资源产生的任何后果由使用者自行承担

---

## Star History

如果这个项目对你有帮助，欢迎点个 ⭐ Star 支持！

## License

[MIT](LICENSE)
