# Routing Contract

分流**决策层**规范。不推倒现有 China / Proxy / Service 数据。

## 两套优先级

| 文件 | 职责 |
|------|------|
| `config/priority.yaml` | **Source Ranking** |
| `config/routing_priority.yaml` | **Routing Precedence** |
| `config/routing_contract.yaml` | 动作、层级、冲突、终结 |
| `config/resolution_policy.yaml` | DNS（与 routing 正交） |

Dataset 层可多标签；**最终交付必须唯一** `DIRECT \| PROXY \| REJECT`。

## 优先级（高 → 低）

```text
Explicit → System → Service → Security → Category
  → GeoSite → GeoIP → Network → Default = PROXY
```

## P1

| 项 | 状态 |
|----|------|
| Service > Category > GeoSite > GeoIP | ✅ + `routing_resolve.py` |
| Explicit Override | ✅ `policies/overrides/` |
| DNS = Resolution | ✅ `resolution_policy.yaml` |
| IPv6 / QUIC / SNI 边界 | ✅ `ROUTING_CAPABILITIES.md` |

```bash
python scripts/routing_contract_validate.py
python scripts/routing_resolve.py --demo
```
