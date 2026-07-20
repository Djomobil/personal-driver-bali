#!/usr/bin/env python3
"""Download real, freely-licensed photos of Bali landmarks from Wikimedia Commons.

For each landmark below, the script queries the Commons API for the best-rated
photo, downloads it into assets/photos/, resizes it (if Pillow is available)
and records author + license attribution in assets/photos/CREDITS.md.

Run: python3 tools/fetch_photos.py            # all landmarks
     python3 tools/fetch_photos.py tegalalang # only some

Requires outbound access to commons.wikimedia.org and upload.wikimedia.org
(enable them in the Claude Code environment network policy, or run locally).
After downloading, run `python3 tools/build.py` so the pages pick the photos up.
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "photos"
UA = {"User-Agent": "KetutBaliDriver/1.0 (landing page; contact via repo)"}

# filename (without .jpg) -> Commons search query
LANDMARKS = {
    # day-tour / multi-day card slots
    "ubud": "Tegallalang rice terraces",
    "uluwatu": "Uluwatu temple cliff sunset",
    "east-bali": "Pura Lempuyang gate Mount Agung",
    "north-bali": "Sekumpul waterfall",
    "multi-sunrise": "Sidemen valley Bali rice fields",
    "multi-best": "Pura Ulun Danu Bratan",
    "multi-island": "Kelingking beach Nusa Penida",
    # iconic-places gallery slots
    "tanah-lot": "Tanah Lot temple",
    "lempuyang": "Pura Lempuyang Gates of Heaven",
    "tegalalang": "Tegallalang rice terrace",
    "sekumpul": "Sekumpul waterfall Bali",
    "monkey-forest": "Ubud Monkey Forest macaque",
    "melasti": "Melasti Beach Ungasan",
    "handara": "Handara Gate Bali",
    "kelingking": "Kelingking Nusa Penida",
}


def api(params: dict) -> dict:
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def best_image(query: str) -> dict | None:
    data = api({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6, "gsrlimit": 8,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size",
        "iiurlwidth": 1400,
    })
    pages = (data.get("query") or {}).get("pages") or {}
    candidates = []
    for p in pages.values():
        info = (p.get("imageinfo") or [{}])[0]
        w, h = info.get("width", 0), info.get("height", 0)
        if w < 1000 or h < 600 or h > w * 1.2:  # want landscape-ish, decent size
            continue
        candidates.append((p.get("index", 99), info))
    if not candidates:
        return None
    return sorted(candidates, key=lambda c: c[0])[0][1]


def meta(info: dict, field: str) -> str:
    v = ((info.get("extmetadata") or {}).get(field) or {}).get("value", "")
    import re
    return re.sub(r"<[^>]+>", "", v).strip()


def main() -> None:
    only = set(sys.argv[1:])
    DEST.mkdir(parents=True, exist_ok=True)
    credits = ["# Crédits photos (Wikimedia Commons)\n"]
    ok = 0
    for name, query in LANDMARKS.items():
        if only and name not in only:
            continue
        try:
            info = best_image(query)
            if not info:
                print(f"!! {name}: no suitable image found for '{query}'")
                continue
            url = info.get("thumburl") or info["url"]
            out = DEST / f"{name}.jpg"
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                out.write_bytes(r.read())
            try:  # optional recompress
                from PIL import Image
                im = Image.open(out).convert("RGB")
                im.thumbnail((1400, 1400))
                im.save(out, "JPEG", quality=82, optimize=True)
            except ImportError:
                pass
            author = meta(info, "Artist") or "Unknown"
            license_ = meta(info, "LicenseShortName") or "See file page"
            page = info.get("descriptionurl", "")
            credits.append(f"- `{name}.jpg` — {author}, {license_} — {page}")
            print(f"ok {name}: {out.stat().st_size // 1024} KB ({license_})")
            ok += 1
        except Exception as e:  # noqa: BLE001 — report and continue with the next landmark
            print(f"!! {name}: {e}")
    if ok:
        (DEST / "CREDITS.md").write_text("\n".join(credits) + "\n", encoding="utf-8")
        print(f"\n{ok} photos saved. Now run: python3 tools/build.py")


if __name__ == "__main__":
    main()
