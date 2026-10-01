# P2 → V2.1–V3 冻结方案（有条件批准修订版）

**状态：** 有条件批准 · 方案已冻结  
**生产流水线：** V2.1 正式下令前 **禁止** 为 P2 修改 Collect/发布  
**当前允许：** 仅 P2.0 Baseline Freeze

## 路线

```text
P2.0 Baseline Freeze  → V2.1 Artifact/Release  → V2.2 Quarantine  
→ V2.3 Shadow+Injection+Enforce  → V2.4 Mihomo IR + Golden L1/L2/L3  
→ 完整发布周期  → V3.0（不并行）→ P2全部完成后审计V3
```

## 八项必须修改（已并入）

1. Baseline Freeze  
2. Artifact Manifest（真相层）  
3. Release 仅分发  
4. Quarantine Content-Type/格式  
5. Growth 多指标  
6. Gate：INFO/WARN/BLOCK_BUILD/BLOCK_RELEASE  
7. Golden 三层  
8. Negative corpus  

详见仓内完整说明与批示对照表。

## 下一触发

主人明示「执行 V2.1」后才改生产流水线。
