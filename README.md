# **Real-Time Sentiment Analysis Dashboard (with Custom Neural Network Classifier)**

## 🧠 **Project Overview**
This project is an end-to-end **real-time sentiment analysis pipeline** that ingests Reddit data, stores structured insights in PostgreSQL, applies deep learning classification, and visualizes everything on a responsive **Streamlit dashboard**.

What started with rule-based VADER analysis evolved into a **custom-trained MLP classifier**, built using PyTorch and powered by an autoencoder for feature compression.

---

## 🎯 **Objectives**
- Ingest real-time or simulated Reddit comments/posts using PRAW
- Preprocess and store incoming text data in PostgreSQL and AWS S3
- Apply sentiment classification via:
    - VADER (baseline)
    - **MLP Neural Network** (trained on labeled Reddit data)
- Build a Streamlit dashboard to visualize sentiment trends
- Deploy all components using Docker
- Deploy pipeline and dashboard to AWS (EC2, S3)

---

## 📊 **Data Collection & Motivation**
Reddit comments were collected in real-time during a culturally and socially active week to ensure sentiment diversity and class balance. I selected three subreddits based on topical relevance and emotional tone:

- **r/gaming**  
  Selected during the **Summer Games Fest**, a time when Reddit users actively discuss trailers, announcements, and reactions. This provided a rich source of **passionate, hype-driven, and sometimes critical** sentiment around game content.

- **r/news**  
  Captured during a week of high-profile events, including **protests in Los Angeles against ICE** and a viral **social media dispute between Donald Trump and Elon Musk**. This subreddit helped supply **polarizing or intense** sentiment data relevant to current events.

- **r/Showerthoughts**  
  Chosen to inject **balance** into the dataset by including a subreddit known for **lighthearted, introspective, or neutral-toned** content. This helped prevent skew toward overly negative sentiment from the other subreddits.

Together, these sources offered a **broad emotional range**—ideal for training a **multiclass sentiment classifier**.

---

## 🛠️ **Tools and Technologies**

| Category           | Tools                             |
| ------------------ | --------------------------------- |
| **Data Ingestion** | PRAW, Python                      |
| **Processing**     | Pandas, Scikit-learn, TF-IDF      |
| **Modeling**       | PyTorch (MLP, Autoencoder), VADER |
| **Visualization**  | Streamlit                         |
| **Storage**        | PostgreSQL, AWS S3                |
| **Deployment**     | Docker, AWS EC2 / S3              |

---

## 🤖 **Deep Learning Classifier**
A PyTorch-based **multiclass sentiment classifier** was trained on labeled Reddit comments using:
- **TF-IDF** vectorization with `max_features=1000`
- **Autoencoder** for dimensionality reduction
- **MLP classifier** with 3 hidden layers + dropout
- **Weighted cross-entropy loss** for class imbalance
- Tracked training loss, accuracy, and class-wise F1-scores over 75 epochs

Final Model Performance:
| Class        | F1-Score |
| ------------ | -------- |
| Negative     | 0.62     |
| Neutral      | 0.70     |
| Positive     | 0.70     |
| **Accuracy** | **67%**  |

---

## 🗺️ **Architecture Overview**
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

## 🚀 **Core Features**
- Live Reddit ingestion
- Real-time sentiment labeling (comments and posts)
- Custom neural network with TF-IDF + autoencoder
- Saved and reusable model weights + training curves
- Interactive visualizations and dashboards

---

## 🌱 **Stretch Goals**
- Deploy model via AWS Lambda + API Gateway
- Real-time stream processing with Kafka or Kinesis
- Add live model inference into ingestion pipeline
- Deploy dashboard publicly and share demo URL
- Transform and document data using dbt

---

## 📈 **Data Visualizations**

### MLP Loss Over Time
![MLP Loss Curve](figures/mlp_loss_curve.png)

### Accuracy Over Time Plot
![MLP Accuracy Over Time](figures/mlp_accuracy_plot.png)

### Confusion Matrix Heatmap
![Confusion Matrix](figures/mlp_confusion_matrix.png)

### Class-wise F1 Scores
![Class-wise F1 Scores](figures/mlp_class_f1_scores.png)


## ✅ **Final Steps**
- Finish work on Streamlit Dashboard
- Add link to Streamlit Dashboard to README.md
