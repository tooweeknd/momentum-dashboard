"""
Momentum Portfolio Tool
========================
NIFTY 500 universe · 4 research-backed strategies · Top 15 stocks

Strategies available:
1. Classic Momentum          — Jegadeesh & Titman (1993)
2. Risk-Adjusted Momentum    — Barroso & Santa-Clara (2015)
3. Dual Momentum             — Gary Antonacci (2014)
4. 52-Week High Momentum     — George & Hwang (2004)
"""

import io
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import streamlit as st
import yfinance as yf

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Momentum Portfolio Tool",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Constants ─────────────────────────────────────────────────────────────────

NIFTY500_CSV_URL = "https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv"
TOP_N            = 15
MA_PERIOD        = 200
LOOKBACK_DAYS    = 252
SKIP_DAYS        = 21
MIN_DATA_NEEDED  = LOOKBACK_DAYS + 5
MIN_MARKET_CAP   = 5_000_000_000   # ₹500 Crore
MAX_ANNUAL_VOL   = 1.20            # 120%

# ── Strategy Definitions ──────────────────────────────────────────────────────

STRATEGIES = {
    "classic": {
        "name":     "Classic Momentum",
        "emoji":    "📈",
        "tagline":  "The original factor — strong stocks keep winning",
        "risk":     "High",
        "best_for": "Experienced investors comfortable with drawdowns in bear markets",
        "allocation": "Equal weight",
        "paper":    "Jegadeesh & Titman, *Journal of Finance*, 1993",
        "plain_english": """
In 1993, Narasimhan Jegadeesh and Sheridan Titman published one of the most replicated
findings in financial economics: **stocks that performed best over the past 12 months
continue to outperform over the next 3–12 months.**

This strategy does exactly that — ranks all 500 stocks by their 12-1 return (12 months ago
to 1 month ago, skipping the last month to avoid short-term reversal) and buys the top 15.
All 15 get equal capital. Simple, transparent, and well-studied.

**When it works best:** Sustained bull markets where trends persist.
**When it struggles:** Sharp market reversals, high-volatility regimes, bear markets.
The strategy has no built-in protection — it stays fully invested even when the market
is crashing.
        """,
        "pros": [
            "Simplest to understand and execute",
            "30+ years of academic evidence",
            "Very strong in bull markets",
        ],
        "cons": [
            "Severe drawdowns during market crashes (momentum crash risk)",
            "No volatility control — can pick erratic, high-risk winners",
            "No downside protection",
        ],
    },

    "risk_adjusted": {
        "name":     "Risk-Adjusted Momentum",
        "emoji":    "⚖️",
        "tagline":  "Momentum with volatility control — best Sharpe ratio",
        "risk":     "Medium",
        "best_for": "Most investors — best balance of returns and risk",
        "allocation": "Score-weighted (risk-adj ratio)",
        "paper":    "Barroso & Santa-Clara, *Journal of Financial Economics*, 2015",
        "plain_english": """
Pedro Barroso and Pedro Santa-Clara identified a key flaw in classic momentum: it generates
its worst returns precisely when you least expect it — during sudden market recoveries after
crashes. They showed that **scaling momentum by its own volatility dramatically improves
risk-adjusted returns** and nearly eliminates the "momentum crash" phenomenon.

This strategy scores each stock as: `12-1 Return / Annualised Volatility`

A stock up 60% with 20% volatility (score: 3.0) ranks **higher** than a stock up 80%
with 70% volatility (score: 1.14). The first stock's trend is smooth and persistent;
the second is erratic and likely to reverse. You want to own smooth trends, not lottery tickets.

Allocation is return-weighted — stronger momentum names get proportionally more capital.

**When it works best:** All market conditions; particularly resilient in choppy markets.
**When it struggles:** Very sharp, narrow bull markets where the most volatile stocks lead.
        """,
        "pros": [
            "Lower maximum drawdown vs classic momentum",
            "Better Sharpe ratio — more return per unit of risk",
            "Filters out speculative, low-quality momentum",
            "Score-weighted sizing: higher risk-adjusted signal → larger position",
        ],
        "cons": [
            "Can underperform classic momentum in strong, broad bull runs",
            "Slightly more complex to explain",
        ],
    },

    "dual": {
        "name":     "Dual Momentum",
        "emoji":    "🛡️",
        "tagline":  "Relative + absolute momentum — built-in bear market shield",
        "risk":     "Low-Medium",
        "best_for": "Capital-preservation focused investors; those who can't tolerate large drawdowns",
        "allocation": "Equal weight",
        "paper":    "Gary Antonacci, *Dual Momentum Investing*, 2014",
        "plain_english": """
Gary Antonacci combined two types of momentum into one system:

1. **Relative Momentum** — rank stocks vs each other (same as classic momentum)
2. **Absolute Momentum** — check if the stock itself is trending up in absolute terms
   (12-1 return must be positive)

A stock must pass **both** tests to enter the portfolio. If a stock ranks in the top 15
but has a negative 12-1 return, it is excluded. This prevents buying stocks that are
"best of a bad bunch" during a falling market.

Additionally, the strategy has a **cash signal**: if Nifty 50's own 12-month return is
negative, the entire strategy moves to cash (or short-term bonds). This is the key
differentiator — it can keep you completely out of bear markets.

**When it works best:** Market downturns, volatile regimes. Capital preservation is exceptional.
**When it struggles:** Sideways markets with many whipsaws (in → cash → in → cash).
The cash filter can cause you to miss early bull market rallies.
        """,
        "pros": [
            "Built-in bear market protection — can move to 100% cash",
            "Avoids buying 'best of a bad bunch' in falling markets",
            "Historically lower maximum drawdown than pure momentum",
            "Clear, rules-based entry/exit criteria",
        ],
        "cons": [
            "Can miss early bull market recoveries (lag from cash signal)",
            "Whipsaw risk: frequent in/out signals in sideways markets",
            "Fewer eligible stocks during weak markets (fewer pass both filters)",
        ],
    },

    "52wk_high": {
        "name":     "52-Week High Momentum",
        "emoji":    "🎯",
        "tagline":  "Breakout-focused — nearness to highs predicts continuation",
        "risk":     "Medium",
        "best_for": "Investors who want a momentum signal different from return-based ranking",
        "allocation": "Equal weight",
        "paper":    "George & Hwang, *Journal of Finance*, 2004",
        "plain_english": """
Thomas George and Chuan-Yang Hwang made a surprising discovery: **how close a stock is
to its 52-week high is a stronger predictor of future returns than the stock's past return itself.**

Why? Investors use the 52-week high as a **psychological anchor**. When a stock approaches
its 52-week high, investors become reluctant to buy (anchoring bias), artificially suppressing
the price. When the stock eventually breaks through — propelled by strong fundamentals or
earnings — the pent-up buying accelerates rapidly. This creates a predictable momentum effect.

Ranking: `Current Price / 52-Week High`
A stock trading at its 52-week high scores 1.0. A stock 20% below its high scores 0.80.
The strategy buys stocks closest to (or just breaking) their 52-week highs.

**When it works best:** Breakout environments, late-stage bull markets, sector rotations.
**When it struggles:** Stocks near 52-week highs in a falling market — these can reverse fast.
        """,
        "pros": [
            "Captures breakout dynamics missed by return-based ranking",
            "Complementary signal to 12-month return — different stocks qualify",
            "Backed by strong academic evidence across global markets",
            "Simple, intuitive logic",
        ],
        "cons": [
            "No volatility filter — can include high-vol breakout names",
            "No downside protection in bear markets",
            "Less differentiation when most stocks are near highs (bull market top)",
        ],
    },
}


