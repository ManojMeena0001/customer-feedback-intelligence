# whatsapp.py
import os
import re
import pandas as pd
from datetime import datetime

RAW = "data/raw"
PROCESSED = "data/processed"

# Regex matches lines like: 28/11/2025, 19:23 - Sender: message
LINE_RE = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s-\s([^:]+):\s(.*)")

def parse_whatsapp_file(filename="whatsapp_export.txt"):
    path = os.path.join(RAW, filename)
    messages = []
    last = None

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            m = LINE_RE.match(line)
            if m:
                date_part = m.group(1)
                time_part = m.group(2)
                sender = m.group(3).strip()
                text = m.group(4).strip()
                # Try parsing timestamp; keep raw if fail
                timestamp = None
                for fmt in ("%d/%m/%Y %H:%M", "%m/%d/%Y %H:%M"):
                    try:
                        timestamp = datetime.strptime(f"{date_part} {time_part}", fmt)
                        break
                    except:
                        timestamp = f"{date_part} {time_part}"
                messages.append({"timestamp": timestamp, "sender": sender, "text": text})
                last = messages[-1]
            else:
                # continuation of previous line
                if last is not None:
                    last["text"] += " " + line.strip()
                else:
                    # orphaned line, skip or store
                    pass

    df = pd.DataFrame(messages)
    # Standardize columns for downstream steps
    df["source"] = "whatsapp"
    os.makedirs(PROCESSED, exist_ok=True)
    out = os.path.join(PROCESSED, "whatsapp_processed.csv")
    df.to_csv(out, index=False)
    print("Saved:", out)
    return df

if __name__ == "__main__":
    parse_whatsapp_file()
