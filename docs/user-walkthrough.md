# User Walkthrough

**Momentum Portfolio Tool — Step-by-Step Guide**
*Last updated: May 2026*

---

## Overview

This tool helps you build and rebalance a momentum-based equity portfolio from the NIFTY 500 universe. You run it once a month, get a ranked list of 15 stocks, and receive exact instructions on what to buy, hold, and sell compared to last month.

**Time required per month:** 5-10 minutes (after the initial 2-minute data load)
**Access:** pick-momentum.streamlit.app (free, no login required)

---

## The Three Tabs

When you open the app, you will see three tabs at the top:

- **Portfolio Tool** - This is where you run the strategy. Start here every month.
- **Strategy Guide** - Detailed explanations of all four strategies with research backing.
- **How to Use** - This walkthrough, embedded in the app.

---

## First-Time Setup (One-time)

### Step 1: Choose a Strategy

At the top of the Portfolio Tool tab, you will see four strategy cards:

| Card | Signal | Best for |
|------|--------|----------|
| Classic Momentum | 12-1 raw return | Aggressive investors |
| Risk-Adjusted Momentum | Return / volatility | Most investors (start here) |
| Dual Momentum | Relative + absolute filter | Capital-preservation focus |
| 52-Week High Momentum | Nearness to 52W high | Breakout-focused investors |

**Recommendation for first-time users:** Select **Risk-Adjusted Momentum**. Click the green "Select" button on that card.

Click "About: [Strategy Name]" to expand a detailed research explanation before committing to a strategy.

---

### Step 2: Check the Market Regime

The Market Regime panel loads automatically. It shows Nifty 50 vs its 200-day SMA:

- **Green - UPTREND:** Nifty 50 is above its 200-day SMA. Good conditions. Proceed with full capital.
- **Red - DOWNTREND:** Nifty 50 is below its 200-day SMA. Consider deploying 50% of intended capital, or wait for conditions to improve.
- **Red + CASH SIGNAL (Dual Momentum only):** Nifty 50's own 12-month return is negative. Do not deploy. Move existing capital to liquid funds.

You can expand the panel to see a full Nifty 50 chart with the 50-day and 200-day SMA lines plotted.

---

### Step 3: Enter Your Capital

In the "Run Strategy" section, enter your total investment amount in rupees. This is the total you want spread across all 15 stocks.

**Example:** Rs 5,00,000 total gives each stock approximately Rs 33,333 (equal weight) or proportionally more/less (return-weighted, depending on the strategy).

---

### Step 4: Click Run Strategy

The app will:
1. Fetch the latest NIFTY 500 constituent list from NSE India (~5 seconds)
2. Download 15 months of price history for all 500 stocks (~1-2 minutes on the first run)
3. Calculate momentum scores and apply all strategy-specific filters
4. Build your 15-stock portfolio

Progress is shown with a progress bar. After the first run, data is cached for 1 hour - re-running within the same hour is near-instant.

---

### Step 5: Review and Act on Results

After the run completes, you will see:

- **Rebalancing Actions panel** - On your first run, all 15 stocks are labelled NEW: buy all of them.
- **Full results table** - All 15 stocks with scores, allocations, and share counts.
- **Charts** - Score bar, allocation donut, return vs volatility scatter, and sector breakdown.

Review these before placing any orders. Check the sector breakdown for concentration.

---

### Step 6: Save Your Run

At the bottom of the results, click **"Save Run & Download History"**. This downloads a file named `momentum_history.json` to your device.

**Keep this file.** Upload it at the start of next month to get:
- Rebalancing actions (NEW / HOLD / EXIT) vs this month's selections
- Performance of this month's portfolio vs Nifty 50

---

## Monthly Workflow (Ongoing)

Repeat this on the **last trading day of each month, after market close** (after 3:30 PM IST). Running after close ensures price data reflects the full day's move.

---

### Step 1: Upload Last Month's History

In the Portfolio History section at the top of the Portfolio Tool tab, click "Browse files" and upload your `momentum_history.json` from last month.

---

### Step 2: Check the Market Regime

Has the overall trend changed since last month? A regime change from green to red is meaningful - consider reducing your capital deployment until conditions stabilise.

---

### Step 3: Run the Strategy

