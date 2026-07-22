"""One-time NPIAS acquisition -> committed per-airport "second opinion" snapshot.

Run once:  python scripts/fetch_npias.py

Writes reference/npias.csv (committed). Two INDEPENDENT FAA signals per airport,
consumed only by the second-opinion layer -- never by the deterministic score:

  * dev_cost_2025_2029 -- the FAA's own five-year development-cost estimate,
    parsed per airport from NPIAS 2025-2029 Appendix A (the authoritative list of
    NPIAS airports). Available for all in-scope airports.
  * capacity_2028 / capacity_2033 -- the FAA's forward runway-capacity outlook,
    transcribed from the NPIAS Narrative, Figure 1. That figure is a graphic (not
    machine-readable text), so the flagged airports are encoded below from a
    manual, cross-checked reading; every other airport is 0 ("not flagged").
    Ordinal: 0 not flagged, 1 congested, 2 capacity constrained, 3 severe.
    (FAA thresholds: congested = >60% of hourly runway capacity >=50% of the time;
     constrained = >80% >=50%; severe = >90% >=75%.)

Reproducible + offline like scripts/fetch_data.py: the ~12 MB Appendix A PDF is
cached under data/raw/ (gitignored); only the small CSV is committed. At runtime
the agent reads the CSV and never touches faa.gov.
"""

import pathlib
import re
import sys

import pandas as pd
import requests
from pypdf import PdfReader

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from airport_agent import config, reference  # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

APPENDIX_A_URL = ("https://www.faa.gov/sites/faa.gov/files/airports/planning_capacity/"
                  "npias/current/ARP-NPIAS-2025-2029-Appendix-A.pdf")

# FAA National Capacity Outlook -- NPIAS 2025-2029 Narrative, Figure 1 (p. 9).
# (2028, 2033) runway-capacity status per airport, transcribed from the figure
# (a graphic) and cross-checked against the FAA's published totals: 11 airports
# capacity-constrained by 2028, 14 by 2033, and 13 more at risk of congestion.
NOT_FLAGGED, CONGESTED, CONSTRAINED, SEVERE = 0, 1, 2, 3
CAPACITY_OUTLOOK: dict[str, tuple[int, int]] = {
    "ATL": (CONGESTED, CONSTRAINED),   "BOS": (CONSTRAINED, SEVERE),
    "BWI": (CONGESTED, CONSTRAINED),   "CLT": (NOT_FLAGGED, CONGESTED),
    "DAL": (CONGESTED, CONGESTED),     "DCA": (CONSTRAINED, CONSTRAINED),
    "DEN": (CONGESTED, CONGESTED),     "DFW": (CONGESTED, CONGESTED),
    "EWR": (CONSTRAINED, SEVERE),      "FLL": (NOT_FLAGGED, CONGESTED),
    "HOU": (CONGESTED, CONGESTED),     "IAD": (NOT_FLAGGED, CONGESTED),
    "JFK": (CONSTRAINED, SEVERE),      "LAS": (CONSTRAINED, SEVERE),
    "LAX": (CONSTRAINED, CONSTRAINED), "LGA": (CONSTRAINED, CONSTRAINED),
    "MDW": (NOT_FLAGGED, CONGESTED),   "MIA": (CONGESTED, CONSTRAINED),
    "ORD": (CONSTRAINED, CONSTRAINED), "PHL": (NOT_FLAGGED, CONGESTED),
    "PHX": (CONGESTED, CONGESTED),     "SAN": (CONSTRAINED, SEVERE),
    "SAT": (CONGESTED, CONGESTED),     "SEA": (CONSTRAINED, SEVERE),
    "SFO": (CONSTRAINED, SEVERE),      "SJC": (CONGESTED, CONGESTED),
    "SNA": (CONGESTED, CONGESTED),
}


