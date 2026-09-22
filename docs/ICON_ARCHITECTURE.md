# Icon Asset Pipeline — Current V3

```text
Service Registry → Icon identity / provenance / license
→ Icon System 3 deterministic build
→ 7 styles + QA / Gate + 7 client indexes
→ immutable V3 release
→ assets/icons/v3/release-pointer.json
```

当前生产权威是 `assets/icons/v3/release-pointer.json` 指向的不可变 release。旧 `assets/icons/manifest.yaml` / `registry.yaml` 仅用于兼容或历史追踪，不代表当前 V3 发布状态。

硬约束：service→icon 必须显式绑定；stable asset 必须可追溯 source/provenance/license；brand、strategy、dataset 语义分离；Builder 不得猜 Logo；sing-box rule JSON 不包含 icon payload。