Use the same strategy as last month for consistency. Enter the same capital amount (or adjust if you have added or withdrawn funds). Click Run Strategy.

---

### Step 4: Review Last Portfolio Performance

A new section appears showing how last month's 15 stocks have performed since you ran the strategy:

- Individual stock returns (green = profit, red = loss)
- Total portfolio return
- Nifty 50 benchmark return over the same period
- Alpha (portfolio return minus Nifty return)

This tells you whether the strategy has been generating value above the index. Track this over 6-12 months to assess strategy fit.

---

### Step 5: Review Rebalancing Actions

This is the most important section for ongoing use:

| Label | Meaning | Action to take |
|-------|---------|----------------|
| **NEW** | Not in last month's portfolio | Buy at market open on the first trading day of the new month |
| **HOLD** | Was in last month's portfolio and remains in top 15 | Do nothing - keep your existing position |
| **EXIT** | Was in last month's portfolio but has dropped out of top 15 | Sell at market open on the first trading day of the new month |

A typical monthly rebalancing involves 3-6 changes (exits + new entries). In stable trending markets, turnover is lower. In choppy or transitioning markets, turnover can be higher.

---

### Step 6: Place Orders

- Execute all BUY and SELL orders at **market open on the first trading day of the new month**
- For NSE: place CNC (Cash and Carry) orders for equity delivery
- Use limit orders near the last closing price to avoid excessive slippage, especially for mid-cap stocks
- If your total capital is above Rs 25 lakhs, stagger execution over 30-60 minutes at open to reduce market impact

---

### Step 7: Save and Replace Your History File

After running the strategy, click "Save Run & Download History" and save the new `momentum_history.json`. This file now contains both last month's and this month's data. Replace the old version with the new one.

---

## Understanding the Results Table

| Column | What it means | How to use it |
|--------|---------------|---------------|
| **#** | Rank by strategy score (1 = strongest signal) | Stock #1 has the highest momentum |
| **Action** | NEW / HOLD / EXIT | Your rebalancing instruction |
| **Symbol** | NSE ticker symbol | Use this in your brokerage platform |
| **Company** | Full company name | Cross-reference with your broker to confirm |
| **Sector** | Industry sector | Check for sector concentration across all 15 |
| **12-1 Return** | 11-month return (excluding the most recent month) | Core momentum signal - higher means stronger trend |
| **12M Return** | Full 12-month return | Compare to 12-1 to see the last-month effect |
| **Ann. Vol** | Annualised daily return volatility | Lower = smoother trend, higher = noisier signal |
| **Risk-Adj Score** | 12-1 Return / Annualised Volatility | Primary ranking metric for Risk-Adjusted strategy |
| **vs 52W High** | How far below the 52-week high (%) | Near 0% means the stock is near a breakout level |
| **Weight** | % of capital allocated | Return-weighted strategies vary this across stocks |
| **Allocated (Rs)** | Rupee amount to invest in this stock | Your target position size |
| **Shares** | Whole shares to buy (rounded down) | Calculated at time of run - verify before ordering |
| **CMP (Rs)** | Current market price at time of run | Verify on your broker platform before ordering |

**Note on share counts:** The share count is based on the price at the time the strategy was run. By the time you place orders the following morning, the price will have changed. Recalculate if needed: `Shares = Floor(Allocated / Actual Price)`.

---

## Understanding the Charts

### Score Bar Chart

A horizontal bar chart showing each stock's momentum score. Green bars = high score, yellow = moderate. All 15 bars will be positive (negative-score stocks are filtered out before selection).

Use this to assess signal concentration: a wide spread between the #1 and #15 bar means strong differentiation. A narrow spread means the top 15 stocks are bunched together - weaker overall conviction.

---

### Capital Allocation Donut

Shows how your total capital is distributed across the 15 stocks. For return-weighted strategies (Risk-Adjusted Momentum), you will see unequal slices - top-ranked stocks receive larger allocations. For equal-weight strategies (Classic, Dual, 52-Week High), all slices are the same size.

---

### Return vs Volatility Scatter

Each bubble represents one stock. The X-axis shows annualised volatility, the Y-axis shows 12-1 return. Bubble size reflects capital allocation.

