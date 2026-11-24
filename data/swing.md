Generated 2026-11-24 16:45 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 7 | 43 | -3.39 | 9.7 | -13.2 | -15.47 | 0.55 | 7.4 | 0.76 (2) | $-508 ($-508) | 14.74 | 11.52 | 21.51 |  |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 5.6 | 5.07 | 6.33 |  |
| SOFI | SOFI | ✗ | 8 | 38 | -1.08 | 13.87 | -10.05 | -12.62 | 0.83 | 6.8 | 1.70 (4) | $-162 ($-162) | 12.86 | 12.31 | 15.51 |  |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 45.98 | 43.08 | 55.06 | near |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 22.4 | 19.52 | 28.45 |  |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 11.35 | 10.27 | 12.45 |  |
| LCID | LCID | ✗ | 10 | 50 | -1.58 | 8.17 | -11.34 | -17.56 | 0.72 | 6.8 | 0.29 (3) | $-237 ($-237) | 2.64 | 2.38 | 3.09 |  |
| SOUN | SOUN | ✗ | 10 | 20 | -7.11 | 7.61 | -10.79 | -18.01 | 0.18 | 7.3 | 0.24 (6) | $-1.1K ($-1.1K) | 2.62 | 2.41 | 3.66 |  |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 2.88 | 2.7 | 3.95 | near |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 1.54 (4) | $744 ($372) | 19.2 | 18.28 | 23.25 | near |

## Today's swing signals (passing names that closed below the lower band)
- None today.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 51.67 | 48.72 | 50.91 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 296.6 | 287.02 | 319.52 |  |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 82.52 | 76.22 | 81.55 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 245.14 | 231.6 | 242.63 |  |
| CDP | COPT Defense Properties | ✓ | 8 | 62 | 1.81 | 4.02 | -1.88 | -4.16 | 3.57 | 6.1 | 2.20 (4) | $272 ($136) | 32.24 | 31.78 | 32.92 |  |
| EEFT | Euronet Worldwide | ✓ | 8 | 50 | 1.77 | 8.15 | -4.61 | -7.44 | 1.77 | 8.2 | 2.48 (3) | $266 ($133) | 67.67 | 61.31 | 67.73 |  |
| VTR | Ventas | ✓ | 8 | 75 | 1.61 | 3.56 | -4.25 | -4.66 | 2.52 | 6.1 | 1.71 (5) | $242 ($121) | 87.17 | 82.97 | 87.6 |  |
| KNSL | Kinsale Capital Group | ✓ | 8 | 62 | 1.49 | 5.21 | -4.7 | -7.42 | 1.85 | 8.0 | 1.45 (3) | $224 ($112) | 408.22 | 362.4 | 388.82 |  |
| CCI | Crown Castle | ✓ | 10 | 60 | 1.18 | 5.96 | -5.99 | -6.99 | 1.49 | 5.2 | 1.00 (5) | $177 ($88) | 82.71 | 80.58 | 87.15 |  |
| SRE | Sempra | ✓ | 13 | 69 | 0.9 | 2.76 | -3.28 | -5.14 | 1.89 | 5.8 | 1.41 (8) | $135 ($68) | 78.76 | 73.36 | 80.26 |  |
| GNTX | Gentex | ✓ | 8 | 62 | 1.2 | 4.65 | -4.54 | -5.25 | 1.7 | 5.6 | 1.74 (5) | $180 ($90) | 19.46 | 18.51 | 19.64 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.47 (3) | $165 ($82) | 67.91 | 66.59 | 72.42 |  |
| MDLZ | Mondelez International | ✓ | 9 | 56 | 0.79 | 3.16 | -2.16 | -4.23 | 1.83 | 6.9 | 2.69 (4) | $118 ($59) | 67.01 | 63.08 | 66.05 |  |

Screened 468 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 13 pass.
