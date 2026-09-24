# 客户端 Icon URL — Current V3

图标与规则文件解耦。当前生产消费入口是 Icon System 3 当前不可变 Release。

## 当前 SSOT

```text
assets/icons/v3/release-pointer.json
      ↓
assets/icons/v3/releases/<version>/
      ↓
index/clients/<client>.json
      ↓
entry.path + digest
```

当前 Release：`2026.09.22-5e0e48ad55c6`

Raw 模式：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/<version>/<entry.path>`

不要把 Legacy `assets/icons/png/`、`rendered/` 或旧 V2 页面当作 Current V3 SSOT。