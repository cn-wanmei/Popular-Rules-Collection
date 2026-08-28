# 国内媒体 / 音视频 / 音乐 / 听书 规则

> 策略建议（中国大陆用户）：**DIRECT**（直连）。
> 仅收录有可信上游的服务，不编造域名。

## 视频 / 直播

| Service | 上游 | 说明 |
|---------|------|------|
| bilibili | BM7 + Meta + v2fly | 哔哩哔哩 |
| iqiyi | BM7 + Meta | 爱奇艺 |
| youku | BM7 + Meta | 优酷 |
| tencentvideo | BM7 | 腾讯视频 |
| wetv | BM7 | WeTV（腾讯出海） |
| pptv | BM7 | PPTV |
| acfun | BM7 + Meta | AcFun |
| cctv | BM7 + Meta | 央视网/CNTV |
| sohu | BM7 | 搜狐视频 |
| letv | BM7 | 乐视 |
| huya | BM7 + Meta | 虎牙直播 |
| douyu | BM7 + Meta | 斗鱼直播 |
| douyin | BM7 + Meta | 抖音 |
| kuaishou | BM7 | 快手 |

## 音乐 / 听书 / 音频

| Service | 上游 | 说明 |
|---------|------|------|
| netease | BM7 + Meta | 网易云音乐 |
| kugou | Meta | 酷狗 |
| kuwo | Meta | 酷我 |
| kugoukuwo | 合并 | 酷狗+酷我 |
| ximalaya | Meta | 喜马拉雅 |
| himalaya | BM7 | Himalaya |
| applemusic | BM7 | Apple Music |
| youtubemusic | Dler 等 | YouTube Music |
| spotify | BM7 + v2fly | Spotify |

## 其他

| Service | 说明 |
|---------|------|
| bahamut | 巴哈姆特（繁中） |
| emby | 自建媒体 |
| tencent | 腾讯生态聚合 |

## 客户端订阅

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/<service>.yaml
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/database/domains/<service>.txt
```

国内媒体建议：`policy: DIRECT`。

## 暂无稳定专用上游（未收录）

- 芒果 TV / MGTV
- 咪咕音乐
- QQ 音乐（多并入 Tencent）
- 蜻蜓 FM / 荔枝
- 番茄小说等

有稳定上游后再增量加入。
