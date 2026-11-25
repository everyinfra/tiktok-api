"""TikTok API 示例（TikTok API in Python）。

  python main.py search "camping gear" --out videos.csv   # 按关键词搜视频 / search videos
  python main.py video "<视频链接>" --out video.json      # 视频详情 / video detail
  python main.py comments "<视频链接>" --out comments.csv # 视频评论 / comments
  python main.py user <用户名>                            # 作者资料 / creator profile
  python main.py videos <用户名> --out user_videos.csv    # 作者的视频 / a creator's videos
"""
import argparse

from everyinfra import fetch, report

SORTS = ["newest", "oldest", "popular"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜视频 / search videos by keyword")
    s.add_argument("keyword")
    v = sub.add_parser("video", help="视频详情 / one video")
    v.add_argument("url")
    c = sub.add_parser("comments", help="视频评论 / comments of one video")
    c.add_argument("url")
    u = sub.add_parser("user", help="作者资料 / creator profile")
    u.add_argument("username")
    vi = sub.add_parser("videos", help="作者的视频 / a creator's videos")
    vi.add_argument("username")
    vi.add_argument("--sort", choices=SORTS, help="newest / oldest / popular")
    for x in (s, v, c, u, vi):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        rows, charged = fetch("search", {"keyword": a.keyword})
    elif a.cmd == "video":
        rows, charged = fetch("video", {"url": a.url})
    elif a.cmd == "comments":
        rows, charged = fetch("comments", {"url": a.url})
    elif a.cmd == "user":
        rows, charged = fetch("profile", {"username": a.username})
    else:
        params = {"username": a.username, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("user_videos", params)
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
