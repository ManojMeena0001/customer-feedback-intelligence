import pandas as pd
import os

RAW = "data/raw"
PROCESSED = "data/processed"

def ingest_app_feedback(filename="app_feedback.csv"):
    """
    Reads app feedback CSV and converts it into a consistent format:
    ['review_id', 'source', 'text', 'rating', 'timestamp', 'platform']
    """

    path = os.path.join(RAW, filename)

    # 1. Load the raw CSV file into a DataFrame (table in memory)
    df = pd.read_csv(path)

    # 2. Create a new DataFrame with standardized column names
    df_processed = pd.DataFrame()

    df_processed["review_id"] = df.get("feedback_id", df.index)
    df_processed["source"] = "app"
    df_processed["text"] = df.get("comment", df.get("text", "")).astype(str)
    df_processed["rating"] = df.get("rating", None)
    df_processed["timestamp"] = df.get("timestamp", None)
    df_processed["platform"] = df.get("platform", "unknown")

    # 3. Save processed file
    os.makedirs(PROCESSED, exist_ok=True)
    out_path = os.path.join(PROCESSED, "app_feedback_processed.csv")
    df_processed.to_csv(out_path, index=False)

    print("Saved:", out_path)
    return df_processed

if __name__ == "__main__":
    ingest_app_feedback()