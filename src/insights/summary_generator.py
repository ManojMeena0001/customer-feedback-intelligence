import pandas as pd
from src.insights.root_cause import (
    compute_aspect_sentiment,
    compute_branch_aspect_matrix,
    compute_source_distribution
)


def generate_summary(input_csv="data/processed/all_feedback_final.csv"):
    """
    Generates a clean, readable summary of your customer feedback analytics.
    No LLM required — uses rule-based template logic.
    """

    df = pd.read_csv(input_csv)

    # Generate analytics
    aspect_table = compute_aspect_sentiment(df)
    branch_matrix = compute_branch_aspect_matrix(df)
    source_dist = compute_source_distribution(df)

    # Identify top issues
    top_aspects = aspect_table.sort_values("negative_rate", ascending=False)

    # Extract top 3 aspects by negative rate
    top_issue = top_aspects.index[0]
    second_issue = top_aspects.index[1] if len(top_aspects) > 1 else None
    third_issue = top_aspects.index[2] if len(top_aspects) > 2 else None

    # Worst-performing branch
    if not branch_matrix.empty:
        branch_neg_counts = branch_matrix.sum(axis=1)
        worst_branch = branch_neg_counts.idxmax()
        worst_branch_count = branch_neg_counts.max()
    else:
        worst_branch = "N/A"
        worst_branch_count = 0

    # Start summary text
    summary = f"""
📌 **Customer Feedback Summary**

### 🔥 Top Issues
1. **{top_issue}** — {aspect_table.loc[top_issue, 'negative_rate']:.1f}% negative
"""
    if second_issue:
        summary += f"2. **{second_issue}** — {aspect_table.loc[second_issue, 'negative_rate']:.1f}% negative\n"
    if third_issue:
        summary += f"3. **{third_issue}** — {aspect_table.loc[third_issue, 'negative_rate']:.1f}% negative\n"

    summary += f"""
---

### 🏪 Branch Performance
- Worst-performing branch: **{worst_branch}**
- Negative reviews: **{worst_branch_count}**

"""

    summary += "### 📲 Source Distribution\n"
    for src, count in source_dist.items():
        summary += f"- {src}: {count}\n"

    summary += "\n---\n"

    summary += "### ✔ Recommendations\n"

    # Delivery recommendation
    if "delivery" in aspect_table.index:
        if aspect_table.loc["delivery", "negative_rate"] > 60:
            summary += "- Improve delivery speed, coordination, and communication.\n"

    # App recommendations
    if "app_issue" in aspect_table.index:
        if aspect_table.loc["app_issue", "negative_rate"] > 50:
            summary += "- Prioritize fixing app crashes, UI bugs, and login issues.\n"

    # Taste
    if "taste" in aspect_table.index:
        if aspect_table.loc["taste", "negative_rate"] < 40:
            summary += "- Taste is mostly positive — maintain food quality.\n"

    # Other categories
    summary += "- Monitor Google reviews daily, as it's the major feedback channel.\n"

    return summary.strip()

