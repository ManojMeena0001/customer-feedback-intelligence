# google_reviews.py
import os
import pandas as pd


# Paths (adjust if your folders are different)
RAW = "data/raw"
PROCESSED = "data/processed"

def ingest_google_reviews(filename="google_reviews.csv"):
    """
    Reads Google reviews CSV and writes a processed CSV with columns:
    ['review_id', 'source', 'text', 'rating', 'timestamp', 'branch']
    """
    path = os.path.join(RAW, filename)
    df = pd.read_csv(path)                    # read raw CSV into a table (DataFrame)

    # Ensure we have the expected columns; if names differ, adapt here
    # Normalize columns to our standard schema
    df_processed = pd.DataFrame()
    df_processed["review_id"] = df.get("review_id", pd.Series(range(len(df))))
    df_processed["source"] = "google"
    df_processed["text"] = df["review_text"].astype(str)   # ensure text
    df_processed["rating"] = df.get("rating", None)
    df_processed["timestamp"] = df.get("timestamp", None)
    df_processed["branch"] = df.get("branch", "unknown")

    # Save processed file
    os.makedirs(PROCESSED, exist_ok=True)
    out_path = os.path.join(PROCESSED, "google_reviews_processed.csv")
    df_processed.to_csv(out_path, index=False)
    print("Saved:", out_path)
    return df_processed

if __name__ == "__main__":
    ingest_google_reviews()
