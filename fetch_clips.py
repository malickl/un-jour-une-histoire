"""Télécharge des clips libres (Pixabay) pour chaque requête clips/requests/*.json, les recadre en 9:16 (1080x1920, 7 s max, sans son).
Sortie : clips/out/<id>.mp4 + <id>.json (source, auteur). Lancé par GitHub Actions (accès internet)."""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

KEY = os.environ.get("PIXABAY_KEY", "")
ROOT = Path(__file__).resolve().parent
REQ, OUT = ROOT / "clips" / "requests", ROOT / "clips" / "out"
MAXD = 7


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "unjouruneistoire-clips/1.0"}), timeout=60) as r:
        return r.read()


def search(q, n=15):
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
        {"key": KEY, "q": q, "per_page": n, "safesearch": "true", "order": "popular"})
    return json.loads(get(url)).get("hits", [])


def pick(hits, used, query=""):
    best = None
    toks = [t for t in query.lower().split() if len(t) > 2]
    for h in hits:
        if h["id"] in used or h.get("duration", 0) < 4:
            continue
        v = h["videos"].get("large") or h["videos"].get("medium")
        if not v or not v.get("url") or v["height"] < 1000:
            continue
        tags = h.get("tags", "").lower()
        match = sum(t in tags for t in toks)
        if toks and not match:
            continue
        sc = match * 500 + h.get("likes", 0) * 2 + h.get("downloads", 0) / 50 + (v["height"] >= 1800) * 50
        if not best or sc > best[0]:
            best = (sc, h, v)
    return best


def main():
    if not KEY:
        sys.exit("PIXABAY_KEY manquante")
    OUT.mkdir(parents=True, exist_ok=True)
    used = set()
    for j in OUT.glob("*.json"):
        used.add(json.loads(j.read_text(encoding="utf-8")).get("pixabay_id"))
    for rq in sorted(REQ.glob("*.json")):
        for item in json.loads(rq.read_text(encoding="utf-8")):
            dst = OUT / f"{item['id']}.mp4"
            if dst.exists():
                continue
            hits = search(item["query"])
            b = pick(hits, used, item.get("match", item["query"]))
            if not b:
                print("AUCUN résultat :", item)
                continue
            _, h, v = b
            used.add(h["id"])
            tmp = OUT / f"{item['id']}.src.mp4"
            tmp.write_bytes(get(v["url"]))
            ss = float(item.get("start", 0))
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ss), "-i", str(tmp), "-t", str(MAXD), "-an",
                            "-vf", "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,fps=30", "-c:v", "libx264", "-preset", "veryfast",
                            "-crf", "22", "-pix_fmt", "yuv420p", str(dst)], check=True)
            tmp.unlink()
            (OUT / f"{item['id']}.json").write_text(json.dumps(
                {"query": item["query"], "pixabay_id": h["id"], "page": h.get("pageURL"), "user": h.get("user"),
                 "duration": h.get("duration"), "tags": h.get("tags")}, ensure_ascii=False, indent=1), encoding="utf-8")
            print("OK", item["id"], "<-", h.get("pageURL"))


if __name__ == "__main__":
    main()
