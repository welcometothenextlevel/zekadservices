#!/usr/bin/env python3
"""Crawls the site from its base URL and checks that every internal link and asset answers 200.

    python3 tools/check_links.py http://127.0.0.1:4237/zekadservices/
    python3 tools/check_links.py https://welcometothenextlevel.github.io/zekadservices/

Follows <a href>, src, srcset, imagesrcset, data-src, <link href>, CSS url() and the web manifest.
Fails if an internal URL escapes the base folder (a root-absolute path would)."""
import re
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag, urlparse

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4237/zekadservices/"
UA = {"User-Agent": "Mozilla/5.0 zeka-link-check"}


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.base = [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "base" and a.get("href"):
            self.base = a["href"]
        for k in ("href", "src", "data-src", "poster"):
            if a.get(k):
                self.refs.append((tag, a[k]))
        for k in ("srcset", "imagesrcset"):
            if a.get(k):
                self.refs += [(tag, part.strip().split(" ")[0]) for part in a[k].split(",") if part.strip()]


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, "", b""
    except Exception as e:  # noqa
        return 0, str(e), b""


seen, queue, bad, checked = set(), [BASE], [], 0
host = urlparse(BASE).netloc
while queue:
    url = queue.pop(0)
    if url in seen:
        continue
    seen.add(url)
    status, ctype, body = fetch(url)
    checked += 1
    if status != 200:
        bad.append((status, url))
        continue
    if not url.startswith(BASE):
        bad.append(("outside base", url))
        continue
    text = None
    if "html" in ctype:
        text = body.decode("utf-8", "replace")
        p = Refs()
        p.feed(text)
        refs = [r for _, r in p.refs]
    elif "css" in ctype:
        text = body.decode("utf-8", "replace")
        refs = re.findall(r"url\(([^)\"']+|\"[^\"]+\"|'[^']+')\)", text)
        refs = [r.strip("\"'") for r in refs]
    elif url.endswith(".webmanifest"):
        refs = re.findall(r'"src"\s*:\s*"([^"]+)"', body.decode())
    else:
        continue
    for r in refs:
        if r.startswith(("tel:", "mailto:", "data:", "#", "javascript:")):
            continue
        absu = urldefrag(urljoin(url, r))[0]
        if urlparse(absu).netloc != host:
            continue
        if not absu.startswith(BASE):
            bad.append(("root-absolute or outside base", f"{r}  (in {url})"))
            continue
        if absu not in seen:
            queue.append(absu)

print(f"checked {checked} URLs under {BASE}")
for b in bad:
    print("BAD", *b)
sys.exit(1 if bad else 0)
