"""Prepare a daily Threads draft for the user to review; never publish it."""

from datetime import datetime
import os
from zoneinfo import ZoneInfo


POSTS = [
    "飲み会のお店決めるとき、結局「どこでもいい」がいちばん困るんよな。みんなは先にジャンル決める？",
    "一杯目って、何頼むかでその日の気分がちょっと出るよね。今日は何の気分？",
    "バーで「いつもの」って言える人、なんかいい。みんなの定番の一杯ってあります？",
    "メニュー見て迷って、結局おすすめ聞いちゃう。そこで好みの一杯に当たるとうれしい。",
    "栄で飲んだ帰り、もう一杯だけ落ち着いて飲みたいなってなることない？",
    "今日はゆっくり一杯飲んで帰りたい気分。そういう夜もあるよね。",
    "お酒の話してたはずなのに、気づいたら全然違う話で盛り上がってる。バーのあの感じ、好きだな。",
    "飲み会の締めって毎回迷う。もう一軒行く？甘いもの食べる？それとも今日は帰る？",
    "一人で行くバーと、誰かと行くバーって楽しみ方が違うよね。どっちも好き。",
    "栄でお店探すとき、最初に見るのって雰囲気？料理？それともお酒の種類？",
]


def main():
    today = datetime.now(ZoneInfo("Asia/Tokyo")).date()
    post = POSTS[today.toordinal() % len(POSTS)]
    heading = f"## 今日のThreads投稿案（{today:%Y年%m月%d日}）"
    note = "これは投稿案です。内容を確認してから、公開する場合だけ手動で実行してください。"
    print(heading)
    print()
    print(post)
    print()
    print("---")
    print(note)
    with open(os.environ["GITHUB_STEP_SUMMARY"], "w", encoding="utf-8") as summary:
        summary.write(f"{heading}\n\n{post}\n\n---\n{note}\n")


if __name__ == "__main__":
    main()
