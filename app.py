import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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
  [data-testid="stRadio"] > label,
  [data-testid="stRadio"] [data-testid="stWidgetLabel"] { display: none !important; }
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

    # Seasonal multipliers (0=Jan … 11=Dec) — summer peak for upstate NY cooling demand
    seasons = {
        "Education":          [1.10, 1.00, 1.15, 1.15, 1.30, 1.50, 1.45, 1.32, 1.10, 0.85, 0.75, 0.78],
        "Office":             [1.00, 0.95, 1.10, 1.20, 1.35, 1.50, 1.48, 1.35, 1.15, 0.90, 0.80, 0.78],
        "Restaurant":         [0.95, 0.90, 1.00, 1.08, 1.15, 1.22, 1.28, 1.22, 1.10, 1.00, 0.94, 0.94],
        "Chip/Semiconductor": [1.00, 0.75, 1.55, 1.10, 1.30, 1.52, 1.58, 1.42, 1.15, 0.88, 0.82, 0.88],
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
if "estimates" not in st.session_state:
    st.session_state.estimates = []
if "show_weather" not in st.session_state:
    st.session_state.show_weather = False

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
    page = st.radio(
        " ",
        ["📈  Sales", "💰  Finance", "🏢  Segments", "📋  Jobs", "📊  LRP", "🔀  Pipeline", "🗺️  Territory"],
        label_visibility="collapsed",
    )

    st.markdown('<hr style="border:none;border-top:1px solid #21262D;margin:14px 0">', unsafe_allow_html=True)

    # Date range
    st.markdown('<span class="sidebar-section-label">Date Range</span>', unsafe_allow_html=True)
    min_d = monthly_df["date"].min().date()
    max_d = monthly_df["date"].max().date()
    ca, cb = st.columns(2)
    with ca:
        start_date = st.date_input("From", value=date(2025, 1, 1), min_value=min_d, max_value=max_d)
    with cb:
        end_date = st.date_input("To",   value=date(2025, 12, 1), min_value=min_d, max_value=max_d)

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
    annual_quota   = 3_600_000 * n_reps          # $3.6M per rep annually → Q1 quota ~$5.4M → ~110% attainment
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
        show_weather = st.checkbox("🌡️ Temperature overlay", value=st.session_state.show_weather, key="wx_toggle")
        st.session_state.show_weather = show_weather

        yr2026 = monthly_df[monthly_df["date"].dt.year == 2026].copy()
        yr2026["seg_rev"] = yr2026[rev_cols].sum(axis=1)
        act_26  = yr2026[yr2026["is_forecast"] == False]
        fcst_26 = yr2026[yr2026["is_forecast"] == True]
        # Include last actual in forecast trace so lines connect
        fcst_conn = pd.concat([act_26.tail(1), fcst_26])

        # Monthly avg temp °F for 2026 (seasonal curve, peaks ~90°F in July)
        def _temp_f(month_num):
            return 57 + 38 * np.sin((month_num - 1 - 2) * np.pi / 6)
        yr2026["temp_f"] = yr2026["date"].dt.month.map(_temp_f)

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
        if show_weather:
            fig.add_trace(go.Scatter(
                x=yr2026["month_label"], y=yr2026["temp_f"],
                name="Avg Temp °F",
                line=dict(color=ORANGE, width=1.5, dash="dot"),
                fill="tozeroy", fillcolor="rgba(255,152,0,0.06)",
                yaxis="y2",
                hovertemplate="<b>%{x}</b><br>Avg Temp: %{y:.0f}°F<extra></extra>",
            ))
            # Correlation between actual rev and temp
            act_temp = yr2026[yr2026["is_forecast"] == False]["temp_f"].values
            act_rev_vals = act_26["seg_rev"].values
            if len(act_temp) > 1:
                corr = np.corrcoef(act_rev_vals, act_temp)[0, 1] * 100
            else:
                corr = 0
            fig.update_layout(
                yaxis2=dict(title="°F", overlaying="y", side="right",
                            showgrid=False, tickfont=dict(color=ORANGE, size=10),
                            range=[0, 120]),
            )

        fig.update_layout(yaxis=dict(tickprefix="$", tickformat=",.0f"))
        fig.update_xaxes(tickangle=-40)
        total_fcst_rev = yr2026["seg_rev"].sum()
        wx_note = "  🌡️ +temp" if show_weather else ""
        base_layout(fig, title=f"2026 Monthly Revenue — Actuals vs Forecast  (FY est. {fmt_usd(total_fcst_rev)}){wx_note}")
        st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)
        if show_weather:
            st.caption(f"📊 Revenue correlates **{corr:.0f}%** with avg monthly temperature (actuals only)")

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

    section_divider()
    st.markdown('<div class="chart-title" style="color:#C9D1D9;font-size:13px;font-weight:600;margin-bottom:8px">Seasonal Forecast — Next 90 Days</div>', unsafe_allow_html=True)

    # Use last 15 months of actuals to project Apr/May/Jun 2026
    hist = monthly_df[monthly_df["is_forecast"] == False].copy()
    hist["seg_rev"] = hist[rev_cols].sum(axis=1)

    # Simple seasonal projection: same 3 months from prior year × YoY growth rate
    # Find Apr/May/Jun 2025 as baseline
    prior = hist[hist["date"].dt.month.isin([4, 5, 6]) & (hist["date"].dt.year == 2025)]["seg_rev"].values
    recent_3  = hist.tail(3)["seg_rev"].mean()
    prior_3   = hist[hist["date"].dt.month.isin([1, 2, 3]) & (hist["date"].dt.year == 2025)]["seg_rev"].mean()
    yoy_growth = recent_3 / prior_3 if prior_3 else 1.1

    forecast_months_90 = ["Apr 2026", "May 2026", "Jun 2026"]
    forecast_vals = prior * yoy_growth if len(prior) == 3 else np.array([recent_3 * 1.05, recent_3 * 1.08, recent_3 * 0.95])
    conf_upper = forecast_vals * 1.12
    conf_lower = forecast_vals * 0.88

    # KPI cards: 30/60/90 day projections
    f1, f2, f3 = st.columns(3)
    for col, lbl, val, acc in [
        (f1, "Next 30 Days",  forecast_vals[0],   BLUE),
        (f2, "Next 60 Days",  forecast_vals[:2].sum(), TEAL),
        (f3, "Next 90 Days",  forecast_vals.sum(), GREEN),
    ]:
        with col:
            st.markdown(kpi_card(lbl, fmt_usd(val), "projected", True, acc), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # Build chart: last 6 months actual + 3 month forecast with confidence band
    hist_tail = hist.tail(6)
    connector_label = hist_tail.iloc[-1]["month_label"]
    connector_val   = hist_tail.iloc[-1]["seg_rev"]

    fig_fc = go.Figure()
    # Confidence band (filled area)
    fig_fc.add_trace(go.Scatter(
        x=forecast_months_90 + forecast_months_90[::-1],
        y=list(conf_upper) + list(conf_lower[::-1]),
        fill="toself", fillcolor="rgba(76,175,80,0.12)",
        line=dict(color="rgba(0,0,0,0)"),
        name="90% Confidence", showlegend=True,
        hoverinfo="skip",
    ))
    # Historical actuals
    fig_fc.add_trace(go.Scatter(
        x=hist_tail["month_label"], y=hist_tail["seg_rev"],
        name="Actual", line=dict(color=BLUE, width=2.5),
        hovertemplate="<b>%{x}</b><br>Actual: $%{y:,.0f}<extra></extra>",
    ))
    # Forecast (connect from last actual)
    fig_fc.add_trace(go.Scatter(
        x=[connector_label] + forecast_months_90,
        y=[connector_val] + list(forecast_vals),
        name="Forecast", line=dict(color=GREEN, width=2.2, dash="dash"),
        hovertemplate="<b>%{x}</b><br>Forecast: $%{y:,.0f}<extra></extra>",
    ))
    fig_fc.update_yaxes(tickprefix="$", tickformat=",.0f")
    base_layout(fig_fc, height=320, title="90-Day Seasonal Revenue Forecast")
    st.plotly_chart(fig_fc, use_container_width=True, config=CHART_CFG)

    section_divider()
    st.markdown('<div class="chart-title" style="color:#C9D1D9;font-size:13px;font-weight:600;margin-bottom:8px">Sales Rep Leaderboard — Q1 2026</div>', unsafe_allow_html=True)

    # Mock rep data (consistent seed)
    np.random.seed(99)
    rep_names    = ["Jordan Mills", "Taylor Chen", "Sam Rivera", "Alex Park", "Casey Brooks", "Morgan Lee"]
    seg_focus    = ["Chip/Semi", "Education", "Office", "Restaurant", "Education", "Chip/Semi"]
    rep_quotas   = [900_000] * 6                            # Q1 quota per rep ($3.6M/4)
    rep_revenues = np.random.uniform(0.55, 1.30, 6) * 900_000
    rep_deals    = np.random.randint(4, 18, 6)
    rep_attain   = rep_revenues / np.array(rep_quotas) * 100

    # Sort by attainment desc
    order = np.argsort(rep_attain)[::-1]

    def attain_color(pct):
        return GREEN if pct >= 90 else (ORANGE if pct >= 70 else RED)

    # Trend sparkline (6 months of mock data per rep)
    rep_trends = [np.random.uniform(0.7, 1.3, 6) * rep_revenues[i] / 6 for i in range(6)]

    rows = []
    for rank, i in enumerate(order):
        trophy = "🏆 " if rank == 0 else f"{rank+1}. "
        rows.append({
            "Rep":          trophy + rep_names[i],
            "Segment":      seg_focus[i],
            "Deals":        int(rep_deals[i]),
            "Revenue":      f"${rep_revenues[i]:,.0f}",
            "Quota":        f"${rep_quotas[i]:,.0f}",
            "Attainment":   f"{rep_attain[i]:.0f}%",
        })

    lb_df = pd.DataFrame(rows)
    st.dataframe(lb_df, use_container_width=True, hide_index=True,
                 column_config={
                     "Rep":       st.column_config.TextColumn("Rep",       width="medium"),
                     "Segment":   st.column_config.TextColumn("Segment",   width="small"),
                     "Deals":     st.column_config.NumberColumn("Deals",   width="small"),
                     "Revenue":   st.column_config.TextColumn("Revenue",   width="medium"),
                     "Quota":     st.column_config.TextColumn("Quota",     width="medium"),
                     "Attainment":st.column_config.TextColumn("Attainment",width="small"),
                 })

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # Bar chart: revenue by rep with quota line
    sorted_names = [("🏆 " if r == 0 else f"{r+1}. ") + rep_names[order[r]] for r in range(6)]
    bar_colors   = [attain_color(rep_attain[i]) for i in order]
    fig_lb = go.Figure()
    fig_lb.add_trace(go.Bar(
        x=sorted_names, y=rep_revenues[order],
        marker_color=bar_colors, marker_opacity=0.85, name="Revenue",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    ))
    fig_lb.add_hline(y=520_000, line_dash="dash", line_color="#8B949E", line_width=1.5,
                     annotation_text="Quota $900K", annotation_position="top right",
                     annotation_font=dict(color="#8B949E", size=10))
    fig_lb.update_yaxes(tickprefix="$", tickformat=",.0f")
    base_layout(fig_lb, height=300, legend=False, title="Revenue by Rep vs Quota")
    st.plotly_chart(fig_lb, use_container_width=True, config=CHART_CFG)


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

    section_divider()
    with st.expander("⚖️ Break-Even Calculator", expanded=False):
        be1, be2, be3 = st.columns(3)
        with be1:
            fixed_costs = st.number_input("Monthly Fixed Costs ($)", min_value=0, value=85_000, step=1_000)
        with be2:
            avg_job_rev = st.number_input("Avg Job Revenue ($)", min_value=1, value=12_500, step=500)
        with be3:
            avg_job_var = st.number_input("Avg Variable Cost / Job ($)", min_value=0, value=7_500, step=250)

        contrib_margin = avg_job_rev - avg_job_var
        if contrib_margin > 0:
            be_jobs   = fixed_costs / contrib_margin
            be_rev    = be_jobs * avg_job_rev
            # Current monthly jobs (from fdeal approximation)
            curr_mo_jobs = max(1, len(fdeal) / max(1, (end_date - start_date).days / 30))
            curr_mo_rev  = fdeal["Value"].sum() / max(1, (end_date - start_date).days / 30)
            margin_safety = (curr_mo_rev - be_rev) / curr_mo_rev * 100 if curr_mo_rev > 0 else 0
        else:
            be_jobs = be_rev = curr_mo_rev = margin_safety = 0

        bc1, bc2, bc3 = st.columns(3)
        ms_color = GREEN if margin_safety > 20 else (ORANGE if margin_safety > 0 else RED)
        for col, lbl, val, acc in [
            (bc1, "Break-Even Jobs/Mo",    f"{be_jobs:.1f}", BLUE),
            (bc2, "Break-Even Revenue",    fmt_usd(be_rev), TEAL),
            (bc3, "Margin of Safety",      f"{margin_safety:.1f}%", ms_color),
        ]:
            with col:
                st.markdown(kpi_card(lbl, val, accent=acc), unsafe_allow_html=True)

        st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

        # Gauge chart
        gauge_val = min(200, (curr_mo_rev / be_rev * 100) if be_rev > 0 else 0)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=gauge_val,
            delta={"reference": 100, "valueformat": ".0f"},
            number={"suffix": "%", "valueformat": ".0f"},
            title={"text": "Current Revenue vs Break-Even", "font": {"color": "#C9D1D9", "size": 13}},
            gauge={
                "axis": {"range": [0, 200], "tickcolor": "#8B949E"},
                "bar":  {"color": GREEN if gauge_val >= 120 else (ORANGE if gauge_val >= 100 else RED)},
                "bgcolor": CHART_BG,
                "bordercolor": "#30363D",
                "steps": [
                    {"range": [0,   100], "color": "rgba(239,83,80,0.15)"},
                    {"range": [100, 130], "color": "rgba(255,152,0,0.15)"},
                    {"range": [130, 200], "color": "rgba(76,175,80,0.15)"},
                ],
                "threshold": {"line": {"color": "#E6EDF3", "width": 2}, "value": 100},
            },
        ))
        fig_gauge.update_layout(
            height=260, paper_bgcolor=PAPER_BG, font=dict(color="#C9D1D9"),
            margin=dict(l=20, r=20, t=40, b=0),
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config=CHART_CFG)

        # What-if slider
        st.markdown('<div style="color:#8B949E;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.7px;margin:12px 0 6px">What-If: Additional Fixed Costs</div>', unsafe_allow_html=True)
        extra_fixed = st.slider("Additional monthly fixed costs", 0, 50_000, 0, 1_000, format="$%d")
        new_be_jobs = (fixed_costs + extra_fixed) / contrib_margin if contrib_margin > 0 else 0
        new_be_rev  = new_be_jobs * avg_job_rev
        delta_jobs  = new_be_jobs - be_jobs
        st.markdown(
            f'<div style="background:rgba(255,152,0,0.08);border:1px solid rgba(255,152,0,0.3);'
            f'border-radius:8px;padding:12px 16px;color:#C9D1D9;font-size:13px">'
            f'Adding <strong style="color:{ORANGE}">{fmt_usd(extra_fixed)}/mo</strong> in fixed costs '
            f'raises break-even to <strong style="color:{ORANGE}">{new_be_jobs:.1f} jobs</strong> '
            f'({fmt_usd(new_be_rev)}/mo) — <strong>+{delta_jobs:.1f} more jobs</strong> required.</div>',
            unsafe_allow_html=True,
        )


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

    section_divider()
    with st.expander("🧮 Job Costing Calculator", expanded=False):
        jc1, jc2, jc3, jc4, jc5 = st.columns(5)
        with jc1: labor_hours   = st.number_input("Labor Hours",     min_value=0.0, value=40.0,    step=1.0)
        with jc2: hourly_rate   = st.number_input("Hourly Rate ($)", min_value=0.0, value=85.0,    step=5.0)
        with jc3: materials     = st.number_input("Materials ($)",   min_value=0.0, value=3_500.0, step=100.0)
        with jc4: overhead_pct  = st.number_input("Overhead %",      min_value=0.0, value=15.0,    step=1.0, max_value=100.0)
        with jc5: markup_pct    = st.number_input("Markup %",        min_value=0.0, value=35.0,    step=1.0)

        labor_cost    = labor_hours * hourly_rate
        direct_cost   = labor_cost + materials
        overhead_cost = direct_cost * (overhead_pct / 100)
        total_cost    = direct_cost + overhead_cost
        sale_price    = total_cost * (1 + markup_pct / 100)
        gm_dollars    = sale_price - total_cost
        gm_pct        = gm_dollars / sale_price * 100 if sale_price else 0
        margin_color  = GREEN if gm_pct >= 40 else (ORANGE if gm_pct >= 25 else RED)

        st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
        oc1, oc2, oc3, oc4 = st.columns(4)
        for col, lbl, val, acc in [
            (oc1, "Total Cost",    fmt_usd(total_cost),  BLUE),
            (oc2, "Sale Price",    fmt_usd(sale_price),  TEAL),
            (oc3, "Gross Margin $", fmt_usd(gm_dollars), margin_color),
            (oc4, "Gross Margin %", f"{gm_pct:.1f}%",    margin_color),
        ]:
            with col:
                st.markdown(kpi_card(lbl, val, accent=acc), unsafe_allow_html=True)

        st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
        cust_name_input = st.text_input("Customer / Job Name (optional)", placeholder="e.g. Pico Semiconductor — Chiller Install")
        if st.button("💾 Save Estimate", use_container_width=False):
            st.session_state.estimates.append({
                "Job":         cust_name_input or f"Estimate #{len(st.session_state.estimates)+1}",
                "Labor":       fmt_usd(labor_cost),
                "Materials":   fmt_usd(materials),
                "Total Cost":  fmt_usd(total_cost),
                "Sale Price":  fmt_usd(sale_price),
                "GM $":        fmt_usd(gm_dollars),
                "GM %":        f"{gm_pct:.1f}%",
            })
            st.success("Estimate saved!")

        if st.session_state.estimates:
            st.markdown("<div style='margin-top:12px;color:#8B949E;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.7px'>Saved Estimates</div>", unsafe_allow_html=True)
            est_df = pd.DataFrame(st.session_state.estimates)
            st.dataframe(est_df, use_container_width=True, hide_index=True)


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


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PIPELINE TRACKER
# ══════════════════════════════════════════════════════════════════════════════
elif "Pipeline" in page:
    page_header("Proposal Pipeline Tracker")

    # Mock pipeline deals with stages
    np.random.seed(77)
    random.seed(77)
    pipe_customers = [
        ("Lakeside Unified School", "Education"), ("TechCore Offices", "Office"),
        ("NanoFab Systems", "Chip/Semiconductor"), ("Harbor Bistro Group", "Restaurant"),
        ("Valley College", "Education"), ("Summit Business Park", "Office"),
        ("FusionChip Labs", "Chip/Semiconductor"), ("Metro Eats", "Restaurant"),
        ("Coastal High School", "Education"), ("Pinnacle Tower", "Office"),
        ("QuantumWafer Inc", "Chip/Semiconductor"), ("Sunrise Diner Chain", "Restaurant"),
        ("Ridgeline Corp Center", "Office"), ("Pacific Semiconductor", "Chip/Semiconductor"),
        ("Eastside School Dist.", "Education"), ("The Noodle House", "Restaurant"),
        ("Skyline Office Park", "Office"), ("BlueChip Fab", "Chip/Semiconductor"),
        ("North County Schools", "Education"), ("Bayside Grill", "Restaurant"),
        ("Harborview Suites", "Office"), ("Apex Circuit Co.", "Chip/Semiconductor"),
        ("Greenfield Academy", "Education"), ("Fusion Kitchen", "Restaurant"),
        ("Corporate Commons", "Office"), ("Wafer Tech Corp", "Chip/Semiconductor"),
        ("Sunrise Elem District", "Education"), ("Seaside Cafe Group", "Restaurant"),
        ("Innovation Plaza", "Office"), ("SilicaCore Mfg", "Chip/Semiconductor"),
    ]
    stages      = ["Prospect", "Proposal Sent", "Follow Up", "Closed Won", "Closed Lost"]
    stage_pool  = ["Prospect"]*8 + ["Proposal Sent"]*9 + ["Follow Up"]*7 + ["Closed Won"]*4 + ["Closed Lost"]*2
    val_range   = {"Chip/Semiconductor":(180_000,950_000),"Education":(45_000,285_000),
                   "Office":(32_000,220_000),"Restaurant":(8_000,72_000)}

    pipe_deals_all = []
    for i, (cust, seg) in enumerate(pipe_customers):
        lo, hi = val_range[seg]
        stage = stage_pool[i % len(stage_pool)]
        days_in = random.randint(1, 45)
        pipe_deals_all.append({
            "Customer": cust, "Segment": seg,
            "Value": random.randint(lo, hi),
            "Stage": stage,
            "Days in Stage": days_in,
        })
    pipe_df = pd.DataFrame(pipe_deals_all)

    # KPI cards
    total_pipe_val   = pipe_df[pipe_df["Stage"].isin(["Prospect","Proposal Sent","Follow Up"])]["Value"].sum()
    avg_days_close   = 38  # mock
    conv_rate        = len(pipe_df[pipe_df["Stage"]=="Closed Won"]) / len(pipe_df) * 100
    prop_this_month  = len(pipe_df[pipe_df["Stage"]=="Proposal Sent"])

    pk1, pk2, pk3, pk4 = st.columns(4)
    for col, lbl, val, delta, pos, acc in [
        (pk1, "Total Pipeline Value",   fmt_usd(total_pipe_val), f"{len(pipe_df)} deals",         True, BLUE),
        (pk2, "Avg Days to Close",      f"{avg_days_close}d",    "−3d vs last quarter",           True, TEAL),
        (pk3, "Conversion Rate",        f"{conv_rate:.0f}%",     "vs 55% target",   conv_rate>=55, GREEN if conv_rate>=55 else ORANGE),
        (pk4, "Proposals This Month",   str(prop_this_month),    "active proposals",              True, ORANGE),
    ]:
        with col:
            st.markdown(kpi_card(lbl, val, delta, pos, acc), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # Funnel chart
    kf1, kf2 = st.columns([1, 1])
    with kf1:
        stage_counts = pipe_df["Stage"].value_counts()
        funnel_stages = ["Prospect", "Proposal Sent", "Follow Up", "Closed Won"]
        funnel_vals   = [stage_counts.get(s, 0) for s in funnel_stages]
        funnel_vals_usd = [pipe_df[pipe_df["Stage"]==s]["Value"].sum() for s in funnel_stages]
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_stages, x=funnel_vals,
            textinfo="value+percent initial",
            marker=dict(color=[BLUE, TEAL, ORANGE, GREEN]),
            textfont=dict(color="#E6EDF3"),
            connector=dict(line=dict(color="#30363D", width=1)),
        ))
        base_layout(fig_funnel, height=320, legend=False, title="Pipeline Funnel — Deal Count")
        st.plotly_chart(fig_funnel, use_container_width=True, config=CHART_CFG)

    with kf2:
        fig_funnel2 = go.Figure(go.Funnel(
            y=funnel_stages, x=[v/1e6 for v in funnel_vals_usd],
            textinfo="value+percent initial",
            texttemplate="%{value:.1f}M (%{percentInitial})",
            marker=dict(color=[BLUE, TEAL, ORANGE, GREEN]),
            textfont=dict(color="#E6EDF3"),
            connector=dict(line=dict(color="#30363D", width=1)),
        ))
        base_layout(fig_funnel2, height=320, legend=False, title="Pipeline Funnel — $ Value ($M)")
        st.plotly_chart(fig_funnel2, use_container_width=True, config=CHART_CFG)

    section_divider()

    # Kanban board
    st.markdown('<div style="color:#C9D1D9;font-size:13px;font-weight:600;margin-bottom:12px">Pipeline Board</div>', unsafe_allow_html=True)
    kanban_stages = ["Prospect", "Proposal Sent", "Follow Up", "Closed Won"]
    kcols = st.columns(4)

    for col_idx, stage in enumerate(kanban_stages):
        stage_deals = pipe_df[pipe_df["Stage"] == stage].head(6)
        with kcols[col_idx]:
            stage_total = stage_deals["Value"].sum()
            st.markdown(
                f'<div style="background:#161B22;border:1px solid #30363D;border-radius:8px;'
                f'padding:10px 12px;margin-bottom:8px">'
                f'<div style="color:#8B949E;font-size:10px;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:.8px">{stage}</div>'
                f'<div style="color:#E6EDF3;font-size:14px;font-weight:700;margin-top:2px">'
                f'{fmt_usd(stage_total)}</div></div>',
                unsafe_allow_html=True,
            )
            for _, deal in stage_deals.iterrows():
                seg_c = SEG_COLOR.get(deal["Segment"], BLUE)
                r_hex, g_hex, b_hex = int(seg_c[1:3],16), int(seg_c[3:5],16), int(seg_c[5:7],16)
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#161B22,#1C2333);'
                    f'border:1px solid #30363D;border-left:3px solid {seg_c};'
                    f'border-radius:8px;padding:10px 12px;margin-bottom:6px">'
                    f'<div style="color:#E6EDF3;font-size:12px;font-weight:600;'
                    f'margin-bottom:4px">{deal["Customer"]}</div>'
                    f'<div style="color:{seg_c};font-size:10px;font-weight:600;'
                    f'margin-bottom:6px">{deal["Segment"]}</div>'
                    f'<div style="display:flex;justify-content:space-between">'
                    f'<span style="color:#E6EDF3;font-size:13px;font-weight:700">'
                    f'${deal["Value"]:,.0f}</span>'
                    f'<span style="color:#8B949E;font-size:10px">'
                    f'{deal["Days in Stage"]}d</span></div></div>',
                    unsafe_allow_html=True,
                )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TERRITORY MAP
