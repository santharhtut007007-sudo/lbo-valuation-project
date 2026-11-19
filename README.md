# Garrett Motion (GTX): Leveraged Buyout Model

A simplified take-private LBO of Garrett Motion Inc. (NASDAQ: GTX), built in Python and Excel. The model prices the deal, builds Sources & Uses, projects five years of cash flow and debt paydown, and solves for sponsor IRR and MOIC. Sensitivity tables show which assumptions drive the return.

**Result:** at a 30% premium (10.7x EV/EBITDA) and 5.0x leverage, the base case returns **7.8% IRR / 1.45x MOIC** over five years, well below a typical 20% sponsor hurdle.

## Transaction summary

$ in millions, except per share data. Market data as of November 2026 (share price approx. $21.52, via yfinance); financials from FY2025 statements.

| Entry valuation | |
|---|---|
| Offer price per share (30% premium) | $27.98 |
| Equity purchase price | 5,164.5 |
| Net debt | 1,292.0 |
| Entry enterprise value | 6,456.5 |
| Entry EV / EBITDA | 10.7x |
| Current EV / EBITDA | 8.7x |

| Uses | $M | Sources | $M |
|---|---|---|---|
| Purchase of equity | 5,164.5 | New debt (5.0x EBITDA) | 3,010.0 |
| Refinance existing debt | 1,469.0 | Balance sheet cash | 100.0 |
| Transaction fees (2% of EV) | 129.1 | Sponsor equity | 3,652.7 |
| **Total uses** | **6,762.7** | **Total sources** | **6,762.7** |

Sponsor equity is 54% of total capitalization.

## Key assumptions

| Assumption | Value | Basis |
|---|---|---|
| Offer premium | 30% | Assumption |
| Leverage (new debt / EBITDA) | 5.0x | Assumption |
| Interest rate on new debt | 9.0% | Historical range 7.6% - 10.5% |
| Revenue growth | 2.0% | Assumption (cyclical business) |
| EBITDA margin | 16.5% | FY2022-25: 15.4% - 17.1% |
| D&A / capex (% of revenue) | 2.8% / 2.3% | FY2025 / FY2022-25 range |
| Tax rate | 21.0% | FY2022-25: 17.8% - 24.8% |
| Exit multiple | 10.7x | Equal to entry multiple |
| Holding period | 5 years | |

## Results

| | Year 0 | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---|---|---|---|---|---|
| EBITDA | 602.0 | 603.2 | 615.3 | 627.6 | 640.1 | 652.9 |
| Free cash flow | | 199.9 | 222.4 | 246.7 | 272.8 | 301.0 |
| Debt, ending | 3,010.0 | 2,810.1 | 2,587.7 | 2,341.0 | 2,068.2 | 1,767.2 |
| EBITDA / interest | | 2.2x | 2.4x | 2.7x | 3.0x | 3.5x |

| Exit (Year 5) | $M |
|---|---|
| Exit enterprise value (10.7x) | 7,002.5 |
| Less: debt | (1,767.2) |
| Plus: cash | 77.0 |
| Exit equity value | 5,312.4 |
| Sponsor equity invested | 3,652.7 |
| **MOIC** | **1.45x** |
| **IRR** | **7.8%** |

### Value creation bridge

| Source | $M | % of gross |
|---|---|---|
| EBITDA growth | 546.0 | 30.5% |
| Multiple expansion | 0.0 | 0.0% |
| Debt paydown | 1,242.8 | 69.5% |
| Transaction fees | (129.1) | |
| **Total value created** | **1,659.7** | |

Roughly 70% of the gross gain comes from paying down debt with operating cash flow. With a flat multiple and 2% growth, little else drives the return.

## Sensitivity analysis

**IRR by offer premium and exit EV / EBITDA**

| Premium | 8.0x | 9.0x | 10.0x | 11.0x | 12.0x |
|---|---|---|---|---|---|
| 0% | 7.7% | 11.4% | 14.7% | 17.6% | 20.3% |
| 10% | 4.4% | 8.1% | 11.2% | 14.1% | 16.7% |
| 20% | 1.7% | 5.2% | 8.3% | 11.1% | 13.6% |
| 30% | (0.7%) | 2.8% | 5.8% | 8.5% | 11.0% |
| 40% | (2.7%) | 0.6% | 3.6% | 6.2% | 8.7% |

**IRR by leverage and revenue growth**

| Debt / EBITDA | 0% | 2% | 4% | 6% | Year 1 EBITDA / interest |
|---|---|---|---|---|---|
| 4.0x | 4.7% | 7.7% | 10.5% | 13.3% | 2.8x |
| 5.0x | 4.3% | 7.8% | 11.1% | 14.2% | 2.2x |
| 6.0x | 3.7% | 7.9% | 11.8% | 15.4% | 1.9x |
| 7.0x | 2.8% | 8.1% | 12.8% | 17.1% | 1.6x |

## Conclusion

At a 30% premium and 10.7x entry, the deal does not clear a 20% hurdle. Only a zero-premium purchase with a 12.0x exit reaches it, which is not a realistic take-private.

**Price matters more than structure.** The market values GTX at 8.7x EBITDA today, so a 30% premium builds in 2.0x of multiple that the exit has to recover.

**Leverage barely helps.** Going from 4.0x to 7.0x debt moves the 2% growth IRR from 7.7% to 8.1%, while Year 1 interest cover falls from 2.8x to 1.6x. At a 9.0% cost of debt, the extra leverage adds risk without adding much return.

**Growth is the real lever.** At 5.0x leverage, 6% revenue growth lifts IRR to about 14%, still short of 20%.

## Limitations

Single debt tranche, with all free cash flow applied to repayment; no mandatory amortization schedule, revolver or minimum cash balance.

Interest is calculated on beginning-of-year debt, so there is no circularity.

No dividends, management rollover, option pool or financing fee amortization.

Constant EBITDA margin, D&A and capex ratios across the projection.

Market data is a point-in-time snapshot and will differ on re-run.

## Repository contents

| Path | Description |
|---|---|
| `src/gtx_numbers.py` | Python model: data pull, Sources & Uses, projection, returns, sensitivities |
| `model/GTX_LBO_Model.xlsx` | Excel model with live formulas (Assumptions, Sources & Uses, Projection, Returns, Sensitivity) |
| `data/` | GTX income statement, balance sheet and cash flow statement (CSV) |

The Excel model includes built-in checks (sources equal uses, IRR cross-check, value bridge reconciliation) and ties to the Python output.
