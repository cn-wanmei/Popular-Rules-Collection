# Actions SHA Pin 契约（三仓共用）

> 禁止 floating `@v4` / `@v5`。新增 workflow 必须 pin 到下表 SHA。

| Action | Pin SHA | 备注 |
|---|---|---|
| `actions/checkout` | `d23441a48e516b6c34aea4fa41551a30e30af803` | v4.2.x 线 |
| `actions/setup-python` | `5fda3b95a4ea91299a34e894583c3862153e4b97` | |
| `actions/upload-artifact` | `b7c566a772e6b6bfb58ed0dc250532a479d7789f` | Collection / Icon 统一 |
| `actions/download-artifact` | `634f93cb2916e3fdff6788551b99b062d0335ce0` | Collection publish |

## 范围

- **Collection**：所有 `.github/workflows/*.yml`  
- **Icon**：`pr-ci.yml` / `icon-github-release.yml` / `release.yml` / `v6-manifest-gate.yml`  
- **Source**：新增或改动 workflow 时对齐本表  

## 升级流程

1. 在官方 release 选定新 SHA  
2. 三仓同步替换并跑 architecture / PR CI  
3. 更新本表  
