# Icon Asset Pipeline（架构锁死）

图标是**第三条产品资产管线**，与 Service Rules / Network Datasets 并列。

```text
Service Registry
      │
      ├──────────────→ Rule Pipeline → generated/
      │
      └──────────────→ config/icons.yaml (service_id → icon_id)
                              │
                       assets/icons/manifest.yaml
                              │
                    Source / Provenance / License
                              │
                         Normalize + Render
                              │
              Brand │ Strategy │ Dataset │ Pending
                              │
                         Icon QA
                              │
                      Client Adapter (URL only)
```

## 绑定

`service ≠ icon file`  
`service_id → icon_id → manifest → variants → PNG/SVG`

## 类别

| 类别 | 示例 | 规则 |
|------|------|------|
| brand | Google, WeChat | 官方色优先；禁止瞎搜 |
| strategy | DIRECT, PROXY, REJECT | 项目几何视觉 |
| dataset | China, GeoIP, ASN | 禁止企业 Logo |
| pending | placeholder | 显式决策 |

## 禁止事项

1. Service 自动搜索 Logo  
2. Builder 猜 Logo  
3. favicon 作永久主资产  
4. 未验证标为 verified  
5. 黑白转换覆盖官方品牌色  
6. Strategy 与 Brand 混用  
7. Dataset 使用企业 Logo  
8. 为 Coverage 造假图标  
9. sing-box 规则 JSON 塞图标  
10. 图标二进制进 database/

## Phase

- **I**：config/icons.yaml + QA（本阶段）  
- **II**：核心 brand 有源升档  
- **III**：strategy/dataset 统一视觉  
- **IV**：QA 驱动替换错配  
- **V**：dark/light/compact 按需  

**不进入「全部批量补齐」。**

```bash
python scripts/icon_config_sync.py
python scripts/icon_qa.py
python scripts/icon_coverage.py
python scripts/icon_identity_audit.py
```
