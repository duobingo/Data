#!/usr/bin/env python3
"""Self-running scheduler (GitHub's cron wasn't firing for this repo).

Runs inside one GitHub Actions job for up to ~5.5 hours: waits for each slot, runs the
pull (and the scan after the close / on Sunday), commits the data, and before the job
time limit re-launches itself (the workflow step after this script does that).

Slots (US Eastern time):
  Weekdays  07:25 premarket · 09:45–15:45 hourly intraday · 16:35 close
  Sunday    17:15 weekly
"""
import datetime as dt
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
BUDGET_MIN = 330  # stop looking for slots after this; the job limit is 350


def slots_for(day):
    wd = day.weekday()
    out = []
    if wd < 5:
        out.append((dt.time(7, 25), "premarket"))
        out += [(dt.time(h, 45), "intraday") for h in range(9, 16)]
        out.append((dt.time(16, 35), "close"))
    elif wd == 6:
        out.append((dt.time(17, 15), "weekly"))
    return [(dt.datetime.combine(day, t, ET), m) for t, m in out]


def next_slot(now):
    for d in range(0, 4):
        day = (now + dt.timedelta(days=d)).date()
        for when, mode in slots_for(day):
            if when > now:
                return when, mode
    return None, None


def sh(cmd):
    print("+", cmd, flush=True)
    return subprocess.run(cmd, shell=True).returncode


def commit(mode):
    if sh("python scripts/privacy_check.py") != 0:
        print("Privacy check failed: discarding this pull's changes instead of publishing them.")
        sh("git checkout -- data && git clean -fdq data")
        return
    sh("git add data")
    if subprocess.run("git diff --cached --quiet", shell=True).returncode == 0:
        print("No data changes.")
        return
    sh(f'git commit -q -m "Data pull ({mode}) $(date -u +"%Y-%m-%d %H:%M") UTC"')
    for _ in range(3):
        if sh("git pull -q --rebase -X theirs") == 0 and sh("git push -q") == 0:
            return
        time.sleep(10)


def write_status(mode, rc):
    import json
    import pathlib
    p = pathlib.Path("data/status.json")
    st = json.loads(p.read_text()) if p.exists() else {}
    now = dt.datetime.now(ET)
    st[mode] = {"time_et": now.strftime("%Y-%m-%d %H:%M"), "ok": rc == 0}
    p.write_text(json.dumps(st, indent=1))
    lines = ["# Data feed status", "",
             "Last run of each pull (ET). The feed runs 7:25 AM premarket, hourly 9:45 AM–3:45 PM, "
             "4:35 PM close (weekdays) and 5:15 PM Sunday. A report should say \"data feed stale\" if the "
             "pull it depends on is older than expected.", "",
             "| Pull | Last run (ET) | OK |", "|---|---|---|"]
    for m in ("premarket", "intraday", "close", "weekly"):
        v = st.get(m)
        lines.append(f"| {m} | {v['time_et'] if v else '—'} | {('yes' if v['ok'] else 'ERRORS') if v else '—'} |")
    pathlib.Path("data/status.md").write_text("\n".join(lines) + "\n")


def run_slot(mode):
    sh("git pull -q --rebase -X theirs")
    rc = sh(f"python scripts/pull.py --mode {mode}")
    if mode in ("close", "weekly"):
        rc |= sh(f"python scripts/scan.py --mode {mode}")
    write_status(mode, rc)
    commit(mode)


def missed_slot(now):
    """A slot from the last 90 minutes that hasn't run yet (e.g. the loop was down)."""
    import json
    import pathlib
    p = pathlib.Path("data/status.json")
    st = json.loads(p.read_text()) if p.exists() else {}
    for when, mode in reversed(slots_for(now.date())):
        if when <= now and now - when <= dt.timedelta(minutes=90):
            last = st.get(mode, {}).get("time_et", "")
            if last < when.strftime("%Y-%m-%d %H:%M"):
                return mode
            return None
    return None


def main():
    start = dt.datetime.now(ET)
    deadline = start + dt.timedelta(minutes=BUDGET_MIN)
    m = missed_slot(start)
    if m:
        print(f"Catching up on missed {m} pull", flush=True)
        run_slot(m)
    while True:
        now = dt.datetime.now(ET)
        when, mode = next_slot(now)
        if when is None or when > deadline:
            # Wait out this job's window (or until 30 min before the slot) so the next
            # run starts in time -- never hand off immediately, which caused a rapid relaunch loop.
            until = deadline if when is None else min(deadline, when - dt.timedelta(minutes=30))
            wait = (until - now).total_seconds()
            if wait > 0:
                print(f"Next slot {when} {mode} is after this job's window; idling {wait/60:.0f} min, then handing off.", flush=True)
                time.sleep(wait)
            return 0
        wait = (when - now).total_seconds()
        print(f"Sleeping {wait/60:.0f} min until {when:%a %H:%M} ET ({mode})", flush=True)
        time.sleep(max(0, wait))
        run_slot(mode)


if __name__ == "__main__":
    sys.exit(main())
