# market-data

Public US market data, refreshed automatically: prices (two-source check), SEC filings and insider trades,
earnings dates and estimates, analyst ratings, forward valuation, clinical-trial and FDA updates, a market-wide
scan of ~900 S&P 500/400 stocks, and a backtested swing screen.

- `scripts/` — the data pulls (`pull.py`, `scan.py`, `swing.py`), the run-time picker (`slot.py`), a fallback slot runner (`scheduler.py`) and a
  portfolio calculator (`portfolio.py`) that reads positions from a local file passed on the command line.
- `config/tickers.yml` — the tracked ticker list; `config/positions.example.yml` — format example with made-up numbers.
- `data/` — generated output.

No personal or account information is stored in this repository.
- `SETUP.md` — how to set this up in a new repository without tripping GitHub's abuse protection.
