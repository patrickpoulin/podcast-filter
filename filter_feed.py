"""
Builds filtered copies of podcast RSS feeds.

Reads the list of feeds from docs/feeds.json (the web page in docs/index.html edits that file)
and writes one filtered feed per entry to docs/feeds/<id>.xml, which GitHub Pages serves.

Each entry in feeds.json looks like:
  {
    "id": "the-herd-prime-cuts",          # becomes the file name / URL
    "title": "The Herd - Prime Cuts",       # name shown in your podcast app
    "source_url": "https://.../podcast.rss",
    "include": ["prime cuts"],               # keep titles containing ANY of these (empty = keep all)
    "exclude": [],                           # then drop titles containing ANY of these
    "max_items": 100,                        # newest N matches to keep (0 = all)
    "artwork": "https://...", "show_name": "..."   # only used by the web page
  }

Matching is case-insensitive "contains", the same rule the web page's preview uses.
Uses only the Python standard library. Episodes are copied byte-for-byte, so audio links,
artwork and show notes stay exactly as the publisher wrote them.
"""

import html
import json
import os
import re
import sys
import urllib.request

CONFIG = os.environ.get("CONFIG", "docs/feeds.json")
OUT_DIR = os.environ.get("OUT_DIR", "docs/feeds")

ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")
ITEM_RE = re.compile(r"<item\b.*?</item>", re.S | re.I)
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.S | re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (podcast-filter)"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def clean_terms(values):
    return [str(v).strip().lower() for v in (values or []) if str(v).strip()]


def plain_title(item_xml):
    m = TITLE_RE.search(item_xml)
    if not m:
        return ""
    t = m.group(1).strip()
    if t.startswith("<![CDATA[") and t.endswith("]]>"):
        t = t[9:-3]
    return html.unescape(t).lower()


def wanted(title, include, exclude):
    if include and not any(term in title for term in include):
        return False
    if any(term in title for term in exclude):
        return False
    return True


def build(entry, source_cache):
    """Returns (xml_text, kept_count, total_count). Raises ValueError on problems."""
    url = entry["source_url"]
    if url not in source_cache:
        source_cache[url] = fetch(url)
    text = source_cache[url]

    items = list(ITEM_RE.finditer(text))
    if not items:
        raise ValueError("no episodes found - is source_url a podcast RSS feed?")

    include = clean_terms(entry.get("include"))
    exclude = clean_terms(entry.get("exclude"))
    kept = [m.group(0) for m in items if wanted(plain_title(m.group(0)), include, exclude)]
    max_items = int(entry.get("max_items") or 0)
    if max_items > 0:
        kept = kept[:max_items]
    if not kept:
        raise ValueError(f"none of the {len(items)} episodes matched include={include} exclude={exclude}")

    head = text[: items[0].start()]
    tail = text[items[-1].end():]
    # Stop podcast apps from following the publisher's redirect back to the full feed.
    head = re.sub(r"\s*<itunes:new-feed-url\b[^>]*>.*?</itunes:new-feed-url>", "", head, flags=re.S | re.I)
    # Remove the show's global ID so apps don't merge this with the original show.
    head = re.sub(r"\s*<podcast:guid\b[^>]*>.*?</podcast:guid>", "", head, flags=re.S | re.I)
    title = str(entry.get("title") or "").strip()
    if title:
        # The first <title> before any episode is the show's title.
        head = TITLE_RE.sub(lambda _: f"<title>{html.escape(title)}</title>", head, count=1)

    return head + "\n".join(kept) + tail, len(kept), len(items)


def main():
    try:
        with open(CONFIG, encoding="utf-8") as f:
            feeds = json.load(f).get("feeds", [])
    except FileNotFoundError:
        feeds = []

    os.makedirs(OUT_DIR, exist_ok=True)
    source_cache = {}
    ok, failed, valid_ids = 0, 0, set()

    for entry in feeds:
        fid = str(entry.get("id", ""))
        if not ID_RE.match(fid) or not entry.get("source_url"):
            print(f"::warning::Skipping entry with bad id or missing source_url: {fid!r}")
            failed += 1
            continue
        valid_ids.add(fid)
        try:
            xml, kept, total = build(entry, source_cache)
        except Exception as e:  # one broken feed shouldn't stop the others
            # Leave any previous version of this feed in place.
            print(f"::warning::{fid}: {e}")
            failed += 1
            continue
        with open(os.path.join(OUT_DIR, f"{fid}.xml"), "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"{fid}: kept {kept} of {total} episodes")
        ok += 1

    # Remove feeds that were deleted from feeds.json.
    for name in os.listdir(OUT_DIR):
        if name.endswith(".xml") and name[:-4] not in valid_ids:
            os.remove(os.path.join(OUT_DIR, name))
            print(f"removed {name} (no longer in feeds.json)")

    print(f"Done: {ok} built, {failed} with problems.")
    if feeds and ok == 0:
        sys.exit("No feeds could be built.")


if __name__ == "__main__":
    main()
