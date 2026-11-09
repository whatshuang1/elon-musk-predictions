#!/usr/bin/env python3
"""Write timelines/<topic>.md from data/claims.json: every dated statement on the topic, in Musk's own words.
Called by sync.py, so the files follow the live site. Nothing here adds or changes a fact: every value is
read from the dataset, and only statements with a verbatim quote are listed."""
import json
from datetime import date
from pathlib import Path

HUBS = [
    ("tesla-roadster", "the Tesla Roadster", "tesla-roadster-production"),
    ("humans-on-mars", "humans on Mars", "humans-on-mars"),
    ("tesla-cybercab", "the Tesla Cybercab", "cybercab-production-before-2027"),
    ("tesla-optimus", "Tesla Optimus", "optimus-high-volume-external-production-2026"),
    ("grok-5", "Grok 5", "grok-5-release"),
    ("full-self-driving", "Tesla Full Self-Driving", "unsupervised-fsd-texas-california-2025"),
]


def cell(s):
    return " ".join(str(s or "").split()).replace("|", "\\|")


def build(root):
    root = Path(root)
    claims = json.loads((root / "data" / "claims.json").read_text())["claims"]
    pred = json.loads((root / "data" / "predictions.json").read_text())
    paraphrased = {p["id"] for p in pred["predictions"] if p.get("quote_is_paraphrase")}
    out = root / "timelines"
    out.mkdir(exist_ok=True)
    for name, label, slug in HUBS:
        url = f"https://twoweeks.lol/predictions/{slug}/"
        group = [c for c in claims if c["url"].split("#")[0] == url]
        if not group:
            raise SystemExit(f"timelines: no claims for {slug}")
        head = max(group, key=lambda c: (c["url"] == url, c["times_moved"] or 0))
        lines = [f"# Every date Elon Musk has given for {label}", "",
                 f"Source: [twoweeks.lol]({url}), which scores each dated Musk claim against what happened. "
                 f"Generated {date.today():%Y-%m-%d} from [`data/claims.json`](../data/claims.json). CC BY 4.0.", "",
                 f"**Main claim:** {cell(head['title'])}. **Verdict:** {head['status']}. "
                 f"**First said:** {head['first_said']}. **First deadline:** {head['first_deadline']}. "
                 f"**Current deadline:** {head['current_deadline']}. **Times moved:** {head['times_moved']}."]
        moves = head.get("goalpost_history") or []
        if len(moves) > 1:
            lines += ["", "Deadlines in order: " + " → ".join(cell(m) for m in moves) + "."]
        lines += ["", "## What he said", "", "| Said on | Musk's words | Source |", "|---|---|---|"]
        rows = sorted(({**s, "_c": c} for c in group for s in c["timeline"]), key=lambda s: s["date_made"] or "")
        for s in rows:
            if s.get("quote") and s["statement_id"] not in paraphrased:
                lines.append(f"| {s['date_made']} | \"{cell(s['quote'])}\" | [source]({s['source']}) |")
        if len(group) > 1:
            lines += ["", "## Related claims", "", "| Claim | Verdict | First deadline | Current deadline | Times moved |", "|---|---|---|---|---|"]
            for c in sorted(group, key=lambda c: c["first_said"] or ""):
                lines.append(f"| [{cell(c['title'])}]({c['url']}) | {c['status']} | {c['first_deadline'] or ''} | {c['current_deadline'] or ''} | {c['times_moved']} |")
        lines += ["", f"Full history, verdict method and sources: {url}", ""]
        (out / f"{name}.md").write_text("\n".join(lines))
