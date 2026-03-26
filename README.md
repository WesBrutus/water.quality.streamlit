# 🌊 Biscayne Bay Water Quality Dashboard

An interactive Streamlit web application for visualizing and analyzing water quality data from Biscayne Bay, Florida.

---

## Purpose

This dashboard provides researchers and students with an interactive tool to explore water quality data collected from Biscayne Bay via Autonomous Underwater Vehicle (AUV).

**Users can:**
- Visualize spatial distribution of water quality parameters across the bay
- Analyze temporal trends and rolling averages in environmental measurements
- Explore statistical patterns and distributions in the data
- Detect anomalous readings automatically (±2σ threshold)
- Compare any two parameters with scatter plot + OLS trendline
- Examine how parameters vary with depth
- Download filtered data as CSV

**Educational Goals:**
- Demonstrate interactive data visualization with Plotly
- Build web applications with Streamlit
- Apply data manipulation with Pandas and NumPy
- Practice AGILE software development methodology

---

## Dataset

**Biscayne Bay Water Quality Data**

| Field | Details |
|---|---|
| File | `biscayneBay_waterquality.csv` |
| Collection Method | Autonomous Underwater Vehicle (AUV) with multi-parameter sensors |
| Date | February 4, 2022 |
| Location | Biscayne Bay, South Florida |
| Observations | 942 data points |
| Coverage | Multiple locations across the bay |

### Parameters Measured

| Parameter | Unit | Description |
|---|---|---|
| Temperature | °C | Water temperature |
| Salinity | ppt | Salt concentration |
| pH | scale | Acidity/alkalinity |
| Dissolved Oxygen | mg/L | Available oxygen for marine life |
| Chlorophyll-a | µg/L | Algae/phytoplankton indicator |
| Turbidity | NTU | Water clarity measurement |
| Blue-Green Algae | cells/mL | Cyanobacteria density |
| Depth | feet | Measurement depth |
| Coordinates | Lat/Lon | GPS location |

---

## Features

### 🎛️ Sidebar Controls
| Control | Description |
|---|---|
| **Primary Metric** | Choose from 8 water quality parameters |
| **Compare With** | Select a second metric for scatter comparison |
| **Data Points Slider** | Adjust number of points displayed (10–942) |
| **Depth Range Filter** | Filter dataset by depth before rendering |
| **Map Style** | Toggle between dark/light/terrain/OSM tile layers |
| **Highlight Anomalies** | Toggle ±2σ anomaly markers on time series |

### 📊 Visualizations

| Section | Chart | Description |
|---|---|---|
| Hero | KPI Cards | Live avg for Temperature, Salinity, pH, Dissolved Oxygen |
| Row 1 | Interactive Map | Spatial distribution with Turbo color scale + hover tooltips |
| Row 1 | Time Series | Raw scatter + 20-point rolling average + anomaly markers |
| Row 2 | Depth Profile | Selected metric vs depth (0.5 ft bins, ±std error bars) |
| Row 2 | Correlation Matrix | Pearson r heatmap for all 8 parameters |
| Row 3 | Scatter Comparison | Dual-metric scatter colored by elapsed time + OLS trendline + r-value |
| Row 3 | Distribution | 40-bin histogram with mean/median reference lines |
| Row 4 | Stats Table | Full describe() summary for all metrics |
| Row 4 | Anomaly Report | Table of ±2σ outliers with GPS coordinates + depth |
| Footer | Raw Data | Expandable full dataset + CSV download button |

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Get the Files

Make sure these files are in the same folder:

