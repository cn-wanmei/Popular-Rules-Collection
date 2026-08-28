# Surge 规则使用说明

> 目录：`generated/surge/`

## 热门规则

| 规则 | 策略 | 直链 |
|------|------|------|
| china | DIRECT | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/china.list) |
| google | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google.list) |
| ai | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ai.list) |
| restricted | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/restricted.list) |
| adblock-light | REJECT | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/adblock-light.list) |

## 示例

```text
RULE-SET,https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/china.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google.list,PROXY
RULE-SET,https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/restricted.list,PROXY
GEOIP,CN,DIRECT
FINAL,PROXY
```

[总览](../README.md)
