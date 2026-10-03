# Release Runbook（Collection + Icon）

> 唯一操作手册：Build → Publish →（可选）用户面向 GitHub Release。  
> **永不**在 Build/Publish 成功时自动创建用户 zip Release。

## 1. Build Client Rules

1. Actions → **Build Client Rules** → Run workflow  
2. 等待成功；记录：
   - `build_run_id` = 该次 run 的数字 ID  
   - `build_head_sha` = 该次 checkout 的完整 commit SHA  
3. 产物：immutable artifact `release-candidate-<run_id>`

## 2. Publish Release Candidate

1. Actions → **Publish Release Candidate** → Run workflow  
2. 输入：
   - `build_run_id`  
   - `build_head_sha`  
3. 期望：job **绿**；`Trigger Documentation Layer` 即使失败也只 warning（`continue-on-error`）  
4. 成功后 main 上 `rule/` / `generated/` / evidence 已原子晋升  
5. 状态以 [`PUBLISH_STATUS.md`](../PUBLISH_STATUS.md) 为准

## 3. 用户规则 zip（可选，手动）

1. Actions → **Client GitHub Release Packages** → Run workflow  
2. 可选 `stamp`；可选 `dry_run=true` 只打包不发 Release  
3. 基线：优先上一 `rules-*` tag 的 `rule/_index.yaml`，否则 `HEAD~1`  
4. 产物命名：`{client}-{YYYY}-{M}-{D}-{HH}-{MM}-{SS}.zip`（禁止 `:[]`）  
5. Tag：`rules-{safe_stamp}`

## 4. 用户图标 zip（可选，手动 · Icon 仓）

1. Icon 仓 Actions → **Icon Style GitHub Release Packages**  
2. 输入已存在的 V6 `release_id`（见 `config/release-pointers.yaml` production）  
3. 可选 `prev_release_id` 做 changelog  
4. **不**在 V6 Release Writer 成功时自动打用户 Release

## 5. 检查清单

- [ ] Build 绿且 artifact 未过期  
- [ ] Publish 绿且 `PUBLISH_STATUS` 已刷新  
- [ ] 需要用户包时再手动 Release  
- [ ] 数字不手写：只引用机器文件  

## 相关

- [RELEASE_NAMING.md](RELEASE_NAMING.md)  
- [SOURCE_COLLECTION_FUNNEL.md](SOURCE_COLLECTION_FUNNEL.md)  
- [ACTIONS_SHA_PIN.md](ACTIONS_SHA_PIN.md)  
