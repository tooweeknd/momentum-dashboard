# Momentum Portfolio Tool

A free, open-source web dashboard for building and monthly-rebalancing a momentum-based equity portfolio from the NIFTY 500 universe. Four research-backed strategies, live market data, no API keys required.

**Live App:** [pick-momentum.streamlit.app](https://pick-momentum.streamlit.app/)
**GitHub:** [github.com/tooweeknd/momentum-dashboard](https://github.com/tooweeknd/momentum-dashboard)

---

## What this tool does

Every month, select a strategy, run the tool, and get:
- A ranked list of the 15 strongest momentum stocks with capital allocation
- Exact rebalancing actions: **BUY**, **HOLD**, **SELL** vs last month
- Performance of last month's portfolio vs Nifty 50
- A market regime signal — are conditions right to deploy?

---

## Quickstart

```bash
git clone https://github.com/tooweeknd/momentum-dashboard.git
cd momentum-dashboard
pip install -r requirements.txt
python -m streamlit run app.py
```

Opens at `http://localhost:8501`. No API keys needed.

---

## The Four Strategies

| Strategy | Core Signal | Research Basis | Risk |
|----------|------------|----------------|------|
| Classic Momentum | 12-1 raw return | Jegadeesh & Titman (1993) | High |
| Risk-Adjusted Momentum | 12-1 return / volatility | Barroso & Santa-Clara (2015) | Medium |
| Dual Momentum | Relative rank + absolute filter + cash signal | Antonacci (2014) | Low-Medium |
| 52-Week High Momentum | Nearness to 52-week high | George & Hwang (2004) | Medium |

Full strategy explanations, research citations, and performance characteristics: [`docs/strategy-guide.md`](docs/strategy-guide.md)

---

## Documentation

| Document | What it covers |
|----------|---------------|
| [`docs/strategy-guide.md`](docs/strategy-guide.md) | Deep research on all 4 strategies, comparisons, which to choose |
| [`docs/user-walkthrough.md`](docs/user-walkthrough.md) | Step-by-step usage guide, monthly workflow, interpreting results |

---

## Monthly Workflow

1. Open the app at month-end (after market close)
2. Check the **Market Regime** panel — if red, read the strategy note before deploying
3. Select your strategy, enter capital, click **Run Strategy**
4. Act on the **Rebalancing Actions**: NEW → buy, HOLD → keep, EXIT → sell
5. Click **Save Run & Download History** — upload this file next month

---

## Key Metrics

| Metric | Formula | What it means |
|--------|---------|---------------|
| 12-1 Return | (Price 1M ago / Price 12M ago) − 1 | Momentum signal skipping short-term reversal |
| Risk-Adj Score | 12-1 Return / Ann. Volatility | Reward per unit of risk — primary ranking metric |
| Ann. Volatility | Daily log-return std × √252 | How erratically the stock moves |
| vs 52W High | (Current / 52W High) − 1 | Proximity to breakout level |

---

## Tech Stack

| Component | Library |
|-----------|---------|
| Dashboard | Streamlit |
| Market data | yfinance (Yahoo Finance) |
| Data processing | pandas, numpy |
| Charts | Plotly |

---

## Important Notes

- Run after market close for accurate end-of-day prices
- yfinance occasionally has brief outages when Yahoo Finance changes their API — usually resolved within a day via `pip install --upgrade yfinance`
- Portfolio history JSON stays on your device — no user data is stored on any server
- Not investment advice

---

## License

MIT — free to use, modify, and distribute.
