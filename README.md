# Popular-Rules-Collection

> **规则数据供应链 + 标准化中间库 + 多客户端构建系统**
> Rules Data Supply Chain · Universal Rule Database · Multi-format Build System

自动采集、标准化、智能去重、冲突检测、版本追踪，并向 **Mihomo / Clash Meta / sing-box / Surge / Shadowrocket / Quantumult X / Egern** 输出规则集。

## 架构

```
Upstream → collect (Fetcher) → backup + manifest
        → normalize → database/
        → deduplicate / conflicts
        → build_* → generated/{mihomo,sing-box,surge,shadowrocket,quantumult-x,egern}
```

## 目录

| 路径 | 用途 |
|------|------|
| `rule/` | 人读浏览 |
| `database/` | Schema 中间库 |
| `generated/` | 客户端产物 |
| `sources/` | registry + health |
| `scripts/` | 采集/标准化/构建 |
| `config/` | categories / profiles / formats |

## 快速开始

```bash
pip install -r requirements.txt
python scripts/collect.py
python scripts/normalize.py --skip-large
python scripts/deduplicate.py
python scripts/build_mihomo.py
python scripts/build_surge.py
python scripts/build_singbox.py
python scripts/build_shadowrocket.py
python scripts/build_quantumultx.py
python scripts/build_egern.py
python scripts/validate.py
```

## 订阅约定

- **Primary**: GitHub Raw
- **Mirror**: jsDelivr / Fastly / Cloudflare（仅加速，非权威）

Example (Egern):

```yaml
rules:
  - rule_set:
      match: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google.yaml"
      policy: Proxy
      update_interval: 86400
```

## License

MIT
