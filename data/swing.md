Generated 2026-11-23 16:43 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 7 | 43 | -3.39 | 9.7 | -13.2 | -15.47 | 0.55 | 7.4 | 0.76 (2) | $-508 ($-508) | 15.06 | 12.32 | 22.17 |  |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 5.74 | 5.12 | 6.42 |  |
| SOFI | SOFI | ✗ | 8 | 38 | -1.08 | 13.87 | -10.05 | -12.62 | 0.83 | 6.8 | 1.70 (4) | $-162 ($-162) | 13.09 | 12.73 | 15.68 | near |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 49.63 | 44.42 | 55.68 |  |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 23.34 | 20.31 | 28.98 |  |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 11.22 | 10.34 | 12.47 |  |
| LCID | LCID | ✗ | 10 | 50 | -1.58 | 8.17 | -11.34 | -17.56 | 0.72 | 6.8 | 0.29 (3) | $-237 ($-237) | 2.61 | 2.44 | 3.12 | near |
| SOUN | SOUN | ✗ | 10 | 20 | -7.11 | 7.61 | -10.79 | -18.01 | 0.18 | 7.3 | 0.24 (6) | $-1.1K ($-1.1K) | 2.89 | 2.56 | 3.75 |  |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 3.07 | 2.87 | 4.01 | near |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 1.54 (4) | $744 ($372) | 20.77 | 18.76 | 23.66 |  |

## Today's swing signals (passing names that closed below the lower band)
- None today.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NRG | NRG Energy | ✓ | 9 | 89 | 6.42 | 8.38 | -9.21 | -9.21 | 7.27 | 5.6 | 99.00 (5) | $963 ($482) | 97.72 | 83.71 | 93.74 |  |
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 51.68 | 48.7 | 50.86 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 304.13 | 289.6 | 321.84 |  |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 81.31 | 73.92 | 80.98 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 240.93 | 228.67 | 241.71 |  |
| CDP | COPT Defense Properties | ✓ | 8 | 62 | 1.81 | 4.02 | -1.88 | -4.16 | 3.57 | 6.1 | 2.20 (4) | $272 ($136) | 31.93 | 31.83 | 33.0 | near |
| EEFT | Euronet Worldwide | ✓ | 8 | 50 | 1.75 | 8.15 | -4.64 | -7.56 | 1.76 | 7.9 | 2.48 (3) | $262 ($131) | 67.11 | 59.78 | 67.3 |  |
| VTR | Ventas | ✓ | 8 | 75 | 1.61 | 3.56 | -4.25 | -4.66 | 2.52 | 6.1 | 1.71 (5) | $242 ($121) | 87.01 | 82.4 | 87.41 |  |
| SRE | Sempra | ✓ | 13 | 69 | 0.9 | 2.76 | -3.28 | -5.14 | 1.89 | 5.8 | 1.41 (8) | $135 ($68) | 77.72 | 73.4 | 80.57 |  |
| KNSL | Kinsale Capital Group | ✓ | 8 | 62 | 1.3 | 5.21 | -5.22 | -7.42 | 1.66 | 8.0 | 1.45 (3) | $195 ($98) | 396.34 | 358.83 | 386.45 |  |
| GNTX | Gentex | ✓ | 8 | 62 | 1.2 | 4.65 | -4.54 | -5.25 | 1.7 | 5.6 | 1.74 (5) | $180 ($90) | 19.54 | 18.52 | 19.68 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.47 (3) | $165 ($82) | 67.96 | 67.24 | 72.77 | near |
| CCI | Crown Castle | ✓ | 10 | 50 | 0.86 | 6.95 | -5.22 | -6.99 | 1.33 | 5.2 | 1.00 (5) | $129 ($64) | 81.24 | 81.18 | 87.41 | near |

Screened 490 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 13 pass.
