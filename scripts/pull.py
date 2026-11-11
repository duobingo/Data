#!/usr/bin/env python3
"""Daily market-data pull for a set of tracked US stocks.

Runs on GitHub Actions (which can reach market-data sites that the Claude cloud
environment cannot). Writes:
  data/latest.md      human/agent-readable summary (what the scheduled tasks read)
  data/latest.json    same data, structured
  data/snapshots/     one JSON per run, kept for history
  data/estimates_history.csv   daily EPS/revenue estimate snapshots (for revision tracking)

Every section is independent: if one source fails, the rest still run and the
failure is listed under "Data quality".
"""
import argparse
import csv
import datetime as dt
import json
import os
import pathlib
import sys
import time
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

import requests
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ET_TZ = ZoneInfo("America/New_York")

SEC_UA = os.environ.get("SEC_USER_AGENT") or "market-data/1.0 (research)"
FINNHUB_KEY = os.environ.get("FINNHUB_API_KEY", "").strip()

ERRORS: list[str] = []
S = requests.Session()
S.headers["User-Agent"] = SEC_UA


def err(section, msg):
    ERRORS.append(f"{section}: {msg}")
    print(f"[warn] {section}: {msg}", file=sys.stderr)


def get_json(url, params=None, headers=None, timeout=20, tries=2):
    last = None
    for i in range(tries):
        try:
            r = S.get(url, params=params, headers=headers, timeout=timeout)
            if r.status_code == 429:
                time.sleep(3 + 3 * i)
                last = f"HTTP 429 {url}"
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
            time.sleep(1)
    raise RuntimeError(last)


def pct(a, b):
    try:
        return round((a / b - 1) * 100, 2)
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------- mode / window

def pick_mode(now_et, forced):
    if forced:
        return forced
    wd, hm = now_et.weekday(), now_et.hour * 60 + now_et.minute
    if wd == 6:
        return "weekly"
    if wd < 5 and 7 * 60 <= hm <= 9 * 60 + 25:
        return "premarket"
    if wd < 5 and 16 * 60 + 5 <= hm <= 20 * 60:
        return "close"
    if wd < 5 and 9 * 60 + 40 <= hm <= 15 * 60 + 59:
        return "intraday"
    return None


# ---------------------------------------------------------------- prices

def pull_prices(tickers, mode):
    out = {}
    try:
        import yfinance as yf
        hist = yf.download(tickers, period="1y", interval="1d", auto_adjust=False,
                           group_by="ticker", progress=False, threads=False)
    except Exception as e:  # noqa: BLE001
        err("prices/yahoo", str(e))
        hist = None

    for t in tickers:
        row = {"ticker": t}
        try:
            if hist is None:
                raise RuntimeError("no Yahoo data")
            df = hist[t] if len(tickers) > 1 else hist
            df = df.dropna(subset=["Close"])
            if df.empty:
                raise RuntimeError("empty")
            c = df["Close"]
            last, prev = float(c.iloc[-1]), float(c.iloc[-2])
            row.update({
                "close_date": str(df.index[-1].date()),
                "close": round(last, 2),
                "day_pct": pct(last, prev),
                "5d_pct": pct(last, float(c.iloc[-6])) if len(c) > 6 else None,
                "1m_pct": pct(last, float(c.iloc[-22])) if len(c) > 22 else None,
                "3m_pct": pct(last, float(c.iloc[-64])) if len(c) > 64 else None,
                "52w_high": round(float(df["High"].max()), 2),
                "52w_low": round(float(df["Low"].min()), 2),
            })
            row["from_52w_high_pct"] = pct(last, row["52w_high"])
            vol = df["Volume"]
            if len(vol) > 21:
                avg = float(vol.iloc[-21:-1].mean())
                row["vol_vs_20d"] = round(float(vol.iloc[-1]) / avg, 2) if avg else None
        except Exception as e:  # noqa: BLE001
            err(f"prices/yahoo/{t}", str(e))
        out[t] = row

    # premarket price (Yahoo intraday with extended hours)
    if mode == "premarket" and hist is not None:
        try:
            import yfinance as yf
            pre = yf.download(tickers, period="1d", interval="5m", prepost=True,
                              group_by="ticker", progress=False, threads=False)
            for t in tickers:
                try:
                    df = (pre[t] if len(tickers) > 1 else pre).dropna(subset=["Close"])
                    if not df.empty and out[t].get("close"):
                        p = float(df["Close"].iloc[-1])
                        out[t]["premarket"] = round(p, 2)
                        out[t]["premarket_pct"] = pct(p, out[t]["close"])
                except Exception:  # noqa: BLE001
                    pass
        except Exception as e:  # noqa: BLE001
            err("prices/premarket", str(e))

    # second source: Finnhub quote
    if FINNHUB_KEY:
        for t in tickers:
            try:
                q = get_json("https://finnhub.io/api/v1/quote", {"symbol": t, "token": FINNHUB_KEY})
                out[t]["finnhub_last"] = q.get("c")
                out[t]["finnhub_prev_close"] = q.get("pc")
                y = out[t].get("close")
                cands = [v for v in (q.get("c"), q.get("pc")) if v]
                out[t]["verified"] = bool(y and any(abs(v / y - 1) < 0.005 for v in cands))
                time.sleep(1.05)
            except Exception as e:  # noqa: BLE001
                err(f"prices/finnhub/{t}", str(e))
                out[t]["verified"] = False
    else:
        for t in tickers:
            out[t]["verified"] = False
        err("prices/finnhub", "FINNHUB_API_KEY not set — prices are single-source (unverified)")
    return out


