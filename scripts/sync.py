#!/usr/bin/env python3
"""Pull the latest dataset from twoweeks.lol/data/ and rewrite the stats block in README.md.
Run daily (launchd com.howard.twoweeks-dataset-sync); commits and pushes only when a file changed."""
import os
os.environ["no_proxy"] = "*"
import csv, collections, re, subprocess, sys, urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["predictions.json", "claims.json", "changelog.json", "schema.json", "predictions.csv", "claims.csv"]

def git(*a):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout

git("pull", "--rebase", "-q")
for f in FILES:
    req = urllib.request.Request(f"https://twoweeks.lol/data/{f}", headers={"User-Agent": "twoweeks-dataset-sync"})
    body = urllib.request.urlopen(req, timeout=60).read()
    if len(body) < 1000:
        sys.exit(f"{f}: suspiciously small ({len(body)} bytes); not syncing")
    (ROOT / "data" / f).write_bytes(body)

rows = list(csv.DictReader(open(ROOT / "data" / "claims.csv")))
st = collections.Counter(r["status"] for r in rows)
co = collections.Counter(r["company"] for r in rows)
resolved = st["delivered"] + st["delivered-late"] + st["missed"] + st["cancelled"] + st["partial"]
moves = sum(int(r["times_moved"] or 0) for r in rows)
lines = [
    f"Snapshot {date.today():%Y-%m-%d}: **{len(rows)} claims**, {moves} deadline moves.",
    "",
    "| Verdict | Claims |", "|---|---|",
    *[f"| {k} | {st[k]} |" for k in ["delivered", "delivered-late", "partial", "missed", "cancelled", "disputed", "pending"] if st[k]],
    "",
    f"Of the {resolved} resolved claims, {st['delivered']} were delivered on time ({st['delivered'] / resolved:.0%})." if resolved else "",
    "",
    "By company: " + ", ".join(f"{k} {v}" for k, v in co.most_common()),
]
readme = ROOT / "README.md"
txt = readme.read_text()
txt = re.sub(r"<!-- stats -->.*?<!-- /stats -->", lambda m: "<!-- stats -->\n" + "\n".join(lines) + "\n<!-- /stats -->", txt, flags=re.S)
readme.write_text(txt)

if git("status", "--porcelain").strip():
    git("add", "data", "README.md")
    git("commit", "-q", "-m", f"data: sync {date.today():%Y-%m-%d}")
    git("push", "-q")
    print("synced")
else:
    print("no change")
