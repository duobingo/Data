#!/usr/bin/env python3
"""News and price watcher: runs every 20 minutes around the clock (GitHub Actions, no AI involved).

Fixed rules decide what counts as an alert, so nothing depends on judgment. Hits are appended to
data/alerts.json (rolling 7 days) and rendered to data/alerts.md (last 72 hours, newest first).
Scheduled desk runs read data/alerts.md when they start.

Watches only public lists: the tracked list in config/tickers.yml and the S&P 500/400 universe in
data/universe.csv. It says nothing about any account.

Checks:
  1. Prices (Yahoo, incl. pre/after-hours): tracked names moving >= 4% vs the last regular close;
     universe names moving >= 8% (liquid names only).
  2. Headlines (Finnhub company news for tracked names + general/merger news for everything):
     keyword rules for leadership, legal/regulatory, guidance, analyst calls, deals, FDA/trials,
     financing/distress and macro (Fed, CPI, jobs, tariffs).
  3. SEC 8-K current feed: material items (exec changes, earnings, deals, delisting,
     unreliable financials, bankruptcy) for any universe or tracked company.

Usage: python scripts/watch.py            (env: FINNHUB_API_KEY, SEC_USER_AGENT; both optional)
"""
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

import requests
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ETZ = ZoneInfo("America/New_York")
FINNHUB_KEY = os.environ.get("FINNHUB_API_KEY", "").strip()
SEC_UA = os.environ.get("SEC_USER_AGENT") or "market-data/1.0 (research)"
S = requests.Session()
S.headers["User-Agent"] = SEC_UA

TRACKED_MOVE = 4.0      # % vs last regular close, any session
UNIVERSE_MOVE = 8.0     # % for the S&P 500/400 radar
MIN_DOLLAR_VOL = 20e6   # liquidity floor for universe movers (avg daily $ volume)
KEEP_DAYS = 7
SHOW_HOURS = 72