# ---------------------------------------------------------------- SEC EDGAR

FORMS = {"8-K", "8-K/A", "4", "10-Q", "10-K", "SC 13D", "SC 13D/A", "SC 13G", "SC 13G/A",
         "SCHEDULE 13D", "SCHEDULE 13D/A", "SCHEDULE 13G", "SCHEDULE 13G/A",
         "S-3", "S-3ASR", "424B5", "424B2", "DEF 14A", "6-K"}

ITEM_8K = {
    "1.01": "Material agreement", "1.02": "Agreement terminated", "1.03": "Bankruptcy",
    "2.01": "Acquisition/disposition completed", "2.02": "Earnings results",
    "2.03": "New debt/obligation", "2.05": "Restructuring/exit costs", "2.06": "Impairment",
    "3.01": "Delisting notice", "3.02": "Unregistered equity sale", "4.01": "Auditor change",
    "4.02": "Prior financials unreliable", "5.01": "Change in control",
    "5.02": "Executive/director change", "5.03": "Bylaws/charter change",
    "5.07": "Shareholder vote", "7.01": "Reg FD disclosure", "8.01": "Other events",
    "9.01": "Exhibits",
}
TX_CODE = {"P": "open-market BUY", "S": "open-market sale", "M": "option exercise",
           "A": "grant/award", "F": "tax withholding", "G": "gift", "C": "conversion"}


def sec_cik_map():
    j = get_json("https://www.sec.gov/files/company_tickers.json")
    return {v["ticker"].upper(): int(v["cik_str"]) for v in j.values()}


def parse_form4(url):
    raw_url = url
    # primaryDocument is often the XSL-rendered path; the raw XML sits one level up
    parts = url.split("/")
    if len(parts) > 2 and parts[-2].lower().startswith("xsl"):
        raw_url = "/".join(parts[:-2] + parts[-1:])
    r = S.get(raw_url, timeout=20)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    owner = root.findtext(".//reportingOwner/reportingOwnerId/rptOwnerName") or "?"
    rel = root.find(".//reportingOwner/reportingOwnerRelationship")
    role = []
    if rel is not None:
        if (rel.findtext("isDirector") or "").strip() in ("1", "true"):
            role.append("Director")
        if (rel.findtext("isOfficer") or "").strip() in ("1", "true"):
            role.append(rel.findtext("officerTitle") or "Officer")
        if (rel.findtext("isTenPercentOwner") or "").strip() in ("1", "true"):
            role.append("10% owner")
    plan = (root.findtext(".//aff10b5One") or "").strip() in ("1", "true")
    txs = []
    for tx in root.findall(".//nonDerivativeTable/nonDerivativeTransaction"):
        code = tx.findtext("transactionCoding/transactionCode") or "?"
        try:
            sh = float(tx.findtext("transactionAmounts/transactionShares/value") or 0)
            px = float(tx.findtext("transactionAmounts/transactionPricePerShare/value") or 0)
        except ValueError:
            sh, px = 0.0, 0.0
        txs.append({"code": code, "type": TX_CODE.get(code, code), "shares": sh,
                    "price": px, "value": round(sh * px)})
    return {"owner": owner.title(), "role": ", ".join(role) or "?", "10b5_1_plan": plan, "transactions": txs}


