"""
app.py — Main Streamlit Dashboard Application
World Population by Country (2020) — EDA Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np

from filters import load_data, apply_filters
import charts as ch

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="World Population Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Global */
    html, body, [data-testid="stApp"] { background-color: #F0F4F8; }
    h1 { color: #1A5276; }
    h2, h3 { color: #1F618D; }

    /* KPI Cards */
    .kpi-container { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 8px; }
    .kpi-card {
        background: linear-gradient(135deg, #1A5276 0%, #2E86C1 100%);
        border-radius: 12px;
        padding: 18px 24px;
        flex: 1; min-width: 160px;
        text-align: center; color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .kpi-card .value { font-size: 1.8rem; font-weight: 700; }
    .kpi-card .label { font-size: 0.82rem; opacity: 0.85; margin-top: 4px; }

    /* Chart card */
    .chart-card {
        background: white; border-radius: 12px;
        padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 16px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #1A5276; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stTextInput label { color: white !important; }

    /* Divider */
    hr { border-top: 1px solid #AED6F1; }
</style>
""", unsafe_allow_html=True)


# ─── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data("data/Population_by_country.xlsx")

df_raw = get_data()


# ─── Sidebar Filters ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Dashboard Filters")
    st.markdown("---")

    # 1. Text / Search filter
    search = st.text_input("🔍 Search Country", placeholder="e.g. Pakistan, France…")

    st.markdown("---")

    # 2. Population range slider (numerical range)
    pop_min = int(df_raw["population_2020"].min())
    pop_max = int(df_raw["population_2020"].max())
    pop_range = st.slider(
        "📊 Population Range",
        min_value=pop_min,
        max_value=pop_max,
        value=(pop_min, pop_max),
        format="%d",
    )

    st.markdown("---")

    # 3. Population category (multi-select)
    all_cats = ["<1M", "1M–10M", "10M–50M", "50M–100M", "100M–500M", ">500M"]
    avail_cats = [c for c in all_cats if c in df_raw["pop_category"].values]
    pop_cats = st.multiselect(
        "🗂 Population Categories",
        options=avail_cats,
        default=avail_cats,
    )

    st.markdown("---")

    # 4. Migration direction (multi-select)
    mig_dirs = st.multiselect(
        "✈️ Net Migration Direction",
        options=["Positive", "Negative", "Neutral/Unknown"],
        default=["Positive", "Negative", "Neutral/Unknown"],
    )

    st.markdown("---")

    # 5. Density slider (numerical range)
    den_min = int(df_raw["density_km2"].min())
    den_max = int(df_raw["density_km2"].max())
    density_range = st.slider(
        "🏙 Density Range (P/Km²)",
        min_value=den_min,
        max_value=den_max,
        value=(den_min, den_max),
    )

    st.markdown("---")

    # 6. Reset filters button
    if st.button("🔄 Reset All Filters"):
        st.rerun()


# ─── Apply filters ────────────────────────────────────────────────────────────
df = apply_filters(
    df_raw,
    search_text=search,
    pop_range=pop_range,
    pop_categories=pop_cats if len(pop_cats) < len(avail_cats) else None,
    migration_dirs=mig_dirs if len(mig_dirs) < 3 else None,
    density_range=density_range if density_range != (den_min, den_max) else None,
)


# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("# 🌍 World Population Dashboard (2020)")
st.markdown(
    "Interactive exploration of demographic indicators across **235 countries and territories**. "
    "Use the sidebar filters to slice the data — all charts update simultaneously."
)
st.markdown("---")


# ─── KPI Cards ───────────────────────────────────────────────────────────────
total_pop     = df["population_2020"].sum()
avg_fertility = df["fertility_rate"].mean()
avg_age       = df["median_age"].mean()
avg_urban     = df["urban_pop_pct"].mean()
most_pop      = df.loc[df["population_2020"].idxmax(), "country"] if len(df) else "—"
fastest_grow  = df.loc[df["yearly_change"].idxmax(), "country"] if len(df) else "—"

col1, col2, col3, col4, col5, col6 = st.columns(6)

def kpi(col, value, label, icon=""):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="value">{icon} {value}</div>
        <div class="label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

kpi(col1, f"{total_pop/1e9:.2f}B",      "Total Population")
kpi(col2, f"{len(df)}",                  "Countries Shown")
kpi(col3, f"{avg_fertility:.2f}",        "Avg Fertility Rate")
kpi(col4, f"{avg_age:.1f} yrs",          "Avg Median Age")
kpi(col5, f"{avg_urban:.1f}%",           "Avg Urban Pop %")
kpi(col6, most_pop,                      "Most Populous")

st.markdown("<br>", unsafe_allow_html=True)


# ─── Guard: need data ─────────────────────────────────────────────────────────
if len(df) == 0:
    st.warning("⚠️ No countries match the current filters. Please adjust your selections.")
    st.stop()


# ─── Section 1: Overview ─────────────────────────────────────────────────────
st.markdown("## 📊 Population Overview")
col_a, col_b = st.columns(2)

with col_a:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.bar_chart(df))
        st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.pie_chart(df))
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ─── Section 2: Distribution ──────────────────────────────────────────────────
st.markdown("## 📈 Distribution & Frequency")
col_c, col_d = st.columns(2)

with col_c:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.histogram(df))
        st.markdown('</div>', unsafe_allow_html=True)

with col_d:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.count_plot(df))
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ─── Section 3: Trends & Growth ──────────────────────────────────────────────
st.markdown("## 📉 Trends & Cumulative Growth")
col_e, col_f = st.columns(2)

with col_e:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.line_chart(df))
        st.markdown('</div>', unsafe_allow_html=True)

with col_f:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.area_chart(df))
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ─── Section 4: Demographics ──────────────────────────────────────────────────
st.markdown("## 🧬 Demographics & Health Indicators")
col_g, col_h = st.columns(2)

with col_g:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.scatter_plot(df))
        st.markdown('</div>', unsafe_allow_html=True)

with col_h:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.box_plot(df))
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ─── Section 5: Migration & Urbanization ─────────────────────────────────────
st.markdown("## ✈️ Migration & Urbanization")
col_i, col_j = st.columns(2)

with col_i:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.violin_plot(df))
        st.markdown('</div>', unsafe_allow_html=True)

with col_j:
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(ch.heatmap(df))
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ─── Section 6: Data Table ────────────────────────────────────────────────────
st.markdown("## 🗃 Filtered Data Table")
display_cols = {
    "rank": "Rank", "country": "Country",
    "population_2020": "Population (2020)",
    "yearly_change": "Yearly Change (%)",
    "density_km2": "Density (P/Km²)",
    "land_area_km2": "Land Area (Km²)",
    "fertility_rate": "Fertility Rate",
    "median_age": "Median Age",
    "urban_pop_pct": "Urban Pop %",
    "world_share": "World Share (%)",
    "migration_dir": "Migration Direction",
}
st.dataframe(
    df[list(display_cols.keys())].rename(columns=display_cols),
    use_container_width=True,
    height=400,
)

st.markdown(
    f"<p style='color:#666;font-size:0.8rem;'>Showing {len(df)} of {len(df_raw)} countries/territories.</p>",
    unsafe_allow_html=True,
)
