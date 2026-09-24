# PRC Icon Engine — Current V3

图标渲染引擎属于 Icon System 3 内部生产组件。当前消费链路：

```text
Icon Identity
  ↓
Source / License / Provenance
  ↓
Normalize / Render
  ↓
Visual + Identity + Client QA
  ↓
Immutable V3 Release
  ↓
7 client indexes
```

当前消费者应读取 `assets/icons/v3/release-pointer.json` 与对应 client index，而不是直接依赖 Legacy `assets/icons/png/{size}/`。