def pull_edgar(tickers, since):
    out = {}
    try:
        ciks = sec_cik_map()
    except Exception as e:  # noqa: BLE001
        err("edgar", f"ticker→CIK map failed: {e}")
        return out
    for t in tickers:
        cik = ciks.get(t)
        if not cik:
            err(f"edgar/{t}", "no CIK found")
            continue
        try:
            j = get_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
            rec = j["filings"]["recent"]
            rows = []
            for i, form in enumerate(rec["form"]):
                if rec["filingDate"][i] < since:
                    break
                if form not in FORMS:
                    continue
                acc = rec["accessionNumber"][i].replace("-", "")
                url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{rec['primaryDocument'][i]}"
                f = {"form": form, "date": rec["filingDate"][i], "url": url,
                     "description": rec.get("primaryDocDescription", [""] * (i + 1))[i]}
                if form.startswith("8-K"):
                    items = [x.strip() for x in (rec.get("items", [""] * (i + 1))[i] or "").split(",") if x.strip()]
                    f["items"] = [f"{x} {ITEM_8K.get(x, '')}".strip() for x in items]
                if form == "4":
                    try:
                        f["form4"] = parse_form4(url)
                    except Exception as e:  # noqa: BLE001
                        f["form4_error"] = str(e)[:120]
                    time.sleep(0.15)
                rows.append(f)
            out[t] = rows
            time.sleep(0.15)
        except Exception as e:  # noqa: BLE001
            err(f"edgar/{t}", str(e))
    return out


# ---------------------------------------------------------------- Finnhub

def r2(x):
    return round(x, 2) if isinstance(x, (int, float)) else x


def fh(path, **params):
    params["token"] = FINNHUB_KEY
    j = get_json(f"https://finnhub.io/api/v1/{path}", params)
    time.sleep(1.05)  # free tier: 60 calls/min
    return j


METRIC_KEYS = ["peTTM", "peExclExtraTTM", "psTTM", "pbAnnual", "epsGrowthTTMYoy",
               "revenueGrowthTTMYoy", "revenueGrowthQuarterlyYoy", "operatingMarginTTM",
               "netProfitMarginTTM", "beta", "marketCapitalization"]


def pull_finnhub(tickers, today, mode, names=None):
    names = names or {}
    if not FINNHUB_KEY:
        err("finnhub", "FINNHUB_API_KEY not set — no earnings calendar, estimates, analyst trends or news")
        return {}
    out = {}
    f_from = (today - dt.timedelta(days=100)).isoformat()
    f_to = (today + dt.timedelta(days=100)).isoformat()
    news_from = (today - dt.timedelta(days=7 if mode == "weekly" else 2)).isoformat()
    for t in tickers:
        d = {}
        try:
            cal = fh("calendar/earnings", symbol=t, **{"from": f_from, "to": f_to}).get("earningsCalendar", [])
            cal.sort(key=lambda x: x.get("date", ""))
            past = [c for c in cal if c.get("date", "") < today.isoformat() or c.get("epsActual") is not None]
            fut = [c for c in cal if c.get("date", "") >= today.isoformat() and c.get("epsActual") is None]
            if fut:
                n = fut[0]
                d["next_earnings"] = {"date": n.get("date"), "hour": n.get("hour"),
                                      "quarter": f"{n.get('year')}Q{n.get('quarter')}",
                                      "eps_est": r2(n.get("epsEstimate")), "rev_est": n.get("revenueEstimate")}
            if past:
                p = past[-1]
                d["last_earnings"] = {"date": p.get("date"), "quarter": f"{p.get('year')}Q{p.get('quarter')}",
                                      "eps_actual": r2(p.get("epsActual")), "eps_est": r2(p.get("epsEstimate")),
                                      "rev_actual": p.get("revenueActual"), "rev_est": p.get("revenueEstimate")}
        except Exception as e:  # noqa: BLE001
            err(f"finnhub/earnings/{t}", str(e))
        try:
            rec = fh("stock/recommendation", symbol=t)
            if rec:
                cur = rec[0]
                d["analysts"] = {k: cur.get(k) for k in ("period", "strongBuy", "buy", "hold", "sell", "strongSell")}
                if len(rec) > 1:
                    prv = rec[1]
                    bulls = lambda r: (r.get("strongBuy", 0) + r.get("buy", 0))  # noqa: E731
                    bears = lambda r: (r.get("sell", 0) + r.get("strongSell", 0))  # noqa: E731
                    d["analysts"]["buy_change_vs_prior_month"] = bulls(cur) - bulls(prv)
                    d["analysts"]["sell_change_vs_prior_month"] = bears(cur) - bears(prv)
        except Exception as e:  # noqa: BLE001
            err(f"finnhub/recs/{t}", str(e))
        try:
            m = fh("stock/metric", symbol=t, metric="all").get("metric", {})
            d["metrics"] = {k: m.get(k) for k in METRIC_KEYS if m.get(k) is not None}
        except Exception as e:  # noqa: BLE001
            err(f"finnhub/metrics/{t}", str(e))
        try:
            news = fh("company-news", symbol=t, **{"from": news_from, "to": today.isoformat()})
            news.sort(key=lambda x: x.get("datetime", 0), reverse=True)
            words = [t.lower()] + [w.lower() for w in names.get(t, [])]
            if len(words) > 1:  # only filter when we know the company's name
                news = [n for n in news if any(w in (n.get("headline") or "").lower() for w in words)]
            d["news"] = [{"time": dt.datetime.fromtimestamp(n["datetime"], ET_TZ).strftime("%m-%d %H:%M"),
                          "source": n.get("source"), "headline": n.get("headline"), "url": n.get("url")}
                         for n in news[:6] if n.get("headline")]
        except Exception as e:  # noqa: BLE001
            err(f"finnhub/news/{t}", str(e))
        out[t] = d
    return out


