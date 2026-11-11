#!/usr/bin/env python3
"""Exact portfolio math and rule checks, so the reports don't do arithmetic by hand.

PRIVATE BY DESIGN: positions are never stored in this (public) repo. The scheduled reports
build a positions file from a private document (format: config/positions.example.yml),
then run:   python3 scripts/portfolio.py /tmp/positions.yml
Prices come from the public data files (data/universe_intraday.csv when fresh, else
data/universe_prices.csv). Output (markdown) goes to stdout only — never commit it.
"""
import datetime as dt
import json
import pathlib
import sys
from zoneinfo import ZoneInfo

import pandas as pd
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ET = ZoneInfo("America/New_York")


def money(x):
    return f"-${abs(x):,.0f}" if x < 0 else f"${x:,.0f}"


def pct(x, nd=1):
    return f"{x:+.{nd}f}%" if x is not None else "—"


def main():
    if len(sys.argv) < 2:
        print("usage: portfolio.py <positions.yml>")
        return 2
    cfg = yaml.safe_load(pathlib.Path(sys.argv[1]).read_text())
    now = dt.datetime.now(ET)
    today = now.date()
    pos = cfg["positions"]
    tickers = sorted(pos)
    lim = cfg["limits"]

    # prices: intraday snapshot if newer than the last close file, else the last close
    close = pd.read_csv(DATA / "universe_prices.csv").set_index("symbol")
    intr = None
    ip = DATA / "universe_intraday.csv"
    if ip.exists():
        intr = pd.read_csv(ip).set_index("symbol")
        if str(intr["bar_date"].max()) <= str(close["date"].max()):
            intr = None  # older than the close file
    px = {}
    for t in tickers + ["SPY"]:
        c = close.loc[t] if t in close.index else None
        if intr is not None and t in intr.index:
            last, prev, bar = float(intr.loc[t, "last"]), float(c["close"]) if c is not None else None, str(intr.loc[t, "bar_date"]) + " (intraday)"
        elif c is not None:
            last, bar = float(c["close"]), str(c["date"]) + " (close)"
            prev = last / (1 + float(c["day_pct"]) / 100)
        else:
            raise SystemExit(f"No price for {t} in the data files")
        px[t] = {"last": last, "prev": prev or last, "bar": bar}

    sectors = {}
    up = DATA / "universe.csv"
    if up.exists():
        u = pd.read_csv(up)
        sectors = dict(zip(u["yf"], u["sector"]))

    rows, flags, lots_out = [], [], []
    invested_cost = 0.0
    invested_value = 0.0
    for t in tickers:
        lots = pos[t]
        sh = sum(float(l["shares"]) for l in lots)
        cost = sum(float(l["shares"]) * float(l["price"]) for l in lots)
        p = px[t]["last"]
        val = sh * p
        invested_cost += cost
        invested_value += val
        rows.append({"ticker": t, "shares": round(sh, 2), "avg_cost": round(cost / sh, 2), "cost": round(cost),
                     "price": round(p, 2), "value": round(val), "gain_usd": round(val - cost),
                     "gain_pct": round((val / cost - 1) * 100, 2), "day_pct": round((p / px[t]["prev"] - 1) * 100, 2),
                     "two_week_pct": None,
                     "sector": sectors.get(t, "?")})
        for l in lots:
            d = dt.date.fromisoformat(str(l["date"]))
            lt = d + dt.timedelta(days=366)
            lp = float(l["price"])
            lots_out.append({"ticker": t, "date": str(d), "shares": l["shares"], "price": lp,
                             "gain_pct": round((p / lp - 1) * 100, 2), "long_term_on": str(lt),
                             "days_to_long_term": (lt - today).days})

    pending_usd = sum(float(o["usd"]) for o in cfg.get("pending", []))
    cash = float(cfg["cash"])
    total = invested_value + cash + pending_usd
    for r in rows:
        r["weight"] = round(r["value"] / total * 100, 2)
        tgt = cfg.get("targets", {}).get(r["ticker"])
        r["target"] = round(tgt * 100, 1) if tgt is not None else None

    # ---- rule checks (plain words) ----
    for r in rows:
        t, w = r["ticker"], r["weight"]
        if w > lim["max_single"] * 100:
            flags.append(f"{t} is {w:.1f}% of the account — above the {lim['max_single']*100:.0f}% single-stock limit.")
        if r["target"] is not None and w - r["target"] >= 4:
            flags.append(f"{t} is {w - r['target']:.1f} points above its {r['target']:.0f}% target ({w:.1f}%).")
        if r["gain_pct"] >= 30:
            flags.append(f"{t} is up {r['gain_pct']:.1f}% from cost — review for a trim (tax-aware rule applies in the first 12 months).")
        if r["gain_pct"] <= -15:
            flags.append(f"{t} is down {r['gain_pct']:.1f}% from cost — add rule may apply if the thesis is intact.")
        if r["gain_pct"] <= -30:
            flags.append(f"{t} is down {r['gain_pct']:.1f}% from cost — full review required.")
    chip = sum(r["weight"] for r in rows if r["ticker"] in lim["chip_names"])
    if chip > lim["chip_cap"] * 100:
        flags.append(f"NVDA + MU are {chip:.1f}% of the account — above the {lim['chip_cap']*100:.0f}% chip cap.")
    shared = sum(r["weight"] for r in rows if r["ticker"] in lim["shared_cycle"])
    by_sector = {}
    for r in rows:
        by_sector[r["sector"]] = by_sector.get(r["sector"], 0) + r["weight"]
    for s, w in by_sector.items():
        if w > lim["sector_cap"] * 100:
            flags.append(f"{s} stocks are {w:.1f}% of the account — above the {lim['sector_cap']*100:.0f}% sector limit.")
    for l in lots_out:
        if 0 < l["days_to_long_term"] <= 30:
            flags.append(f"{l['ticker']} lot bought {l['date']} turns long-term on {l['long_term_on']} "
                         f"({l['days_to_long_term']} days) — avoid selling it before then if possible.")
    cash_pct = cash / total * 100

    # vs S&P 500 since the first buy (Nov 5 close)
    spy_start = cfg.get("spy_start")  # SPY close on the day of the first buy, if given
    spy_ret = (px["SPY"]["last"] / float(spy_start) - 1) * 100 if spy_start else None
    port_ret = (invested_value / invested_cost - 1) * 100

    out = {"generated_et": now.strftime("%Y-%m-%d %H:%M"), "price_bar": px[tickers[0]]["bar"],
           "total": round(total), "invested_value": round(invested_value), "invested_cost": round(invested_cost),
           "gain_usd": round(invested_value - invested_cost), "gain_pct": round(port_ret, 2),
           "spy_since_nov5_pct": round(spy_ret, 2) if spy_ret is not None else None,
           "cash": round(cash), "cash_pct": round(cash_pct, 1), "pending": cfg.get("pending", []),
           "chip_pct": round(chip, 1), "shared_cycle_pct": round(shared, 1), "sectors": by_sector,
           "positions": rows, "lots": lots_out, "flags": flags}

    L = [f"# Your portfolio — {out['generated_et']} ET",
         f"Prices: {out['price_bar']}. "
         f"Positions as of {cfg['as_of']}. Use these numbers in reports instead of recomputing.", "",
         f"- **Account:** {money(total)} = stocks {money(invested_value)} + cash {money(cash)} + held for pending orders {money(pending_usd)}",
         f"- **Stocks vs what you paid:** {money(invested_value - invested_cost)} ({pct(port_ret)}). "
         f"S&P 500 since the Nov 5 close: {pct(spy_ret)}.",
         f"- **Cash:** {cash_pct:.1f}% of the account (includes the {money(lim['trading_account'])} short-term trading money).",
         f"- **Nvidia + Micron:** {chip:.1f}% (cap {lim['chip_cap']*100:.0f}%). "
         f"**AI/ad-cycle names** (Alphabet, Amazon, Meta, Nvidia, Micron, AppLovin): {shared:.1f}%.",
         "", "| Stock | Shares | Avg cost | Price | Today | Value | Gain/loss | Weight | Target |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: -r["value"]):
        tgt_txt = "—" if r["target"] is None else f"{r['target']:.0f}%"
        L.append(f"| {r['ticker']} | {r['shares']} | ${r['avg_cost']:,.2f} | ${r['price']:,.2f} | {pct(r['day_pct'])} | "
                 f"{money(r['value'])} | {money(r['gain_usd'])} ({pct(r['gain_pct'])}) | {r['weight']:.1f}% | "
                 f"{tgt_txt} |")
    if cfg.get("pending"):
        L += ["", "**Pending orders:** " + "; ".join(
            f"{o['side']} {o['ticker']} {money(o['usd'])} at ${o['limit']} ({o.get('note', '')})" for o in cfg["pending"])]
    L += ["", "## Rule checks"]
    L += [f"- {f}" for f in flags] or ["- No rule is triggered right now."]
    L += ["", "## Sector weights", ", ".join(f"{s}: {w:.1f}%" for s, w in sorted(by_sector.items(), key=lambda x: -x[1]))]
    print("\n".join(L))
    if "--json" in sys.argv:
        print("\n<!--json\n" + json.dumps(out, default=str) + "\n-->")
    return 0


if __name__ == "__main__":
    sys.exit(main())