- **Top-left quadrant:** High return, low volatility. These are the highest-quality momentum names.
- **Bottom-right quadrant:** Low return, high volatility. These are automatically filtered out in Risk-Adjusted and Dual Momentum strategies.
- **Large bubbles in the top-left:** Your highest-conviction positions.

---

### Sector Allocation Bar

Shows total capital allocated per GICS sector. Use this to identify concentration risk. If 5 or more of your 15 stocks are from the same sector, your portfolio has a significant sector tilt - you are taking both a momentum bet and a sector bet simultaneously.

Sector concentration is not necessarily bad (sectors can trend strongly for months), but it is important to be aware of. If the entire portfolio is in one sector, a sector-specific negative event affects all 15 positions at once.

---

## Portfolio History Management

### What is the history file?

`momentum_history.json` stores every run you have saved - the date, strategy used, Nifty 50 price, and all 15 selected stocks with their prices, scores, and allocations. This file lives entirely on your device. No data is transmitted to or stored on any server.

### How to manage the file

- **Save after every run** - Do not skip this step. Without a saved run, next month you will have no baseline for NEW/HOLD/EXIT labels or performance tracking.
- **Keep only the latest version** - The file accumulates all past runs. You do not need separate files per month.
- **Back it up** - Save a copy to Google Drive, Dropbox, or email it to yourself monthly. If the file is lost, you lose your entire rebalancing history.
- **One file per strategy** - If you run multiple strategies with separate capital pools, rename the files descriptively: `momentum_history_risk_adjusted.json`, `momentum_history_dual.json`, etc.

### What happens if I lose the file?

The app still works. You will be able to run the strategy and get a portfolio. You just will not see NEW/HOLD/EXIT labels (all stocks will show as NEW) and you will not see last-run performance until you have completed two saved runs.

---

## Common Questions

**Q: The data says "possibly delisted" for some stocks. Is this a problem?**

A small number of stocks in the NIFTY 500 constituent list may have had symbol changes, delistings, or temporary data issues on Yahoo Finance. These are automatically skipped. The final portfolio of 15 is drawn entirely from stocks with clean, complete data. No action required on your part.

---

**Q: My expected stocks are not appearing. Did the market cap filter remove them?**

Market cap data from the data source can occasionally be missing or stale. Stocks with no market cap data are kept in the universe (benefit of the doubt - they are already in NIFTY 500). Stocks with market cap data showing below Rs 500 Cr are filtered as a liquidity protection measure. This filter does not affect ranking - it only removes stocks from the eligible universe before ranking begins.

---

**Q: A stock I held last month is labelled EXIT but it still seems to be performing well.**

EXIT means the stock's momentum score dropped it out of the top 15 relative to peers - not that it has performed badly in absolute terms. Its score may have declined because other stocks accelerated faster, or because its own momentum faded slightly. For consistent, backtestable results, follow the signal and exit as instructed. Overriding exit signals is one of the most common ways to underperform a mechanical strategy.

---

**Q: Should I invest all capital at once or spread purchases over several days?**

The strategy is designed for full deployment at each monthly rebalancing, executed at market open on the first trading day of the month. Spreading purchases over multiple days introduces timing inconsistency and partially defeats the monthly signal. Place all orders on rebalancing day.

---

**Q: What if the NSE constituent list fails to load?**

NSE India's servers occasionally block or throttle automated requests. If you see a loading error: (a) wait 5-10 minutes and try again, or (b) download the NIFTY 500 constituent CSV manually from nseindia.com and upload it using the manual upload option in the app.

---

**Q: Can I run this strategy on a weekly or bi-weekly basis instead of monthly?**

The strategies are calibrated for monthly holding periods. The academic evidence supporting momentum signals uses monthly formation and holding periods. Running more frequently increases transaction costs (brokerage, STT, stamp duty) without a corresponding improvement in signal quality. Monthly is the intended and optimal cadence.

---

**Q: The Dual Momentum strategy is showing a CASH signal. What should I do?**

