"""Post one prepared Threads message each time this script runs."""

import datetime
import json
import os
import urllib.parse
import urllib.request

API = "https://graph.threads.net/v1.0"
POSTS = [
    "飲み会のお店、今日はどれ？\n①にぎやかに盛り上がる\n②落ち着いて話せる\n③まずは一杯飲んでから決める\nみんなはどのタイプ？",
    "一杯目を決める時間って、ちょっと楽しい。今日は何を飲みたい気分？",
    "バーで「いつもの」を頼む人、ちょっと憧れる。みんなのいつもの一杯は何ですか？",
    "バーあるある。メニューを見て迷って、結局おすすめを聞く。そこから新しいお気に入りが見つかったりする。",
    "名古屋・栄で飲む夜。にぎやかな一軒目のあと、ゆっくり話せる場所に寄りたくなることありませんか？",
    "今日は一日おつかれさま。BarEnd.で、肩の力を抜いて一杯どうぞ。",
    "お酒の思い出って、味より一緒にいた人や会話を覚えてたりする。みんなの忘れられない一杯は？",
    "飲み会の締め、どれが好き？\n①もう一軒\n②甘いもの\n③まっすぐ帰る\n明日の自分と相談して決めよう。",
    "バーは、お酒を飲むだけじゃなくて、知らない人の話を聞いたり、友だちとゆっくり話したりする場所でもある。",
    "栄でお店を探すとき、決め手は何？\n雰囲気、料理、お酒、それとも一緒に行く人？",
]


def api_request(method, path, params=None):
    token = os.environ["THREADS_ACCESS_TOKEN"]
    url = f"{API}/{path}"
    headers = {"Authorization": f"Bearer {token}"}
    data = None
    if params is not None:
        data = urllib.parse.urlencode(params).encode()
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def main():
    user_id = api_request("GET", "me?fields=id")["id"]
    post_text = POSTS[datetime.date.today().toordinal() % len(POSTS)]
    container = api_request(
        "POST",
        f"{user_id}/threads",
        {"media_type": "TEXT", "text": post_text},
    )
    published = api_request(
        "POST",
        f"{user_id}/threads_publish",
        {"creation_id": container["id"]},
    )
    print("Threadsに投稿しました。投稿ID:", published["id"])


if __name__ == "__main__":
    main()
