"""Generate Momentum Portfolio Tool PDF — professional design with clickable links."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

# ── Palette ───────────────────────────────────────────────────────────────────
C_BG      = colors.HexColor("#0f172a")   # dark navy
C_NAVY2   = colors.HexColor("#1e293b")   # slightly lighter navy
C_NAVY3   = colors.HexColor("#334155")   # slate-700
C_GREEN   = colors.HexColor("#22c55e")   # accent green
C_GREEN_L = colors.HexColor("#dcfce7")   # light green bg
C_BLUE    = colors.HexColor("#3b82f6")   # blue
C_BLUE_L  = colors.HexColor("#eff6ff")   # light blue bg
C_GOLD    = colors.HexColor("#f59e0b")   # amber
C_GOLD_L  = colors.HexColor("#fef3c7")   # light amber
C_RED     = colors.HexColor("#ef4444")   # red
C_RED_L   = colors.HexColor("#fee2e2")   # light red
C_TEXT    = colors.HexColor("#0f172a")   # near-black body text
C_MUTED   = colors.HexColor("#64748b")   # slate-500
C_LIGHT   = colors.HexColor("#f8fafc")   # off-white
C_BORDER  = colors.HexColor("#e2e8f0")   # border grey
C_WHITE   = colors.white

W, H = A4   # 595 x 842 pt  (≈ 210 x 297 mm)
MARGIN_X = 18 * mm
BODY_W   = W - 2 * MARGIN_X   # usable body width ≈ 559 pt

# ── Link targets ──────────────────────────────────────────────────────────────
URL_APP    = "https://pick-momentum.streamlit.app"
URL_GITHUB = "https://github.com/tooweeknd/momentum-dashboard"
URL_LI     = "https://linkedin.com/in/durgeshh/"

# ── Footer / Header callbacks (with clickable link annotations) ───────────────

def _draw_footer(c, page_num):
    """Draw footer bar with clickable links."""
    fh = 24
    c.setFillColor(C_BG)
    c.rect(0, 0, W, fh, fill=1, stroke=0)

    font, fs = "Helvetica", 7.5
    c.setFont(font, fs)

    parts = [
        (URL_LI,     "linkedin.com/in/durgeshh/",               C_GREEN),
        (None,       "   |   ",                                  C_MUTED),
        (URL_APP,    "pick-momentum.streamlit.app",              C_GREEN),
        (None,       "   |   ",                                  C_MUTED),
        (URL_GITHUB, "github.com/tooweeknd/momentum-dashboard",  C_GREEN),
    ]
    total_w = sum(c.stringWidth(t, font, fs) for _, t, _ in parts)
    x = (W - total_w) / 2
    y = 8

    for url, text, color in parts:
        tw = c.stringWidth(text, font, fs)
        c.setFillColor(color)
        c.drawString(x, y, text)
        if url:
            c.linkURL(url, (x, y - 2, x + tw, y + fs + 2), relative=0)
        x += tw

    # page number on the right
    if page_num > 1:
        c.setFont("Helvetica", 7)
        c.setFillColor(C_MUTED)
        c.drawRightString(W - 15, y, f"{page_num}")


def _draw_header(c, page_num):
    """Draw thin navy header bar on inner pages."""
    hh = 20
    c.setFillColor(C_BG)
    c.rect(0, H - hh, W, hh, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(C_GREEN)
    c.drawString(MARGIN_X, H - 13, "MOMENTUM PORTFOLIO TOOL")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(C_MUTED)
    c.drawRightString(W - MARGIN_X, H - 13, URL_APP)
    c.linkURL(URL_APP, (W - MARGIN_X - 150, H - 18, W - MARGIN_X, H - 6), relative=0)


def on_first_page(c, doc):
    c.saveState()
    _draw_footer(c, doc.page)
    c.restoreState()


def on_later_pages(c, doc):
    c.saveState()
    _draw_header(c, doc.page)
    _draw_footer(c, doc.page)
    c.restoreState()


# ── Style factory ─────────────────────────────────────────────────────────────

def S(name="body", **kw):
    """Quick ParagraphStyle builder."""
    defaults = dict(
        fontName="Helvetica", fontSize=9.5,
        textColor=C_TEXT, leading=14, spaceAfter=4,
    )
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


def make_styles():
    return {
        # Cover
        "cover_tag":   S("cover_tag",   fontSize=9,  fontName="Helvetica-Bold",
                         textColor=C_GREEN, alignment=TA_CENTER, spaceAfter=6),
        "cover_title": S("cover_title", fontSize=34, fontName="Helvetica-Bold",
                         textColor=C_WHITE, alignment=TA_CENTER, spaceAfter=4, leading=40),
        "cover_sub":   S("cover_sub",   fontSize=13, fontName="Helvetica",
                         textColor=colors.HexColor("#94a3b8"), alignment=TA_CENTER, spaceAfter=18),
        "cover_body":  S("cover_body",  fontSize=10, fontName="Helvetica",
                         textColor=colors.HexColor("#cbd5e1"), alignment=TA_JUSTIFY,
                         leading=16, spaceAfter=8),
        # Section headings
        "h1":  S("h1",  fontSize=17, fontName="Helvetica-Bold", textColor=C_BG,
                 spaceBefore=10, spaceAfter=5, leading=20),
        "h2":  S("h2",  fontSize=12, fontName="Helvetica-Bold", textColor=C_BLUE,
                 spaceBefore=10, spaceAfter=4, leading=15),
        "h3":  S("h3",  fontSize=10.5, fontName="Helvetica-Bold", textColor=C_TEXT,
                 spaceBefore=6, spaceAfter=3),
        # Body
        "body":   S("body",   alignment=TA_JUSTIFY, leading=14),
        "bodyW":  S("bodyW",  alignment=TA_JUSTIFY, leading=14, textColor=C_WHITE),
        "bullet": S("bullet", leftIndent=10, spaceAfter=3, leading=13),
        "small":  S("small",  fontSize=8, textColor=C_MUTED, leading=11),
        "label":  S("label",  fontSize=7.5, fontName="Helvetica-Bold",
                    textColor=C_MUTED, spaceAfter=1),
        # Caption / note
        "caption": S("caption", fontSize=8, fontName="Helvetica-Oblique",
                     textColor=C_MUTED, alignment=TA_CENTER),
        # CTA / link
        "link_green": S("link_green", fontSize=10, fontName="Helvetica-Bold",
                        textColor=C_GREEN, alignment=TA_CENTER),
    }


# ── Utility flowables ─────────────────────────────────────────────────────────

def hr(color=C_GREEN, thickness=1.0, width="100%", before=4, after=8):
    return HRFlowable(width=width, thickness=thickness, color=color,
                      spaceBefore=before, spaceAfter=after)


def sp(h=6):
    return Spacer(1, h)


def _tbl(data, col_widths, style_cmds):
    """Helper: build Table with given style commands."""
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(style_cmds))
    return t


# ── Reusable block builders ───────────────────────────────────────────────────

def section_heading_block(title, s):
    """Heading + green rule."""
    return KeepTogether([
        Paragraph(title, s["h1"]),
        hr(),
    ])


def stat_box(items, s):
    """Dark stat key-value table (cover page)."""
    kst = ParagraphStyle("sk", fontSize=8.5, fontName="Helvetica-Bold",
                         textColor=C_GREEN, leading=12)
    vst = ParagraphStyle("sv", fontSize=8.5, fontName="Helvetica",
                         textColor=C_WHITE, leading=12)
    rows = [[Paragraph(k, kst), Paragraph(v, vst)] for k, v in items]
    t = _tbl(rows, [52 * mm, 110 * mm], [
        ("BACKGROUND", (0, 0), (-1, -1), C_BG),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [C_BG, C_NAVY2]),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.3, C_NAVY3),
    ])
    return t


def data_table(headers, rows, col_widths=None, header_bg=None):
    """Styled data table with alternating rows."""
    if header_bg is None:
        header_bg = C_BG
    if col_widths is None:
        n = len(headers)
        col_widths = [BODY_W / n] * n

    hst = ParagraphStyle("th", fontSize=8, fontName="Helvetica-Bold",
                         textColor=C_WHITE, alignment=TA_CENTER, leading=10)
    dst = ParagraphStyle("td", fontSize=8.5, fontName="Helvetica",
                         textColor=C_TEXT, leading=12)

    data = [[Paragraph(h, hst) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), dst) for c in row])

    t = _tbl(data, col_widths, [
        ("BACKGROUND",    (0, 0), (-1, 0),  header_bg),
        ("ROWBACKGROUNDS",(1, 0), (-1, -1), [C_WHITE, C_LIGHT]),
        ("GRID",          (0, 0), (-1, -1), 0.35, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ])
    return t


def risk_badge(risk_label):
    """Colored risk badge text."""
    color = (C_GREEN if "Low" in risk_label
             else C_GOLD if "Medium" in risk_label
             else C_RED)
    return Paragraph(
        f"● {risk_label}",
        ParagraphStyle("rb", fontSize=8.5, fontName="Helvetica-Bold",
                       textColor=color, alignment=TA_LEFT),
    )


def strategy_card(num, title, research, signal, allocation, risk_label, body_text, best_for, s):
    """Premium strategy card with dark header, meta strip, and content."""
    risk_color = (C_GREEN if "Low" in risk_label
                  else C_GOLD if "Medium" in risk_label
                  else C_RED)

    # Header row: number pill + title + risk badge
    hdr_num = ParagraphStyle("hn", fontSize=22, fontName="Helvetica-Bold",
                              textColor=C_GREEN, alignment=TA_CENTER, leading=26)
    hdr_title = ParagraphStyle("ht", fontSize=12, fontName="Helvetica-Bold",
                                textColor=C_WHITE, leading=16)
    hdr_risk = ParagraphStyle("hr2", fontSize=9, fontName="Helvetica-Bold",
                               textColor=risk_color, alignment=TA_RIGHT)

    hdr = _tbl(
        [[Paragraph(num, hdr_num),
          Paragraph(title, hdr_title),
          Paragraph(f"Risk: {risk_label}", hdr_risk)]],
        [14 * mm, 118 * mm, 38 * mm],
        [("BACKGROUND",   (0, 0), (-1, -1), C_BG),
         ("TOPPADDING",   (0, 0), (-1, -1), 8),
         ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
         ("LEFTPADDING",  (0, 0), (-1, -1), 8),
         ("RIGHTPADDING", (0, 0), (-1, -1), 8),
         ("VALIGN",       (0, 0), (-1, -1), "MIDDLE")],
    )

    # Meta strip
    meta_st = ParagraphStyle("ms", fontSize=7.5, fontName="Helvetica",
                              textColor=C_MUTED, leading=11)
    meta_bold = ParagraphStyle("mb", fontSize=7.5, fontName="Helvetica-Bold",
                               textColor=C_TEXT, leading=11)
    meta = _tbl(
        [[Paragraph("RESEARCH", meta_st), Paragraph("SIGNAL", meta_st),
          Paragraph("ALLOCATION", meta_st)],
         [Paragraph(research, meta_bold), Paragraph(signal, meta_bold),
          Paragraph(allocation, meta_bold)]],
        [72 * mm, 62 * mm, 36 * mm],
        [("BACKGROUND",   (0, 0), (-1, -1), C_LIGHT),
         ("TOPPADDING",   (0, 0), (-1, -1), 3),
         ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
         ("LEFTPADDING",  (0, 0), (-1, -1), 8),
         ("RIGHTPADDING", (0, 0), (-1, -1), 6),
         ("LINEBELOW",    (0, 0), (-1, 0),  0.5, C_BORDER),
         ("VALIGN",       (0, 0), (-1, -1), "MIDDLE")],
    )

    # Body
    body_tbl = _tbl(
        [[Paragraph(body_text, s["body"])]],
        [BODY_W],
        [("BACKGROUND",   (0, 0), (-1, -1), C_WHITE),
         ("TOPPADDING",   (0, 0), (-1, -1), 8),
         ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
         ("LEFTPADDING",  (0, 0), (-1, -1), 10),
         ("RIGHTPADDING", (0, 0), (-1, -1), 10),
         ("BOX",          (0, 0), (-1, -1), 0.4, C_BORDER)],
    )

    # Best for
    bf_tbl = _tbl(
        [[Paragraph(f"✦  Best for: {best_for}",
                    ParagraphStyle("bf", fontSize=8.5, fontName="Helvetica-Oblique",
                                   textColor=C_BLUE, leading=12))]],
        [BODY_W],
        [("BACKGROUND",   (0, 0), (-1, -1), C_BLUE_L),
         ("TOPPADDING",   (0, 0), (-1, -1), 6),
         ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
         ("LEFTPADDING",  (0, 0), (-1, -1), 10),
         ("RIGHTPADDING", (0, 0), (-1, -1), 10),
         ("BOX",          (0, 0), (-1, -1), 0.4, C_BORDER)],
    )

    return KeepTogether([hdr, meta, body_tbl, bf_tbl, sp(8)])


def callout_box(title, items, bg=C_NAVY2, title_color=C_GREEN, text_color=C_WHITE):
    """Dark callout box with bullet list."""
    content = [
        Paragraph(title, ParagraphStyle("cbh", fontSize=10, fontName="Helvetica-Bold",
                                         textColor=title_color)),
        sp(4),
    ]
    ist = ParagraphStyle("cbi", fontSize=8.5, fontName="Helvetica",
                         textColor=text_color, leading=13, leftIndent=6)
    for item in items:
        content.append(Paragraph(f"•  {item}", ist))

    rows = [[item] for item in content]
    t = _tbl([[r[0]] for r in rows], [BODY_W], [
        ("BACKGROUND",   (0, 0), (-1, -1), bg),
        ("TOPPADDING",   (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING",   (0, 0), (0, 0),   10),
        ("BOTTOMPADDING",(0, -1), (0, -1), 10),
    ])
    return t


# ── App Preview / Mockup helpers ──────────────────────────────────────────────

def action_badge(action):
    """Colored action badge: NEW / HOLD / EXIT."""
    cfg = {
        "NEW":  (C_GREEN,  C_GREEN_L),
        "HOLD": (C_BLUE,   C_BLUE_L),
        "EXIT": (C_RED,    C_RED_L),
    }
    fg, bg = cfg.get(action, (C_MUTED, C_LIGHT))
    st = ParagraphStyle("ab", fontSize=8, fontName="Helvetica-Bold",
                        textColor=fg, alignment=TA_CENTER)
    t = _tbl([[Paragraph(action, st)]], [14 * mm], [
        ("BACKGROUND",   (0, 0), (-1, -1), bg),
        ("TOPPADDING",   (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
        ("LEFTPADDING",  (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("BOX",          (0, 0), (-1, -1), 0.6, fg),
    ])
    return t


def mock_results_table():
    """A realistic-looking sample output table."""
    # Header
    hst = ParagraphStyle("mh", fontSize=7.5, fontName="Helvetica-Bold",
                         textColor=C_WHITE, alignment=TA_CENTER, leading=9)
    dst = ParagraphStyle("md", fontSize=7.5, fontName="Helvetica",
                         textColor=C_TEXT, leading=10)
    dst_r = ParagraphStyle("mdr", fontSize=7.5, fontName="Helvetica",
                           textColor=C_TEXT, leading=10, alignment=TA_RIGHT)

    headers = ["#", "Action", "Symbol", "Company", "Sector",
               "Score", "12-1 Ret", "Ann.Vol", "Weight", "Alloc (₹)"]
    col_w = [8*mm, 15*mm, 22*mm, 36*mm, 28*mm,
             14*mm, 14*mm, 13*mm, 13*mm, 19*mm]

    # Sample rows (representative data — for illustration)
    raw = [
        ("1",  "HOLD", "RELIANCE",   "Reliance Industries",     "Energy",        "3.12", "+62.4%", "20.1%", "9.2%",  "₹46,000"),
        ("2",  "NEW",  "BAJFINANCE", "Bajaj Finance",           "Fin. Services", "2.87", "+58.3%", "20.3%", "8.6%",  "₹43,000"),
        ("3",  "HOLD", "HDFCBANK",   "HDFC Bank",               "Fin. Services", "2.54", "+51.2%", "20.2%", "7.6%",  "₹38,000"),
        ("4",  "NEW",  "LTIM",       "LTIMindtree",             "IT",            "2.41", "+48.7%", "20.2%", "7.2%",  "₹36,000"),
        ("5",  "HOLD", "TITAN",      "Titan Company",           "Consumer",      "2.28", "+46.0%", "20.2%", "6.8%",  "₹34,000"),
        ("6",  "EXIT", "INFY",       "Infosys",                 "IT",            "—",    "+12.1%", "18.4%", "—",     "SELL"),
    ]

    action_colors = {"HOLD": C_BLUE_L, "NEW": C_GREEN_L, "EXIT": C_RED_L}
    action_txt_colors = {"HOLD": C_BLUE, "NEW": C_GREEN, "EXIT": C_RED}

    data = [[Paragraph(h, hst) for h in headers]]
    for row in raw:
        action = row[1]
        bg_row = action_colors.get(action, C_WHITE)
        ac_style = ParagraphStyle("ac", fontSize=7.5, fontName="Helvetica-Bold",
                                  textColor=action_txt_colors.get(action, C_TEXT),
                                  alignment=TA_CENTER, leading=10)
        cells = [
            Paragraph(row[0], dst_r),
            Paragraph(row[1], ac_style),
            Paragraph(row[2], ParagraphStyle("sym", fontSize=7.5, fontName="Helvetica-Bold",
                                              textColor=C_BG, leading=10)),
            Paragraph(row[3], dst),
            Paragraph(row[4], dst),
            Paragraph(row[5], dst_r),
            Paragraph(row[6], ParagraphStyle("ret", fontSize=7.5, fontName="Helvetica",
                                              textColor=C_GREEN if row[6].startswith("+") else C_RED,
                                              leading=10, alignment=TA_RIGHT)),
            Paragraph(row[7], dst_r),
            Paragraph(row[8], dst_r),
            Paragraph(row[9], dst_r),
        ]
        data.append(cells)

    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  C_BG),
        ("ROWBACKGROUNDS",(1, 0), (-1, -1), [C_WHITE, C_LIGHT]),
        # Colour the Action column cells individually won't work per-cell easily;
        # use overall grid styling
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
    ]))
    return t


def mock_regime_panel():
    """Green market regime panel mockup."""
    st_label = ParagraphStyle("rl", fontSize=10, fontName="Helvetica-Bold",
                              textColor=C_WHITE, alignment=TA_CENTER)
    st_val   = ParagraphStyle("rv", fontSize=22, fontName="Helvetica-Bold",
                              textColor=C_GREEN, alignment=TA_CENTER, leading=26)
    st_sub   = ParagraphStyle("rs", fontSize=8.5, fontName="Helvetica",
                              textColor=colors.HexColor("#94a3b8"), alignment=TA_CENTER, leading=12)

    inner = [
        [Paragraph("MARKET REGIME", st_label)],
        [Paragraph("▲  UPTREND", st_val)],
        [Paragraph("Nifty 50 is above its 200-day moving average\n"
                   "Momentum conditions are favourable — deploy capital as planned.", st_sub)],
    ]
    t = _tbl([[r[0]] for r in inner], [BODY_W * 0.48], [
        ("BACKGROUND",   (0, 0), (-1, -1), C_BG),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (0, 0),   10),
        ("BOTTOMPADDING",(0, -1),(0, -1),  10),
        ("LINEBELOW",    (0, 0), (-1, 0),  1.5, C_GREEN),
        ("BOX",          (0, 0), (-1, -1), 0.5, C_GREEN),
    ])
    return t


def mock_rebalancing_panel():
    """Rebalancing actions summary panel."""
    title_st = ParagraphStyle("rbt", fontSize=10, fontName="Helvetica-Bold",
                              textColor=C_WHITE)
    actions = [
        ("NEW",  "BAJFINANCE", "Bajaj Finance",   "+58.3%", "₹43,000", "18 shares"),
        ("NEW",  "LTIM",       "LTIMindtree",     "+48.7%", "₹36,000", "4 shares"),
        ("HOLD", "RELIANCE",   "Reliance Ind.",   "+62.4%", "₹46,000", "16 shares"),
        ("HOLD", "HDFCBANK",   "HDFC Bank",       "+51.2%", "₹38,000", "22 shares"),
        ("EXIT", "INFY",       "Infosys",         "+12.1%", "SELL ALL", "—"),
    ]
    acs_bold = {"NEW": C_GREEN, "HOLD": C_BLUE, "EXIT": C_RED}
    hst = ParagraphStyle("rh", fontSize=7.5, fontName="Helvetica-Bold",
                         textColor=C_WHITE, alignment=TA_CENTER, leading=10)
    nst = ParagraphStyle("rn", fontSize=7.5, fontName="Helvetica",
                         textColor=C_TEXT, leading=10)

    header_row = [Paragraph(h, hst)
                  for h in ["Action", "Symbol", "Company", "12-1 Ret", "Allocated", "Shares"]]
    data = [header_row]
    for act, sym, company, ret, alloc, shares in actions:
        ast = ParagraphStyle("ast2", fontSize=7.5, fontName="Helvetica-Bold",
                             textColor=acs_bold[act], alignment=TA_CENTER, leading=10)
        data.append([
            Paragraph(act, ast),
            Paragraph(sym, ParagraphStyle("sym2", fontSize=7.5, fontName="Helvetica-Bold",
                                          textColor=C_BG, leading=10)),
            Paragraph(company, nst),
            Paragraph(ret, ParagraphStyle("ret2", fontSize=7.5, fontName="Helvetica",
                                          textColor=C_GREEN if ret.startswith("+") else C_RED,
                                          leading=10)),
            Paragraph(alloc, nst),
            Paragraph(shares, nst),
        ])

    t = Table(data, colWidths=[16*mm, 22*mm, 46*mm, 20*mm, 22*mm, 22*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  C_NAVY2),
        ("ROWBACKGROUNDS",(1, 0), (-1, -1), [C_WHITE, C_LIGHT]),
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("BOX",           (0, 0), (-1, -1), 0.5, C_BORDER),
    ]))
    return t


# ── Page builders ─────────────────────────────────────────────────────────────

def page_cover(s):
    """Page 1 — dark full-page cover."""
    inner = [
        sp(22 * mm),
        Paragraph("MOMENTUM", s["cover_tag"]),
        Paragraph("Portfolio Tool", s["cover_title"]),
        Paragraph(
            "A research-backed approach to systematic momentum investing in the NIFTY 500",
            s["cover_sub"],
        ),
        HRFlowable(width="55%", thickness=1.5, color=C_GREEN,
                   spaceAfter=18, spaceBefore=2),
        Paragraph(
            "Momentum investing — buying recent winners and avoiding recent losers — is "
            "one of the most well-documented anomalies in financial markets, replicated "
            "across 40+ years and 40+ countries. This tool applies four research-backed "
            "strategies to the full NIFTY 500 universe, giving Indian retail investors a "
            "systematic, rules-based framework for monthly portfolio construction. "
            "No gut-feel. No API keys. No cost.",
            s["cover_body"],
        ),
        sp(14),
        stat_box([
            ("Universe",    "NIFTY 500 stocks — full NSE India universe"),
            ("Strategies",  "4 research-backed approaches, each with academic citation"),
            ("Rebalancing", "Monthly — run once, act once, done"),
            ("Data",        "Live prices from Yahoo Finance — free, no key required"),
            ("App",         "pick-momentum.streamlit.app (free, no login)"),
            ("Source code", "github.com/tooweeknd/momentum-dashboard (MIT licence)"),
        ], s),
        sp(20),
        Paragraph(
            '<a href="https://pick-momentum.streamlit.app" color="#22c55e">'
            '<u>pick-momentum.streamlit.app</u></a>',
            ParagraphStyle("cov_link", fontSize=13, fontName="Helvetica-Bold",
                           textColor=C_GREEN, alignment=TA_CENTER),
        ),
        sp(14),
        Paragraph(
            "Not investment advice. For educational purposes only. "
            "Past momentum performance does not guarantee future results.",
            ParagraphStyle("disc", fontSize=7.5, fontName="Helvetica-Oblique",
                           textColor=colors.HexColor("#475569"), alignment=TA_CENTER),
        ),
    ]

    # Wrap everything in a dark table that fills the body area
    rows = [[item] for item in inner]
    cover_t = _tbl([[r[0]] for r in rows], [BODY_W], [
        ("BACKGROUND",   (0, 0), (-1, -1), C_BG),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12 * mm),
    ])
    return [cover_t, PageBreak()]


def page_preview(s):
    """Page 2 — visual tool preview / sample output."""
    story = []
    story.append(section_heading_block("What the Tool Shows You", s))
    story.append(Paragraph(
        "Each month the tool produces three outputs: a Market Regime signal, a ranked "
        "portfolio of 15 stocks with capital allocation, and exact Rebalancing Actions "
        "vs last month. The samples below show representative output from the "
        "Risk-Adjusted Momentum strategy on a ₹5,00,000 portfolio.",
        s["body"],
    ))
    story.append(sp(10))

    # Two-panel row: regime + strategy card sample
    regime_panel = mock_regime_panel()
    strategy_mini = _tbl([[
        Paragraph("STRATEGY ACTIVE", ParagraphStyle("sml", fontSize=8, fontName="Helvetica-Bold",
                                                     textColor=C_GREEN)),
        Paragraph("Risk-Adjusted Momentum", ParagraphStyle("smv", fontSize=11,
                                                            fontName="Helvetica-Bold",
                                                            textColor=C_WHITE, leading=14)),
        Paragraph("Barroso & Santa-Clara (2015)\nReturn / Volatility signal",
                  ParagraphStyle("sms", fontSize=8, fontName="Helvetica",
                                 textColor=colors.HexColor("#94a3b8"), leading=11)),
        Paragraph("15 stocks  ·  ₹5,00,000 capital",
                  ParagraphStyle("smd", fontSize=8.5, fontName="Helvetica-Bold",
                                 textColor=C_MUTED)),
    ]], [BODY_W * 0.50], [
        ("BACKGROUND",   (0, 0), (-1, -1), C_NAVY2),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING",   (0, 0), (0, 0),   10),
        ("BOTTOMPADDING",(0, -1),(0, -1),  10),
        ("BOX",          (0, 0), (-1, -1), 0.5, C_NAVY3),
    ])

    two_col = _tbl([[regime_panel, strategy_mini]], [BODY_W * 0.49, BODY_W * 0.51], [
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0),   5),
    ])
    story.append(two_col)
    story.append(sp(12))

    # Results table
    story.append(Paragraph(
        "Portfolio Results — Risk-Adjusted Momentum  (sample output)",
        s["h2"],
    ))
    story.append(Paragraph(
        "The results table shows all 15 selected stocks ranked by their Risk-Adjusted "
        "Score (12-1 return ÷ volatility). Green rows are NEW additions; blue rows are "
        "existing HOLD positions; red rows are EXIT signals vs last month.",
        s["body"],
    ))
    story.append(sp(4))
    story.append(mock_results_table())
    story.append(Paragraph(
        "Sample data shown for illustration. Actual results vary monthly based on market conditions.",
        s["caption"],
    ))
    story.append(sp(12))

    # Rebalancing panel
    story.append(Paragraph("Rebalancing Actions — What to do Next Month", s["h2"]))
    story.append(Paragraph(
        "The rebalancing panel compares this month's portfolio against last month's, "
        "giving you three simple actions: NEW stocks to buy, positions to HOLD unchanged, "
        "and stocks to EXIT (sell). Typically 3-5 stocks change per month.",
        s["body"],
    ))
    story.append(sp(4))
    story.append(mock_rebalancing_panel())
    story.append(sp(6))

    story.append(callout_box(
        "Charts included in the full output",
        [
            "Bar chart — Portfolio weights showing relative capital allocation per stock",
            "Sector pie chart — Diversification across NIFTY 500 sectors",
            "Return distribution histogram — Spread of 12-1 returns in the portfolio",
            "Risk-Return scatter — Each stock plotted by return vs volatility",
        ],
        bg=C_BG,
    ))
    story.append(PageBreak())
    return story


def page_strategies(s):
    """Pages 3-4 — the four strategies."""
    story = []
    story.append(section_heading_block("The Four Momentum Strategies", s))
    story.append(Paragraph(
        "Each strategy is grounded in peer-reviewed research. All four operate on the "
        "same NIFTY 500 universe with the same 12-month lookback window — only the "
        "ranking signal and allocation rule differ.",
        s["body"],
    ))
    story.append(sp(8))

    story.append(strategy_card(
        "1", "Classic Momentum",
        research="Jegadeesh & Titman, Journal of Finance, 1993",
        signal="12-1 return (12M, skip last month)",
        allocation="Equal weight — 1/15 per stock",
        risk_label="High",
        body_text=(
            "The foundational momentum paper — one of the most replicated findings in "
            "financial economics. Ranks all 500 stocks by their return over the past 12 months "
            "(excluding the most recent month to avoid short-term reversal noise) and selects "
            "the top 15 with equal capital allocation. Simple, transparent, and battle-tested "
            "across 30+ years of out-of-sample evidence in markets worldwide. Most aggressive "
            "of the four strategies — no built-in downside protection."
        ),
        best_for="Aggressive investors in sustained bull markets who can tolerate sharp drawdowns.",
        s=s,
    ))

    story.append(strategy_card(
        "2", "Risk-Adjusted Momentum  ★ Recommended",
        research="Barroso & Santa-Clara, Journal of Financial Economics, 2015",
        signal="12-1 return ÷ Annualised volatility",
        allocation="Return-weighted — larger signal → larger position",
        risk_label="Medium",
        body_text=(
            "Divides each stock's momentum return by its annualised volatility. A stock "
            "up 60% with 20% volatility scores 3.0 and ranks above a stock up 80% with 70% "
            "volatility (score: 1.14). This rewards smooth, persistent uptrends over erratic "
            "spikes. Barroso & Santa-Clara showed this reduces momentum crash risk by ~80% "
            "while preserving most of the return premium. Additionally filters out stocks "
            "below their own 200-day moving average, avoiding broken downtrends. Capital is "
            "allocated proportional to momentum score — stronger signals get more weight."
        ),
        best_for="Most investors — best Sharpe ratio and crash resilience across market conditions.",
        s=s,
    ))

    story.append(PageBreak())

    story.append(strategy_card(
        "3", "Dual Momentum",
        research="Gary Antonacci, Dual Momentum Investing, 2014",
        signal="Relative rank + absolute return must be positive",
        allocation="Equal weight",
        risk_label="Low-Medium",
        body_text=(
            "Combines two momentum types. Relative momentum ranks stocks versus peers. "
            "Absolute momentum requires each stock's own 12-1 return to be positive — "
            "preventing selection of the 'best of a bad bunch' during falling markets. "
            "The critical feature: if the Nifty 50's own 12-month return turns negative, "
            "the strategy signals a full move to cash or liquid funds, keeping you out of "
            "prolonged bear markets entirely. Antonacci's research showed this mechanism "
            "reduced maximum drawdown from ~50% to ~22% without significantly sacrificing "
            "long-term returns. Ideal for investors who value capital preservation."
        ),
        best_for="Capital-preservation investors who cannot tolerate large drawdowns.",
        s=s,
    ))

    story.append(strategy_card(
        "4", "52-Week High Momentum",
        research="George & Hwang, Journal of Finance, 2004",
        signal="Current price ÷ 52-week high (nearness to high)",
        allocation="Equal weight",
        risk_label="Medium",
        body_text=(
            "Ranks stocks by how close they are to their 52-week high, rather than by "
            "raw past return. The behavioural rationale: investors anchor psychologically "
            "to the 52-week high as a perceived resistance level. When strong fundamentals "
            "eventually push a stock through this ceiling, pent-up buying pressure "
            "accelerates the breakout. George & Hwang found that this simple metric "
            "predicted future returns better than the conventional 12-month past return, "
            "and the effect is distinct from and incremental to classic momentum. "
            "Captures breakout dynamics that return-ranked strategies miss."
        ),
        best_for="Breakout investors; selects different stocks from return-ranked strategies.",
        s=s,
    ))

    story.append(PageBreak())
    return story


def page_comparison(s):
    """Page 5 — strategy comparison + investor profiles."""
    story = []
    story.append(section_heading_block("Choosing the Right Strategy", s))

    comp_headers = ["Strategy", "Signal", "Allocation", "Risk", "Bear Protection", "Best For"]
    comp_rows = [
        ["Classic Momentum",  "12-1 Return",           "Equal",            "High",     "None",             "Aggressive / bull markets"],
        ["Risk-Adjusted ★",   "Return ÷ Volatility",   "Return-weighted",  "Medium",   "Volatility filter","Most investors"],
        ["Dual Momentum",     "Relative + Absolute",   "Equal",            "Low-Med",  "Full cash signal", "Capital preservation"],
        ["52-Week High",      "Price ÷ 52W High",      "Equal",            "Medium",   "None",             "Breakout environments"],
    ]
    story.append(data_table(
        comp_headers, comp_rows,
        col_widths=[34*mm, 40*mm, 32*mm, 18*mm, 32*mm, 36*mm],
    ))
    story.append(sp(12))

    story.append(Paragraph("Match your profile to a strategy", s["h2"]))

    profiles = [
        ("New to systematic investing",
         "Start with Risk-Adjusted Momentum. Best-documented improvement over classic momentum with built-in volatility control and 200-DMA filter."),
        ("High risk tolerance, strong bull market",
         "Classic Momentum. Maximum upside capture with simple, transparent execution. Accept the higher crash risk."),
        ("Capital preservation is priority #1",
         "Dual Momentum. The cash signal keeps you out of bear markets entirely. Accept that you will miss early recovery rallies."),
        ("Want a differentiated angle",
         "52-Week High. Captures breakout dynamics; typically selects 30-50% different stocks from return-based strategies."),
        ("Running multiple capital pools",
         "Risk-Adjusted as primary (70%), Dual Momentum as secondary (30%) hedge. Do not run the same strategy twice."),
    ]

    p_label = ParagraphStyle("pl", fontSize=9, fontName="Helvetica-Bold", textColor=C_BG,
                             leading=12)
    p_body  = ParagraphStyle("pb", fontSize=9, fontName="Helvetica", textColor=C_TEXT,
                             leading=13)
    for i, (profile, rec) in enumerate(profiles):
        bg_left  = C_NAVY2 if i % 2 == 0 else C_NAVY3
        bg_right = C_LIGHT if i % 2 == 0 else C_WHITE
        t = _tbl([[Paragraph(profile, ParagraphStyle("pl2", fontSize=9, fontName="Helvetica-Bold",
                                                      textColor=C_WHITE, leading=12)),
                   Paragraph(rec, p_body)]],
                 [52 * mm, BODY_W - 52 * mm], [
            ("BACKGROUND",   (0, 0), (0, 0),   bg_left),
            ("BACKGROUND",   (1, 0), (1, 0),   bg_right),
            ("TOPPADDING",   (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
            ("LEFTPADDING",  (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("GRID",         (0, 0), (-1, -1), 0.3, C_BORDER),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ])
        story.append(t)

    story.append(PageBreak())
    return story


def page_metrics(s):
    """Page 6 — metrics table + market regime."""
    story = []
    story.append(section_heading_block("Understanding the Metrics", s))

    metrics_headers = ["Metric", "Formula", "What it tells you"]
    metrics_rows = [
        ["12-1 Return",
         "(Price 21 days ago / Price 252 days ago) - 1",
         "Core momentum. Skips last month to avoid short-term reversal."],
        ["12M Return",
         "(Current Price / Price 252 days ago) - 1",
         "Full 12-month return. Reference only — includes last month."],
        ["Annualised Volatility",
         "Daily log-return std x sqrt(252)",
         "How erratically the stock moves. Lower = smoother trend."],
        ["Risk-Adjusted Score",
         "12-1 Return / Ann. Volatility",
         "Reward per unit of risk. Primary ranking metric for Strategy 2."],
        ["52W Score",
         "Current Price / 52-Week High",
         "Nearness to breakout. 1.0 means exactly at 52-week high."],
        ["vs 52W High",
         "(Current / 52W High) - 1",
         "% below the 52-week high. Near 0% = approaching breakout."],
        ["Weight",
         "Stock return / Sum of all 15 returns  (or equal 1/15)",
         "Capital allocation %. Strategy-dependent (equal or return-weighted)."],
        ["Allocated (Rs)",
         "Weight x Total Capital",
         "Rupee amount to deploy in this stock this month."],
        ["Shares",
         "Floor(Allocated / CMP)",
         "Whole shares to buy. Rounded down — no fractional shares on NSE/BSE."],
    ]
    story.append(data_table(
        metrics_headers, metrics_rows,
        col_widths=[38 * mm, 68 * mm, 76 * mm],
    ))
    story.append(sp(12))

    story.append(Paragraph("Market Regime Filter", s["h2"]))
    story.append(Paragraph(
        "Every time the app loads, it checks whether the Nifty 50 index is above or below "
        "its 200-day simple moving average (SMA). This single macro filter provides a "
        "reliable regime signal — deploy in uptrends, reduce exposure in downtrends.",
        s["body"],
    ))
    story.append(sp(6))

    regime_headers = ["Signal", "Condition", "Recommended Action"]
    regime_rows = [
        ["GREEN — UPTREND",       "Nifty 50 above 200-day SMA",        "Deploy full capital as planned"],
        ["RED — DOWNTREND",       "Nifty 50 below 200-day SMA",        "Reduce position sizes by 50% or wait"],
        ["CASH (Dual only)",      "Nifty 50 12-month return < 0%",     "Move entirely to cash / liquid funds"],
    ]
    rt = Table(
        [[Paragraph(h, ParagraphStyle("rh", fontSize=8, fontName="Helvetica-Bold",
                                       textColor=C_WHITE, alignment=TA_CENTER, leading=10))
          for h in regime_headers]] +
        [[Paragraph(c, ParagraphStyle("rc", fontSize=8.5, fontName="Helvetica",
                                       textColor=C_TEXT, leading=12))
          for c in row]
         for row in regime_rows],
        colWidths=[46 * mm, 68 * mm, 68 * mm],
    )
    rt.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  C_BG),
        ("BACKGROUND",    (0, 1), (-1, 1),  C_GREEN_L),
        ("BACKGROUND",    (0, 2), (-1, 2),  C_RED_L),
        ("BACKGROUND",    (0, 3), (-1, 3),  C_GOLD_L),
        ("TEXTCOLOR",     (0, 1), (0, 1),   colors.HexColor("#15803d")),
        ("TEXTCOLOR",     (0, 2), (0, 2),   C_RED),
        ("TEXTCOLOR",     (0, 3), (0, 3),   colors.HexColor("#92400e")),
        ("FONTNAME",      (0, 1), (0, -1),  "Helvetica-Bold"),
        ("GRID",          (0, 0), (-1, -1), 0.35, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
    ]))
    story.append(rt)
    story.append(PageBreak())
    return story


def page_workflow(s):
    """Page 7 — monthly workflow."""
    story = []
    story.append(section_heading_block("Monthly Rebalancing Workflow", s))
    story.append(Paragraph(
        "Run the tool once per month on the <b>last trading day after market close</b> "
        "(after 3:30 PM IST). The entire process takes 5-10 minutes.",
        s["body"],
    ))
    story.append(sp(10))

    steps = [
        ("1", "Open the app",
         'Navigate to <a href="https://pick-momentum.streamlit.app" color="#3b82f6">'
         '<u>pick-momentum.streamlit.app</u></a>. No login required.'),
        ("2", "Upload last month's history",
         "In the Portfolio History section, upload your <b>momentum_history.json</b> "
         "saved last month. This enables rebalancing comparison and performance tracking."),
        ("3", "Check the Market Regime panel",
         "Green = deploy full capital as planned.  Red = reduce size by ~50% or pause. "
         "Dual Momentum cash signal = move entirely to liquid/debt funds."),
        ("4", "Select your strategy and enter capital",
         "Use the same strategy as last month. Enter your <b>current total capital</b> "
         "(include cash from any EXIT sales)."),
        ("5", "Click Run Strategy",
         "Data download takes 1-2 minutes on first run; near-instant if recently cached."),
        ("6", "Review the Rebalancing Actions table",
         "<b>NEW</b> = buy at next market open.  <b>HOLD</b> = no action.  "
         "<b>EXIT</b> = sell at next market open."),
        ("7", "Place orders",
         "Market open on the <b>first trading day of the new month</b>. "
         "Use CNC (delivery) orders. Avoid market orders in low-liquidity stocks."),
        ("8", "Save & Download History",
         "Click <b>Save Run & Download History</b>. This JSON file is your input for "
         "next month — store it safely."),
    ]

    step_num_st  = ParagraphStyle("sn", fontSize=14, fontName="Helvetica-Bold",
                                   textColor=C_WHITE, alignment=TA_CENTER)
    step_body_st = ParagraphStyle("sb", fontSize=9, fontName="Helvetica",
                                   textColor=C_TEXT, leading=13)
    step_title_st= ParagraphStyle("st", fontSize=9.5, fontName="Helvetica-Bold",
                                   textColor=C_BG, leading=13)

    for num, title, desc in steps:
        row = [[
            Paragraph(num, step_num_st),
            [Paragraph(title, step_title_st), Paragraph(desc, step_body_st)],
        ]]
        # Inner table for text cell
        inner_t = _tbl(
            [[Paragraph(title, step_title_st)],
             [Paragraph(desc, step_body_st)]],
            [BODY_W - 14 * mm],
            [("TOPPADDING",   (0, 0), (-1, -1), 1),
             ("BOTTOMPADDING",(0, 0), (-1, -1), 1),
             ("LEFTPADDING",  (0, 0), (-1, -1), 0),
             ("RIGHTPADDING", (0, 0), (-1, -1), 0)],
        )
        outer_t = _tbl(
            [[Paragraph(num, step_num_st), inner_t]],
            [12 * mm, BODY_W - 12 * mm],
            [("BACKGROUND",   (0, 0), (0, 0),   C_GREEN),
             ("BACKGROUND",   (1, 0), (1, 0),   C_WHITE),
             ("TOPPADDING",   (0, 0), (-1, -1), 7),
             ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
             ("LEFTPADDING",  (0, 0), (-1, -1), 6),
             ("RIGHTPADDING", (0, 0), (-1, -1), 8),
             ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
             ("BOX",          (0, 0), (-1, -1), 0.4, C_BORDER)],
        )
        story.append(outer_t)
        story.append(sp(3))

    story.append(sp(10))
    story.append(callout_box(
        "Best-practice reminders",
        [
            "Always run after market close — intraday prices skew momentum signals",
            "Place orders at market open next day, not at close on rebalancing day",
            "Stick to one strategy for at least 6-12 months before evaluating performance",
            "Budget for ~0.25-0.35% transaction cost per round trip (brokerage + STT + charges)",
            "Keep a simple trade log — note actual fill prices vs tool-shown CMP",
        ],
        bg=C_BG,
    ))

    story.append(PageBreak())
    return story


def page_risks(s):
    """Page 8 — risks and disclaimer."""
    story = []
    story.append(Paragraph(
        "Important Risks to Understand",
        ParagraphStyle("h1_red", fontSize=17, fontName="Helvetica-Bold",
                       textColor=C_RED, spaceBefore=10, spaceAfter=5, leading=20),
    ))
    story.append(hr(color=C_RED))

    risks = [
        ("Momentum Crash Risk",
         "All momentum strategies can experience sharp, sudden reversals — particularly "
         "after market bottoms when underperforming stocks recover quickly. In US markets, "
         "the classic momentum factor lost ~65% in two months in 2009. The 200-day SMA "
         "filter and Dual Momentum's cash signal reduce but do not eliminate this risk."),
        ("Transaction Costs",
         "Monthly rebalancing incurs brokerage, STT (0.1%), exchange charges, stamp duty, "
         "and market impact. Estimated 0.25–0.35% per round trip, or roughly 1.5–2.5% "
         "annually on a fully-churned portfolio. For a Rs 5 lakh portfolio: Rs 7,500–12,500 "
         "per year in costs. Factor this into your return expectations."),
        ("Data Limitations",
         "Price data from Yahoo Finance may have brief gaps, split-adjustment errors, or "
         "delayed updates for some NSE stocks. Always verify key prices on your broker "
         "platform before placing orders. Stocks that fail to download are automatically "
         "skipped — the portfolio may have fewer than 15 stocks if data is unavailable."),
        ("Regime Dependence",
         "Momentum strategies are directionally exposed to equity market returns — they "
         "are not market-neutral. In prolonged bear markets, even well-constructed momentum "
         "portfolios will lose money. Only Dual Momentum has a built-in mechanism to exit "
         "equities entirely via its cash signal."),
        ("Not Investment Advice",
         "This tool is for informational and educational purposes only. Past momentum "
         "performance does not guarantee future returns. The academic evidence cited covers "
         "long historical periods — individual strategy performance in any given year can "
         "vary significantly. Consult a SEBI-registered investment advisor before making "
         "investment decisions."),
    ]

    for risk_title, risk_body in risks:
        t = _tbl([[
            Paragraph(risk_title,
                      ParagraphStyle("rt", fontSize=9.5, fontName="Helvetica-Bold",
                                     textColor=C_RED, leading=13)),
            Paragraph(risk_body,
                      ParagraphStyle("rb", fontSize=9, fontName="Helvetica",
                                     textColor=C_TEXT, leading=13)),
        ]], [38 * mm, BODY_W - 38 * mm], [
            ("BACKGROUND",   (0, 0), (-1, -1), colors.HexColor("#fff7f7")),
            ("TOPPADDING",   (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
            ("LEFTPADDING",  (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
            ("LINEBEFORE",   (0, 0), (0, -1),  3, C_RED),
            ("BOX",          (0, 0), (-1, -1), 0.4, C_BORDER),
        ])
        story.append(t)
        story.append(sp(5))

    story.append(sp(10))

    # Final CTA
    cta_inner = [
        Paragraph(
            "Try the tool free",
            ParagraphStyle("cta1", fontSize=13, fontName="Helvetica-Bold",
                           textColor=C_WHITE, alignment=TA_CENTER),
        ),
        Paragraph(
            '<a href="https://pick-momentum.streamlit.app" color="#22c55e">'
            '<u>pick-momentum.streamlit.app</u></a>',
            ParagraphStyle("cta2", fontSize=14, fontName="Helvetica-Bold",
                           textColor=C_GREEN, alignment=TA_CENTER),
        ),
        sp(6),
        Paragraph(
            '<a href="https://github.com/tooweeknd/momentum-dashboard" color="#64748b">'
            '<u>github.com/tooweeknd/momentum-dashboard</u></a>'
            "  ·  Open source (MIT)  ·  No login  ·  No data stored",
            ParagraphStyle("cta3", fontSize=8.5, fontName="Helvetica",
                           textColor=C_MUTED, alignment=TA_CENTER, leading=13),
        ),
    ]
    cta_rows = [[item] for item in cta_inner]
    cta_t = _tbl([[r[0]] for r in cta_rows], [BODY_W], [
        ("BACKGROUND",   (0, 0), (-1, -1), C_BG),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING",   (0, 0), (0, 0),   14),
        ("BOTTOMPADDING",(0, -1),(0, -1),  14),
    ])
    story.append(cta_t)
    return story


# ── Main build ─────────────────────────────────────────────────────────────────

def build():
    out_path = "C:/Users/Durgesh/momentum-dashboard/Momentum_Portfolio_Tool.pdf"
    s = make_styles()

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=24 * mm, bottomMargin=24 * mm,
        title="Momentum Portfolio Tool",
        author="tooweeknd",
        subject="Research-backed momentum investing for NIFTY 500",
        creator="Momentum Portfolio Tool",
    )

    story = []
    story += page_cover(s)
    story += page_preview(s)
    story += page_strategies(s)
    story += page_comparison(s)
    story += page_metrics(s)
    story += page_workflow(s)
    story += page_risks(s)

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"PDF saved: {out_path}")


if __name__ == "__main__":
    build()