# Keyword rules: (category, severity, regex). Severity: 1 = act/know now, 2 = worth a look.
RULES = [
    ("Leadership", 1, r"\b(ceo|chief executive|cfo|chairman|founder)\b.{0,60}\b(resign|steps? down|stepping down|ousted|oust|fired|terminated|departs?|departure|leave of absence|replaced|succession|removal|remove)\b"),
    ("Leadership", 1, r"\b(resign|steps? down|ousted|oust|fired|departure|removal)\b.{0,60}\b(ceo|chief executive|cfo|chairman)\b"),
    ("Leadership", 1, r"\bboard\b.{0,40}\b(probe|investigat|review|weigh|consider)\w*\b.{0,40}\b(ceo|chief executive|conduct|affair)"),
    ("Leadership", 1, r"\b(ceo|leadership|management) (change|shake-?up|turmoil|scandal|crisis|probe)\b|\b(affair|misconduct|resignation)\b"),
    ("Legal/regulatory", 1, r"\b(subpoena|indict\w*|sec charges?|doj|department of justice|ftc sues?|antitrust (suit|case|probe)|criminal (probe|investigation)|class action|export (control|ban|curb)s?|sanction\w*|raided|whistleblower|fraud)\b"),
    ("Legal/regulatory", 2, r"\b(probe|investigation|lawsuit|sued|fine[ds]?|penalt(y|ies)|settle(s|ment)|recall\w*)\b"),
    ("Guidance", 1, r"\b(cuts?|lowers?|slashes?|withdraws?|suspends?|raises?|boosts?|lifts?)\b.{0,30}\b(guidance|forecast|outlook)\b|\bprofit warning\b|\bpre-?announce\w*\b|\bmisses? (estimates|expectations)\b"),
    ("Analyst", 2, r"\b(downgrade[sd]?|upgrade[sd]?|cut to (sell|neutral|underperform|hold)|raised to (buy|outperform|overweight))\b"),
    ("Deal", 1, r"\b(to acquire|acquisition of|agrees? to buy|takeover|merger|buyout|tender offer|activist|stake in|13d|spin-?off|strategic review|exploring (a )?sale)\b"),
    ("FDA/trial", 1, r"\b(fda (approv|reject|declin|clear)\w*|complete response letter|crl\b|clinical hold|met (its )?primary endpoint|failed .{0,20}(trial|endpoint)|phase 3 .{0,30}(results|data|fail|succe)\w*|black box|boxed warning|label warning)\b"),
    ("Financing/distress", 1, r"\b(bankruptcy|chapter 11|going concern|default\w*|delist\w*|trading halt\w*|halted|share offering|stock offering|dilut\w*|convertible|credit downgrade|restat\w*|accounting (issue|irregularit)\w*|short seller|short report)\b"),
    ("Buyback/dividend", 2, r"\b(buyback|repurchase|special dividend|dividend (cut|suspend|raise|increase))\w*\b"),
    ("Contract/customer", 2, r"\b(wins?|awarded|signs?|loses?|lost)\b.{0,30}\b(contract|deal|order|customer)\b"),
]
MACRO = [
    ("Fed/rates", r"\b(fomc|fed (chair|governor|official|minutes|decision|hike|cut)|powell|waller|rate (hike|cut)|treasury yields?)\b"),
    ("Inflation/jobs", r"\b(cpi|ppi|pce|inflation (report|data)|jobs report|nonfarm payrolls?|unemployment rate|jobless claims)\b"),
    ("Policy/trade", r"\b(tariffs?|trade war|export controls?|government shutdown|executive order|sanctions?)\b"),
    ("Market stress", r"\b(sell-?off|plunge|crash|circuit breaker|vix (spike|jump|surge)|flight to safety)\b"),
]
ITEM_8K = {
    "1.01": ("Material agreement", 2), "1.02": ("Agreement terminated", 1), "1.03": ("Bankruptcy", 1),
    "2.01": ("Acquisition/disposition completed", 2), "2.02": ("Earnings results", 2),
    "2.05": ("Restructuring/exit costs", 1), "2.06": ("Impairment", 1), "3.01": ("Delisting notice", 1),
    "4.01": ("Auditor change", 1), "4.02": ("Prior financials unreliable", 1), "5.01": ("Change in control", 1),
    "5.02": ("Executive/director change", 1),
}

ERRORS: list[str] = []


def err(where, msg):
    ERRORS.append(f"{where}: {str(msg)[:200]}")


def now_et():
    return dt.datetime.now(ETZ)


def aid(*parts):
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:16]


def get_json(url, params=None, timeout=20):
    for i in range(2):
        try:
            r = S.get(url, params=params, timeout=timeout)
            if r.status_code == 429:
                time.sleep(5)
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            if i == 1:
                raise e
            time.sleep(2)
    return None


def load_lists():
    cfg = yaml.safe_load((ROOT / "config" / "tickers.yml").read_text())
    tracked = list(dict.fromkeys(cfg.get("tracked", []) + cfg.get("swing_test", [])))
    uni = {}
    up = DATA / "universe.csv"
    if up.exists():
        import csv
        with up.open() as f:
            for r in csv.DictReader(f):
                uni[r["symbol"]] = {"name": r.get("name", ""), "sector": r.get("sector", ""), "yf": r.get("yf") or r["symbol"]}
    return tracked, uni


def session_name(t):
    hm = t.hour * 60 + t.minute
    if t.weekday() >= 5:
        return "weekend"
    if 4 * 60 <= hm < 9 * 60 + 30:
        return "premarket"
    if 9 * 60 + 30 <= hm < 16 * 60:
        return "regular"
    if 16 * 60 <= hm < 20 * 60:
        return "after-hours"
    return "overnight"


# ------------------------------------------------------------------ prices

