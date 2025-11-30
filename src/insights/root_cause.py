import pandas as pd


def compute_aspect_sentiment(df):
    """
    Returns table: aspect | positive | negative | neutral | total | negative_rate
    """
    result = (
        df.groupby(["aspect", "sentiment"])
          .size()
          .unstack(fill_value=0)
    )

    # Add totals
    result["total"] = result.sum(axis=1)

    # Add negative rate (%) = negative / total
    if "NEGATIVE" in result.columns:
        result["negative_rate"] = (result["NEGATIVE"] / result["total"]) * 100
    else:
        result["negative_rate"] = 0

    return result.sort_values("negative_rate", ascending=False)


def compute_branch_aspect_matrix(df):
    """
    Returns a matrix: branch × aspect with counts of negative reviews
    """
    neg = df[df["sentiment"] == "NEGATIVE"]
    matrix = pd.crosstab(neg["branch"], neg["aspect"])
    return matrix


def compute_source_distribution(df):
    """
    Returns distribution of feedback by source (google/whatsapp/email/app)
    """
    return df["source"].value_counts()