```
your-project/
├── main.py                        # Streamlit app
├── biscayneBay_waterquality.csv   # Data file (REQUIRED)
└── requirements.txt               # Dependencies
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run

> ⚠️ **IMPORTANT:** Always use `streamlit run`, never `python main.py`

```bash
streamlit run main.py
```

The dashboard opens automatically at **http://localhost:8501**

---

## Using the Dashboard

1. **Select a Primary Metric** — use the sidebar dropdown to choose which water quality parameter to visualize across all charts
2. **Select a Comparison Metric** — optionally pick a second parameter to enable the scatter comparison panel
3. **Adjust Data Points** — use the slider to control how many of the 942 observations are shown
4. **Filter by Depth** — narrow the dataset to a specific depth range
5. **Explore the Map** — hover over points to see values, timestamp, and depth; zoom/pan freely
6. **View Trends** — time series shows raw data, 20-point rolling mean, and anomaly flags
7. **Check Correlations** — the heatmap reveals which parameters co-vary across the mission
8. **Inspect Anomalies** — outliers beyond ±2σ are highlighted in the chart and listed in the anomaly table with their GPS coordinates
9. **Download Data** — expand Raw Data and click the CSV download button to export the current filtered dataset

---

## AGILE Development Process

This project was built using AGILE methodology across 4 sprints.

### Sprint 1 — Foundation (Week 1)
**Goal:** Load and understand the data

**Completed:**
- Data loading function with `@st.cache_data`
- Column name cleaning (`.str.strip()`)
- DateTime parsing for temporal analysis

### Sprint 2 — Visualizations (Week 2)
**Goal:** Create interactive charts

**Completed:**
- Interactive Plotly map with hover tooltips
- Time series line chart
- Responsive two-column layout

### Sprint 3 — User Controls (Week 3)
**Goal:** Add interactivity and polish

**Completed:**
- Parameter selection dropdown
- Data sample slider
- Statistical summary table
- Expandable raw data view
- Documentation and styling

### Sprint 4 — Advanced Analytics (Week 4)
**Goal:** Expand analytical depth and visual design

**Completed:**
- Dark ocean editorial theme (custom CSS, DM Serif Display + DM Mono fonts)
- Live KPI cards (Temperature, Salinity, pH, Dissolved Oxygen)
- Depth profile chart (mean ± std per 0.5 ft bin, reversed y-axis)
- Correlation matrix heatmap (all 8 parameters)
- Scatter comparison panel with OLS trendline + Pearson r
- Distribution histogram with mean/median reference lines
- Rolling average overlay on time series (20-point window)
- Anomaly detection (±2σ flagging on chart + GPS table)
- Depth range filter slider
- Map style picker (dark/light/terrain/OSM)
- Anomaly highlight toggle
- CSV download button for filtered data
- Centralized METRICS config dict + shared PLOTLY_TEMPLATE

---

## Code Structure

```python
# 1. Imports & Page Config
# 2. Custom CSS (ocean dark theme)
# 3. METRICS config dict — label, unit, color per parameter
# 4. PLOTLY_TEMPLATE — shared dark chart styling
# 5. load_data() — cached CSV load, timestamp parse, Elapsed Min column
# 6. Sidebar widgets — metric selectors, sliders, toggles
# 7. Hero banner + KPI cards
# 8. Row 1: Map | Time Series
# 9. Row 2: Depth Profile | Correlation Matrix
# 10. Row 3: Scatter Comparison | Histogram
# 11. Row 4: Stats Table | Anomaly Report
# 12. Raw Data expander + CSV Download
```

---

## Technologies

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.8+ | Programming language |
| Streamlit | 1.31.0 | Web app framework |
| Pandas | 2.2.0 | Data manipulation |
| Plotly | 5.18.0 | Interactive charts |
| NumPy | 1.26.0 | Numerical operations |
| SciPy (via statsmodels) | — | OLS trendline (via Plotly trendline='ols') |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `"missing ScriptRunContext"` warnings | Use `streamlit run main.py`, not `python main.py` |
| `FileNotFoundError: biscayneBay_waterquality.csv` | CSV must be in the same folder as `main.py` |
| `KeyError: 'Date m/d/y'` | Code already handles this via `df.columns.str.strip()` |
| Blank map | Ensure you have an internet connection (map tiles are fetched live) |
| OLS trendline error | Run `pip install statsmodels` |

---

## Acknowledgments

- Water quality data from Biscayne Bay AUV monitoring
- Built with Python, Streamlit, Plotly, Pandas, and NumPy
- Developed using AGILE methodology across 4 sprints
