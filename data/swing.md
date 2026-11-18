Generated 2026-11-18 16:44 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 7 | 43 | -3.39 | 9.7 | -13.2 | -15.47 | 0.55 | 7.4 | 0.76 (2) | $-508 ($-508) | 17.05 | 15.54 | 24.11 |  |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 6.08 | 5.46 | 6.58 |  |
| SOFI | SOFI | ✗ | 8 | 38 | -1.08 | 13.87 | -10.05 | -12.62 | 0.83 | 6.8 | 1.70 (4) | $-162 ($-162) | 14.11 | 13.75 | 15.92 | near |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 53.07 | 46.37 | 56.26 |  |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 23.48 | 23.87 | 30.3 | BUY SIGNAL |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 11.8 | 10.79 | 12.59 |  |
| LCID | LCID | ✗ | 10 | 50 | -1.58 | 8.17 | -11.34 | -17.56 | 0.72 | 6.8 | 0.29 (3) | $-237 ($-237) | 2.94 | 2.68 | 3.24 |  |
| SOUN | SOUN | ✗ | 10 | 20 | -7.11 | 7.61 | -10.79 | -18.01 | 0.18 | 7.3 | 0.24 (6) | $-1.1K ($-1.1K) | 3.01 | 3.05 | 3.98 | BUY SIGNAL |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 3.23 | 3.32 | 4.14 | BUY SIGNAL |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 1.54 (4) | $744 ($372) | 21.8 | 20.17 | 24.55 |  |

## Today's swing signals (passing names that closed below the lower band)
- **KBR** close 33.08 · entry: limit near 33.08 at the open · stop 29.6 (-10.5%) · target 20-day avg 37.91 (+14.6%) · 453 shares ≈ $15.0K · exit by 10 trading days · backtest: 9 trades, 56% wins, avg 1.19%, PF 1.64
- Watch name **IONQ** closed below its lower band (FAILS the backtest — do not trade). Stop 17.32, target 30.3, 324 shares ≈ $7.6K.
- Watch name **SOUN** closed below its lower band (FAILS the backtest — do not trade). Stop 2.44, target 3.98, 3539 shares ≈ $10.7K.
- Watch name **ACHR** closed below its lower band (FAILS the backtest — do not trade). Stop 2.4, target 4.14, 2411 shares ≈ $7.8K.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NRG | NRG Energy | ✓ | 9 | 89 | 6.42 | 8.38 | -9.21 | -9.21 | 7.27 | 5.6 | 99.00 (5) | $963 ($482) | 93.66 | 84.28 | 93.78 |  |
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 52.05 | 47.97 | 50.52 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 305.82 | 300.77 | 324.73 | near |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 83.66 | 69.73 | 79.53 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 247.25 | 227.97 | 241.25 |  |
| ARE | Alexandria Real Estate Equities | ✓ | 8 | 62 | 1.9 | 8.55 | -9.18 | -11.21 | 1.55 | 8.6 | 99.00 (1) | $285 ($142) | 42.37 | 39.55 | 43.21 |  |
| SRE | Sempra | ✓ | 12 | 75 | 1.24 | 2.76 | -3.3 | -5.14 | 2.5 | 5.3 | 1.88 (7) | $186 ($93) | 77.52 | 74.98 | 81.72 |  |
| KBR | KBR, Inc. | ✓ | 9 | 56 | 1.19 | 5.45 | -4.15 | -8.34 | 1.64 | 7.6 | 1.04 (3) | $178 ($89) | 33.08 | 33.63 | 37.91 | BUY SIGNAL |
| KNSL | Kinsale Capital Group | ✓ | 8 | 62 | 1.3 | 5.21 | -5.22 | -7.42 | 1.66 | 8.0 | 1.45 (3) | $195 ($98) | 398.47 | 354.68 | 383.18 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.47 (3) | $165 ($82) | 70.16 | 69.75 | 73.72 | near |
| CCI | Crown Castle | ✓ | 10 | 50 | 0.86 | 6.95 | -5.22 | -6.99 | 1.33 | 5.2 | 1.00 (5) | $129 ($64) | 83.94 | 81.86 | 87.75 |  |
| ALLY | Ally Financial | ✓ | 10 | 70 | 0.79 | 3.87 | -6.41 | -7.31 | 1.41 | 6.2 | 1.69 (4) | $118 ($59) | 37.67 | 37.27 | 38.47 | near |
| EEFT | Euronet Worldwide | ✓ | 9 | 44 | 0.85 | 8.15 | -4.98 | -7.44 | 1.31 | 7.7 | 2.48 (3) | $128 ($64) | 68.0 | 59.82 | 67.31 |  |
| GNTX | Gentex | ✓ | 9 | 56 | 0.85 | 4.65 | -3.89 | -5.25 | 1.49 | 6.2 | 1.74 (5) | $128 ($64) | 19.33 | 18.52 | 19.96 |  |

Screened 483 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 14 pass.