When the Dual Momentum cash signal is active (Nifty 50's 12-month return is negative), the strategy instructs you not to be invested in equities. If you have existing positions, exit them at the next rebalancing. Move the freed capital to a liquid fund or short-duration debt fund. Re-enter equities only when the signal flips back to positive - when Nifty 50's 12-month return turns positive.

Staying disciplined during the cash phase is difficult psychologically, especially if markets appear to be recovering. Stick to the rule. The cash signal is the defining risk-management feature of Dual Momentum.

---

**Q: What does a negative alpha mean?**

Alpha is portfolio return minus Nifty 50 return over the same period. Negative alpha means the strategy underperformed the index for that month. Single-month alpha is noisy and largely meaningless. Evaluate alpha over a rolling 6-12 month window. Sustained negative alpha over 12 months is a signal to review your strategy choice or execution.

---

## Tips for Better Outcomes

**1. Run consistently on the same day each month**

Momentum signals are calibrated to monthly rebalancing. Drifting to bi-monthly or skipping months introduces timing drift and reduces the reliability of performance comparisons.

**2. Do not override signals**

If a stock is flagged EXIT, sell it. If a stock is NEW, buy it. The systematic advantage of a rules-based strategy is eliminated the moment you start making ad hoc overrides. Override bias is the primary source of underperformance vs the mechanical strategy in live implementations.

**3. Benchmark consistently against Nifty 50**

The app shows your alpha vs Nifty 50 after each run. This is your scorecard. Track it monthly. If you are generating consistently negative alpha over 6+ months, reconsider your strategy choice. If you are generating 0% alpha, check that you are executing rebalancing on the correct day and at the correct prices.

**4. Keep a trade log**

Note the actual buy and sell prices vs the tool's CMP at run time. Over 6-12 months, this reveals your average slippage and execution quality. High slippage (more than 0.5% per trade) suggests you should use limit orders rather than market orders.

**5. Size positions appropriately**

With Rs 5 lakh spread across 15 stocks, each position is approximately Rs 33,333. For stocks priced at Rs 2,000, that is 16 shares - reasonable. For stocks priced at Rs 500, that is 66 shares. For stocks priced at Rs 10,000, that is 3 shares. When a position drops below 3-4 shares, the rounding effect becomes significant and may cause actual allocation to deviate meaningfully from the target weight.

**6. Account for transaction costs in your return expectations**

Each monthly rebalancing with 4-6 stock changes involves 8-12 trades. Estimated round-trip cost per trade on NSE equity delivery: 0.25-0.35% (brokerage + STT + exchange charges + stamp duty). Over 12 months with 5 changes per month, total annual friction is approximately 1.5-2.5% of capital. Factor this into your return expectations when comparing to the Nifty 50 benchmark.

**7. Do not chase past strategy performance**

If you see that the 52-Week High strategy outperformed over the last 3 months, resist the urge to switch. Strategies rotate in and out of favour based on market regime. Choose a strategy based on your risk tolerance and investment objective, then stick with it through the regime cycles. Switching strategies after a period of underperformance locks in the loss and often means you switch just before the strategy recovers.

---

## Transaction Cost Reference

| Cost Component | Rate | Notes |
|----------------|------|-------|
| Brokerage (discount broker) | 0.01-0.05% | Flat fee brokers may charge Rs 20 per trade instead |
| STT (Securities Transaction Tax) | 0.1% on sell side | Delivery equity; mandatory |
| Exchange + SEBI charges | ~0.003% | Fixed, minimal |
| Stamp duty | 0.015% on buy side | State-mandated |
| Approximate round-trip total | 0.25-0.35% | Per stock bought and later sold |

For a Rs 5 lakh portfolio turning over 5 stocks per month (10 trades), monthly friction is approximately Rs 375-525. Annual: Rs 4,500-6,300, or roughly 1-1.3% of capital. This is a realistic drag to account for when evaluating strategy performance.

---

## Quick Reference Card

| Action | When | How |
|--------|------|-----|
| First run | Any time | Select strategy -> Enter capital -> Run -> Save history |
| Monthly rebalance | Last trading day of month, after 3:30 PM IST | Upload history -> Check regime -> Run -> Review actions -> Save history |
| Place orders | First trading day of new month, market open | Execute all NEW buys and EXIT sells |
| Review performance | Each monthly run | Check alpha vs Nifty in the performance section |
| Back up history | After each save | Copy momentum_history.json to cloud storage |
