import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page Config
st.set_page_config(page_title="OLA Ride Insights", layout="wide")

st.title("🚕 OLA Ride Insights Dashboard")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Power BI Visuals", "🗄️ SQL Queries", "📋 Raw Data"])

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

# TAB 2: Power BI Visuals
with tab2:
    st.header("📈 Power BI Style Visualizations")
    
    st.subheader("1. Rides by Booking Status")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Booking_Status' in df.columns:
            booking_status_data = df['Booking_Status'].value_counts().reset_index()
            booking_status_data.columns = ['Status', 'Count']
            fig_status = px.bar(
                booking_status_data,
                x='Status',
                y='Count',
                color='Status',
                title='Total Rides by Status',
                labels={'Count': 'Number of Rides'},
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        if 'Customer_Rating' in df.columns:
            rating_dist = df['Customer_Rating'].value_counts().sort_index().reset_index()
            rating_dist.columns = ['Rating', 'Count']
            fig_rating = px.bar(
                rating_dist,
                x='Rating',
                y='Count',
                title='Customer Rating Distribution',
                labels={'Count': 'Number of Rides'},
                color='Rating',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_rating, use_container_width=True)
    
    st.subheader("2. Top Pickup Locations")
    col3, col4 = st.columns(2)
    
    with col3:
        if 'Pickup_Location' in df.columns:
            top_pickup = df['Pickup_Location'].value_counts().head(10).reset_index()
            top_pickup.columns = ['Location', 'Rides']
            fig_pickup = px.barh(
                top_pickup,
                x='Rides',
                y='Location',
                title='Top 10 Pickup Locations',
                labels={'Rides': 'Number of Rides'},
                color='Rides',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_pickup, use_container_width=True)
    
    with col4:
        if 'Vehicle_Type' in df.columns:
            vehicle_dist = df['Vehicle_Type'].value_counts().reset_index()
            vehicle_dist.columns = ['Vehicle', 'Count']
            fig_vehicle = px.pie(
                vehicle_dist,
                values='Count',
                names='Vehicle',
                title='Vehicle Type Distribution'
            )
            st.plotly_chart(fig_vehicle, use_container_width=True)
    
    st.subheader("3. Revenue Analysis")
    col5, col6 = st.columns(2)
    
    with col5:
        if 'Fare' in df.columns and 'Vehicle_Type' in df.columns:
            revenue_by_vehicle = df.groupby('Vehicle_Type')['Fare'].sum().reset_index().sort_values('Fare', ascending=False)
            revenue_by_vehicle.columns = ['Vehicle', 'Revenue']
            fig_revenue = px.bar(
                revenue_by_vehicle,
                x='Vehicle',
                y='Revenue',
                title='Total Revenue by Vehicle Type',
                labels={'Revenue': 'Revenue (₹)'},
                color='Revenue',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col6:
        if 'Fare' in df.columns and 'Pickup_Location' in df.columns:
            top_revenue_locations = df.groupby('Pickup_Location')['Fare'].sum().nlargest(10).reset_index()
            top_revenue_locations.columns = ['Location', 'Revenue']
            fig_loc_revenue = px.barh(
                top_revenue_locations,
                x='Revenue',
                y='Location',
                title='Top 10 Revenue Locations',
                labels={'Revenue': 'Revenue (₹)'},
                color='Revenue',
                color_continuous_scale='Blues_r'
            )
            st.plotly_chart(fig_loc_revenue, use_container_width=True)
    
    st.subheader("4. Time Series Analysis")
    if 'Date' in df.columns:
        df_copy = df.copy()
        df_copy['Date'] = pd.to_datetime(df_copy['Date'])
        
        # Daily rides trend
        daily_rides = df_copy.groupby('Date').size().reset_index(name='Rides')
        fig_daily = px.line(
            daily_rides,
            x='Date',
            y='Rides',
            title='Daily Rides Trend',
            labels={'Rides': 'Number of Rides'},
            markers=True
        )
        st.plotly_chart(fig_daily, use_container_width=True)
    
    st.subheader("5. Heatmap: Pickup Location vs Vehicle Type")
    if 'Pickup_Location' in df.columns and 'Vehicle_Type' in df.columns:
        heatmap_data = pd.crosstab(df['Pickup_Location'], df['Vehicle_Type'])
        fig_heatmap = px.imshow(
            heatmap_data,
            labels=dict(x='Vehicle Type', y='Pickup Location', color='Rides'),
            title='Pickup Location vs Vehicle Type Heatmap',
            color_continuous_scale='YlOrRd'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

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
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="OLA_Ride_Data.csv",
        mime="text/csv"
    )
