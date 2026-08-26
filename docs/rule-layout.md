# rule/ layout (Primary Ecosystem)

Physical path is derived **only** from `primary_category` + display names.

```text
config/categories.yaml          # ecosystem id → display_name
config/service_primary.yaml     # service id → primary_category, display_name, tags
database/services/*.yaml        # data
        ↓
scripts/generate_rule_pages.py
        ↓
rule/{Ecosystem}/{Service}/
```

Examples:

| Service | Path |
|---------|------|
| wechat | `rule/Tencent/WeChat/` |
| alipay | `rule/Alibaba/Alipay/` |
| douyin | `rule/ByteDance/Douyin/` |
| icbc (future) | `rule/UnionPay/ICBC/` |
| xbox | `rule/Microsoft/Xbox/` |

Do not hand-edit `rule/`.
