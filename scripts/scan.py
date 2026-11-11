#!/usr/bin/env python3
"""Market-wide scanner for the short-term trading sleeve.

Universe: S&P 500 + S&P 400 (from Wikipedia, cached in data/universe.csv).
Writes data/scan.md (+ data/scan.json) with candidate lists:
  1. Earnings reactions  - beat EPS and revenue, gapped up on heavy volume, held the gap
  2. Breakouts           - new 52-week high on heavy volume, in an uptrend
  3. Oversold uptrends   - sharp 3-day drop, RSI < 30, still above the 200-day average
  4. Insider cluster buys - open-market purchases (not 10b5-1 plans) in the last 14 days
plus the market regime (SPY vs its 50/200-day averages, VIX).

These are candidates, not trades: the daily brief checks news, catalysts and
the trading rules before proposing anything.
"""
import argparse
import datetime as dt
import io
import json
import pathlib
import re
import sys
import time
import xml.etree.ElementTree as ET

import pandas as pd
import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pull  # noqa: E402  (shared helpers: session, keys, mode windows)

DATA = pull.DATA
ERRORS = []
WIKI = {"S&P 500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
        "S&P 400": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"}


def err(section, msg):
    ERRORS.append(f"{section}: {msg}")
    print(f"[warn] {section}: {msg}", file=sys.stderr)


# ---------------------------------------------------------------- universe

def load_universe():
    path = DATA / "universe.csv"
    fresh = path.exists() and (time.time() - path.stat().st_mtime) < 6 * 86400
    if fresh:
        return pd.read_csv(path)
    frames = []
    for idx, url in WIKI.items():
        try:
            html = requests.get(url, headers={"User-Agent": "market-data/1.0 (personal research)"},
                                timeout=30).text
            t = pd.read_html(io.StringIO(html))[0]
            sym = next(c for c in t.columns if str(c).lower() in ("symbol", "ticker symbol", "ticker"))
            name = next(c for c in t.columns if "security" in str(c).lower() or "company" in str(c).lower())
            sector = next((c for c in t.columns if "sector" in str(c).lower()), None)
            sub = next((c for c in t.columns if "sub-industry" in str(c).lower()), None)
            df = pd.DataFrame({
                "symbol": t[sym].astype(str).str.strip(),
                "name": t[name].astype(str),
                "sector": t[sector].astype(str) if sector else "",
                "sub_industry": t[sub].astype(str) if sub else "",
                "index": idx})
            frames.append(df)
        except Exception as e:  # noqa: BLE001
            err(f"universe/{idx}", str(e))
    if frames:
        u = pd.concat(frames).drop_duplicates("symbol")
        u["yf"] = u["symbol"].str.replace(".", "-", regex=False)
        DATA.mkdir(exist_ok=True)
        u.to_csv(path, index=False)
        return u
    if path.exists():
        err("universe", "refresh failed; using cached list")
        return pd.read_csv(path)
    raise RuntimeError("no universe available")


# ---------------------------------------------------------------- prices + indicators

def rsi(close, n=14):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = up / dn.replace(0, float("nan"))
    return (100 - 100 / (1 + rs)).fillna(100)


def download(symbols):
    import yfinance as yf
    out = {}
    for i in range(0, len(symbols), 120):
        chunk = symbols[i:i + 120]
        for attempt in range(2):
            try:
                h = yf.download(chunk, period="14mo", interval="1d", auto_adjust=False,
                                group_by="ticker", progress=False, threads=True)
                for s in chunk:
                    try:
                        df = h[s].dropna(subset=["Close"])
                        if len(df) > 60:
                            out[s] = df
                    except Exception:  # noqa: BLE001
                        pass
                break
            except Exception as e:  # noqa: BLE001
                if attempt:
                    err("prices", f"chunk {i}: {e}")
                time.sleep(5)
        time.sleep(1.5)
    return out


def features(df):
    c, h, l, o, v = df["Close"], df["High"], df["Low"], df["Open"], df["Volume"]
    last = float(c.iloc[-1])
    rng = float(h.iloc[-1] - l.iloc[-1])
    prior_high = float(h.iloc[-253:-1].max()) if len(h) > 20 else float("nan")
    vol50 = float(v.iloc[-51:-1].mean())
    return {
        "date": str(df.index[-1].date()),
        "close": round(last, 2),
        "day_pct": round((last / float(c.iloc[-2]) - 1) * 100, 2),
        "gap_pct": round((float(o.iloc[-1]) / float(c.iloc[-2]) - 1) * 100, 2),
        "3d_pct": round((last / float(c.iloc[-4]) - 1) * 100, 2),
        "1m_pct": round((last / float(c.iloc[-22]) - 1) * 100, 2) if len(c) > 22 else None,
        "3m_pct": round((last / float(c.iloc[-64]) - 1) * 100, 2) if len(c) > 64 else None,
        "vol_ratio": round(float(v.iloc[-1]) / vol50, 2) if vol50 else None,
        "dollar_vol_m": round(float((c * v).iloc[-21:-1].mean()) / 1e6, 1),
        "rsi14": round(float(rsi(c).iloc[-1]), 1),
        "sma50": round(float(c.iloc[-50:].mean()), 2),
        "sma200": round(float(c.iloc[-200:].mean()), 2) if len(c) >= 200 else None,
        "new_52w_high": bool(float(h.iloc[-1]) >= prior_high),
        "from_high_pct": round((last / float(h.iloc[-252:].max()) - 1) * 100, 1),
        "low_20d": round(float(l.iloc[-20:].min()), 2),
        "rsi_5d_ago": round(float(rsi(c).iloc[-6]), 1) if len(c) > 20 else None,
        "clv": round((last - float(l.iloc[-1])) / rng, 2) if rng else 0.5,  # 1 = closed at high
        "day_low": round(float(l.iloc[-1]), 2),
        "atr14": round(float((h - l).iloc[-14:].mean()), 2),
    }


def reaction(df, report_date, hour):
    """Price reaction to an earnings report: the first session after the news."""
    idx = df.index.normalize()
    rd = pd.Timestamp(report_date)
    sessions = [i for i, d in enumerate(idx) if (d > rd if hour == "amc" else d >= rd)]
    if not sessions:
        return None
    i = sessions[0]
    if i == 0:
        return None
    c, o, h, l, v = df["Close"], df["Open"], df["High"], df["Low"], df["Volume"]
    prev = float(c.iloc[i - 1])
    rng = float(h.iloc[i] - l.iloc[i])
    vol50 = float(v.iloc[max(0, i - 50):i].mean())
    return {"reaction_date": str(df.index[i].date()),
            "gap_pct": round((float(o.iloc[i]) / prev - 1) * 100, 2),
            "reaction_pct": round((float(c.iloc[i]) / prev - 1) * 100, 2),
            "vol_ratio": round(float(v.iloc[i]) / vol50, 2) if vol50 else None,
            "clv": round((float(c.iloc[i]) - float(l.iloc[i])) / rng, 2) if rng else 0.5,
            "reaction_low": round(float(l.iloc[i]), 2),
            "since_pct": round((float(c.iloc[-1]) / float(c.iloc[i]) - 1) * 100, 2)}


# ---------------------------------------------------------------- earnings (market-wide)

def earnings_reactions(universe, prices, today):
    if not pull.FINNHUB_KEY:
        err("earnings", "FINNHUB_API_KEY not set")
        return []
    frm = (today - dt.timedelta(days=6)).isoformat()
    try:
        cal = pull.get_json("https://finnhub.io/api/v1/calendar/earnings",
                            {"from": frm, "to": today.isoformat(), "token": pull.FINNHUB_KEY}, timeout=40)
        cal = cal.get("earningsCalendar", [])
    except Exception as e:  # noqa: BLE001
        err("earnings", str(e))
        return []
    fh_to_yf = {s.replace("-", "."): s for s in prices}
    rows = []
    for e in cal:
        s = fh_to_yf.get(e.get("symbol", ""))
        if not s or e.get("epsActual") is None:
            continue
        eps_a, eps_e = e.get("epsActual"), e.get("epsEstimate")
        rev_a, rev_e = e.get("revenueActual"), e.get("revenueEstimate")
        r = reaction(prices[s], e["date"], e.get("hour"))
        if not r:
            continue
        eps_beat = eps_e not in (None, 0) and eps_a > eps_e
        rev_beat = bool(rev_a and rev_e and rev_a > rev_e)
        row = {"symbol": s, "report_date": e["date"], "hour": e.get("hour"),
               "eps_actual": eps_a, "eps_est": eps_e,
               "eps_surprise_pct": round((eps_a / eps_e - 1) * 100, 1) if eps_e not in (None, 0) and eps_e > 0 else None,
               "rev_surprise_pct": round((rev_a / rev_e - 1) * 100, 1) if rev_a and rev_e else None,
               "beat_both": eps_beat and rev_beat, **r}
        f = feat(s)
        if f:
            row.update({"close": f["close"], "dollar_vol_m": f["dollar_vol_m"]})
        rows.append(row)
    return rows


# ---------------------------------------------------------------- insider buys (market-wide, EDGAR daily index)

def insider_buys(universe, today, lookback_trading_days=10):
    state_path = DATA / "insider_buys.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"days": {}, "buys": []}
    try:
        ciks = pull.sec_cik_map()
    except Exception as e:  # noqa: BLE001
        err("insider", f"CIK map: {e}")
        return []
    want = {}
    for s in universe["yf"]:
        c = ciks.get(s.upper()) or ciks.get(s.upper().replace("-", "."))
        if c:
            want[c] = s
    days = [today - dt.timedelta(days=i) for i in range(0, 16)]
    days = [d for d in days if d.weekday() < 5][:lookback_trading_days]
    fetched = 0
    for d in sorted(days):
        key = d.isoformat()
        if state["days"].get(key) == "done" or d > today:
            continue
        q = (d.month - 1) // 3 + 1
        url = f"https://www.sec.gov/Archives/edgar/daily-index/{d.year}/QTR{q}/form.{d:%Y%m%d}.idx"
        try:
            r = pull.S.get(url, timeout=30)
            if r.status_code == 404:
                if d < today:
                    state["days"][key] = "done"  # holiday / no index
                continue
            r.raise_for_status()
        except Exception as e:  # noqa: BLE001
            err("insider", f"index {key}: {e}")
            continue
        seen = set()
        for line in r.text.splitlines():
            if not line.startswith("4 "):
                continue
            m = re.search(r"\s(\d{1,10})\s+(\d{4}-?\d{2}-?\d{2})\s+(edgar/data/\S+\.txt)\s*$", line)
            if not m:
                continue
            cik, path = int(m.group(1)), m.group(3)
            if cik not in want or path in seen:
                continue
            seen.add(path)
            if fetched >= 700:
                break
            try:
                t = pull.S.get(f"https://www.sec.gov/Archives/{path}", timeout=20).text
                fetched += 1
                xm = re.search(r"<XML>\s*(.*?)\s*</XML>", t, re.S)
                if not xm:
                    continue
                root = ET.fromstring(xm.group(1).strip())
                issuer_cik = int((root.findtext(".//issuer/issuerCik") or "0").strip() or 0)
                if issuer_cik != cik:
                    continue
                owner = (root.findtext(".//reportingOwner/reportingOwnerId/rptOwnerName") or "?").title()
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
                for tx in root.findall(".//nonDerivativeTable/nonDerivativeTransaction"):
                    if (tx.findtext("transactionCoding/transactionCode") or "") != "P" or plan:
                        continue
                    try:
                        sh = float(tx.findtext("transactionAmounts/transactionShares/value") or 0)
                        px = float(tx.findtext("transactionAmounts/transactionPricePerShare/value") or 0)
                    except ValueError:
                        continue
                    tdate = (tx.findtext("transactionDate/value") or key)[:10]
                    state["buys"].append({"symbol": want[cik], "filed": key, "tx_date": tdate,
                                          "owner": owner, "role": ", ".join(role) or "?",
                                          "shares": sh, "price": px, "value": round(sh * px),
                                          "acc": path})
                time.sleep(0.11)
            except Exception:  # noqa: BLE001
                time.sleep(0.11)
                continue
        if d < today and fetched < 700:
            state["days"][key] = "done"
    # keep 30 days, de-duplicate
    cutoff = (today - dt.timedelta(days=30)).isoformat()
    uniq = {}
    for b in state["buys"]:
        if b["filed"] >= cutoff:
            uniq[(b["acc"], b["owner"], b["shares"], b["price"])] = b
    state["buys"] = list(uniq.values())
    state["days"] = {k: v for k, v in state["days"].items() if k >= cutoff}
    state_path.write_text(json.dumps(state))
    # cluster: last 14 days, by symbol
    c14 = (today - dt.timedelta(days=14)).isoformat()
    agg = {}
    for b in state["buys"]:
        if b["tx_date"] < c14:
            continue
        a = agg.setdefault(b["symbol"], {"symbol": b["symbol"], "insiders": set(), "total": 0, "buys": []})
        a["insiders"].add(b["owner"])
        a["total"] += b["value"]
        a["buys"].append(b)
    out = []
    for a in agg.values():
        if len(a["insiders"]) >= 2 or a["total"] >= 500_000:
            out.append({"symbol": a["symbol"], "n_insiders": len(a["insiders"]), "total": a["total"],
                        "who": "; ".join(sorted({f"{b['owner']} ({b['role']})" for b in a["buys"]}))[:200],
                        "avg_price": round(sum(b["value"] for b in a["buys"]) / max(1, sum(b["shares"] for b in a["buys"])), 2),
                        "last_tx": max(b["tx_date"] for b in a["buys"])})
    return sorted(out, key=lambda x: (-x["n_insiders"], -x["total"]))



# ---------------------------------------------------------------- quality under fear

def fear_screen(FEAT, ok, insider_syms, today):
    cands = [(s, f) for s, f in FEAT.items() if ok(s, f) and f.get("from_high_pct") is not None
             and f["from_high_pct"] <= -25]
    cands.sort(key=lambda x: x[1]["from_high_pct"])
    cands = cands[:160]
    cache_path = DATA / "fundamentals_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    stale = (today - dt.timedelta(days=7)).isoformat()
    out = []
    for s, f in cands:
        c = cache.get(s)
        if (not c or c.get("asof", "") < stale) and pull.FINNHUB_KEY:
            try:
                m = pull.fh("stock/metric", symbol=s.replace("-", "."), metric="all").get("metric", {})
                c = {"asof": today.isoformat(),
                     "pe": m.get("peTTM") or m.get("peExclExtraTTM"),
                     "pfcf": m.get("pfcfShareTTM"),
                     "rev_growth": m.get("revenueGrowthTTMYoy"),
                     "op_margin": m.get("operatingMarginTTM"),
                     "net_margin": m.get("netProfitMarginTTM"),
                     "roe": m.get("roeTTM"),
                     "de": m.get("totalDebt/totalEquityQuarterly") or m.get("totalDebt/totalEquityAnnual")}
                cache[s] = c
            except Exception as e:  # noqa: BLE001
                err(f"fear/{s}", str(e)[:80])
                continue
        if not c:
            continue
        pe, pfcf, g, om, nm_, roe, de = (c.get(k) for k in ("pe", "pfcf", "rev_growth", "op_margin", "net_margin", "roe", "de"))
        profitable = (om or 0) > 0 and (nm_ or 0) > 0 and pe is not None and pe > 0
        if not profitable or g is None or g <= 0 or (de is not None and de > 2):
            continue
        # score: cheaper, faster-growing, higher-return, less levered, more beaten down = higher
        score = 0.0
        score += max(0, 30 - min(pe, 60)) / 3            # P/E under 30 earns up to 10
        score += min(g, 40) / 4                          # revenue growth up to 10
        score += min(roe or 0, 40) / 4                   # ROE up to 10
        score += 5 if (pfcf and 0 < pfcf < 20) else 0
        score += 5 if (de is not None and de < 0.5) else 0
        score += min(-f["from_high_pct"], 60) / 6        # drawdown up to 10
        turning = bool((f.get("rsi_5d_ago") is not None and f["rsi_5d_ago"] < 35 and f["rsi14"] > f["rsi_5d_ago"] + 5)
                       or f["close"] >= f["low_20d"] * 1.05)
        ins = s in insider_syms
        score += 5 if turning else 0
        score += 5 if ins else 0
        out.append({"symbol": s, **f, **{k: c.get(k) for k in ("pe", "pfcf", "rev_growth", "op_margin", "roe", "de")},
                    "turning": turning, "insider": ins, "score": round(score, 1)})
    cache_path.write_text(json.dumps(cache))
    return sorted(out, key=lambda r: -r["score"])

# ---------------------------------------------------------------- main

FEAT = {}


def feat(s):
    return FEAT.get(s)


def money(x):
    return pull.money(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["premarket", "close", "weekly"])
    a = ap.parse_args()
    now_et = dt.datetime.now(dt.timezone.utc).astimezone(pull.ET_TZ)
    mode = pull.pick_mode(now_et, a.mode)
    if mode not in ("close", "weekly"):
        print("Scanner runs only on close and weekly pulls.")
        return 0
    today = now_et.date()
    DATA.mkdir(exist_ok=True)

    import yaml
    cfg = yaml.safe_load((pull.ROOT / "config" / "tickers.yml").read_text())
    core = set(cfg.get("tracked", []))

    u = load_universe()
    syms = list(u["yf"])
    watch = [t for t in cfg.get("swing_test", [])]
    prices = download(syms + [w for w in watch if w not in syms] + ["SPY", "^VIX"])
    for s, df in prices.items():
        try:
            FEAT[s] = features(df)
        except Exception:  # noqa: BLE001
            pass
    meta = u.set_index("yf").to_dict("index")

    def ok(s, f):
        m = meta.get(s, {})
        return (f and f["close"] >= 10 and f["dollar_vol_m"] >= 20 and s not in core
                and "semiconductor" not in str(m.get("sub_industry", "")).lower())

    # regime
    spy, vix = FEAT.get("SPY"), FEAT.get("^VIX")
    regime = {}
    if spy:
        regime = {"spy": spy["close"], "spy_vs_50d_pct": round((spy["close"] / spy["sma50"] - 1) * 100, 2),
                  "spy_vs_200d_pct": round((spy["close"] / spy["sma200"] - 1) * 100, 2) if spy["sma200"] else None}
        regime["risk"] = ("RISK-OFF" if spy["sma200"] and spy["close"] < spy["sma200"] else
                          "CAUTION" if spy["close"] < spy["sma50"] else "RISK-ON")
    if vix:
        regime["vix"] = vix["close"]
        if vix["close"] >= 30:
            regime["risk"] = "RISK-OFF"

    # 1 earnings reactions
    er = [r for r in earnings_reactions(u, prices, today)
          if r["beat_both"] and r["reaction_pct"] >= 4 and (r["vol_ratio"] or 0) >= 2 and r["clv"] >= 0.5
          and r["since_pct"] > -5 and (r.get("close") or 0) > r["reaction_low"]  # still holding the move
          and ok(r["symbol"], feat(r["symbol"]))]
    er.sort(key=lambda r: -r["reaction_pct"])

    # 2 breakouts
    bo = []
    for s, f in FEAT.items():
        if not ok(s, f) or not f["sma200"]:
            continue
        if f["new_52w_high"] and (f["vol_ratio"] or 0) >= 1.8 and f["clv"] >= 0.7 and f["close"] > f["sma50"] > f["sma200"]:
            bo.append({"symbol": s, **f})
    bo.sort(key=lambda r: -(r["vol_ratio"] or 0))

    # 3 oversold in uptrend
    ov = []
    for s, f in FEAT.items():
        if not ok(s, f) or not f["sma200"]:
            continue
        if f["3d_pct"] <= -8 and f["rsi14"] <= 30 and f["close"] > f["sma200"]:
            ov.append({"symbol": s, **f})
    ov.sort(key=lambda r: r["3d_pct"])

    # 4 insider clusters
    try:
        ins = [r for r in insider_buys(u, today) if r["symbol"] not in core]
    except Exception as e:  # noqa: BLE001
        err("insider", str(e))
        ins = []
    for r in ins:
        f = feat(r["symbol"])
        if f:
            r.update({"close": f["close"], "1m_pct": f["1m_pct"], "vs_insider_px_pct":
                      round((f["close"] / r["avg_price"] - 1) * 100, 1) if r["avg_price"] else None})

    # 5 quality under fear: far below the high, fundamentals intact
    try:
        fear = fear_screen(FEAT, ok, {r["symbol"] for r in ins}, today)
    except Exception as e:  # noqa: BLE001
        err("fear", str(e))
        fear = []

    # 6 daily movers (liquid names; tracked names marked rather than excluded)
    def liquid(s, f):
        m = meta.get(s, {})
        return f and s in meta and f["close"] >= 10 and f["dollar_vol_m"] >= 20
    movers = [{"symbol": s, **f, "core": s in core,
               "semi": "semiconductor" in str(meta.get(s, {}).get("sub_industry", "")).lower()}
              for s, f in FEAT.items() if liquid(s, f)]
    gainers = sorted(movers, key=lambda r: -r["day_pct"])[:10]
    losers = sorted(movers, key=lambda r: r["day_pct"])[:10]

    out = {"generated_et": now_et.strftime("%Y-%m-%d %H:%M"), "mode": mode, "universe": len(syms),
           "priced": len(FEAT), "regime": regime, "earnings": er[:15], "breakouts": bo[:15],
           "oversold": ov[:15], "insider_clusters": ins[:15], "quality_fear": fear[:20], "gainers": gainers, "losers": losers, "errors": ERRORS}
    (DATA / "scan.json").write_text(json.dumps(out, indent=1, default=str))
    try:
        import swing
        smd, sjson = swing.run(prices, meta, core, set(watch), today, pull.fmt, pull.money)
        (DATA / "swing.md").write_text(f"Generated {out['generated_et']} ET\n\n" + smd)
        (DATA / "swing.json").write_text(json.dumps(sjson, indent=1, default=str))
    except Exception as e:  # noqa: BLE001
        err("swing", str(e))
    # full price table for every scanned name (used to track open sleeve trades)
    cols = ["date", "close", "day_pct", "day_low", "atr14", "sma50", "sma200", "rsi14", "1m_pct", "vol_ratio"]
    rows = [{"symbol": s, **{k: f.get(k) for k in cols}} for s, f in sorted(FEAT.items())]
    pd.DataFrame(rows).to_csv(DATA / "universe_prices.csv", index=False)

    def nm(s):
        m = meta.get(s, {})
        return f"{m.get('name', '')} · {m.get('sector', '')}".strip(" ·")

    L = [f"# Short-term scan — {out['generated_et']} ET",
         f"Universe: S&P 500 + S&P 400 ({out['universe']} names, {out['priced']} priced). "
         "Filters: price ≥ $10, avg daily dollar volume ≥ $20M, no semiconductors, no names from the tracked list. "
         "These are candidates; check news, catalysts and the trading rules before proposing a trade.", ""]
    L.append("## Market regime")
    if regime:
        L.append(f"- **{regime.get('risk')}** · SPY {regime['spy']} ({pull.fmt(regime['spy_vs_50d_pct'])}% vs 50-day, "
                 f"{pull.fmt(regime.get('spy_vs_200d_pct'))}% vs 200-day) · VIX {pull.fmt(regime.get('vix'))}")
    L.append("")
    L.append("## 1. Earnings reactions (beat EPS and revenue, jumped ≥4% on ≥2× volume, still above the reaction-day low and within 5% of the reaction-day close)")
    L.append("| Ticker | Company | Reported | Reaction day | Reaction % | Gap % | Vol × | EPS surprise % | Rev surprise % | Since % | Reaction-day low | Close |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in er[:15]:
        L.append(f"| {r['symbol']} | {nm(r['symbol'])} | {r['report_date']} {r['hour'] or ''} | {r['reaction_date']} | "
                 f"{r['reaction_pct']} | {r['gap_pct']} | {r['vol_ratio']} | {pull.fmt(r['eps_surprise_pct'])} | "
                 f"{pull.fmt(r['rev_surprise_pct'])} | {r['since_pct']} | {r['reaction_low']} | {r.get('close')} |")
    if not er:
        L.append("| — | none today | | | | | | | | | | |")
    L.append("")
    L.append("## 2. Breakouts (new 52-week high on ≥1.8× volume, closed near the high, above 50- and 200-day)")
    L.append("| Ticker | Company | Close | Day % | Vol × | 1m % | 3m % | RSI | ATR | Day low |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in bo[:15]:
        L.append(f"| {r['symbol']} | {nm(r['symbol'])} | {r['close']} | {r['day_pct']} | {r['vol_ratio']} | "
                 f"{pull.fmt(r['1m_pct'])} | {pull.fmt(r['3m_pct'])} | {r['rsi14']} | {r['atr14']} | {r['day_low']} |")
    if not bo:
        L.append("| — | none today | | | | | | | | |")
    L.append("")
    L.append("## 3. Oversold in an uptrend (down ≥8% in 3 days, RSI ≤ 30, still above the 200-day)")
    L.append("| Ticker | Company | Close | 3d % | Day % | RSI | Vol × | vs 200-day % | ATR |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in ov[:15]:
        L.append(f"| {r['symbol']} | {nm(r['symbol'])} | {r['close']} | {r['3d_pct']} | {r['day_pct']} | {r['rsi14']} | "
                 f"{r['vol_ratio']} | {pull.fmt(pull.pct(r['close'], r['sma200']))} | {r['atr14']} |")
    if not ov:
        L.append("| — | none today | | | | | | | |")
    L.append("")
    L.append("## 4. Insider cluster buys (open-market, not 10b5-1, last 14 days: ≥2 insiders or ≥$500K)")
    L.append("| Ticker | Company | Insiders | Total bought | Avg insider price | Close | vs insider price % | Last buy | Who |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in ins[:15]:
        L.append(f"| {r['symbol']} | {nm(r['symbol'])} | {r['n_insiders']} | {money(r['total'])} | {r['avg_price']} | "
                 f"{pull.fmt(r.get('close'))} | {pull.fmt(r.get('vs_insider_px_pct'))} | {r['last_tx']} | {r['who']} |")
    if not ins:
        L.append("| — | none | | | | | | | |")
    L.append("")
    L.append("Insider history builds up over the first two weeks of runs.")
    L.append("")
    L.append("## 5. Quality under fear (25%+ below 52-week high, profitable, revenue growing, debt manageable)")
    L.append("Sorted by a value-and-quality score. 'Turning' = RSI rising from below 35 or price above its 20-day low by 5%+ (selling may be exhausting). Insider ✓ = in the insider list above.")
    L.append("| Ticker | Company | Close | From high % | RSI | Turning | P/E TTM | P/FCF | Rev growth % | Op margin % | ROE % | Debt/Equity | Insider | Score |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in fear[:20]:
        L.append(f"| {r['symbol']} | {nm(r['symbol'])} | {r['close']} | {r['from_high_pct']} | {r['rsi14']} | {'✓' if r['turning'] else ''} | "
                 f"{pull.fmt(r.get('pe'))} | {pull.fmt(r.get('pfcf'))} | {pull.fmt(r.get('rev_growth'))} | {pull.fmt(r.get('op_margin'))} | "
                 f"{pull.fmt(r.get('roe'))} | {pull.fmt(r.get('de'))} | {'✓' if r['insider'] else ''} | {r['score']} |")
    if not fear:
        L.append("| — | none | | | | | | | | | | | | |")
    L.append("")
    L.append("## 6. Daily movers (top 10 up and down among liquid S&P 500/400 names)")
    L.append("How to use: for each loser, find the reason. If it's fear, a sector selloff or a one-off, and the business is intact, check setup F (quality under fear) or C (oversold bounce); skip it if estimates are being cut or the business is broken. For each gainer, find the reason. If it's real news (earnings, guidance, a contract, an upgrade) on heavy volume, check setups A or B; skip pure hype or short squeezes. Tracked = on the tracked list. Semi = semiconductor.")
    for label, rows in (("Losers", losers), ("Gainers", gainers)):
        L.append(f"**{label}**")
        L.append("| Ticker | Company | Day % | Gap % | Vol × | 1m % | From 52w high % | RSI | vs 200-day % | Flags |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            flags = ", ".join(x for x, on in (("Tracked", r["core"]), ("Semi", r["semi"])) if on)
            L.append(f"| {r['symbol']} | {nm(r['symbol'])} | {r['day_pct']} | {r['gap_pct']} | {r['vol_ratio']} | "
                     f"{pull.fmt(r['1m_pct'])} | {pull.fmt(r.get('from_high_pct'))} | {r['rsi14']} | "
                     f"{pull.fmt(pull.pct(r['close'], r['sma200']) if r['sma200'] else None)} | {flags} |")
        L.append("")
    L.append("## Data quality")
    L += [f"- {e}" for e in ERRORS[:20]] or ["- All scanner sources returned data."]
    (DATA / "scan.md").write_text("\n".join(L) + "\n")
    print(f"Wrote data/scan.md: {len(er)} earnings, {len(bo)} breakouts, {len(ov)} oversold, {len(ins)} insider; "
          f"{len(ERRORS)} warnings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
