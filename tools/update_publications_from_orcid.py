import json
import re
import sys
from urllib.request import Request, urlopen

# This script generates publications.json based on ORCID
# Usage:
# python tools/update_publications_from_orcid.py 0009-0004-0314-8868 _data/publications.json

def get_json(url: str) -> dict:
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def extract_year(work: dict):
    # ORCID often provides published-date: {"year":{"value":"2023"}, ...}
    pd = (work.get("publication-date") or {})
    y = (pd.get("year") or {}).get("value")
    try:
        return int(y) if y else None
    except Exception:
        return None

def extract_doi(external_ids: dict):
    ids = (external_ids or {}).get("external-id", [])
    for e in ids:
        if (e.get("external-id-type") or "").lower() == "doi":
            v = e.get("external-id-value")
            if v:
                return v.strip()
    return None

def main(orcid: str, out_path: str):
    # Public ORCID record (no auth) for works summary:
    summary = get_json(f"https://pub.orcid.org/v3.0/{orcid}/works")

    groups = summary.get("group", [])
    pubs = []
    for g in groups:
        # pick the "work-summary" entries
        summaries = g.get("work-summary", [])
        if not summaries:
            continue

        # Choose the first summary; ORCID groups duplicates/versions
        ws = summaries[0]

        title = (((ws.get("title") or {}).get("title") or {}).get("value") or "").strip()
        if not title:
            continue

        year = extract_year(ws)
        doi = extract_doi(ws.get("external-ids"))

        # "journal-title" is venue-ish; may be empty
        venue = ((ws.get("journal-title") or {}).get("value") or "").strip() or None

        pubs.append({"title": title, "year": year, "venue": venue, "doi": doi})

    # sort: year desc, then title
    pubs.sort(key=lambda p: (p["year"] or 0, p["title"].lower()), reverse=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pubs, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(pubs)} publications to {out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: update_publications_from_orcid.py <ORCID_ID> <output_json_path>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
