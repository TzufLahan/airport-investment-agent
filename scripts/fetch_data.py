"""One-time data acquisition -> committed per-airport metrics snapshot (Step 2).

Run once:  python scripts/fetch_data.py
It writes data/processed/airport_metrics.csv, which IS committed. At runtime the
agent reads that snapshot and never touches these endpoints -- for an investment
tool, a flaky endpoint must never break analysis mid-session (reliability).

Public sources, each used for the metric it measures best:
  * BTS T-100 Domestic Market (TranStats DL_SelectFields form POST) -> passengers
    and market distance per origin-destination, per year. Domestic + US-carrier
    is effectively complete for domestic traffic (foreign carriers cannot fly US
    cabotage). Source for GROWTH (passenger CAGR) and LONG-HAUL share.
  * BTS T-100 aggregates (ArcGIS REST API) -> departures + arrivals per airport
    for the latest year = operations, the load side of CONGESTION.

Volume comes from FAA CY enplanements in the reference table (authoritative total,
including international), so it is not re-fetched here.
"""

import pathlib
import re
import sys
import zipfile

import pandas as pd
import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from airport_agent import config, reference  # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# TranStats T-100 Domestic Market (US carriers) download page. The obfuscated
# query params identify the table; the download is a standard ASP.NET postback.
TRANSTATS_URL = ("https://www.transtats.bts.gov/DL_SelectFields.aspx"
                 "?gnoyr_VQ=FIL&QO_fu146_anzr=Nv4+Pn44vr45")
T100_FIELDS = ["PASSENGERS", "DISTANCE", "ORIGIN", "DEST", "YEAR", "MONTH", "CLASS"]

ARCGIS_OPS_URL = ("https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/"
                  "T100_Domestic_Market_and_Segment_Data/FeatureServer/1/query")


def _hidden(html: str, name: str) -> str:
    """Pull an ASP.NET hidden field's value out of the page HTML."""
    m = re.search(r'id="%s"[^>]*value="([^"]*)"' % re.escape(name), html)
    return m.group(1) if m else ""


def download_t100_market(year: int, session: requests.Session) -> pd.DataFrame:
    """Fetch one year of T-100 Domestic Market via the form POST; cache the zip."""
    raw_zip = config.RAW_DIR / f"t100_market_{year}.zip"
    if not raw_zip.exists():
        print(f"  downloading T-100 Market {year} from TranStats ...")
        html = session.get(TRANSTATS_URL, timeout=60).text
        form = {
            "__EVENTTARGET": "", "__EVENTARGUMENT": "", "__LASTFOCUS": "",
            "__VIEWSTATE": _hidden(html, "__VIEWSTATE"),
            "__VIEWSTATEGENERATOR": _hidden(html, "__VIEWSTATEGENERATOR"),
            "__EVENTVALIDATION": _hidden(html, "__EVENTVALIDATION"),
            "cboGeography": "All", "cboYear": str(year), "cboPeriod": "All",
            "chkDownloadZip": "on", "btnDownload": "Download",
        }
        for field in T100_FIELDS:
            form[field] = "on"
        resp = session.post(TRANSTATS_URL, data=form, timeout=300)
        if resp.content[:2] != b"PK":
            raise RuntimeError(
                f"TranStats returned non-zip for {year} "
                f"(content-type={resp.headers.get('Content-Type')}); form may have changed."
            )
        config.ensure_dirs()
        raw_zip.write_bytes(resp.content)
    zf = zipfile.ZipFile(raw_zip)
    csv_name = next(n for n in zf.namelist()
                    if n.lower().endswith(".csv") and "documentation" not in n.lower())
    return pd.read_csv(zf.open(csv_name), low_memory=False)


def download_ops(session: requests.Session) -> pd.Series:
    """Per-airport operations (departures + arrivals), latest year, from ArcGIS."""
    print("  downloading operations from BTS T-100 ArcGIS API ...")
    params = {
        "where": "1=1", "outFields": "origin,departures,arrivals",
        "returnGeometry": "false", "resultRecordCount": 5000, "f": "json",
    }
    js = session.get(ARCGIS_OPS_URL, params=params, timeout=120).json()
    df = pd.DataFrame(f["attributes"] for f in js["features"])
    df["ops"] = df["departures"].fillna(0) + df["arrivals"].fillna(0)
    return df.set_index("origin")["ops"]


def _passengers_by_origin(market: pd.DataFrame) -> pd.Series:
    """Total departing passengers per origin (cargo rows have 0 pax, so drop out)."""
    d = market[market["PASSENGERS"] > 0]
    return d.groupby("ORIGIN")["PASSENGERS"].sum()


def _longhaul_share(market: pd.DataFrame, origin: str) -> float | None:
    """Percent of an origin's departing passengers on markets over LONG_HAUL_MILES."""
    d = market[(market["ORIGIN"] == origin) & (market["PASSENGERS"] > 0)]
    total = d["PASSENGERS"].sum()
    if total == 0:
        return None
    lh = d[d["DISTANCE"] > config.LONG_HAUL_MILES]["PASSENGERS"].sum()
    return round(100 * lh / total, 1)


def build_snapshot() -> None:
    scope = sorted(reference.in_scope_iatas())
    session = requests.Session()
    session.headers.update({"User-Agent": UA})

    market_latest = download_t100_market(config.LATEST_YEAR, session)
    market_base = download_t100_market(config.GROWTH_BASE_YEAR, session)
    ops = download_ops(session)

    pax_latest = _passengers_by_origin(market_latest)
    pax_base = _passengers_by_origin(market_base)
    years = config.LATEST_YEAR - config.GROWTH_BASE_YEAR

    records = []
    for iata in scope:
        pl = pax_latest.get(iata)
        pb = pax_base.get(iata)
        growth = None
        if pl and pb and pb > 0:
            growth = round(100 * ((pl / pb) ** (1 / years) - 1), 2)
        records.append({
            "iata": iata,
            "pax_base": None if pb is None else int(pb),
            "pax_latest": None if pl is None else int(pl),
            "growth_cagr_pct": growth,
            "longhaul_share_pct": _longhaul_share(market_latest, iata),
            "ops": int(ops.loc[iata]) if iata in ops.index else None,
        })
    out = pd.DataFrame(records)

    # Coverage guard: every in-scope airport must have volume-trend and ops data.
    # A silent gap here would quietly break a Tier-1 congestion score downstream.
    gap = out[out["pax_latest"].isna() | out["ops"].isna()]["iata"].tolist()
    if gap:
        print("  WARNING: missing passenger/ops data for:", gap)

    config.ensure_dirs()
    out.to_csv(config.AIRPORT_METRICS, index=False)
    print(f"\nWrote {len(out)} airports -> {config.AIRPORT_METRICS}")
    print(out.to_string(index=False))


if __name__ == "__main__":
    build_snapshot()
