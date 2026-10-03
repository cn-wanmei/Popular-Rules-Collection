# 客户端 Release 命名约定

## 文件名（必须安全）

```
{client}-{YYYY}-{M}-{D}-{HH}-{MM}-{SS}.zip
```

示例：`egern-2026-10-2-13-47-26.zip`

**禁止**出现在文件名中的字符：`: [ ] * ? " < > | \ /`

原因：GitHub Actions artifact、shell glob、`gh release create` 均会误解析这些字符。

## 展示戳（仅 notes / 标题）

```
{YYYY}-{M}-{D}-{H}[{MM}:{SS}]
```

示例：`2026-10-2-13[47:26]`

## Git tag

```
rules-{YYYY}-{M}-{D}-{HH}-{MM}-{SS}
```

与安全文件名时间戳一致。

## 实现

- 生成：`scripts/package_client_releases.py`
- 发布：`.github/workflows/client-github-release.yml`（仅 `workflow_dispatch`）
