# 规则目录与服务选择

> 当前目录模型以 `rule/_index.yaml` 为准。旧版 Provider/Group 平铺路径不再作为当前规则路径规范。

## 当前模型

rule/_index.yaml
      ↓
服务集 / Provider
      ↓
独立服务 / 子服务
      ↓
docs/services/<同层级>/README.md
      ↓
generated/<client>/<同层级> + Raw URL

## 使用入口

- [全量服务目录](SERVICE_CATALOG.md)
- [完整使用说明](RULE_USAGE_GUIDE.md)
- [规则索引](../rule/_index.yaml)
- [Generated Manifest](../generated/manifest.json)

## 规则字段

每条规则索引记录包含 `entity`、`id`、`display_name`、`rule_count` 和 `sha256`。当前 Release 共 262 条索引记录。服务页面进一步补充七客户端实际编译产物统计。

## 选择原则

服务集适合宽覆盖；独立子服务适合精确分流。不要从聚合规则手工复制规则来创建第三套子规则。