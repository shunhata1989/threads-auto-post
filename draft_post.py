"""Prepare a daily Threads draft for the user to review; never publish it."""

from datetime import datetime
import os
from zoneinfo import ZoneInfo

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


def main():
    today = datetime.now(ZoneInfo("Asia/Tokyo")).date()
    post = POSTS[today.toordinal() % len(POSTS)]
    print(f"## 今日のThreads投稿案（{today:%Y年%m月%d日}）")
    print()
    print(post)
    print()
    print("---")
    print("これは投稿案です。内容を確認してから、公開する場合だけ手動で実行してください。")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "w", encoding="utf-8") as summary:
        summary.write(f"## 今日のThreads投稿案（{today:%Y年%m月%d日}）\n\n{post}\n\n---\nこれは投稿案です。公開は手動実行するまで行われません。\n")


if __name__ == "__main__":
    main()
