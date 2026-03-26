import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page Config
st.set_page_config(
    page_title="Biscayne Bay Water Quality",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS — Ocean-inspired dark editorial theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&display=swap');
html, body, [data-testid="stAppViewContainer"] { background: #050d18; color: #c8dff0; font-family: 'DM Mono', monospace; }
[data-testid="stSidebar"] { background: #071525; border-right: 1px solid #0e2a45; }
.hero { background: linear-gradient(135deg, #071c35 0%, #0a2d52 50%, #063a6b 100%); border: 1px solid #0e4278; border-radius: 4px; padding: 2.5rem 3rem; margin-bottom: 2rem; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, transparent, transparent 40px, rgba(14,66,120,0.15) 40px, rgba(14,66,120,0.15) 41px); pointer-events: none; }
.hero-title { font-family: 'DM Serif Display', serif; font-size: 3rem; color: #7ecfff; line-height: 1.1; margin: 0 0 0.5rem; letter-spacing: -0.02em; }
.hero-subtitle { font-size: 0.8rem; color: #5a8ab0; letter-spacing: 0.2em; text-transform: uppercase; margin: 0; }
.hero-meta { font-size: 0.75rem; color: #3a6a8f; margin-top: 1rem; letter-spacing: 0.05em; }
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.metric-card { background: #071525; border: 1px solid #0e2a45; border-top: 3px solid; padding: 1.2rem 1.4rem; border-radius: 2px; transition: border-color 0.2s; }
.metric-card:hover { border-color: #7ecfff !important; }
.metric-label { font-size: 0.65rem; color: #3a6a8f; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 0.4rem; }
.metric-value { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: #c8dff0; line-height: 1; }
.metric-unit { font-size: 0.7rem; color: #5a8ab0; margin-top: 0.2rem; }
.section-header { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: #7ecfff; border-bottom: 1px solid #0e2a45; padding-bottom: 0.5rem; margin-bottom: 1rem; letter-spacing: -0.01em; }
.info-box { background: #071e36; border-left: 3px solid #1a7fbf; padding: 0.8rem 1rem; font-size: 0.78rem; color: #7aabcc; border-radius: 0 2px 2px 0; margin-bottom: 1rem; }
.warn-box { background: #1a1206; border-left: 3px solid #c9850a; padding: 0.8rem 1rem; font-size: 0.78rem; color: #c9a45a; border-radius: 0 2px 2px 0; margin-bottom: 1rem; }
[data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stSlider label, [data-testid="stSidebar"] .stMultiSelect label { color: #5a8ab0 !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.15em; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #7ecfff; font-family: 'DM Serif Display', serif; }
[data-testid="stPlotlyChart"] { border: 1px solid #0e2a45; border-radius: 2px; overflow: hidden; }
[data-testid="stDataFrame"] { border: 1px solid #0e2a45; border-radius: 2px; }
[data-testid="stExpander"] { border: 1px solid #0e2a45 !important; border-radius: 2px !important; background: #071525 !important; }
.footer { text-align: center; font-size: 0.68rem; color: #1e4060; padding: 2rem 0 1rem; letter-spacing: 0.1em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

METRICS = {
    'Temp C':        {'label': 'Temperature',       'unit': '°C',       'color': '#ff6b35'},
    'Sal ppt':       {'label': 'Salinity',           'unit': 'ppt',      'color': '#00b4d8'},
    'pH':            {'label': 'pH',                 'unit': 'pH',       'color': '#a8dadc'},
    'Chl ug/L':      {'label': 'Chlorophyll-a',      'unit': 'µg/L',     'color': '#52b788'},
    'ODO mg/L':      {'label': 'Dissolved Oxygen',   'unit': 'mg/L',     'color': '#74c0fc'},
    'Turbid+ NTU':   {'label': 'Turbidity',          'unit': 'NTU',      'color': '#e9c46a'},
    'Depth feet':    {'label': 'Depth',              'unit': 'ft',       'color': '#9b8ee0'},
    'BGA-PC cells/mL': {'label': 'Blue-Green Algae', 'unit': 'cells/mL', 'color': '#2dc653'},
}

PLOTLY_TEMPLATE = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#071525',
    font=dict(color='#7aabcc', family='DM Mono, monospace', size=11),
    xaxis=dict(gridcolor='#0e2a45', linecolor='#0e2a45', zerolinecolor='#0e2a45'),
    yaxis=dict(gridcolor='#0e2a45', linecolor='#0e2a45', zerolinecolor='#0e2a45'),
    coloraxis_colorbar=dict(bgcolor='#071525', tickcolor='#5a8ab0', title_font_color='#5a8ab0'),
)

@st.cache_data
def load_data():
    df = pd.read_csv('biscayneBay_waterquality.csv')
    df.columns = df.columns.str.strip()
    date_col = next((c for c in df.columns if 'Date' in c and 'm/d/y' in c), None)
    time_col = next((c for c in df.columns if 'Time' in c and 'hh:mm:ss' in c), None)
    if date_col and time_col:
        df['Timestamp'] = pd.to_datetime(df[date_col].astype(str) + ' ' + df[time_col].astype(str), errors='coerce')
    else:
        st.error(f"Could not find date/time columns. Available: {list(df.columns)}")
        st.stop()
    df = df.sort_values('Timestamp').reset_index(drop=True)
    df['Elapsed Min'] = (df['Timestamp'] - df['Timestamp'].min()).dt.total_seconds() / 60
    return df

df = load_data()
available_metrics = [m for m in METRICS if m in df.columns]

with st.sidebar:
    st.markdown("### 🌊 Controls")
    st.markdown("---")
    selected_metric = st.selectbox("Primary Metric", options=available_metrics,
        format_func=lambda m: f"{METRICS[m]['label']} ({METRICS[m]['unit']})")
    compare_metric = st.selectbox("Compare With (optional)",
        options=["None"] + [m for m in available_metrics if m != selected_metric],
        format_func=lambda m: "None" if m == "None" else f"{METRICS[m]['label']} ({METRICS[m]['unit']})")
    st.markdown("---")
    sample_size = st.slider("Data Points to Display", min_value=10, max_value=len(df), value=min(500, len(df)), step=10)
    depth_range = None
    if 'Depth feet' in df.columns:
        d_min, d_max = float(df['Depth feet'].min()), float(df['Depth feet'].max())
        depth_range = st.slider("Filter by Depth (ft)", min_value=d_min, max_value=d_max, value=(d_min, d_max), step=0.1)
    st.markdown("---")
    map_style = st.selectbox("Map Style", options=["carto-darkmatter","carto-positron","open-street-map","stamen-terrain"], index=0)
    show_anomalies = st.checkbox("Highlight Anomalies (±2σ)", value=True)
    st.markdown("---")
    st.markdown("<div style='font-size:0.68rem;color:#2a5070;letter-spacing:0.08em'>AUV Survey · Feb 4, 2022<br>Biscayne Bay, South Florida<br>942 observations</div>", unsafe_allow_html=True)

filtered = df.copy()
if depth_range and 'Depth feet' in df.columns:
    filtered = filtered[(filtered['Depth feet'] >= depth_range[0]) & (filtered['Depth feet'] <= depth_range[1])]
filtered = filtered.head(sample_size)
meta = METRICS[selected_metric]

st.markdown(f"""<div class="hero">
  <p class="hero-subtitle">Environmental Monitoring · AUV Survey</p>
  <h1 class="hero-title">Biscayne Bay<br>Water Quality</h1>
  <p class="hero-meta">📍 South Florida &nbsp;|&nbsp; 📅 February 4, 2022 &nbsp;|&nbsp;
  🔬 {len(filtered):,} / {len(df):,} observations &nbsp;|&nbsp;
  📊 Viewing: <strong style="color:#7ecfff">{meta['label']}</strong></p>
</div>""", unsafe_allow_html=True)

col_metrics = [m for m in ['Temp C', 'Sal ppt', 'pH', 'ODO mg/L'] if m in df.columns]
card_html = '<div class="metric-grid">'
for m, color in zip(col_metrics, ['#ff6b35','#00b4d8','#a8dadc','#74c0fc']):
    val = filtered[m].mean()
    info = METRICS[m]
    card_html += f'<div class="metric-card" style="border-top-color:{color}"><div class="metric-label">{info["label"]}</div><div class="metric-value">{val:.2f}</div><div class="metric-unit">avg · {info["unit"]}</div></div>'
card_html += '</div>'
st.markdown(card_html, unsafe_allow_html=True)

map_col, ts_col = st.columns([3, 2])
with map_col:
    st.markdown(f'<div class="section-header">📍 Spatial Distribution — {meta["label"]}</div>', unsafe_allow_html=True)
    plot_df = filtered.dropna(subset=[selected_metric, 'Latitude', 'Longitude'])
    fig_map = px.scatter_mapbox(plot_df, lat="Latitude", lon="Longitude", color=selected_metric,
        size=selected_metric, size_max=14, color_continuous_scale='Turbo', zoom=13, mapbox_style=map_style,
        hover_data={'Timestamp': True, 'Depth feet': True, selected_metric: ':.3f', 'Latitude': False, 'Longitude': False},
        labels={selected_metric: f"{meta['label']} ({meta['unit']})"})
    fig_map.update_layout(**PLOTLY_TEMPLATE, height=420, margin=dict(r=0,t=0,l=0,b=0),
        coloraxis_colorbar=dict(title=f"{meta['unit']}", bgcolor='#071525', tickcolor='#5a8ab0', outlinecolor='#0e2a45', title_font_color='#7aabcc'))
    st.plotly_chart(fig_map, use_container_width=True)

with ts_col:
    st.markdown('<div class="section-header">📈 Temporal Trend</div>', unsafe_allow_html=True)
    ts_df = filtered.dropna(subset=[selected_metric,'Timestamp']).sort_values('Timestamp').copy()
    ts_df['rolling'] = ts_df[selected_metric].rolling(window=20, center=True, min_periods=1).mean()
    mean_v, std_v = ts_df[selected_metric].mean(), ts_df[selected_metric].std()
    ts_df['anomaly'] = (ts_df[selected_metric] - mean_v).abs() > 2 * std_v
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=ts_df['Timestamp'], y=ts_df[selected_metric], mode='markers',
        marker=dict(size=3, color=meta['color'], opacity=0.35), name='Raw'))
    fig_ts.add_trace(go.Scatter(x=ts_df['Timestamp'], y=ts_df['rolling'], mode='lines',
        line=dict(color=meta['color'], width=2), name='20-pt avg'))
    if show_anomalies:
        anom = ts_df[ts_df['anomaly']]
        fig_ts.add_trace(go.Scatter(x=anom['Timestamp'], y=anom[selected_metric], mode='markers',
            marker=dict(size=8, color='#ff4444', symbol='x'), name='Anomaly (±2σ)'))
    fig_ts.update_layout(**PLOTLY_TEMPLATE, height=420, margin=dict(r=10,t=10,l=10,b=40),
        legend=dict(orientation='h',y=-0.15,x=0,font=dict(size=10)),
        xaxis_title='Time', yaxis_title=f"{meta['label']} ({meta['unit']})")
    st.plotly_chart(fig_ts, use_container_width=True)

st.markdown("---")
depth_col, corr_col = st.columns(2)
with depth_col:
    st.markdown('<div class="section-header">🔭 Depth Profile</div>', unsafe_allow_html=True)
    if 'Depth feet' in filtered.columns:
        dp_df = filtered.dropna(subset=[selected_metric,'Depth feet']).copy()
        dp_df['depth_bin'] = (dp_df['Depth feet'] / 0.5).round() * 0.5
        depth_profile = dp_df.groupby('depth_bin')[selected_metric].agg(['mean','std']).reset_index()
        depth_profile.columns = ['Depth (ft)','Mean','Std']
        fig_depth = go.Figure()
        fig_depth.add_trace(go.Scatter(x=depth_profile['Mean'], y=depth_profile['Depth (ft)'],
            mode='lines+markers', line=dict(color=meta['color'],width=2), marker=dict(size=5,color=meta['color']),
            error_x=dict(array=depth_profile['Std'],color='#0e2a45',thickness=1), name=meta['label']))
        fig_depth.update_layout(**PLOTLY_TEMPLATE, height=340, margin=dict(r=10,t=10,l=10,b=10),
            xaxis_title=f"{meta['label']} ({meta['unit']})",
            yaxis=dict(title='Depth (ft)',autorange='reversed',gridcolor='#0e2a45'))
        st.plotly_chart(fig_depth, use_container_width=True)
        st.markdown('<div class="info-box">Depth profile shows mean ± std at each 0.5 ft bin.</div>', unsafe_allow_html=True)

with corr_col:
    st.markdown('<div class="section-header">🔗 Correlation Matrix</div>', unsafe_allow_html=True)
    corr_metrics = [m for m in available_metrics if m in filtered.columns]
    corr_df = filtered[corr_metrics].dropna()
    corr_mat = corr_df.corr()
    short_labels = [METRICS[m]['label'] for m in corr_metrics]
    fig_corr = go.Figure(go.Heatmap(z=corr_mat.values, x=short_labels, y=short_labels,
        colorscale='RdBu_r', zmid=0, zmin=-1, zmax=1,
        text=np.round(corr_mat.values, 2), texttemplate='%{text}', textfont=dict(size=9,color='#c8dff0'),
        colorbar=dict(bgcolor='#071525',tickcolor='#5a8ab0',outlinecolor='#0e2a45',title_font_color='#7aabcc',title='r')))
    fig_corr.update_layout(**PLOTLY_TEMPLATE, height=340, margin=dict(r=10,t=10,l=10,b=10),
        xaxis=dict(tickfont=dict(size=9)), yaxis=dict(tickfont=dict(size=9)))
    st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")
cmp_col, hist_col = st.columns(2)
with cmp_col:
    if compare_metric != "None" and compare_metric in filtered.columns:
        st.markdown(f'<div class="section-header">⚡ {meta["label"]} vs {METRICS[compare_metric]["label"]}</div>', unsafe_allow_html=True)
        cmp_df = filtered.dropna(subset=[selected_metric, compare_metric])
        fig_cmp = px.scatter(cmp_df, x=selected_metric, y=compare_metric, color='Elapsed Min',
            color_continuous_scale='Turbo', trendline='ols',
            labels={selected_metric: f"{meta['label']} ({meta['unit']})",
                    compare_metric: f"{METRICS[compare_metric]['label']} ({METRICS[compare_metric]['unit']})",
                    'Elapsed Min': 'Elapsed (min)'})
        fig_cmp.update_traces(marker=dict(size=4, opacity=0.7))
        fig_cmp.update_layout(**PLOTLY_TEMPLATE, height=320, margin=dict(r=10,t=10,l=10,b=10))
        st.plotly_chart(fig_cmp, use_container_width=True)
        r = cmp_df[[selected_metric, compare_metric]].corr().iloc[0,1]
        color = '#52b788' if abs(r)>0.5 else '#e9c46a' if abs(r)>0.2 else '#5a8ab0'
        st.markdown(f'<div class="info-box">Pearson <em>r</em> = <strong style="color:{color}">{r:.3f}</strong></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-header">⚡ Dual-Axis Overlay</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">Select a second metric in the sidebar to enable scatter comparison with OLS trendline.</div>', unsafe_allow_html=True)

with hist_col:
    st.markdown(f'<div class="section-header">📊 Distribution — {meta["label"]}</div>', unsafe_allow_html=True)
    hist_df = filtered.dropna(subset=[selected_metric])
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(x=hist_df[selected_metric], nbinsx=40, marker_color=meta['color'], opacity=0.8))
    m_mean, m_med = hist_df[selected_metric].mean(), hist_df[selected_metric].median()
    for val, label, col in [(m_mean,'Mean','#ffffff'),(m_med,'Median','#7ecfff')]:
        fig_hist.add_vline(x=val, line_dash='dash', line_color=col, line_width=1.5,
            annotation_text=f"{label}: {val:.2f}", annotation_font_color=col, annotation_font_size=10)
    fig_hist.update_layout(**PLOTLY_TEMPLATE, height=320, margin=dict(r=10,t=10,l=10,b=10),
        xaxis_title=f"{meta['label']} ({meta['unit']})", yaxis_title="Count", bargap=0.05, showlegend=False)
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")
stat_col, anom_col = st.columns([3, 2])
with stat_col:
    st.markdown('<div class="section-header">📋 Statistical Summary — All Metrics</div>', unsafe_allow_html=True)
    summary = filtered[available_metrics].describe().T
    summary.index = [METRICS[m]['label'] for m in summary.index]
    st.dataframe(summary.round(4), use_container_width=True)

with anom_col:
    st.markdown(f'<div class="section-header">⚠️ Anomaly Report — {meta["label"]}</div>', unsafe_allow_html=True)
    m_val, s_val = filtered[selected_metric].mean(), filtered[selected_metric].std()
    anom_rows = filtered[(filtered[selected_metric]-m_val).abs() > 2*s_val][['Timestamp',selected_metric,'Depth feet','Latitude','Longitude']].dropna()
    if len(anom_rows) > 0:
        st.dataframe(anom_rows.rename(columns={selected_metric:f"{meta['label']} ({meta['unit']})"}).head(30), use_container_width=True)
        st.markdown(f'<div class="warn-box">{len(anom_rows)} anomalous readings detected (beyond ±2σ from mean {m_val:.2f} {meta["unit"]}).</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">No anomalies detected at ±2σ threshold.</div>', unsafe_allow_html=True)

st.markdown("---")
with st.expander("🗄️ Raw Data Table"):
    st.dataframe(filtered, use_container_width=True)
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(label="⬇️ Download Filtered Data as CSV", data=csv,
        file_name=f"biscayne_bay_{selected_metric.replace(' ','_').replace('/','_')}_filtered.csv", mime='text/csv')

st.markdown('<div class="footer">Biscayne Bay Water Quality Dashboard · AUV Survey Feb 4 2022 · Built with Streamlit, Plotly & Pandas · Environmental Data Science</div>', unsafe_allow_html=True)
