"""
Generate social-media-ready screenshots of the Momentum Portfolio Tool.
Output: social_screenshots/ folder (PNG, lossless)

Sizes:
  - LinkedIn / Twitter post: 1200 x 628
  - Instagram square:        1080 x 1080
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# ── Paths & output dir ────────────────────────────────────────────────────────
OUT   = "C:/Users/Durgesh/momentum-dashboard/social_screenshots"
os.makedirs(OUT, exist_ok=True)

FONT_REG  = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_LITE = "C:/Windows/Fonts/segoeuil.ttf"

# ── Colour palette (matches app) ──────────────────────────────────────────────
BG      = (15,  23,  42)    # #0f172a  dark navy
NAVY2   = (30,  41,  59)    # #1e293b
NAVY3   = (51,  65,  85)    # #334155
GREEN   = (34, 197,  94)    # #22c55e
GREEN_L = (220, 252, 231)   # #dcfce7
BLUE    = (59, 130, 246)    # #3b82f6
BLUE_L  = (239, 246, 255)   # #eff6ff
GOLD    = (245, 158,  11)   # #f59e0b
GOLD_L  = (254, 243, 199)   # #fef3c7
RED     = (239,  68,  68)   # #ef4444
RED_L   = (254, 226, 226)   # #fee2e2
TEXT    = (15,  23,  42)    # near-black
MUTED   = (100, 116, 135)   # #64748b
LIGHT   = (248, 250, 252)   # #f8fafc
BORDER  = (226, 232, 240)   # #e2e8f0
WHITE   = (255, 255, 255)

# ── Font cache ────────────────────────────────────────────────────────────────
_fcache = {}
def F(size, bold=False, lite=False):
    path = FONT_BOLD if bold else (FONT_LITE if lite else FONT_REG)
    key  = (path, size)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(path, size)
    return _fcache[key]


# ── Draw helpers ──────────────────────────────────────────────────────────────

def rounded_rect(draw, xy, radius, fill, outline=None, outline_w=1):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill,
                           outline=outline, width=outline_w)


def text_w(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]


def text_h(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]


def centered_text(draw, text, font, color, cx, cy):
    w = text_w(draw, text, font)
    h = text_h(draw, text, font)
    draw.text((cx - w // 2, cy - h // 2), text, font=font, fill=color)


def badge(draw, text, x, y, fg, bg, font, pad_x=10, pad_y=4, radius=4):
    """Draw a colored badge/pill."""
    w = text_w(draw, text, font) + 2 * pad_x
    h = text_h(draw, text, font) + 2 * pad_y
    rounded_rect(draw, (x, y, x + w, y + h), radius, bg)
    draw.text((x + pad_x, y + pad_y), text, font=font, fill=fg)
    return w, h


def footer_bar(img, draw, W, H, url="pick-momentum.streamlit.app"):
    """Navy footer strip with URL."""
    fh = 36
    draw.rectangle([0, H - fh, W, H], fill=BG)
    draw.line([0, H - fh, W, H - fh], fill=NAVY3, width=1)
    parts = [
        ("linkedin.com/in/durgeshh/",          GREEN),
        ("   ·   ",                             NAVY3),
        (url,                                   GREEN),
        ("   ·   ",                             NAVY3),
        ("github.com/tooweeknd/momentum-dashboard", GREEN),
    ]
    total = sum(text_w(draw, p, F(13)) for p, _ in parts)
    x = (W - total) // 2
    y = H - fh + (fh - text_h(draw, "A", F(13))) // 2
    for part, col in parts:
        draw.text((x, y), part, font=F(13), fill=col)
        x += text_w(draw, part, F(13))


def header_bar(img, draw, W, label="MOMENTUM PORTFOLIO TOOL"):
    """Thin dark header strip."""
    hh = 40
    draw.rectangle([0, 0, W, hh], fill=BG)
    draw.text((20, 12), label, font=F(13, bold=True), fill=GREEN)
    url = "pick-momentum.streamlit.app"
    uw  = text_w(draw, url, F(12))
    draw.text((W - uw - 20, 14), url, font=F(12), fill=MUTED)


# ── Screenshot 1: Strategy Selector overview ──────────────────────────────────

def shot_strategy_selector():
    W, H = 1200, 628
    img  = Image.new("RGB", (W, H), LIGHT)
    draw = ImageDraw.Draw(img)

    header_bar(img, draw, W)

    # Title area
    draw.text((40, 55), "Momentum Portfolio Tool", font=F(28, bold=True), fill=TEXT)
    draw.text((40, 92), "NIFTY 500  ·  4 research-backed strategies  ·  Monthly rebalancing",
              font=F(14), fill=MUTED)

    # Section label
    draw.text((40, 130), "Select a Strategy", font=F(18, bold=True), fill=TEXT)
    draw.line([40, 158, W - 40, 158], fill=GREEN, width=2)

    strategies = [
        ("📈", "Classic Momentum",      "High",   GOLD,  "12-1 return · Equal weight",
         "Jegadeesh & Titman, 1993", "The foundational momentum paper.\nTop 15 NIFTY 500 stocks by 12M return."),
        ("⚖️", "Risk-Adjusted\nMomentum", "Medium", GREEN, "Return÷Vol · Return-weighted",
         "Barroso & Santa-Clara, 2015", "Rewards smooth uptrends.\nReduces crash risk by ~80%. Recommended."),
        ("🛡", "Dual Momentum",          "Low-Med", BLUE, "Relative+Absolute · Cash signal",
         "Gary Antonacci, 2014", "Full cash exit in bear markets.\nMinimises drawdown."),
        ("🎯", "52-Week High",           "Medium", GOLD,  "Price÷52W High · Equal weight",
         "George & Hwang, 2004", "Captures breakout dynamics.\nDifferent stocks from return strategies."),
    ]

    card_w  = (W - 80 - 3 * 16) // 4
    card_h  = 380
    x_start = 40
    y_start = 168

    for i, (emoji, name, risk, risk_col, signal, paper, desc) in enumerate(strategies):
        cx = x_start + i * (card_w + 16)
        cy = y_start

        # Card background
        rounded_rect(draw, (cx, cy, cx + card_w, cy + card_h), 10,
                     WHITE, outline=BORDER, outline_w=1)

        # Top accent bar
        rounded_rect(draw, (cx, cy, cx + card_w, cy + 6), 10, GREEN)
        draw.rectangle([cx, cy + 3, cx + card_w, cy + 6], fill=GREEN)

        # Emoji
        draw.text((cx + 16, cy + 18), emoji, font=F(28), fill=TEXT)

        # Strategy name
        for j, line in enumerate(name.split("\n")):
            draw.text((cx + 16, cy + 56 + j * 24), line,
                      font=F(15, bold=True), fill=TEXT)

        # Risk badge
        risk_bg = (GREEN_L if risk == "Low-Med" else
                   (GOLD_L if risk == "Medium" else RED_L))
        badge(draw, f"● {risk}", cx + 16, cy + 106, risk_col, risk_bg, F(11, bold=True))

        # Divider
        draw.line([cx + 12, cy + 134, cx + card_w - 12, cy + 134],
                  fill=BORDER, width=1)

        # Signal
        draw.text((cx + 16, cy + 144), "Signal", font=F(10, bold=True), fill=MUTED)
        draw.text((cx + 16, cy + 158), signal, font=F(11), fill=TEXT)

        # Paper
        draw.text((cx + 16, cy + 192), "Research", font=F(10, bold=True), fill=MUTED)
        draw.text((cx + 16, cy + 206), paper, font=F(10), fill=MUTED)

        # Description
        draw.line([cx + 12, cy + 230, cx + card_w - 12, cy + 230],
                  fill=BORDER, width=1)
        for j, line in enumerate(desc.split("\n")):
            draw.text((cx + 16, cy + 240 + j * 18), line, font=F(12), fill=TEXT)

        # Select button
        btn_y = cy + card_h - 48
        rounded_rect(draw, (cx + 16, btn_y, cx + card_w - 16, btn_y + 32),
                     6, GREEN if i == 1 else NAVY2)
        btn_text = "● Selected" if i == 1 else "Select"
        btn_col  = BG if i == 1 else WHITE
        bw = text_w(draw, btn_text, F(12, bold=True))
        draw.text((cx + (card_w - bw) // 2, btn_y + 8),
                  btn_text, font=F(12, bold=True), fill=btn_col)

    footer_bar(img, draw, W, H)
    img.save(f"{OUT}/01_strategy_selector.png")
    print("Saved: 01_strategy_selector.png")


# ── Screenshot 2: Market Regime + Run panel ───────────────────────────────────

def shot_market_regime():
    W, H = 1200, 628
    img  = Image.new("RGB", (W, H), LIGHT)
    draw = ImageDraw.Draw(img)

    header_bar(img, draw, W)

    draw.text((40, 55), "Market Regime — Nifty 50 vs 200-Day SMA",
              font=F(22, bold=True), fill=TEXT)
    draw.line([40, 88, W - 40, 88], fill=GREEN, width=2)

    # ── Regime panel ─────────────────────────────────────────────────────────
    px, py, pw, ph = 40, 100, 560, 220
    rounded_rect(draw, (px, py, px + pw, py + ph), 10, BG, outline=GREEN, outline_w=2)
    draw.rectangle([px, py, px + pw, py + 4], fill=GREEN)

    draw.text((px + 20, py + 18), "MARKET REGIME", font=F(11, bold=True), fill=GREEN)
    draw.text((px + 20, py + 50), "▲  UPTREND", font=F(32, bold=True), fill=GREEN)
    draw.text((px + 20, py + 96),
              "Nifty 50 is trading ABOVE its 200-day",
              font=F(13), fill=(148, 163, 184))
    draw.text((px + 20, py + 116),
              "moving average.  Momentum conditions",
              font=F(13), fill=(148, 163, 184))
    draw.text((px + 20, py + 136),
              "are FAVOURABLE — deploy capital as planned.",
              font=F(13), fill=(148, 163, 184))

    # Nifty stat
    draw.line([px + 20, py + 164, px + pw - 20, py + 164], fill=NAVY3, width=1)
    draw.text((px + 20, py + 174), "Nifty 50", font=F(11, bold=True), fill=MUTED)
    draw.text((px + 20, py + 192), "24,315", font=F(18, bold=True), fill=WHITE)
    draw.text((px + 160, py + 174), "200-Day SMA", font=F(11, bold=True), fill=MUTED)
    draw.text((px + 160, py + 192), "22,841", font=F(18, bold=True), fill=MUTED)
    draw.text((px + 340, py + 174), "Above by", font=F(11, bold=True), fill=MUTED)
    draw.text((px + 340, py + 192), "+6.4%", font=F(18, bold=True), fill=GREEN)

    # ── Strategy info panel ───────────────────────────────────────────────────
    sp2x, sp2y = 620, 100
    sp2w, sp2h = 540, 220
    rounded_rect(draw, (sp2x, sp2y, sp2x + sp2w, sp2y + sp2h),
                 10, WHITE, outline=BORDER, outline_w=1)
    draw.rectangle([sp2x, sp2y, sp2x + sp2w, sp2y + 4], fill=BLUE)

    draw.text((sp2x + 20, sp2y + 18), "ACTIVE STRATEGY",
              font=F(11, bold=True), fill=BLUE)
    draw.text((sp2x + 20, sp2y + 48), "Risk-Adjusted Momentum",
              font=F(22, bold=True), fill=TEXT)
    badge(draw, "★ Recommended", sp2x + 20, sp2y + 84,
          GREEN, GREEN_L, F(11, bold=True), pad_x=8)

    draw.line([sp2x + 20, sp2y + 118, sp2x + sp2w - 20, sp2y + 118],
              fill=BORDER, width=1)

    cols = [("Research", "Barroso & Santa-Clara, 2015"),
            ("Signal",   "12-1 Return ÷ Annualised Vol"),
            ("Alloc",    "Return-weighted"),
            ("Risk",     "Medium")]
    for idx, (lbl, val) in enumerate(cols):
        col_x = sp2x + 20 + (idx % 2) * 260
        col_y = sp2y + 132 + (idx // 2) * 38
        draw.text((col_x, col_y), lbl, font=F(10, bold=True), fill=MUTED)
        draw.text((col_x, col_y + 15), val, font=F(12), fill=TEXT)

    # ── Capital input ─────────────────────────────────────────────────────────
    iy = 340
    draw.text((40, iy), "Total Capital (₹)", font=F(14, bold=True), fill=TEXT)
    rounded_rect(draw, (40, iy + 28, 340, iy + 62), 6, WHITE, outline=BORDER, outline_w=2)
    draw.text((56, iy + 40), "5,00,000", font=F(16), fill=TEXT)

    rounded_rect(draw, (360, iy + 28, 560, iy + 62), 6, GREEN)
    cw = text_w(draw, "▶  Run Strategy", F(15, bold=True))
    draw.text((360 + (200 - cw) // 2, iy + 40),
              "▶  Run Strategy", font=F(15, bold=True), fill=BG)

    # ── Mini chart sketch ─────────────────────────────────────────────────────
    cx0, cy0 = 620, 340
    cw2, ch2 = 540, 240
    rounded_rect(draw, (cx0, cy0, cx0 + cw2, cy0 + ch2), 10, WHITE, outline=BORDER)
    draw.text((cx0 + 16, cy0 + 12), "Nifty 50 — 12-Month Price vs 200-DMA",
              font=F(11, bold=True), fill=TEXT)

    # Draw a simple price line chart
    import random
    random.seed(42)
    prices = [19500]
    for _ in range(59):
        prices.append(prices[-1] * (1 + random.gauss(0.003, 0.012)))
    # 200 DMA approximation — start lower
    sma_val = 22841
    sma_start = sma_val * 0.93

    chart_l, chart_r = cx0 + 20, cx0 + cw2 - 20
    chart_t, chart_b = cy0 + 38,  cy0 + ch2 - 24
    chart_w = chart_r - chart_l
    chart_h = chart_b - chart_t

    min_p, max_p = min(prices) * 0.97, max(prices) * 1.02

    def px_pos(i, val):
        x = chart_l + int(i / (len(prices) - 1) * chart_w)
        y = chart_b - int((val - min_p) / (max_p - min_p) * chart_h)
        return x, y

    # SMA line (dashed grey)
    sma_points = [sma_start + (sma_val - sma_start) * i / 59 for i in range(60)]
    for i in range(0, 59, 2):
        x0s, y0s = px_pos(i, sma_points[i])
        x1s, y1s = px_pos(i + 1, sma_points[i + 1])
        draw.line([x0s, y0s, x1s, y1s], fill=MUTED, width=1)

    # Price line (green)
    pts = [px_pos(i, prices[i]) for i in range(60)]
    for i in range(59):
        draw.line([pts[i], pts[i + 1]], fill=GREEN, width=2)

    # Labels
    last_x, last_y = pts[-1]
    badge(draw, "Price", last_x - 48, last_y - 10, GREEN, GREEN_L, F(9))
    sma_lx, sma_ly = px_pos(55, sma_points[55])
    draw.text((sma_lx - 30, sma_ly - 18), "200-DMA", font=F(9), fill=MUTED)

    footer_bar(img, draw, W, H)
    img.save(f"{OUT}/02_market_regime.png")
    print("Saved: 02_market_regime.png")


# ── Screenshot 3: Portfolio Results table ─────────────────────────────────────

def shot_results_table():
    W, H = 1200, 628
    img  = Image.new("RGB", (W, H), LIGHT)
    draw = ImageDraw.Draw(img)

    header_bar(img, draw, W)

    draw.text((40, 55), "Portfolio Results — Risk-Adjusted Momentum",
              font=F(22, bold=True), fill=TEXT)
    draw.text((40, 86), "Top 15 stocks from NIFTY 500  ·  Capital: ₹5,00,000  ·  Run: 30 Apr 2026",
              font=F(13), fill=MUTED)
    draw.line([40, 110, W - 40, 110], fill=GREEN, width=2)

    # Column headers
    cols  = ["#", "Action", "Symbol", "Company",           "Sector",        "Score", "12-1 Ret", "Ann.Vol", "Weight", "Alloc (₹)", "Shares", "CMP (₹)"]
    widths = [28,  68,       80,       190,                  120,             52,      70,          60,        58,       80,          52,       80]

    rows_data = [
        (1,  "HOLD", "RELIANCE",  "Reliance Industries", "Energy",        "3.12", "+62.4%", "20.1%", "9.2%",  "46,100", "16", "2,881"),
        (2,  "NEW",  "BAJFINANCE","Bajaj Finance",       "Fin. Services", "2.87", "+58.3%", "20.3%", "8.6%",  "43,000", "18", "2,388"),
        (3,  "HOLD", "HDFCBANK",  "HDFC Bank",           "Fin. Services", "2.54", "+51.2%", "20.2%", "7.6%",  "38,000", "22", "1,727"),
        (4,  "NEW",  "LTIM",      "LTIMindtree",         "IT",            "2.41", "+48.7%", "20.2%", "7.2%",  "36,000",  "4", "9,001"),
        (5,  "HOLD", "TITAN",     "Titan Company",       "Consumer",      "2.28", "+46.0%", "20.2%", "6.8%",  "34,000", "11", "3,090"),
        (6,  "HOLD", "ADANIENT",  "Adani Enterprises",   "Diversified",   "2.15", "+43.5%", "20.2%", "6.5%",  "32,300",  "9", "3,589"),
        (7,  "NEW",  "TATAPOWER", "Tata Power",          "Utilities",     "2.01", "+40.7%", "20.2%", "6.1%",  "30,300", "71",  "426"),
        (8,  "HOLD", "ZOMATO",    "Zomato",              "Consumer",      "1.94", "+39.2%", "20.2%", "5.9%",  "29,400",  "99",  "297"),
        (9,  "HOLD", "PIIND",     "PI Industries",       "Chemicals",     "1.87", "+37.8%", "20.2%", "5.7%",  "28,200",  "6", "4,700"),
        (10, "HOLD", "PERSISTENT","Persistent Systems",  "IT",            "1.79", "+36.2%", "20.2%", "5.4%",  "27,100",  "3", "9,033"),
        (11, "NEW",  "HINDUNILVR","Hindustan Unilever",  "Consumer",      "1.72", "+34.8%", "20.2%", "5.2%",  "25,800", "10", "2,580"),
        (12, "HOLD", "CIPLA",     "Cipla",               "Healthcare",    "1.65", "+33.4%", "20.2%", "5.0%",  "24,800", "17", "1,459"),
        (13, "HOLD", "ASTRAL",    "Astral",              "Materials",     "1.58", "+32.0%", "20.2%", "4.8%",  "23,900", "12", "1,991"),
        (14, "HOLD", "ABCAPITAL", "Aditya Birla Capital", "Fin. Services","1.51", "+30.5%", "20.2%", "4.6%",  "22,800", "104",  "219"),
        (15, "NEW",  "CAMS",      "CAMS",                "Fin. Services", "1.44", "+29.1%", "20.2%", "4.3%",  "21,500",  "5", "4,300"),
    ]

    row_h  = 28
    tbl_x  = 40
    tbl_y  = 120
    tbl_w  = W - 80

    # Header row
    rounded_rect(draw, (tbl_x, tbl_y, tbl_x + tbl_w, tbl_y + row_h), 6, BG)
    x = tbl_x
    for col, w in zip(cols, widths):
        cw_ = text_w(draw, col, F(10, bold=True))
        draw.text((x + (w - cw_) // 2, tbl_y + 8), col, font=F(10, bold=True), fill=WHITE)
        x += w

    # Data rows (show 12 rows to fit)
    action_cfg = {
        "NEW":  (GREEN, GREEN_L, "NEW"),
        "HOLD": (BLUE,  BLUE_L,  "HOLD"),
        "EXIT": (RED,   RED_L,   "EXIT"),
    }

    for ridx, row in enumerate(rows_data[:12]):
        ry = tbl_y + (ridx + 1) * row_h
        row_bg = WHITE if ridx % 2 == 0 else LIGHT
        draw.rectangle([tbl_x, ry, tbl_x + tbl_w, ry + row_h - 1], fill=row_bg)

        num, action, sym, company, sector, score, ret12_1, vol, weight, alloc, shares, cmp = row
        values = [str(num), action, sym, company, sector, score, ret12_1, vol, weight, alloc, shares, cmp]

        x = tbl_x
        for vidx, (val, w) in enumerate(zip(values, widths)):
            if vidx == 1:  # Action badge
                fg, bg, lbl = action_cfg[val]
                bw2 = text_w(draw, lbl, F(9, bold=True)) + 10
                bh2 = row_h - 10
                bx  = x + (w - bw2) // 2
                by  = ry + 5
                rounded_rect(draw, (bx, by, bx + bw2, by + bh2), 3, bg)
                tw2 = text_w(draw, lbl, F(9, bold=True))
                draw.text((bx + (bw2 - tw2) // 2, by + 3), lbl, font=F(9, bold=True), fill=fg)
            elif vidx == 2:  # Symbol bold
                draw.text((x + 4, ry + 7), val, font=F(10, bold=True), fill=TEXT)
            elif vidx == 6:  # Return — green
                col_v = GREEN if val.startswith("+") else RED
                vw_ = text_w(draw, val, F(10))
                draw.text((x + w - vw_ - 4, ry + 7), val, font=F(10), fill=col_v)
            elif vidx in (0, 5, 7, 8, 9, 10, 11):  # right-align numbers
                vw_ = text_w(draw, val, F(10))
                draw.text((x + w - vw_ - 4, ry + 7), val, font=F(10), fill=TEXT)
            else:
                draw.text((x + 4, ry + 7), val, font=F(10), fill=TEXT)
            x += w

        # Row bottom border
        draw.line([tbl_x, ry + row_h - 1, tbl_x + tbl_w, ry + row_h - 1],
                  fill=BORDER, width=1)

    # Truncation note
    note_y = tbl_y + 13 * row_h + 6
    draw.text((tbl_x, note_y), "Showing 12 of 15 stocks  ·  Sample data for illustration",
              font=F(11), fill=MUTED)

    footer_bar(img, draw, W, H)
    img.save(f"{OUT}/03_results_table.png")
    print("Saved: 03_results_table.png")


# ── Screenshot 4: Rebalancing Actions ─────────────────────────────────────────

def shot_rebalancing():
    W, H = 1200, 628
    img  = Image.new("RGB", (W, H), LIGHT)
    draw = ImageDraw.Draw(img)

    header_bar(img, draw, W)

    draw.text((40, 55), "Monthly Rebalancing Actions",
              font=F(22, bold=True), fill=TEXT)
    draw.text((40, 86), "vs April 2026 portfolio  ·  Strategy: Risk-Adjusted Momentum",
              font=F(13), fill=MUTED)
    draw.line([40, 110, W - 40, 110], fill=GREEN, width=2)

    # Summary badges row
    badges = [("3  NEW", GREEN, GREEN_L), ("9  HOLD", BLUE, BLUE_L), ("3  EXIT", RED, RED_L)]
    bx = 40
    for label, fg, bg in badges:
        bw_, _ = badge(draw, label, bx, 122, fg, bg, F(14, bold=True), pad_x=16, pad_y=8, radius=6)
        bx += bw_ + 12

    # Performance vs Nifty mini-panel (right side)
    pp_x, pp_y, pp_w, pp_h = 720, 116, 440, 72
    rounded_rect(draw, (pp_x, pp_y, pp_x + pp_w, pp_y + pp_h), 8, WHITE, outline=BORDER)
    draw.text((pp_x + 14, pp_y + 10), "Last Portfolio vs Nifty 50",
              font=F(11, bold=True), fill=MUTED)
    draw.text((pp_x + 14, pp_y + 32), "+18.4%", font=F(22, bold=True), fill=GREEN)
    draw.text((pp_x + 110, pp_y + 32), "portfolio", font=F(12), fill=MUTED)
    draw.text((pp_x + 220, pp_y + 32), "+11.2%", font=F(22, bold=True), fill=MUTED)
    draw.text((pp_x + 316, pp_y + 32), "Nifty 50", font=F(12), fill=MUTED)
    badge(draw, "▲ +7.2% alpha", pp_x + 14, pp_y + 54, GREEN, GREEN_L, F(10, bold=True))

    # Table
    tbl_x  = 40
    tbl_y  = 208
    tbl_w  = W - 80
    row_h  = 38
    cols   = ["Action", "Symbol", "Company",              "Sector",        "12-1 Ret", "Allocated", "Shares", "CMP (₹)", "Change"]
    widths = [80,        88,       200,                    138,             80,          96,           64,       88,       120]

    rebal_rows = [
        ("NEW",  "BAJFINANCE", "Bajaj Finance",        "Fin. Services", "+58.3%",  "₹43,000",   "18",  "₹2,388",  "Added to portfolio"),
        ("NEW",  "LTIM",       "LTIMindtree",          "IT",            "+48.7%",  "₹36,000",    "4",  "₹9,001",  "Added to portfolio"),
        ("NEW",  "HINDUNILVR", "Hindustan Unilever",   "Consumer",      "+34.8%",  "₹25,800",   "10",  "₹2,580",  "Added to portfolio"),
        ("HOLD", "RELIANCE",   "Reliance Industries",  "Energy",        "+62.4%",  "₹46,100",   "16",  "₹2,881",  "↑ weight 7.1%→9.2%"),
        ("HOLD", "HDFCBANK",   "HDFC Bank",            "Fin. Services", "+51.2%",  "₹38,000",   "22",  "₹1,727",  "No change"),
        ("HOLD", "TITAN",      "Titan Company",        "Consumer",      "+46.0%",  "₹34,000",   "11",  "₹3,090",  "No change"),
        ("HOLD", "ADANIENT",   "Adani Enterprises",    "Diversified",   "+43.5%",  "₹32,300",    "9",  "₹3,589",  "↓ weight 7.8%→6.5%"),
        ("HOLD", "TATAPOWER",  "Tata Power",           "Utilities",     "+40.7%",  "₹30,300",   "71",  "₹426",    "No change"),
        ("HOLD", "ZOMATO",     "Zomato",               "Consumer",      "+39.2%",  "₹29,400",   "99",  "₹297",    "No change"),
        ("EXIT", "INFY",       "Infosys",              "IT",            "+12.1%",  "SELL ALL",   "—",  "₹1,621",  "Below threshold"),
        ("EXIT", "WIPRO",      "Wipro",                "IT",            "+8.4%",   "SELL ALL",   "—",  "₹312",    "Below threshold"),
        ("EXIT", "HCLTECH",    "HCL Technologies",     "IT",            "+7.2%",   "SELL ALL",   "—",  "₹1,847",  "Below threshold"),
    ]

    action_cfg = {
        "NEW":  (GREEN, GREEN_L),
        "HOLD": (BLUE,  BLUE_L),
        "EXIT": (RED,   RED_L),
    }

    # Header
    rounded_rect(draw, (tbl_x, tbl_y, tbl_x + tbl_w, tbl_y + 30), 6, BG)
    x = tbl_x
    for col, w in zip(cols, widths):
        cw_ = text_w(draw, col, F(10, bold=True))
        draw.text((x + (w - cw_) // 2, tbl_y + 8), col, font=F(10, bold=True), fill=WHITE)
        x += w

    for ridx, row in enumerate(rebal_rows):
        ry = tbl_y + 30 + ridx * row_h
        action = row[0]
        fg, bg = action_cfg[action]

        # Row bg — tint for action type
        tint = {
            "NEW":  (240, 253, 244),
            "HOLD": (WHITE),
            "EXIT": (255, 242, 242),
        }[action]
        row_bg = tint if ridx % 2 == 0 else (LIGHT if action == "HOLD" else tint)
        draw.rectangle([tbl_x, ry, tbl_x + tbl_w, ry + row_h - 1], fill=row_bg)

        values = list(row)
        x = tbl_x
        for vidx, (val, w) in enumerate(zip(values, widths)):
            if vidx == 0:  # Action badge
                bw2 = text_w(draw, val, F(10, bold=True)) + 12
                bh2 = row_h - 12
                bx_ = x + (w - bw2) // 2
                by_ = ry + 6
                rounded_rect(draw, (bx_, by_, bx_ + bw2, by_ + bh2), 4, bg)
                tw2 = text_w(draw, val, F(10, bold=True))
                draw.text((bx_ + (bw2 - tw2) // 2, by_ + 4), val, font=F(10, bold=True), fill=fg)
            elif vidx == 1:  # Symbol
                draw.text((x + 6, ry + 10), val, font=F(11, bold=True), fill=TEXT)
            elif vidx == 4:  # Return
                col_v = GREEN if val.startswith("+") else RED
                vw_   = text_w(draw, val, F(10))
                draw.text((x + w - vw_ - 6, ry + 10), val, font=F(10), fill=col_v)
            elif vidx == 8:  # Change note
                note_col = GREEN if "Added" in val else (RED if "Below" in val else MUTED)
                draw.text((x + 6, ry + 10), val, font=F(10), fill=note_col)
            else:
                draw.text((x + 6, ry + 10), val, font=F(10), fill=TEXT)
            x += w
        draw.line([tbl_x, ry + row_h - 1, tbl_x + tbl_w, ry + row_h - 1],
                  fill=BORDER, width=1)

    footer_bar(img, draw, W, H)
    img.save(f"{OUT}/04_rebalancing_actions.png")
    print("Saved: 04_rebalancing_actions.png")


# ── Screenshot 5: Charts (2x2 grid) ──────────────────────────────────────────

def shot_charts():
    W, H = 1200, 628
    img  = Image.new("RGB", (W, H), LIGHT)
    draw = ImageDraw.Draw(img)

    header_bar(img, draw, W)
    draw.text((40, 54), "Portfolio Analytics — Risk-Adjusted Momentum",
              font=F(20, bold=True), fill=TEXT)
    draw.line([40, 84, W - 40, 84], fill=GREEN, width=2)

    import math, random
    random.seed(7)

    cw2 = (W - 80 - 20) // 2
    ch2 = (H - 100 - 20) // 2
    positions = [(40, 92), (60 + cw2, 92), (40, 114 + ch2), (60 + cw2, 114 + ch2)]

    titles = [
        "Momentum Score by Stock",
        "Capital Allocation",
        "Return vs Volatility",
        "Sector Breakdown",
    ]

    stocks = ["RELIANCE", "BAJFINANCE", "HDFCBANK", "LTIM", "TITAN",
              "ADANIENT", "TATAPOWER", "ZOMATO", "PIIND", "PERSISTENT",
              "HINDUNILVR", "CIPLA", "ASTRAL", "ABCAPITAL", "CAMS"]
    scores = [3.12, 2.87, 2.54, 2.41, 2.28, 2.15, 2.01, 1.94, 1.87, 1.79,
              1.72, 1.65, 1.58, 1.51, 1.44]
    weights = [9.2, 8.6, 7.6, 7.2, 6.8, 6.5, 6.1, 5.9, 5.7, 5.4,
               5.2, 5.0, 4.8, 4.6, 4.3]

    # ── Chart 1: Horizontal bar chart (scores) ────────────────────────────────
    cx1, cy1 = positions[0]
    rounded_rect(draw, (cx1, cy1, cx1 + cw2, cy1 + ch2), 8, WHITE, outline=BORDER)
    draw.text((cx1 + 12, cy1 + 10), titles[0], font=F(12, bold=True), fill=TEXT)

    bar_x0  = cx1 + 110
    bar_max = cw2 - 130
    bar_h2  = 12
    n_show  = min(8, len(stocks))
    bar_y_start = cy1 + 34

    for i in range(n_show):
        by = bar_y_start + i * (bar_h2 + 6)
        draw.text((cx1 + 14, by), stocks[i], font=F(9), fill=MUTED)
        bw2 = int(scores[i] / 3.5 * bar_max)
        col = tuple(int(GREEN[j] * scores[i] / 3.5 + BLUE[j] * (1 - scores[i] / 3.5))
                    for j in range(3))
        draw.rounded_rectangle([bar_x0, by, bar_x0 + bw2, by + bar_h2],
                                radius=3, fill=col)
        draw.text((bar_x0 + bw2 + 4, by), f"{scores[i]:.2f}", font=F(9), fill=TEXT)

    # ── Chart 2: Donut chart (allocation) ────────────────────────────────────
    cx2, cy2 = positions[1]
    rounded_rect(draw, (cx2, cy2, cx2 + cw2, cy2 + ch2), 8, WHITE, outline=BORDER)
    draw.text((cx2 + 12, cy2 + 10), titles[1], font=F(12, bold=True), fill=TEXT)

    donut_cx = cx2 + cw2 // 2 - 30
    donut_cy = cy2 + ch2 // 2 + 10
    outer_r  = min(ch2, cw2) // 2 - 30
    inner_r  = outer_r - 28

    palette = [GREEN, BLUE, GOLD, (239, 68, 68), (168, 85, 247),
               (251, 146, 60), (20, 184, 166), (236, 72, 153),
               (132, 204, 22), (234, 179, 8)]
    start_angle = -90
    top5_other  = weights[:5] + [sum(weights[5:])]
    labels_5    = stocks[:5] + ["Others"]
    total_w     = sum(top5_other)

    for i, (w_val, lbl) in enumerate(zip(top5_other, labels_5)):
        sweep = 360 * w_val / total_w
        col   = palette[i % len(palette)]
        draw.pieslice(
            [donut_cx - outer_r, donut_cy - outer_r,
             donut_cx + outer_r, donut_cy + outer_r],
            start=start_angle, end=start_angle + sweep - 1, fill=col,
        )
        start_angle += sweep

    # Inner white circle (donut hole)
    draw.ellipse([donut_cx - inner_r, donut_cy - inner_r,
                  donut_cx + inner_r, donut_cy + inner_r], fill=WHITE)
    centered_text(draw, "₹5L", F(16, bold=True), TEXT, donut_cx, donut_cy)
    centered_text(draw, "total", F(10), MUTED, donut_cx, donut_cy + 18)

    # Legend
    leg_x = cx2 + cw2 - 115
    for i, (lbl, w_val) in enumerate(zip(labels_5, top5_other)):
        ly = cy2 + 30 + i * 20
        draw.rectangle([leg_x, ly + 3, leg_x + 10, ly + 13], fill=palette[i])
        draw.text((leg_x + 14, ly), f"{lbl} {w_val:.1f}%", font=F(9), fill=TEXT)

    # ── Chart 3: Scatter (return vs vol) ─────────────────────────────────────
    cx3, cy3 = positions[2]
    rounded_rect(draw, (cx3, cy3, cx3 + cw2, cy3 + ch2), 8, WHITE, outline=BORDER)
    draw.text((cx3 + 12, cy3 + 10), titles[2], font=F(12, bold=True), fill=TEXT)

    sc_l, sc_r = cx3 + 36, cx3 + cw2 - 16
    sc_t, sc_b = cy3 + 34, cy3 + ch2 - 28
    draw.rectangle([sc_l, sc_t, sc_r, sc_b], fill=LIGHT, outline=BORDER)

    draw.text((cx3 + 12, cy3 + ch2 - 18), "Volatility →", font=F(9), fill=MUTED)

    ret_vals = [62.4, 58.3, 51.2, 48.7, 46.0, 43.5, 40.7, 39.2, 37.8, 36.2,
                34.8, 33.4, 32.0, 30.5, 29.1]
    vol_vals = [20.1, 20.3, 20.2, 20.2, 20.2, 20.2, 20.2, 20.2, 20.2, 20.2,
                20.2, 20.2, 20.2, 20.2, 20.2]
    # Add some variance to vol
    vol_vals = [v + random.gauss(0, 2.5) for v in vol_vals]

    min_v, max_v = 14, 34
    min_r, max_r = 25, 68

    for i in range(len(stocks)):
        sx = sc_l + int((vol_vals[i] - min_v) / (max_v - min_v) * (sc_r - sc_l))
        sy = sc_b - int((ret_vals[i] - min_r) / (max_r - min_r) * (sc_b - sc_t))
        r  = int(weights[i] / 9.2 * 10) + 4
        col = GREEN if i < 3 else BLUE
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col + (160,) if False else col)
        if i < 5:
            draw.text((sx + r + 2, sy - 6), stocks[i], font=F(8), fill=MUTED)

    # Axis labels
    draw.text((sc_l - 30, sc_t - 6), "Ret%", font=F(9), fill=MUTED)

    # ── Chart 4: Sector bar ───────────────────────────────────────────────────
    cx4, cy4 = positions[3]
    rounded_rect(draw, (cx4, cy4, cx4 + cw2, cy4 + ch2), 8, WHITE, outline=BORDER)
    draw.text((cx4 + 12, cy4 + 10), titles[3], font=F(12, bold=True), fill=TEXT)

    sectors = {"Fin. Services": 3, "IT": 3, "Consumer": 3,
               "Energy": 1, "Diversified": 1, "Utilities": 1, "Chemicals": 1, "Healthcare": 1, "Materials": 1}
    sector_cols = [GREEN, BLUE, GOLD, (239, 68, 68), (168, 85, 247),
                   (251, 146, 60), (20, 184, 166), (236, 72, 153), (132, 204, 22)]

    sb_y0   = cy4 + 30
    sb_maxh = ch2 - 55
    sb_w2   = int((cw2 - 30) / len(sectors)) - 4

    for idx, ((sec, cnt), col) in enumerate(zip(sectors.items(), sector_cols)):
        bar_h3 = int(cnt / 3 * sb_maxh * 0.8)
        bx_    = cx4 + 16 + idx * (sb_w2 + 4)
        by_top = sb_y0 + sb_maxh - bar_h3
        draw.rounded_rectangle([bx_, by_top, bx_ + sb_w2, sb_y0 + sb_maxh],
                                radius=3, fill=col)
        draw.text((bx_ + sb_w2 // 2 - 4, by_top - 14), str(cnt),
                  font=F(10, bold=True), fill=TEXT)
        # rotated label workaround — just write abbreviated
        short = sec[:4]
        draw.text((bx_, sb_y0 + sb_maxh + 4), short, font=F(8), fill=MUTED)

    footer_bar(img, draw, W, H)
    img.save(f"{OUT}/05_charts.png")
    print("Saved: 05_charts.png")


# ── Screenshot 6: Performance tracking ───────────────────────────────────────

def shot_performance():
    W, H = 1200, 628
    img  = Image.new("RGB", (W, H), LIGHT)
    draw = ImageDraw.Draw(img)

    header_bar(img, draw, W)

    draw.text((40, 55), "Portfolio Performance Tracking",
              font=F(22, bold=True), fill=TEXT)
    draw.text((40, 86), "Last month vs Nifty 50  ·  History loaded: 5 runs",
              font=F(13), fill=MUTED)
    draw.line([40, 110, W - 40, 110], fill=GREEN, width=2)

    # ── KPI cards ─────────────────────────────────────────────────────────────
    kpis = [
        ("Last Portfolio Return", "+18.4%",  GREEN,  "Apr 2026"),
        ("Nifty 50 Return",       "+11.2%",  MUTED,  "Same period"),
        ("Alpha Generated",       "+7.2%",   GREEN,  "Outperformance"),
        ("Stocks that beat Nifty","11 / 15", BLUE,   "73% hit rate"),
    ]
    kw   = (W - 80 - 3 * 16) // 4
    ky   = 120
    kh   = 88

    for i, (label, value, col, sub) in enumerate(kpis):
        kx = 40 + i * (kw + 16)
        rounded_rect(draw, (kx, ky, kx + kw, ky + kh), 8, WHITE, outline=BORDER)
        draw.rectangle([kx, ky, kx + kw, ky + 4], fill=col)
        draw.text((kx + 14, ky + 12), label, font=F(10, bold=True), fill=MUTED)
        draw.text((kx + 14, ky + 34), value, font=F(26, bold=True), fill=col)
        draw.text((kx + 14, ky + 68), sub, font=F(10), fill=MUTED)

    # ── Month-by-month performance table ─────────────────────────────────────
    draw.text((40, 222), "Month-by-Month History", font=F(15, bold=True), fill=TEXT)
    draw.line([40, 244, W - 40, 244], fill=BORDER, width=1)

    hist_headers = ["Month", "Strategy",               "# Stocks", "Portfolio",  "Nifty 50",  "Alpha",     "Status"]
    hist_widths  = [88,       200,                       80,          96,           96,           88,          120]
    hist_rows    = [
        ("Apr 2026", "Risk-Adjusted Momentum", "15", "+18.4%", "+11.2%", "+7.2%",  "✓ Above"),
        ("Mar 2026", "Risk-Adjusted Momentum", "15", "+12.1%", "+9.8%",  "+2.3%",  "✓ Above"),
        ("Feb 2026", "Risk-Adjusted Momentum", "14", "+8.7%",  "+11.3%", "-2.6%",  "✗ Below"),
        ("Jan 2026", "Risk-Adjusted Momentum", "15", "+15.2%", "+7.4%",  "+7.8%",  "✓ Above"),
        ("Dec 2025", "Risk-Adjusted Momentum", "15", "+21.3%", "+14.1%", "+7.2%",  "✓ Above"),
    ]

    th_y = 252
    rounded_rect(draw, (40, th_y, W - 40, th_y + 28), 4, BG)
    x = 40
    for col, w in zip(hist_headers, hist_widths):
        cw_ = text_w(draw, col, F(10, bold=True))
        draw.text((x + (w - cw_) // 2, th_y + 8), col, font=F(10, bold=True), fill=WHITE)
        x += w

    for ridx, row in enumerate(hist_rows):
        ry = th_y + 28 + ridx * 34
        row_bg = WHITE if ridx % 2 == 0 else LIGHT
        draw.rectangle([40, ry, W - 40, ry + 34], fill=row_bg)

        x = 40
        for vidx, (val, w) in enumerate(zip(row, hist_widths)):
            if vidx in (3, 4, 5):  # returns
                col_v = GREEN if val.startswith("+") else RED
                vw_   = text_w(draw, val, F(11))
                draw.text((x + w - vw_ - 6, ry + 9), val, font=F(11), fill=col_v)
            elif vidx == 6:  # status
                col_v = GREEN if "Above" in val else RED
                draw.text((x + 8, ry + 9), val, font=F(11), fill=col_v)
            else:
                draw.text((x + 8, ry + 9), val, font=F(10), fill=TEXT)
            x += w
        draw.line([40, ry + 34, W - 40, ry + 34], fill=BORDER, width=1)

    # Cumulative gain note
    rounded_rect(draw, (40, th_y + 28 + 5 * 34 + 8, W - 40, th_y + 28 + 5 * 34 + 48),
                 6, GREEN_L, outline=GREEN, outline_w=1)
    draw.text((56, th_y + 28 + 5 * 34 + 20),
              "Cumulative 5-month portfolio return: +96.4%   vs Nifty 50: +59.5%   ·   Running alpha: +36.9%",
              font=F(12, bold=True), fill=TEXT)

    footer_bar(img, draw, W, H)
    img.save(f"{OUT}/06_performance_tracking.png")
    print("Saved: 06_performance_tracking.png")


# ── Screenshot 7: Square — "What you get" (Instagram/LinkedIn square) ─────────

def shot_square_overview():
    W = H = 1080
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Full dark background — this is the "hero" square post

    # Green top accent strip
    draw.rectangle([0, 0, W, 6], fill=GREEN)

    # Logo / branding
    draw.text((50, 28), "MOMENTUM PORTFOLIO TOOL",
              font=F(16, bold=True), fill=GREEN)
    draw.text((50, 54), "pick-momentum.streamlit.app",
              font=F(13), fill=MUTED)

    # Big headline
    draw.text((50, 110), "Build a NIFTY 500", font=F(42, bold=True), fill=WHITE)
    draw.text((50, 162), "Momentum Portfolio", font=F(42, bold=True), fill=GREEN)
    draw.text((50, 214), "in 5 minutes.", font=F(42, bold=True), fill=WHITE)

    draw.text((50, 276),
              "Research-backed. Free. No login. No API key.",
              font=F(16), fill=(148, 163, 184))

    draw.line([50, 310, W - 50, 310], fill=NAVY3, width=1)

    # 4 strategies
    draw.text((50, 328), "4 Strategies", font=F(18, bold=True), fill=WHITE)
    strategies_sq = [
        ("📈", "Classic Momentum",       "High risk · 12-1 return",         GOLD),
        ("⚖️", "Risk-Adjusted ★",        "Medium · Return÷Vol",             GREEN),
        ("🛡",  "Dual Momentum",          "Low-med · Cash signal in bear mkts", BLUE),
        ("🎯", "52-Week High",           "Medium · Breakout-focused",         MUTED),
    ]
    for i, (em, name, sig, col) in enumerate(strategies_sq):
        sy = 360 + i * 74
        rounded_rect(draw, (50, sy, W - 50, sy + 62), 8, NAVY2)
        draw.text((70, sy + 18), em, font=F(22), fill=WHITE)
        draw.text((110, sy + 14), name, font=F(16, bold=True), fill=WHITE)
        draw.text((110, sy + 36), sig, font=F(12), fill=col)
        # right side badge
        if name == "Risk-Adjusted ★":
            badge(draw, "Recommended", W - 180, sy + 20, GREEN, GREEN_L, F(11, bold=True))

    draw.line([50, 668, W - 50, 668], fill=NAVY3, width=1)

    # What you get bullets
    draw.text((50, 686), "What you get every month:", font=F(16, bold=True), fill=WHITE)
    bullets = [
        ("▶",  "Top 15 momentum stocks with exact rupee allocation", WHITE),
        ("▶",  "NEW / HOLD / EXIT rebalancing actions vs last month", WHITE),
        ("▶",  "Portfolio performance vs Nifty 50 benchmark", WHITE),
        ("▶",  "Market regime signal — deploy or stay defensive", WHITE),
    ]
    for i, (sym, text, col) in enumerate(bullets):
        by = 716 + i * 38
        draw.text((50, by), sym, font=F(13, bold=True), fill=GREEN)
        draw.text((78, by), text, font=F(14), fill=col)

    # Bottom CTA
    rounded_rect(draw, (50, H - 100, W - 50, H - 30), 10, GREEN)
    cta = "Try free → pick-momentum.streamlit.app"
    cw_ = text_w(draw, cta, F(17, bold=True))
    draw.text(((W - cw_) // 2, H - 76), cta, font=F(17, bold=True), fill=BG)

    img.save(f"{OUT}/07_square_overview.png")
    print("Saved: 07_square_overview.png")


# ── Screenshot 8: Square — Strategy deep dive ─────────────────────────────────

def shot_square_strategy():
    W = H = 1080
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 6], fill=BLUE)
    draw.text((50, 28), "MOMENTUM PORTFOLIO TOOL",
              font=F(16, bold=True), fill=GREEN)
    draw.text((50, 54), "Strategy Deep Dive", font=F(13), fill=MUTED)

    draw.text((50, 100), "Risk-Adjusted", font=F(46, bold=True), fill=WHITE)
    draw.text((50, 154), "Momentum", font=F(46, bold=True), fill=BLUE)
    badge(draw, "★  Recommended for most investors", 50, 212,
          GREEN, GREEN_L, F(14, bold=True), pad_x=14, pad_y=8, radius=6)

    draw.text((50, 268), "Based on: Barroso & Santa-Clara (2015)",
              font=F(14), fill=MUTED)
    draw.text((50, 292), "Journal of Financial Economics", font=F(13), fill=MUTED)

    draw.line([50, 326, W - 50, 326], fill=NAVY3, width=1)

    draw.text((50, 344), "How it ranks stocks:", font=F(16, bold=True), fill=WHITE)
    draw.text((50, 376),
              "Score  =  12-1 Month Return  ÷  Annualised Volatility",
              font=F(18, bold=True), fill=GREEN)
    draw.text((50, 416),
              "Rewards smooth, persistent uptrends over erratic spikes.",
              font=F(14), fill=(148, 163, 184))

    draw.line([50, 454, W - 50, 454], fill=NAVY3, width=1)

    # Example comparison
    draw.text((50, 472), "Example — which stock ranks higher?",
              font=F(15, bold=True), fill=WHITE)

    for i, (sym, ret, vol, score, winner) in enumerate([
        ("Stock A", "+60%", "20% vol", "3.0", True),
        ("Stock B", "+80%", "70% vol", "1.1", False),
    ]):
        sy = 512 + i * 100
        col = (NAVY2 if winner else NAVY3)
        rounded_rect(draw, (50, sy, W - 50, sy + 82), 8, col)
        draw.text((76, sy + 14), sym, font=F(16, bold=True), fill=WHITE)
        draw.text((76, sy + 40), f"Returned {ret}  ·  {vol}  →  Score: {score}",
                  font=F(14), fill=(148, 163, 184))
        if winner:
            badge(draw, "Higher rank", W - 200, sy + 24, GREEN, GREEN_L, F(12, bold=True))
        else:
            badge(draw, "Lower rank", W - 180, sy + 24, MUTED, NAVY3, F(12, bold=True))

    draw.line([50, 726, W - 50, 726], fill=NAVY3, width=1)

    draw.text((50, 748), "Key benefits:", font=F(15, bold=True), fill=WHITE)
    benefits = [
        "Reduces momentum crash risk by ~80%  (Barroso & Santa-Clara)",
        "200-day MA filter removes broken downtrends from universe",
        "Return-weighted allocation — stronger signals get more capital",
    ]
    for i, b in enumerate(benefits):
        draw.text((50, 782 + i * 38), f"✓  {b}", font=F(13), fill=GREEN)

    rounded_rect(draw, (50, H - 100, W - 50, H - 30), 10, BLUE)
    cta = "Try free → pick-momentum.streamlit.app"
    cw_ = text_w(draw, cta, F(17, bold=True))
    draw.text(((W - cw_) // 2, H - 76), cta, font=F(17, bold=True), fill=WHITE)

    img.save(f"{OUT}/08_square_strategy.png")
    print("Saved: 08_square_strategy.png")


# ── Run all ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating screenshots...")
    shot_strategy_selector()
    shot_market_regime()
    shot_results_table()
    shot_rebalancing()
    shot_charts()
    shot_performance()
    shot_square_overview()
    shot_square_strategy()
    print(f"\nAll screenshots saved to: {OUT}")
