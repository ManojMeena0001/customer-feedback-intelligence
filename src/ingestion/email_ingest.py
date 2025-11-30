# email_ingest.py
import os
import pandas as pd

RAW = "data/raw"
PROCESSED = "data/processed"

def ingest_emails(filename="emails.csv"):
    path = os.path.join(RAW, filename)
    df = pd.read_csv(path)

    # Normalize to our schema
    df_processed = pd.DataFrame()
    df_processed["review_id"] = df.get("message_id", pd.Series(range(len(df))))
    df_processed["source"] = "email"
    df_processed["text"] = df.get("body", df.get("message", "")).astype(str)
    df_processed["timestamp"] = df.get("timestamp", None)
    df_processed["sender"] = df.get("from", None)

    os.makedirs(PROCESSED, exist_ok=True)
    out = os.path.join(PROCESSED, "emails_processed.csv")
    df_processed.to_csv(out, index=False)
    print("Saved:", out)
    return df_processed

if __name__ == "__main__":
    ingest_emails()
