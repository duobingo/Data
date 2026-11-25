Generated 2026-11-25 17:07 ET

# Swing scan (setup G) — range trades, backtested

Rule tested over ~2 years of daily prices: buy the open after a close below the lower band (20-day average − 2 std dev); stop 2 ATR below entry; sell at the first close back at the 20-day average; time stop 10 trading days; 0.1% slippage each side. PASS = 8+ trades, profit factor ≥ 1.3, average trade ≥ +0.5%, worst trade better than −12%, last 6 months not losing. Only PASS names (or a watch name that passes) may be traded under setup G.

Position: shares = min($2,000 ÷ (entry − stop), $15,000 ÷ entry). $ per trade assumes a $15K position; after-tax halves net gains.

## Watch names (tested every day regardless of screen)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HIMS | Hims & Hers Health | ✗ | 7 | 43 | -3.39 | 9.7 | -13.2 | -15.47 | 0.55 | 7.4 | 0.76 (2) | $-508 ($-508) | 14.65 | 11.05 | 20.78 |  |
| BFLY | BFLY | ✗ | 3 | 33 | 0.61 | 22.34 | -10.26 | -11.09 | 1.09 | 10.3 | 2.37 (2) | $92 ($46) | 5.49 | 5.1 | 6.22 |  |
| SOFI | SOFI | ✗ | 9 | 33 | -2.32 | 13.87 | -10.41 | -12.62 | 0.67 | 6.3 | 0.95 (5) | $-348 ($-348) | 13.07 | 12.03 | 15.3 |  |
| RKLB | RKLB | ✗ | 5 | 40 | -1.54 | 10.85 | -9.8 | -16.06 | 0.74 | 8.6 | 99.00 (1) | $-231 ($-231) | 47.02 | 42.11 | 54.48 |  |
| IONQ | IONQ | ✗ | 6 | 17 | -6.13 | 28.42 | -13.04 | -20.32 | 0.44 | 9.0 | 0.00 (2) | $-920 ($-920) | 23.54 | 19.02 | 28.01 |  |
| RIVN | RIVN | ✗ | 4 | 25 | -4.26 | 15.4 | -10.82 | -13.66 | 0.47 | 7.2 | 0.00 (2) | $-639 ($-639) | 11.71 | 10.28 | 12.45 |  |
| LCID | LCID | ✗ | 10 | 50 | -1.58 | 8.17 | -11.34 | -17.56 | 0.72 | 6.8 | 0.29 (3) | $-237 ($-237) | 2.56 | 2.32 | 3.04 |  |
| SOUN | SOUN | ✗ | 11 | 18 | -8.15 | 7.61 | -11.65 | -18.47 | 0.15 | 7.1 | 0.18 (7) | $-1.2K ($-1.2K) | 2.64 | 2.3 | 3.57 |  |
| ACHR | ACHR | ✗ | 7 | 29 | -4.37 | 10.64 | -10.37 | -20.59 | 0.41 | 9.0 | 0.49 (3) | $-656 ($-656) | 3.04 | 2.59 | 3.88 |  |
| OKLO | OKLO | ✗ | 8 | 50 | 4.96 | 19.7 | -9.78 | -14.76 | 2.01 | 7.2 | 1.54 (4) | $744 ($372) | 19.47 | 17.98 | 22.87 |  |

## Today's swing signals (passing names that closed below the lower band)
- None today.

## Passing swing names (top 20 by total backtest edge)
| Ticker | Company | Pass | Trades | Win % | Avg % | Avg win % | Avg loss % | Worst % | PF | Days | Last 6m PF (n) | $/trade (after tax) | Close | Lower band | 20-day avg | Signal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NRG | NRG Energy | ✓ | 9 | 89 | 6.42 | 8.38 | -9.21 | -9.21 | 7.27 | 5.6 | 99.00 (5) | $963 ($482) | 91.94 | 83.31 | 93.27 |  |
| PSN | Parsons Corporation | ✓ | 9 | 78 | 5.17 | 8.75 | -7.33 | -7.39 | 4.18 | 8.7 | 99.00 (3) | $776 ($388) | 53.26 | 48.62 | 51.04 |  |
| CDNS | Cadence Design Systems | ✓ | 8 | 88 | 4.04 | 5.7 | -7.61 | -7.61 | 5.25 | 6.9 | 99.00 (3) | $606 ($303) | 294.89 | 284.75 | 317.14 |  |
| GEHC | GE HealthCare | ✓ | 8 | 75 | 2.57 | 4.63 | -3.6 | -4.68 | 3.86 | 7.1 | 2.67 (4) | $386 ($193) | 83.33 | 77.28 | 81.92 |  |
| WELL | Welltower | ✓ | 8 | 75 | 2.02 | 3.86 | -3.51 | -4.61 | 3.3 | 7.1 | 2.42 (5) | $303 ($152) | 246.18 | 235.18 | 243.58 |  |
| VTR | Ventas | ✓ | 8 | 75 | 1.61 | 3.56 | -4.25 | -4.66 | 2.52 | 6.1 | 1.71 (5) | $242 ($121) | 87.36 | 84.44 | 87.91 |  |
| CCI | Crown Castle | ✓ | 10 | 60 | 1.19 | 5.98 | -5.99 | -6.99 | 1.5 | 5.2 | 1.00 (5) | $178 ($89) | 83.63 | 80.2 | 86.95 |  |
| ALLY | Ally Financial | ✓ | 11 | 73 | 1.08 | 3.88 | -6.41 | -7.31 | 1.62 | 6.0 | 1.68 (4) | $162 ($81) | 38.46 | 36.52 | 38.06 |  |
| SRE | Sempra | ✓ | 13 | 69 | 0.9 | 2.76 | -3.28 | -5.14 | 1.89 | 5.8 | 1.41 (8) | $135 ($68) | 79.09 | 73.39 | 79.98 |  |
| GNTX | Gentex | ✓ | 8 | 62 | 1.2 | 4.65 | -4.54 | -5.25 | 1.7 | 5.6 | 1.74 (5) | $180 ($90) | 19.66 | 18.51 | 19.62 |  |
| SYF | Synchrony Financial | ✓ | 8 | 62 | 1.1 | 4.96 | -5.33 | -5.67 | 1.55 | 7.6 | 1.47 (3) | $165 ($82) | 68.73 | 66.21 | 72.09 |  |

Screened 472 swingy names (liquid, ≥$10, median 5-day range ≥ 4%, 3-month move within ±20%, crosses its 20-day average often; no tracked names or semiconductors); 11 pass.
