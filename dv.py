
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Medical Reports Dashboard",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Medical Reports Analytics Dashboard")
st.write("Interactive dashboard for analyzing medical reports.")

# Generate sample medical data
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 300

    data = pd.DataFrame({
        "Patient_ID": [f"P{i+1:03}" for i in range(n)],
        "Age": np.random.randint(18, 90, n),
        "Gender": np.random.choice(
            ["Male", "Female"], n
        ),
        "Blood_Group": np.random.choice(
            ["A+", "A-", "B+", "B-", "AB+", "O+", "O-"], n
        ),
        "Condition": np.random.choice(
            ["Diabetes", "Heart Disease",
             "Hypertension", "Asthma", "Healthy"], n
        ),
        "Glucose": np.random.normal(110, 25, n).round(1),
        "Report_Status": np.random.choice(
            ["Normal", "Abnormal"], n, p=[0.7, 0.3]
        )
    })

    return data


df = load_data()

# Sidebar filters
st.sidebar.header("Filter Medical Reports")

conditions = st.sidebar.multiselect(
    "Select Conditions",
    options=sorted(df["Condition"].unique()),
    default=sorted(df["Condition"].unique())
)

genders = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

blood_groups = st.sidebar.multiselect(
    "Select Blood Groups",
    options=sorted(df["Blood_Group"].unique()),
    default=sorted(df["Blood_Group"].unique())
)

statuses = st.sidebar.multiselect(
    "Select Report Status",
    options=sorted(df["Report_Status"].unique()),
    default=sorted(df["Report_Status"].unique())
)

age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max()))
)

# Apply filters
filtered_df = df[
    (df["Condition"].isin(conditions)) &
    (df["Gender"].isin(genders)) &
    (df["Blood_Group"].isin(blood_groups)) &
    (df["Report_Status"].isin(statuses)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

# KPI cards
st.subheader("📊 Key Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Patients", len(filtered_df))

c2.metric(
    "Average Age",
    f"{filtered_df['Age'].mean():.1f}"
    if not filtered_df.empty else "N/A"
)

c3.metric(
    "Abnormal Reports",
    int((filtered_df["Report_Status"] == "Abnormal").sum())
)

c4.metric(
    "Average Glucose",
    f"{filtered_df['Glucose'].mean():.1f}"
    if not filtered_df.empty else "N/A"
)

st.divider()

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# BAR GRAPH
st.subheader("1. Patients by Medical Condition")

condition_counts = (
    filtered_df["Condition"]
    .value_counts()
    .reset_index()
)
condition_counts.columns = ["Condition", "Patients"]

fig_bar = px.bar(
    condition_counts,
    x="Condition",
    y="Patients",
    color="Condition",
    title="Number of Patients by Condition",
    text="Patients"
)

st.plotly_chart(fig_bar, use_container_width=True)

# PIE CHART
st.subheader("2. Patient Distribution by Gender")

gender_counts = (
    filtered_df["Gender"]
    .value_counts()
    .reset_index()
)
gender_counts.columns = ["Gender", "Patients"]

fig_pie = px.pie(
    gender_counts,
    names="Gender",
    values="Patients",
    hole=0.35,
    title="Gender Distribution"
)

st.plotly_chart(fig_pie, use_container_width=True)

# HISTOGRAM
st.subheader("3. Patient Age Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="Age",
    color="Gender",
    nbins=15,
    title="Age Distribution of Patients",
    labels={"Age": "Age in Years"}
)

st.plotly_chart(fig_hist, use_container_width=True)

# SCATTER PLOT
st.subheader("4. Age vs Glucose Level")

fig_scatter = px.scatter(
    filtered_df,
    x="Age",
    y="Glucose",
    color="Condition",
    hover_data=["Patient_ID", "Gender"],
    title="Relationship Between Age and Glucose"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# BLOOD GROUP BAR CHART
st.subheader("5. Patients by Blood Group")

blood_counts = (
    filtered_df["Blood_Group"]
    .value_counts()
    .reset_index()
)
blood_counts.columns = ["Blood Group", "Patients"]

fig_blood = px.bar(
    blood_counts,
    x="Blood Group",
    y="Patients",
    color="Blood Group",
    title="Blood Group Distribution"
)

st.plotly_chart(fig_blood, use_container_width=True)

# REPORT STATUS PIE CHART
st.subheader("6. Medical Report Status")

status_counts = (
    filtered_df["Report_Status"]
    .value_counts()
    .reset_index()
)
status_counts.columns = ["Status", "Count"]

fig_status = px.pie(
    status_counts,
    names="Status",
    values="Count",
    title="Normal vs Abnormal Reports"
)

st.plotly_chart(fig_status, use_container_width=True)

# PATIENT TABLE
st.subheader("📋 Patient Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Download filtered data
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Medical Reports CSV",
    data=csv,
    file_name="medical_reports.csv",
    mime="text/csv"
)

st.caption(
    "Educational demo using randomly generated data. "
    "Not intended for medical diagnosis."
)
