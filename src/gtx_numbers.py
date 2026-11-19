import pandas as pd
import yfinance as yf

# ---------------------------------------------
# 1. Get the data
# ---------------------------------------------
folder = "/Users/santharhtut/Desktop/Finance Projects/lbo-valuation-project/data/"
inc = pd.read_csv(folder + "gtx_income_statement.csv", index_col=0)
bal = pd.read_csv(folder + "gtx_balance_sheet.csv", index_col=0)
cf  = pd.read_csv(folder + "gtx_cash_flow.csv", index_col=0)
info = yf.Ticker("GTX").info

# ---------------------------------------------
# 2. The key numbers
#    Everything is in $ millions from here on,
#    so we never have to mix units.
# ---------------------------------------------
M = 1_000_000

price  = info.get("currentPrice")                  # $ per share
shares = info.get("sharesOutstanding") / M         # millions of shares
debt   = bal.loc["Total Debt"].iloc[0] / M
cash   = bal.loc["Cash Cash Equivalents And Short Term Investments"].iloc[0] / M
ebitda = inc.loc["EBITDA"].iloc[0] / M

# Quick look at the last 4 years (for later)
rows = ["Total Revenue", "EBITDA", "Interest Expense", "Tax Provision"]
history = (inc.reindex(rows).iloc[:, :4] / M).round(0)

# ---------------------------------------------
# 3. What GTX is worth today (no premium yet)
# ---------------------------------------------
market_cap = price * shares
net_debt   = debt - cash
ev_today   = market_cap + net_debt

summary = pd.DataFrame({
    "GTX today ($M)": {
        "Market cap":      market_cap,
        "Debt":            debt,
        "Cash":            cash,
        "Net debt":        net_debt,
        "EV":              ev_today,
        "EBITDA":          ebitda,
        "EV / EBITDA":     ev_today / ebitda,
    }
}).round(2)

# ---------------------------------------------
# 4. What we would actually pay
# ---------------------------------------------
premium     = 0.30                       # we pay 30% above market price
offer_price = price * (1 + premium)
buy_shares  = offer_price * shares       # cost of buying all the shares

entry_ev       = buy_shares + net_debt
entry_multiple = entry_ev / ebitda

# ---------------------------------------------
# 5. USES: how much money do we need?
# ---------------------------------------------
fees       = 0.02 * entry_ev             # 2% deal costs
total_uses = buy_shares + debt + fees    # shares + pay off old debt + fees

uses = pd.DataFrame({
    "$M": {
        "Buy shares":         buy_shares,
        "Pay off old debt":   debt,
        "Fees":               fees,
        "Total Uses":         total_uses,
    }
}).round(2)

# ---------------------------------------------
# 6. SOURCES: where does the money come from?
# ---------------------------------------------
leverage  = 5                            # new debt = 5x EBITDA
cash_used = 100                          # $M of GTX's own cash we use

new_debt       = leverage * ebitda
sponsor_equity = total_uses - new_debt - cash_used     # whatever is left
total_sources  = new_debt + cash_used + sponsor_equity

sources = pd.DataFrame({
    "$M": {
        "New debt":          new_debt,
        "GTX cash used":     cash_used,
        "Sponsor equity":    sponsor_equity,
        "Total Sources":     total_sources,
    }
}).round(2)

# ---------------------------------------------
# 7. Quick checks
# ---------------------------------------------
print("Entry multiple:", round(entry_multiple, 2))
print("Sources equal Uses:", abs(total_sources - total_uses) < 0.01)
print("Sponsor equity is", round(sponsor_equity / total_uses * 100, 1), "% of Uses")

# ---------------------------------------------
# 8. History ratios (to help us choose assumptions)
# ---------------------------------------------
rows = ["Total Revenue", "EBITDA", "Pretax Income", "Tax Provision", "Interest Expense"]
hist = (inc.reindex(rows).iloc[:, :4] / M).T.iloc[::-1]      # oldest year first

hist["Capex"] = -cf.loc["Capital Expenditure"] / M            # make it positive
hist["Debt"]  = bal.loc["Total Debt"] / M

hist["Revenue growth"] = hist["Total Revenue"].pct_change()
hist["EBITDA margin"]  = hist["EBITDA"] / hist["Total Revenue"]
hist["Capex % rev"]    = hist["Capex"] / hist["Total Revenue"]
hist["Tax rate"]       = hist["Tax Provision"] / hist["Pretax Income"]
hist["Interest rate"]  = hist["Interest Expense"] / hist["Debt"]

