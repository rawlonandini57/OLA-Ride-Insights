import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page Config
st.set_page_config(page_title="OLA Ride Insights", layout="wide")

st.title("🚕 OLA Ride Insights Dashboard")

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📈 Power BI", "🗄️ SQL Queries", "📋 Raw Data", "📸 Images"])

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("OLA_Ride_Data_Sheet.csv")
    return df

df = load_data()

# TAB 1: Dashboard
with tab1:
    st.header("OLA Ride Insights Dashboard")
    
    # Sidebar Filters
    st.sidebar.header("Filters")
    
    pickup_location = st.sidebar.multiselect(
        "Select Pickup Location",
        options=df["Pickup_Location"].unique(),
        default=df["Pickup_Location"].unique()
    )
    
    vehicle = st.sidebar.multiselect(
        "Select Vehicle Type",
        options=df["Vehicle_Type"].unique(),
        default=df["Vehicle_Type"].unique()
    )
    
    df_filtered = df[(df["Pickup_Location"].isin(pickup_location)) & (df["Vehicle_Type"].isin(vehicle))]
    
    # KPI Section
    st.subheader("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Rides", len(df_filtered))
    
    if 'Fare' in df_filtered.columns:
        col2.metric("Total Revenue", f"₹{df_filtered['Fare'].sum():,.0f}")
        col3.metric("Average Fare", f"₹{df_filtered['Fare'].mean():.2f}")
    else:
        col2.metric("Total Revenue", "N/A")
        col3.metric("Average Fare", "N/A")
    
    if 'Customer_Rating' in df_filtered.columns:
        col4.metric("Average Rating", f"{df_filtered['Customer_Rating'].mean():.2f}")
    else:
        col4.metric("Average Rating", "N/A")
    
    st.divider()
    
    # Ride Status Chart
    st.subheader("Ride Status Distribution")
    
    if 'Booking_Status' in df_filtered.columns:
        status_chart = px.pie(
            df_filtered,
            names="Booking_Status",
            title="Ride Status"
        )
        st.plotly_chart(status_chart, use_container_width=True)
    
    # Vehicle Type Usage
    st.subheader("Vehicle Type Usage")
    
    vehicle_chart = px.bar(
        df_filtered.groupby("Vehicle_Type").size().reset_index(name="Rides"),
        x="Vehicle_Type",
        y="Rides",
        color="Vehicle_Type"
    )
    st.plotly_chart(vehicle_chart, use_container_width=True)

# TAB 2: Power BI
with tab2:
    st.header("📈 Power BI Dashboard")
    
    pbix_file = "OLA Ride Power BI Dashboard.pbix"
    pbix_image = "OLA_POWER_BI-ANSWERS.png"
    
    if Path(pbix_image).exists():
        st.subheader("Power BI Dashboard Preview")
        st.image(pbix_image, use_column_width=True)
        st.success("✅ Power BI Dashboard displayed above")
    else:
        st.warning("⚠️ Power BI image not found")
    
    if Path(pbix_file).exists():
        st.info("📥 Download Power BI File")
        with open(pbix_file, "rb") as file:
            st.download_button(
                label="📥 Download Power BI File (.pbix)",
                data=file,
                file_name=pbix_file,
                mime="application/octet-stream"
            )
    else:
        st.warning("⚠️ Power BI file not found")

# TAB 3: SQL Queries
with tab3:
    st.header("🗄️ SQL Queries & Results")
    
    sql_file = "OLA_Ride_SQL queries.sql"
    
    if Path(sql_file).exists():
        with open(sql_file, "r") as file:
            sql_content = file.read()
        
        st.subheader("SQL Query Code")
        st.code(sql_content, language="sql")
    else:
        st.warning("⚠️ SQL queries file not found")
    
    # Display SQL results image
    sql_answers_image = "OLA_SQL-ANSWERS.png"
    if Path(sql_answers_image).exists():
        st.subheader("SQL Query Results")
        st.image(sql_answers_image, use_column_width=True)
        st.success("✅ SQL query results displayed above")
    else:
        st.warning("⚠️ SQL results image not found")

# TAB 4: Raw Data
with tab4:
    st.header("📋 Raw Data - OLA_Ride_Data_Sheet.csv")
    
    st.subheader("📊 Data Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("File Size", f"{len(df) * len(df.columns)} cells")
    
    st.subheader("📈 Column Information")
    st.write(df.dtypes)
    
    st.subheader("🔍 Data Preview")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("📥 Download Options")
    
    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="OLA_Ride_Data.csv",
        mime="text/csv"
    )
    
    # Download Excel
    try:
        import openpyxl
        excel_file = df.to_excel(index=False)
        st.download_button(
            label="📥 Download as Excel",
            data=excel_file,
            file_name="OLA_Ride_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ImportError:
        st.info("Excel export requires openpyxl library")

# TAB 5: Images & Files
with tab5:
    st.header("📸 Images & Files from Repository")
    
    st.subheader("Available Files")
    
    # Power BI Questions
    if Path("OLA_QUESTIONS.png").exists():
        st.subheader("📋 OLA Questions")
        st.image("OLA_QUESTIONS.png", use_column_width=True)
    
    # Power BI Answers
    if Path("OLA_POWER_BI-ANSWERS.png").exists():
        st.subheader("📊 Power BI Answers")
        st.image("OLA_POWER_BI-ANSWERS.png", use_column_width=True)
    
    # SQL Questions
    if Path("OLA_SQL-ANSWERS.png").exists():
        st.subheader("🗄️ SQL Answers")
        st.image("OLA_SQL-ANSWERS.png", use_column_width=True)
    
    # List all files in repo
    st.subheader("📁 All Repository Files")
    repo_files = list(Path(".").glob("*"))
    for file in repo_files:
        if file.is_file():
            st.write(f"✅ {file.name}")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info("""
## 📚 About This Dashboard
This dashboard displays:
- 📊 Interactive charts & KPIs
- 📈 Power BI visualizations
- 🗄️ SQL queries & results
- 📋 Raw data export
- 📸 Repository images
""")
