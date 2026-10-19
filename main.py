import os
import urllib.parse
import urllib.request
import json

API = "https://graph.threads.net/v1.0"

user_id = os.environ.get("THREADS_USER_ID")
access_token = os.environ.get("THREADS_ACCESS_TOKEN")
post_text = os.environ.get("POST_TEXT")

if not user_id or not access_token or not post_text:
    raise SystemExit("設定が足りません。Threadsの設定が必要です。")

def send(path, values):
    data = urllib.parse.urlencode(values).encode()
    request = urllib.request.Request(
        f"{API}/{path}",
        data=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())

container = send(
    f"{user_id}/threads",
    {"media_type": "TEXT", "text": post_text},
)

result = send(
    f"{user_id}/threads_publish",
    {"creation_id": container["id"]},
)

print("投稿できました:", result["id"])
