import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Reddit Sentiment Dashboard",
    layout="wide",
)

st.title("🧠 Real-Time Reddit Sentiment Dashboard")

# --- Sidebar Controls ---
st.sidebar.title("🔧 Dashboard Controls")

data_source = st.sidebar.radio(
    "Select Data Type:",
    ["Posts", "Comments"],
    index=0
)

selected_subreddit = st.sidebar.selectbox(
    "Filter by Subreddit:",
    ["All", "r/gaming", "r/news", "r/Showerthoughts"]
)


# Create Tabs
tabs = st.tabs(["📊 Sentiment Distribution", "☁️ Wordclouds", "📈 BERT Classifier Performance", "🤖 MLP Performance", "🛠️ Classic ML Model Performance", "🔮 Real-Time Predictor"])

# ---- TAB 1: Sentiment Distribution ----
with tabs[0]:
    st.header("Sentiment Distribution")
    st.write("Distribution of sentiment across collected Reddit posts and comments.")

    if data_source == 'Posts':

        dist_img = Image.open("figures/overall_post_sentiment_distribution.png")
        st.image(dist_img, caption="Sentiment Distribution in Posts", use_container_width=True)

        dist_img = Image.open("figures/subreddit_post_sentiment_distribution.png")
        st.image(dist_img, caption="Posts Sentiment Distribution by Subreddit", use_container_width=True)

    if data_source == 'Comments':

        dist_img = Image.open("figures/overall_comment_sentiment_distribution.png")
        st.image(dist_img, caption="Sentiment Distribution in Comments", use_container_width=True)

        dist_img = Image.open("figures/subreddit_comment_sentiment_distribution.png")
        st.image(dist_img, caption="Comments Sentiment Distribution by Subreddit", use_container_width=True)

    dist_img = Image.open("figures/top_words_contributing_to_sentiment.png")
    st.image(dist_img, caption="Top Words Contributing to Sentiment", use_container_width=True)

# ---- TAB 2: Wordclouds ----
with tabs[1]:
    st.header("Wordclouds")
    st.write("Most frequent words by sentiment class and subreddit.")

    if data_source == 'Comments':
        if selected_subreddit == 'All':

            st.subheader("Overall Positive")
            wc_pos = Image.open("figures/overall_positive_comments_wordcloud.png")
            st.image(wc_pos, use_container_width=True)
        
            st.subheader("Overall Negative")
            wc_neg = Image.open("figures/overall_negative_comments_wordcloud.png")
            st.image(wc_neg, use_container_width=True)

        elif selected_subreddit == 'r/gaming':
            st.subheader("Positive - r/gaming")
            wc_gaming_pos = Image.open("figures/gaming_positive_comments_wordcloud.png")
            st.image(wc_gaming_pos, use_container_width=True)

            st.subheader("Negative - r/gaming")
            wc_gaming_neg = Image.open("figures/gaming_negative_comments_wordcloud.png")
            st.image(wc_gaming_neg, use_container_width=True)

        elif selected_subreddit =='r/news':
            st.subheader("Positive - r/news")
            wc_news_neg = Image.open("figures/news_positive_comments_wordcloud.png")
            st.image(wc_news_neg, use_container_width=True)

            st.subheader("Negative - r/news")
            wc_news_neg = Image.open("figures/news_negative_comments_wordcloud.png")
            st.image(wc_news_neg, use_container_width=True)

        elif selected_subreddit == 'r/Showerthoughts':
            st.subheader("Positive - r/Showerthoughts")
            wc_showerthoughts_pos = Image.open("figures/showerthoughts_positive_comments_wordcloud.png")
            st.image(wc_showerthoughts_pos, use_container_width=True)

            st.subheader("Negative - r/Showerthoughts")
            wc_showerthoughts_neg = Image.open("figures/showerthoughts_negative_comments_wordcloud.png")
            st.image(wc_showerthoughts_neg, use_container_width=True)

    else:
        st.info('Wordclouds are currently only available for comments.')

# ---- TAB 3: BERT Classifier Performance ----
with tabs[2]:
    st.header("BERT Performance")
    st.write("Confusion Matrix and F1 Scores.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Confusion Matrix")
        st.image("figures/bert_confusion_matrix.png", use_container_width=True)

    with col2:
        st.subheader("F1 Scores")
        st.image("figures/bert_f1_scores_sentiment.png", use_container_width=True)

# ---- TAB 4: MLP Performance ----
with tabs[3]:
    st.header("Custom MLP Performance")
    st.write("Model accuracy, loss, confusion matrix, and F1 scores.")

    st.subheader("MLP Loss Curve")
    st.image("figures/mlp_loss_curve.png", use_container_width=True)

    st.subheader("Accuracy Over Time")
    st.image("figures/mlp_accuracy_plot.png", use_container_width=True)

    st.subheader("Confusion Matrix")
    st.image("figures/mlp_confusion_matrix.png", use_container_width=True)

    st.subheader("Class-wise F1 Scores")
    st.image("figures/mlp_class_f1_scores.png", use_container_width=True)

# ---- TAB 5: Classic ML Model Performance ----
with tabs[4]:
    st.header("Model Performance")
    st.write("Logistic Regression & Random Forest Confusion Matrix plots.")

    st.subheader("Logistic Regression Confusion Matrix")
    st.image("figures/logistic_regression_confusion_matrix.png", use_container_width=True)

    st.subheader("Random Forest Confusion Matrix")
    st.image("figures/random_forest_confusion_matrix.png", use_container_width=True)

# ---- TAB 6: Real-Time Predictor ----
with tabs[5]:
    from transformers import BertTokenizerFast, BertForSequenceClassification
    import torch

    # Load your fine-tuned BERT model
    @st.cache_resource
    def load_bert_model():
        model = BertForSequenceClassification.from_pretrained("../src/bert_classification_model")
        tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
        model.eval()
        return tokenizer, model

    tokenizer, model = load_bert_model()

    # Add UI
    st.header("🔮 Real-Time Reddit Sentiment Predictor")
    st.write("Enter any Reddit comment or post and get an instant sentiment prediction using the fine-tuned BERT model.")

    user_input = st.text_area("Enter your comment/post text here:")

    if st.button("Predict Sentiment"):
        if not user_input.strip():
            st.warning("Please enter some text to analyze.")
        else:
            inputs = tokenizer(
                user_input,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )

            with torch.no_grad():
                logits = model(**inputs).logits
                prediction = torch.argmax(logits, dim=1).item()

            label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
            st.success(f"Predicted Sentiment: **{label_map[prediction]}**")
