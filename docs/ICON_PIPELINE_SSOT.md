# Icon Pipeline SSOT

```text
manifest / source → no_black → engine → rendered/png → icon_qa → client_adapter
```

禁止历史 `icon_*_apply` / phase 脚本回到 Collect 主路径。
Canonical URL 仅由 `icon_client_adapter` 生成。
