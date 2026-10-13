#!/usr/bin/env python3
"""
Criterion 4: an appeal is recorded without overwriting the decision.  <- UNIT 8

run_eval.py only POSTs to /submit, so this does the submit -> appeal -> /log
round trip for 10 submissions and checks each id has BOTH a `decided` entry and
an `under_review` entry.

    python app.py                              # in one terminal
    python appeal_check.py --label before      # in another

Run it 3 times (three separate runs, changing nothing between them).
"""

import argparse
import datetime as dt
import json

import requests

import config
import scenarios

URL = f"http://{config.HOST}:{config.PORT}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=URL)
    args = parser.parse_args()

    # 10 submissions. The text doesn't matter for this criterion, only that
    # each gets a real content_id.
    texts = (scenarios.AI * 2)[:10]
    stamp = dt.datetime.now().strftime("%H%M%S")
    results = []

    for i, text in enumerate(texts, 1):
        row = {"n": i}
        sub = requests.post(f"{args.url}/submit", timeout=90,
                            json={"text": text, "creator_id": f"eval_appeal_{stamp}_{i}"})
        row["submit_status"] = sub.status_code
        if sub.status_code != 200:
            row["error"] = sub.text[:200]
            results.append(row)
            continue
        cid = sub.json()["content_id"]
        row["content_id"] = cid

        app = requests.post(f"{args.url}/appeal", timeout=30,
                            json={"content_id": cid, "reasoning": "I wrote this myself."})
        row["appeal_status"] = app.status_code
        row["appeal_response"] = app.json()
        results.append(row)

    log = requests.get(f"{args.url}/log", timeout=30).json()["entries"]
    passed = 0
    for row in results:
        cid = row.get("content_id")
        mine = [e for e in log if e.get("content_id") == cid]
        row["has_decided"] = any(e.get("status") == "decided" for e in mine)
        row["has_under_review"] = any(e.get("status") == "under_review" for e in mine)
        row["pass"] = row["has_decided"] and row["has_under_review"]
        passed += row["pass"]
        row["log_entries"] = mine

    print(json.dumps(results, indent=2))
    print(f"\nCriterion 4: {passed}/10 appeals recorded with the decision kept")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_{dt.datetime.now():%Y-%m-%d_%H%M}{label}.md"
    path.write_text(
        f"# Appeal check{label}\n\nProduced by: `appeal_check.py::main`\n\n"
        f"**{passed}/10**\n\n```json\n{json.dumps(results, indent=2)}\n```\n",
        encoding="utf-8")
    print(f"Wrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