def price_moves(tracked, uni):
    """Last trade (incl. pre/post) vs last regular-session close."""
    out = []
    try:
        import yfinance as yf
    except Exception as e:  # noqa: BLE001
        err("prices", f"yfinance missing: {e}")
        return out
    sess = session_name(now_et())
    if sess in ("weekend", "overnight"):
        return out  # no new trades to compare; news and filings still checked
    groups = [("tracked", tracked, TRACKED_MOVE)]
    if sess in ("regular", "premarket", "after-hours"):
        groups.append(("universe", [u["yf"] for s, u in uni.items() if s not in tracked], UNIVERSE_MOVE))
    for label, syms, thresh in groups:
        if not syms:
            continue
        for i in range(0, len(syms), 200):
            chunk = syms[i:i + 200]
            try:
                daily = yf.download(chunk, period="1mo", interval="1d", auto_adjust=False, group_by="ticker",
                                    progress=False, threads=True)
                intra = yf.download(chunk, period="1d", interval="5m", prepost=True, auto_adjust=False,
                                    group_by="ticker", progress=False, threads=True)
            except Exception as e:  # noqa: BLE001
                err(f"prices/{label}", e)
                continue
            for t in chunk:
                try:
                    d = (daily[t] if len(chunk) > 1 else daily).dropna(subset=["Close"])
                    x = (intra[t] if len(chunk) > 1 else intra).dropna(subset=["Close"])
                    if d.empty or x.empty:
                        continue
                    today = now_et().date()
                    # reference = last regular close strictly before the latest intraday bar's session,
                    # unless we're after the close, where it is today's regular close
                    last_bar_time = x.index[-1].tz_convert(ETZ)
                    if sess == "after-hours" and d.index[-1].date() == today:
                        ref = float(d["Close"].iloc[-1])
                    else:
                        prior = d[d.index.date < today] if sess != "after-hours" else d
                        if prior.empty:
                            continue
                        ref = float(prior["Close"].iloc[-1])
                    last = float(x["Close"].iloc[-1])
                    move = (last / ref - 1) * 100 if ref else 0
                    if abs(move) < thresh:
                        continue
                    dvol = float((d["Close"] * d["Volume"]).tail(20).mean())
                    if label == "universe" and dvol < MIN_DOLLAR_VOL:
                        continue
                    sym = t.replace("-", ".") if label == "universe" else t
                    info = uni.get(sym) or uni.get(t) or {}
                    out.append({
                        "id": aid("px", t, today, sess, int(move // 3)),  # re-alert each further 3%
                        "kind": "price", "group": label, "ticker": t, "name": info.get("name", ""),
                        "sector": info.get("sector", ""), "severity": 1 if label == "tracked" else 2,
                        "category": f"{'Up' if move > 0 else 'Down'} {abs(move):.1f}% ({sess})",
                        "title": f"{t} {move:+.1f}% at {last:.2f} vs {ref:.2f} close ({sess}, {last_bar_time:%H:%M} ET)",
                        "url": "", "move_pct": round(move, 2),
                    })
                except Exception as e:  # noqa: BLE001
                    err(f"prices/{t}", e)
    return out


# ------------------------------------------------------------------ headlines

def classify(text):
    hits = []
    low = text.lower()
    for cat, sev, rx in RULES:
        if re.search(rx, low):
            hits.append((cat, sev))
    if not hits:
        return None
    sev = min(s for _, s in hits)
    cats = list(dict.fromkeys(c for c, _ in hits))
    return ", ".join(cats), sev


def headlines(tracked, uni, since_ts):
    out = []
    if not FINNHUB_KEY:
        err("news", "FINNHUB_API_KEY not set — headline checks skipped")
        return out
    known = set(tracked) | set(uni)
    today = now_et().date()
    frm = (today - dt.timedelta(days=1)).isoformat()

    def add(item, ticker, group):
        ts = item.get("datetime") or 0
        if ts < since_ts:
            return
        text = f"{item.get('headline', '')}. {item.get('summary', '')[:300]}"
        c = classify(text)
        if not c:
            return
        cat, sev = c
        out.append({
            "id": aid("news", ticker, item.get("id") or item.get("url")),
            "kind": "news", "group": group, "ticker": ticker,
            "name": (uni.get(ticker) or {}).get("name", ""), "sector": (uni.get(ticker) or {}).get("sector", ""),
            "severity": sev if group == "tracked" else max(sev, 2), "category": cat,
            "title": item.get("headline", "")[:220], "source": item.get("source", ""),
            "url": item.get("url", ""), "published": dt.datetime.fromtimestamp(ts, ETZ).strftime("%Y-%m-%d %H:%M"),
        })

    for t in tracked:
        try:
            items = get_json("https://finnhub.io/api/v1/company-news",
                             {"symbol": t, "from": frm, "to": today.isoformat(), "token": FINNHUB_KEY}) or []
            for it in items[:40]:
                add(it, t, "tracked")
        except Exception as e:  # noqa: BLE001
            err(f"news/{t}", e)
        time.sleep(1.05)  # free tier: 60 calls/min

    for cat in ("general", "merger"):
        try:
            items = get_json("https://finnhub.io/api/v1/news", {"category": cat, "token": FINNHUB_KEY}) or []
        except Exception as e:  # noqa: BLE001
            err(f"news/{cat}", e)
            continue
        for it in items:
            ts = it.get("datetime") or 0
            if ts < since_ts:
                continue
            rel = [r.strip() for r in (it.get("related") or "").split(",") if r.strip() in known]
            for r in rel:
                add(it, r, "tracked" if r in tracked else "universe")
            text = f"{it.get('headline', '')}. {it.get('summary', '')[:300]}".lower()
            for mcat, rx in MACRO:
                if re.search(rx, text):
                    out.append({
                        "id": aid("macro", it.get("id") or it.get("url")), "kind": "macro", "group": "market",
                        "ticker": "", "name": "", "sector": "", "severity": 2, "category": mcat,
                        "title": it.get("headline", "")[:220], "source": it.get("source", ""), "url": it.get("url", ""),
                        "published": dt.datetime.fromtimestamp(ts, ETZ).strftime("%Y-%m-%d %H:%M"),
                    })
                    break
        time.sleep(1.05)
    return out


# ------------------------------------------------------------------ SEC 8-K feed

def sec_8k(tracked, uni, since_dt):
    out = []
    try:
        cmap = get_json("https://www.sec.gov/files/company_tickers.json")
        cik_to_t = {int(v["cik_str"]): v["ticker"].replace(".", "-") for v in cmap.values()}
    except Exception as e:  # noqa: BLE001
        err("sec/tickers", e)
        return out
    known = set(tracked) | {s.replace(".", "-") for s in uni}
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for start in (0, 100):
        try:
            r = S.get("https://www.sec.gov/cgi-bin/browse-edgar",
                      params={"action": "getcurrent", "type": "8-K", "count": 100, "start": start, "output": "atom"},
                      timeout=20)
            r.raise_for_status()
            root = ET.fromstring(r.content)
        except Exception as e:  # noqa: BLE001
            err("sec/8k", e)
            break
        for e in root.findall("a:entry", ns):
            title = e.findtext("a:title", "", ns)
            m = re.search(r"\((\d{6,10})\)", title)
            if not m:
                continue
            t = cik_to_t.get(int(m.group(1)))
            if not t or t not in known:
                continue
            upd = e.findtext("a:updated", "", ns)
            try:
                when = dt.datetime.fromisoformat(upd).astimezone(ETZ)
            except Exception:  # noqa: BLE001
                when = now_et()
            if when < since_dt:
                continue
            summ = e.findtext("a:summary", "", ns)
            items = re.findall(r"Item (\d\.\d\d)", summ)
            flagged = [(i, *ITEM_8K[i]) for i in items if i in ITEM_8K]
            if not flagged:
                continue
            sev = min(f[2] for f in flagged)
            link = e.find("a:link", ns)
            group = "tracked" if t in tracked else "universe"
            out.append({
                "id": aid("8k", t, link.get("href") if link is not None else title), "kind": "filing", "group": group,
                "ticker": t, "name": (uni.get(t.replace("-", ".")) or uni.get(t) or {}).get("name", ""), "sector": "",
                "severity": sev if group == "tracked" else max(sev, 2),
                "category": "8-K: " + "; ".join(f"{i} {n}" for i, n, _ in flagged),
                "title": title[:200], "url": link.get("href") if link is not None else "",
                "published": when.strftime("%Y-%m-%d %H:%M"),
            })
        time.sleep(0.5)
    return out


# ------------------------------------------------------------------ store + render

def render(alerts, now):
    cut = now - dt.timedelta(hours=SHOW_HOURS)
    recent = [a for a in alerts if dt.datetime.fromisoformat(a["first_seen"]) >= cut]
    recent.sort(key=lambda a: a["first_seen"], reverse=True)
    L = [f"# Alerts — watcher run {now:%Y-%m-%d %H:%M} ET",
         "",
         "Rule-based hits from the 20-minute watcher (prices incl. pre/after-hours, headlines, SEC 8-Ks). "
         f"Last {SHOW_HOURS} hours, newest first. 'First seen' = when the watcher caught it. "
         "Severity 1 = know now; 2 = worth a look. Desk runs: read everything first seen since your last run.",
         ""]
    sections = [
        ("Tracked list", lambda a: a["group"] == "tracked"),
        ("Market radar (S&P 500/400 movers, news, filings)", lambda a: a["group"] == "universe"),
        ("Market-wide news (Fed, data, policy)", lambda a: a["group"] == "market"),
    ]
    for head, f in sections:
        rows = [a for a in recent if f(a)]
        L += [f"## {head}", ""]
        if not rows:
            L += ["- none", ""]
            continue
        L += ["| First seen (ET) | Sev | Ticker | Type | What | Link |", "|---|---|---|---|---|---|"]
        for a in rows[:150]:
            link = f"[link]({a['url']})" if a.get("url") else ""
            what = a["title"].replace("|", "/")
            L.append(f"| {a['first_seen'][5:16].replace('T', ' ')} | {a['severity']} | {a.get('ticker') or '—'} | "
                     f"{a['category']} | {what} | {link} |")
        L.append("")
    L += ["## Watcher health", ""]
    L += [f"- {e}" for e in ERRORS] or ["- All checks ran."]
    return "\n".join(L) + "\n"


def main():
    now = now_et()
    tracked, uni = load_lists()
    store_p = DATA / "alerts.json"
    store = json.loads(store_p.read_text()) if store_p.exists() else {"alerts": [], "last_run": None}
    last = store.get("last_run")
    since = dt.datetime.fromisoformat(last) - dt.timedelta(minutes=10) if last else now - dt.timedelta(hours=6)
    since = max(since, now - dt.timedelta(hours=24))

    found = []
    found += price_moves(tracked, uni)
    found += headlines(tracked, uni, since.timestamp())
    found += sec_8k(tracked, uni, since)

    seen = {a["id"] for a in store["alerts"]}
    new = 0
    for a in found:
        if a["id"] in seen:
            continue
        a["first_seen"] = now.isoformat(timespec="minutes")
        store["alerts"].append(a)
        seen.add(a["id"])
        new += 1
    keep = now - dt.timedelta(days=KEEP_DAYS)
    store["alerts"] = [a for a in store["alerts"] if dt.datetime.fromisoformat(a["first_seen"]) >= keep]
    store["last_run"] = now.isoformat(timespec="minutes")
    store["errors"] = ERRORS
    DATA.mkdir(exist_ok=True)
    store_p.write_text(json.dumps(store, indent=1))
    (DATA / "alerts.md").write_text(render(store["alerts"], now))
    print(f"watch: {len(found)} hits, {new} new; errors: {len(ERRORS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