ratios = hist[["Revenue growth", "EBITDA margin", "Capex % rev",
               "Tax rate", "Interest rate"]].round(3)

# ---------------------------------------------
# 9. Assumptions (change these any time)
# ---------------------------------------------
growth        = 0.02     # revenue growth per year
ebitda_margin = 0.165    # EBITDA as % of revenue
da_pct        = 0.028    # depreciation & amortization, % of revenue
capex_pct     = 0.023    # capex, % of revenue
tax_rate      = 0.21
interest_rate = 0.09     # on the NEW debt

# ---------------------------------------------
# 10. Project Year 1 to 5
# ---------------------------------------------
revenue    = inc.loc["Total Revenue"].iloc[0] / M    # last year's revenue
debt_start = new_debt                                # debt at the start of Year 1

proj_rows = []
for year in range(1, 6):
    revenue    = revenue * (1 + growth)
    ebitda_t   = revenue * ebitda_margin
    interest   = debt_start * interest_rate          # on last year's closing debt
    da         = revenue * da_pct
    tax        = max(0, tax_rate * (ebitda_t - da - interest))
    capex      = revenue * capex_pct
    fcf        = ebitda_t - interest - tax - capex   # cash left to repay debt
    debt_end   = debt_start - fcf

    proj_rows.append({
        "Year": year,
        "Revenue": revenue,
        "EBITDA": ebitda_t,
        "Interest": interest,
        "Tax": tax,
        "Capex": capex,
        "FCF": fcf,
        "Debt (end)": debt_end,
        "Coverage (x)": ebitda_t / interest,
    })
    debt_start = debt_end                            # next year starts here

projection = pd.DataFrame(proj_rows).set_index("Year").round(1)

# ---------------------------------------------
# 11. Exit (end of Year 5) and returns
# ---------------------------------------------
exit_multiple = entry_multiple             # assume we sell at the same multiple we paid
cash_left = cash - cash_used

exit_ebitda = projection.loc[5, "EBITDA"]
exit_debt   = projection.loc[5, "Debt (end)"]

exit_ev     = exit_ebitda * exit_multiple
exit_equity = exit_ev - exit_debt + cash_left

moic = exit_equity / sponsor_equity
irr  = moic ** (1 / 5) - 1

print("Exit EV:", round(exit_ev, 1))
print("Exit equity:", round(exit_equity, 1))
print("MOIC:", round(moic, 2))
print("IRR:", round(irr * 100, 1), "%")

# ---------------------------------------------
# 12. The whole model in one box
# ---------------------------------------------
def run_lbo(premium=0.30, leverage=5, exit_multiple=None, growth=0.02,
            cash_used=100, interest_rate=0.09):

    # Day 0: what we pay and how we fund it
    buy_shares = price * (1 + premium) * shares
    entry_ev   = buy_shares + net_debt
    entry_mult = entry_ev / ebitda
    total_uses = buy_shares + debt + 0.02 * entry_ev
    new_debt   = leverage * ebitda
    sponsor_eq = total_uses - new_debt - cash_used

    if exit_multiple is None:
        exit_multiple = entry_mult          # sell at the same multiple we paid

    # Years 1 to 5
    revenue  = inc.loc["Total Revenue"].iloc[0] / M
    debt_now = new_debt
    for year in range(5):
        revenue  = revenue * (1 + growth)
        ebitda_t = revenue * ebitda_margin
        interest = debt_now * interest_rate
        tax      = max(0, tax_rate * (ebitda_t - revenue * da_pct - interest))
        fcf      = ebitda_t - interest - tax - revenue * capex_pct
        debt_now = debt_now - fcf

    # Exit
    exit_equity = ebitda_t * exit_multiple - debt_now + (cash - cash_used)
    if exit_equity <= 0:
        return -1.0                          # we lost everything
    moic = exit_equity / sponsor_eq
    return moic ** (1 / 5) - 1

print("Check, IRR (%):", round(run_lbo() * 100, 1))   # should match the IRR above

# ---------------------------------------------
# 13. Sensitivity: premium x exit multiple (IRR in %)
# ---------------------------------------------
premiums       = [0.0, 0.1, 0.2, 0.3, 0.4]
exit_multiples = [8, 9, 10, 11, 12]

sens = pd.DataFrame(index=premiums, columns=exit_multiples, dtype=float)
for p in premiums:
    for m in exit_multiples:
        sens.loc[p, m] = run_lbo(premium=p, exit_multiple=m) * 100

sens = sens.round(1)