import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    layout="wide"
)

logo_path = Path(__file__).parent / "healthcare.png"

header_image, header_text = st.columns([1, 7])

with header_image:
    if logo_path.exists():
        st.image(
            str(logo_path),
            width=100
        )

with header_text:
    st.title("Healthcare Performance Dashboard")
    st.write("Healthcare analytics and performance monitoring")


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
   APPLICATION
   ========================================================= */

.stApp {
    background-color: #000000;
    color: #FFFFFF;
}


/* =========================================================
   HEADINGS
   ========================================================= */

h1, h2, h3, h4 {
    color: #FFFFFF !important;
}


/* =========================================================
   KPI CARDS
   ========================================================= */

/* Base KPI card */

[data-testid="stMetric"] {
    border-radius: 18px !important;
    padding: 20px !important;
    min-height: 125px !important;

    border: 1px solid rgba(255,255,255,0.15) !important;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.55) !important;

    overflow: hidden !important;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease !important;
}


/* =========================================================
   FIVE DIFFERENT GRADIENT COLORS
   ========================================================= */

/* Total Patients - BLUE */

[data-testid="stHorizontalBlock"]
> div:nth-child(1)
[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            #00C6FF 0%,
            #0072FF 55%,
            #003BBA 100%
        ) !important;
}


/* Total Admissions - PURPLE */

[data-testid="stHorizontalBlock"]
> div:nth-child(2)
[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            #C471F5 0%,
            #8E2DE2 50%,
            #4A00E0 100%
        ) !important;
}


/* Total Billing - GREEN */

[data-testid="stHorizontalBlock"]
> div:nth-child(3)
[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            #00F2A9 0%,
            #00B09B 50%,
            #008F5A 100%
        ) !important;
}


/* Average Billing - ORANGE */

[data-testid="stHorizontalBlock"]
> div:nth-child(4)
[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            #FFD200 0%,
            #F7971E 50%,
            #F12711 100%
        ) !important;
}


/* Average Age - PINK */

[data-testid="stHorizontalBlock"]
> div:nth-child(5)
[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            #FF758C 0%,
            #FF416C 50%,
            #C2185B 100%
        ) !important;
}


/* =========================================================
   KPI TEXT
   ========================================================= */

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


/* =========================================================
   KPI HOVER EFFECT
   ========================================================= */

[data-testid="stMetric"]:hover {
    transform: translateY(-6px) !important;

    box-shadow:
        0 15px 35px rgba(0,0,0,0.75) !important;
}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

.stDownloadButton button {
    background:
        linear-gradient(
            135deg,
            #2563EB,
            #7C3AED
        ) !important;

    color: #FFFFFF !important;

    border: none !important;

    border-radius: 8px !important;

    font-weight: 700 !important;
}


.stDownloadButton button:hover {
    background:
        linear-gradient(
            135deg,
            #1D4ED8,
            #6D28D9
        ) !important;

    color: #FFFFFF !important;
}


/* =========================================================
   SELECT BOX
   ========================================================= */

div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1px solid #374151 !important;
}


div[data-baseweb="select"] span {
    color: #FFFFFF !important;
}


/* =========================================================
   RESPONSIVE KPI
   ========================================================= */

