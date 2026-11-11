Generated 2026-11-11 10:28 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 8 | 38 | -4.68 | 9.7 | -13.31 | -15.47 | 0.44 | 7.9 | 1.10 (3) | $-702 ($-702) | 19.76 | 20.48 | 26.63 | BUY SIGNAL |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 6.88 | 5.84 | 6.91 |  |
| SOFI | SOFI | ✗ | 8 | 38 | -1.08 | 13.87 | -10.05 | -12.62 | 0.83 | 6.8 | 1.70 (4) | $-162 ($-162) | 16.38 | 13.7 | 15.89 |  |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 66.87 | 45.36 | 54.84 |  |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 34.33 | 27.13 | 31.58 |  |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 13.52 | 10.98 | 12.69 |  |
| LCID | LCID | ✗ | 11 | 45 | -2.61 | 8.17 | -11.6 | -17.56 | 0.59 | 7.2 | 0.29 (3) | $-392 ($-392) | 3.82 | 2.83 | 3.32 |  |
| SOUN | SOUN | ✗ | 9 | 22 | -6.16 | 7.61 | -10.1 | -18.01 | 0.22 | 7.8 | 0.35 (5) | $-924 ($-924) | 3.91 | 3.79 | 4.34 | near |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 4.88 | 3.58 | 4.21 |  |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 2.33 (5) | $744 ($372) | 26.09 | 20.94 | 25.81 |  |

## Today's swing signals (passing names that closed below the lower band)
- **SYF** close 71.07 · entry: limit near 71.07 at the open · stop 66.14 (-6.9%) · target 20-day avg 74.32 (+4.6%) · 211 shares ≈ $15.0K · exit by 10 trading days · backtest: 8 trades, 62% wins, avg 1.1%, PF 1.55
- Watch name **HIMS** closed below its lower band (FAILS the backtest — do not trade). Stop 15.16, target 26.63, 434 shares ≈ $8.6K.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NRG | NRG Energy | ✓ | 9 | 89 | 6.42 | 8.38 | -9.21 | -9.21 | 7.27 | 5.6 | 99.00 (5) | $963 ($482) | 98.97 | 83.82 | 95.31 |  |
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 50.79 | 43.13 | 49.04 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 331.57 | 307.54 | 326.7 |  |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 82.74 | 64.4 | 76.31 |  |
| ACM | AECOM | ✓ | 10 | 80 | 2.04 | 3.69 | -4.54 | -5.05 | 3.25 | 7.3 | 99.00 (5) | $306 ($153) | 70.1 | 55.25 | 63.59 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 246.01 | 225.65 | 238.6 |  |
| ARE | Alexandria Real Estate Equities | ✓ | 8 | 62 | 1.9 | 8.55 | -9.18 | -11.21 | 1.55 | 8.6 | 99.00 (1) | $285 ($142) | 43.64 | 39.09 | 42.79 |  |
| SRE | Sempra | ✓ | 12 | 75 | 1.24 | 2.76 | -3.3 | -5.14 | 2.5 | 5.3 | 2.07 (8) | $186 ($93) | 78.32 | 77.33 | 82.79 |  |
| VTR | Ventas | ✓ | 8 | 75 | 1.61 | 3.56 | -4.25 | -4.66 | 2.52 | 6.1 | 1.71 (5) | $242 ($121) | 90.29 | 81.65 | 86.6 |  |
| KBR | KBR, Inc. | ✓ | 9 | 56 | 1.19 | 5.45 | -4.15 | -8.34 | 1.64 | 7.6 | 1.04 (3) | $178 ($89) | 37.85 | 35.87 | 38.48 |  |
| KNSL | Kinsale Capital Group | ✓ | 8 | 62 | 1.3 | 5.21 | -5.22 | -7.42 | 1.66 | 8.0 | 1.45 (3) | $195 ($98) | 387.77 | 349.44 | 375.84 |  |
| GWRE | Guidewire Software | ✓ | 9 | 56 | 1.05 | 7.31 | -6.77 | -9.71 | 1.35 | 8.6 | 99.00 (2) | $158 ($79) | 155.12 | 148.32 | 169.86 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.47 (3) | $165 ($82) | 71.07 | 71.46 | 74.32 | BUY SIGNAL |
| CCI | Crown Castle | ✓ | 10 | 50 | 0.86 | 6.95 | -5.22 | -6.99 | 1.33 | 5.2 | 1.00 (5) | $129 ($64) | 88.9 | 77.77 | 86.0 |  |
| TPL | Texas Pacific Land Corporation | ✓ | 9 | 67 | 0.91 | 5.5 | -8.27 | -8.78 | 1.33 | 5.0 | 2.98 (5) | $136 ($68) | 282.48 | 262.07 | 319.27 |  |
| DTM | DT Midstream | ✓ | 8 | 75 | 1.0 | 2.27 | -2.82 | -5.5 | 2.42 | 6.9 | 1.48 (5) | $150 ($75) | 119.84 | 113.12 | 121.68 |  |
| ALLY | Ally Financial | ✓ | 10 | 70 | 0.79 | 3.87 | -6.41 | -7.31 | 1.41 | 6.2 | 1.69 (4) | $118 ($59) | 37.79 | 37.2 | 38.45 |  |
| EEFT | Euronet Worldwide | ✓ | 9 | 44 | 0.85 | 8.15 | -4.98 | -7.44 | 1.31 | 7.7 | 2.48 (3) | $128 ($64) | 69.56 | 59.33 | 66.3 |  |
| GNTX | Gentex | ✓ | 9 | 56 | 0.85 | 4.65 | -3.89 | -5.25 | 1.49 | 6.2 | 1.74 (5) | $128 ($64) | 19.24 | 19.1 | 20.42 | near |
| TDG | TransDigm Group | ✓ | 8 | 50 | 0.67 | 4.48 | -3.14 | -5.43 | 1.43 | 8.6 | 1.61 (3) | $100 ($50) | 1228.39 | 1087.19 | 1167.59 |  |

Screened 492 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 20 pass.
