# **Real-Time Sentiment Analysis Dashboard (with Custom Neural Network Classifier)**

## **Project Overview**
This project is an end-to-end **real-time sentiment analysis pipeline** that ingests Reddit data, stores structured insights in PostgreSQL, applies deep learning classification, and visualizes everything on a responsive **Streamlit dashboard**.

What started with rule-based VADER analysis evolved into a **custom-trained MLP classifier**, built using PyTorch and powered by an autoencoder for feature compression.

---

## **Objectives**
- Ingest real-time or simulated Reddit comments/posts using PRAW
- Preprocess and store incoming text data in PostgreSQL and AWS S3
- Apply sentiment classification via:
    - VADER (baseline)
    - **MLP Neural Network** (trained on labeled Reddit data)
- Build a Streamlit dashboard to visualize sentiment trends
- Deploy all components using Docker
- Deploy pipeline and dashboard to AWS (EC2, S3)

---

## **Tools and Technologies**

| Category           | Tools                             |
| ------------------ | --------------------------------- |
| **Data Ingestion** | PRAW, Python                      |
| **Processing**     | Pandas, Scikit-learn, TF-IDF      |
| **Modeling**       | PyTorch (MLP, Autoencoder), VADER |
| **Visualization**  | Streamlit                         |
| **Storage**        | PostgreSQL, AWS S3                |
| **Deployment**     | Docker, AWS EC2 / S3              |

---

## **Deep Learning Classifier**
A PyTorch-based **multiclass sentiment classifier** was trained on labeled Reddit comments using:
- **TF-IDF** vectorization with `max_features=1000`
- **Autoencoder** for dimensionality reduction
- **MLP classifier** with 3 hidden layers + dropout
- **Weighted cross-entropy loss** for class imbalance
- Tracked training metrics and F1-scores across 75 epochs

Final Model Performance:
| Class        | F1-Score |
| ------------ | -------- |
| Negative     | 0.62     |
| Neutral      | 0.70     |
| Positive     | 0.70     |
| **Accuracy** | **67%**  |

---

## **Architecture Overview**
```text
[Reddit API]
    ↓
[PRAW Ingestion Script (Docker)]
    ↓
[Structured Data Store (PostgreSQL) in EC2 cloud instance]
    ↓
[AWS S3]
    ↓
[Sentiment Analysis Classifier (VADER + MLP)]
    ↓
[Streamlit Dashboard (Docker)]
```

---

## **Core Features***
- Live Reddit ingestion
- Real-time sentiment labeling (comments and posts)
- Custom neural network with TF-IDF + autoencoder
- Saved and reusable model weights + training curves
- Interactive visualizations and dashboards

---

## **Stretch Goals**
- Deploy model via AWS Lambda + API Gateway
- Real-time stream processing with Kafka or Kinesis
- Add live model inference into ingestion pipeline
- Deploy dashboard publicly and share demo URL
- Transform and document data using dbt

---

## Data Visualizations

### MLP Loss Over Time
![MLP Loss Curve](figures/mlp_loss_curve.png)

### Accuracy Over Time Plot
![MLP Accuracy Over Time](figures/mlp_accuracy_plot.png)

### Confusion Matrix Heatmap
![Confusion Matrix](figures/mlp_confusion_matrix.png)

### Class-wise F1 Scores
![Class-wise F1 Scores](figures/mlp_class_f1_scores.png)


## Final Steps
- Finish work on Streamlit Dashboard
- Add link to Sreamlit Dashboard to README.md
