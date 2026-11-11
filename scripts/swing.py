"""Range-swing setup (G): find stocks that swing back and forth, and backtest the
swing rule on each before it can be traded.

Rule tested (daily bars, last ~2 years):
  Entry  - close below the lower Bollinger band (20-day average − 2 std dev), buy next open
  Stop   - entry − 2 × ATR(14); if the day's low hits it, exit at the stop (or the open if it gapped below)
  Target - first close at or above the 20-day average → exit at that close
  Time   - exit at the close after 10 trading days
  Costs  - 0.10% per side for slippage

A name PASSES if: ≥ 8 trades, profit factor ≥ 1.3, average trade ≥ +0.5% after costs,
worst trade > −12%, and the last 6 months are not losing (profit factor ≥ 1.0 or < 3 trades).
"""
import math

import pandas as pd

COST = 0.001
MAX_HOLD = 10


def atr(df, n=14):
    h, l, c = df["High"], df["Low"], df["Close"]
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def backtest(df, lookback=504):
    df = df.iloc[-(lookback + 30):].copy()
    c = df["Close"]
    mid = c.rolling(20).mean()
    sd = c.rolling(20).std()
    lower = mid - 2 * sd
    a = atr(df)
    o, h, l = df["Open"], df["High"], df["Low"]
    trades, i, n = [], 25, len(df)
    while i < n - 1:
        if c.iloc[i] < lower.iloc[i] and not math.isnan(a.iloc[i]):
            e_i = i + 1
            entry = float(o.iloc[e_i]) * (1 + COST)
            stop = entry - 2 * float(a.iloc[i])
            exit_px, j = None, e_i
            while j < n:
                if float(l.iloc[j]) <= stop:
                    exit_px = min(float(o.iloc[j]), stop) if j > e_i else stop
                    break
                if float(c.iloc[j]) >= float(mid.iloc[j]) or j - e_i >= MAX_HOLD:
                    exit_px = float(c.iloc[j])
                    break
                j += 1
            if exit_px is None:
                break  # still open at the end of the data
            ret = exit_px * (1 - COST) / entry - 1
            trades.append({"entry_date": str(df.index[e_i].date()), "ret": ret, "days": j - e_i + 1})
            i = j + 1
        else:
            i += 1
    return trades


def stats(trades):
    if not trades:
        return {"trades": 0}
    r = [t["ret"] for t in trades]
    wins, losses = [x for x in r if x > 0], [x for x in r if x <= 0]
    pf = (sum(wins) / -sum(losses)) if losses and sum(losses) < 0 else (99.0 if wins else 0.0)
    return {"trades": len(r), "win_rate": round(100 * len(wins) / len(r)),
            "avg_pct": round(100 * sum(r) / len(r), 2),
            "avg_win_pct": round(100 * sum(wins) / len(wins), 2) if wins else 0.0,
            "avg_loss_pct": round(100 * sum(losses) / len(losses), 2) if losses else 0.0,
            "worst_pct": round(100 * min(r), 2), "pf": round(pf, 2),
            "avg_days": round(sum(t["days"] for t in trades) / len(trades), 1)}


def evaluate(df, today):
    trades = backtest(df)
    s = stats(trades)
    six_mo = str((pd.Timestamp(today) - pd.Timedelta(days=182)).date())
    recent = stats([t for t in trades if t["entry_date"] >= six_mo])
    s["recent_trades"] = recent.get("trades", 0)
    s["recent_pf"] = recent.get("pf")
    s["recent_avg_pct"] = recent.get("avg_pct")
    s["passes"] = bool(s["trades"] >= 8 and s["pf"] >= 1.3 and s["avg_pct"] >= 0.5 and s["worst_pct"] > -12
                       and (recent.get("trades", 0) < 3 or (recent.get("pf") or 0) >= 1.0))
    # per-trade $ on a $15K position, after ~50% tax on net gains
    s["exp_per_15k"] = round(15000 * s.get("avg_pct", 0) / 100)
    s["exp_per_15k_after_tax"] = round(s["exp_per_15k"] * (0.5 if s["exp_per_15k"] > 0 else 1))
    # current state
    c = df["Close"]
    mid = c.rolling(20).mean()
    sd = c.rolling(20).std()
    a = atr(df)
    last, m, lo, at = float(c.iloc[-1]), float(mid.iloc[-1]), float(mid.iloc[-1] - 2 * sd.iloc[-1]), float(a.iloc[-1])
    s.update({"close": round(last, 2), "lower_band": round(lo, 2), "mid_band": round(m, 2), "atr": round(at, 2),
              "signal": last < lo, "near_signal": lo <= last <= lo + 0.5 * at})
    stop = last - 2 * at
    s["stop"] = round(stop, 2)
    s["stop_pct"] = round((stop / last - 1) * 100, 1)
    s["target"] = round(m, 2)
    s["target_pct"] = round((m / last - 1) * 100, 1)
    risk_per_sh = last - stop
    shares = int(min(2000 / risk_per_sh, 15000 / last)) if risk_per_sh > 0 else 0
    s["shares"] = shares
    s["position_usd"] = round(shares * last)
    return s


