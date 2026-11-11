Generated 2026-11-09 16:50 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 7 | 43 | -3.14 | 9.7 | -12.77 | -14.01 | 0.57 | 8.1 | 99.00 (2) | $-471 ($-471) | 22.94 | 23.72 | 27.55 | BUY SIGNAL |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 6.67 | 5.82 | 7.02 |  |
| SOFI | SOFI | ✗ | 8 | 38 | -1.08 | 13.87 | -10.05 | -12.62 | 0.83 | 6.8 | 1.70 (4) | $-162 ($-162) | 16.75 | 13.43 | 15.72 |  |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 58.86 | 46.26 | 54.53 |  |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 35.34 | 27.21 | 31.43 |  |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 14.01 | 11.01 | 12.64 |  |
| LCID | LCID | ✗ | 11 | 45 | -2.61 | 8.17 | -11.6 | -17.56 | 0.59 | 7.2 | 0.29 (3) | $-392 ($-392) | 3.6 | 2.9 | 3.27 |  |
| SOUN | SOUN | ✗ | 9 | 22 | -6.16 | 7.61 | -10.1 | -18.01 | 0.22 | 7.8 | 0.35 (5) | $-924 ($-924) | 4.05 | 3.91 | 4.42 |  |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 4.81 | 3.66 | 4.15 |  |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 2.33 (5) | $744 ($372) | 26.84 | 20.6 | 26.29 |  |

## Today's swing signals (passing names that closed below the lower band)
- None today.
- Watch name **HIMS** closed below its lower band (FAILS the backtest — do not trade). Stop 18.78, target 27.55, 481 shares ≈ $11.0K.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NRG | NRG Energy | ✓ | 9 | 89 | 6.42 | 8.38 | -9.21 | -9.21 | 7.27 | 5.6 | 4.93 (6) | $963 ($482) | 97.4 | 83.13 | 95.91 |  |
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 51.49 | 41.59 | 48.25 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 336.53 | 307.47 | 326.73 |  |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 84.03 | 63.11 | 74.86 |  |
| ACM | AECOM | ✓ | 10 | 80 | 2.04 | 3.69 | -4.54 | -5.05 | 3.25 | 7.3 | 99.00 (5) | $306 ($153) | 70.21 | 55.08 | 62.44 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 247.35 | 224.7 | 237.03 |  |
| ARE | Alexandria Real Estate Equities | ✓ | 8 | 62 | 1.9 | 8.55 | -9.18 | -11.21 | 1.55 | 8.6 | 99.00 (1) | $285 ($142) | 45.88 | 39.0 | 42.64 |  |
| SRE | Sempra | ✓ | 12 | 75 | 1.24 | 2.76 | -3.3 | -5.14 | 2.5 | 5.3 | 2.07 (8) | $186 ($93) | 78.77 | 78.58 | 83.17 | near |
| VTR | Ventas | ✓ | 8 | 75 | 1.61 | 3.56 | -4.25 | -4.66 | 2.52 | 6.1 | 1.71 (5) | $242 ($121) | 89.49 | 81.53 | 85.98 |  |
| KBR | KBR, Inc. | ✓ | 9 | 56 | 1.19 | 5.45 | -4.15 | -8.34 | 1.64 | 7.6 | 1.04 (3) | $178 ($89) | 38.65 | 34.93 | 38.17 |  |
| KNSL | Kinsale Capital Group | ✓ | 8 | 62 | 1.3 | 5.21 | -5.22 | -7.42 | 1.66 | 8.0 | 1.45 (3) | $195 ($98) | 386.07 | 341.19 | 371.01 |  |
| CART | Maplebear Inc. | ✓ | 8 | 50 | 1.26 | 9.22 | -6.71 | -7.61 | 1.38 | 8.0 | 2.36 (2) | $189 ($94) | 58.46 | 46.82 | 55.08 |  |
| GWRE | Guidewire Software | ✓ | 9 | 56 | 1.05 | 7.31 | -6.77 | -9.71 | 1.35 | 8.6 | 99.00 (2) | $158 ($79) | 160.84 | 151.4 | 170.86 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.95 (4) | $165 ($82) | 73.22 | 72.0 | 74.45 | near |
| CCI | Crown Castle | ✓ | 10 | 50 | 0.86 | 6.95 | -5.22 | -6.99 | 1.33 | 5.2 | 1.00 (5) | $129 ($64) | 87.83 | 76.23 | 85.03 |  |
| DTM | DT Midstream | ✓ | 8 | 75 | 1.0 | 2.27 | -2.82 | -5.5 | 2.42 | 6.9 | 1.48 (5) | $150 ($75) | 116.48 | 113.59 | 122.24 |  |
| ALLY | Ally Financial | ✓ | 10 | 70 | 0.79 | 3.87 | -6.41 | -7.31 | 1.41 | 6.2 | 1.69 (4) | $118 ($59) | 38.53 | 36.94 | 38.4 |  |
| EEFT | Euronet Worldwide | ✓ | 9 | 44 | 0.85 | 8.15 | -4.98 | -7.44 | 1.31 | 7.7 | 2.48 (3) | $128 ($64) | 70.92 | 59.12 | 65.68 |  |
| GNTX | Gentex | ✓ | 9 | 56 | 0.85 | 4.65 | -3.89 | -5.25 | 1.49 | 6.2 | 1.74 (5) | $128 ($64) | 19.5 | 19.47 | 20.57 | near |
| TDG | TransDigm Group | ✓ | 8 | 50 | 0.77 | 4.68 | -3.14 | -5.43 | 1.49 | 8.8 | 1.61 (3) | $116 ($58) | 1218.85 | 1080.11 | 1156.0 |  |

Screened 482 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 20 pass.
