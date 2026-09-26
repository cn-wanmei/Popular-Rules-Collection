# Directory Layout v2

## 设计原则

`rule/` 面向人工浏览与选择；`generated/` 面向客户端直接使用。两者都从同一 Semantic IR Run 派生，不能互相作为输入源。

## Rule

Provider 聚合：

`rule/{provider}/{aggregate}/{aggregate}.yaml`

独立子服务：

`rule/{provider}/{service}/{service}.yaml`

例如：

```text
rule/apple/apple/apple.yaml
rule/acfun/acfun_aggregate/acfun_aggregate.yaml
rule/acfun/acfun/acfun.yaml
rule/12306/12306/12306.yaml
```

其中 `12306` 当前没有独立的 provider aggregate 实体；该路径表示其已登记的同名服务。

## Generated

Provider 聚合：

`generated/{client}/{provider}/{aggregate}/{aggregate}`

独立子服务：

`generated/{client}/{provider}/{service}/{service}`

例如：

```text
generated/mihomo/acfun/acfun_aggregate/acfun_aggregate.yaml
generated/mihomo/acfun/acfun/acfun.yaml
generated/mihomo/12306/12306/12306.yaml
```

## 校验

发行树必须声明 `layout_schema: directory_layout_v2`。

构建阶段检查重复路径、legacy direct provider aggregate 路径、Run ID、Semantic IR digest 与 resolver 一致性。

`EntityPathResolver` 是路径生成的唯一代码出口。
