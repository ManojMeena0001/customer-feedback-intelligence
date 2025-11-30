import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.nlp_models.sentiment import get_sentiment

samples = [
    "Delivery was late and food was cold.",
    "Amazing service! Loved the pizza.",
    "Packaging was okay, nothing special."
]

for s in samples:
    label, score = get_sentiment(s)
    print(f"TEXT: {s}")
    print(f"Sentiment: {label} (confidence {score:.2f})")
    print("--------------------------------")
