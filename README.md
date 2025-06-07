# **Cloud Computing Project: Real-Time Sentiment Analysis Dashboard**

## **Project Goal**
Build an end-to-end **real-time sentiment analysis system** that:
- Ingests live text data from a public API (e.g., Twitter or Reddit)
- Applies sentiment analysis using a lightweight model
- Transforms and stores the data
- Visualizes insights on a responsive **Streamlit dashboard**
- Is fully containerized and deployed to **AWS**

---

## **Tools and Technologies**
- **Docker** - containerize all components
- **AWS (RDS)** - cloud infrastructure and storage
    - **EC2** - cloud VM
    - **S3** - storing stream data periodically
- **Python** - scripting and model logic
- **PostgreSQL** - store real-time data for future querying, dashboards, and ML models
    - **psycopg2** - PostgreSQL adapter for Python language
- **Python Reddit API Wrapper (PRAW)** - scrapes data from subreddits
- **VADER** - A lexicon + rule-based sentiment analysis tool
- **dbt** - transform and document data in the warehouse
- **Streamlit** - interactive web dashboard
- **Real-Time Pipeline** - simulate or build true stream (Kafka, Kinesis, or polling)
- *(Optional)* Kafka, or other real-time tools

---

## **High-level architecture**
```text
[API Source]
    ↓
[Ingestion Script (Docker)]
    ↓
[Transfer raw data to AWS S3]
    ↓
[Sentiment Analysis Script]
    ↓
[Structured Data Store (PostgreSQL)]
    ↓
[dbt Transformations]
    ↓
[Streamlit Dashboard (Docker)]
```

## **Success Criteria**
- Collect and stream data from a public API
- Run a real-time or simulated ingestion process
- Store raw + processed data in AWS (S3 and/or RDS)
- Apply a basic sentiment analysis model (e.g., VADER)
- Use dbt to transform and clean sentiment data
- Build and deploy an interactive Streamlit dashboard
- Deploy entire stack using Docker and AWS (ECS/EC2 or Lambda)

## **Stretch Goals**
- Stream with Kafka or Kinesis instead of polling
- Train and deploy my own sentiment classifier
- Deploy model using AWS Lambda + API Gateway
- Add logging, error tracking, or retry logic


### **Potential Additions to Project:**
- Create script to classify sentiment in real-time as data is ingested to PostgreSQL DB
    - Store sentiment result immediately in DB
- Create MLP neural network model to classify positive neutral negative sentiments in posts and comments
- Live Deployment URL (when Streamlit dashboard is deployed)
- Screenshots or GIFs of the dashboard
- Setup Instructions (for running locally or in Docker)