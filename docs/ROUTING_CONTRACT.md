# Routing Contract

分流**决策层**规范。不推倒现有 China / Proxy / Service 数据。

## 两套优先级

| 文件 | 职责 |
|------|------|
| `config/priority.yaml` | **Source Ranking**（来源质量） |
| `config/routing_priority.yaml` | **Routing Precedence**（最终动作） |
| `config/routing_contract.yaml` | 动作集合、层级、冲突、终结策略 |

Dataset 层 `action_conflict: keep_all` 允许同一域名多标签；  
**生成客户端规则时必须 resolve 为唯一** `DIRECT | PROXY | REJECT`。

## 优先级（高 → 低）

```text
Explicit Override
  → System (LAN / private / reserved)
  → Service
  → Security
  → Category
  → GeoSite
  → GeoIP
  → Network
  → Default = PROXY
```

## 原则

- Service 信息密度 > Region
- Domain > GeoIP
- CN 地理 ≠ 所有中国公司国际业务一律 DIRECT
- DNS 为 **resolution**，与 routing 正交（见 `database/policies/dns/`）
- IPv4/IPv6 系统网段应对称

## Policies

| Policy | 路径 |
|--------|------|
| DIRECT | `database/policies/direct/` |
| PROXY | `database/policies/proxy/` |
| REJECT | `database/policies/reject/` |
| Overrides | `database/policies/overrides/` (`force_*`) |
| DNS | `database/policies/dns/` |

## 校验

```bash
python scripts/routing_contract_validate.py
```
