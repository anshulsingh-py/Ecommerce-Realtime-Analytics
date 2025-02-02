import streamlit as st
import pandas as pd
import redis
import json
import time
REDIS_HOST = "54.243.237.120"
REDIS_PORT = "6379"
REDIS_PASS = "Test@1234"

# Connect to Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)

# Function to fetch all product IDs from Redis
def get_all_products():
    keys = redis_client.keys("product:*")
    product_ids = [key.split(":")[1] for key in keys]
    return sorted(product_ids)

# Function to fetch data for a selected product
def fetch_product_data(product_id):
    key = f"product:{product_id}"
    raw_data = redis_client.lrange(key, 0, -1)

    if not raw_data:
        return pd.DataFrame(columns=["timestamp", "price"])  # Return empty DataFrame if no data

    parsed_data = [json.loads(item) for item in raw_data]
    df = pd.DataFrame(parsed_data)
    df = df.rename(columns={'window_end': 'timestamp', 'total_revenue': 'price'})


    # Convert timestamp to datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort data by timestamp
    return df.sort_values("timestamp")

# Streamlit UI
st.set_page_config(page_title="Real-Time Price Trends", layout="wide")
st.title("📈 Real-Time Product Price Trend")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
refresh_interval = st.sidebar.slider("Auto-refresh Interval (seconds)", 5, 60, 10)
date_range = st.sidebar.date_input("Select Date Range", [])

# Dropdown to select a product
product_ids = get_all_products()
if not product_ids:
    st.warning("No products found in Redis. Waiting for data...")
    time.sleep(refresh_interval)
    st.experimental_rerun()

selected_product = st.sidebar.selectbox("Select a product:", product_ids)

# Fetch data for the selected product
df = fetch_product_data(selected_product)

# Filter by date range if selected
if not df.empty and date_range:
    df = df[(df["timestamp"].dt.date >= date_range[0]) & (df["timestamp"].dt.date <= date_range[-1])]

# Display the line chart
if not df.empty:
    st.write(f"### 📊 Price Trend for Product `{selected_product}`")
    st.line_chart(df.set_index("timestamp"))

    # Show last price point
    st.write(f"**Latest Price:** ${df['price'].iloc[-1]:.2f} at {df['timestamp'].iloc[-1]}")
else:
    st.warning("No data available for the selected product and date range.")

# Auto-refresh mechanism
st.sidebar.write(f"🔄 Auto-refreshing every **{refresh_interval}** seconds...")
time.sleep(refresh_interval)
# st.experimental_rerun()
