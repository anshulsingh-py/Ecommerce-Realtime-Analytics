import streamlit as st
import pandas as pd
import redis

# Connect to Redis
redis_host = '174.129.175.196'  # Use 'localhost' or the IP address of your Redis server
redis_port = 6379              # Default Redis port
redis_password = 'Anshul@18414'

import streamlit as st
import pandas as pd
import redis

# Connect to Redis
redis_client = redis.StrictRedis(host=redis_host, port=6379, password=redis_password, decode_responses=True)

def fetch_data_from_redis():
    keys = redis_client.keys("product:*")
    data = []
    for key in keys:
        product_data = redis_client.hgetall(key)
        data.append(product_data)
    return pd.DataFrame(data)

st.title("Real-Time E-Commerce Dashboard")

# Fetch data from Redis
data = fetch_data_from_redis()

if not data.empty:
    st.write("## Top Products by Revenue")
    st.bar_chart(data.set_index("product_id")["total_revenue"].astype(float))
else:
    st.write("No data available yet.")