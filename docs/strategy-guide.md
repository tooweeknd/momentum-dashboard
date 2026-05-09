# Momentum Strategy Guide

**Momentum Portfolio Tool — Strategy Reference**
*Last updated: May 2026*

---

## Table of Contents

1. [What Is Momentum Investing?](#what-is-momentum-investing)
2. [Strategy 1: Classic Momentum](#strategy-1-classic-momentum)
3. [Strategy 2: Risk-Adjusted Momentum](#strategy-2-risk-adjusted-momentum)
4. [Strategy 3: Dual Momentum](#strategy-3-dual-momentum)
5. [Strategy 4: 52-Week High Momentum](#strategy-4-52-week-high-momentum)
6. [Strategy Comparison Table](#strategy-comparison-table)
7. [Which Strategy Suits You?](#which-strategy-suits-you)
8. [Momentum Investing in Indian Markets](#momentum-investing-in-indian-markets)
9. [Risk Warnings](#risk-warnings)
10. [Glossary](#glossary)

---

## What Is Momentum Investing?

Momentum investing is the practice of buying assets that have recently performed well and selling (or avoiding) assets that have recently performed poorly — based on the empirically observed tendency for recent price trends to continue over the near- to medium-term.

It is not trend-following based on gut feel. It is a systematic, rules-based approach backed by decades of academic research across global markets. Momentum is widely considered one of the most robust return anomalies in finance — it has been replicated in over 40 countries and across asset classes including equities, bonds, commodities, and currencies.

The core intuition: markets are not instantaneously efficient. Information diffuses gradually, investor psychology causes herding and under-reaction, and institutional constraints create persistent price trends.

---

## Strategy 1: Classic Momentum

### Core Thesis (Plain English)

Stocks that have gone up the most over the past 6–12 months tend to continue going up over the next 1–6 months. Stocks that have fallen the most tend to continue falling. This is not a coincidence — it is a repeatable pattern driven by how investors process new information: slowly, with cognitive biases, and subject to institutional momentum.

Buy the recent winners. Avoid or short the recent losers. Rebalance monthly.

---

### Academic Foundation

**Primary Paper:** Jegadeesh, N., & Titman, S. (1993). *Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency.* The Journal of Finance, 48(1), 65–91.

**Key Findings:**
- Studied NYSE and AMEX stocks from 1965–1989 (over 24 years of data).
- A strategy of buying the top decile of 6-month past returners and shorting the bottom decile earned **approximately 1% per month** (roughly 12% annualised) over the subsequent 6 months.
- Returns were robust across multiple formation and holding period combinations (3–12 months formation, 3–12 months holding).
- The effect was not explained by risk (beta) or firm size alone.
- The authors explicitly showed that the returns are **not** due to common risk factors known at the time.

**Follow-up Paper:** Jegadeesh, N., & Titman, S. (2001). *Profitability of Momentum Strategies: An Evaluation of Alternative Explanations.* The Journal of Finance, 56(2), 699–720.
- Confirmed that momentum profits continued in the 1990s (out-of-sample period), ruling out data mining.
- Momentum returns were approximately **1.39% per month** in the post-1993 period.

**Supporting Evidence:**
- Fama, E.F., & French, K.R. (1996). *Multifactor Explanations of Asset Pricing Anomalies.* Journal of Finance, 51(1). Fama and French acknowledged momentum is a persistent anomaly their 3-factor model cannot explain.
- Carhart, M.M. (1997). *On Persistence in Mutual Fund Performance.* Journal of Finance, 52(1). Added momentum as a 4th systematic factor (WML — Winners Minus Losers) to the Fama-French model.
- Asness, C.S., Moskowitz, T.J., & Pedersen, L.H. (2013). *Value and Momentum Everywhere.* Journal of Finance, 68(3). Demonstrated momentum across 8 diverse markets and 4 asset classes simultaneously, with Sharpe ratios exceeding 0.5 for most implementations.

---

### Signal Construction

The Classic Momentum score is the total return of a stock over a **lookback window**, typically **12 months excluding the most recent 1 month** (the skip-month adjustment).

```
Momentum Score = Price(t-1) / Price(t-12) - 1
```

Where:
- `t` = current month
- `t-1` = one month ago (skip month — avoids short-term reversal contamination)
- `t-12` = twelve months ago

**Why skip the most recent month?** Research by Jegadeesh (1990) and Lehmann (1990) demonstrated that stocks exhibit short-term reversal at the 1-month horizon. Including the most recent month's return in the lookback injects mean-reversion noise into the signal. Excluding it isolates the genuine intermediate-horizon momentum.

**Ranking and Portfolio Construction:**
1. Compute momentum score for all eligible stocks.
2. Rank all stocks from highest to lowest score.
3. Select the top N stocks (e.g., top 10, top 20, or top decile).
4. Weight equally or by signal strength (rank-weighted or score-weighted).
5. Rebalance monthly.

**In this tool:** Momentum Score = (Price today / Price 12 months ago) - 1, with the 1-month skip applied where data permits.

---

### Historical Performance Evidence

| Metric | Global Average (Developed Markets) | India (NSE, 2005–2023) |
|---|---|---|
| Annualised Return (long-only) | ~15–18% | ~18–22% |
| Sharpe Ratio | ~0.5–0.8 | ~0.6–0.9 |
| Max Drawdown | -40% to -60% (crashes) | -45% to -55% |
| Monthly Hit Rate | ~55–60% | ~57–63% |

Indian market studies (Sehgal & Jain, 2011; Ansari & Khan, 2012) found momentum profits of 1.5–2% per month in the Nifty 500 universe, somewhat higher than US markets — consistent with less institutional efficiency and higher retail participation.

---

### Risk Profile and Drawdown Characteristics

**Classic Momentum is a high-return, high-risk strategy.** Its primary weakness is severe drawdown during momentum crashes.

**Momentum Crashes** (Daniel & Moskowitz, 2016, *Journal of Financial Economics*):
- Momentum crashes are large, rapid, and concentrated — they happen in a short window (1–3 months).
- They typically occur after a period of market panic followed by a sharp rebound.
- The worst performers (short leg of momentum) tend to recover fastest — crushing a short momentum portfolio.
- Between 1927–2013, momentum crashed more than -50% in several episodes (1932, 2001, 2009).
- In India: the 2008 crash saw Nifty 500 momentum portfolios draw down 55–65% from peak.

**Risk characteristics:**
- Beta: ~1.0–1.2 (moderate market sensitivity)
- Volatility: ~20–30% annualised
- Tail risk: Fat left tail (occasional -20% to -40% monthly loss in crashes)
- Correlation to market: moderate (~0.6–0.8)

---

### When It Works Best / When It Fails

**Works best when:**
- Markets are in a sustained trending phase (bull or bear, but consistent)
- Macro environment is stable with gradual information diffusion
- Earnings surprises are autocorrelated (good quarters follow good quarters)
- Sector rotation is in progress

**Fails when:**
- Markets reverse sharply and violently (V-shaped recoveries after crashes)
- High uncertainty: multiple regime changes in a short period
- Markets trade in a wide, directionless range
- Liquidity crises where prices detach from fundamentals
- January/April in India (FII flows, fiscal year-end rebalancing)

---

### Comparison Notes

Classic Momentum is the **benchmark** strategy. All others below attempt to improve upon it by managing specific weaknesses:
- **Risk-Adjusted Momentum** addresses the crash risk.
- **Dual Momentum** adds a safety switch to move to cash in bear markets.
- **52-Week High Momentum** uses a different, arguably more intuitive signal.

---

### Implementation in This Tool

- **Lookback period:** 12 months (configurable in settings)
- **Skip-month:** 1 month applied automatically
- **Universe:** Configurable (Nifty 50, Nifty 100, Nifty 500, custom)
- **Portfolio size:** Configurable (default: 10 stocks)
- **Weighting:** Equal weight (default) or rank-weighted
- **Rebalancing:** Monthly on a fixed date
- **Output columns:** Momentum Score, Rank, Signal (BUY/HOLD/EXIT)

---

## Strategy 2: Risk-Adjusted Momentum

### Core Thesis (Plain English)

Classic momentum gives every month equal weight in the signal, whether that month was volatile or calm. But a 5% gain during a stable period is informationally very different from a 5% gain during a market panic.

Risk-adjusted momentum scales the momentum signal down when volatility is high (signal is less reliable) and scales it up when volatility is low (signal is more reliable). The result: you carry less risk during turbulent markets and more during stable ones — which dramatically reduces crash exposure while preserving most of the upside.

---

### Academic Foundation

**Primary Paper (Scaling by Volatility):** Barroso, P., & Santa-Clara, P. (2015). *Momentum Has Its Moments.* Journal of Financial Economics, 116(1), 111–120.

**Key Findings:**
- Studied US momentum from 1927–2011.
- Standard momentum had a Sharpe Ratio of 0.53 but a maximum drawdown of -91.6%.
- Scaling momentum returns by the inverse of their past volatility reduced the maximum drawdown to -25.6% (a dramatic improvement).
- The volatility-scaled strategy had a Sharpe Ratio of **0.97** — nearly double the classic strategy.
- The key insight: momentum's own variance is predictable. High current variance predicts bad future momentum returns.
- The paper explicitly showed that momentum crashes are predictable: they happen when momentum variance (not market variance) is elevated.

**Supporting Paper:** Moreira, A., & Muir, T. (2017). *Volatility-Managed Portfolios.* Journal of Finance, 72(4), 1611–1644.

**Key Findings:**
- Extended the Barroso-Santa-Clara framework to all major factor portfolios (value, size, profitability, momentum).
- Showed that scaling ANY factor by its inverse realized variance produces economically and statistically significant improvements.
- For momentum specifically, the volatility-managed version produced **47 basis points per month additional alpha** over the raw momentum strategy.
- The improvement comes almost entirely from avoiding large drawdowns, not from better upside capture.
- Importantly, the gains are robust to different estimation windows (1 week to 6 months).

**Additional Reference:** Daniel, K., & Moskowitz, T.J. (2016). *Momentum Crashes.* Journal of Financial Economics, 122(2), 221–247.
- Provides the theoretical foundation explaining *why* volatility-scaling works: momentum has negative skewness that clusters when option-implied volatility is high.

---

### Signal Construction

**Step 1: Compute Classic Momentum Score**
```
Raw_Momentum(i) = Price(t-1) / Price(t-12) - 1
```

**Step 2: Compute Realized Volatility**
```
Realized_Vol(i) = Standard Deviation of daily returns over past 1 month × √252
```
(Annualised, using 21 trading days)

**Step 3: Scale the Signal**
```
Risk_Adjusted_Score(i) = Raw_Momentum(i) / Realized_Vol(i)
```

This is essentially a **risk-adjusted return** — how much return per unit of risk the stock delivered. A stock with 20% momentum and 15% volatility scores higher than a stock with 25% momentum but 40% volatility.

**Alternative: Target Volatility Scaling (Moreira & Muir approach)**

At the portfolio level, rather than scoring individual stocks, scale the portfolio's total exposure:

```
Position Size = (Target_Volatility / Realized_Portfolio_Vol) × Base_Position
```

Where `Target_Volatility` is typically 12% annualised (investor-defined). When realized vol exceeds target, reduce exposure. When realized vol is below target, increase toward fully invested.

**In this tool:** Individual-stock risk-adjusted scoring (Step 1–3 above) is used for ranking. The portfolio-level scaling from Moreira-Muir is optionally applied to size overall exposure.

---

### Historical Performance Evidence

| Metric | Classic Momentum | Risk-Adjusted Momentum |
|---|---|---|
| Annualised Return | ~15–18% | ~14–17% |
| Sharpe Ratio | ~0.53 | ~0.90–1.0 |
| Max Drawdown | ~-60% to -91% | ~-20% to -30% |
| Calmar Ratio (Return/MaxDD) | ~0.25 | ~0.60–0.80 |
| Monthly Skewness | -2.5 (very negative) | ~-0.5 (near normal) |

The trade-off: slightly lower raw return in exchange for dramatically better risk-adjusted returns and survivable drawdowns.

---

### Risk Profile and Drawdown Characteristics

Risk-adjusted momentum is **the most crash-resistant of the four strategies**. Its primary innovation is that volatility is itself a signal — and high volatility is a warning, not just a consequence.

**Why drawdowns are smaller:**
- High-volatility stocks (which crash hardest) get downweighted in the ranking.
- The strategy naturally reduces exposure to stocks during market stress (when all stocks show elevated vol).
- Crash episodes, which are characterized by massive volatility spikes, automatically cause the strategy to de-risk.

**Risk profile:**
- Beta: ~0.7–0.9 (lower than classic momentum)
- Volatility: ~15–20% annualised
- Tail risk: Substantially reduced
- Correlation to market: ~0.5–0.7

---

### When It Works Best / When It Fails

**Works best when:**
- Markets are transitioning between regimes (volatility is informative)
- Following a period of market stress (strategy is already de-risked, benefits from recovery)
- Long-term (5+ years), as the crash protection compounds significantly
- Used with a long-only constraint (no shorts available to retail investors)

**Fails when:**
- Volatility spikes on positive news (false signal — the strategy de-risks when it shouldn't)
- Low-volatility, slow-moving bear markets (the gradual decline does not trigger de-risking)
- Markets where volatility is structurally high for non-risk reasons (circuit breakers, thin liquidity)

---

### Comparison Notes

- Produces the best **Sharpe Ratio** of the four strategies.
- Drawdowns are comparable to Dual Momentum but without going fully to cash.
- More granular signal than Classic Momentum — differentiates between high-return/high-risk and high-return/low-risk stocks.
- More complex to compute than the others; requires daily return data for volatility estimation.

---

### Implementation in This Tool

- **Scoring:** `Momentum_Score / Realized_Volatility` (21-day rolling vol, annualised)
- **Ranking:** Stocks ranked by risk-adjusted score (highest = strongest signal)
- **Optional target-vol scaling:** Applied to overall portfolio size (default: off)
- **Data requirement:** Daily closing prices for past 12 months
- **Output columns:** Raw Score, Realized Vol (%), Risk-Adj Score, Rank, Signal

---

## Strategy 3: Dual Momentum

### Core Thesis (Plain English)

Gary Antonacci's Dual Momentum combines two distinct momentum ideas:

1. **Relative Momentum:** Among a set of assets, pick the ones doing best relative to each other (classic cross-sectional momentum).
2. **Absolute Momentum (Trend Following):** Even the best-performing asset should be avoided if it has a negative return over the past 12 months — which typically signals a broad bear market. In that case, move to cash (or short-term bonds).

The result: you stay invested in the best performers during bull markets, and you move entirely to safety during sustained bear markets. The cash signal is the key innovation — it gives Dual Momentum a "circuit breaker" that Classic Momentum lacks.

---

### Academic Foundation

**Primary Source:** Antonacci, G. (2014). *Dual Momentum Investing: An Innovative Strategy for Higher Returns with Lower Risk.* McGraw-Hill.

**Supporting Papers by Antonacci:**
- Antonacci, G. (2012). *Risk Premia Harvesting Through Dual Momentum.* Portfolio Management Consultants.
  - Tested from 1974–2012 across US stocks, international stocks, and bonds.
  - Dual Momentum produced **~17.4% annualised return** vs. 11.9% for buy-and-hold S&P 500.
  - Maximum drawdown of **-17.8%** vs. -50.9% for buy-and-hold.
  - Sharpe Ratio of ~1.0 vs. 0.4 for buy-and-hold.

**Academic Basis for Absolute Momentum:**
- Moskowitz, T.J., Ooi, Y.H., & Pedersen, L.H. (2012). *Time Series Momentum.* Journal of Financial Economics, 104(2), 228–250.
  - Studied 58 liquid instruments (equities, bonds, currencies, commodities) from 1985–2012.
  - Found significant positive returns to **time-series momentum** (absolute momentum): buying assets with positive past 12-month returns, selling those with negative returns.
  - Average excess return of **~1% per month** with Sharpe Ratios of 0.6–1.8 across instruments.
  - Crucially: time-series momentum is particularly strong after extreme market moves — it helps avoid bear markets.

**For Indian Market Context:**
- Sehgal, S., & Jain, S. (2011). *Short-Term Momentum Patterns in Stock and Sectoral Returns.* Journal of Advances in Management Research.
- Ansari, V.A., & Khan, S. (2012). *Momentum and Season Effects: Momentum Effect in Indian Stock Market.* VIKALPA.

---

### Signal Construction

Dual Momentum has two components evaluated monthly:

**Step 1: Absolute Momentum (Market Regime Filter)**
```
Nifty_12M_Return = Nifty_Price(today) / Nifty_Price(12_months_ago) - 1

If Nifty_12M_Return < 0:
    Signal = CASH (exit all equity positions, move to liquid fund/FD)
Else:
    Proceed to Step 2
```

**Why Nifty 12M return?** The 12-month return of the broad market is one of the simplest and most robust trend signals available. When it is negative, the market has entered a sustained downtrend — and the probability of further loss over the next 6 months is materially higher than normal.

**Step 2: Relative Momentum (Stock Selection)**
```
Momentum_Score(i) = Price(t-1) / Price(t-12) - 1   [with 1-month skip]

Rank all stocks by Momentum_Score.
Select top N stocks.
```

**Combined Logic:**
```
if Nifty_12M_Return < 0:
    Hold: 0% equities, 100% cash/liquid
else:
    Hold: Top N momentum stocks, equal weight
```

**Optional enhancement (Antonacci's original framework):**
- Use multiple asset classes: when equity momentum is negative, check if bonds have positive absolute momentum before going to cash.
- In Indian context: compare Nifty vs. liquid fund vs. gold ETF — go to whichever has positive 12M momentum.

---

### Historical Performance Evidence

| Metric | Buy & Hold Nifty | Classic Momentum | Dual Momentum |
|---|---|---|---|
| Annualised Return (India, est.) | ~12–14% | ~18–22% | ~16–20% |
| Max Drawdown | ~-55% | ~-50% | ~-20% to -30% |
| Sharpe Ratio | ~0.5 | ~0.6–0.9 | ~0.9–1.2 |
| Time in Cash | 0% | 0% | ~15–25% |
| Bear Market Protection | None | Partial | Strong |

*Note: Indian backtests are illustrative estimates based on available academic studies and the Nifty 500 universe (2003–2023). Actual results vary by universe and implementation.*

The most striking feature: **Dual Momentum significantly reduces maximum drawdown** — often by 50% or more compared to Classic Momentum — while giving up only modest upside.

---

### Risk Profile and Drawdown Characteristics

Dual Momentum is the strategy most focused on **capital preservation**. The cash signal acts as an automatic bear market hedge.

**How it handled major Indian bear markets:**
- **2008 Global Financial Crisis:** Nifty fell -60%. Dual Momentum would have moved to cash in late 2007/early 2008, avoiding most of the decline.
- **2020 COVID Crash:** Nifty fell -38% in ~40 days. The speed of the crash meant the monthly signal may not have triggered immediately — this is a known limitation.
- **2015–2016 Correction:** Gradual enough that the 12M signal would have triggered.

**Risk profile:**
- Beta: ~0.6–0.8 (significantly lower due to cash allocation)
- Volatility: ~12–18% annualised
- Tail risk: Lower than Classic Momentum; cash periods absorb bear market losses
- Whipsaw risk: Monthly rebalancing can cause false exits (move to cash then back to equity)

**Key limitation:** In very fast crashes (V-shaped, like COVID March 2020), the monthly signal lags and may not protect fully. The 12-month lookback is also slow — it takes many months of negative trend before the signal fires.

---

### When It Works Best / When It Fails

**Works best when:**
- Bear markets are gradual and sustained (2008-style, multi-month declines)
- Investor has low risk tolerance and cannot stomach -40% drawdowns
- Investor will actually follow the system during cash periods (not FOMO back into equity)
- Long-term horizon (10+ years): avoiding one major crash is worth occasional whipsaws

**Fails when:**
- V-shaped crashes and immediate recoveries (2020 COVID bounce)
- Choppy, oscillating markets (repeated false signals → cash in, cash out, friction costs)
- Investor cannot hold liquid/cash during prolonged bear markets without deviating
- Short backtesting periods that don't capture a full bear market

---

### Comparison Notes

- Unique among the four strategies in having a **complete exit to cash** — others stay invested at all times.
- Simpler signal than Risk-Adjusted Momentum; no volatility calculation required.
- Better bear market protection than Classic or 52-Week High Momentum.
- Slightly lower annualised return than Classic Momentum in pure bull markets (penalty for holding cash).
- The "portfolio-level" nature of the cash signal means all stocks exit simultaneously — no gradual de-risking.

---

### Implementation in This Tool

- **Market regime check:** Nifty 50 or Nifty 500 12-month return evaluated monthly
- **Cash signal threshold:** 0% (configurable: some users use -5% to reduce whipsaws)
- **Cash equivalent:** Tool flags CASH signal; user directs funds to liquid ETF or savings account
- **Relative momentum signal:** Same 12-month lookback with 1-month skip
- **Output:** Market Regime indicator (BULL / BEAR), per-stock signals, overall portfolio action
- **Regime history chart:** Shows all past BULL/BEAR signals with Nifty overlay

---

## Strategy 4: 52-Week High Momentum

### Core Thesis (Plain English)

The 52-week high is a psychologically significant price level. Investors anchor to it — they remember the highest price a stock has traded at over the past year. When a stock approaches or breaks above its 52-week high, investors hesitate to buy (anchoring bias: "it's expensive now"). This creates under-reaction. The stock has positive fundamental news but the price does not fully reflect it. Eventually the market catches up, producing a price run-up.

The signal: stocks trading closest to (or recently above) their 52-week high have the strongest momentum, even after controlling for other factors.

---

### Academic Foundation

**Primary Paper:** George, T.J., & Hwang, C.S. (2004). *The 52-Week High and Momentum Investing.* The Journal of Finance, 59(5), 2145–2176.

**Key Findings:**
- Studied NYSE, AMEX, and NASDAQ stocks from 1963–2001 (38 years).
- Stocks closest to their 52-week high outperformed those furthest from it by **0.45% per month** (approximately 5.4% annualised) after controlling for Jegadeesh-Titman momentum.
- **Crucially:** The 52-week high signal contains information not captured by past returns alone.
- The 52-week high strategy explained **more of the momentum effect than past returns themselves** in some sub-periods.
- The signal is based purely on price proximity — no earnings, no fundamentals required.
- The strategy worked because of **investor anchoring**: market makers and institutional traders under-react when prices approach the 52-week high, creating predictable drift.

**Supporting Research:**
- Liu, M., Liu, Q., & Ma, T. (2011). *The 52-Week High Momentum Strategy in International Stock Markets.* Journal of International Money and Finance, 30(1), 180–204.
  - Confirmed 52-week high momentum in 20 international markets.
  - Annualised excess returns ranged from 3.2% to 11.7% across markets.
  - Signal was strongest in less developed markets (higher retail participation, more anchoring bias).
  - This finding is particularly relevant for Indian markets.

- Hong, H., Lim, T., & Stein, J.C. (2000). *Bad News Travels Slowly: Size, Analyst Coverage, and the Profitability of Momentum Strategies.* Journal of Finance, 55(1), 265–295.
  - Complementary paper showing that information diffusion drives the under-reaction that creates the 52-week high signal.

---

### Signal Construction

```
52W_High_Score(i) = Current_Price(i) / 52_Week_High_Price(i)
```

Where:
- `Current_Price(i)` = closing price today
- `52_Week_High_Price(i)` = highest closing price over the past 252 trading days

A score of **1.0** means the stock is exactly at its 52-week high.
A score of **0.80** means the stock is 20% below its 52-week high.
A score of **1.05** means the stock has recently broken above its 52-week high (new all-time or 52W high).

**Ranking:** Stocks are ranked from highest score to lowest. The top N stocks are selected.

**Note on scores above 1.0:** A score slightly above 1.0 indicates a recent 52-week high breakout — historically a particularly strong signal. George & Hwang found these stocks produced the strongest subsequent returns.

**Optional enhancement:** Combine 52W High Score with a volume confirmation filter:
```
If 52W_High_Score > 0.95 AND 20D_Average_Volume > 1.5x 60D_Average_Volume:
    Strengthen the signal
```

---

### Historical Performance Evidence

| Metric | US Markets (George & Hwang, 1963–2001) | India (estimated) |
|---|---|---|
| Annualised Excess Return | ~5–6% over benchmark | ~8–12% |
| Signal Persistence | 6–12 months | 6–12 months |
| Works after Controlling for Classic Momentum | Yes (+0.45%/month alpha) | Likely yes |
| Retail-driven markets premium | Lower | Higher |

Indian market data suggests the 52-week high effect may be stronger than in the US, consistent with Liu et al. (2011)'s finding that the effect is stronger in markets with higher retail participation and lower analyst coverage.

---

### Risk Profile and Drawdown Characteristics

The 52-Week High strategy has a risk profile **between Classic Momentum and Risk-Adjusted Momentum**:

- It naturally selects stocks near all-time highs — which tend to be fundamentally strong companies.
- Stocks near their 52-week high tend to have lower realized volatility than the broader market.
- However, like Classic Momentum, it has no cash signal — it stays invested at all times.

**Risk profile:**
- Beta: ~0.9–1.1
- Volatility: ~18–25% annualised
- Max Drawdown: ~-35% to -55%
- Crash sensitivity: Moderate (similar to Classic Momentum but slightly less severe)

**Crash behavior:** Stocks near their 52-week high tend to hold up better in early-stage selloffs (they are already "overbought" only in the anchoring sense, not fundamentally). However, in severe bear markets, they fall with everything else.

---

### When It Works Best / When It Fails

**Works best when:**
- Markets are in a broad bull phase with sector leadership
- Individual stocks are breaking out on earnings or news catalysts
- High retail participation amplifies anchoring effects
- Mid-cap and small-cap focused (more anchoring bias; less efficient pricing)

**Fails when:**
- Broad market selloff: "near 52-week high" stocks fall hard as sentiment reverses
- Earnings disappointment on breakout stocks (the signal doesn't use fundamentals)
- Market is making new all-time highs: all stocks cluster near their 52-week highs → signal degenerates
- Very thin liquidity stocks: 52-week high may be an old, thin-volume print

---

### Comparison Notes

- **Most intuitive** of the four strategies to explain to a layperson: "buy stocks near their year-high."
- **Lowest data requirement**: only needs current price and 52-week high.
- Provides **independent signal** from Classic Momentum — can be combined for improved results.
- Does not incorporate volatility information (unlike Risk-Adjusted Momentum).
- Does not have a cash/bear-market switch (unlike Dual Momentum).
- Works particularly well for **mid/small-cap** stocks where anchoring effects are stronger.

---

### Implementation in This Tool

- **Signal:** `Current Price / 52-Week High Price`
- **Lookback window:** 252 trading days (approximately 12 months)
- **Ranking:** Highest score = strongest signal
- **Output columns:** 52W High, Current Price, Proximity Score (%), Rank, Signal
- **Visual indicator:** Stocks above 0.95 score highlighted; stocks at/above 52W high flagged with breakout marker
- **Universe filter:** Optional minimum average daily volume filter to exclude illiquid stocks

---

## Strategy Comparison Table

| Feature | Classic Momentum | Risk-Adjusted Momentum | Dual Momentum | 52-Week High |
|---|---|---|---|---|
| **Primary Signal** | 12M past return | Return / Volatility | 12M return + market filter | Price / 52W High |
| **Academic Source** | Jegadeesh & Titman (1993) | Barroso & Santa-Clara (2015) | Antonacci (2012/2014) | George & Hwang (2004) |
| **Data Required** | Monthly prices (12M) | Daily prices (12M) | Monthly prices + index (12M) | Daily prices (52W) |
| **Complexity** | Low | Medium | Low-Medium | Low |
| **Has Cash Signal?** | No | No (only size reduction) | Yes | No |
| **Bear Market Protection** | Weak | Moderate | Strong | Weak |
| **Est. Annualised Return (India)** | 18–22% | 14–17% | 16–20% | 15–19% |
| **Max Drawdown (India, est.)** | -45 to -55% | -20 to -30% | -20 to -30% | -35 to -50% |
| **Sharpe Ratio** | 0.6–0.9 | 0.9–1.0 | 0.9–1.2 | 0.7–0.9 |
| **Signal Frequency** | Monthly | Monthly | Monthly | Monthly |
| **Best Market Phase** | Trending bull | All phases | All phases | Breakout phase |
| **Worst Market Phase** | Sharp reversals | Vol spikes on good news | Fast V-shaped crash | All stocks near high |
| **Suitable Horizon** | 3–10 years | 5–15 years | 10+ years | 2–7 years |
| **Recommended for** | Aggressive growth | Risk-conscious | Capital preservation | Mid/small-cap focus |

---

## Which Strategy Suits You?

### By Risk Tolerance

**High risk tolerance — full drawdowns acceptable:**
Use **Classic Momentum**. Maximises raw return. Expect drawdowns of 40–55%. Requires conviction to hold through crashes.

**Medium risk tolerance — want strong returns but not -50% drawdowns:**
Use **Risk-Adjusted Momentum**. Best Sharpe ratio. Drawdowns typically below -30%. Slightly lower upside.

**Low risk tolerance — capital preservation matters most:**
Use **Dual Momentum**. Exits to cash in bear markets. May miss some upside. Dramatically lower drawdowns. Requires willingness to hold cash for extended periods.

**Sector / thematic investor — interested in breakouts:**
Use **52-Week High Momentum**. Works well as a complement to Classic Momentum. Best for mid/small-cap focused portfolios.

### By Investment Horizon

| Horizon | Recommended Strategy |
|---|---|
| Under 3 years | Dual Momentum (capital preservation priority) |
| 3–7 years | Risk-Adjusted Momentum or Dual Momentum |
| 7–15 years | Classic Momentum or Risk-Adjusted Momentum |
| 15+ years | Classic Momentum (crashes average out over decades) |

### By Portfolio Size (Indian Context)

| Portfolio Size | Recommendation |
|---|---|
| Under ₹2 lakh | Dual Momentum (fewer holdings, lower transaction costs) |
| ₹2L – ₹10L | Risk-Adjusted Momentum (top 10–15 stocks) |
| ₹10L – ₹50L | Classic or Risk-Adjusted Momentum (top 15–20 stocks) |
| Above ₹50L | All four strategies can be run in combination |

### Combining Strategies

A common advanced approach: **run two strategies simultaneously and average the rankings.** For example:

- **Classic + Risk-Adjusted**: Average the momentum scores. Gets you diversification of signal.
- **Classic + 52-Week High**: Historically produced higher Sharpe ratios than either alone (as shown by George & Hwang and Antonacci's research on combining signals).
- **Dual + Risk-Adjusted**: The most conservative combination; volatility scaling + cash switch.

---

## Momentum Investing in Indian Markets

### Why Momentum Works Especially Well in India

1. **High retail participation:** Approximately 90%+ of daily trading volume involves retail investors who are more prone to anchoring, herding, and delayed reaction to news — exactly the behavioral biases that momentum exploits.

2. **Analyst coverage gaps:** Indian mid-cap and small-cap stocks have far less analyst coverage than US stocks. Information diffuses more slowly, creating longer-lasting momentum trends.

3. **Earnings autocorrelation:** Indian corporate earnings have historically shown significant quarter-to-quarter autocorrelation — companies beating estimates tend to beat again. This fundamental driver underlies momentum.

4. **FII flow cycles:** Foreign Institutional Investor (FII) flows tend to create persistent sector rotation patterns — when FIIs buy IT, they buy it for multiple quarters. This creates medium-term sector momentum.

5. **Regulatory and index inclusion effects:** Stocks entering Nifty indices receive significant buying pressure from passive funds, creating strong momentum. Stocks near inclusion are particularly interesting for 52-Week High momentum.

### India-Specific Considerations

**Fiscal Year Effects:**
- March-end: FII rebalancing, mutual fund portfolio disclosure effects. Momentum may reverse briefly.
- April: New fiscal year FII inflows often restart momentum trends.
- January: Global rebalancing effects can cause temporary reversals.

**Sector Concentration Risk:**
- Momentum portfolios in India can become heavily concentrated in 2–3 sectors (IT, BFSI, Pharma have historically dominated).
- Monitor sector weights. Consider a maximum sector concentration limit (e.g., no more than 40% in one sector).

**Liquidity Constraints:**
- If using Nifty 500 universe, filter out stocks with average daily trading volume below ₹2 crore to avoid impact costs.
- For portfolios above ₹10 lakh, avoid stocks with market cap below ₹1,000 crore.

**Tax Implications (India):**
- Monthly rebalancing creates frequent short-term capital gains (STCG at 20% for equity held less than 12 months).
- Alternatively, quarterly rebalancing reduces STCG frequency at modest performance cost.
- Consider holding winners for 12+ months where possible to shift gains to LTCG (10%).

**SEBI Regulations:**
- This tool operates in dry-run / educational mode. All signals are for informational purposes.
- No SEBI registration required for personal portfolio management.
- If acting on signals, comply with relevant SEBI regulations on algorithmic trading.

### Academic Evidence from India

- **Sehgal, S., & Jain, S. (2011):** Found momentum profits of 1.5–2.0% per month in Nifty 500 stocks (2001–2010). Stronger in mid/small-cap.
- **Ansari & Khan (2012):** Confirmed momentum in BSE 500 with 6-month lookback. Returns decayed over 24 months.
- **Novy-Marx, R. (2012)** (*Journal of Financial Economics*): Showed that 7–12 month momentum ("intermediate" momentum) is stronger than 1–6 month — directly relevant for the 12-month lookback used here.

---

## Risk Warnings

**Read these carefully before using any momentum strategy.**

### Strategy-Level Risks

1. **Momentum crashes are real and severe.** All four strategies (especially Classic and 52-Week High) can lose 30–60% in rapid market reversals. Past performance does not guarantee future results.

2. **Model risk:** All signals are based on historical patterns. Past correlations can and do break down. A strategy that worked for 30 years in the US may behave differently in India, or during a structural market shift.

3. **Overcrowding risk:** As momentum strategies become more popular, they can become self-defeating. When too many investors follow the same signal, entry prices rise and subsequent returns fall. Monitor for crowding by checking how many stocks your signal shares with well-known momentum ETFs.

4. **Liquidity risk:** If you must sell during a momentum crash, mid/small-cap momentum stocks may have very wide bid-ask spreads or be illiquid entirely.

5. **Behavioral execution risk:** The biggest risk in momentum investing is *you*. The strategy requires buying stocks that have already run up (feels expensive) and exiting stocks that have fallen (feels like selling low). Most investors cannot follow rules mechanically during market extremes.

### Operational Risks

6. **Data quality risk:** Incorrect prices, corporate action errors (stock splits, dividends), or missing data will corrupt the momentum signal. Always verify data quality before acting on signals.

7. **Survivorship bias:** Historical backtests typically exclude delisted stocks, overstating past performance. Real-world returns will be lower.

8. **Rebalancing friction:** Transaction costs, STT, GST, and brokerage fees reduce net returns. Monthly rebalancing in a 10-stock portfolio generates 20 trades/month. At 0.1% per side, this adds up to 2.4% annualised drag — material for smaller portfolios.

9. **Market impact:** For larger portfolios (above ₹50 lakh), your own trades may move prices in mid/small-cap stocks.

### This Tool is Not Financial Advice

- Signals generated by this tool are for educational and informational purposes only.
- This tool does not constitute a SEBI-registered investment advisory service.
- Always consult a qualified financial advisor before making investment decisions.
- Past strategy performance shown in this tool is based on historical data and simulations. It does not guarantee future results.

---

## Glossary

| Term | Definition |
|---|---|
| **Absolute Momentum** | The return of an asset compared to a fixed benchmark (typically cash/zero). Positive absolute momentum = asset has gone up over the lookback period. Used in Dual Momentum's market filter. |
| **Alpha** | Return in excess of what is predicted by a benchmark or risk model. Momentum alpha is the return attributable to the momentum signal after accounting for market risk. |
| **Anchoring Bias** | A cognitive bias where investors fixate on a reference price (e.g., the 52-week high) and adjust slowly from it, creating predictable under-reaction in prices. |
| **Annualised Return** | The compound annual growth rate of a strategy's total return over its history. Formula: `(Ending Value / Starting Value)^(1/Years) - 1`. |
| **Backtesting** | Simulating a strategy's performance on historical data. Essential for strategy evaluation but subject to look-ahead bias and survivorship bias if not done carefully. |
| **Beta** | A measure of a portfolio's sensitivity to market movements. Beta of 1.0 = moves exactly with the market. Beta of 0.7 = moves 70% as much as the market. |
| **Calmar Ratio** | Annualised return divided by maximum drawdown. Higher = better risk-adjusted performance. A Calmar of 0.5 means the strategy returned 50 paise per rupee of maximum loss. |
| **Carhart 4-Factor Model** | An asset pricing model that extends Fama-French 3 factors (market, size, value) with a momentum factor (WML). Widely used in academic performance attribution. |
| **Cross-Sectional Momentum** | Ranking stocks relative to each other by past returns and buying the top-ranked ones. Also called "relative momentum." Different from time-series/absolute momentum. |
| **Drawdown** | The peak-to-trough decline in portfolio value during a specific period. Maximum drawdown is the largest such decline over the full history. |
| **Dual Momentum** | Gary Antonacci's strategy combining relative momentum (stock selection) with absolute momentum (market filter). Exits to cash when the market's 12M return is negative. |
| **Equal Weight** | Allocating the same rupee amount to each position in the portfolio. Simpler and often outperforms cap-weighted in momentum portfolios. |
| **Factor Investing** | Investing based on systematic, persistent sources of return (factors) such as momentum, value, size, and quality. |
| **52-Week High** | The highest closing price of a stock over the past 252 trading days (~12 months). Used as the denominator in the 52-Week High Momentum signal. |
| **Formation Period** | The historical lookback window used to calculate the momentum signal (typically 6–12 months). |
| **Holding Period** | The duration for which selected stocks are held before the portfolio is rebalanced. Typically 1 month in this tool. |
| **Intermediate Momentum** | The momentum signal based on 7–12 month past returns (as opposed to 1–6 month). Research suggests intermediate momentum is more reliable than short-term momentum. |
| **Lookback Window** | The historical period over which the momentum signal is measured. This tool uses 12 months by default. |
| **Market Regime** | A characterization of the current market environment (bull or bear). In Dual Momentum, regime is determined by the 12-month return of the Nifty index. |
| **Max Drawdown** | The maximum observed loss from a historical peak in portfolio value. A key measure of downside risk. |
| **Momentum Crash** | A rapid, severe decline in a momentum portfolio, typically occurring when laggard (short) stocks rebound sharply. The most significant risk of momentum strategies. |
| **Momentum Factor (WML)** | Winners Minus Losers — the return spread between the top-performing and bottom-performing stocks, used as a factor in academic models. |
| **Realized Volatility** | The standard deviation of actual historical returns over a period, annualised. Used in Risk-Adjusted Momentum to scale the signal. Formula: `StdDev(daily returns) × √252`. |
| **Rebalancing** | Periodically re-evaluating the portfolio and buying/selling stocks to align with the current momentum rankings. This tool supports monthly rebalancing. |
| **Relative Momentum** | Ranking assets against each other by past returns. You are always invested; you simply shift capital to the current winners. |
| **Risk-Adjusted Momentum** | A strategy that divides each stock's momentum score by its recent volatility, favouring high-return, low-volatility stocks. Based on Barroso & Santa-Clara (2015). |
| **Sharpe Ratio** | Return in excess of the risk-free rate divided by the standard deviation of returns. Higher = better risk-adjusted performance. A Sharpe of 1.0 means the strategy earned 1 unit of return per unit of risk. |
| **Signal** | The output of the momentum calculation for a stock — the numerical score and the resulting action (BUY/HOLD/EXIT). |
| **Skip Month** | The practice of excluding the most recent 1-month return from the momentum lookback window, to avoid contamination from short-term reversal. |
| **STCG / LTCG** | Short-Term Capital Gains (equity held < 12 months, taxed at 20% in India) and Long-Term Capital Gains (equity held ≥ 12 months, taxed at 10% above ₹1 lakh). |
| **Target Volatility** | A desired level of portfolio volatility used in Moreira-Muir volatility management. The portfolio's position size is scaled to maintain this target. |
| **Time-Series Momentum** | Each asset's return compared to its own past return (positive = buy, negative = sell). Same as absolute momentum. Studied systematically by Moskowitz, Ooi & Pedersen (2012). |
| **Universe** | The set of stocks from which the momentum portfolio is constructed (e.g., Nifty 50, Nifty 100, Nifty 500). |
| **Volatility-Managed Portfolio** | A portfolio where position sizes are scaled inversely with recent volatility, as in Moreira & Muir (2017). Reduces crash exposure. |
| **Whipsaw** | A false signal: the strategy exits to cash (or reduces exposure) only for the market to immediately recover, resulting in a loss from both the exit and re-entry. A key risk of the Dual Momentum cash signal. |
| **Winners Minus Losers (WML)** | See Momentum Factor. |

---

*This document is for informational and educational purposes only. It does not constitute investment advice. All references to historical performance are based on academic research and simulations; actual results will differ.*