# ══════════════════════════════════════════════════════════════════════════════
elif "Territory" in page:
    page_header("Service Territory Map")

    # Mock job locations across Upstate NY — Buffalo, Rochester, Syracuse
    np.random.seed(55)
    random.seed(55)

    territory_customers = [
        # Buffalo area (42.88, -78.88)
        ("Praxair Buffalo Facility",        "Chip/Semiconductor", 42.9150, -78.8420),
        ("Moog Inc - East Aurora",          "Chip/Semiconductor", 42.7670, -78.6130),
        ("Buffalo State College",           "Education",          42.9346, -78.8750),
        ("Canisius University",             "Education",          42.9280, -78.8540),
        ("Seneca Street Office Complex",    "Office",             42.8750, -78.8620),
        ("Larkinville Business Center",     "Office",             42.8780, -78.8730),
        ("Anchor Bar & Grill",              "Restaurant",         42.8990, -78.8640),
        ("Lloyd Taco Factory",              "Restaurant",         42.9220, -78.8760),
        ("Elmwood Village Dining",          "Restaurant",         42.9210, -78.8840),
        ("NFTA Transit Center",             "Office",             42.8857, -78.8784),
        # Rochester area (43.16, -77.61)
        ("Paychex HQ",                      "Office",             43.1360, -77.5540),
        ("Wegmans Corporate",               "Office",             43.1150, -77.6710),
        ("University of Rochester",         "Education",          43.1283, -77.6275),
        ("Monroe Community College",        "Education",          43.0840, -77.5660),
        ("Rochester Institute of Tech",     "Education",          43.0848, -77.6741),
        ("Finger Lakes Semiconductor",      "Chip/Semiconductor", 43.1720, -77.5880),
        ("Photon Dynamics Rochester",       "Chip/Semiconductor", 43.1550, -77.6200),
        ("Nick Tahou Hots",                 "Restaurant",         43.1570, -77.6330),
        ("Edwards Restaurant Group",        "Restaurant",         43.1490, -77.5990),
        ("Midtown Tower Office",            "Office",             43.1566, -77.6105),
        # Syracuse area (43.05, -76.15)
        ("Lockheed Martin - Syracuse",      "Chip/Semiconductor", 43.1050, -76.2100),
        ("Welch Allyn / Hillrom",           "Chip/Semiconductor", 43.0600, -76.0320),
        ("Syracuse University",             "Education",          43.0370, -76.1357),
        ("Onondaga Community College",      "Education",          43.0210, -76.2100),
        ("Le Moyne College",                "Education",          43.0688, -76.0808),
        ("Armory Square Office Suites",     "Office",             43.0490, -76.1540),
        ("Clinton Square Corporate Ctr",    "Office",             43.0520, -76.1520),
        ("Dinosaur Bar-B-Que",              "Restaurant",         43.0618, -76.1616),
        ("Pastabilities Restaurant",        "Restaurant",         43.0500, -76.1480),
        ("Empire State Office Park",        "Office",             43.0800, -76.1750),
    ]

    map_records = []
    val_range_t = {"Chip/Semiconductor":(180_000,950_000),"Education":(45_000,285_000),
                   "Office":(32_000,220_000),"Restaurant":(8_000,72_000)}
    for cust, seg, lat, lon in territory_customers:
        lo, hi = val_range_t[seg]
        val = random.randint(lo, hi)
        map_records.append({"Customer": cust, "Segment": seg,
                             "lat": lat + np.random.uniform(-0.008, 0.008),
                             "lon": lon + np.random.uniform(-0.008, 0.008),
                             "Value": val})
    map_df = pd.DataFrame(map_records)

    # Filter by active_segs
    map_df_f = map_df[map_df["Segment"].isin(active_segs)]

    # KPI cards
    jobs_by_seg = map_df_f.groupby("Segment")["Value"].count()
    mk1, mk2, mk3, mk4 = st.columns(4)
    for col, lbl, val, delta, pos, acc in [
        (mk1, "Total Job Sites",     str(len(map_df_f)),          "in territory",               True, BLUE),
        (mk2, "Territory Revenue",   fmt_usd(map_df_f["Value"].sum()), "+11% vs prior year",    True, GREEN),
        (mk3, "Avg Travel Time",     "28 min",                    "mock estimate",               True, TEAL),
        (mk4, "Revenue Density",     fmt_usd(map_df_f["Value"].sum() / max(1, len(map_df_f))), "per site", True, ORANGE),
    ]:
        with col:
            st.markdown(kpi_card(lbl, val, delta, pos, acc), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # Map
    map_df_f = map_df_f.copy()
    map_df_f["Value_K"] = map_df_f["Value"] / 1000
    map_df_f["Label"]   = map_df_f["Customer"] + "<br>$" + map_df_f["Value"].map(lambda v: f"{v:,.0f}")
    color_map = {"Education": BLUE, "Office": TEAL, "Restaurant": GREEN, "Chip/Semiconductor": ORANGE}

    fig_map = px.scatter_mapbox(
        map_df_f, lat="lat", lon="lon",
        color="Segment",
        color_discrete_map=color_map,
        size="Value_K",
        size_max=22,
        hover_name="Customer",
        hover_data={"lat": False, "lon": False, "Value_K": False,
                    "Value": ":$,.0f", "Segment": True},
        zoom=7,
        center={"lat": 43.05, "lon": -77.20},
        mapbox_style="open-street-map",
        height=480,
    )
    fig_map.update_layout(
        paper_bgcolor=PAPER_BG,
        font=dict(color="#C9D1D9"),
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(bgcolor="rgba(13,17,23,0.85)", bordercolor="#30363D",
                    borderwidth=1, font=dict(color="#C9D1D9")),
    )
    st.plotly_chart(fig_map, use_container_width=True, config=CHART_CFG)

    section_divider()

    # Revenue by segment breakdown
    st.markdown('<div style="color:#C9D1D9;font-size:13px;font-weight:600;margin-bottom:8px">Revenue by Site</div>', unsafe_allow_html=True)
    map_disp = map_df_f.copy()
    map_disp["Value"] = map_disp["Value"].map(lambda v: f"${v:,.0f}")
    map_disp = map_disp.drop(columns=["lat","lon","Value_K","Label"])
    st.dataframe(map_disp.sort_values("Value", ascending=False),
                 use_container_width=True, hide_index=True)
