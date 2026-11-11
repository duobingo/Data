# Setting up the feed in a new repository (safe start)

Lesson learned: a brand-new account that suddenly starts many automated runs gets flagged
as abuse. Start slowly and keep every run short.

1. Create a **public** repository and add two repository secrets (Settings → Secrets and
   variables → Actions): `FINNHUB_API_KEY` and `SEC_USER_AGENT`.
2. Push this code. Then in the Actions tab, run **Data pull** once by hand (mode: close).
   Check that it finishes and commits data. Do nothing else that day.
3. Leave the set-time schedule in **Data pull** to run on its own: about 12 short runs
   per weekday (premarket, hourly during market hours, after the close) and one on Sunday.
   Runs that land at the wrong time or repeat a finished pull exit within seconds.
4. After 2 trading days, check `data/status.md`. If the set-time runs are firing, you're done.
5. Only if the set-time schedule never fires: start **Scheduler (fallback only)** once by hand.
   It never hands off early and never re-launches after a run shorter than 10 minutes.
   Never run both the fallback and the set-time schedule for long.

Rules that keep runs normal-looking:
- No workflow re-launches itself in a loop, and none starts on every push.
- Runs never cancel each other (`cancel-in-progress: false`); a second run waits.
- Every job has a time limit (40 minutes for a pull).
- Nothing personal is ever committed: `scripts/privacy_check.py` runs before every commit.
