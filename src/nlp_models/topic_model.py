from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
import pandas as pd

from src.preprocessing.cleaner import clean_text_basic


def generate_topics(
        input_csv="data/processed/google_reviews_processed.csv",
        output_csv="data/processed/google_reviews_with_topics.csv"):

    # 1. Load Data
    df = pd.read_csv(input_csv)
    df["clean_text"] = df["text"].apply(clean_text_basic)

    # 2. Embeddings
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(df["clean_text"].tolist(), show_progress_bar=True)

    # 3. Better UMAP for small datasets
    umap_model = UMAP(
        n_neighbors=4,
        n_components=5,
        min_dist=0.0,
        metric="cosine"
    )

    # 4. BERTopic with easier clustering
    topic_model = BERTopic(
        umap_model=umap_model,
        min_topic_size=2,      # very important
        verbose=True,
        low_memory=True
    )

    # 5. Fit
    topics, _ = topic_model.fit_transform(df["clean_text"], embeddings)

    # 6. Save
    df["topic"] = topics
    df.to_csv(output_csv, index=False)

    print(f"[+] Saved topics to: {output_csv}")
    print("[+] Unique topics:", df["topic"].unique())

    return topic_model, df
