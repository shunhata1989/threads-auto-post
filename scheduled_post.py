"""Publish one scheduled Threads post with a rotating JPEG photo."""

import os
import os
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from draft_post import POSTS
from main import main as publish


SUNDAY_POSTS_FROM_NOV_22 = [
    "日曜日も営業しています。栄で一杯飲みたくなったら、気軽にお立ち寄りください。",
    "明日からまた一週間ですね。日曜の夜にゆっくり飲みたい方は、BarEnd.でお待ちしています。",
    "休日の最後に、もう少しだけゆっくり過ごしませんか？BarEnd.は日曜日も営業しています。",
    "日曜の栄で、カラオケやゲームを楽しみながら一杯いかがでしょうか。今日も営業しています🎤",
]

WEEKDAY_POSTS_FROM_DEC_15 = [
    "カクテルの名前が分からなくても大丈夫です。「甘めがいい」など、お好みを教えていただければ一緒に考えます。",
    "一杯目はビールにするか、カクテルにするか。メニューを見ると迷うこともありますね。今日はどちらの気分でしょうか🍺",
    "乾杯のあとは、ゆっくりお話しするのも、カラオケで盛り上がるのもいいですね。今夜はどんな過ごし方をされますか？",
    "カラオケの一曲目って意外と迷いませんか？最初に歌う曲は決めている派でしょうか🎤",
    "甘めのカクテルが飲みたい日も、すっきりした一杯がいい日もありますね。その日の気分でお選びください🍸",
    "栄で飲んだあとに「もう一軒行こうか」となったら、BarEnd.も候補に入れていただけるとうれしいです。",
    "飲み会のお店選びでは、雰囲気・場所・遊べる要素のどれを重視しますか？幹事さんの参考にしたいです。",
    "ビールを飲みながら話す夜も、カクテルをゆっくり楽しむ夜も。どちらもいい時間ですね。",
    "バーで注文に迷ったら、スタッフに気軽に声をかけてください。好みに合う一杯をご提供しますよ！！",
    "友達とゲームを始めると、つい本気になってしまうことがありますね。飲みながら遊ぶのも楽しいです🎮",
    "初めてのお店に入るときは少し緊張しますよね。BarEnd.は初めての方も歓迎しています。",
    "今日は仕事終わりに一杯、という方も多いでしょうか。栄でお飲みになる際は、ぜひお立ち寄りください。",
    "カラオケは歌うのはもちろん、人の選曲を聴くのも楽しいです。皆さんの十八番は何でしょうか🎶",
    "ビールの苦みが恋しい日と、カクテルの香りを楽しみたい日。今夜はどちらでしょうか。",
    "名古屋・栄で二軒目をお探しでしたら、BarEnd.へどうぞ。カラオケやゲームも楽しめます。",
    "お酒の強さより、好きな味で選ぶのがいちばんです。迷ったときは、甘め・さっぱりなど好みを教えてください。",
    "友達と話し込んでいたら、思ったより時間が経っていることがありますね。そんな夜もいいものです。",
    "飲み会では、みんなで同じものを頼みますか？それぞれ好きなものを選びますか？お店ごとに違って面白いですね。",
    "一人でゆっくり飲みたい夜も、誰かと楽しく過ごしたい夜もありますね。ご自分のペースでお楽しみください。",
    "「もう一曲だけ」と言いながら、つい何曲も歌ってしまうことがありますね。カラオケ好きの方、お待ちしています🎤",
    "カクテルは色で選ぶのも楽しいですが、味の好みから選ぶのもおすすめです。お気軽にご相談ください。",
    "名古屋・栄で飲む場所をお探しでしたら、BarEnd.へどうぞ。初めての方もお待ちしています。",
    "仕事の話をする夜も、くだらない話で笑う夜もありますね。飲みながらだと、いつもより話しやすいこともあります。",
    "今日はいつもの一杯にしますか？それとも、普段あまり頼まないものを試してみますか🍸",
    "飲み会の二軒目は、カラオケに行くかバーで話すか悩みますね。BarEnd.ならどちらも楽しめます。",
    "ビールにもカクテルにも、それぞれ良さがあります。最初の一杯は何を選ぶことが多いですか？",
    "お酒に詳しくなくても、バーは気軽に楽しめる場所です。好みを伝えながら一杯選んでみてください。",
    "栄で遊んだ帰りにもう少し話したくなったら、BarEnd.でゆっくり過ごしていってください。",
    "カラオケやゲームをしながら飲む夜も、いつもと違った楽しさがあります。今夜の予定にいかがでしょうか🎮",
    "今週もお疲れさまでした。最後の一杯は、いつものお気に入りにしますか？新しいものにしてみますか？",
]

NEW_YEAR_POST = (
    "新年あけましておめでとうございます🎍\n"
    "昨年はBarEnd.をご利用いただき、ありがとうございました。\n"
    "1月1日は店休日とさせていただきます。本年もどうぞよろしくお願いいたします。"
)

YEAR_END_POST = (
    "本年もBarEnd.をご利用いただき、ありがとうございました。\n"
    "皆さま、どうぞ良いお年をお迎えください。\n"
    "来年もよろしくお願いいたします。"
)


POST_DAYS = {0, 1, 3, 4, 6}  # Monday, Tuesday, Thursday, Friday, Sunday
START_DATE = date(2026, 10, 23)

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
    if (
        os.environ.get("SCHEDULE_CRON") == "0 3 1 1 *"
        and today != date(2027, 1, 1)
    ):
        print("昼12時の特別投稿は2027年1月1日のみです。")
        return
    if today < START_DATE:
        print("自動投稿は10月23日（金）から開始します。")
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

    if today == date(2026, 12, 31):
        post = YEAR_END_POST
    elif today == date(2027, 1, 1):
        if os.environ.get("SCHEDULE_CRON") == "0 10 * * 0,1,2,4,5":
            print("1月1日の19時投稿はスキップし、新年の投稿は12時に行います。")
            return
        post = NEW_YEAR_POST
    elif today.weekday() == 6:
        if today >= date(2026, 11, 22):
            new_sunday_number = sum(
                day.weekday() == 6 and day >= date(2026, 11, 22)
                for day in scheduled_dates
            ) - 1
            post = SUNDAY_POSTS_FROM_NOV_22[
                new_sunday_number % len(SUNDAY_POSTS_FROM_NOV_22)
            ]
        else:
            sunday_number = sum(day.weekday() == 6 for day in scheduled_dates) - 1
            post = SUNDAY_POSTS[sunday_number % len(SUNDAY_POSTS)]
    else:
        weekday_number = sum(day.weekday() != 6 for day in scheduled_dates) - 1
        if today >= date(2026, 12, 15):
            new_weekday_number = sum(
                day.weekday() != 6
                and day >= date(2026, 12, 15)
                and day not in {date(2026, 12, 31), date(2027, 1, 1)}
                for day in scheduled_dates
            ) - 1
            post = WEEKDAY_POSTS_FROM_DEC_15[
                new_weekday_number % len(WEEKDAY_POSTS_FROM_DEC_15)
            ]
        else:
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