# ── Data Fetching ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=86_400, show_spinner=False)
def load_nifty500_constituents() -> tuple:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.nseindia.com/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com/", headers=headers, timeout=12)
        time.sleep(0.6)
        resp = session.get(NIFTY500_CSV_URL, headers=headers, timeout=20)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
        df.columns = df.columns.str.strip()
        df = df.rename(columns={
            "Company Name": "company", "Industry": "sector",
            "Symbol": "symbol", "Series": "series",
        })
        df = df[df["series"].str.strip() == "EQ"].copy()
        df["symbol"] = df["symbol"].str.strip()
        df["ticker"] = df["symbol"] + ".NS"
        return df[["symbol", "company", "sector", "ticker"]].reset_index(drop=True), None
    except Exception as exc:
        return None, str(exc)


@st.cache_data(ttl=3_600, show_spinner=False)
def load_nifty_trend() -> dict | None:
    try:
        raw   = yf.download("^NSEI", period="2y", auto_adjust=True, progress=False)
        close = raw["Close"].squeeze()
        ma200 = close.rolling(MA_PERIOD).mean()
        ma50  = close.rolling(50).mean()
        current = float(close.iloc[-1])
        ma_val  = float(ma200.iloc[-1])
        nifty_ret_12m = float((close.iloc[-1] / close.iloc[-LOOKBACK_DAYS]) - 1) \
            if len(close) >= LOOKBACK_DAYS else None
        return {
            "price":         current,
            "ma200":         ma_val,
            "ma50":          float(ma50.iloc[-1]),
            "pct_vs_ma":     (current - ma_val) / ma_val * 100,
            "is_uptrend":    current > ma_val,
            "ret_12m":       nifty_ret_12m,
            "as_of":         close.index[-1].strftime("%d %b %Y"),
            "close":         close.tail(500),
            "ma200_s":       ma200.tail(500),
            "ma50_s":        ma50.tail(500),
        }
    except Exception:
        return None


@st.cache_data(ttl=3_600, show_spinner=False)
def load_price_data(tickers_tuple: tuple) -> pd.DataFrame | None:
    tickers = list(tickers_tuple)
    start   = (datetime.today() - timedelta(days=460)).strftime("%Y-%m-%d")
    end     = datetime.today().strftime("%Y-%m-%d")
    try:
        raw = yf.download(tickers, start=start, end=end,
                          auto_adjust=True, progress=False, threads=True)
        if isinstance(raw.columns, pd.MultiIndex):
            return raw["Close"]
        return raw[["Close"]].rename(columns={"Close": tickers[0]})
    except Exception as exc:
        st.error(f"Price data download failed: {exc}")
        return None


def _fetch_one_mcap(ticker: str) -> tuple:
    try:
        mc = yf.Ticker(ticker).fast_info.market_cap
        return ticker, float(mc) if mc else 0.0
    except Exception:
        return ticker, 0.0


def batch_market_caps(tickers: list, workers: int = 30) -> dict:
    results: dict = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(_fetch_one_mcap, t): t for t in tickers}
        for fut in as_completed(futures):
            t, mc = fut.result()
            results[t] = mc
    return results


# ── Strategy Scoring ──────────────────────────────────────────────────────────

def compute_stock_metrics(series: pd.Series) -> dict | None:
    if len(series) < MIN_DATA_NEEDED:
        return None
    current_px = float(series.iloc[-1])
    px_1m_ago  = float(series.iloc[-SKIP_DAYS])
    px_12m_ago = float(series.iloc[-LOOKBACK_DAYS])
    if any(p <= 0 for p in [current_px, px_1m_ago, px_12m_ago]):
        return None

    ret_12m  = (current_px / px_12m_ago) - 1
    ret_12_1 = (px_1m_ago  / px_12m_ago) - 1

    # Restrict to last 252 trading days so all stocks use an identical volatility window
    log_ret = np.log(series.tail(253) / series.tail(253).shift(1)).dropna()
    ann_vol = float(log_ret.std() * np.sqrt(252))
    if ann_vol <= 0 or ann_vol > MAX_ANNUAL_VOL:
        return None

    ma200 = series.rolling(MA_PERIOD).mean()
    above_200 = current_px > float(ma200.iloc[-1]) if not np.isnan(float(ma200.iloc[-1])) else True

    high_52wk   = float(series.tail(252).max())
    pct_52wk_hi = (current_px / high_52wk) - 1

    return {
        "price":       current_px,
        "ret_12m":     ret_12m,
        "ret_12_1":    ret_12_1,
        "ann_vol":     ann_vol,
        "above_200ma": above_200,
        "high_52wk":   high_52wk,
        "pct_52wk_hi": pct_52wk_hi,
    }


def compute_score(strategy_key: str, m: dict) -> float | None:
    """Return a score for ranking. Return None to exclude the stock."""
    if strategy_key == "classic":
        return m["ret_12_1"]

    elif strategy_key == "risk_adjusted":
        return m["ret_12_1"] / m["ann_vol"] if m["ann_vol"] > 0 else None

    elif strategy_key == "dual":
        # Absolute momentum filter: 12-1 return must be positive
        if m["ret_12_1"] <= 0:
            return None
        return m["ret_12_1"]

    elif strategy_key == "52wk_high":
        return m["price"] / m["high_52wk"]

    return None


def compute_weights(top: pd.DataFrame, strategy_key: str) -> pd.Series:
    if strategy_key == "risk_adjusted":
        # Weight by risk-adjusted score (ret/vol) — the same signal used for ranking.
        # This means a stock ranked #1 by score also receives the largest allocation.
        scores = top["score"].clip(lower=0)
        total  = scores.sum()
        return scores / total if total > 0 else pd.Series([1.0 / len(top)] * len(top), index=top.index)
    else:
        return pd.Series([1.0 / len(top)] * len(top), index=top.index)


