# 书源格式规范详解

本文档详细说明 Legado（阅读 APP）的书源、净化源、订阅源的 JSON 格式规范，供贡献者参考。

---

## 📋 目录

- [Legado 书源格式](#legado-书源格式)
  - [顶层字段](#顶层字段)
  - [ruleSearch 搜索规则](#rulesearch-搜索规则)
  - [ruleBookInfo 详情规则](#rulebookinfo-详情规则)
  - [ruleToc 目录规则](#ruletoc-目录规则)
  - [ruleContent 正文规则](#rulecontent-正文规则)
  - [选择器语法](#选择器语法)
- [Legado 净化源格式](#legado-净化源格式)
- [Legado 订阅源格式](#legado-订阅源格式)
- [URL 变量替换](#url-变量替换)
- [常见问题](#常见问题)

---

## Legado 书源格式

Legado（阅读 APP 3.0+）使用 JSON 数组格式，每个元素是一个书源对象。

### 顶层字段

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `bookSourceName` | string | ✅ | - | 书源名称，显示在书源列表中 |
| `bookSourceGroup` | string | ❌ | "" | 书源分组，用于分类管理 |
| `bookSourceUrl` | string | ✅ | - | 书源站点主页 URL |
| `bookSourceType` | int | ✅ | 0 | 书源类型：0=文本小说, 1=音频, 2=图片(漫画), 3=文件 |
| `bookSourceComment` | string | ❌ | "" | 书源备注说明 |
| `enabled` | boolean | ❌ | true | 是否启用该书源 |
| `enabledExplore` | boolean | ❌ | false | 是否启用发现页（分类浏览） |
| `enabledCookieJar` | boolean | ❌ | false | 是否启用 Cookie 存储（需要登录的站点） |
| `searchUrl` | string | ✅ | - | 搜索请求 URL，支持变量替换 |
| `exploreUrl` | string | ❌ | "" | 发现页 URL，支持多分类（用 `::` 分隔） |
| `ruleSearch` | object | ✅ | - | 搜索结果页解析规则 |
| `ruleBookInfo` | object | ✅ | - | 书籍详情页解析规则 |
| `ruleToc` | object | ✅ | - | 目录页解析规则 |
| `ruleContent` | object | ✅ | - | 正文页解析规则 |
| `lastUpdateTime` | long | ❌ | 0 | 最后更新时间（毫秒时间戳） |
| `customOrder` | int | ❌ | 0 | 自定义排序权重 |
| `variableComment` | string | ❌ | "" | 变量说明 |

### ruleSearch 搜索规则

搜索结果页的解析规则，用于从搜索结果列表中提取书籍信息。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookList` | string | ✅ | 搜索结果列表的选择器，选中每一条结果 |
| `name` | string | ✅ | 书籍名称选择器 |
| `author` | string | ❌ | 作者选择器 |
| `kind` | string | ❌ | 分类选择器 |
| `lastChapter` | string | ❌ | 最新章节选择器 |
| `updateTime` | string | ❌ | 更新时间选择器 |
| `intro` | string | ❌ | 简介选择器 |
| `url` | string | ✅ | 书籍详情页 URL 选择器 |
| `coverUrl` | string | ❌ | 封面图片 URL 选择器 |
| `wordCount` | string | ❌ | 字数选择器 |

**示例：**
```json
"ruleSearch": {
  "bookList": "class.result-list@tag.li",
  "name": "class.book-title@text",
  "author": "class.book-author@text",
  "url": "class.book-title@tag.a@href",
  "coverUrl": "class.book-cover@tag.img@src"
}
```

### ruleBookInfo 详情规则

书籍详情页的解析规则。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ❌ | 书名选择器（如搜索页已有可省略） |
| `author` | string | ❌ | 作者选择器 |
| `kind` | string | ❌ | 分类选择器 |
| `lastChapter` | string | ❌ | 最新章节选择器 |
| `intro` | string | ❌ | 简介选择器 |
| `coverUrl` | string | ❌ | 封面选择器 |
| `tocUrl` | string | ❌ | 目录页 URL 选择器（如详情页和目录页是同一页面可省略） |
| `wordCount` | string | ❌ | 字数选择器 |
| `updateTime` | string | ❌ | 更新时间选择器 |

### ruleToc 目录规则

目录页的解析规则。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `chapterList` | string | ✅ | 章节列表选择器 |
| `chapterName` | string | ✅ | 章节名称选择器 |
| `chapterUrl` | string | ✅ | 章节 URL 选择器 |
| `isVolume` | string | ❌ | 卷标识选择器（用于分卷目录） |

### ruleContent 正文规则

正文页的解析规则。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `content` | string | ✅ | 正文内容选择器 |
| `nextContentUrl` | string | ❌ | 下一页 URL 选择器（用于分页正文） |
| `replaceRegex` | array | ❌ | 正文替换正则列表 |
| `webJs` | string | ❌ | 页面注入 JS（用于动态加载内容的站点） |
| `sourceRegex` | string | ❌ | 源正则替换 |
| `replaceRules` | array | ❌ | 替换规则列表 |

**replaceRegex 格式：**
```json
"replaceRegex": [
  "广告关键词.*?\\n",
  "https?://[^\\s]+"
]
```
数组中每个元素是一个正则表达式，匹配到的内容会被替换为空字符串。

### 选择器语法

Legado 使用自定义的 CSS-like 选择器语法，支持以下操作：

| 语法 | 说明 | 示例 |
|------|------|------|
| `class.xxx` | 按 class 选择 | `class.book-list` |
| `id.xxx` | 按 id 选择 | `id.content` |
| `tag.xxx` | 按标签选择 | `tag.div` |
| `@text` | 获取元素文本 | `class.title@text` |
| `@html` | 获取元素 HTML | `class.content@html` |
| `@href` | 获取 href 属性 | `tag.a@href` |
| `@src` | 获取 src 属性 | `tag.img@src` |
| `@attr.xxx` | 获取自定义属性 | `tag.a@attr.data-url` |
| `@ownText` | 获取直接子文本（不含子元素） | `class.title@ownText` |

**链式调用：**
```
class.book-list@tag.li@tag.a@href
```
表示：选中 class=book-list 的元素 → 其下的 li 标签 → li 下的 a 标签 → 获取 href 属性。

**多选择器（用 `||` 分隔，取第一个匹配的）：**
```
class.content || id.content || tag.article
```

---

## Legado 净化源格式

净化源用于对抓取到的正文进行二次过滤，去除广告、修正排版等。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sourceName` | string | ✅ | 净化源名称 |
| `sourceGroup` | string | ❌ | 分组 |
| `enabled` | boolean | ❌ | 是否启用 |
| `url` | string | ✅ | 生效的 URL 正则，`.*` 表示所有站点 |
| `replaceRegex` | array | ✅ | 替换规则列表 |
| `js` | string | ❌ | 自定义 JS 处理 |
| `comment` | string | ❌ | 备注说明 |
| `lastUpdateTime` | long | ❌ | 更新时间 |

**replaceRegex 两种格式：**

格式一（简单字符串，匹配即删除）：
```json
"replaceRegex": [
  "广告.*?\\n",
  "https?://[^\\s]+"
]
```

格式二（对象，支持自定义替换内容）：
```json
"replaceRegex": [
  {
    "regex": "原内容正则",
    "replacement": "替换为"
  }
]
```

---

## Legado 订阅源格式

订阅源用于自动同步远程书源/净化源。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sourceName` | string | ✅ | 订阅源名称 |
| `sourceGroup` | string | ❌ | 分组 |
| `enabled` | boolean | ❌ | 是否启用 |
| `url` | string | ✅ | 订阅地址（返回 JSON 数组的 URL） |
| `comment` | string | ❌ | 备注 |
| `lastUpdateTime` | long | ❌ | 更新时间 |

---

## URL 变量替换

在 `searchUrl`、`exploreUrl` 等字段中，可以使用以下变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{key}}` | 搜索关键词（URL 编码） | `search?q={{key}}` |
| `{{page}}` | 页码（从 1 开始） | `&page={{page}}` |
| `{{start}}` | 起始偏移量 | `&start={{start}}` |
| `{{name}}` | 书名（详情页用） | - |
| `{{author}}` | 作者（详情页用） | - |

**searchUrl 示例：**
```
https://example.com/search?keyword={{key}}&page={{page}}
```

**exploreUrl 多分类示例：**
```
玄幻::https://example.com/category/xuanhuan
都市::https://example.com/category/dushi
历史::https://example.com/category/lishi
```
格式：`分类名::URL`，多个分类用换行或 `,` 分隔。

---

## 常见问题

**Q: 搜索结果的 URL 是相对路径怎么办？**
A: Legado 会自动根据 `bookSourceUrl` 补全相对路径。如果是其他域名的绝对路径，选择器直接获取完整 URL 即可。

**Q: 正文分页怎么处理？**
A: 在 `ruleContent` 中配置 `nextContentUrl` 选择器，指向下一页的链接，Legado 会自动拼接多页内容。

**Q: 网站需要登录怎么办？**
A: 启用 `enabledCookieJar: true`，然后在 APP 内通过「登录」功能登录该网站，Cookie 会自动保存并用于后续请求。

**Q: 网站内容是动态加载的（JS 渲染）怎么办？**
A: 在 `ruleContent` 中使用 `webJs` 字段注入 JS 代码，等待内容加载完成后再解析。

**Q: 如何调试书源规则？**
A: 在 Legado APP 中，书源管理 → 点击书源 → 「调试」，可以逐步骤查看搜索、详情、目录、正文的解析结果，方便定位问题。

---

## 参考资源

- Legado 官方文档：https://www.legado.cc/
- Legado GitHub：https://github.com/gedoor/legado
- 书源规则调试教程：在 APP 内「帮助」中查看
