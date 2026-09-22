# 规则目录与使用场景

## 三层边界

`data/runs/<run-id>/canonical` 是 V3 Canonical 真源；`data/runs/<run-id>/ir` 是语义中间层；最终从同一个 Run 生成两个面向消费者的发行投影：

```text
Semantic IR
   ├── rule/                         用户浏览 / 搜索 / 选择
   └── generated/
         ├── <client>/               客户端规则
         └── <network-scope>/        网络数据
```

## 人类可读规则树

```text
rule/
├── <provider>/all/rules.yaml
├── <provider>/<service>/rules.yaml
├── china/all/rules.yaml
├── category/<category>/all/rules.yaml
├── group/<group>/rules.yaml
├── aggregate/<aggregate>/rules.yaml
└── unmapped/<service>/rules.yaml
```

每个 `rules.yaml` 都是通用、客户端无关的规则记录，并带有 Run ID 与 Semantic IR digest；它不是编辑源，也不是客户端运行时格式。

## 客户端与网络发行

`generated/<client>/...` 由 Client Adapter 编译；`generated/<network-scope>/...` 是网络数据发行树。

## SSOT

V3 Canonical=`data/runs/<run-id>/canonical`；Semantic IR=`data/runs/<run-id>/ir`；用户规则发行入口=`rule/`；机器订阅入口=`generated/`。

`rules/` 已删除，不再存在第三套规则目录。