# 文档与目录设计

## 原则

| 层 | 职责 | 路径 |
|----|------|------|
| 数据 | Canonical / Provenance | `database/` |
| 产物 | 多客户端规则 | `generated/` |
| 说明 | 给人看的解释 | `docs/rules/`（**自动生成**） |
| 配置 | 官方站、CDN 模板 | `config/` |

**禁止**：每个 `.list` 旁手写超长 README；禁止在 README 里贴全量域名。

## 推荐目录

```text
docs/
├── rules/           # 每服务一篇，generate_docs.py 生成
│   ├── README.md    # 索引
│   ├── claude.md
│   └── ...
templates/
config/
├── cdn.yaml
└── official_sites.yaml
```

不使用 `rule/Claude/README.md` 与 generated 文件一一对应的爆炸结构。

## 流水线

```text
… → statistics → generate_links → generate_docs → size_gate → commit
```

## 订阅链接模板

- GitHub Raw / jsDelivr / Fastly / Cloudflare 加速
- 由 `generate_links.py` 写出 `generated/subscription_links.json`