def _validate_outlook() -> None:
    """Guard the manual transcription against the FAA's published counts."""
    c28 = sum(1 for a, _ in CAPACITY_OUTLOOK.values() if a >= CONSTRAINED)
    c33 = sum(1 for _, b in CAPACITY_OUTLOOK.values() if b >= CONSTRAINED)
    at_risk = sum(1 for a, b in CAPACITY_OUTLOOK.values() if max(a, b) == CONGESTED)
    if (c28, c33, at_risk) != (11, 14, 13):
        raise AssertionError(
            f"capacity outlook transcription drifted: got constrained-2028={c28}, "
            f"constrained-2033={c33}, at-risk={at_risk}; expected 11/14/13.")


def download_appendix_a(session: requests.Session) -> pathlib.Path:
    """Cache the Appendix A PDF under data/raw/ (gitignored); download if absent."""
    pdf = config.RAW_DIR / "npias_appendix_a.pdf"
    if not pdf.exists():
        print("  downloading NPIAS 2025-2029 Appendix A (~12 MB) ...")
        resp = session.get(APPENDIX_A_URL, timeout=180)
        if resp.content[:5] != b"%PDF-":
            raise RuntimeError("Appendix A download was not a PDF; the URL may have moved.")
        config.ensure_dirs()
        pdf.write_bytes(resp.content)
    return pdf


def parse_dev_costs(pdf_path: pathlib.Path, codes: list[str]) -> dict[str, int]:
    """Per-airport 2025-2029 development cost from Appendix A.

    Each airport row reads: City Airport LocID Own Cat Hub Enplaned Based DevCost,
    immediately followed by the NEXT airport's (capitalised) city. We anchor on
    'LocID Own Cat Hub' and take the LAST integer before that next city name -- the
    development cost is always the final numeric column. Reading the last number,
    rather than a fixed position, survives two Appendix-A quirks: pypdf sometimes
    splits a long enplanement across a space (e.g. '23,880,45 9'), and joint
    civil-military fields carry a non-standard ownership code (e.g. CHS -> 'MA').
    Running page headers are stripped first so a page-break split still matches.
    """
    text = "\n".join(pg.extract_text() or "" for pg in PdfReader(str(pdf_path)).pages)
    text = re.sub(r"National Plan of Integrated Airport Systems \(2025-2029\)", " ", text)
    text = re.sub(r"\bA-\d+\b", " ", text)          # running appendix page numbers
    text = re.sub(r"\s+", " ", text)

    costs: dict[str, int] = {}
    for code in codes:
        anchor = re.search(
            rf"\b{re.escape(code)}\s+[A-Z]{{1,2}}\s+(?:P|CS|R|GA)\s+[LMSN]\s+", text)
        if not anchor:
            continue
        nums: list[int] = []
        for tok in text[anchor.end():].split(" "):
            if re.fullmatch(r"[\d,]+", tok):
                nums.append(int(tok.replace(",", "")))
            elif re.match(r"[A-Z][a-z]", tok):   # next airport's city -> row ended
                break
        if nums:
            costs[code] = nums[-1]
    return costs


def build_snapshot() -> None:
    _validate_outlook()
    codes = sorted(reference.in_scope_iatas())

    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    pdf = download_appendix_a(session)
    costs = parse_dev_costs(pdf, codes)

    # Coverage guard: a silently missing airport would give a hole in the overlay.
    missing = [c for c in codes if c not in costs]
    if missing:
        print("  WARNING: no development cost parsed for:", missing)

    records = []
    for code in codes:
        c28, c33 = CAPACITY_OUTLOOK.get(code, (NOT_FLAGGED, NOT_FLAGGED))
        records.append({
            "iata": code,
            "npias_locid": code,
            "dev_cost_2025_2029": costs.get(code),
            "capacity_2028": c28,
            "capacity_2033": c33,
        })
    out = pd.DataFrame(records)
    out["dev_cost_2025_2029"] = out["dev_cost_2025_2029"].astype("Int64")

    config.REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.NPIAS_CSV, index=False)
    print(f"\nWrote {len(out)} airports -> {config.NPIAS_CSV}  "
          f"(dev-cost parsed for {len(costs)}/{len(codes)}, "
          f"{len(CAPACITY_OUTLOOK)} capacity-flagged)")
    print(out.to_string(index=False))


if __name__ == "__main__":
    build_snapshot()
