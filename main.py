"""Publish only the reviewed Threads text and optional photo."""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.threads.net/v1.0"


def api_request(method, path, params=None):
    token = os.environ["THREADS_ACCESS_TOKEN"]
    url = f"{API}/{path}"
    headers = {"Authorization": f"Bearer {token}"}
    data = urllib.parse.urlencode(params).encode() if params is not None else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Threads API returned HTTP {error.code}: {details}") from error


def main():
    text = os.environ.get("POST_TEXT", "").strip()
    image_url = os.environ.get("IMAGE_URL", "").strip()
    alt_text = os.environ.get("ALT_TEXT", "").strip()

    if not text:
        raise SystemExit("POST_TEXT is empty. Add the reviewed post text before running this workflow.")
    if alt_text and not image_url:
        raise SystemExit("ALT_TEXT requires IMAGE_URL.")

    if image_url:
        parsed_url = urllib.parse.urlparse(image_url)
        if parsed_url.scheme != "https" or not parsed_url.netloc:
            raise SystemExit("IMAGE_URL must be a publicly accessible HTTPS image URL.")
        media = {"media_type": "IMAGE", "image_url": image_url, "text": text}
        if alt_text:
            media["alt_text"] = alt_text
    else:
        media = {"media_type": "TEXT", "text": text}

    user = api_request("GET", "me?fields=id")
    creation = api_request("POST", f"{user['id']}/threads", media)
    result = api_request(
        "POST",
        f"{user['id']}/threads_publish",
        {"creation_id": creation["id"]},
    )
    post_type = "image post" if image_url else "text post"
    print(f"Published reviewed {post_type}. Threads post ID: {result['id']}")


if __name__ == "__main__":
    main()
