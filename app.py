import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page Config
st.set_page_config(page_title="OLA Ride Insights", layout="wide")

st.title("🚕 OLA Ride Insights Dashboard")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Power BI", "🗄️ SQL Queries", "📋 Raw Data"])

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
    
    # Revenue by Pickup Location
    st.subheader("Revenue by Pickup Location")
    
    if 'Fare' in df_filtered.columns:
        location_chart = px.bar(
            df_filtered.groupby("Pickup_Location")["Fare"].sum().reset_index(),
            x="Pickup_Location",
            y="Fare",
            color="Pickup_Location"
        )
        st.plotly_chart(location_chart, use_container_width=True)
    
    # Ride Trends
    st.subheader("Ride Trend")
    
    if 'Date' in df_filtered.columns:
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy["Date"] = pd.to_datetime(df_filtered_copy["Date"])
        trend = df_filtered_copy.groupby("Date").size().reset_index(name="Rides")
        
        trend_chart = px.line(
            trend,
            x="Date",
            y="Rides",
            markers=True
        )
        st.plotly_chart(trend_chart, use_container_width=True)

# TAB 2: Power BI
with tab2:
    st.header("📈 Power BI Dashboard")
    
    # Check if Power BI file exists
    pbix_file = "OLA Ride Power BI Dashboard.pbix"
    
    if Path(pbix_file).exists():
        st.info("Power BI Dashboard File Available")
        st.write(f"**File:** {pbix_file}")
        st.write("Note: To view the Power BI dashboard, download and open the .pbix file in Power BI Desktop")
        
        # Display Power BI image if available
        pbix_image = "OLA_POWER_BI-ANSWERS.png"
        if Path(pbix_image).exists():
            st.subheader("Power BI Dashboard Preview")
            st.image(pbix_image, use_column_width=True)
        
        # Provide download link
        try:
            with open(pbix_file, "rb") as file:
                st.download_button(
                    label="📥 Download Power BI File",
                    data=file,
                    file_name=pbix_file,
                    mime="application/octet-stream"
                )
        except FileNotFoundError:
            st.warning("Power BI file exists but cannot be read")
    else:
        st.warning("Power BI file not found in the repository")

# TAB 3: SQL Queries
with tab3:
    st.header("🗄️ SQL Queries")
    
    sql_file = "OLA_Ride_SQL queries.sql"
    
    if Path(sql_file).exists():
        try:
            with open(sql_file, "r") as file:
                sql_content = file.read()
            
            st.subheader("SQL Queries")
            st.code(sql_content, language="sql")
        except Exception as e:
            st.error(f"Error reading SQL file: {e}")
        
        # Display SQL answers image if available
        sql_answers_image = "OLA_SQL-ANSWERS.png"
        if Path(sql_answers_image).exists():
            st.subheader("SQL Query Results")
            st.image(sql_answers_image, use_column_width=True)
    else:
        st.warning("SQL queries file not found in the repository")

# TAB 4: Raw Data
with tab4:
    st.header("📋 Raw Data")
    
    st.subheader("Data Preview")
    st.dataframe(df)
    
    st.subheader("Data Summary")
    st.write(f"Total Records: {len(df)}")
    st.write(f"Total Columns: {len(df.columns)}")
    st.write(f"Columns: {', '.join(df.columns.tolist())}")
    
    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="OLA_Ride_Data.csv",
        mime="text/csv"
    )
