# 国内独立规则来源评估（2026-08-25）

## 评估标准

| 维度 | 要求 |
|------|------|
| 维护中 | 近 30 天有更新 / 日更 CI |
| 独立国内规则 | 公司或 App 级可单独引用，非仅 `cn` 大杂烩 |
| 可采格式 | 文本 list/yaml（避免只提供 .dat/.mrs 二进制） |
| 非二次镜像 | 尽量避免「只聚合 BM 再发一遍」 |
| 许可与体积 | 可合规引用，单文件不逼近 GitHub 100MB |

## 候选仓库结论

| 仓库 | Stars/活跃 | 国内独立规则 | 结论 |
|------|------------|--------------|------|
| **MetaCubeX/meta-rules-dat** | ~5k，日更 | alibaba / tencent / baidu / bytedance / jd / alibabacloud / netease / bilibili 等 `.list` | **采纳为第 6 源** |
| **v2fly/domain-list-community** | 上游权威 | data/ 内公司标签 | 中期可选；现经 MetaCubeX 间接使用 |
| **blackmatrix7/ios_rule_script** | 已接入 | Alibaba/Tencent/WeChat/DouYin/银行/运营商等 | **已有；补挂国内目录** |
| Hawaiine/mihomo-rules 等合集 | 日更 | 多来自 BM+v2fly+Loyalsoldier | **不采纳**（重复聚合） |
| ACL4SSR | 配置向 | 偏 GFW/广告，App 细类弱 | **不采纳** |
| HenryChiao / 666OS 等 | 配置+规则 | 二次构建 BM/MetaCubeX | **不采纳**（防循环） |
| 个人自用小仓 | 低星 | 覆盖不全 / 难审计 | **不采纳** |

## 关键事实

- MetaCubeX **无** `wechat.list` / `taobao.list` / `alipay.list` / `qq.list`（404）。
- 淘宝/天猫 → 使用 **alibaba**；QQ 系 → **tencent**；微信 → BM **wechat**。
- 多数「热门 mihomo 规则仓」是配置模板或再分发，不是新数据源。

## 已写入 Registry

1. 源 `metacubex`：`geo/geosite/{alibaba,alibabacloud,tencent,baidu,bytedance,jd,netease,bilibili}.list`
2. BM 国内 P0：alibaba, alipay, tencent, wechat, bytedance, douyin, baidu, jingdong, netease, 三运营商, 12306, unionpay, didi, pinduoduo, meituan, xiaohongshu, tencentvideo
