#!/usr/bin/env python3
"""Decide what a scheduled run should do, so duplicate or early cron runs do nothing.

GitHub's schedule fires each pull at two UTC times (to cover daylight saving) and can
start late. This prints the mode to run (premarket / intraday / close / weekly) or
nothing if the run falls outside a window or that pull already ran. A forced mode
(manual run) is always printed.
"""
import datetime as dt
import json
import pathlib
import sys
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")


def pick_mode(now_et, forced):
    """Same windows as pull.pick_mode (copied so this runs before packages are installed)."""
    if forced:
        return forced
    wd, hm = now_et.weekday(), now_et.hour * 60 + now_et.minute
    if wd == 6:
        return "weekly" if hm >= 17 * 60 else None
    if wd < 5 and 7 * 60 <= hm <= 9 * 60 + 25:
        return "premarket"
    if wd < 5 and 16 * 60 + 5 <= hm <= 20 * 60:
        return "close"
    if wd < 5 and 9 * 60 + 40 <= hm <= 15 * 60 + 59:
        return "intraday"
    return None


def decide(now, forced=None):
    if forced:
        return forced
    mode = pick_mode(now, None)
    if not mode:
        return ""
    p = pathlib.Path(__file__).resolve().parent.parent / "data" / "status.json"
    st = json.loads(p.read_text()) if p.exists() else {}
    last = st.get(mode, {}).get("time_et")
    if last:
        last = dt.datetime.strptime(last, "%Y-%m-%d %H:%M").replace(tzinfo=ET)
        gap = dt.timedelta(minutes=40) if mode == "intraday" else dt.timedelta(hours=8)
        if now - last < gap:
            return ""
    return mode


if __name__ == "__main__":
    print(decide(dt.datetime.now(ET), sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None))
