"""Publish only the Threads text explicitly supplied by the user."""

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
    if not text:
        raise SystemExit("POST_TEXT is empty. Add the reviewed post text before running this workflow.")

    user = api_request("GET", "me?fields=id")
    creation = api_request(
        "POST",
        f"{user['id']}/threads",
        {"media_type": "TEXT", "text": text},
    )
    result = api_request(
        "POST",
        f"{user['id']}/threads_publish",
        {"creation_id": creation["id"]},
    )
    print(f"Published approved post. Threads post ID: {result['id']}")


if __name__ == "__main__":
    main()
