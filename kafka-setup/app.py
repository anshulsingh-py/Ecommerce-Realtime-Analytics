import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Simple Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📈 Simple Streamlit Dashboard")

# Create sample data
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=100),
        'Sales': np.random.randint(100, 1000, 100),
        'Expenses': np.random.randint(50, 500, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
    })
    return data

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect(
    "Select Region:",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=[df['Date'].min(), df['Date'].max()]
)

# Filter data based on selections
filtered_df = df[
    (df['Region'].isin(selected_region)) &
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1]))
]

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Overview")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.metric(label="Total Sales", value=f"${filtered_df['Sales'].sum():,}")
    st.metric(label="Total Expenses", value=f"${filtered_df['Expenses'].sum():,}")

with col2:
    st.subheader("Sales Trend")
    fig = px.line(
        filtered_df,
        x='Date',
        y='Sales',
        title='Sales Over Time'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    fig2 = px.bar(
        region_sales,
        x='Region',
        y='Sales',
        color='Region',
        title='Regional Sales Distribution'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Add some text
st.markdown("### Key Observations:")
st.write("- Sales trends over time")
st.write("- Regional performance comparison")
st.write("- Total sales vs expenses")
