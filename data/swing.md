Generated 2026-11-13 17:11 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 8 | 38 | -4.68 | 9.7 | -13.3 | -15.47 | 0.44 | 7.9 | 0.76 (2) | $-702 ($-702) | 19.73 | 18.71 | 25.78 | near |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 6.08 | 5.78 | 6.8 | near |
| SOFI | SOFI | ✗ | 8 | 38 | -1.08 | 13.87 | -10.05 | -12.62 | 0.83 | 6.8 | 1.70 (4) | $-162 ($-162) | 15.42 | 13.88 | 15.95 |  |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 61.53 | 45.45 | 55.78 |  |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 28.88 | 26.9 | 31.28 |  |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 12.18 | 10.95 | 12.67 |  |
| LCID | LCID | ✗ | 10 | 50 | -1.58 | 8.17 | -11.34 | -17.56 | 0.72 | 6.8 | 0.29 (3) | $-237 ($-237) | 2.95 | 2.81 | 3.29 | near |
| SOUN | SOUN | ✗ | 9 | 22 | -6.16 | 7.61 | -10.1 | -18.01 | 0.22 | 7.8 | 0.35 (5) | $-924 ($-924) | 3.49 | 3.57 | 4.22 | BUY SIGNAL |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 4.03 | 3.59 | 4.21 |  |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 2.33 (5) | $744 ($372) | 23.92 | 20.94 | 25.32 |  |

## Today's swing signals (passing names that closed below the lower band)
- None today.
- Watch name **SOUN** closed below its lower band (FAILS the backtest — do not trade). Stop 2.93, target 4.22, 3560 shares ≈ $12.4K.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 49.72 | 44.74 | 49.6 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 323.01 | 308.17 | 327.21 |  |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 83.02 | 65.98 | 77.55 |  |
| ACM | AECOM | ✓ | 10 | 80 | 2.04 | 3.69 | -4.54 | -5.05 | 3.25 | 7.3 | 99.00 (4) | $306 ($153) | 70.5 | 56.08 | 64.72 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 244.46 | 226.37 | 239.66 |  |
| ARE | Alexandria Real Estate Equities | ✓ | 8 | 62 | 1.9 | 8.55 | -9.18 | -11.21 | 1.55 | 8.6 | 99.00 (1) | $285 ($142) | 43.84 | 39.24 | 43.07 |  |
| SRE | Sempra | ✓ | 12 | 75 | 1.24 | 2.76 | -3.3 | -5.14 | 2.5 | 5.3 | 2.07 (8) | $186 ($93) | 79.54 | 76.57 | 82.44 |  |
| VTR | Ventas | ✓ | 8 | 75 | 1.61 | 3.56 | -4.25 | -4.66 | 2.52 | 6.1 | 1.71 (5) | $242 ($121) | 88.92 | 81.87 | 87.0 |  |
| KBR | KBR, Inc. | ✓ | 9 | 56 | 1.19 | 5.45 | -4.15 | -8.34 | 1.64 | 7.6 | 1.04 (3) | $178 ($89) | 35.59 | 35.19 | 38.31 | near |
| KNSL | Kinsale Capital Group | ✓ | 8 | 62 | 1.3 | 5.21 | -5.22 | -7.42 | 1.66 | 8.0 | 1.45 (3) | $195 ($98) | 395.89 | 352.59 | 379.24 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.47 (3) | $165 ($82) | 72.25 | 71.13 | 74.18 | near |
| TPL | Texas Pacific Land Corporation | ✓ | 9 | 67 | 0.91 | 5.5 | -8.27 | -8.78 | 1.33 | 5.0 | 2.98 (5) | $136 ($68) | 291.91 | 256.27 | 313.0 |  |
| DTM | DT Midstream | ✓ | 8 | 75 | 1.0 | 2.27 | -2.82 | -5.5 | 2.42 | 6.9 | 1.48 (5) | $150 ($75) | 119.73 | 112.94 | 121.48 |  |
| ALLY | Ally Financial | ✓ | 10 | 70 | 0.79 | 3.87 | -6.41 | -7.31 | 1.41 | 6.2 | 1.69 (4) | $118 ($59) | 38.31 | 37.39 | 38.52 |  |
| EEFT | Euronet Worldwide | ✓ | 9 | 44 | 0.85 | 8.15 | -4.98 | -7.44 | 1.31 | 7.7 | 2.48 (3) | $128 ($64) | 71.11 | 59.39 | 66.87 |  |
| GNTX | Gentex | ✓ | 9 | 56 | 0.85 | 4.65 | -3.89 | -5.25 | 1.49 | 6.2 | 1.74 (5) | $128 ($64) | 19.2 | 18.9 | 20.26 |  |

Screened 480 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 16 pass.
