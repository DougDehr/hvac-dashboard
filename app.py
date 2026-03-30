import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date, timedelta
import random

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AirFlow HVAC · Analytics",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* App shell */
  .stApp { background-color: #0D1117; }
  section[data-testid="stSidebar"] {
    background-color: #0D1117;
    border-right: 1px solid #21262D;
  }
  /* Remove default top padding */
  .block-container { padding-top: 48px !important; }

  /* Sidebar nav radio — make it look like a nav menu */
  [data-testid="stRadio"] > div { gap: 2px !important; }
  [data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    padding: 9px 14px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #8B949E !important;
  }
  [data-testid="stRadio"] label:hover { background: rgba(255,255,255,0.05) !important; }
  [data-testid="stRadio"] label[data-checked="true"] {
    background: rgba(33,150,243,0.12) !important;
    color: #58A6FF !important;
  }
  /* Hide radio circles */
  [data-testid="stRadio"] label > div:first-child { display: none !important; }

  /* KPI cards */
  .kpi-card {
    background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 18px 18px 14px;
    height: 100%;
    box-sizing: border-box;
  }
  .kpi-label {
    color: #8B949E;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .9px;
    margin-bottom: 10px;
  }
  .kpi-value {
    color: #E6EDF3;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -0.3px;
    line-height: 1.1;
  }
  .kpi-delta-pos { color: #3FB950; font-size: 11px; margin-top: 8px; font-weight: 500; }
  .kpi-delta-neg { color: #F85149; font-size: 11px; margin-top: 8px; font-weight: 500; }

  /* Segment cards */
  .seg-card {
    background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 16px 16px 12px;
  }
  .seg-card-metric-label {
    color: #8B949E;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .5px;
    margin-bottom: 3px;
  }
  .seg-card-metric-value {
    color: #E6EDF3;
    font-size: 16px;
    font-weight: 700;
  }

  /* Section divider */
  .divider { border: none; border-top: 1px solid #21262D; margin: 20px 0; }

  /* Page header */
  .page-title { color: #E6EDF3; font-size: 22px; font-weight: 700; margin-bottom: 2px; }
  .page-sub   { color: #8B949E; font-size: 12px; margin-bottom: 20px; }

  /* Chart section label */
  .chart-label { color: #8B949E; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .7px; margin-bottom: 6px; }

  /* Table tweaks */
  [data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
  [data-testid="stDataFrame"] th { background: #161B22 !important; }

  /* Sidebar label overrides */
  .sidebar-section-label {
    color: #8B949E;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
    display: block;
  }

  /* KPI drill-down expand buttons */
  .kpi-expand-btn button {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid #30363D !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    color: #8B949E !important;
    font-size: 10px !important;
    letter-spacing: .8px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    padding: 5px 0 !important;
    margin-top: 0 !important;
    transition: all 0.15s !important;
  }
  .kpi-expand-btn button:hover {
    color: #58A6FF !important;
    background: rgba(33,150,243,0.06) !important;
  }
  .kpi-expand-active button {
    color: #58A6FF !important;
    background: rgba(33,150,243,0.10) !important;
    border: 1px solid rgba(33,150,243,0.35) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    font-size: 10px !important;
    letter-spacing: .8px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    padding: 5px 0 !important;
    margin-top: 0 !important;
    width: 100% !important;
  }
  /* Detail panel */
  .kpi-detail-panel {
    background: linear-gradient(135deg, #0D1117, #161B22);
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 20px 24px;
    margin: 4px 0 20px;
  }
  .kpi-detail-title {
    color: #58A6FF;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 14px;
  }
  /* Forecast badge */
  .forecast-badge {
    display: inline-block;
    background: rgba(255,152,0,0.12);
    border: 1px solid rgba(255,152,0,0.4);
    color: #FF9800;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .7px;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
  }
</style>
""", unsafe_allow_html=True)

# ─── Design Tokens ────────────────────────────────────────────────────────────
BLUE   = "#2196F3"
GREEN  = "#4CAF50"
ORANGE = "#FF9800"
TEAL   = "#26C6DA"
RED    = "#EF5350"
PURPLE = "#AB47BC"

CHART_BG   = "#161B22"
PAPER_BG   = "#0D1117"
GRID_COL   = "#21262D"
TICK_COL   = "#8B949E"

ALL_SEGS = ["Education", "Office", "Restaurant", "Chip/Semiconductor"]

SEG_COLOR = {
    "Education":          BLUE,
    "Office":             TEAL,
    "Restaurant":         GREEN,
    "Chip/Semiconductor": ORANGE,
}

SEG_COLS = {
    "Education":          ("education_rev",   "education_cogs"),
    "Office":             ("office_rev",       "office_cogs"),
    "Restaurant":         ("restaurant_rev",   "restaurant_cogs"),
    "Chip/Semiconductor": ("chip_rev",         "chip_cogs"),
}

CHART_CFG = dict(displayModeBar=False)

# ─── Data Generation ──────────────────────────────────────────────────────────
@st.cache_data
def generate_data():
    np.random.seed(42)
    random.seed(42)

    # Jan 2025 – Mar 2026: actuals   |   Apr 2026 – Dec 2026: forecast
    actual_months   = pd.date_range("2025-01-01", "2026-03-01", freq="MS")
    forecast_months = pd.date_range("2026-04-01", "2026-12-01", freq="MS")

    # Seasonal multipliers (0=Jan … 11=Dec)
    seasons = {
        "Education":          [1.10, 1.00, 1.15, 1.20, 1.10, 0.55, 0.35, 0.45, 1.35, 1.45, 1.20, 0.85],
        "Office":             [1.00, 0.95, 1.10, 1.22, 1.12, 0.60, 0.45, 0.55, 1.28, 1.32, 1.15, 0.80],
        "Restaurant":         [0.95, 0.90, 1.00, 1.05, 1.12, 1.18, 1.22, 1.18, 1.06, 1.00, 0.94, 0.94],
        "Chip/Semiconductor": [1.00, 0.75, 1.55, 0.65, 1.20, 0.88, 1.10, 1.35, 0.78, 1.62, 1.00, 0.88],
    }
    # Actual bases — calibrated so Jan-Mar 2026 ≈ $6 M
    bases_act  = {"Education": 403_000, "Office": 490_000,
                  "Restaurant": 200_000, "Chip/Semiconductor": 795_000}
    # Forecast bases — calibrated so full-year 2026 (Q1 actual + Q2-Q4 fcst) ≈ $30 M
    bases_fcst = {"Education": 567_000, "Office": 690_000,
                  "Restaurant": 282_000, "Chip/Semiconductor": 1_119_000}
    noise  = {"Education": (0.91,1.09), "Office": (0.89,1.11),
               "Restaurant": (0.95,1.05), "Chip/Semiconductor": (0.68,1.32)}
    cogs_r = {"Education": (0.62,0.67), "Office": (0.64,0.70),
               "Restaurant": (0.70,0.75), "Chip/Semiconductor": (0.57,0.62)}

    def _make_records(months, bases, is_forecast):
        recs = []
        for m in months:
            mi   = m.month - 1
            revs = {s: bases[s] * seasons[s][mi] * np.random.uniform(*noise[s]) for s in ALL_SEGS}
            cogs = {s: revs[s] * np.random.uniform(*cogs_r[s]) for s in ALL_SEGS}
            total = sum(revs.values())
            tc    = sum(cogs.values())
            gp    = total - tc
            opex  = total * np.random.uniform(0.18, 0.22)
            recs.append(dict(
                date=m,
                month_label=m.strftime("%b %Y"),
                is_forecast=is_forecast,
                education_rev=revs["Education"],      education_cogs=cogs["Education"],
                office_rev=revs["Office"],            office_cogs=cogs["Office"],
                restaurant_rev=revs["Restaurant"],    restaurant_cogs=cogs["Restaurant"],
                chip_rev=revs["Chip/Semiconductor"],  chip_cogs=cogs["Chip/Semiconductor"],
                total_rev=total, total_cogs=tc,
                gross_profit=gp, opex=opex, ebitda=gp - opex,
            ))
        return recs

    records  = _make_records(actual_months,   bases_act,  is_forecast=False)
    records += _make_records(forecast_months, bases_fcst, is_forecast=True)

    df = pd.DataFrame(records)
    df["projected_rev"] = df["total_rev"].rolling(3, center=True, min_periods=1).mean() * 1.06

    # ── Deals ──────────────────────────────────────────────────────────────────
    customers = [
        ("Riverside Unified School District", "Education"),
        ("Sunnyvale Community College",        "Education"),
        ("Oakwood High School",                "Education"),
        ("Mesa Elementary District",           "Education"),
        ("Valley Technical Institute",         "Education"),
        ("Northgate Office Plaza",             "Office"),
        ("Centennial Tower",                   "Office"),
        ("Harbor Business Park",               "Office"),
        ("Westside Corporate Center",          "Office"),
        ("Downtown Financial Suites",          "Office"),
        ("Pico Semiconductor",                 "Chip/Semiconductor"),
        ("NovaTech Fabrication",               "Chip/Semiconductor"),
        ("SiliconCore Systems",                "Chip/Semiconductor"),
        ("Apex Wafer Technologies",            "Chip/Semiconductor"),
        ("The Burger Collective",              "Restaurant"),
        ("Golden Gate Bistro Group",           "Restaurant"),
        ("Pacific Rim Dining",                 "Restaurant"),
        ("Sunset Grill Chain",                 "Restaurant"),
        ("Harbor View Kitchen",                "Restaurant"),
        ("Urban Eats Franchise",               "Restaurant"),
    ]
    job_types = [
        "New Installation", "System Upgrade", "Maintenance Contract",
        "Emergency Repair", "Chiller Replacement", "Air Handler Install",
        "Controls Upgrade", "Preventive Maintenance",
    ]
    status_pool = [
        "Closed Won", "Closed Won", "Closed Won", "Closed Won",
        "In Progress", "In Progress", "Proposal Sent", "Closed Lost",
    ]
    val_range = {
        "Chip/Semiconductor": (180_000, 950_000),
        "Education":          (45_000,  285_000),
        "Office":             (32_000,  220_000),
        "Restaurant":         (8_000,    72_000),
    }
    deal_dates = pd.date_range("2025-01-04", "2026-03-20", freq="6D")
    deals = []
    for d in deal_dates[:65]:
        cust, seg = random.choice(customers)
        lo, hi = val_range[seg]
        deals.append(dict(
            Customer=cust, Segment=seg,
            Job_Type=random.choice(job_types),
            Value=random.randint(lo, hi),
            Status=random.choice(status_pool),
            Close_Date=d.strftime("%Y-%m-%d"),
        ))
    return df, pd.DataFrame(deals)


monthly_df, deals_df = generate_data()

# ─── Session State ────────────────────────────────────────────────────────────
if "drill_seg" not in st.session_state:
    st.session_state.drill_seg = None
if "active_kpi" not in st.session_state:
    st.session_state.active_kpi = None

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand
    st.markdown("""
    <div style="padding:22px 4px 14px;text-align:center">
      <div style="font-size:38px;line-height:1">❄️</div>
      <div style="font-size:18px;font-weight:700;color:#E6EDF3;margin-top:8px">AirFlow HVAC</div>
      <div style="font-size:10px;color:#8B949E;letter-spacing:2px;margin-top:3px;font-weight:600">ANALYTICS</div>
    </div>
    <hr style="border:none;border-top:1px solid #21262D;margin:0 0 14px">
    """, unsafe_allow_html=True)

    # Navigation
    st.markdown('<span class="sidebar-section-label">Navigation</span>', unsafe_allow_html=True)
    page = st.radio(
        "nav",
        ["📈  Sales", "💰  Finance", "🏢  Segments", "📋  Jobs", "📊  LRP"],
        label_visibility="collapsed",
    )

    st.markdown('<hr style="border:none;border-top:1px solid #21262D;margin:14px 0">', unsafe_allow_html=True)

    # Date range
    st.markdown('<span class="sidebar-section-label">Date Range</span>', unsafe_allow_html=True)
    min_d = monthly_df["date"].min().date()
    max_d = monthly_df["date"].max().date()
    ca, cb = st.columns(2)
    with ca:
        start_date = st.date_input("From", value=date(2026, 1, 1), min_value=min_d, max_value=max_d)
    with cb:
        end_date = st.date_input("To",   value=date(2026, 3, 1), min_value=min_d, max_value=max_d)

    st.markdown('<hr style="border:none;border-top:1px solid #21262D;margin:14px 0">', unsafe_allow_html=True)

    # Segment filter chips
    st.markdown('<span class="sidebar-section-label">Segments</span>', unsafe_allow_html=True)
    seg_options = ["All", "Education", "Chip/Semi", "Office", "Restaurant"]
    try:
        selected_pills = st.pills(
            "seg_filter",
            options=seg_options,
            selection_mode="multi",
            default=["All"],
            label_visibility="collapsed",
        )
    except AttributeError:
        # Fallback for Streamlit < 1.38
        selected_pills = st.multiselect(
            "Segments",
            options=seg_options,
            default=["All"],
            label_visibility="collapsed",
        )

    st.markdown('<hr style="border:none;border-top:1px solid #21262D;margin:14px 0">', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#8B949E;font-size:11px;text-align:center">Mock data · Jan 2025 – Mar 2026<br>'
        '<span style="color:#3FB950">●</span> Live · refreshed on load</div>',
        unsafe_allow_html=True,
    )

# ─── Resolve Active Segments ──────────────────────────────────────────────────
_pill_to_seg = {"Education": "Education", "Office": "Office",
                "Restaurant": "Restaurant", "Chip/Semi": "Chip/Semiconductor"}

if not selected_pills or "All" in selected_pills:
    active_segs = ALL_SEGS
else:
    active_segs = [_pill_to_seg[p] for p in selected_pills if p in _pill_to_seg] or ALL_SEGS

# ─── Filter Monthly Data ──────────────────────────────────────────────────────
date_mask = (monthly_df["date"] >= pd.Timestamp(start_date)) & \
            (monthly_df["date"] <= pd.Timestamp(end_date))
fdf = monthly_df[date_mask].copy()

rev_cols  = [SEG_COLS[s][0] for s in active_segs]
cogs_cols = [SEG_COLS[s][1] for s in active_segs]

fdf["seg_rev"]    = fdf[rev_cols].sum(axis=1)
fdf["seg_cogs"]   = fdf[cogs_cols].sum(axis=1)
fdf["seg_profit"] = fdf["seg_rev"] - fdf["seg_cogs"]

_safe_rev = fdf["total_rev"].replace(0, np.nan)
fdf["seg_projected"] = fdf["projected_rev"] * (fdf["seg_rev"] / _safe_rev)

_safe_seg = fdf["seg_rev"].replace(0, np.nan)
fdf["seg_gm_pct"] = fdf["seg_profit"] / _safe_seg * 100
fdf["seg_opex"]   = fdf["opex"] * (fdf["seg_rev"] / _safe_rev)
fdf["seg_ebitda"] = fdf["seg_profit"] - fdf["seg_opex"]
fdf["seg_nm_pct"] = fdf["seg_ebitda"] / _safe_seg * 100

# ─── Filter Deals ─────────────────────────────────────────────────────────────
deal_dt = pd.to_datetime(deals_df["Close_Date"])
deal_mask = (deal_dt >= pd.Timestamp(start_date)) & \
            (deal_dt <= pd.Timestamp(end_date) + timedelta(days=31))
fdeal = deals_df[deal_mask & deals_df["Segment"].isin(active_segs)].copy()

date_label = f"{start_date.strftime('%b %Y')} – {end_date.strftime('%b %Y')}"

# ─── Helpers ──────────────────────────────────────────────────────────────────
def fmt_usd(v):
    if v >= 1_000_000: return f"${v / 1_000_000:.2f}M"
    if v >= 1_000:     return f"${v / 1_000:.0f}K"
    return f"${v:.0f}"

def kpi_card(label, value, delta=None, positive=True, accent=BLUE):
    dhtml = ""
    if delta:
        arr = "▲" if positive else "▼"
        cls = "kpi-delta-pos" if positive else "kpi-delta-neg"
        dhtml = f'<div class="{cls}">{arr} {delta}</div>'
    return (
        f'<div class="kpi-card" style="border-left:4px solid {accent}">'
        f'  <div class="kpi-label">{label}</div>'
        f'  <div class="kpi-value">{value}</div>'
        f'  {dhtml}'
        f'</div>'
    )

def base_layout(fig, height=370, title="", legend=True, h_legend=True):
    leg_cfg = dict(
        orientation="h" if h_legend else "v",
        y=1.08 if h_legend else 0.5,
        x=0,
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color="#C9D1D9"),
    ) if legend else dict(visible=False)
    fig.update_layout(
        height=height,
        template="plotly_dark",
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=CHART_BG,
        title=dict(
            text=title,
            font=dict(size=12, color="#8B949E"),
            x=0, y=0.99, pad=dict(l=0, b=4),
        ) if title else dict(text=""),
        font=dict(family="Inter,ui-sans-serif,system-ui,sans-serif",
                  color="#C9D1D9", size=12),
        margin=dict(l=8, r=12, t=44 if title else 28, b=8),
        hovermode="x unified",
        legend=leg_cfg,
        xaxis=dict(gridcolor=GRID_COL, linecolor="#30363D",
                   tickfont=dict(color=TICK_COL), showgrid=False),
        yaxis=dict(gridcolor=GRID_COL, linecolor="#30363D",
                   tickfont=dict(color=TICK_COL)),
    )
    return fig

def sparkline_fig(series, color=BLUE, height=76):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fig = go.Figure(go.Scatter(
        y=series.values,
        mode="lines",
        line=dict(color=color, width=1.8),
        fill="tozeroy",
        fillcolor=f"rgba({r},{g},{b},0.15)",
        hoverinfo="skip",
    ))
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig

STATUS_ICON = {
    "Closed Won":    "🟢 Closed Won",
    "In Progress":   "🔵 In Progress",
    "Proposal Sent": "🟡 Proposal Sent",
    "Closed Lost":   "🔴 Closed Lost",
}

def render_deals_table(df_in, max_rows=None):
    d = df_in.copy()
    d["Status"] = d["Status"].map(STATUS_ICON)
    d["Value"]  = d["Value"].map(lambda v: f"${v:,.0f}")
    d.rename(columns={"Job_Type": "Job Type", "Close_Date": "Close Date"}, inplace=True)
    cols = ["Customer", "Segment", "Job Type", "Value", "Status", "Close Date"]
    # Only include Segment col if it's in the dataframe
    cols = [c for c in cols if c in d.columns]
    out = d.sort_values("Close Date", ascending=False)
    if max_rows:
        out = out.head(max_rows)
    st.dataframe(
        out[cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Customer":   st.column_config.TextColumn("Customer",   width="large"),
            "Segment":    st.column_config.TextColumn("Segment",    width="medium"),
            "Job Type":   st.column_config.TextColumn("Job Type",   width="medium"),
            "Value":      st.column_config.TextColumn("Value",      width="small"),
            "Status":     st.column_config.TextColumn("Status",     width="medium"),
            "Close Date": st.column_config.TextColumn("Close Date", width="small"),
        },
    )

def seg_summary(df_monthly, segs=None):
    segs = segs or active_segs
    rows = []
    for s in segs:
        rc, cc = SEG_COLS[s]
        rev  = df_monthly[rc].sum()
        cogs = df_monthly[cc].sum()
        gp   = rev - cogs
        gm   = gp / rev * 100 if rev else 0
        rows.append(dict(Segment=s, Revenue=rev, COGS=cogs, Gross_Profit=gp, Margin_Pct=gm))
    return pd.DataFrame(rows)

def section_divider():
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

def page_header(title, sub=None):
    sub_html = f'<div class="page-sub">{sub}</div>' if sub else ""
    st.markdown(f'<div class="page-title">{title}</div>{sub_html}', unsafe_allow_html=True)

def chart_label(text):
    st.markdown(f'<div class="chart-label">{text}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SALES
# ══════════════════════════════════════════════════════════════════════════════
if "Sales" in page:
    page_header("Sales Overview", date_label)

    # ── Derived metrics ───────────────────────────────────────────────────────
    # YTD = actual months in 2026 only (Jan–Mar), regardless of date filter
    ytd_df  = monthly_df[(monthly_df["is_forecast"] == False) &
                          (monthly_df["date"].dt.year == 2026)].copy()
    ytd_df["seg_rev"] = ytd_df[rev_cols].sum(axis=1)
    ytd_rev = ytd_df["seg_rev"].sum()                              # ≈ $6 M

    pipeline_deals = deals_df[deals_df["Status"].isin(["In Progress", "Proposal Sent"])]
    pipeline  = pipeline_deals["Value"].sum()
    won       = deals_df[deals_df["Status"] == "Closed Won"]
    n_closed  = len(won)
    avg_deal  = won["Value"].mean() if n_closed else 0

    n_reps         = 6
    annual_quota   = 520_000 * n_reps
    quota_attain   = ytd_rev / (annual_quota / 4) * 100   # vs Q1 quota
    rev_per_rep    = ytd_rev / n_reps
    avg_cycle_days = 42
    all_deals      = deals_df[deals_df["Segment"].isin(active_segs)]
    total_d        = len(all_deals)
    win_rate_pct   = len(all_deals[all_deals["Status"] == "Closed Won"]) / total_d * 100 if total_d else 0
    pipe_deals     = all_deals[all_deals["Status"].isin(["In Progress", "Proposal Sent"])]
    n_pipe         = len(pipe_deals)
    proj_close     = pipe_deals["Value"].sum() * (win_rate_pct / 100)

    qa_acc = GREEN if quota_attain >= 90 else (ORANGE if quota_attain >= 70 else RED)
    wr_acc = GREEN if win_rate_pct >= 60 else (ORANGE if win_rate_pct >= 40 else RED)

    # ── Helper: render a clickable KPI card ───────────────────────────────────
    def clickable_kpi(col_obj, kpi_key, lbl, val, delta, pos, acc):
        is_act = st.session_state.active_kpi == kpi_key
        with col_obj:
            st.markdown(kpi_card(lbl, val, delta, pos, acc), unsafe_allow_html=True)
            div_cls = "kpi-expand-active" if is_act else "kpi-expand-btn"
            st.markdown(f'<div class="{div_cls}">', unsafe_allow_html=True)
            btn_label = "▴ close" if is_act else "▾ view details"
            if st.button(btn_label, key=f"kpibtn_{kpi_key}", use_container_width=True):
                st.session_state.active_kpi = None if is_act else kpi_key
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 1 KPI cards ───────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    clickable_kpi(k1, "ytd_rev",   "Total Revenue YTD", fmt_usd(ytd_rev), "+18.4% vs Q1 prior year", True,  BLUE)
    clickable_kpi(k2, "pipeline",  "Pipeline Value",    fmt_usd(pipeline), "+8.1% vs last quarter",  True,  TEAL)
    clickable_kpi(k3, "deals",     "Deals Closed",      str(n_closed),     "+5 vs prior year",       True,  GREEN)
    clickable_kpi(k4, "avg_deal",  "Avg Deal Size",     fmt_usd(avg_deal), "+3.2% vs prior year",    True,  ORANGE)

    # ── Row 1 detail panel ────────────────────────────────────────────────────
    if st.session_state.active_kpi == "ytd_rev":
        st.markdown('<div class="kpi-detail-panel">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-detail-title">📊 Total Revenue YTD — Monthly Breakdown</div>', unsafe_allow_html=True)
        dc1, dc2 = st.columns([2, 1])
        with dc1:
            fig_d = go.Figure(go.Bar(
                x=ytd_df["month_label"], y=ytd_df["seg_rev"],
                marker_color=[BLUE, TEAL, GREEN], marker_opacity=0.85,
                hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
            ))
            fig_d.update_yaxes(tickprefix="$", tickformat=",.0f")
            base_layout(fig_d, height=220, legend=False, title="Jan–Mar 2026 Actuals")
            st.plotly_chart(fig_d, use_container_width=True, config=CHART_CFG)
        with dc2:
            st.markdown(f"""
            <div style="padding:16px 0">
              <div style="color:#8B949E;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px">YTD Actual</div>
              <div style="color:#E6EDF3;font-size:22px;font-weight:700">{fmt_usd(ytd_rev)}</div>
              <div style="color:#3FB950;font-size:11px;margin-top:4px">▲ +18.4% vs Q1 prior year</div>
              <div style="margin-top:16px;color:#8B949E;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px">Full-Year Forecast</div>
              <div style="color:{ORANGE};font-size:22px;font-weight:700">$30.00M</div>
              <div style="color:#8B949E;font-size:11px;margin-top:4px">{fmt_usd(ytd_rev)} actual + {fmt_usd(30_000_000-ytd_rev)} forecast</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.active_kpi == "pipeline":
        st.markdown('<div class="kpi-detail-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-detail-title">🔵 Pipeline Value — {fmt_usd(pipeline)} across {len(pipeline_deals)} deals</div>', unsafe_allow_html=True)
        # Segment subtotals
        pipe_seg = pipeline_deals.groupby("Segment")["Value"].agg(["sum","count"]).reset_index()
        pipe_seg.columns = ["Segment","Total Value","# Deals"]
        pipe_seg["Avg Deal"] = pipe_seg["Total Value"] / pipe_seg["# Deals"]
        pipe_seg_disp = pipe_seg.copy()
        pipe_seg_disp["Total Value"] = pipe_seg_disp["Total Value"].map(lambda v: f"${v:,.0f}")
        pipe_seg_disp["Avg Deal"]    = pipe_seg_disp["Avg Deal"].map(lambda v: f"${v:,.0f}")
        pc1, pc2 = st.columns([1, 2])
        with pc1:
            st.dataframe(pipe_seg_disp, use_container_width=True, hide_index=True)
        with pc2:
            pipe_deals_disp = pipeline_deals.copy()
            pipe_deals_disp["Value"] = pipe_deals_disp["Value"].map(lambda v: f"${v:,.0f}")
            pipe_deals_disp.rename(columns={"Job_Type":"Job Type","Close_Date":"Close Date","Status":"Status"}, inplace=True)
            st.dataframe(
                pipe_deals_disp.sort_values("Close Date", ascending=False)
                    [["Customer","Segment","Job Type","Value","Status","Close Date"]],
                use_container_width=True, hide_index=True, height=220,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.active_kpi == "deals":
        st.markdown('<div class="kpi-detail-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-detail-title">🟢 Closed Won Deals — {n_closed} total, {fmt_usd(won["Value"].sum())} booked</div>', unsafe_allow_html=True)
        won_disp = won.copy()
        won_disp["Value"] = won_disp["Value"].map(lambda v: f"${v:,.0f}")
        won_disp.rename(columns={"Job_Type":"Job Type","Close_Date":"Close Date"}, inplace=True)
        st.dataframe(
            won_disp.sort_values("Close Date", ascending=False)
                [["Customer","Segment","Job Type","Value","Close Date"]],
            use_container_width=True, hide_index=True, height=240,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.active_kpi == "avg_deal":
        st.markdown('<div class="kpi-detail-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-detail-title">💰 Avg Deal Size — {fmt_usd(avg_deal)} overall</div>', unsafe_allow_html=True)
        seg_avg = deals_df[deals_df["Status"] == "Closed Won"].groupby("Segment")["Value"].mean().reset_index()
        seg_avg.columns = ["Segment","Avg Deal Size"]
        fig_avg = go.Figure(go.Bar(
            x=seg_avg["Segment"], y=seg_avg["Avg Deal Size"],
            marker_color=[SEG_COLOR[s] for s in seg_avg["Segment"]],
            marker_opacity=0.85,
            text=seg_avg["Avg Deal Size"].map(lambda v: fmt_usd(v)),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Avg Deal: $%{y:,.0f}<extra></extra>",
        ))
        fig_avg.update_yaxes(tickprefix="$", tickformat=",.0f")
        base_layout(fig_avg, height=220, legend=False, title="Avg Closed Won Deal Size by Segment")
        st.plotly_chart(fig_avg, use_container_width=True, config=CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 2 productivity KPI cards ──────────────────────────────────────────
    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    p1, p2, p3, p4, p5, p6 = st.columns(6)
    clickable_kpi(p1, "quota",      "Quota Attainment",      f"{quota_attain:.0f}%",  "vs 80% Q1 target",    quota_attain >= 80, qa_acc)
    clickable_kpi(p2, "rev_rep",    "Revenue / Rep",         fmt_usd(rev_per_rep),    "+6.1% vs prior year", True,               BLUE)
    clickable_kpi(p3, "cycle",      "Avg Sales Cycle",       f"{avg_cycle_days}d",    "−4d vs prior year",   True,               TEAL)
    clickable_kpi(p4, "win_rate",   "Win Rate %",            f"{win_rate_pct:.0f}%",  "vs 55% target",       win_rate_pct >= 55, wr_acc)
    clickable_kpi(p5, "n_pipe",     "Deals in Pipeline",     str(n_pipe),             f"{n_pipe} active",    True,               ORANGE)
    clickable_kpi(p6, "proj_close", "Projected Close Value", fmt_usd(proj_close),     "pipeline × win rate", True,               PURPLE)

    # ── Row 2 detail panels ───────────────────────────────────────────────────
    if st.session_state.active_kpi == "win_rate":
        st.markdown('<div class="kpi-detail-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-detail-title">🎯 Win Rate — {win_rate_pct:.0f}% overall</div>', unsafe_allow_html=True)
        wr_seg = deals_df.groupby("Segment").apply(
            lambda g: pd.Series({"Won": (g["Status"]=="Closed Won").sum(),
                                  "Lost": (g["Status"]=="Closed Lost").sum(),
                                  "Total": len(g)})
        ).reset_index()
        wr_seg["Win Rate %"] = (wr_seg["Won"] / wr_seg["Total"] * 100).round(1)
        wc1, wc2 = st.columns([1, 2])
        with wc1:
            wr_disp = wr_seg.copy()
            wr_disp["Win Rate %"] = wr_disp["Win Rate %"].map(lambda v: f"{v:.1f}%")
            st.dataframe(wr_disp, use_container_width=True, hide_index=True)
        with wc2:
            fig_wr = go.Figure()
            fig_wr.add_trace(go.Bar(name="Won",  x=wr_seg["Segment"], y=wr_seg["Won"],
                                    marker_color=GREEN, marker_opacity=0.85,
                                    hovertemplate="<b>%{x}</b><br>Won: %{y}<extra></extra>"))
            fig_wr.add_trace(go.Bar(name="Lost", x=wr_seg["Segment"], y=wr_seg["Lost"],
                                    marker_color=RED, marker_opacity=0.85,
                                    hovertemplate="<b>%{x}</b><br>Lost: %{y}<extra></extra>"))
            fig_wr.update_layout(barmode="group")
            base_layout(fig_wr, height=220, title="Won vs Lost by Segment")
            st.plotly_chart(fig_wr, use_container_width=True, config=CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.active_kpi in ("n_pipe", "proj_close"):
        st.markdown('<div class="kpi-detail-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-detail-title">🔵 Pipeline Deals — {n_pipe} active, {fmt_usd(proj_close)} projected to close</div>', unsafe_allow_html=True)
        pd_disp = pipe_deals.copy()
        pd_disp["Value"] = pd_disp["Value"].map(lambda v: f"${v:,.0f}")
        pd_disp.rename(columns={"Job_Type":"Job Type","Close_Date":"Close Date"}, inplace=True)
        st.dataframe(
            pd_disp.sort_values("Value", ascending=False)
                [["Customer","Segment","Job Type","Value","Status","Close Date"]],
            use_container_width=True, hide_index=True, height=240,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.active_kpi in ("quota", "rev_rep"):
        st.markdown('<div class="kpi-detail-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-detail-title">👤 Rep Productivity — Q1 2026</div>', unsafe_allow_html=True)
        reps = [f"Rep {i+1}" for i in range(n_reps)]
        np.random.seed(7)
        rep_rev = np.random.uniform(0.6, 1.3, n_reps) * (ytd_rev / n_reps)
        rep_quota = annual_quota / 4 / n_reps
        rep_attain = rep_rev / rep_quota * 100
        rep_df = pd.DataFrame({"Rep": reps,
                                "Q1 Revenue": [fmt_usd(v) for v in rep_rev],
                                "Quota": fmt_usd(rep_quota),
                                "Attainment": [f"{v:.0f}%" for v in rep_attain]})
        st.dataframe(rep_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # ── Row 1: Actuals + Forecast chart  |  GM% by Segment ───────────────────
    r1, r2 = st.columns(2)

    with r1:
        # Always show full-year 2026: actuals (Jan–Mar) solid + forecast (Apr–Dec) dashed
        yr2026 = monthly_df[monthly_df["date"].dt.year == 2026].copy()
        yr2026["seg_rev"] = yr2026[rev_cols].sum(axis=1)
        act_26  = yr2026[yr2026["is_forecast"] == False]
        fcst_26 = yr2026[yr2026["is_forecast"] == True]
        # Include last actual in forecast trace so lines connect
        fcst_conn = pd.concat([act_26.tail(1), fcst_26])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=act_26["month_label"], y=act_26["seg_rev"],
            name="Actual",
            line=dict(color=BLUE, width=2.8),
            fill="tozeroy", fillcolor="rgba(33,150,243,0.12)",
            hovertemplate="<b>%{x}</b><br>Actual: $%{y:,.0f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=fcst_conn["month_label"], y=fcst_conn["seg_rev"],
            name="Forecast",
            line=dict(color=ORANGE, width=2.2, dash="dash"),
            fill="tozeroy", fillcolor="rgba(255,152,0,0.06)",
            hovertemplate="<b>%{x}</b><br>Forecast: $%{y:,.0f}<extra></extra>",
        ))
        # Actuals | Forecast divider — annotation added separately (add_vline annotation
        # fails on categorical axes in Plotly ≥ 5.20 because it tries to mean() strings)
        fig.add_vline(x="Mar 2026", line_dash="dot", line_color="#30363D", line_width=1)
        fig.add_annotation(x="Mar 2026", y=1.04, yref="paper", xref="x",
                           text="← Actual | Forecast →", showarrow=False,
                           font=dict(color="#8B949E", size=10), xanchor="center")
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        fig.update_xaxes(tickangle=-40)
        total_fcst_rev = yr2026["seg_rev"].sum()
        base_layout(fig, title=f"2026 Monthly Revenue — Actuals vs Forecast  (FY est. {fmt_usd(total_fcst_rev)})")
        st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

    with r2:
        sdf = seg_summary(fdf)
        fig2 = go.Figure(go.Bar(
            x=sdf["Margin_Pct"],
            y=sdf["Segment"],
            orientation="h",
            marker_color=[SEG_COLOR[s] for s in sdf["Segment"]],
            marker_opacity=0.85,
            text=sdf["Margin_Pct"].map(lambda v: f"{v:.1f}%"),
            textposition="outside",
            textfont=dict(color="#E6EDF3", size=12),
            hovertemplate="<b>%{y}</b><br>Gross Margin: %{x:.1f}%<extra></extra>",
        ))
        fig2.update_xaxes(ticksuffix="%", range=[0, 58])
        fig2.update_yaxes(automargin=True)
        base_layout(fig2, legend=False, title="Gross Margin % by Segment")
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CFG)

    # ── Row 2: Rev vs Cost (stacked)  |  Margin Trend ─────────────────────────
    r3, r4 = st.columns(2)

    with r3:
        sdf2 = seg_summary(fdf)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name="COGS", x=sdf2["Segment"], y=sdf2["COGS"],
            marker_color=RED, marker_opacity=0.85,
            hovertemplate="<b>%{x}</b><br>COGS: $%{y:,.0f}<extra></extra>",
        ))
        fig3.add_trace(go.Bar(
            name="Gross Profit", x=sdf2["Segment"], y=sdf2["Gross_Profit"],
            marker_color=GREEN, marker_opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Gross Profit: $%{y:,.0f}<extra></extra>",
        ))
        fig3.update_layout(barmode="stack")
        fig3.update_yaxes(tickprefix="$", tickformat=",.0f")
        base_layout(fig3, title="Revenue vs Cost by Segment")
        st.plotly_chart(fig3, use_container_width=True, config=CHART_CFG)

    with r4:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=fdf["month_label"], y=fdf["seg_gm_pct"],
            name="Gross Margin %",
            line=dict(color=GREEN, width=2.5),
            fill="tozeroy", fillcolor="rgba(76,175,80,0.08)",
            hovertemplate="<b>%{x}</b><br>Gross Margin: %{y:.1f}%<extra></extra>",
        ))
        fig4.add_trace(go.Scatter(
            x=fdf["month_label"], y=fdf["seg_nm_pct"],
            name="Net Margin %",
            line=dict(color=TEAL, width=2),
            hovertemplate="<b>%{x}</b><br>Net Margin: %{y:.1f}%<extra></extra>",
        ))
        fig4.update_yaxes(ticksuffix="%", tickformat=".1f")
        fig4.update_xaxes(tickangle=-40)
        base_layout(fig4, title="Margin Trend")
        st.plotly_chart(fig4, use_container_width=True, config=CHART_CFG)

    section_divider()

    st.markdown('<div class="chart-label">Recent Deals</div>', unsafe_allow_html=True)
    render_deals_table(fdeal, max_rows=25)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FINANCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Finance" in page:
    page_header("Finance & Margin Analysis", date_label)

    total_rev    = fdf["seg_rev"].sum()
    total_cogs   = fdf["seg_cogs"].sum()
    gross_profit = fdf["seg_profit"].sum()
    total_opex   = fdf["seg_opex"].sum()
    ebitda       = fdf["seg_ebitda"].sum()

    gm_pct = gross_profit / total_rev * 100 if total_rev else 0
    nm_pct = ebitda       / total_rev * 100 if total_rev else 0

    k1, k2, k3, k4 = st.columns(4)
    for col, lbl, val, delta, pos, acc in [
        (k1, "Gross Margin %", f"{gm_pct:.1f}%",              "+1.2pp vs prior year",  True,  GREEN),
        (k2, "Net Margin %",   f"{nm_pct:.1f}%",              "+0.8pp vs prior year",  True,  TEAL),
        (k3, "Total Costs",    fmt_usd(total_cogs + total_opex), "−3.1% vs prior year", False, ORANGE),
        (k4, "EBITDA",         fmt_usd(ebitda),               "+15.3% vs prior year",  True,  BLUE),
    ]:
        with col:
            st.markdown(kpi_card(lbl, val, delta, pos, acc), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    sdf = seg_summary(fdf)

    # ── Row 1: GM% bar  |  Rev vs COGS stacked ────────────────────────────────
    r1, r2 = st.columns(2)

    with r1:
        fig = go.Figure(go.Bar(
            x=sdf["Margin_Pct"], y=sdf["Segment"],
            orientation="h",
            marker_color=[SEG_COLOR[s] for s in sdf["Segment"]],
            marker_opacity=0.85,
            text=sdf["Margin_Pct"].map(lambda v: f"{v:.1f}%"),
            textposition="outside",
            textfont=dict(color="#E6EDF3", size=12),
            hovertemplate="<b>%{y}</b><br>Gross Margin: %{x:.1f}%<extra></extra>",
        ))
        fig.update_xaxes(ticksuffix="%", range=[0, 58])
        fig.update_yaxes(automargin=True)
        base_layout(fig, height=300, legend=False, title="Gross Margin % by Segment")
        st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

    with r2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="COGS", x=sdf["Segment"], y=sdf["COGS"],
            marker_color=RED, marker_opacity=0.85,
            hovertemplate="<b>%{x}</b><br>COGS: $%{y:,.0f}<extra></extra>",
        ))
        fig2.add_trace(go.Bar(
            name="Gross Profit", x=sdf["Segment"], y=sdf["Gross_Profit"],
            marker_color=GREEN, marker_opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Gross Profit: $%{y:,.0f}<extra></extra>",
        ))
        fig2.update_layout(barmode="stack")
        fig2.update_yaxes(tickprefix="$", tickformat=",.0f")
        base_layout(fig2, height=300, title="Revenue vs COGS by Segment")
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CFG)

    # ── Full-width Margin Trend ────────────────────────────────────────────────
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=fdf["month_label"], y=fdf["seg_gm_pct"],
        name="Gross Margin %",
        line=dict(color=GREEN, width=2.5),
        fill="tozeroy", fillcolor="rgba(76,175,80,0.08)",
        hovertemplate="<b>%{x}</b><br>Gross Margin: %{y:.1f}%<extra></extra>",
    ))
    fig3.add_trace(go.Scatter(
        x=fdf["month_label"], y=fdf["seg_nm_pct"],
        name="Net Margin %",
        line=dict(color=BLUE, width=2.5),
        fill="tozeroy", fillcolor="rgba(33,150,243,0.08)",
        hovertemplate="<b>%{x}</b><br>Net Margin: %{y:.1f}%<extra></extra>",
    ))
    fig3.update_yaxes(ticksuffix="%", tickformat=".1f")
    fig3.update_xaxes(tickangle=-40)
    base_layout(fig3, height=300, title="Margin Trend Over Period")
    st.plotly_chart(fig3, use_container_width=True, config=CHART_CFG)

    section_divider()

    # ── Segment Summary Table ──────────────────────────────────────────────────
    st.markdown('<div class="chart-label">Segment Financial Summary</div>', unsafe_allow_html=True)

    tbl = sdf.copy()
    totals = pd.DataFrame([{
        "Segment":      "TOTAL",
        "Revenue":      sdf["Revenue"].sum(),
        "COGS":         sdf["COGS"].sum(),
        "Gross_Profit": sdf["Gross_Profit"].sum(),
        "Margin_Pct":   (sdf["Gross_Profit"].sum() / sdf["Revenue"].sum() * 100
                         if sdf["Revenue"].sum() else 0),
    }])
    tbl = pd.concat([tbl, totals], ignore_index=True)
    tbl.rename(columns={"Gross_Profit": "Gross Profit", "Margin_Pct": "Margin %"}, inplace=True)
    for c in ["Revenue", "COGS", "Gross Profit"]:
        tbl[c] = tbl[c].map(lambda v: f"${v:,.0f}")
    tbl["Margin %"] = tbl["Margin %"].map(lambda v: f"{v:.1f}%")

    st.dataframe(tbl, use_container_width=True, hide_index=True,
                 column_config={
                     "Segment":      st.column_config.TextColumn("Segment",      width="medium"),
                     "Revenue":      st.column_config.TextColumn("Revenue",      width="medium"),
                     "COGS":         st.column_config.TextColumn("COGS",         width="medium"),
                     "Gross Profit": st.column_config.TextColumn("Gross Profit", width="medium"),
                     "Margin %":     st.column_config.TextColumn("Margin %",     width="small"),
                 })


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SEGMENTS
# ══════════════════════════════════════════════════════════════════════════════
elif "Segments" in page:
    page_header("Segment Overview",
                f"{date_label} · Click a card to drill into segment detail")

    # 4-column segment cards
    card_cols = st.columns(4)

    for i, seg in enumerate(ALL_SEGS):
        rc, cc  = SEG_COLS[seg]
        seg_rev = fdf[rc].sum()
        seg_cog = fdf[cc].sum()
        seg_gm  = (seg_rev - seg_cog) / seg_rev * 100 if seg_rev else 0
        seg_all_deals = deals_df[deals_df["Segment"] == seg]
        n_deals = len(seg_all_deals)
        avg_d   = seg_all_deals["Value"].mean() if n_deals else 0
        color   = SEG_COLOR[seg]
        is_active = st.session_state.drill_seg == seg

        with card_cols[i]:
            # Card body
            st.markdown(f"""
            <div class="seg-card" style="border-top:3px solid {color}">
              <div style="color:{color};font-size:10px;font-weight:700;
                          text-transform:uppercase;letter-spacing:1px;margin-bottom:14px">
                {seg}
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:12px">
                <div>
                  <div class="seg-card-metric-label">Revenue</div>
                  <div class="seg-card-metric-value">{fmt_usd(seg_rev)}</div>
                </div>
                <div style="text-align:right">
                  <div class="seg-card-metric-label">Margin</div>
                  <div class="seg-card-metric-value" style="color:{color}">{seg_gm:.1f}%</div>
                </div>
              </div>
              <div style="display:flex;justify-content:space-between">
                <div>
                  <div class="seg-card-metric-label">Deals</div>
                  <div class="seg-card-metric-value">{n_deals}</div>
                </div>
                <div style="text-align:right">
                  <div class="seg-card-metric-label">Avg Size</div>
                  <div class="seg-card-metric-value">{fmt_usd(avg_d)}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Sparkline
            st.plotly_chart(
                sparkline_fig(fdf[rc], color=color),
                use_container_width=True,
                config=CHART_CFG,
                key=f"spark_{seg}",
            )

            # Drill-down button
            btn_label = "▾ Viewing" if is_active else "View Details →"
            if st.button(btn_label, key=f"drill_{seg}", use_container_width=True):
                st.session_state.drill_seg = None if is_active else seg
                st.rerun()

    # ── Drill-down Detail ──────────────────────────────────────────────────────
    if st.session_state.drill_seg and st.session_state.drill_seg in ALL_SEGS:
        seg   = st.session_state.drill_seg
        rc, cc = SEG_COLS[seg]
        color  = SEG_COLOR[seg]
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

        section_divider()
        st.markdown(
            f'<div style="color:{color};font-size:17px;font-weight:700;margin-bottom:16px">'
            f'  📊 {seg} — Detailed View'
            f'</div>',
            unsafe_allow_html=True,
        )

        d1, d2 = st.columns(2)

        with d1:
            fig_r = go.Figure()
            fig_r.add_trace(go.Scatter(
                x=fdf["month_label"], y=fdf[rc],
                name="Revenue",
                line=dict(color=color, width=2.5),
                fill="tozeroy",
                fillcolor=f"rgba({r},{g},{b},0.10)",
                hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
            ))
            fig_r.update_yaxes(tickprefix="$", tickformat=",.0f")
            fig_r.update_xaxes(tickangle=-40)
            base_layout(fig_r, legend=False, title=f"{seg} — Monthly Revenue Trend")
            st.plotly_chart(fig_r, use_container_width=True, config=CHART_CFG)

        with d2:
            fig_c = go.Figure()
            fig_c.add_trace(go.Bar(
                x=fdf["month_label"], y=fdf[cc],
                name="COGS",
                marker_color=RED, marker_opacity=0.85,
                hovertemplate="<b>%{x}</b><br>COGS: $%{y:,.0f}<extra></extra>",
            ))
            fig_c.add_trace(go.Bar(
                x=fdf["month_label"], y=fdf[rc] - fdf[cc],
                name="Gross Profit",
                marker_color=color, marker_opacity=0.85,
                hovertemplate="<b>%{x}</b><br>Gross Profit: $%{y:,.0f}<extra></extra>",
            ))
            fig_c.update_layout(barmode="stack")
            fig_c.update_yaxes(tickprefix="$", tickformat=",.0f")
            fig_c.update_xaxes(tickangle=-40)
            base_layout(fig_c, title=f"{seg} — Revenue vs Cost")
            st.plotly_chart(fig_c, use_container_width=True, config=CHART_CFG)

        st.markdown(f'<div class="chart-label">Deals — {seg}</div>', unsafe_allow_html=True)
        seg_deals = deals_df[deals_df["Segment"] == seg].copy()
        render_deals_table(seg_deals)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: JOBS
# ══════════════════════════════════════════════════════════════════════════════
elif "Jobs" in page:
    page_header("Jobs Pipeline", date_label)

    # Summary KPIs
    total_jobs  = len(fdeal)
    total_value = fdeal["Value"].sum()
    won_count   = (fdeal["Status"] == "Closed Won").sum()
    active_count= (fdeal["Status"] == "In Progress").sum()
    win_rate    = won_count / total_jobs * 100 if total_jobs else 0

    k1, k2, k3, k4 = st.columns(4)
    for col, lbl, val, delta, pos, acc in [
        (k1, "Total Jobs",   str(total_jobs),       f"{active_count} in progress",  True,  BLUE),
        (k2, "Total Value",  fmt_usd(total_value),  "+9.8% vs prior year",          True,  GREEN),
        (k3, "Win Rate",     f"{win_rate:.0f}%",    "+2.1pp vs prior year",         True,  TEAL),
        (k4, "Jobs Won",     str(won_count),        f"of {total_jobs} total",       True,  ORANGE),
    ]:
        with col:
            st.markdown(kpi_card(lbl, val, delta, pos, acc), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Filter Controls ────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns([3, 2, 2])
    with fc1:
        search = st.text_input(
            "search", placeholder="🔍  Search by customer name…",
            label_visibility="collapsed",
        )
    with fc2:
        status_filter = st.multiselect(
            "status",
            options=["Closed Won", "In Progress", "Proposal Sent", "Closed Lost"],
            default=[],
            placeholder="All statuses",
            label_visibility="collapsed",
        )
    with fc3:
        seg_filter2 = st.multiselect(
            "seg2",
            options=ALL_SEGS,
            default=[],
            placeholder="All segments",
            label_visibility="collapsed",
        )

    # Apply filters
    jobs = fdeal.copy()
    if search:
        jobs = jobs[jobs["Customer"].str.contains(search, case=False, na=False)]
    if status_filter:
        jobs = jobs[jobs["Status"].isin(status_filter)]
    if seg_filter2:
        jobs = jobs[jobs["Segment"].isin(seg_filter2)]

    st.markdown(
        f'<div style="color:#8B949E;font-size:11px;margin:6px 0 8px">'
        f'  Showing {len(jobs)} of {total_jobs} jobs'
        f'</div>',
        unsafe_allow_html=True,
    )

    render_deals_table(jobs)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LRP  (Long Range Plan)
# ══════════════════════════════════════════════════════════════════════════════
elif "LRP" in page:
    page_header("Long Range Plan — Revenue & Headcount Model")

    # ── Model Inputs ──────────────────────────────────────────────────────────
    st.markdown(
        '<div style="background:linear-gradient(135deg,#161B22,#1C2333);'
        'border:1px solid #30363D;border-radius:10px;padding:20px 24px 16px;margin-bottom:24px">'
        '<div style="color:#8B949E;font-size:10px;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.9px;margin-bottom:16px">Model Inputs</div>',
        unsafe_allow_html=True,
    )

    ir1c1, ir1c2, ir1c3, ir1c4, ir1c5, ir1c6 = st.columns(6)
    with ir1c1:
        target_26 = st.number_input("2026 Target ($M)", min_value=1.0, max_value=200.0, value=30.0, step=1.0)
    with ir1c2:
        target_27 = st.number_input("2027 Target ($M)", min_value=1.0, max_value=200.0, value=40.0, step=1.0)
    with ir1c3:
        target_28 = st.number_input("2028 Target ($M)", min_value=1.0, max_value=200.0, value=50.0, step=1.0)
    with ir1c4:
        quota_per_rep = st.slider("Quota / Rep ($K)", min_value=300, max_value=2000, value=500, step=25, format="$%dK")
    with ir1c5:
        attainment_pct = st.slider("Attainment %", min_value=50, max_value=100, value=75, step=5, format="%d%%")
    with ir1c6:
        ramp_months = st.slider("Ramp Time (mo)", min_value=1, max_value=6, value=3, step=1)

    ir2c1, ir2c2, _ = st.columns([1, 1, 4])
    with ir2c1:
        current_reps  = st.number_input("Current Reps", min_value=1, max_value=200, value=6, step=1)
    with ir2c2:
        current_rev_m = st.number_input("Current Rev ($M)", min_value=0.1, max_value=200.0, value=6.0, step=0.5, format="%.1f")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Core Math ─────────────────────────────────────────────────────────────
    eff_rev_per_rep = (quota_per_rep * 1_000) * (attainment_pct / 100)
    year_targets    = {2026: target_26 * 1e6, 2027: target_27 * 1e6, 2028: target_28 * 1e6}
    ramp_qtrs       = max(1, int(np.ceil(ramp_months / 3)))

    # Cumulative reps needed at end of each year
    reps_cum = {yr: int(np.ceil(t / eff_rev_per_rep)) for yr, t in year_targets.items()}

    # Incremental hires per year
    hires_yr = {
        2026: max(0, reps_cum[2026] - current_reps),
        2027: max(0, reps_cum[2027] - reps_cum[2026]),
        2028: max(0, reps_cum[2028] - reps_cum[2027]),
    }
    total_to_hire = sum(hires_yr.values())

    # Spread each year's hires evenly across that year's 4 quarters
    # Quarter index: 0–3 = 2026, 4–7 = 2027, 8–11 = 2028
    hires_by_q = []
    for yr in [2026, 2027, 2028]:
        h = hires_yr[yr]
        base, rem = h // 4, h % 4
        hires_by_q.extend([base + (1 if i < rem else 0) for i in range(4)])

    rev_gap_26   = max(0.0, year_targets[2026] - current_rev_m * 1e6)
    gap_color    = GREEN if rev_gap_26 == 0 else (ORANGE if rev_gap_26 < year_targets[2026] * 0.25 else RED)
    hire_color   = GREEN if total_to_hire == 0 else (ORANGE if total_to_hire <= 5 else RED)

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    lk1, lk2, lk3, lk4, lk5, lk6 = st.columns(6)
    for col, lbl, val, delta, pos, acc in [
        (lk1, "2026 Target",       f"${target_26:.0f}M",      "Year 1 goal",                  True,               BLUE),
        (lk2, "2027 Target",       f"${target_27:.0f}M",      "Year 2 goal",                  True,               TEAL),
        (lk3, "2028 Target",       f"${target_28:.0f}M",      "Year 3 goal",                  True,               GREEN),
        (lk4, "Reps by 2028",      str(reps_cum[2028]),       f"need {reps_cum[2028]} total",  True,               ORANGE),
        (lk5, "Total to Hire",     str(total_to_hire),        f"have {current_reps} today",   total_to_hire == 0, hire_color),
        (lk6, "2026 Revenue Gap",  fmt_usd(rev_gap_26),       f"to ${target_26:.0f}M target", rev_gap_26 == 0,    gap_color),
    ]:
        with col:
            st.markdown(kpi_card(lbl, val, delta, pos, acc), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Formula Callout ────────────────────────────────────────────────────────
    formula_color = GREEN if total_to_hire == 0 else (ORANGE if total_to_hire <= 5 else RED)
    hire_sentence = (
        "Your current team can cover the plan — no new hires required."
        if total_to_hire == 0
        else (f"You have <strong>{current_reps}</strong> today. "
              f"Hire <strong style='color:{formula_color}'>{total_to_hire} more</strong> "
              f"across 12 quarters ({hires_yr[2026]} in 2026 · {hires_yr[2027]} in 2027 · {hires_yr[2028]} in 2028).")
    )
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#161B22,#1C2333);border:1px solid #30363D;
                border-left:5px solid {formula_color};border-radius:10px;
                padding:22px 28px;margin-bottom:20px">
      <div style="color:#8B949E;font-size:10px;font-weight:700;text-transform:uppercase;
                  letter-spacing:.9px;margin-bottom:12px">3-Year Plan Breakdown</div>
      <div style="color:#E6EDF3;font-size:17px;font-weight:600;line-height:1.7">
        To hit
        <span style="color:{BLUE};">${target_26:.0f}M</span> →
        <span style="color:{TEAL};">${target_27:.0f}M</span> →
        <span style="color:{GREEN};">${target_28:.0f}M</span>
        at <span style="color:{ORANGE};">{attainment_pct}% attainment</span>
        on a <span style="color:{ORANGE};">${quota_per_rep:,}K quota</span>,
        you need <span style="color:{formula_color};font-size:22px;font-weight:800;">{reps_cum[2028]} reps</span> by end of 2028.
        {hire_sentence}
      </div>
      <div style="margin-top:14px;color:#8B949E;font-size:12px;line-height:1.8">
        <span style="color:#C9D1D9">Rev / rep (effective):</span> {fmt_usd(eff_rev_per_rep)} &nbsp;·&nbsp;
        <span style="color:#C9D1D9">Ramp time:</span> {ramp_months} mo ({ramp_qtrs} qtrs) &nbsp;·&nbsp;
        <span style="color:#C9D1D9">2026 reps needed:</span> {reps_cum[2026]} &nbsp;·&nbsp;
        <span style="color:#C9D1D9">2027 reps needed:</span> {reps_cum[2027]}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Build 12-Quarter Revenue Model ────────────────────────────────────────
    quarters_12 = [f"Q{q+1} {yr}" for yr in [2026, 2027, 2028] for q in range(4)]
    yr_for_q    = [yr for yr in [2026, 2027, 2028] for _ in range(4)]

    # Revenue per quarter per cohort
    cohort_keys = ["Current Team", "2026 Hires", "2027 Hires", "2028 Hires"]
    cohort_hire_start_q = {
        "2026 Hires": 0,   # hired across Q0–Q3 (2026)
        "2027 Hires": 4,   # hired across Q4–Q7 (2027)
        "2028 Hires": 8,   # hired across Q8–Q11 (2028)
    }
    cohort_colors_map = {
        "Current Team": BLUE,
        "2026 Hires":   GREEN,
        "2027 Hires":   TEAL,
        "2028 Hires":   ORANGE,
    }

    # For each quarter, compute revenue contribution by cohort
    qtr_rev_by_cohort = {k: [] for k in cohort_keys}
    hire_plan_rows = []
    cumulative_reps_count = current_reps

    for qi in range(12):
        yr = yr_for_q[qi]
        yr_tgt = year_targets[yr]

        # Current team
        curr_q = current_reps * eff_rev_per_rep / 4
        qtr_rev_by_cohort["Current Team"].append(curr_q)

        # New hire cohorts — hires_by_q[j] reps hired in quarter j
        for cohort, start_q in cohort_hire_start_q.items():
            contrib = 0.0
            for j in range(start_q, min(start_q + 4, qi + 1)):
                qtrs_since = qi - j
                if qtrs_since == 0:
                    ramp_pct = 0.5
                elif qtrs_since < ramp_qtrs:
                    ramp_pct = 0.5 + 0.5 * (qtrs_since / ramp_qtrs)
                else:
                    ramp_pct = 1.0
                contrib += hires_by_q[j] * eff_rev_per_rep / 4 * ramp_pct
            qtr_rev_by_cohort[cohort].append(contrib)

        total_q = sum(v[qi] for v in qtr_rev_by_cohort.values())
        cumulative_reps_count += hires_by_q[qi]

        hire_plan_rows.append({
            "Quarter":         quarters_12[qi],
            "Year Target":     fmt_usd(yr_tgt),
            "Reps to Hire":    hires_by_q[qi],
            "Cumul. Reps":     cumulative_reps_count,
            "Proj. Qtr Rev":   total_q,
            "Ann. Run Rate":   total_q * 4,
            "Gap to Yr Target": max(0, yr_tgt - total_q * 4),
        })

    plan_df = pd.DataFrame(hire_plan_rows)

    # ── Row 1: Growth Curve  |  Cohort Bar ────────────────────────────────────
    ch1, ch2 = st.columns(2)

    with ch1:
        qtr_totals = [sum(qtr_rev_by_cohort[k][qi] for k in cohort_keys) / 1e6
                      for qi in range(12)]
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Scatter(
            x=quarters_12, y=qtr_totals,
            name="Quarterly Revenue",
            line=dict(color=BLUE, width=2.8),
            fill="tozeroy", fillcolor="rgba(33,150,243,0.10)",
            mode="lines+markers", marker=dict(size=5, color=BLUE),
            hovertemplate="<b>%{x}</b><br>Qtr Rev: $%{y:.2f}M<extra></extra>",
        ))
        fig_growth.update_yaxes(tickprefix="$", ticksuffix="M", tickformat=".1f")
        fig_growth.update_xaxes(tickangle=-40)
        base_layout(fig_growth, title="Quarterly Revenue Growth — 2026–2028", legend=False)
        st.plotly_chart(fig_growth, use_container_width=True, config=CHART_CFG)

    with ch2:
        fig_cohort = go.Figure()
        for cohort in cohort_keys:
            vals = [v / 1e6 for v in qtr_rev_by_cohort[cohort]]
            fig_cohort.add_trace(go.Bar(
                name=cohort, x=quarters_12, y=vals,
                marker_color=cohort_colors_map[cohort], marker_opacity=0.85,
                hovertemplate=f"<b>%{{x}}</b><br>{cohort}: $%{{y:.2f}}M<extra></extra>",
            ))
        fig_cohort.update_layout(barmode="stack")
        fig_cohort.update_yaxes(tickprefix="$", ticksuffix="M", tickformat=".1f")
        fig_cohort.update_xaxes(tickangle=-40)
        base_layout(fig_cohort, title="Revenue by Rep Cohort — 2026–2028")
        st.plotly_chart(fig_cohort, use_container_width=True, config=CHART_CFG)

    section_divider()

    # ── Hiring Plan Table ──────────────────────────────────────────────────────
    st.markdown('<div class="chart-label">3-Year Hiring Plan by Quarter</div>', unsafe_allow_html=True)

    disp_plan = plan_df.copy()
    disp_plan["Proj. Qtr Rev"]    = disp_plan["Proj. Qtr Rev"].map(lambda v: f"${v/1e6:.2f}M")
    disp_plan["Ann. Run Rate"]    = disp_plan["Ann. Run Rate"].map(lambda v: f"${v/1e6:.2f}M")
    disp_plan["Gap to Yr Target"] = disp_plan["Gap to Yr Target"].map(
        lambda v: "✅ On Target" if v < 1_000 else f"${v/1e6:.2f}M"
    )

    st.dataframe(
        disp_plan,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Quarter":         st.column_config.TextColumn("Quarter",          width="small"),
            "Year Target":     st.column_config.TextColumn("Year Target",      width="small"),
            "Reps to Hire":    st.column_config.NumberColumn("Hire This Qtr",  width="small"),
            "Cumul. Reps":     st.column_config.NumberColumn("Cumul. Reps",    width="small"),
            "Proj. Qtr Rev":   st.column_config.TextColumn("Proj. Qtr Rev",   width="medium"),
            "Ann. Run Rate":   st.column_config.TextColumn("Ann. Run Rate",   width="medium"),
            "Gap to Yr Target":st.column_config.TextColumn("Gap to Yr Target",width="medium"),
        },
    )