def run_strategy(
    close_df: pd.DataFrame,
    constituents: pd.DataFrame,
    strategy_key: str,
    capital: float,
    progress_bar,
) -> pd.DataFrame:
    records = []
    tickers = close_df.columns.tolist()
    n       = len(tickers)

    for i, ticker in enumerate(tickers):
        if i % 10 == 0:
            progress_bar.progress(int((i + 1) / n * 65), text=f"Scoring stocks… {i+1}/{n}")

        series  = close_df[ticker].dropna()
        m       = compute_stock_metrics(series)
        if m is None:
            continue

        # Individual trend filter for risk_adjusted and dual (not enforced for classic / 52wk_high)
        if strategy_key in ("risk_adjusted", "dual") and not m["above_200ma"]:
            continue

        score = compute_score(strategy_key, m)
        if score is None:
            continue

        sym = ticker.replace(".NS", "")
        row = constituents[constituents["symbol"] == sym]
        records.append({
            "ticker":      ticker,
            "symbol":      sym,
            "company":     row["company"].values[0] if len(row) else sym,
            "sector":      row["sector"].values[0]  if len(row) else "—",
            "price":       m["price"],
            "ret_12m":     m["ret_12m"],
            "ret_12_1":    m["ret_12_1"],
            "ann_vol":     m["ann_vol"],
            "high_52wk":   m["high_52wk"],   # actual ₹ value — stored so display can show it
            "pct_52wk_hi": m["pct_52wk_hi"],
            "score":       score,
        })

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records).sort_values("score", ascending=False).reset_index(drop=True)

    progress_bar.progress(70, text="Fetching market caps…")
    mcaps = batch_market_caps(df.head(60)["ticker"].tolist())
    df["market_cap"] = df["ticker"].map(mcaps).fillna(0.0)
    df = df[(df["market_cap"] >= MIN_MARKET_CAP) | (df["market_cap"] == 0.0)].copy()

    progress_bar.progress(90, text="Building portfolio…")
    top = df.head(TOP_N).copy()
    top.insert(0, "rank", range(1, len(top) + 1))
    top["weight"]     = compute_weights(top, strategy_key)
    top["allocation"] = (top["weight"] * capital).round(0)
    top["shares"]     = (top["allocation"] / top["price"]).apply(np.floor).astype(int)

    progress_bar.progress(100, text="Done.")
    return top


# ── Portfolio History (upload/download — works on any host) ───────────────────

def load_history_from_upload(uploaded_file) -> list:
    try:
        return json.loads(uploaded_file.read())
    except Exception:
        return []


def history_to_json(history: list) -> str:
    return json.dumps(history, indent=2)


def append_run(history: list, top: pd.DataFrame, strategy_key: str,
               run_date: str, nifty_price: float) -> list:
    run = {
        "date":         run_date,
        "strategy":     strategy_key,
        "nifty_price":  round(nifty_price, 2),
        "stocks": top[[
            "symbol", "company", "sector", "price",
            "score", "ret_12_1", "ret_12m", "ann_vol", "weight", "allocation",
        ]].round(6).to_dict("records"),
    }
    return history + [run]


def get_last_run(history: list, strategy_key: str) -> dict | None:
    """Return most recent run for this strategy."""
    matching = [r for r in history if r.get("strategy") == strategy_key]
    return matching[-1] if matching else None


def compute_rebalancing(current_symbols: list, last_run: dict | None) -> tuple:
    if last_run is None:
        return {s: "NEW" for s in current_symbols}, set()
    last_symbols = {r["symbol"] for r in last_run["stocks"]}
    actions = {s: ("HOLD" if s in last_symbols else "NEW") for s in current_symbols}
    exits   = last_symbols - set(current_symbols)
    return actions, exits


def compute_last_run_performance(last_run: dict, close_df: pd.DataFrame, nifty_price: float) -> pd.DataFrame | None:
    if last_run is None or close_df is None:
        return None
    rows = []
    for r in last_run["stocks"]:
        ticker = r["symbol"] + ".NS"
        if ticker not in close_df.columns:
            continue
        series = close_df[ticker].dropna()
        if len(series) < 2:
            continue
        entry   = r["price"]
        current = float(series.iloc[-1])
        rows.append({
            "symbol":    r["symbol"],
            "company":   r["company"],
            "entry_px":  entry,
            "current_px": current,
            "return":    (current / entry) - 1,
            "weight":    r["weight"],
        })
    if not rows:
        return None
    df = pd.DataFrame(rows)
    df["weighted_ret"] = df["return"] * df["weight"]
    return df


# ── UI Components ─────────────────────────────────────────────────────────────

