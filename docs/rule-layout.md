# rule/ layout — Historical Reference

> **历史说明：** 本页保留旧 V1 layout 设计，不能作为当前 Release 的路径规范。

当前入口：[rule/_index.yaml](../rule/_index.yaml) · [SERVICE_CATALOG.md](SERVICE_CATALOG.md) · [ARCHITECTURE.md](ARCHITECTURE.md)

旧文档曾使用 `rule/{Ecosystem}/{Service}/` 与 V1 Canonical Service Model；当前 Release 的实际规则发行路径直接读取 `rule/_index.yaml`，例如 `alibaba/alipay/alipay.yaml`。

V3 Canonical 真源位于 `data/runs/<run>/canonical/`；`rule/` 是同一 Semantic IR Run 的人类可读发行投影。