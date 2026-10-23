"""Publish only the reviewed Threads text and optional photo."""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.threads.net/v1.0"
IMAGE_BASE_URL = "https://raw.githubusercontent.com/shunhata1989/threads-auto-post/main/images/%E5%90%8D%E7%A7%B0%E6%9C%AA%E8%A8%AD%E5%AE%9A%E3%83%95%E3%82%A9%E3%83%AB%E3%82%BF%E3%82%99/"


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


def wait_for_container(container_id, timeout=180):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = api_request("GET", f"{container_id}?fields=status,error_message")
        state = status.get("status")
        print(f"写真の準備状況: {state}")
        if state == "FINISHED":
            return
        if state == "ERROR":
            raise RuntimeError(f"Threads photo processing failed: {status.get('error_message', 'Unknown error')}")
        time.sleep(5)
    raise TimeoutError("Threads photo processing did not finish within 180 seconds.")





def main():
    text = os.environ.get("POST_TEXT", "").strip()
    image_file = os.environ.get("IMAGE_FILE", "写真なし").strip()
    image_url = os.environ.get("IMAGE_URL", "").strip()
    alt_text = os.environ.get("ALT_TEXT", "").strip()

    if not text:
        raise SystemExit("POST_TEXT is empty. Add the reviewed post text before running this workflow.")
    if image_file and image_file != "写真なし":
        if image_file != os.path.basename(image_file):
            raise SystemExit("Choose a photo from the workflow list.")
        image_url = IMAGE_BASE_URL + urllib.parse.quote(image_file, safe="")
    if alt_text and not image_url:
        raise SystemExit("ALT_TEXT requires a photo.")

    if image_url:
        parsed_url = urllib.parse.urlparse(image_url)
        if parsed_url.scheme != "https" or not parsed_url.netloc:
            raise SystemExit("The photo URL must use HTTPS.")
        media = {"media_type": "IMAGE", "image_url": image_url, "text": text}
        if alt_text:
            media["alt_text"] = alt_text
    else:
        media = {"media_type": "TEXT", "text": text}

    user = api_request("GET", "me?fields=id")
    creation = api_request("POST", f"{user['id']}/threads", media)
    wait_for_container(creation["id"]) 
    result = api_request(
        "POST",
        f"{user['id']}/threads_publish",
        {"creation_id": creation["id"]},
    )
    post_type = "image post" if image_url else "text post"
    print(f"Published reviewed {post_type}. Threads post ID: {result['id']}")


if __name__ == "__main__":
    main()