def render_strategy_selector() -> str:
    st.subheader("Select Strategy")

    cols = st.columns(4)
    strategy_keys = list(STRATEGIES.keys())

    if "selected_strategy" not in st.session_state:
        st.session_state.selected_strategy = "risk_adjusted"

    for i, key in enumerate(strategy_keys):
        s = STRATEGIES[key]
        with cols[i]:
            selected = st.session_state.selected_strategy == key
            border   = "2px solid #22c55e" if selected else "1px solid #374151"
            bg       = "#052e16" if selected else "#111827"
            st.markdown(
                f"""<div style="border:{border};border-radius:8px;padding:14px;
                    background:{bg};min-height:160px;cursor:pointer">
                    <div style="font-size:1.5rem">{s['emoji']}</div>
                    <div style="font-weight:700;margin:4px 0">{s['name']}</div>
                    <div style="font-size:0.78rem;color:#9ca3af;margin-bottom:8px">{s['tagline']}</div>
                    <div style="font-size:0.72rem">
                        <span style="color:#6b7280">Risk:</span>
                        <span style="color:#e5e7eb">&nbsp;{s['risk']}</span>&nbsp;&nbsp;
                        <span style="color:#6b7280">Alloc:</span>
                        <span style="color:#e5e7eb">&nbsp;{s['allocation']}</span>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button("Select", key=f"btn_{key}",
                         type="primary" if selected else "secondary",
                         use_container_width=True):
                st.session_state.selected_strategy = key
                st.rerun()

    selected_key = st.session_state.selected_strategy
    s = STRATEGIES[selected_key]

    with st.expander(f"About: {s['name']} — research & reasoning", expanded=False):
        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown(f"**Research basis:** {s['paper']}")
            st.markdown(s["plain_english"])
        with col_right:
            st.markdown("**Strengths**")
            for p in s["pros"]:
                st.markdown(f"- {p}")
            st.markdown("**Weaknesses**")
            for c in s["cons"]:
                st.markdown(f"- {c}")
            st.markdown(f"**Best for:** {s['best_for']}")

    return selected_key


def render_trend_panel(trend: dict | None, strategy_key: str) -> None:
    if trend is None:
        st.warning("Could not load Nifty 50 trend data.")
        return

    label = "UPTREND ↑" if trend["is_uptrend"] else "DOWNTREND ↓"
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(f"Nifty 50  ({trend['as_of']})", f"₹{trend['price']:,.0f}")
    c2.metric("200-Day SMA", f"₹{trend['ma200']:,.0f}")
    c3.metric("50-Day SMA",  f"₹{trend['ma50']:,.0f}")
    c4.metric("vs 200 SMA",  f"{trend['pct_vs_ma']:+.2f}%")
    c5.metric("Regime",      label)

    # Strategy-specific regime messaging
    if strategy_key == "dual" and trend["ret_12m"] is not None and trend["ret_12m"] < 0:
        st.error(
            f"**CASH SIGNAL (Dual Momentum):** Nifty 50's 12-month return is "
            f"{trend['ret_12m']:.1%} — negative. Dual Momentum rules call for moving "
            "**entirely to cash or liquid funds**. Do not deploy this portfolio right now."
        )
    elif not trend["is_uptrend"]:
        st.error(
            f"**{label}** — Nifty is below its 200-day SMA. Momentum strategies underperform "
            "in this regime. Consider reducing position sizes or waiting for trend recovery."
        )
    else:
        st.success(
            f"**{label}** — Nifty is above its 200-day SMA. Favourable regime for momentum."
        )

    with st.expander("View Nifty 50 Chart"):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trend["close"].index, y=trend["close"],
                                 name="Nifty 50", line=dict(color="#3b82f6", width=1.5)))
        fig.add_trace(go.Scatter(x=trend["ma50_s"].index, y=trend["ma50_s"],
                                 name="50-Day SMA", line=dict(color="#a855f7", width=1.4, dash="dot")))
        fig.add_trace(go.Scatter(x=trend["ma200_s"].index, y=trend["ma200_s"],
                                 name="200-Day SMA", line=dict(color="#f59e0b", width=1.8, dash="dash")))
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0),
                          legend=dict(orientation="h", y=-0.2), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)


def render_performance(last_run: dict, close_df: pd.DataFrame, nifty_price: float) -> None:
    perf = compute_last_run_performance(last_run, close_df, nifty_price)
    if perf is None or perf.empty:
        return

    last_nifty    = last_run.get("nifty_price", nifty_price)
    nifty_ret     = (nifty_price / last_nifty) - 1 if last_nifty > 0 else 0
    portfolio_ret = perf["weighted_ret"].sum()
    alpha         = portfolio_ret - nifty_ret

    st.subheader(f"Last Portfolio Performance — since {last_run['date']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Portfolio Return", f"{portfolio_ret:+.2%}", delta=f"vs Nifty {nifty_ret:+.2%}")
    c2.metric("Nifty 50 Return",  f"{nifty_ret:+.2%}")
    c3.metric("Alpha",            f"{alpha:+.2%}", delta_color="normal" if alpha >= 0 else "inverse")

    perf_s = perf.sort_values("return", ascending=False)
    colors = ["#22c55e" if r >= 0 else "#ef4444" for r in perf_s["return"]]
    fig = go.Figure(go.Bar(
        x=perf_s["return"], y=perf_s["symbol"], orientation="h",
        marker_color=colors,
        text=perf_s["return"].map("{:+.1%}".format), textposition="outside",
    ))
    fig.add_vline(x=nifty_ret, line_color="#f59e0b", line_width=1.5,
                  annotation_text="Nifty", annotation_position="top")
    fig.update_layout(title="Individual Stock Returns Since Last Run",
                      height=420, margin=dict(l=0, r=60, t=50, b=0),
                      xaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)


def render_rebalancing(top: pd.DataFrame, last_run: dict | None, strategy_key: str = "") -> None:
    if last_run is None:
        st.info("First run — all positions are new. Save this run to enable rebalancing comparison next month.")
        return

    actions, exits = compute_rebalancing(top["symbol"].tolist(), last_run)
    top = top.copy()
    top["action"] = top["symbol"].map(actions)

    new_s  = top[top["action"] == "NEW"]
    hold_s = top[top["action"] == "HOLD"]

    st.subheader("Rebalancing Actions")
    c1, c2, c3 = st.columns(3)
    c1.metric("Buy — New Entries",   len(new_s),  delta=f"+{len(new_s)}")
    c2.metric("Hold — Carry Forward", len(hold_s))
    c3.metric("Sell — Exits",         len(exits),  delta=f"-{len(exits)}" if exits else "—")

    col_l, col_r = st.columns(2)
    with col_l:
        if not new_s.empty:
            st.markdown("**Buy — place these orders**")
            # classic/dual  : score == ret_12_1 — only show 12-1 Return (no redundant column)
            # 52wk_high     : show 52W High (₹) + Gap from 52W High — verifiable + meaningful
            # risk_adjusted : show Risk-Adj Score + 12-1 Return (genuinely different values)
            if strategy_key in ("classic", "dual"):
                reb_df = (new_s[["symbol", "company", "sector", "ret_12_1", "allocation"]]
                          .assign(ret_12_1=lambda d: d["ret_12_1"].map("{:.2%}".format),
                                  allocation=lambda d: d["allocation"].map("₹{:,.0f}".format))
                          .rename(columns={"ret_12_1": "12-1 Return", "allocation": "Allocated"}))
            elif strategy_key == "52wk_high":
                reb_df = (new_s[["symbol", "company", "sector", "high_52wk", "pct_52wk_hi", "ret_12_1", "allocation"]]
                          .assign(high_52wk=lambda d: d["high_52wk"].map("₹{:,.2f}".format),
                                  pct_52wk_hi=lambda d: d["pct_52wk_hi"].map("{:.2%}".format),
                                  ret_12_1=lambda d: d["ret_12_1"].map("{:.2%}".format),
                                  allocation=lambda d: d["allocation"].map("₹{:,.0f}".format))
                          .rename(columns={"high_52wk": "52W High (₹)", "pct_52wk_hi": "Gap from 52W High",
                                           "ret_12_1": "12-1 Return", "allocation": "Allocated"}))
            else:  # risk_adjusted
                reb_df = (new_s[["symbol", "company", "sector", "score", "ret_12_1", "allocation"]]
                          .assign(score=lambda d: d["score"].map("{:.2f}".format),
                                  ret_12_1=lambda d: d["ret_12_1"].map("{:.2%}".format),
                                  allocation=lambda d: d["allocation"].map("₹{:,.0f}".format))
                          .rename(columns={"score": "Risk-Adj Score", "ret_12_1": "12-1 Return",
                                           "allocation": "Allocated"}))
            st.dataframe(reb_df, hide_index=True, use_container_width=True)
    with col_r:
        if exits:
            st.markdown("**Sell — close these positions**")
            exit_rows = [r for r in last_run["stocks"] if r["symbol"] in exits]
            st.dataframe(pd.DataFrame(exit_rows)[["symbol", "company", "sector"]],
                         hide_index=True, use_container_width=True)
        else:
            st.success("No exits this month — all previous picks remain in the top 15.")


def render_results(top: pd.DataFrame, strategy_key: str, last_run: dict | None) -> None:
    actions, _ = compute_rebalancing(top["symbol"].tolist(), last_run)
    top = top.copy()
    top["action"] = top["symbol"].map(actions)

    s_label = "Risk-Adj Score" if strategy_key == "risk_adjusted" else \
              "Gap from 52W High" if strategy_key == "52wk_high" else \
              "Momentum Score"

    st.subheader(f"Top {len(top)} Stocks — {STRATEGIES[strategy_key]['name']}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Selected", len(top))
    # c2: show a metric that is NOT redundant with c3 (Avg 12-1 Return)
    if strategy_key == "risk_adjusted":
        c2.metric("Avg Risk-Adj Score",   f"{top['score'].mean():.2f}",
                  help="Average (12-1 Return ÷ Ann. Volatility) across the 15 stocks")
    elif strategy_key == "52wk_high":
        c2.metric("Avg Gap from 52W High", f"{top['pct_52wk_hi'].mean():.2%}",
                  help="Average % below the 52-week high. 0.00% = stock is exactly at its 52-week high (strongest breakout signal). Closer to 0% = stronger signal.")
    else:
        # classic / dual: score == ret_12_1 — show 12M return (full year) instead, which IS different
        c2.metric("Avg 12M Return",       f"{top['ret_12m'].mean():.1%}",
                  help="Average full 12-month return (includes last month). Compare to 12-1 Return below.")
    c3.metric("Avg 12-1 Return",          f"{top['ret_12_1'].mean():.1%}",
              help="Average 12-1 momentum signal (12M return skipping last month)")
    c4.metric("Avg Volatility",           f"{top['ann_vol'].mean():.1%}",
              help="Average annualised volatility over the past 252 trading days")

    st.divider()

    # ── Build display columns per strategy ───────────────────────────────────
    #
    # Column layout per strategy
    # ─────────────────────────────────────────────────────────────────────────────
    # classic / dual:
    #   score == ret_12_1 exactly → drop score (already shown as "12-1 Return")
    #   pct_52wk_hi kept as supplementary reference column
    #
    # 52wk_high:
    #   Ranking signal = price / 52W_high (score ≈ 0.97–1.00 in bull market)
    #   Display as TWO columns:
    #     • "52W High (₹)"      — actual high price → user can verify against broker
    #     • "Gap from 52W High" — pct_52wk_hi = (price/high)−1, always ≤ 0
    #       0.00% = stock is AT its 52-week high (strongest signal)
    #       −2.34% = stock is 2.34% below its 52-week high
    #   score column dropped (raw ratio adds nothing the two columns don't already show)
    #
    # risk_adjusted:
    #   score = ret_12_1 / ann_vol — genuinely different from all other columns, keep it
    #   pct_52wk_hi shown as supplementary reference

    base_cols = ["rank", "action", "symbol", "company", "sector"]

    if strategy_key in ("classic", "dual"):
        display_cols = base_cols + ["ret_12_1", "ret_12m", "ann_vol",
                                    "pct_52wk_hi", "weight", "allocation", "shares", "price"]
    elif strategy_key == "52wk_high":
        # high_52wk (₹) + pct_52wk_hi (%) together make the metric fully transparent
        display_cols = base_cols + ["high_52wk", "pct_52wk_hi", "ret_12_1", "ret_12m", "ann_vol",
                                    "weight", "allocation", "shares", "price"]
    else:  # risk_adjusted
        display_cols = base_cols + ["score", "ret_12_1", "ret_12m", "ann_vol",
                                    "pct_52wk_hi", "weight", "allocation", "shares", "price"]

    display = top[display_cols].copy()

    fmt_map = {
        "score":       "{:.2f}".format,        # risk_adjusted only: dimensionless ratio
        "ret_12_1":    "{:.2%}".format,
        "ret_12m":     "{:.2%}".format,
        "ann_vol":     "{:.1%}".format,
        "high_52wk":   "₹{:,.2f}".format,     # 52wk_high only: actual high price in ₹
        "pct_52wk_hi": "{:.2%}".format,        # 2 d.p.: "-0.03%" and "-1.24%" are visibly different
        "weight":      "{:.2%}".format,
        "allocation":  "₹{:,.0f}".format,
        "price":       "₹{:,.2f}".format,
    }
    for col, fn in fmt_map.items():
        if col in display.columns:
            display[col] = display[col].map(fn)

    rename_map = {
        "rank":        "#",
        "action":      "Action",
        "symbol":      "Symbol",
        "company":     "Company",
        "sector":      "Sector",
        "score":       s_label,                # only present for risk_adjusted
        "ret_12_1":    "12-1 Return",
        "ret_12m":     "12M Return",
        "ann_vol":     "Ann. Vol",
        "high_52wk":   "52W High (₹)",         # 52wk_high only: verifiable against broker
        "pct_52wk_hi": "Gap from 52W High",    # 0.00% = at high; −2.34% = 2.34% below high
        "weight":      "Weight",
        "allocation":  "Allocated (₹)",
        "shares":      "Shares",
        "price":       "CMP (₹)",
    }
    display.rename(columns=rename_map, inplace=True)
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.divider()
    col_l, col_r = st.columns(2)
    with col_l:
        # Bar chart: plot the most informative metric per strategy
        if strategy_key in ("classic", "dual"):
            # score == ret_12_1 → plot ret_12_1 with % labels
            chart_col   = "ret_12_1"
            chart_title = "12-1 Return — Ranking Signal"
            bar_fmt     = "{:.1%}".format
            x_tickfmt   = ".0%"
        elif strategy_key == "52wk_high":
            # pct_52wk_hi IS the ranking signal (price/52W_high − 1).
            # Stocks nearest to 0% ranked highest (at 52-week high = strongest breakout).
            # Values are always ≤ 0, so x-axis runs from most-negative (weakest) to 0 (strongest).
            chart_col   = "pct_52wk_hi"
            chart_title = "Gap from 52-Week High — Ranking Signal (0% = at 52W high)"
            bar_fmt     = "{:.2%}".format
            x_tickfmt   = ".1%"
        else:  # risk_adjusted
            # score = ret_12_1 / ann_vol — genuinely different per stock, plot it
            chart_col   = "score"
            chart_title = "Risk-Adjusted Score (Return ÷ Volatility)"
            bar_fmt     = "{:.2f}".format
            x_tickfmt   = ".2f"

        sorted_top = top.sort_values(chart_col)
        fig = go.Figure(go.Bar(
            x=sorted_top[chart_col], y=sorted_top["symbol"], orientation="h",
            marker=dict(color=sorted_top[chart_col],
                        colorscale=[[0, "#fbbf24"], [1, "#16a34a"]]),
            text=sorted_top[chart_col].map(bar_fmt), textposition="outside",
        ))
        fig.update_layout(title=chart_title, height=480,
                          margin=dict(l=0, r=60, t=50, b=0))
        fig.update_xaxes(tickformat=x_tickfmt)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig_pie = px.pie(top, names="symbol", values="allocation",
                         title="Capital Allocation", hole=0.42)
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(height=480, margin=dict(l=0, r=0, t=50, b=0), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    col_l2, col_r2 = st.columns(2)
    with col_l2:
        # For risk_adjusted: color by score (risk-adj ratio, wide range → meaningful gradient)
        # For classic/dual/52wk_high: score range is narrow or same as y-axis;
        #   color by ann_vol (inverted) so greener = lower volatility = smoother trend
        if strategy_key == "risk_adjusted":
            scatter_color     = "score"
            scatter_color_lbl = "Risk-Adj Score"
            scatter_cscale    = ["#fbbf24", "#16a34a"]
        else:
            scatter_color     = "ann_vol"
            scatter_color_lbl = "Ann. Vol"
            scatter_cscale    = ["#16a34a", "#ef4444"]   # green=low vol, red=high vol

        fig_s = px.scatter(
            top, x="ann_vol", y="ret_12_1", text="symbol",
            size="allocation", color=scatter_color,
            color_continuous_scale=scatter_cscale,
            title="Return vs Volatility (bubble = allocation, colour = " + scatter_color_lbl + ")",
            labels={"ann_vol": "Annualised Vol", "ret_12_1": "12-1 Return",
                    scatter_color: scatter_color_lbl},
        )
        fig_s.update_traces(textposition="top center")
        fig_s.update_xaxes(tickformat=".0%")
        fig_s.update_yaxes(tickformat=".0%")
        fig_s.update_layout(height=400, margin=dict(l=0, r=0, t=50, b=0),
                             coloraxis_showscale=False)
        st.plotly_chart(fig_s, use_container_width=True)

    with col_r2:
        sector_df = (top.groupby("sector")["allocation"].sum()
                     .reset_index().sort_values("allocation", ascending=False))
        fig_sec = px.bar(sector_df, x="sector", y="allocation",
                         title="Sector Allocation", color="allocation",
                         color_continuous_scale=["#93c5fd", "#1d4ed8"],
                         labels={"sector": "", "allocation": "₹ Allocated"})
        fig_sec.update_layout(height=400, margin=dict(l=0, r=0, t=50, b=0),
                               coloraxis_showscale=False, xaxis_tickangle=-30)
        st.plotly_chart(fig_sec, use_container_width=True)


# ── Embedded Docs ─────────────────────────────────────────────────────────────

def render_strategy_guide_tab() -> None:
    st.header("Strategy Guide")
    st.caption("Research-backed explanations of all four momentum strategies.")

    for key, s in STRATEGIES.items():
        with st.expander(f"{s['emoji']}  {s['name']} — {s['tagline']}", expanded=False):
            col_l, col_r = st.columns([3, 2])
            with col_l:
                st.markdown(f"**Research basis:** {s['paper']}")
                st.markdown(s["plain_english"])
            with col_r:
                st.markdown(f"**Risk level:** `{s['risk']}`")
                st.markdown(f"**Allocation:** `{s['allocation']}`")
                st.markdown(f"**Best for:** {s['best_for']}")
                st.markdown("**Strengths**")
                for p in s["pros"]:
                    st.markdown(f"- {p}")
                st.markdown("**Weaknesses**")
                for c in s["cons"]:
                    st.markdown(f"- {c}")

    st.divider()
    st.subheader("Choosing the Right Strategy")
    st.markdown("""
| Investor Profile | Recommended Strategy |
|---|---|
| First-time momentum investor | **Risk-Adjusted Momentum** — best balance of returns and risk |
| Aggressive, comfortable with drawdowns | **Classic Momentum** — maximum upside in bull markets |
| Capital preservation is priority | **Dual Momentum** — built-in cash signal in bear markets |
| Want a different signal from the rest | **52-Week High Momentum** — captures breakout dynamics |
| Running multiple strategies | Use **Risk-Adjusted** as primary, **Dual** as a risk check |
    """)

    st.divider()
    st.subheader("Momentum in Indian Markets")
    st.markdown("""
Momentum as a factor is well-documented globally, and India is no exception. Several studies
have confirmed that price momentum generates statistically significant returns in Indian equities:

- The NIFTY 500 universe is broad enough to provide meaningful dispersion between winners and losers.
- Indian markets exhibit stronger momentum persistence than developed markets, partly due to
  higher retail participation and slower institutional price discovery.
- Momentum strategies in India tend to work best in trending bull markets (2014–2017, 2020–2021)
  and experience sharp reversals during sudden corrections (Mar 2020, Oct 2021).
- The 200-day SMA filter is particularly important for Indian markets, which can experience
  rapid 20–30% index corrections during global risk-off events.

**Transaction cost reality:** Monthly rebalancing on NSE/BSE typically costs 0.1–0.3% per trade
(brokerage + STT + exchange charges + impact cost on mid-caps). Over 12 months with ~5–8 trades
per rebalance, total annual friction is roughly 1–2%. Factor this into return expectations.
    """)

    st.divider()
    st.subheader("Metric Reference")
    st.markdown("""
| Metric | Formula | Interpretation |
|---|---|---|
| **12-1 Return** | (Price 21 days ago / Price 252 days ago) − 1 | Core momentum signal — skips last month to avoid short-term reversal |
| **12M Return** | (Current Price / Price 252 days ago) − 1 | Full 12-month return including last month — for reference |
| **Ann. Volatility** | Daily log-return std × √252 (last 252 days) | How erratically the stock moves — lower is smoother |
| **Risk-Adj Score** | 12-1 Return / Ann. Volatility | Reward per unit of risk — higher means smoother, more reliable trend |
| **Momentum Score** | Same as 12-1 Return | Used for Classic and Dual strategies |
| **52W High (₹)** | Max closing price over the past 252 trading days | Cross-check reference — verify against your broker or Yahoo Finance |
| **Gap from 52W High** | (Current Price / 52-Week High) − 1 | % below 52-week high. **0.00% = stock is AT its 52-week high** (strongest breakout signal). −2.34% means the stock is 2.34% below its 52-week high. Always ≤ 0 by construction. |
| **Weight** | Risk-Adj Score / Sum of scores (risk_adjusted) or Equal 1/15 (others) | Portfolio allocation percentage |
| **Allocated (₹)** | Weight × Total Capital | Rupee amount to invest in each stock |
| **Shares** | Floor(Allocated / CMP) | Whole shares to buy (rounded down) |
    """)


def render_walkthrough_tab() -> None:
    st.header("How to Use This Tool")

    st.subheader("Overview")
    st.markdown("""
This tool ranks the top 15 momentum stocks from the NIFTY 500 universe each month and tells you
exactly what to buy, hold, and sell. It is designed for **monthly rebalancing** — run it once at
the end of each month, act on the output, and repeat.
    """)

    st.divider()
    st.subheader("Step-by-Step: First Run")
    st.markdown("""
**Step 1 — Pick a strategy**
Read the strategy cards at the top. If you are unsure, start with **Risk-Adjusted Momentum** —
it has the best track record across varied market conditions.

**Step 2 — Check the Market Regime panel**
This loads automatically. It compares Nifty 50's current price to its 200-day moving average.
- Green (UPTREND) → conditions are favourable. Proceed.
- Red (DOWNTREND) → momentum tends to underperform. Consider reducing position sizes by 50%
  or waiting for the signal to flip green.
- For Dual Momentum: if you see a **CASH SIGNAL**, do not deploy. Move to liquid funds.

**Step 3 — Enter your capital**
Enter the total rupee amount you want to invest across the 15 stocks. The tool calculates
individual stock allocations automatically.

**Step 4 — Click Run Strategy**
First run takes 1–2 minutes (downloading ~15 months of price data for 500 stocks).
Subsequent runs within the same hour are near-instant (data is cached).

**Step 5 — Read the results**
You'll see a ranked table with 15 stocks. Each stock shows its momentum score, return,
volatility, suggested allocation, and approximate number of shares to buy.

**Step 6 — Save your run**
Click **Save Run & Download History**. This downloads a `momentum_history.json` file.
Keep this file — upload it next month to get rebalancing actions and performance tracking.
    """)

    st.divider()
    st.subheader("Step-by-Step: Monthly Rebalancing")
    st.markdown("""
**Do this on the last trading day of each month, after market close.**

1. Open the app at [pick-momentum.streamlit.app](https://pick-momentum.streamlit.app/)
2. Upload your `momentum_history.json` from last month in the **Portfolio History** section
3. Select the same strategy you used last month
4. Enter your current capital (adjust if you've added or withdrawn funds)
5. Click **Run Strategy**
6. Review the **Last Portfolio Performance** section — see how last month's picks did vs Nifty
7. Review the **Rebalancing Actions** section:
   - `NEW` stocks → place buy orders
   - `HOLD` stocks → no action needed
   - `EXIT` stocks → place sell orders
8. Place all orders at **market open on the first trading day of the new month**
9. Click **Save Run & Download History** and save the new file (replaces your old one)
    """)

    st.divider()
    st.subheader("Understanding the Results Table")
    st.markdown("""
| Column | What it means | What to look for |
|---|---|---|
| **#** | Rank by strategy score | Lower rank = stronger signal |
| **Action** | NEW / HOLD / EXIT | Your rebalancing instruction |
| **Symbol** | NSE ticker | — |
| **12-1 Return** | Momentum over past 11 months | Higher = stronger trend |
| **12M Return** | Full 12-month return | Compare to 12-1 for last-month effect |
| **Ann. Vol** | Annualised volatility | Lower = smoother trend |
| **Risk-Adj Score** | Return ÷ volatility | The core ranking metric for Risk-Adjusted strategy |
| **52W High (₹)** | Highest price over the past year | Verify against your broker — used only in 52-Week High strategy |
| **Gap from 52W High** | % below 52-week high | 0.00% = at its 52W high (strongest signal); shown only in 52-Week High strategy |
| **Weight** | % of capital allocated | Higher weight = stronger signal |
| **Allocated (₹)** | Rupee amount to deploy | Divide by share price for quantity |
| **Shares** | Whole shares to buy | Already calculated for you |
| **CMP (₹)** | Current market price | Use as reference for order placement |
    """)

    st.divider()
    st.subheader("Understanding the Charts")
    st.markdown("""
**Score Bar Chart** — Shows the ranking signal for each stock. Longer green bar = stronger
momentum. Use this to quickly see how concentrated or spread out the signals are.

**Capital Allocation Donut** — Shows how capital is distributed. Risk-Adjusted Momentum uses
score-weighted allocation (higher risk-adj score → larger slice); all other strategies show equal slices.

**Return vs Volatility Scatter** — The ideal stock is top-left (high return, low volatility).
Bubble size = allocation. Stocks toward the top-left with large bubbles are the highest-
conviction picks.

**Sector Allocation Bar** — Shows concentration by sector. If one sector dominates (e.g., 6 of
15 stocks are IT), be aware you're taking a sector bet, not just a momentum bet.
    """)

    st.divider()
    st.subheader("FAQs")
    st.markdown("""
**Q: What if the NSE data fails to load?**
Download `ind_nifty500list.csv` from nseindia.com and use the upload fallback.

**Q: The app is slow on first run — is that normal?**
Yes. Downloading 15 months of price data for ~490 stocks takes 1–2 minutes. After that,
data is cached for 1 hour — re-running within the hour is instant.

**Q: Should I use the same strategy every month?**
Yes. Switching strategies monthly defeats the purpose of systematic investing. Pick one
and stick with it for at least 6–12 months to evaluate it properly.

**Q: What if fewer than 15 stocks pass the filters?**
This can happen in broad market downturns (most stocks below 200-DMA). The tool will show
however many pass. In this case, consider not deploying or reducing capital.

**Q: Can I run multiple strategies simultaneously with different capital pools?**
Yes — each strategy produces its own results and its own history file. Use separate
`momentum_history_[strategy].json` filenames to keep them distinct.

**Q: When exactly should I place orders?**
At market open on the first trading day of the month. Avoid placing orders in the last
30 minutes of the rebalancing day — impact cost is higher near close.
    """)


# ── Like counter & Feedback ───────────────────────────────────────────────────

_COUNT_NS  = "pick-momentum"
_COUNT_KEY = "likes"
_COUNTER_BASE = "https://api.counterapi.dev/v1"


@st.cache_data(ttl=60)
def _fetch_like_count():
    """Return current like count from counterapi.dev, or None on failure."""
    try:
        r = requests.get(
            f"{_COUNTER_BASE}/{_COUNT_NS}/{_COUNT_KEY}",
            timeout=3,
        )
        if r.ok:
            return int(r.json().get("count", 0))
    except Exception:
        pass
    return None


def _do_like():
    """Increment like count; bust cache so next read reflects new value."""
    try:
        r = requests.get(
            f"{_COUNTER_BASE}/{_COUNT_NS}/{_COUNT_KEY}/up",
            timeout=3,
        )
        if r.ok:
            _fetch_like_count.clear()
            return int(r.json().get("count", 0))
    except Exception:
        pass
    return None


def _send_feedback_email(name, email, message):
    """
    Send feedback via Gmail SMTP.
    Returns True on success, None if secrets not configured, raises on SMTP error.

    Setup (one-time):
      1. Enable 2-Step Verification on durgesh.investing@gmail.com
      2. Google Account > Security > App Passwords → generate a 16-char password
      3. Add to .streamlit/secrets.toml:
             [feedback]
             gmail_app_password = "xxxx xxxx xxxx xxxx"
         AND add the same secret in Streamlit Cloud dashboard (app settings → Secrets).
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    try:
        app_pwd = st.secrets["feedback"]["gmail_app_password"]
    except Exception:
        return None  # secrets not yet configured → caller will show mailto fallback

    addr = "durgesh.investing@gmail.com"
    msg  = MIMEMultipart()
    msg["From"]    = addr
    msg["To"]      = addr
    msg["Subject"] = f"[Momentum Tool] Feedback from {name or 'Anonymous'}"
    body = (
        f"Name:    {name  or '—'}\n"
        f"Email:   {email or '—'}\n\n"
        f"{message}\n\n"
        "— via pick-momentum.streamlit.app"
    )
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP("smtp.gmail.com", 587) as srv:
        srv.starttls()
        srv.login(addr, app_pwd)
        srv.send_message(msg)
    return True


def render_top_actions():
    """Like counter + feedback popover — placed in the top-right column."""
    import urllib.parse

    liked = st.session_state.get("liked", False)

    # ── Like button ───────────────────────────────────────────────────────────
    count = _fetch_like_count()
    if count is not None:
        label = f"{'❤️' if liked else '🤍'}  {count:,} likes"
    else:
        label = "❤️ Liked!" if liked else "🤍 Like"

    if st.button(label, key="like_btn", disabled=liked, use_container_width=True,
                 help="Found this useful? Give it a like!"):
        _do_like()
        st.session_state["liked"] = True
        st.rerun()

    # ── Feedback popover ──────────────────────────────────────────────────────
    with st.popover("💬 Feedback", use_container_width=True):
        st.markdown("**Share suggestions or report issues**")
        f_name  = st.text_input("Your name (optional)", key="fb_name")
        f_email = st.text_input("Your email (optional)", key="fb_email",
                                placeholder="if you'd like a reply")
        f_msg   = st.text_area("Message *", key="fb_msg", height=130,
                               placeholder="Feature ideas, bugs, questions…")

        if st.button("Send Feedback", key="fb_submit", type="primary"):
            if not f_msg.strip():
                st.warning("Please write a message before sending.")
            else:
                try:
                    result = _send_feedback_email(f_name, f_email, f_msg.strip())
                except Exception as exc:
                    st.error(f"Could not send: {exc}")
                    result = None

                if result is True:
                    st.success("Sent! Thank you for the feedback.")
                else:
                    # SMTP not configured — open user's mail client instead
                    subj = urllib.parse.quote(
                        f"[Momentum Tool] Feedback from {f_name or 'a user'}"
                    )
                    body_enc = urllib.parse.quote(f_msg.strip())
                    mailto = (
                        f"mailto:durgesh.investing@gmail.com"
                        f"?subject={subj}&body={body_enc}"
                    )
                    st.markdown(
                        f'<a href="{mailto}">📧 Open in your email app to send</a>',
                        unsafe_allow_html=True,
                    )
                    st.caption("Or email directly: durgesh.investing@gmail.com")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    hdr_l, hdr_r = st.columns([5, 2])
    with hdr_l:
        st.title("Momentum Portfolio Tool")
        st.caption("NIFTY 500 · 4 research-backed strategies · Monthly rebalancing")
    with hdr_r:
        st.write("")   # push buttons down to align with title baseline
        render_top_actions()

    tab_tool, tab_guide, tab_how = st.tabs(["Portfolio Tool", "Strategy Guide", "How to Use"])

    with tab_guide:
        render_strategy_guide_tab()

    with tab_how:
        render_walkthrough_tab()

    with tab_tool:
        st.divider()

        # 1. Strategy selection
        strategy_key = render_strategy_selector()
        st.divider()

        # 2. Market regime
        st.subheader("Market Regime — Nifty 50 vs 200-Day SMA")
        with st.spinner("Loading market data…"):
            trend = load_nifty_trend()
        render_trend_panel(trend, strategy_key)
        st.divider()

        # 3. Portfolio history — upload
        st.subheader("Portfolio History")
        history: list = st.session_state.get("history", [])

        col_up, col_info = st.columns([2, 4])
        with col_up:
            uploaded = st.file_uploader(
                "Upload history file (from previous run)",
                type="json", key="history_upload",
                help="Upload the history.json you downloaded after your last run to enable rebalancing comparison.",
            )
            if uploaded:
                history = load_history_from_upload(uploaded)
                st.session_state["history"] = history
                st.success(f"Loaded {len(history)} past run(s).")
        with col_info:
            if history:
                last_strat_run = get_last_run(history, strategy_key)
                runs_for_strat = [r for r in history if r.get("strategy") == strategy_key]
                st.info(
                    f"History loaded: **{len(history)}** total run(s), "
                    f"**{len(runs_for_strat)}** with current strategy. "
                    + (f"Last run: **{last_strat_run['date']}**" if last_strat_run else "No prior run for this strategy.")
                )
            else:
                st.info("No history loaded. First run? Save after running to enable next month's rebalancing.")

        st.divider()

        # 4. Run controls
        st.subheader("Run Strategy")
        c_cap, c_btn, _ = st.columns([2, 1, 3])
        with c_cap:
            capital = st.number_input("Total Capital (₹)",
                                      min_value=10_000, max_value=50_000_000,
                                      value=500_000, step=10_000, format="%d")
        with c_btn:
            st.write("")
            run = st.button("Run Strategy", type="primary", use_container_width=True)

        if not run:
            st.info("Set your capital and click **Run Strategy**.")
            return

        # 5. Execution
        progress = st.progress(0, text="Starting…")

        progress.progress(3, text="Fetching NIFTY 500 constituents…")
        constituents, err = load_nifty500_constituents()

        if constituents is None:
            progress.empty()
            st.error(f"Failed to load NIFTY 500 list: {err}")
            uploaded_csv = st.file_uploader("Upload ind_nifty500list.csv", type="csv")
            if not uploaded_csv:
                return
            df = pd.read_csv(uploaded_csv)
            df.columns = df.columns.str.strip()
            df = df.rename(columns={"Company Name": "company", "Industry": "sector",
                                     "Symbol": "symbol", "Series": "series"})
            df = df[df["series"].str.strip() == "EQ"].copy()
            df["symbol"] = df["symbol"].str.strip()
            df["ticker"] = df["symbol"] + ".NS"
            constituents = df[["symbol", "company", "sector", "ticker"]]

        st.success(f"Loaded **{len(constituents)}** stocks.")

        tickers = tuple(constituents["ticker"].tolist())
        progress.progress(8, text=f"Downloading price data for {len(tickers)} stocks…")
        close_df = load_price_data(tickers)

        if close_df is None or close_df.empty:
            progress.empty()
            st.error("Price data download failed.")
            return

        st.success(f"Price data ready for **{close_df.shape[1]}** tickers.")

        results = run_strategy(close_df, constituents, strategy_key, capital, progress)
        progress.empty()

        if results.empty:
            st.warning(
                "No stocks passed all filters. "
                + ("Try a different strategy, or " if strategy_key == "dual" else "")
                + "check if the market is in a broad downtrend."
            )
            return

        nifty_price = trend["price"] if trend else 0.0
        last_run    = get_last_run(history, strategy_key)

        st.divider()

        if last_run:
            render_performance(last_run, close_df, nifty_price)
            st.divider()

        render_rebalancing(results, last_run, strategy_key)
        st.divider()
        render_results(results, strategy_key, last_run)

        # 6. Save & download
        st.divider()
        run_date    = datetime.today().strftime("%Y-%m-%d")
        new_history = append_run(history, results, strategy_key, run_date, nifty_price)

        c_save, c_dl, _ = st.columns([2, 2, 2])
        with c_save:
            st.download_button(
                label="Save Run & Download History",
                data=history_to_json(new_history),
                file_name="momentum_history.json",
                mime="application/json",
                use_container_width=True,
                type="primary",
                help="Download this file and upload it next month to see rebalancing actions and performance.",
            )
            if st.button("Save to session (this tab only)", use_container_width=True):
                st.session_state["history"] = new_history
                st.success("Saved. Upload the history file next visit to persist across sessions.")

        with c_dl:
            csv_out = results[[
                "rank", "symbol", "company", "sector",
                "score", "ret_12_1", "ret_12m", "ann_vol",
                "pct_52wk_hi", "weight", "allocation", "shares", "price",
            ]].copy()
            for col in ["score", "ret_12_1", "ret_12m", "ann_vol", "pct_52wk_hi", "weight"]:
                csv_out[col] = csv_out[col].map("{:.6f}".format)
            st.download_button(
                label="Download Portfolio CSV",
                data=csv_out.to_csv(index=False),
                file_name=f"momentum_{strategy_key}_{run_date}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.caption(
            f"Data: Yahoo Finance. Strategy: {STRATEGIES[strategy_key]['name']}. "
            f"Generated: {datetime.today().strftime('%d %b %Y %H:%M')}. Not investment advice."
        )


if __name__ == "__main__":
    main()
