"""Publish one scheduled Threads post with a rotating JPEG photo."""

import os
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from draft_post import POSTS
from main import main as publish

POST_DAYS = {0, 1, 3, 4, 6}  # Monday, Tuesday, Thursday, Friday, Sunday
START_DATE = date(2026, 10, 25)

# Threads image posts use JPEG photos here. The other uploaded HEIC/WEBP files
# stay in the repository but are not selected by the automatic publisher.
PHOTO_FILES = [
    "4801034125978605363.20c975eb8212b91e54dc0136225cac20.22100120.JPG",
    "IMG_0993.JPG",
    "IMG_3566.JPG",
    "IMG_3567.JPG",
    "IMG_3568.JPG",
    "IMG_3569.JPG",
    "IMG_3570.JPG",
    "IMG_3571.JPG",
    "IMG_3572.JPG",
    "IMG_3573.JPG",
    "IMG_3574.JPG",
    "IMG_3575.JPG",
    "IMG_3576.JPG",
    "IMG_3577.JPG",
    "IMG_3578.JPG",
    "IMG_3579.JPG",
    "IMG_3580.JPG",
    "IMG_3581.JPG",
    "IMG_3582.JPG",
    "IMG_3585.JPG",
    "IMG_3587.JPG",
    "IMG_3589.JPG",
    "IMG_3590.JPG",
    "IMG_3592.JPG",
    "IMG_3593.JPG",
    "IMG_3594.JPG",
    "IMG_7143.JPG",
    "IMG_7144.JPG",
]

SUNDAY_POSTS = [
    "日曜の夜、栄で飲む場所を探している方へ。BarEnd.は日曜日も営業しています。ゆっくり飲みたい夜にどうぞ。",
    "日曜日もBarEnd.は営業しています。日曜の夜、栄で一杯飲みたくなったら気軽に寄ってください。",
    "日曜に飲みたい気分の日もありますよね。BarEnd.は今日も営業中です。栄でお待ちしています。",
    "日曜日の夜もBarEnd.は営業しています。明日からの一週間の前に、栄でゆっくり一杯どうですか？",
]


def main():
    today = datetime.now(ZoneInfo("Asia/Tokyo")).date()
    if today < START_DATE:
        print("自動投稿は10月25日（日）から開始します。")
        return

    if today.weekday() not in POST_DAYS:
        print("今日は投稿予定日ではありません。")
        return

    scheduled_dates = [
        START_DATE + timedelta(days=offset)
        for offset in range((today - START_DATE).days + 1)
        if (START_DATE + timedelta(days=offset)).weekday() in POST_DAYS
    ]
    post_number = len(scheduled_dates) - 1

    if today.weekday() == 6:
        sunday_number = sum(day.weekday() == 6 for day in scheduled_dates) - 1
        post = SUNDAY_POSTS[sunday_number % len(SUNDAY_POSTS)]
    else:
        weekday_number = sum(day.weekday() != 6 for day in scheduled_dates) - 1
        weekday_posts = POSTS[:-1]  # Keep the Sunday opening message for Sundays.
        post = weekday_posts[weekday_number % len(weekday_posts)]

    photo_file = PHOTO_FILES[post_number % len(PHOTO_FILES)]
    os.environ["POST_TEXT"] = post
    os.environ["IMAGE_FILE"] = photo_file
    os.environ["ALT_TEXT"] = "BarEnd.で撮影したカクテルや店内の写真。"

    print(f"今日の投稿文: {post}")
    print(f"今日の写真: {photo_file}")
    publish()


if __name__ == "__main__":
    main()