def swingy(df):
    """Swings a lot without trending hard: median 5-day range ≥ 4%, 3-month move within ±20%,
    and crosses its 20-day average often."""
    c, h, l = df["Close"], df["High"], df["Low"]
    if len(c) < 260:
        return False
    rng = ((h.rolling(5).max() - l.rolling(5).min()) / c).iloc[-60:].median()
    move3m = c.iloc[-1] / c.iloc[-64] - 1
    mid = c.rolling(20).mean()
    crosses = int(((c > mid) != (c.shift() > mid.shift())).iloc[-120:].sum())
    return bool(rng >= 0.04 and abs(move3m) <= 0.20 and crosses >= 10)


def run(prices, meta, core, watch, today, fmt, money):
    rows, watch_rows = [], []
    for s, df in prices.items():
        if s in ("SPY", "^VIX"):
            continue
        try:
            df = df.dropna(subset=["Close"])
            is_watch = s in watch
            m = meta.get(s, {})
            liquid = float((df["Close"] * df["Volume"]).iloc[-21:-1].mean()) >= (5e6 if is_watch else 20e6)
            if not liquid and not is_watch:
                continue
            if not is_watch and (s in core or "semiconductor" in str(m.get("sub_industry", "")).lower()
                                 or float(df["Close"].iloc[-1]) < 10 or not swingy(df)):
                continue
            ev = evaluate(df, today)
            ev["symbol"] = s
            ev["name"] = m.get("name", s)
            ev["liquid"] = liquid
            (watch_rows if is_watch else rows).append(ev)
        except Exception:  # noqa: BLE001
            continue
    passing = sorted([r for r in rows if r.get("passes")], key=lambda r: -r["avg_pct"] * r["trades"])
    signals = [r for r in passing if r["signal"]]

    L = ["# Swing scan (setup G) — range trades, backtested", "",
         "Rule tested over ~2 years of daily prices: buy the open after a close below the lower band "
         "(20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; "
         "time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, "
         "average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. "
         "Only PASS names (or a watch name that passes) may be traded under setup G.", "",
         "Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; "
         "after-tax halves net gains.", ""]

    def table(title, rs):
        L.append(f"## {title}")
        L.append("| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for r in rs:
            if not r.get("trades"):
                L.append(f"| {r['symbol']} | {r['name']} | ✗ | 0 | | | | | | | | | | {r['close']} | {r['lower_band']} | {r['mid_band']} | |")
                continue
            sig = "BUY SIGNAL" if r["signal"] else ("near" if r["near_signal"] else "")
            L.append(f"| {r['symbol']} | {r['name']} | {'✓' if r['passes'] else '✗'} | {r['trades']} | {r['win_rate']} | {r['avg_pct']} | "
                     f"{r['avg_win_pct']} | {r['avg_loss_pct']} | {r['worst_pct']} | {r['pf']} | {r['avg_days']} | "
                     f"{fmt(r['recent_pf'])} ({r['recent_trades']}) | {money(r['exp_per_15k'])} ({money(r['exp_per_15k_after_tax'])}) | "
                     f"{r['close']} | {r['lower_band']} | {r['mid_band']} | {sig} |")
        if not rs:
            L.append("| — | none | | | | | | | | | | | | | | | |")
        L.append("")

    table("Watch names (tested every day regardless of screen)", watch_rows)
    L.append("## Today's swing signals (passing names that closed below the lower band)")
    if signals:
        for r in signals:
            L.append(f"- **{r['symbol']}** close {r['close']} · entry: limit near {r['close']} at the open · "
                     f"stop {r['stop']} ({r['stop_pct']}%) · target 20-day avg {r['target']} (+{r['target_pct']}%) · "
                     f"{r['shares']} shares ≈ {money(r['position_usd'])} · exit by 10 trading days · "
                     f"backtest: {r['trades']} trades, {r['win_rate']}% wins, avg {r['avg_pct']}%, PF {r['pf']}")
    else:
        L.append("- None today.")
    for r in watch_rows:
        if r.get("signal"):
            tag = "passes the backtest" if r.get("passes") else "FAILS the backtest — do not trade"
            L.append(f"- Watch name **{r['symbol']}** closed below its lower band ({tag}). Stop {r['stop']}, target {r['target']}, "
                     f"{r['shares']} shares ≈ {money(r['position_usd'])}.")
    L.append("")
    table("Passing swing names (top 20 by total backtest edge)", passing[:20])
    L.append(f"Screened {len(rows)} swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, "
             f"crosses its 20-day average often; no tracked names or semiconductors); {len(passing)} pass.")
    return "\n".join(L) + "\n", {"watch": watch_rows, "passing": passing[:20], "signals": signals}
