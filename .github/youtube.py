#!/usr/bin/env python3
"""Sucht die neuesten Videos passender YouTube-Kanäle und schreibt sie nach youtube.json."""
import html, json, re, sys, urllib.error, urllib.request

CHANNELS = {
    "zCrexpy": "UCKGsnVRGTkEt1qufI9SiHWQ",
    "Papaplatte Gaming": "UCxdaFKaMlRHtVkBeGygsYTw",
    "LetsHugo Gaming": "UCfDLplO_xeVw-E-oPEmGCQg",
    "REWI GAMING": "UCUPu9bnAZXalA7V7illF_kQ",
    "Trymacs": "UC6Gc4KQ1ueDnh8x7plaAD3w",
    "BastiGHG": "UCgZpwegd4AdDlZNrIamIgRw",
    "Felikah Gaming": "UC65jRxRh5LRLiINxkiuODgA",
    "Voltrox": "UC9qSeKSaJ-YolQo4bCpZfIg",
}
HEADERS = {"User-Agent": "Mozilla/5.0", "Cookie": "SOCS=CAI"}
ENTRY = re.compile(r"<entry>.*?<yt:videoId>([^<]+)</yt:videoId>.*?<title>([^<]+)</title>.*?<published>([^<]+)", re.S)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def is_short(video_id):
    request = urllib.request.Request("https://www.youtube.com/shorts/" + video_id, headers=HEADERS)
    try:
        return urllib.request.build_opener(NoRedirect).open(request, timeout=15).status == 200
    except urllib.error.HTTPError:
        return False


def newest(name, channel_id):
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=20) as response:
        feed = response.read().decode("utf-8")
    for video_id, title, published in ENTRY.findall(feed):
        title = html.unescape(title)
        if "#" not in title and not is_short(video_id):
            return {"id": video_id, "title": title, "channel": name, "date": published[:10]}
    return None


videos = []
for name, channel_id in CHANNELS.items():
    try:
        video = newest(name, channel_id)
        if video:
            videos.append(video)
    except Exception as error:
        print("Übersprungen:", name, error, file=sys.stderr)

videos.sort(key=lambda v: v["date"], reverse=True)
if len(videos) < 3:
    sys.exit("Zu wenige Videos gefunden, die Liste bleibt unverändert.")
with open("youtube.json", "w", encoding="utf-8") as out:
    json.dump(videos[:3], out, ensure_ascii=False, indent=1)
    out.write("\n")
