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
- **dbt** - transform and document data in the warehouse
- **AWS (S3, RDS, Lambda)** - cloud infrastructure and storage
    - **EC2** - cloud VM
- **Streamlit** - interactive web dashboard
- **Real-Time Pipeline** - simulate or build true stream (Kafka, Kinesis, or polling)
- **Python** - scripting and model logic
- **PostgreSQL** - store Reddit comments with sentiment labels for future querying, dashboards, or ML models
- **PRAW** -
- **psycopg2** - 
- *(Optional)* Kafka, or other real-time tools

---

## **High-level architecture** (WIP)
```text
[API Source]
    ↓
[Ingestion Script (Docker)]
    ↓
[AWS S3 or Kafka Topic]
    ↓
[Sentiment Analysis Script]
    ↓
[Structured Data Store (PostgreSQL, Redshift)]
    ↓
[dbt Transformations]
    ↓
[Streamlit Dashboard (Docker)]
```

## **Success Criteria**
- Collect and stream data from a public API
- Run a real-time or simulated ingestion process
- Apply a basic sentiment analysis model (e.g., VADER)
- Store raw + processed data in AWS (S3 and/or RDS)
- Use dbt to transform and clean sentiment data
- Build and deploy an interactive Streamlit dashboard
- Deploy entire stack using Docker and AWS (ECS/EC2 or Lambda)

## **Stretch Goals**
- Stream with Kafka or Kinesis instead of polling
- Train and deploy your own sentiment classifier
- Deploy model using AWS Lambda + API Gateway
- Add logging, error tracking, or retry logic


### **Potential Additions to Project:**
- Live Deployment URL (when Streamlit dashboard is deployed)
- Screenshots or GIFs of the dashboard
- Setup Instructions (for running locally or in Docker)
- Credits or Inspiration (if you forked ideas or used external resources)