def track_estimates(fin, today):
    """Append today's next-quarter estimates; return revisions vs ~7 and ~30 days ago."""
    path = DATA / "estimates_history.csv"
    rows = []
    if path.exists():
        with path.open() as f:
            rows = list(csv.DictReader(f))
    td = today.isoformat()
    rows = [r for r in rows if r["date"] != td]
    for t, d in fin.items():
        n = d.get("next_earnings")
        if n and (n.get("eps_est") is not None or n.get("rev_est") is not None):
            rows.append({"date": td, "ticker": t, "quarter": n["quarter"],
                         "eps_est": n.get("eps_est"), "rev_est": n.get("rev_est")})
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "ticker", "quarter", "eps_est", "rev_est"])
        w.writeheader()
        w.writerows(rows)

    def num(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    revs = {}
    for t, d in fin.items():
        n = d.get("next_earnings")
        if not n:
            continue
        hist = [r for r in rows if r["ticker"] == t and r["quarter"] == n["quarter"]]
        cur = num(n.get("eps_est"))
        out = {"quarter": n["quarter"], "eps_est": cur, "days_of_history": len(hist)}
        for label, days in (("7d", 7), ("30d", 30)):
            cutoff = (today - dt.timedelta(days=days)).isoformat()
            older = [r for r in hist if r["date"] <= cutoff]
            if older and cur is not None and num(older[-1]["eps_est"]):
                out[f"eps_rev_{label}_pct"] = pct(cur, num(older[-1]["eps_est"]))
        revs[t] = out
    return revs


# ---------------------------------------------------------------- clinical / FDA

BAD_STATUS = {"TERMINATED", "SUSPENDED", "WITHDRAWN"}


def pull_clinical(sponsors, since):
    """Report only events that matter: results first posted, new Phase 3 registered,
    a Phase 2/3 trial terminated/suspended/withdrawn, or a status change since the last run."""
    state_path = DATA / "clinical_state.json"
    first_run = not state_path.exists()
    state = {} if first_run else json.loads(state_path.read_text())
    out = {}
    for t, name in sponsors.items():
        try:
            j = get_json("https://clinicaltrials.gov/api/v2/studies", {
                "query.spons": name,
                "filter.advanced": f"AREA[LastUpdatePostDate]RANGE[{since},MAX]",
                "pageSize": 500, "format": "json"})
            rows = []
            for s in j.get("studies", []):
                ps = s.get("protocolSection", {})
                phases = ps.get("designModule", {}).get("phases", []) or []
                late = any(p in ("PHASE2", "PHASE3") for p in phases)
                st = ps.get("statusModule", {})
                nct = ps.get("identificationModule", {}).get("nctId")
                status = st.get("overallStatus")
                results_date = st.get("resultsFirstPostDateStruct", {}).get("date") or ""
                first_post = st.get("studyFirstPostDateStruct", {}).get("date") or ""
                prev = state.get(nct)
                state[nct] = status

                events = []
                if results_date >= since:
                    events.append("RESULTS POSTED")
                if "PHASE3" in phases and first_post >= since:
                    events.append("NEW PHASE 3")
                if late and status in BAD_STATUS and (prev != status):
                    events.append(f"{status}")
                elif late and prev and prev != status and not first_run:
                    events.append(f"status {prev} → {status}")
                if not events:
                    continue
                rows.append({
                    "nct": nct,
                    "title": ps.get("identificationModule", {}).get("briefTitle"),
                    "phase": "/".join(p.replace("PHASE", "P") for p in phases),
                    "status": status, "events": events,
                    "primary_completion": st.get("primaryCompletionDateStruct", {}).get("date"),
                    "conditions": ", ".join((ps.get("conditionsModule", {}).get("conditions") or [])[:3]),
                })
            rank = lambda r: (0 if any(e in BAD_STATUS for e in r["events"]) else  # noqa: E731
                              1 if "RESULTS POSTED" in r["events"] else 2)
            rows.sort(key=rank)
            out[t] = rows[:15]
        except Exception as e:  # noqa: BLE001
            err(f"clinical/{t}", str(e))
    state_path.write_text(json.dumps(state))
    return out


def pull_fda(drug_sponsors, device_applicants, since_compact, today_compact):
    out = {}
    for t, name in drug_sponsors.items():
        try:
            q = f'sponsor_name:"{name}" AND submissions.submission_status_date:[{since_compact} TO {today_compact}]'
            j = get_json("https://api.fda.gov/drug/drugsfda.json", {"search": q, "limit": 50})
            rows = []
            for app in j.get("results", []):
                brand = ", ".join(sorted({p.get("brand_name", "") for p in app.get("products", [])}))
                for sub in app.get("submissions", []):
                    d = sub.get("submission_status_date", "")
                    if since_compact <= d <= today_compact:
                        rows.append({"date": d, "brand": brand, "application": app.get("application_number"),
                                     "type": sub.get("submission_type"), "status": sub.get("submission_status"),
                                     "class": sub.get("submission_class_code_description")})
            out[t] = sorted(rows, key=lambda r: r["date"], reverse=True)
        except RuntimeError as e:
            if "404" in str(e):
                out[t] = []  # openFDA returns 404 when there are no matches
            else:
                err(f"fda/{t}", str(e))
    for t, name in device_applicants.items():
        try:
            q = f'applicant:"{name}" AND decision_date:[{since_compact} TO {today_compact}]'
            j = get_json("https://api.fda.gov/device/510k.json", {"search": q, "limit": 20})
            out[t] = [{"date": r.get("decision_date"), "device": r.get("device_name"),
                       "k_number": r.get("k_number"), "decision": r.get("decision_description")}
                      for r in j.get("results", [])]
        except RuntimeError as e:
            if "404" in str(e):
                out[t] = []
            else:
                err(f"fda/{t}", str(e))
    return out



VAL_KEYS = {"forwardPE": "fwd_pe", "trailingPE": "ttm_pe", "pegRatio": "peg", "targetMeanPrice": "target_mean",
            "targetLowPrice": "target_low", "targetHighPrice": "target_high", "recommendationKey": "rating",
            "numberOfAnalystOpinions": "n_analysts", "shortPercentOfFloat": "short_pct"}


def pull_valuation(tickers):
    """Forward P/E and analyst price targets from Yahoo (one call per company)."""
    out = {}
    try:
        import yfinance as yf
    except Exception as e:  # noqa: BLE001
        err("valuation", str(e))
        return out
    for t in tickers:
        try:
            info = yf.Ticker(t).info or {}
            out[t] = {v: info.get(k) for k, v in VAL_KEYS.items() if info.get(k) is not None}
        except Exception as e:  # noqa: BLE001
            err(f"valuation/{t}", str(e)[:80])
        time.sleep(0.5)
    return out

# ---------------------------------------------------------------- markdown

def fmt(x, suffix=""):
    if x is None or x == "":
        return "—"
    if isinstance(x, float):
        return f"{x:,.2f}{suffix}"
    return f"{x}{suffix}"


def money(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "—"
    for unit, div in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(x) >= div:
            return f"${x / div:,.1f}{unit}"
    return f"${x:,.0f}"


def render_md(d, groups):
    L = []
    L.append(f"# Trading desk data — {d['mode']} pull")
    L.append(f"Generated {d['generated_et']} ET ({d['generated_utc']} UTC). "
             f"Filings/news since {d['since']}.")
    L.append("")
    L.append("Use these numbers as the price source. A price marked ✓ matched two sources "
             "(Yahoo + Finnhub) within 0.5%; ✗ means single-source — label orders based on it UNVERIFIED PRICE.")
    L.append("")

    L.append("## Data quality")
    if d["errors"]:
        L += [f"- {e}" for e in d["errors"][:40]]
        if len(d["errors"]) > 40:
            L.append(f"- …and {len(d['errors']) - 40} more (see latest.json)")
    else:
        L.append("- All sources returned data.")
    L.append("")

    pre = d["mode"] == "premarket"
    L.append("## Prices")
    hdr = "| Group | Ticker | Close date | Close | ✓ | Day % | 5d % | 1m % | 3m % | From 52w high % | Vol vs 20d |"
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    if pre:
        hdr += " Premarket | Pre % |"
        sep += "---|---|"
    L += [hdr, sep]
    for g, ts in groups.items():
        for t in ts:
            p = d["prices"].get(t, {})
            row = (f"| {g} | {t} | {fmt(p.get('close_date'))} | {fmt(p.get('close'))} | "
                   f"{'✓' if p.get('verified') else '✗'} | {fmt(p.get('day_pct'))} | {fmt(p.get('5d_pct'))} | "
                   f"{fmt(p.get('1m_pct'))} | {fmt(p.get('3m_pct'))} | {fmt(p.get('from_52w_high_pct'))} | "
                   f"{fmt(p.get('vol_vs_20d'))} |")
            if pre:
                row += f" {fmt(p.get('premarket'))} | {fmt(p.get('premarket_pct'))} |"
            L.append(row)
    L.append("")

    L.append("## SEC filings")
    any_f = False
    for t, rows in d["edgar"].items():
        for f in rows:
            if f["form"] == "4":
                continue
            any_f = True
            extra = f" — {'; '.join(f['items'])}" if f.get("items") else ""
            L.append(f"- **{t}** {f['form']} ({f['date']}){extra} — [filing]({f['url']})")
    if not any_f:
        L.append("- None (excluding Form 4).")
    L.append("")

    L.append("## Insider trades (Form 4)")
    any_i = False
    for t, rows in d["edgar"].items():
        for f in rows:
            if f["form"] != "4" or "form4" not in f:
                continue
            f4 = f["form4"]
            for tx in f4["transactions"]:
                if tx["code"] not in ("P", "S"):
                    continue
                any_i = True
                flag = "  ← OPEN-MARKET BUY" if tx["code"] == "P" else ""
                plan = " (10b5-1 plan)" if f4["10b5_1_plan"] else ""
                L.append(f"- **{t}** {f['date']} · {f4['owner']} ({f4['role']}) · {tx['type']}{plan} · "
                         f"{tx['shares']:,.0f} sh @ ${tx['price']:,.2f} = {money(tx['value'])}{flag}")
    if not any_i:
        L.append("- No open-market buys or sales filed.")
    L.append("")

    L.append("## Earnings and estimates")
    L.append("| Ticker | Next report | Time | Qtr | EPS est | EPS rev 7d % | EPS rev 30d % | Rev est | Last qtr EPS act vs est |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for g, ts in groups.items():
        if g == "Benchmark":
            continue
        for t in ts:
            f = d["finnhub"].get(t, {})
            n, last, r = f.get("next_earnings", {}), f.get("last_earnings", {}), d["revisions"].get(t, {})
            surprise = "—"
            if last.get("eps_actual") is not None and last.get("eps_est"):
                surprise = f"{last['eps_actual']} vs {last['eps_est']} ({fmt(pct(last['eps_actual'], last['eps_est']), '%')})"
            L.append(f"| {t} | {fmt(n.get('date'))} | {fmt(n.get('hour'))} | {fmt(n.get('quarter'))} | "
                     f"{fmt(n.get('eps_est'))} | {fmt(r.get('eps_rev_7d_pct'))} | {fmt(r.get('eps_rev_30d_pct'))} | "
                     f"{money(n.get('rev_est'))} | {surprise} |")
    L.append("")
    L.append("Estimate revisions build up from daily snapshots, so they fill in after the pipeline has run 7 and 30 days.")
    L.append("")

    L.append("## Analyst ratings (monthly trend)")
    L.append("| Ticker | Month | Strong buy | Buy | Hold | Sell | Strong sell | Δ buys vs prior | Δ sells vs prior |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for g, ts in groups.items():
        for t in ts:
            a = d["finnhub"].get(t, {}).get("analysts")
            if a:
                L.append(f"| {t} | {a.get('period')} | {a.get('strongBuy')} | {a.get('buy')} | {a.get('hold')} | "
                         f"{a.get('sell')} | {a.get('strongSell')} | {fmt(a.get('buy_change_vs_prior_month'))} | "
                         f"{fmt(a.get('sell_change_vs_prior_month'))} |")
    L.append("")

    L.append("## Valuation and growth (trailing)")
    L.append("| Ticker | P/E TTM | P/S TTM | Rev growth TTM % | Rev growth last qtr % | Op margin TTM % | Beta |")
    L.append("|---|---|---|---|---|---|---|")
    for g, ts in groups.items():
        for t in ts:
            m = d["finnhub"].get(t, {}).get("metrics")
            if m:
                L.append(f"| {t} | {fmt(m.get('peTTM'))} | {fmt(m.get('psTTM'))} | {fmt(m.get('revenueGrowthTTMYoy'))} | "
                         f"{fmt(m.get('revenueGrowthQuarterlyYoy'))} | {fmt(m.get('operatingMarginTTM'))} | {fmt(m.get('beta'))} |")
    L.append("")
    L.append("")
    L.append("## Forward valuation and analyst targets (Yahoo)")
    L.append("| Ticker | Fwd P/E | P/E TTM | PEG | Avg analyst target | Upside to avg target % | Target range | Rating (n) | Short % float |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for g, ts in groups.items():
        if g == "Benchmark":
            continue
        for t in ts:
            v = d.get("valuation", {}).get(t)
            if not v:
                continue
            close = d["prices"].get(t, {}).get("close")
            up = pct(v["target_mean"], close) if v.get("target_mean") and close else None
            rng = f"{fmt(v.get('target_low'))}–{fmt(v.get('target_high'))}" if v.get("target_low") else "—"
            sp = round(v["short_pct"] * 100, 1) if v.get("short_pct") is not None else None
            L.append(f"| {t} | {fmt(r2(v.get('fwd_pe')))} | {fmt(r2(v.get('ttm_pe')))} | {fmt(r2(v.get('peg')))} | "
                     f"{fmt(v.get('target_mean'))} | {fmt(up)} | {rng} | {v.get('rating', '—')} ({v.get('n_analysts', '—')}) | {fmt(sp)} |")
    L.append("")
    L.append("5-year average P/E and independent fair values (e.g. Morningstar) are not in this feed; get those from search and cite the source and date.")
    L.append("")

    L.append("## Clinical trials (results posted, new Phase 3, terminations, status changes)")
    any_c = False
    for t, rows in d["clinical"].items():
        for r in rows:
            any_c = True
            L.append(f"- **{t}** · **{', '.join(r['events'])}** · [{r['nct']}](https://clinicaltrials.gov/study/{r['nct']}) "
                     f"{r['phase']} · {r['status']} · primary completion {fmt(r['primary_completion'])} — "
                     f"{r['title']} ({r['conditions']})")
    if not any_c:
        L.append("- No material trial events.")
    L.append("")

    L.append("## FDA actions")
    any_d = False
    for t, rows in d["fda"].items():
        for r in rows:
            any_d = True
            if "brand" in r:
                L.append(f"- **{t}** {r['date']} · {r['brand']} ({r['application']}) · {r['type']} {r['status']} · {fmt(r.get('class'))}")
            else:
                L.append(f"- **{t}** {r['date']} · 510(k) {r['k_number']} · {r['device']} · {r['decision']}")
    if not any_d:
        L.append("- None.")
    L.append("")

    L.append("## Headlines")
    for g, ts in groups.items():
        for t in ts:
            news = d["finnhub"].get(t, {}).get("news") or []
            if news:
                L.append(f"**{t}**")
                L += [f"- {n['time']} · {n['source']} · [{n['headline']}]({n['url']})" for n in news]
                L.append("")
    return "\n".join(L) + "\n"



def intraday(groups, tickers, now_et):
    """Hourly snapshot during market hours: current price and day % for tracked names, swing
    names and the whole S&P 500/400 universe. Writes data/intraday.md and data/universe_intraday.csv."""
    import pandas as pd
    import yfinance as yf
    uni = []
    up = DATA / "universe.csv"
    if up.exists():
        uni = list(pd.read_csv(up)["yf"])
    syms = list(dict.fromkeys(tickers + uni))
    rows = {}
    for i in range(0, len(syms), 150):
        chunk = syms[i:i + 150]
        try:
            h = yf.download(chunk, period="5d", interval="1d", auto_adjust=False, group_by="ticker",
                            progress=False, threads=True)
            for t in chunk:
                try:
                    df = (h[t] if len(chunk) > 1 else h).dropna(subset=["Close"])
                    if len(df) < 2:
                        continue
                    last, prev = float(df["Close"].iloc[-1]), float(df["Close"].iloc[-2])
                    rows[t] = {"symbol": t, "bar_date": str(df.index[-1].date()), "last": round(last, 2),
                               "day_pct": pct(last, prev), "day_low": round(float(df["Low"].iloc[-1]), 2),
                               "day_high": round(float(df["High"].iloc[-1]), 2)}
                except Exception:  # noqa: BLE001
                    pass
        except Exception as e:  # noqa: BLE001
            err("intraday", str(e))
        time.sleep(1)
    pd.DataFrame(rows.values()).to_csv(DATA / "universe_intraday.csv", index=False)
    L = [f"# Intraday snapshot — {now_et:%Y-%m-%d %H:%M} ET",
         "Prices from Yahoo Finance (may lag the market by up to ~15 minutes). Not used for orders; "
         "for checking where things stand during the day. Full universe in data/universe_intraday.csv.", "",
         "| Group | Ticker | Last | Day % | Day low | Day high |", "|---|---|---|---|---|---|"]
    for g, ts in groups.items():
        for t in ts:
            r = rows.get(t, {})
            L.append(f"| {g} | {t} | {fmt(r.get('last'))} | {fmt(r.get('day_pct'))} | {fmt(r.get('day_low'))} | {fmt(r.get('day_high'))} |")
    movers = sorted((r for r in rows.values() if r.get("day_pct") is not None), key=lambda r: r["day_pct"])
    L += ["", "**Biggest losers so far (universe)**: " + ", ".join(f"{r['symbol']} {r['day_pct']}%" for r in movers[:10]),
          "", "**Biggest gainers so far (universe)**: " + ", ".join(f"{r['symbol']} {r['day_pct']}%" for r in movers[::-1][:10])]
    if ERRORS:
        L += ["", "Data quality: " + "; ".join(ERRORS[:5])]
    (DATA / "intraday.md").write_text("\n".join(L) + "\n")
    print(f"Wrote data/intraday.md ({len(rows)} prices)")
    return 0

# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["premarket", "close", "weekly", "intraday"])
    ap.add_argument("--force", action="store_true", help="run even outside the time window")
    a = ap.parse_args()

    now_utc = dt.datetime.now(dt.timezone.utc)
    now_et = now_utc.astimezone(ET_TZ)
    mode = pick_mode(now_et, a.mode)
    if not mode:
        if not a.force:
            print(f"Outside run windows ({now_et:%a %H:%M} ET); nothing to do.")
            return 0
        mode = "close"

    cfg = yaml.safe_load((ROOT / "config" / "tickers.yml").read_text())
    groups = {"Tracked": cfg.get("tracked", []) + cfg.get("swing_test", []),
              "Benchmark": cfg.get("benchmarks", [])}
    tickers = [t for ts in groups.values() for t in ts]
    companies = [t for g, ts in groups.items() if g != "Benchmark" for t in ts]

    today = now_et.date()
    lookback = 8 if mode == "weekly" else (4 if today.weekday() == 0 else 2)
    since = (today - dt.timedelta(days=lookback)).isoformat()

    DATA.mkdir(exist_ok=True)
    if mode == "intraday":
        return intraday(groups, tickers, now_et)
    d = {"mode": mode, "generated_utc": now_utc.strftime("%Y-%m-%d %H:%M"),
         "generated_et": now_et.strftime("%Y-%m-%d %H:%M"), "since": since}
    d["prices"] = pull_prices(tickers, mode)
    d["edgar"] = pull_edgar(companies, since)
    names = dict(cfg.get("names", {}))
    up = DATA / "universe.csv"
    if up.exists():
        import pandas as pd
        u = pd.read_csv(up)
        for sym, nm in zip(u["yf"], u["name"]):
            first = str(nm).replace(",", " ").split()[0] if isinstance(nm, str) and nm.strip() else ""
            if len(first) > 2:
                names.setdefault(sym, [first])
    d["finnhub"] = pull_finnhub(companies, today, mode, names)
    d["revisions"] = track_estimates(d["finnhub"], today) if d["finnhub"] else {}
    clin_since = (today - dt.timedelta(days=8 if mode == "weekly" else 3)).isoformat()
    d["clinical"] = pull_clinical(cfg.get("clinical_sponsors", {}), clin_since)
    d["fda"] = pull_fda(cfg.get("fda_drug_sponsors", {}), cfg.get("fda_device_applicants", {}),
                        (today - dt.timedelta(days=14)).strftime("%Y%m%d"), today.strftime("%Y%m%d"))
    d["valuation"] = pull_valuation(companies) if mode in ("close", "weekly", "premarket") else {}
    d["errors"] = ERRORS

    DATA.mkdir(exist_ok=True)
    (DATA / "snapshots").mkdir(exist_ok=True)
    (DATA / "latest.json").write_text(json.dumps(d, indent=1, default=str))
    (DATA / "snapshots" / f"{today.isoformat()}_{mode}.json").write_text(json.dumps(d, default=str))
    (DATA / "latest.md").write_text(render_md(d, groups))
    print(f"Wrote data/latest.md ({mode}); {len(ERRORS)} warnings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
