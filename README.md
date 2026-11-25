# TikTok API

[English](#english) · [中文](#中文)

## English

This repo reads public TikTok data with Python or curl. You can search videos by keyword, read video details and comments, and look up a creator's profile and videos. You need one EveryInfra API key. You do not need a TikTok account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 5 capabilities cost $0.56 per 1,000 calls (about $0.00056 per call). Failed calls and empty results are not charged. The EveryInfra TikTok API has 28 capabilities, all listed on the platform page: <https://everyinfra.com/en/tiktok-api?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### Quick start

```bash
git clone https://github.com/everyinfra/tiktok-api.git
cd tiktok-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "camping gear" --out videos.csv
python main.py video "<video url>" --out video.json
python main.py comments "<video url>" --out comments.csv
python main.py user <username>
python main.py videos <username> --out user_videos.csv
```

- For `video` and `comments`, pass the `url` from a `search` result, for example https://www.tiktok.com/@<username>/video/<video id>.
- For `user` and `videos`, pass the `author_username` from a `search` result, with or without @. Do not pass a full profile link. An unknown username returns an empty result and is not charged.
- `comments` attaches at most two replies to each top-level comment.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"tiktok","action":"search","params":{"keyword":"camping gear"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `video`, `comments`, `profile`, and `user_videos` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $0.56 |
| `video` | $0.56 |
| `comments` | $0.56 |
| `profile` | $0.56 |
| `user_videos` | $0.56 |

- Billing is per call, about $0.00056 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>
- Prices for the other 23 TikTok capabilities are on the platform page: <https://everyinfra.com/en/tiktok-api?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### Fields

These are the fields that the 5 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_name` | Author's display name. |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `share_count` | Shares. null means not disclosed, not 0. |
| `view_count` | Views or plays. null means not disclosed, not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `collect_count` | Saves or favorites. null means not disclosed, not 0. |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `duration_sec` | Duration in seconds, the same value as duration_seconds (both names are returned): the video's length on video rows, the sound's length on music_search, music_chart and music_detail. |
| `cover_image_url` | Video cover image link (signed, expires). |
| `language` | Content language code (for example zh, en) as judged by the platform; it can be wrong. |
| `hashtags` | Hashtags in the text, in order of appearance; absent when there are none. |
| `music` | Background music: id, title (track name), author, is_original (whether it is an original sound), play_url (audio URL, expires), cover_url. |
| `is_ad` | Whether the video is an ad. |
| `is_pinned` | Whether it is pinned on the author's profile. |
| `is_sponsored` | Whether it contains sponsored content. |
| `is_slideshow` | Whether it is a photo carousel (not a video). |
| `author_id` | Author's unique ID on the platform. |
| `author_url` | Link to the author's profile on the platform. |
| `author_avatar_url` | Author's avatar image link (on most platforms signed and expires). |
| `author_is_verified` | Whether the author has a verified badge; not returned on some requests. |
| `author_is_private` | Whether the author's account is private. |
| `author_follower_count` | Author's follower count. null means not disclosed. |
| `author_following_count` | How many accounts the author follows; not returned on some requests. |
| `author_like_count` | Total likes the author's profile has received; not returned on some requests. |
| `author_video_count` | Total number of videos the author has posted; not returned on some requests. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `duration_seconds` | Duration in seconds. null for content that is not video or audio. |
| `author_bio` | The author's profile bio; not returned on some requests. |

All parameters and fields: <https://everyinfra.com/en/tiktok-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

#### `video` (video details)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_name` | Author's display name. |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `share_count` | Shares. null means not disclosed, not 0. |
| `view_count` | Views or plays. null means not disclosed, not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `collect_count` | Saves or favorites. null means not disclosed, not 0. |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `duration_sec` | Duration in seconds, the same value as duration_seconds (both names are returned): the video's length on video rows, the sound's length on music_search, music_chart and music_detail. |
| `cover_image_url` | Video cover image link (signed, expires). |
| `language` | Content language code (for example zh, en) as judged by the platform; it can be wrong. |
| `country` | Country or region: a full name or an ISO code depending on the platform, not normalized. |
| `hashtags` | Hashtags in the text, in order of appearance; absent when there are none. |
| `music` | Background music: id, title (track name), author, is_original (whether it is an original sound), play_url (audio URL, expires), cover_url. |
| `is_ad` | Whether the video is an ad. |
| `is_pinned` | Whether it is pinned on the author's profile. |
| `is_sponsored` | Whether it contains sponsored content. |
| `is_slideshow` | Whether it is a photo carousel (not a video). |
| `has_shop_product` | Whether the video has a TikTok Shop product attached; if the key is absent, it cannot be determined. |
| `author_id` | Author's unique ID on the platform. |
| `author_url` | Link to the author's profile on the platform. |
| `author_avatar_url` | Author's avatar image link (on most platforms signed and expires). |
| `author_bio` | The author's profile bio; not returned on some requests. |
| `author_is_verified` | Whether the author has a verified badge; not returned on some requests. |
| `author_is_private` | Whether the author's account is private. |
| `author_is_seller` | Whether the author is a TikTok Shop seller. |
| `author_follower_count` | Author's follower count. null means not disclosed. |
| `author_following_count` | How many accounts the author follows; not returned on some requests. |
| `author_like_count` | Total likes the author's profile has received; not returned on some requests. |
| `author_video_count` | Total number of videos the author has posted; not returned on some requests. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `duration_seconds` | Duration in seconds. null for content that is not video or audio. |

All parameters and fields: <https://everyinfra.com/en/tiktok-api/video?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

#### `comments` (comments)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `author_id` | Author's unique ID on the platform. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `reply_count` | Replies, usually replies to a comment. null means not disclosed. |
| `is_reply` | Whether it is a reply. |
| `liked_by_author` | Whether the comment was liked by the author. |
| `pinned_by_author` | Whether the comment is pinned by the author. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `reply_to_id` | ID of the comment being replied to. |

All parameters and fields: <https://everyinfra.com/en/tiktok-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

#### `profile` (profile or object details)

| Field | Meaning |
|---|---|
| `user_id` | User's unique ID on the platform. |
| `username` | Username (@handle). |
| `display_name` | Display name; can differ from username. |
| `bio` | Profile bio written by the account; may contain line breaks and emoji. |
| `url` | Link to the record on the platform. |
| `external_url` | External link on the profile. |
| `follower_count` | Followers. null means not disclosed, not 0. |
| `following_count` | Accounts followed. null means not disclosed, not 0. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `video_count` | Number of videos. |
| `friend_count` | Number of friends. |
| `is_verified` | Whether the platform verified the account. null means it cannot be determined. |
| `is_private` | Whether the account is private. |
| `avatar_url` | Avatar image link. |
| `created_at` | Creation time, same format as posted_at. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/tiktok-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

#### `user_videos` (videos by user)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_name` | Author's display name. |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `share_count` | Shares. null means not disclosed, not 0. |
| `view_count` | Views or plays. null means not disclosed, not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `collect_count` | Saves or favorites. null means not disclosed, not 0. |
| `duration_sec` | Duration in seconds, the same value as duration_seconds (both names are returned): the video's length on video rows, the sound's length on music_search, music_chart and music_detail. |
| `cover_image_url` | Video cover image link (signed, expires). |
| `country` | Country or region: a full name or an ISO code depending on the platform, not normalized. |
| `music` | Background music: id, title (track name), author, is_original (whether it is an original sound), play_url (audio URL, expires), cover_url. |
| `is_ad` | Whether the video is an ad. |
| `is_pinned` | Whether it is pinned on the author's profile. |
| `is_slideshow` | Whether it is a photo carousel (not a video). |
| `author_id` | Author's unique ID on the platform. |
| `author_url` | Link to the author's profile on the platform. |
| `author_avatar_url` | Author's avatar image link (on most platforms signed and expires). |
| `author_bio` | The author's profile bio; not returned on some requests. |
| `author_is_verified` | Whether the author has a verified badge; not returned on some requests. |
| `author_is_private` | Whether the author's account is private. |
| `author_follower_count` | Author's follower count. null means not disclosed. |
| `author_following_count` | How many accounts the author follows; not returned on some requests. |
| `author_like_count` | Total likes the author's profile has received; not returned on some requests. |
| `author_video_count` | Total number of videos the author has posted; not returned on some requests. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `duration_seconds` | Duration in seconds. null for content that is not video or audio. |
| `hashtags` | Hashtags in the text, in order of appearance; absent when there are none. |

All parameters and fields: <https://everyinfra.com/en/tiktok-api/user_videos?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### FAQ

**Do I need a TikTok account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.56 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

**Can I connect the TikTok API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>. An agent can then search TikTok content, read comments, and look up accounts by itself.

**What legal points apply when I use TikTok data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which TikTok data can I get?**

The EveryInfra TikTok API has 28 capabilities:

- keyword search
- profile or object details
- videos by user
- video details
- comments
- topic content
- followers
- transcript
- shop product search
- shop creator details
- hashtag search
- music search
- music chart
- account search
- videos using a sound
- comment replies
- shop best sellers
- shop products by category
- following
- video download links
- live room
- shop store products
- shop product reviews
- trending hashtags
- Username to user ID
- link recognition
- hashtag detail
- music detail

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/tiktok-api?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### Tested

Before release, we ran the 5 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "camping gear" --out videos.csv` | 2026-11-25 13:16 | 10 | $0.000556 |
| `python main.py video "<video url>" --out video.json` | 2026-11-25 13:16 | 1 | $0.000556 |
| `python main.py comments "<video url>" --out comments.csv` | 2026-11-25 13:17 | 20 | $0.000556 |
| `python main.py user <username>` | 2026-11-25 13:17 | 1 | $0.000556 |
| `python main.py videos <username> --out user_videos.csv` | 2026-11-25 13:17 | 10 | $0.000556 |

## 中文

本仓库用 Python 或 curl 读 TikTok 公开数据：按关键词搜视频，读视频详情和评论，查作者资料和作者视频。只需一把 EveryInfra API Key，不用 TikTok 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 5 个能力每千次 $0.56（每次约 $0.00056），失败和空结果不收费。TikTok 共 28 个能力：<https://everyinfra.com/tiktok-api?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/tiktok-api.git
cd tiktok-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "camping gear" --out videos.csv
python main.py video "<视频链接>" --out video.json
python main.py comments "<视频链接>" --out comments.csv
python main.py user <用户名>
python main.py videos <用户名> --out user_videos.csv
```

- `video` 和 `comments` 传 `search` 结果里的 `url`，形如 https://www.tiktok.com/@<用户名>/video/<视频 ID>。
- `user` 和 `videos` 传 `search` 结果里的 `author_username`，带不带 @ 都行；不要传完整主页链接。用户名不存在时返回空结果，不扣费。
- `comments` 每条顶层评论最多附带两条回复。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"tiktok","action":"search","params":{"keyword":"camping gear"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`video`、`comments`、`profile`、`user_videos` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $0.56 |
| 视频详情 | `video` | $0.56 |
| 评论 | `comments` | $0.56 |
| 主页或对象详情 | `profile` | $0.56 |
| 用户视频 | `user_videos` | $0.56 |

- 按调用次数计费，每次约 $0.00056；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>
- TikTok 其他 23 个能力的单价见平台页 <https://everyinfra.com/tiktok-api?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### 返回字段

下面是这 5 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_name` | 评价人名字（shop_product_reviews），平台已打码，如 n**h。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 分享/转发数。 |
| `view_count` | 浏览/播放数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `collect_count` | 收藏数。 |
| `repost_count` | 转发数。 |
| `duration_sec` | 时长，单位秒，与 duration_seconds 同值（两个名字都返回）：视频行是视频时长，music_search、music_chart、music_detail 是声音的时长。 |
| `cover_image_url` | 视频封面图链接（带签名，会过期）。 |
| `language` | 内容语言代码（如 zh、en），由平台判定，可能不准。 |
| `hashtags` | 正文里的话题标签数组，按出现顺序；没有时不出现这个字段。 |
| `music` | 背景音乐：id、title（曲名）、author、is_original（是否原声）、play_url（音频地址，会过期）、cover_url。 |
| `is_ad` | 是否广告视频。 |
| `is_pinned` | 是否在作者主页置顶。 |
| `is_sponsored` | 是否含赞助内容。 |
| `is_slideshow` | 是否图文轮播（不是视频）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_url` | 作者在原平台的主页链接。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_is_verified` | 作者是否有认证标；部分请求不返回。 |
| `author_is_private` | 作者是否私密账号。 |
| `author_follower_count` | 作者粉丝数。 |
| `author_following_count` | 作者关注的账号数；部分请求不返回。 |
| `author_like_count` | 作者主页获赞总数；部分请求不返回。 |
| `author_video_count` | 作者发布的视频总数；部分请求不返回。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `duration_seconds` | 时长，单位秒。 |
| `author_bio` | 作者主页简介；部分请求不返回。 |

完整参数和字段：<https://everyinfra.com/tiktok-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

#### `video`（视频详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_name` | 评价人名字（shop_product_reviews），平台已打码，如 n**h。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 分享/转发数。 |
| `view_count` | 浏览/播放数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `collect_count` | 收藏数。 |
| `repost_count` | 转发数。 |
| `duration_sec` | 时长，单位秒，与 duration_seconds 同值（两个名字都返回）：视频行是视频时长，music_search、music_chart、music_detail 是声音的时长。 |
| `cover_image_url` | 视频封面图链接（带签名，会过期）。 |
| `language` | 内容语言代码（如 zh、en），由平台判定，可能不准。 |
| `country` | 国家或地区。 |
| `hashtags` | 正文里的话题标签数组，按出现顺序；没有时不出现这个字段。 |
| `music` | 背景音乐：id、title（曲名）、author、is_original（是否原声）、play_url（音频地址，会过期）、cover_url。 |
| `is_ad` | 是否广告视频。 |
| `is_pinned` | 是否在作者主页置顶。 |
| `is_sponsored` | 是否含赞助内容。 |
| `is_slideshow` | 是否图文轮播（不是视频）。 |
| `has_shop_product` | 视频是否挂了 TikTok Shop 商品；没有这个键表示无法判定。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_url` | 作者在原平台的主页链接。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_bio` | 作者主页简介；部分请求不返回。 |
| `author_is_verified` | 作者是否有认证标；部分请求不返回。 |
| `author_is_private` | 作者是否私密账号。 |
| `author_is_seller` | 作者是否 TikTok Shop 卖家。 |
| `author_follower_count` | 作者粉丝数。 |
| `author_following_count` | 作者关注的账号数；部分请求不返回。 |
| `author_like_count` | 作者主页获赞总数；部分请求不返回。 |
| `author_video_count` | 作者发布的视频总数；部分请求不返回。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `duration_seconds` | 时长，单位秒。 |

完整参数和字段：<https://everyinfra.com/tiktok-api/video?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

#### `comments`（评论）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `like_count` | 点赞数。 |
| `reply_count` | 回复数，通常用于评论的子回复。 |
| `is_reply` | 是否为回复。 |
| `liked_by_author` | 评论是否被作者点赞。 |
| `pinned_by_author` | 评论是否被作者置顶。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `reply_to_id` | 被回复评论 ID。 |

完整参数和字段：<https://everyinfra.com/tiktok-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

#### `profile`（主页或对象详情）

| 字段 | 含义 |
|---|---|
| `user_id` | 用户在原平台的唯一 ID。 |
| `username` | 用户名（@handle）。 |
| `display_name` | 显示名，可能与 username 不同。 |
| `bio` | 个人简介，账号自己填写的文本。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `external_url` | 主页外链。 |
| `follower_count` | 粉丝数。 |
| `following_count` | 关注数。 |
| `like_count` | 点赞数。 |
| `video_count` | 视频数。 |
| `friend_count` | 好友数。 |
| `is_verified` | 是否为平台认证账号（蓝V等）。 |
| `is_private` | 是否私密账号。 |
| `avatar_url` | 头像图片链接。 |
| `created_at` | 创建时间，格式同 posted_at。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/tiktok-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

#### `user_videos`（用户视频）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_name` | 评价人名字（shop_product_reviews），平台已打码，如 n**h。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 分享/转发数。 |
| `view_count` | 浏览/播放数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `collect_count` | 收藏数。 |
| `duration_sec` | 时长，单位秒，与 duration_seconds 同值（两个名字都返回）：视频行是视频时长，music_search、music_chart、music_detail 是声音的时长。 |
| `cover_image_url` | 视频封面图链接（带签名，会过期）。 |
| `country` | 国家或地区。 |
| `music` | 背景音乐：id、title（曲名）、author、is_original（是否原声）、play_url（音频地址，会过期）、cover_url。 |
| `is_ad` | 是否广告视频。 |
| `is_pinned` | 是否在作者主页置顶。 |
| `is_slideshow` | 是否图文轮播（不是视频）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_url` | 作者在原平台的主页链接。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_bio` | 作者主页简介；部分请求不返回。 |
| `author_is_verified` | 作者是否有认证标；部分请求不返回。 |
| `author_is_private` | 作者是否私密账号。 |
| `author_follower_count` | 作者粉丝数。 |
| `author_following_count` | 作者关注的账号数；部分请求不返回。 |
| `author_like_count` | 作者主页获赞总数；部分请求不返回。 |
| `author_video_count` | 作者发布的视频总数；部分请求不返回。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `duration_seconds` | 时长，单位秒。 |
| `hashtags` | 正文里的话题标签数组，按出现顺序；没有时不出现这个字段。 |

完整参数和字段：<https://everyinfra.com/tiktok-api/user_videos?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### 常见问题

**调用时要不要提供 TikTok 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.56 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

**能把 TikTok 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>。Agent 能自己搜 TikTok 内容、读评论、查账号。

**用 TikTok 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 TikTok 的哪些数据？**

TikTok 有 28 个能力：关键词搜索、主页或对象详情、用户视频、视频详情、评论、话题内容、粉丝数量、视频文稿、电商商品搜索、带货达人、话题搜索、音乐搜索、音乐榜、账号搜索、用某音乐的视频、评论回复、商城热销榜、商城类目商品、关注列表、视频下载链接、直播间、店铺商品、商品评价、趋势话题榜、用户名换编号、链接识别、话题详情、音乐详情。每个能力的参数和返回字段见平台页 <https://everyinfra.com/tiktok-api?utm_source=github&utm_medium=example_repo&utm_campaign=tiktok-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 5 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "camping gear" --out videos.csv` | 2026-11-25 13:16 | 10 | $0.000556 |
| `python main.py video "<视频链接>" --out video.json` | 2026-11-25 13:16 | 1 | $0.000556 |
| `python main.py comments "<视频链接>" --out comments.csv` | 2026-11-25 13:17 | 20 | $0.000556 |
| `python main.py user <用户名>` | 2026-11-25 13:17 | 1 | $0.000556 |
| `python main.py videos <用户名> --out user_videos.csv` | 2026-11-25 13:17 | 10 | $0.000556 |

`video` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "7672476589984091423",
  "text": "Cama plegable de camping XXL DoCred con colchón, estructura …",
  "like_count": 7931,
  "comment_count": 151,
  "share_count": 279,
  "view_count": 877900,
  "posted_at": "2026-08-10T18:47:58+00:00",
  "collect_count": 966,
  "repost_count": 0,
  "duration_sec": 45,
  "language": "es",
  "is_ad": true,
  "duration_seconds": 45
}
```

## License

MIT
