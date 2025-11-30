from transformers import pipeline
from src.preprocessing.cleaner import clean_text_basic

# Load HuggingFace pre-trained model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def get_sentiment(text):
    """
    Returns (label, score) for the input text.
    Example: ("NEGATIVE", 0.97)
    """
    # Clean text lightly for BERT
    clean = clean_text_basic(text)

    # Run through model
    result = sentiment_pipeline(clean[:512])[0]

    # Extract predicted label & confidence score
    label = result["label"]
    score = float(result["score"])

    return label, score
