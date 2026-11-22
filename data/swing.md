Generated 2026-11-22 18:12 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 7 | 43 | -3.39 | 9.7 | -13.2 | -15.47 | 0.55 | 7.4 | 0.76 (2) | $-508 ($-508) | 14.6 | 13.26 | 22.8 |  |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 5.4 | 5.2 | 6.47 | near |
| SOFI | SOFI | ✗ | 8 | 38 | -1.08 | 13.87 | -10.05 | -12.62 | 0.83 | 6.8 | 1.70 (4) | $-162 ($-162) | 12.48 | 12.99 | 15.75 | BUY SIGNAL |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 45.42 | 44.95 | 55.89 | near |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 20.72 | 21.07 | 29.35 | BUY SIGNAL |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 10.33 | 10.37 | 12.48 | BUY SIGNAL |
| LCID | LCID | ✗ | 10 | 50 | -1.58 | 8.17 | -11.34 | -17.56 | 0.72 | 6.8 | 0.29 (3) | $-237 ($-237) | 2.5 | 2.51 | 3.16 | BUY SIGNAL |
| SOUN | SOUN | ✗ | 10 | 20 | -7.11 | 7.61 | -10.79 | -18.01 | 0.18 | 7.3 | 0.24 (6) | $-1.1K ($-1.1K) | 2.61 | 2.68 | 3.81 | BUY SIGNAL |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 2.91 | 3.0 | 4.06 | BUY SIGNAL |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 1.54 (4) | $744 ($372) | 19.85 | 19.11 | 23.92 | near |

## Today's swing signals (passing names that closed below the lower band)
- **CDNS** close 281.58 · entry: limit near 281.58 at the open · stop 251.52 (-10.7%) · target 20-day avg 322.75 (+14.6%) · 53 shares ≈ $14.9K · exit by 10 trading days · backtest: 8 trades, 88% wins, avg 4.04%, PF 5.25
- **CDP** close 31.87 · entry: limit near 31.87 at the open · stop 30.39 (-4.7%) · target 20-day avg 33.11 (+3.9%) · 470 shares ≈ $15.0K · exit by 10 trading days · backtest: 8 trades, 62% wins, avg 1.81%, PF 3.57
- **SYF** close 67.76 · entry: limit near 67.76 at the open · stop 62.81 (-7.3%) · target 20-day avg 73.11 (+7.9%) · 221 shares ≈ $15.0K · exit by 10 trading days · backtest: 8 trades, 62% wins, avg 1.1%, PF 1.55
- Watch name **SOFI** closed below its lower band (FAILS the backtest — do not trade). Stop 10.82, target 15.75, 1201 shares ≈ $15.0K.
- Watch name **IONQ** closed below its lower band (FAILS the backtest — do not trade). Stop 14.62, target 29.35, 327 shares ≈ $6.8K.
- Watch name **RIVN** closed below its lower band (FAILS the backtest — do not trade). Stop 8.94, target 12.48, 1443 shares ≈ $14.9K.
- Watch name **LCID** closed below its lower band (FAILS the backtest — do not trade). Stop 1.8, target 3.16, 2865 shares ≈ $7.2K.
- Watch name **SOUN** closed below its lower band (FAILS the backtest — do not trade). Stop 2.05, target 3.81, 3562 shares ≈ $9.3K.
- Watch name **ACHR** closed below its lower band (FAILS the backtest — do not trade). Stop 2.07, target 4.06, 2372 shares ≈ $6.9K.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 50.05 | 48.62 | 50.78 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 281.58 | 291.6 | 322.75 | BUY SIGNAL |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 80.64 | 72.4 | 80.51 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 240.34 | 228.65 | 241.69 |  |
| KD | Kyndryl | ✓ | 8 | 50 | 1.93 | 10.25 | -6.39 | -9.72 | 1.61 | 7.8 | 1.24 (2) | $290 ($145) | 15.12 | 12.75 | 15.52 |  |
| EEFT | Euronet Worldwide | ✓ | 8 | 50 | 1.82 | 8.15 | -4.5 | -7.01 | 1.81 | 7.5 | 2.48 (3) | $273 ($136) | 64.4 | 59.48 | 67.14 |  |
| CDP | COPT Defense Properties | ✓ | 8 | 62 | 1.81 | 4.02 | -1.88 | -4.16 | 3.57 | 6.1 | 2.20 (4) | $272 ($136) | 31.87 | 31.95 | 33.11 | BUY SIGNAL |
| VTR | Ventas | ✓ | 8 | 75 | 1.61 | 3.56 | -4.25 | -4.66 | 2.52 | 6.1 | 1.71 (5) | $242 ($121) | 86.55 | 82.43 | 87.43 |  |
| SRE | Sempra | ✓ | 13 | 69 | 0.9 | 2.76 | -3.28 | -5.14 | 1.89 | 5.8 | 1.41 (8) | $135 ($68) | 76.16 | 73.68 | 80.9 |  |
| KNSL | Kinsale Capital Group | ✓ | 8 | 62 | 1.3 | 5.21 | -5.22 | -7.42 | 1.66 | 8.0 | 1.45 (3) | $195 ($98) | 398.58 | 356.98 | 385.12 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.47 (3) | $165 ($82) | 67.76 | 68.01 | 73.11 | BUY SIGNAL |
| CCI | Crown Castle | ✓ | 10 | 50 | 0.86 | 6.95 | -5.22 | -6.99 | 1.33 | 5.2 | 1.00 (5) | $129 ($64) | 82.4 | 82.21 | 87.72 | near |

Screened 463 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 12 pass.
