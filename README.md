# Real-Time eCommerce Analytics System 🚀

## 📌 Overview
This project demonstrates a **real-time eCommerce analytics pipeline** that processes user purchase events, aggregates revenue per product, and visualizes insights dynamically. Using **Apache Kafka, Spark Streaming, Redis, and Streamlit**, it enables businesses to track revenue trends in real time.

## 🏗️ Architecture
```
 User Events → Kafka (Streaming) → Spark Processing → Redis (Storage) → Streamlit (Visualization)
```

1. **Kafka**: Ingests real-time purchase events
2. **Spark Streaming**: Aggregates revenue per product
3. **Redis**: Stores the processed results for quick access
4. **Streamlit**: Provides a live dashboard for visualization

## 🛠️ Tech Stack
- **Apache Kafka** - Real-time event streaming
- **Apache Spark Streaming** - Data processing
- **Redis** - In-memory storage
- **Streamlit** - Interactive visualization
- **Docker** - Containerization

## 🚀 Getting Started
### Prerequisites
- Docker & Docker Compose installed
- Python 3.x

### Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ecommerce-real-time-analytics.git
   cd ecommerce-real-time-analytics
   ```
2. **Start the services using Docker**
   ```bash
   docker-compose up -d
   ```
3. **Run the Kafka Producer** (Simulates eCommerce transactions)
   ```bash
   python data-generation/generate.py
   ```
4. **Start Spark Streaming Job** (Processes and sends data to Redis)
   ```bash
   spark-submit spark-processing/streaming_job.py
   ```
5. **Launch the Streamlit Dashboard**
   ```bash
   streamlit run app.py
   ```

## 📊 Features
✔ Real-time streaming analytics with Kafka & Spark  
✔ Aggregation of revenue per product  
✔ Interactive visualization using Streamlit  
✔ Efficient storage with Redis  
✔ Scalable & containerized setup with Docker  

## 🚀 Future Enhancements
- **Track top-selling products**
- **Improve Redis storage using TTL or a time-series DB**
- **Deploy to AWS with MSK, Glue, and DynamoDB**



