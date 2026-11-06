import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION & HEADER
# =========================================================
st.set_page_config(
    page_title="Healthcare Dashboard",
    layout="wide"
)

logo_path = Path(__file__).parent / "healthcare.png"
header_image, header_text = st.columns([1, 7])

with header_image:
    if logo_path.exists():
        st.image(str(logo_path), width=100)

with header_text:
    st.title("Healthcare Performance Dashboard")
    st.write("Healthcare analytics and performance monitoring")

# =========================================================
# CUSTOM CSS (DARK THEME & GRADIENT KPI CARDS)
# =========================================================
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: #FFFFFF;
}

h1, h2, h3, h4 {
    color: #FFFFFF !important;
}

/* Base KPI card */
[data-testid="stMetric"] {
    border-radius: 18px !important;
    padding: 20px !important;
    min-height: 125px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.55) !important;
    overflow: hidden !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

/* Five Different Gradient Colors for KPIs */
[data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="stMetric"] {
    background: linear-gradient(135deg, #00C6FF 0%, #0072FF 55%, #003BBA 100%) !important;
}

[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] {
    background: linear-gradient(135deg, #C471F5 0%, #8E2DE2 50%, #4A00E0 100%) !important;
}

[data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] {
    background: linear-gradient(135deg, #00F2A9 0%, #00B09B 50%, #008F5A 100%) !important;
}

[data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFD200 0%, #F7971E 50%, #F12711 100%) !important;
}

[data-testid="stHorizontalBlock"] > div:nth-child(5) [data-testid="stMetric"] {
    background: linear-gradient(135deg, #FF758C 0%, #FF416C 50%, #C2185B 100%) !important;
}

[data-testid="stMetricLabel"] {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 29px !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #FFFFFF !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-6px) !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.75) !important;
}

.stDownloadButton button {
    background: linear-gradient(135deg, #2563EB, #7C3AED) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.stDownloadButton button:hover {
    background: linear-gradient(135deg, #1D4ED8, #6D28D9) !important;
    color: #FFFFFF !important;
}

div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1px solid #374151 !important;
}

div[data-baseweb="select"] span {
    color: #FFFFFF !important;
}

@media (max-width: 900px) {
    [data-testid="stMetric"] { min-height: 105px !important; padding: 15px !important; }
    [data-testid="stMetricValue"] { font-size: 22px !important; }
    [data-testid="stMetricLabel"] { font-size: 12px !important; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA SOURCE VALIDATION & LOADING
# =========================================================
CSV_FILE = Path(__file__).parent / "healthcare_dataset.csv"

if not CSV_FILE.exists():
    st.error("❌ healthcare_dataset.csv was not found.")
    st.info("Please place healthcare_dataset.csv in the same folder as app.py.")
    st.stop()

try:
    data = pd.read_csv(CSV_FILE)
except Exception as e:
    st.error(f"❌ Error reading healthcare_dataset.csv: {e}")
    st.stop()

# Standardize Columns
data.columns = data.columns.astype(str).str.strip().str.lower().str.replace(r"\s+", "_", regex=True)

required_cols = [
    "name", "age", "gender", "blood_type", "medical_condition", 
    "date_of_admission", "doctor", "hospital", "insurance_provider", 
    "billing_amount", "room_number", "admission_type", "discharge_date", 
    "medication", "test_results"
]

missing_cols = [col for col in required_cols if col not in data.columns]
if missing_cols:
    st.error("❌ Required columns are missing:")
    st.write(missing_cols)
    st.stop()

# Type Conversion
data["age"] = pd.to_numeric(data["age"], errors="coerce")
data["billing_amount"] = pd.to_numeric(data["billing_amount"], errors="coerce")
data["date_of_admission"] = pd.to_datetime(data["date_of_admission"], errors="coerce")
data["discharge_date"] = pd.to_datetime(data["discharge_date"], errors="coerce")

# Calculate Length of Stay (Days)
data["length_of_stay"] = (data["discharge_date"] - data["date_of_admission"]).dt.days

# Drop completely broken rows if necessary
data = data.dropna(subset=["billing_amount", "age"])

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("📊 Filter Options")

all_hospitals = ["All"] + sorted(data["hospital"].dropna().unique().tolist())
selected_hospital = st.sidebar.selectbox("Select Hospital", all_hospitals)

all_conditions = ["All"] + sorted(data["medical_condition"].dropna().unique().tolist())
selected_condition = st.sidebar.selectbox("Medical Condition", all_conditions)

all_genders = ["All"] + sorted(data["gender"].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", all_genders)

# Apply filters to dataset
filtered_data = data.copy()
if selected_hospital != "All":
    filtered_data = filtered_data[filtered_data["hospital"] == selected_hospital]
if selected_condition != "All":
    filtered_data = filtered_data[filtered_data["medical_condition"] == selected_condition]
if selected_gender != "All":
    filtered_data = filtered_data[filtered_data["gender"] == selected_gender]

# =========================================================
# KPI METRICS DISPLAY
# =========================================================
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

total_patients = len(filtered_data)
total_admissions = len(filtered_data[filtered_data["admission_type"].isin(["Urgent", "Emergency"])])
total_billing = filtered_data["billing_amount"].sum()
avg_billing = filtered_data["billing_amount"].mean() if total_patients > 0 else 0
avg_age = filtered_data["age"].mean() if total_patients > 0 else 0

with kpi_col1:
    st.metric("Total Patients", f"{total_patients:,}")
with kpi_col2:
    st.metric("Acute Admissions", f"{total_admissions:,}")
with kpi_col3:
    st.metric("Total Billing", f"${total_billing:,.2f}")
with kpi_col4:
    st.metric("Avg Billing", f"${avg_billing:,.2f}")
with kpi_col5:
    st.metric("Average Age", f"{avg_age:.1f} Yrs")

st.markdown("---")

# =========================================================
# CHARTS & VISUALIZATIONS
# =========================================================
chart_col1, chart_col2 = st.columns(2)

# Global Dark Plotly Layout Configuration
plotly_dark_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FFFFFF"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.1)", title_font=dict(color="#FFFFFF")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title_font=dict(color="#FFFFFF"))
)

with chart_col1:
    st.subheader("Medical Conditions Breakdown")
    if not filtered_data.empty:
        # Fixed the index aggregation bug by using reset_index
        df_condition = filtered_data.groupby("medical_condition").size().reset_index(name="Count")
        fig_condition = px.bar(
            df_condition,
            x="medical_condition", y="Count",
            labels={"medical_condition": "Condition", "Count": "Number of Patients"},
            color_discrete_sequence=["#00C6FF"]
        )
        fig_condition.update_layout(plotly_dark_layout)
        st.plotly_chart(fig_condition, use_container_width=True)
    else:
        st.info("No records match the current filters.")

with chart_col2:
    st.subheader("Admission Type by Insurance Provider")
    if not filtered_data.empty:
        df_insurance = filtered_data.groupby(["insurance_provider", "admission_type"]).size().reset_index(name="Count")
        fig_insurance = px.bar(
            df_insurance,
            x="insurance_provider", y="Count",
            color="admission_type",
            barmode="group",
            labels={"insurance_provider": "Insurance Provider", "Count": "Admissions"},
            color_discrete_sequence=["#C471F5", "#00F2A9", "#FFD200"]
        )
        fig_insurance.update_layout(plotly_dark_layout)
        st.plotly_chart(fig_insurance, use_container_width=True)
    else:
        st.info("No records match the current filters.")

st.markdown("---")

# =========================================================
# RAW DATA INSPECTION & DOWNLOAD
# =========================================================
st.subheader("📋 Filtered Patient Logs")
if not filtered_data.empty:
    st.dataframe(filtered_data, use_container_width=True)
    
    csv_download = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_download,
        file_name="filtered_healthcare_data.csv",
        mime="text/csv"
    )
else:
    st.info("No data available to display or download.")
