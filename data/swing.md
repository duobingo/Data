Generated 2026-11-27 16:46 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 7 | 43 | -3.39 | 9.7 | -13.2 | -15.47 | 0.55 | 7.4 | 0.76 (2) | $-508 ($-508) | 15.0 | 10.94 | 20.05 |  |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 5.79 | 5.18 | 6.13 |  |
| SOFI | SOFI | ✗ | 9 | 33 | -2.32 | 13.87 | -10.41 | -12.62 | 0.67 | 6.3 | 0.95 (5) | $-348 ($-348) | 13.37 | 11.9 | 15.09 |  |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 50.88 | 41.8 | 54.07 |  |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 24.97 | 18.77 | 27.67 |  |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 12.18 | 10.36 | 12.48 |  |
| LCID | LCID | ✗ | 10 | 50 | -1.58 | 8.17 | -11.34 | -17.56 | 0.72 | 6.8 | 0.29 (3) | $-237 ($-237) | 2.6 | 2.26 | 3.01 |  |
| SOUN | SOUN | ✗ | 11 | 18 | -8.15 | 7.61 | -11.65 | -18.47 | 0.15 | 7.1 | 0.18 (7) | $-1.2K ($-1.2K) | 2.78 | 2.23 | 3.49 |  |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 3.22 | 2.52 | 3.82 |  |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 1.54 (4) | $744 ($372) | 20.85 | 17.97 | 22.57 |  |

## Today's swing signals (passing names that closed below the lower band)
- None today.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NRG | NRG Energy | ✓ | 9 | 89 | 6.42 | 8.38 | -9.21 | -9.21 | 7.27 | 5.6 | 99.00 (5) | $963 ($482) | 93.83 | 83.32 | 93.08 |  |
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 53.86 | 48.68 | 51.27 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 303.91 | 284.67 | 315.2 |  |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 84.62 | 78.33 | 82.33 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 249.69 | 237.15 | 244.4 |  |
| VTR | Ventas | ✓ | 8 | 75 | 1.61 | 3.56 | -4.25 | -4.66 | 2.52 | 6.1 | 1.71 (5) | $242 ($121) | 88.59 | 85.3 | 88.16 |  |
| ALLY | Ally Financial | ✓ | 11 | 73 | 1.08 | 3.88 | -6.41 | -7.31 | 1.62 | 6.0 | 1.68 (4) | $162 ($81) | 38.75 | 36.62 | 38.02 |  |
| SRE | Sempra | ✓ | 13 | 69 | 0.9 | 2.76 | -3.28 | -5.14 | 1.89 | 5.8 | 1.41 (8) | $135 ($68) | 79.05 | 73.65 | 79.64 |  |
| CCI | Crown Castle | ✓ | 10 | 60 | 1.17 | 5.94 | -5.99 | -6.99 | 1.49 | 5.2 | 1.00 (5) | $176 ($88) | 84.2 | 79.92 | 86.72 |  |
| GNTX | Gentex | ✓ | 8 | 62 | 1.2 | 4.65 | -4.54 | -5.25 | 1.7 | 5.6 | 1.74 (5) | $180 ($90) | 19.87 | 18.52 | 19.6 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.47 (3) | $165 ($82) | 69.77 | 66.24 | 71.73 |  |
| MDLZ | Mondelez International | ✓ | 9 | 56 | 0.6 | 3.16 | -2.6 | -4.23 | 1.52 | 6.9 | 2.69 (4) | $90 ($45) | 67.77 | 65.02 | 66.61 |  |

Screened 479 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 12 pass.
