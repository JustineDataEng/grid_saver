import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Grid Saver | Adaptive Grid Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM STYLES
# ============================================================
st.markdown("""
<style>
    .main { background-color: #0D1117; }
    .stApp { background-color: #0D1117; }
    .metric-card {
        background: #161B22;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #30363D;
        text-align: center;
    }
    h1, h2, h3 { color: white !important; }
    .stMarkdown { color: #CCCCCC; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# NOTE: Demand is simulated using carbon intensity as a proxy
# for demonstration purposes.
# Real demand forecasting will be implemented using PJM load datasets.
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv('https://drive.google.com/uc?export=download&id=10NCU3HEZC2KDiqHCii6E1XuRa9G0Y9zg')
    df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
    df = df.sort_values('Datetime (UTC)').reset_index(drop=True)

    carbon_col = 'Carbon intensity gCO\u2082eq/kWh (direct)'
    cfe_col = 'Carbon-free energy percentage (CFE%)'

    df['hour'] = df['Datetime (UTC)'].dt.hour
    df['month'] = df['Datetime (UTC)'].dt.month
    df['date'] = df['Datetime (UTC)'].dt.date
    df['month_name'] = df['Datetime (UTC)'].dt.strftime('%b')

    carbon_max = df[carbon_col].max()
    carbon_min = df[carbon_col].min()
    cfe_max = df[cfe_col].max()

    df['stress_score'] = (
        ((df[carbon_col] - carbon_min) / (carbon_max - carbon_min) * 70) +
        ((1 - df[cfe_col] / cfe_max) * 30)
    ).round(1)

    stress_threshold = df['stress_score'].quantile(0.85)
    df['is_vulnerable'] = df['stress_score'] >= stress_threshold

    def classify_status(score):
        if score < 40:
            return 'STABLE'
        elif score < 70:
            return 'WARNING'
        else:
            return 'CRITICAL'

    df['grid_status'] = df['stress_score'].apply(classify_status)

    df['simulated_demand_mw'] = (
        (df[carbon_col] - carbon_min) /
        (carbon_max - carbon_min) * 20000 + 55000
    )

    df['hvac_load_mw'] = df['simulated_demand_mw'] * 0.13
    return df, stress_threshold, carbon_col, cfe_col

with st.spinner("Loading grid data..."):
    df, stress_threshold, carbon_col, cfe_col = load_data()

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.image("https://img.icons8.com/fluency/96/lightning-bolt.png", width=60)
st.sidebar.title("Grid Saver")
st.sidebar.markdown("**Adaptive Grid Intelligence Platform**")
st.sidebar.markdown("---")

# UPGRADE 1: Live Grid Mode Toggle
live_mode = st.sidebar.toggle("⚡ Live Grid Mode", value=False)
if live_mode:
    st.sidebar.markdown(
        "<p style='color:#2ECC71; font-size:0.8rem;'>Showing last 24 hours</p>",
        unsafe_allow_html=True
    )

st.sidebar.markdown("---")

month_options = ['All Year'] + list(df['month_name'].unique())
selected_month = st.sidebar.selectbox("Select Month", month_options)

reduction_rate_input = st.sidebar.slider(
    "HVAC Reduction Rate (%)",
    min_value=1, max_value=10, value=4, step=1
)

apply_intervention = st.sidebar.toggle("Apply Grid Saver Intervention", value=True)

st.sidebar.markdown("---")

with st.sidebar.expander("Dataset Information"):
    st.write("""
    **Source:** Electricity Maps US-TEX-ERCO 2025
    **Records:** 8,761 hourly observations
    **Region:** Texas ERCOT grid
    **Variables:** Carbon intensity, CFE%, timestamps
    **Academic access:** Cite Electricity Maps in publications
    **Note:** Demand simulated from carbon intensity.
    Real forecasting will be added via PJM datasets.
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("**Stack**")
st.sidebar.markdown("Colab + GitHub + Streamlit")
st.sidebar.markdown("---")
st.sidebar.markdown("*Justine Adzormado*")
st.sidebar.markdown("*Red Bull Basement 2026*")

# ============================================================
# FILTER DATA
# ============================================================
if live_mode:
    df_view = df.tail(24).copy()
elif selected_month != 'All Year':
    df_view = df[df['month_name'] == selected_month].copy()
else:
    df_view = df.copy()

df_view['grid_saver_reduction_mw'] = np.where(
    df_view['is_vulnerable'],
    df_view['hvac_load_mw'] * (reduction_rate_input / 100),
    0
)
df_view['optimized_demand_mw'] = (
    df_view['simulated_demand_mw'] - df_view['grid_saver_reduction_mw']
)

# ============================================================
# HEADER
# ============================================================
mode_label = "LIVE MODE" if live_mode else "ANALYSIS MODE"
mode_color = "#2ECC71" if live_mode else "#4A9EFF"

st.markdown(f"""
<div style='background: linear-gradient(135deg, #1B4F8C, #0D1117);
     padding: 30px; border-radius: 12px; margin-bottom: 20px;
     border: 1px solid #30363D;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 style='color: white; margin: 0; font-size: 2.2rem;'>⚡ Grid Saver</h1>
            <p style='color: #4A9EFF; margin: 5px 0 0 0; font-size: 1.1rem;'>
                Adaptive Grid Intelligence Platform
            </p>
            <p style='color: #888; margin: 5px 0 0 0; font-size: 0.9rem;'>
                Texas ERCOT 2025 | Sense Layer | Red Bull Basement 2026
            </p>
        </div>
        <div style='background: {mode_color}22; border: 2px solid {mode_color};
             padding: 10px 20px; border-radius: 8px; text-align: center;'>
            <p style='color: {mode_color}; font-weight: bold; margin: 0; font-size: 1rem;'>
                {"🔴 " if live_mode else "📊 "}{mode_label}
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1 - GRID STATUS
# ============================================================
st.markdown("## ⚡ Grid Status")

current_score = df_view['stress_score'].iloc[-1]
current_status = df_view['grid_status'].iloc[-1]
current_carbon = df_view[carbon_col].iloc[-1]
current_cfe = df_view[cfe_col].iloc[-1]
vulnerable_pct = df_view['is_vulnerable'].mean() * 100
vulnerable_hours = int(df_view['is_vulnerable'].sum())

status_color = {'STABLE': '#2ECC71', 'WARNING': '#F39C12', 'CRITICAL': '#E74C3C'}
status_icon = {'STABLE': '🟢', 'WARNING': '🟡', 'CRITICAL': '🔴'}

col1, col2, col3, col4, col5, col6 = st.columns(6)
cards = [
    (col1, status_icon[current_status], current_status, "Grid Status", status_color[current_status]),
    (col2, f"{current_score:.0f}", "/100", "Stress Score", "white"),
    (col3, f"{current_carbon:.0f}", "gCO2eq/kWh", "Carbon Intensity", "#FF6B6B"),
    (col4, f"{current_cfe:.1f}%", "CFE", "Carbon-Free Energy", "#2ECC71"),
    (col5, f"{vulnerable_pct:.1f}%", "of period", "Time at Risk", "#F39C12"),
    (col6, f"{vulnerable_hours}", "hours", "Vulnerability Hours", "#4A9EFF"),
]
for col, val, sub, label, color in cards:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: {color}; font-size: 1.6rem; margin: 0;'>{val}</h2>
            <p style='color: #666; margin: 2px 0; font-size: 0.75rem;'>{sub}</p>
            <p style='color: #888; margin: 0; font-size: 0.75rem;'>{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Pre-calculate action for explain button
current_stress = current_score
if current_stress >= stress_threshold:
    action_color = "#E74C3C"
    action_icon_str = "🔴"
    action_title = "CRITICAL - Immediate Action Required"
    action_text = f"Reduce residential HVAC load by {reduction_rate_input}% across coordination zones"
    expected = f"Expected peak reduction: ~{reduction_rate_input * 0.9:.1f}% | Grid stabilization: HIGH confidence"
elif current_stress >= stress_threshold * 0.7:
    action_color = "#F39C12"
    action_icon_str = "🟡"
    action_title = "WARNING - Prepare for Intervention"
    action_text = f"Pre-stage HVAC coordination. Prepare {reduction_rate_input}% reduction if stress increases"
    expected = f"Monitoring window: Next 2-4 hours | Pre-emptive coordination recommended"
else:
    action_color = "#2ECC71"
    action_icon_str = "🟢"
    action_title = "STABLE - No Action Required"
    action_text = "Grid operating within safe parameters. Continue monitoring."
    expected = f"Next vulnerability check: Hourly | System: Active monitoring"

# ============================================================
# SECTION 2 - DEMAND GRAPH
# ============================================================
st.markdown("## 📈 Grid Demand and Vulnerability Windows")

color_map = {'STABLE': '#2ECC71', 'WARNING': '#F39C12', 'CRITICAL': '#E74C3C'}
fig_demand = go.Figure()

fig_demand.add_trace(go.Scatter(
    x=df_view['Datetime (UTC)'], y=df_view['simulated_demand_mw'],
    mode='lines', line=dict(color='#4A9EFF', width=1, dash='dot'),
    opacity=0.3, showlegend=False,
))

for status in ['STABLE', 'WARNING', 'CRITICAL']:
    mask = df_view['grid_status'] == status
    if mask.any():
        fig_demand.add_trace(go.Scatter(
            x=df_view[mask]['Datetime (UTC)'],
            y=df_view[mask]['simulated_demand_mw'],
            mode='markers+lines',
            name=status,
            marker=dict(color=color_map[status], size=4, opacity=0.8),
            line=dict(color=color_map[status], width=0.5),
            connectgaps=False,
        ))

fig_demand.update_layout(
    paper_bgcolor='#161B22', plot_bgcolor='#161B22',
    font=dict(color='white'),
    title=dict(text='Grid Demand by Stress Status - ERCOT Texas 2025',
               font=dict(color='white', size=14)),
    xaxis=dict(gridcolor='#30363D', color='#888'),
    yaxis=dict(gridcolor='#30363D', color='#888', title='Simulated Demand (MW)'),
    legend=dict(bgcolor='#1A1A2E', bordercolor='#333'),
    height=350, margin=dict(t=50, b=30),
)
st.plotly_chart(fig_demand, use_container_width=True)

# ============================================================
# SECTION 3 - PEAK RISK TIMELINE
# ============================================================
st.markdown("## ⏰ Peak Risk Timeline")
col_left, col_right = st.columns(2)

with col_left:
    hourly_stress = df_view.groupby('hour')['stress_score'].mean().round(1)
    bar_colors = ['#E74C3C' if s >= stress_threshold else
                  '#F39C12' if s >= stress_threshold * 0.7 else
                  '#2ECC71' for s in hourly_stress.values]
    fig_hour = go.Figure(go.Bar(
        x=[f'{h:02d}:00' for h in hourly_stress.index],
        y=hourly_stress.values, marker_color=bar_colors,
    ))
    fig_hour.add_hline(y=stress_threshold, line_dash='dash', line_color='#FF4444',
                       annotation_text=f'Threshold ({stress_threshold:.0f})',
                       annotation_font_color='#FF4444')
    fig_hour.update_layout(
        paper_bgcolor='#161B22', plot_bgcolor='#161B22', font=dict(color='white'),
        title=dict(text='Avg Stress by Hour of Day', font=dict(color='white', size=13)),
        xaxis=dict(gridcolor='#30363D', color='#888', title='Hour (UTC)'),
        yaxis=dict(gridcolor='#30363D', color='#888', title='Stress Score'),
        height=300, margin=dict(t=50, b=30),
    )
    st.plotly_chart(fig_hour, use_container_width=True)

with col_right:
    monthly_stress = df_view.groupby('month_name')['stress_score'].mean().round(1)
    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthly_stress = monthly_stress.reindex([m for m in month_order if m in monthly_stress.index])
    bar_colors_m = ['#E74C3C' if s >= stress_threshold else
                    '#F39C12' if s >= stress_threshold * 0.7 else
                    '#2ECC71' for s in monthly_stress.values]
    fig_month = go.Figure(go.Bar(
        x=monthly_stress.index, y=monthly_stress.values, marker_color=bar_colors_m,
    ))
    fig_month.update_layout(
        paper_bgcolor='#161B22', plot_bgcolor='#161B22', font=dict(color='white'),
        title=dict(text='Avg Stress by Month', font=dict(color='white', size=13)),
        xaxis=dict(gridcolor='#30363D', color='#888', title='Month'),
        yaxis=dict(gridcolor='#30363D', color='#888', title='Stress Score'),
        height=300, margin=dict(t=50, b=30),
    )
    st.plotly_chart(fig_month, use_container_width=True)

# ============================================================
# SECTION 4 - SIMULATION
# ============================================================
st.markdown("## 🎯 Grid Saver Load Reduction Simulation")

daily_max = df_view.groupby('date')['stress_score'].max()
worst_day = daily_max.idxmax()
day_data = df_view[df_view['date'] == worst_day].copy()

peak_original = day_data['simulated_demand_mw'].max()
peak_optimized = day_data['optimized_demand_mw'].max()
pct_reduction = ((peak_original - peak_optimized) / peak_original * 100)
mw_saved = peak_original - peak_optimized

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
sim_cards = [
    (col_m1, f"{peak_original:,.0f} MW", "Original Peak", "#E74C3C"),
    (col_m2, f"{peak_optimized:,.0f} MW", "After Grid Saver", "#2ECC71"),
    (col_m3, f"{pct_reduction:.1f}%", "Peak Reduction", "#4A9EFF"),
    (col_m4, f"{mw_saved:,.0f} MW", "MW Removed", "#F39C12"),
]
for col, val, label, color in sim_cards:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: {color}; font-size: 1.6rem; margin: 0;'>{val}</h2>
            <p style='color: #888; margin: 5px 0 0 0; font-size: 0.8rem;'>{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if not apply_intervention:
    st.info("Grid Saver intervention is OFF. Toggle it on in the sidebar to see the impact.")

fig_sim = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Before vs After Grid Saver Intervention',
                    'HVAC Load Reduction Applied'),
    vertical_spacing=0.12
)
fig_sim.add_trace(go.Scatter(
    x=day_data['Datetime (UTC)'], y=day_data['simulated_demand_mw'],
    name='Original Demand', line=dict(color='#E74C3C', width=2.5),
    fill='tozeroy', fillcolor='rgba(231,76,60,0.1)'
), row=1, col=1)

if apply_intervention:
    fig_sim.add_trace(go.Scatter(
        x=day_data['Datetime (UTC)'], y=day_data['optimized_demand_mw'],
        name='Grid Saver Optimized', line=dict(color='#2ECC71', width=2.5, dash='dash'),
        fill='tozeroy', fillcolor='rgba(46,204,113,0.1)'
    ), row=1, col=1)
    fig_sim.add_hline(y=peak_optimized, line_dash='dot', line_color='#2ECC71',
                      annotation_text=f'Optimized: {peak_optimized:,.0f} MW',
                      annotation_font_color='#2ECC71', row=1, col=1)

fig_sim.add_hline(y=peak_original, line_dash='dot', line_color='#E74C3C',
                  annotation_text=f'Original Peak: {peak_original:,.0f} MW',
                  annotation_font_color='#E74C3C', row=1, col=1)

fig_sim.add_trace(go.Bar(
    x=day_data['Datetime (UTC)'],
    y=day_data['grid_saver_reduction_mw'] if apply_intervention else [0]*len(day_data),
    name='Reduction (MW)', marker_color='#3498DB', opacity=0.7
), row=2, col=1)

fig_sim.update_layout(
    paper_bgcolor='#161B22', plot_bgcolor='#161B22',
    font=dict(color='white'), height=550,
    legend=dict(bgcolor='#1A1A2E', bordercolor='#333'),
    margin=dict(t=60, b=30),
)
fig_sim.update_xaxes(gridcolor='#30363D', color='#888')
fig_sim.update_yaxes(gridcolor='#30363D', color='#888')
st.plotly_chart(fig_sim, use_container_width=True)

# ============================================================
# UPGRADE 2: IMPACT AT SCALE
# ============================================================
st.markdown("## 🌍 Impact at Scale")
st.markdown("*Drag the slider to see how Grid Saver scales from neighbourhood to city to national grid.*")

homes = st.slider("Number of Homes Coordinated", 1000, 1000000, 100000, step=1000)
scaled_reduction = homes * 0.2 * (reduction_rate_input / 100)

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
grid_impact = "City-scale" if homes < 100000 else "Regional-scale" if homes < 500000 else "National-scale"
impact_color = "#F39C12" if homes < 100000 else "#4A9EFF" if homes < 500000 else "#2ECC71"
reserve_note = "Exceeds reserve margin" if scaled_reduction > 200 else "Building toward reserve margin"
rm_color = "#2ECC71" if scaled_reduction > 200 else "#F39C12"

scale_cards = [
    (col_s1, f"{homes:,}", "Homes", "Homes Coordinated", "#4A9EFF"),
    (col_s2, f"{scaled_reduction:,.1f} kW", "total", "Grid Reduction", "#2ECC71"),
    (col_s3, grid_impact, "", "Impact Level", impact_color),
    (col_s4, reserve_note, "", "Reserve Margin", rm_color),
]
for col, val, sub, label, color in scale_cards:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: {color}; font-size: 1.3rem; margin: 0;'>{val}</h2>
            <p style='color: #666; margin: 2px 0; font-size: 0.75rem;'>{sub}</p>
            <p style='color: #888; margin: 0; font-size: 0.75rem;'>{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SECTION 5 - RECOMMENDED ACTION + EXPLAIN BUTTON
# ============================================================
st.markdown("## 🤖 Recommended Grid Action")

st.markdown(f"""
<div style='background: #161B22; border-left: 5px solid {action_color};
     padding: 20px; border-radius: 8px; margin: 10px 0;'>
    <h3 style='color: {action_color}; margin: 0;'>{action_icon_str} {action_title}</h3>
    <p style='color: white; margin: 10px 0 5px 0; font-size: 1rem;'>
        <strong>Recommended Action:</strong> {action_text}
    </p>
    <p style='color: #888; margin: 0; font-size: 0.9rem;'>{expected}</p>
</div>
""", unsafe_allow_html=True)

# UPGRADE 3: Explain My Decision Button
if st.button("🧠 Explain Grid Decision"):
    stress_level = 'HIGH' if current_stress >= stress_threshold else 'MODERATE' if current_stress >= stress_threshold * 0.7 else 'LOW'
    st.markdown(f"""
    <div style='background: #161B22; border: 1px solid #1B4F8C;
         padding: 25px; border-radius: 10px; margin-top: 15px;'>
        <h3 style='color: #4A9EFF; margin: 0 0 15px 0;'>AI Decision Explanation</h3>
        <p style='color: #CCC; margin: 5px 0;'>
            Grid Saver classified the system as
            <strong style='color: {action_color};'>{current_status}</strong>
            based on:
        </p>
        <ul style='color: #CCC; margin: 10px 0;'>
            <li>Stress Score: <strong style='color: white;'>{current_score:.1f} / 100</strong>
                (threshold: {stress_threshold:.0f})</li>
            <li>Carbon Intensity: <strong style='color: #FF6B6B;'>{current_carbon:.0f} gCO2eq/kWh</strong></li>
            <li>Carbon-Free Energy: <strong style='color: #2ECC71;'>{current_cfe:.1f}%</strong></li>
            <li>Grid Stress Level: <strong style='color: {action_color};'>{stress_level}</strong></li>
        </ul>
        <p style='color: #CCC; margin: 10px 0 5px 0;'>
            <strong>Recommended Action:</strong>
            <span style='color: white;'>{action_text}</span>
        </p>
        <p style='color: #888; margin: 0; font-size: 0.9rem;'>{expected}</p>
        <p style='color: #555; margin: 15px 0 0 0; font-size: 0.8rem;'>
            Reserve Margin: A {reduction_rate_input}% HVAC reduction across {homes:,} homes
            removes approximately {scaled_reduction:,.1f} kW from peak demand,
            bringing the grid back within safe operating bounds.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SECTION 6 - SYSTEM ARCHITECTURE
# ============================================================
st.markdown("## 🏗️ System Architecture")
col_a, col_b, col_c = st.columns(3)

arch = [
    (col_a, "👁️", "SENSE", "#1B4F8C", "#4A9EFF",
     "Detect grid stress signals", "Carbon intensity monitoring",
     "Electricity Maps US-TEX-ERCO", "8,761 hourly records",
     "✅ ACTIVE", "#2ECC71"),
    (col_b, "🧠", "PREDICT", "#1A6B2E", "#2ECC71",
     "Forecast vulnerability windows", "XGBoost + LSTM models",
     "PJM 145,367 hourly records", "24-hour advance warning",
     "⏳ IN BUILD", "#F39C12"),
    (col_c, "⚡", "ACT", "#7B1A1A", "#E74C3C",
     "Coordinate HVAC load reduction", "3-5% surgical precision",
     "Pecan Street 680K records", "Human-override safety protocol",
     "⏳ UPCOMING", "#F39C12"),
]

for col, icon, title, bg, color, l1, l2, l3, l4, status, sc in arch:
    with col:
        st.markdown(f"""
        <div style='background: {bg}22; border: 1px solid {color};
             padding: 20px; border-radius: 10px; text-align: center;
             border-top: 4px solid {color};'>
            <h2 style='color: {color}; font-size: 2rem; margin: 0;'>{icon}</h2>
            <h3 style='color: {color}; margin: 10px 0 5px 0;'>{title}</h3>
            <p style='color: #888; font-size: 0.85rem; margin: 0;'>
                {l1}<br>{l2}<br>{l3}<br>{l4}
            </p>
            <p style='color: {sc}; font-size: 0.8rem; margin: 10px 0 0 0;'>{status}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='background: #161B22; padding: 15px; border-radius: 8px;
     border: 1px solid #30363D; text-align: center; margin-top: 20px;'>
    <p style='color: #888; margin: 0; font-size: 0.85rem;'>
        Grid Saver | Adaptive Grid Intelligence Platform |
        Justine Adzormado | Red Bull Basement 2026 |
        Built with Colab + GitHub + Streamlit
    </p>
    <p style='color: #555; margin: 5px 0 0 0; font-size: 0.75rem;'>
        Data: Electricity Maps US-TEX-ERCO 2025 (Academic Access) |
        Demand simulated from carbon intensity for prototype demonstration |
        Real forecasting via PJM datasets
    </p>
</div>
""", unsafe_allow_html=True)