@media (max-width: 900px) {

    [data-testid="stMetric"] {
        min-height: 105px !important;
        padding: 15px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 22px !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
    }
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================



# =========================================================
# CSV FILE
# =========================================================

CSV_FILE = (
    Path(__file__).parent
    / "healthcare_dataset.csv"
)


# =========================================================
# CHECK CSV
# =========================================================

if not CSV_FILE.exists():

    st.error(
        "❌ healthcare_dataset.csv was not found."
    )

    st.info(
        "Please place healthcare_dataset.csv "
        "in the same folder as app.py."
    )

    st.stop()


# =========================================================
# LOAD DATA
# =========================================================

try:

    data = pd.read_csv(
        CSV_FILE
    )

except Exception as e:

    st.error(
        f"❌ Error reading healthcare_dataset.csv: {e}"
    )

    st.stop()


# =========================================================
# STANDARDIZE COLUMN NAMES
# =========================================================

data.columns = (
    data.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(
        r"\s+",
        "_",
        regex=True
    )
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_cols = [

    "name",
    "age",
    "gender",
    "blood_type",
    "medical_condition",
    "date_of_admission",
    "doctor",
    "hospital",
    "insurance_provider",
    "billing_amount",
    "room_number",
    "admission_type",
    "discharge_date",
    "medication",
    "test_results"

]


# =========================================================
# VALIDATE COLUMNS
# =========================================================

missing_cols = [

    column

    for column in required_cols

    if column not in data.columns

]


if missing_cols:

    st.error(
        "❌ Required columns are missing:"
    )

    st.write(
        missing_cols
    )

    st.write(
        "Columns available in your CSV:"
    )

    st.write(
        data.columns.tolist()
    )

    st.stop()


# =========================================================
# DATA TYPE CONVERSION
# =========================================================

data["age"] = pd.to_numeric(
    data["age"],
    errors="coerce"
)


data["billing_amount"] = pd.to_numeric(
    data["billing_amount"],
    errors="coerce"
)


data["date_of_admission"] = pd.to_datetime(
    data["date_of_admission"],
    errors="coerce"
)


data["discharge_date"] = pd.to_datetime(
    data["discharge_date"],
    errors="coerce"
)


# =========================================================
# LENGTH OF STAY
# =========================================================

data["length_of_stay"] = (
    data["discharge_date"]
    -
    data["date_of_admission"]
).dt.days


# =========================================================
# MONTH
# =========================================================

data["month"] = (
    data["date_of_admission"]
    .dt.strftime("%b-%Y")
)


# =========================================================
# MONTH DATE
# =========================================================

data["month_date"] = (
    data["date_of_admission"]
    .dt.to_period("M")
    .dt.to_timestamp()
)


# =========================================================
# CLEAN BILLING
# =========================================================

data["billing_amount"] = (
    data["billing_amount"]
    .fillna(0)
)


# =========================================================
# FILTER SECTION
# =========================================================

st.subheader(
    "🔎 Dashboard Filters"
)


f1, f2, f3 = st.columns(3)


# =========================================================
# GENDER
# =========================================================

with f1:

    gender = st.selectbox(

        "Select Gender",

        ["All"] +

        sorted(
            data["gender"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    )


# =========================================================
# HOSPITAL
# =========================================================

with f2:

    hospital = st.selectbox(

        "Select Hospital",

        ["All"] +

        sorted(
            data["hospital"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    )


# =========================================================
# MEDICAL CONDITION
# =========================================================

with f3:

    medical_condition = st.selectbox(

        "Select Medical Condition",

        ["All"] +

        sorted(
            data["medical_condition"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered = data.copy()


if gender != "All":

    filtered = filtered[
        filtered["gender"].astype(str)
        == gender
    ]


if hospital != "All":

    filtered = filtered[
        filtered["hospital"].astype(str)
        == hospital
    ]


if medical_condition != "All":

    filtered = filtered[
        filtered["medical_condition"].astype(str)
        == medical_condition
    ]


# =========================================================
# EMPTY DATA
# =========================================================

if filtered.empty:

    st.warning(
        "⚠️ No records match the selected filters."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_patients = (
    filtered["name"].nunique()
)


total_admissions = (
    len(filtered)
)


total_billing = (
    filtered["billing_amount"].sum()
)


avg_billing = (
    filtered["billing_amount"].mean()
)


avg_age = (
    filtered["age"].mean()
)


avg_stay = (
    filtered["length_of_stay"].mean()
)


# =========================================================
# HANDLE NaN
# =========================================================

if pd.isna(avg_billing):

    avg_billing = 0


if pd.isna(avg_age):

    avg_age = 0


if pd.isna(avg_stay):

    avg_stay = 0


# =========================================================
# KPI SECTION
# =========================================================

st.subheader(
    "📊 Key Performance Indicators"
)


k1, k2, k3, k4, k5 = st.columns(5)


# =========================================================
# KPI 1
# =========================================================

with k1:

    st.metric(
        label="👥 Total Patients",
        value=f"{total_patients:,}"
    )


# =========================================================
# KPI 2
# =========================================================

with k2:

    st.metric(
        label="🏥 Total Admissions",
        value=f"{total_admissions:,}"
    )


# =========================================================
# KPI 3
# =========================================================

with k3:

    st.metric(
        label="💰 Total Billing",
        value=f"₹{total_billing:,.2f}"
    )


# =========================================================
# KPI 4
# =========================================================

with k4:

    st.metric(
        label="💳 Average Billing",
        value=f"₹{avg_billing:,.2f}"
    )


# =========================================================
# KPI 5
# =========================================================

with k5:

    st.metric(
        label="👤 Average Age",
        value=f"{avg_age:.1f} years"
    )


# =========================================================
# GAUGE FUNCTION
# =========================================================

def gauge(
    title,
    value,
    minimum,
    maximum,
    suffix=""
):

    value = float(value)


    if maximum <= minimum:

        maximum = minimum + 1


    display_value = max(
        minimum,
        min(value, maximum)
    )


    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=display_value,

            number={
                "suffix": suffix,
                "font": {
                    "size": 28,
                    "color": "white"
                }
            },

            title={
                "text": title,
                "font": {
                    "size": 18,
                    "color": "white"
                }
            },

            gauge={

                "axis": {
                    "range": [
                        minimum,
                        maximum
                    ],
                    "tickcolor": "white"
                },

                "bar": {
                    "color": "#144FE2"
                },

                "bgcolor": "#20A790",

                "steps": [

                    {
                        "range": [
                            minimum,
                            minimum +
                            (
                                maximum -
                                minimum
                            ) * 0.50
                        ],
                        "color": "#29B867"
                    },

                    {
                        "range": [
                            minimum +
                            (
                                maximum -
                                minimum
                            ) * 0.50,

                            minimum +
                            (
                                maximum -
                                minimum
                            ) * 0.80
                        ],
                        "color": "#99642F"
                    },

                    {
                        "range": [
                            minimum +
                            (
                                maximum -
                                minimum
                            ) * 0.80,

                            maximum
                        ],
                        "color": "#962C2C"
                    }

                ],

                "threshold": {

                    "line": {
                        "color": "#FFFFFF",
                        "width": 4
                    },

                    "thickness": 0.75,

                    "value": display_value

                }

            }

        )

    )


    fig.update_layout(

        height=250,

        margin=dict(
            l=10,
            r=10,
            t=40,
            b=10
        ),

        paper_bgcolor="black",

        plot_bgcolor="black",

        font={
            "color": "white"
        }

    )


    return fig


# =========================================================
# HEALTHCARE METRICS
# =========================================================

st.subheader(
    "📈 Healthcare Metrics"
)


g1, g2, g3, g4 = st.columns(4)


# =========================================================
# AVERAGE AGE
# =========================================================

g1.plotly_chart(

    gauge(
        "Average Age",
        avg_age,
        0,
        100,
        " years"
    ),

    use_container_width=True

)


# =========================================================
# AVERAGE BILLING
# =========================================================

billing_max = max(
    avg_billing * 2,
    1
)


g2.plotly_chart(

    gauge(
        "Average Billing",
        avg_billing,
        0,
        billing_max,
        " rupees"
    ),

    use_container_width=True

)


# =========================================================
# TOTAL PATIENTS
# =========================================================

patients_max = max(
    total_patients * 1.25,
    1
)


g3.plotly_chart(

    gauge(
        "Total Patients",
        total_patients,
        0,
        patients_max,
        ""
    ),

    use_container_width=True

)


# =========================================================
# AVERAGE STAY
# =========================================================

stay_max = max(
    avg_stay * 2,
    1
)


g4.plotly_chart(

    gauge(
        "Average Stay",
        avg_stay,
        0,
        stay_max,
        " days"
    ),

    use_container_width=True

)


# =========================================================
# HOSPITAL BILLING
# =========================================================

st.subheader(
    "🏥 Hospital Billing Analysis"
)


hospital_billing = (

    filtered

    .groupby(
        "hospital",
        as_index=False
    )["billing_amount"]

    .sum()

    .sort_values(
        "billing_amount",
        ascending=False
    )

)


fig = px.bar(

    hospital_billing,

    x="hospital",

    y="billing_amount",

    title="Total Billing Amount by Hospital",

    labels={
        "hospital": "Hospital",
        "billing_amount":
            "Total Billing Amount"
    },

    color="billing_amount",

    color_continuous_scale="Reds"

)


fig.update_layout(

    height=450,

    xaxis_tickangle=-45,

    showlegend=False,

    plot_bgcolor="black",

    paper_bgcolor="black",

    font={
        "color": "white"
    }

)


fig.update_traces(

    hovertemplate=
    "<b>%{x}</b><br>"
    "Total Billing: ₹%{y:,.2f}"
    "<extra></extra>"

)


st.plotly_chart(

    fig,

    use_container_width=True

)


# =========================================================
# MONTHLY BILLING
# =========================================================

st.subheader(
    "📅 Monthly Billing Trend"
)


monthly_billing = (

    filtered

    .dropna(
        subset=["month_date"]
    )

    .groupby(
        [
            "month",
            "month_date"
        ],
        as_index=False
    )["billing_amount"]

    .sum()

    .sort_values(
        "month_date"
    )

)


fig = px.line(

    monthly_billing,

    x="month",

    y="billing_amount",

    title="Monthly Billing Amount Trend",

    labels={
        "month": "Month",
        "billing_amount":
            "Total Billing Amount"
    },

    markers=True

)


fig.update_traces(

    line={
        "width": 3,
        "color": "#00C6FF"
    },

    marker={
        "size": 7,
        "color": "#8E2DE2"
    },

    hovertemplate=
    "<b>%{x}</b><br>"
    "Billing: ₹%{y:,.2f}"
    "<extra></extra>"

)


fig.update_layout(

    height=450,

    plot_bgcolor="black",

    paper_bgcolor="black",

    hovermode="x unified",

    font={
        "color": "white"
    },

    xaxis={
        "title": "Month",
        "tickangle": -45
    },

    yaxis={
        "title": "Total Billing Amount"
    }

)


st.plotly_chart(

    fig,

    use_container_width=True

)


# =========================================================
# MEDICAL CONDITION BILLING
# =========================================================

st.subheader(
    "🩺 Monthly Medical Bill by Condition"
)


monthly_condition = (

    filtered

    .dropna(
        subset=["month_date"]
    )

    .groupby(
        [
            "month",
            "month_date",
            "medical_condition"
        ],
        as_index=False
    )["billing_amount"]

    .sum()

    .sort_values(
        "month_date"
    )

)


fig = px.bar(

    monthly_condition,

    x="month",

    y="billing_amount",

    color="medical_condition",

    title="Medical Condition Billing by Month",

    labels={

        "month": "Month",

        "billing_amount":
            "Total Billing Amount",

        "medical_condition":
            "Medical Condition"

    },

    barmode="stack"

)


fig.update_layout(

    height=500,

    plot_bgcolor="black",

    paper_bgcolor="black",

    hovermode="x unified",

    font={
        "color": "white"
    },

    xaxis={
        "title": "Month",
        "tickangle": -45
    },

    yaxis={
        "title": "Total Billing Amount"
    },

    legend={
        "title": "Medical Condition"
    }

)


fig.update_traces(

    hovertemplate=
    "<b>%{x}</b><br>"
    "%{fullData.name}: ₹%{y:,.2f}"
    "<extra></extra>"

)


st.plotly_chart(

    fig,

    use_container_width=True

)


# =========================================================
# MEDICAL CONDITION DISTRIBUTION
# =========================================================

st.subheader(
    "🩺 Patients by Medical Condition"
)


condition_count = (

    filtered[
        "medical_condition"
    ]

    .value_counts()

    .reset_index()

)


condition_count.columns = [

    "medical_condition",
    "patients"

]


fig = px.pie(

    condition_count,

    names="medical_condition",

    values="patients",

    title=
    "Patient Distribution by Medical Condition",

    hole=0.4

)


fig.update_layout(

    paper_bgcolor="black",

    font={
        "color": "white"
    }

)


st.plotly_chart(

    fig,

    use_container_width=True

)


# =========================================================
# ADMISSION TYPE
# =========================================================

st.subheader(
    "🚑 Admission Type Analysis"
)


admission_count = (

    filtered[
        "admission_type"
    ]

    .value_counts()

    .reset_index()

)


admission_count.columns = [

    "admission_type",
    "patients"

]


fig = px.bar(

    admission_count,

    x="admission_type",

    y="patients",

    title="Patients by Admission Type",

    color="admission_type"

)


fig.update_layout(

    plot_bgcolor="black",

    paper_bgcolor="black",

    font={
        "color": "white"
    }

)


st.plotly_chart(

    fig,

    use_container_width=True

)


# =========================================================
# DATA TABLE
# =========================================================

st.subheader(
    "📋 Healthcare Data Table"
)


st.dataframe(

    filtered,

    use_container_width=True,

    height=400

)


# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================

csv_data = filtered.to_csv(
    index=False
)


st.download_button(

    label="⬇️ Download Filtered Data",

    data=csv_data,

    file_name="filtered_healthcare_data.csv",

    mime="text/csv"

)
