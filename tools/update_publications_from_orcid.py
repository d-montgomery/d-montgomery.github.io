import json
import re
import sys
from difflib import SequenceMatcher
from urllib.request import Request, urlopen

# This script generates publications.json based on ORCID
# Usage:
# python3 tools/update_publications_from_orcid.py 0009-0004-0314-8868 _data/publications.json

ARXIV_DOI_PREFIX = "10.48550/arxiv."

def get_json(url: str) -> dict:
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def extract_year(work: dict):
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

def extract_put_code(ws: dict):
    pc = ws.get("put-code")
    try:
        return int(pc) if pc is not None else None
    except Exception:
        return None

def extract_authors_from_work(full_work: dict):
    """
    Returns a list of author names from ORCID work record contributors (if present).
    """
    out = []
    contribs = (full_work.get("contributors") or {}).get("contributor") or []
    for c in contribs:
        name = ((c.get("credit-name") or {}).get("value") or "").strip()
        if name:
            out.append(name)
    # de-dupe while preserving order
    seen = set()
    deduped = []
    for a in out:
        k = a.lower()
        if k not in seen:
            seen.add(k)
            deduped.append(a)
    return deduped

def get_work_detail(orcid: str, put_code: int) -> dict:
    return get_json(f"https://pub.orcid.org/v3.0/{orcid}/work/{put_code}")

# -------------------------
# Deduplication helpers
# -------------------------
def norm_title(t: str) -> str:
    """Normalize a title to improve near-duplicate matching."""
    t = (t or "").lower()
    t = re.sub(r"[\W_]+", " ", t)   # remove punctuation/underscores
    t = re.sub(r"\s+", " ", t).strip()
    return t

def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def is_arxiv_doi(doi: str | None) -> bool:
    if not doi:
        return False
    return doi.strip().lower().startswith(ARXIV_DOI_PREFIX)

def pub_score(p: dict) -> tuple:
    """
    Higher is better.
    Priority:
      1) non-arXiv DOI > arXiv DOI > no DOI
      2) has venue
      3) has year
      4) overall completeness (count of non-empty fields)
    """
    doi = (p.get("doi") or "").strip()
    venue = p.get("venue")
    year = p.get("year")

    doi_score = 2 if (doi and not is_arxiv_doi(doi)) else (1 if doi else 0)
    venue_score = 1 if venue else 0
    year_score = 1 if year else 0
    completeness = sum(1 for _, v in p.items() if v not in (None, "", [], {}))
    return (doi_score, venue_score, year_score, completeness)

def dedupe_pubs_by_title(pubs: list[dict], threshold: float = 0.94) -> list[dict]:
    """
    Deduplicate publications by near-matching titles.
    If two titles are similar (>= threshold), keep the higher-scoring record.
    """
    kept: list[dict] = []
    kept_norm: list[str] = []

    for p in pubs:
        t_norm = norm_title(p.get("title", ""))
        if not t_norm:
            kept.append(p)
            kept_norm.append(t_norm)
            continue

        best_i = -1
        best_sim = 0.0
        for i, kt in enumerate(kept_norm):
            if not kt:
                continue
            s = title_similarity(t_norm, kt)
            if s > best_sim:
                best_sim = s
                best_i = i

        if best_sim >= threshold and best_i >= 0:
            # near-duplicate: keep the better one
            if pub_score(p) > pub_score(kept[best_i]):
                kept[best_i] = p
                kept_norm[best_i] = t_norm
            # else drop p
        else:
            kept.append(p)
            kept_norm.append(t_norm)

    return kept

def main(orcid: str, out_path: str):
    summary = get_json(f"https://pub.orcid.org/v3.0/{orcid}/works")

    groups = summary.get("group", [])
    pubs = []

    for g in groups:
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
        venue = ((ws.get("journal-title") or {}).get("value") or "").strip() or None

        # Fetch full work to extract contributors/authors (if available)
        put_code = extract_put_code(ws)
        authors = None
        if put_code is not None:
            try:
                full = get_work_detail(orcid, put_code)
                authors = extract_authors_from_work(full)
                if not authors:
                    authors = None
            except Exception:
                authors = None

        pubs.append({
            "title": title,
            "year": year,
            "venue": venue,
            "doi": doi,
            "authors": authors
        })

    # Dedupe near-duplicate titles, prefer non-arXiv/journal versions
    before = len(pubs)
    pubs = dedupe_pubs_by_title(pubs, threshold=0.94)
    after = len(pubs)

    # Sort: year desc, then title
    pubs.sort(key=lambda p: (p.get("year") or 0, (p.get("title") or "").lower()), reverse=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pubs, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(pubs)} publications to {out_path} (deduped {before-after})")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: update_publications_from_orcid.py <ORCID_ID> <output_json_path>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
