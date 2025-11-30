import sys
import os
from pathlib import Path

# Ensure project root is on sys.path so `from src...` imports work
# When running `python dashboard/app.py`, Python's import path doesn't include
# the repository root by default (it includes the `dashboard` dir). Insert the
# project root at the front of `sys.path` so `src` is discoverable.
project_root = Path(__file__).resolve().parents[1]
project_root_str = str(project_root)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

print("\nPYTHONPATH CHECK:")
for p in sys.path:
    print(p)
print("-----\n")
def main():
    """Run the Streamlit dashboard.

    Imports heavy dependencies inside the function so that importing the
    module (for tests or other scripts) doesn't immediately require
    `streamlit`/`pandas` to be installed.
    """

    import streamlit as st
    import pandas as pd
    import plotly.express as px

    from src.insights.summary_generator import generate_summary
    from src.insights.root_cause import (
        compute_aspect_sentiment,
        compute_branch_aspect_matrix,
        compute_source_distribution,
    )

    # ---------------------------
    # Load Data
    # ---------------------------
    data_file = project_root / "data" / "processed" / "all_feedback_final.csv"
    df = pd.read_csv(str(data_file))

    # ---------------------------
    # Streamlit Layout
    # ---------------------------
    st.set_page_config(
        page_title="Customer Feedback Intelligence",
        layout="wide",
    )

    st.title("📊 Customer Feedback Intelligence Dashboard")
    st.markdown("---")

    # ---------------------------
    # Summary Section
    # ---------------------------
    st.header("📝 Executive Summary")
    summary = generate_summary()
    st.markdown(summary)
    st.markdown("---")

    # ---------------------------
    # Sentiment by Aspect
    # ---------------------------
    st.header("📌 Aspect-wise Sentiment Overview")

    aspect_table = compute_aspect_sentiment(df).reset_index()

    fig_aspect = px.bar(
        aspect_table,
        x="aspect",
        y="negative_rate",
        color="aspect",
        title="Negative Sentiment Rate by Aspect (%)",
    )
    st.plotly_chart(fig_aspect, use_container_width=True)
    st.markdown("---")

    # ---------------------------
    # Branch Matrix (Negative Reviews)
    # ---------------------------
    st.header("🏪 Branch × Aspect (Negative Reviews Only)")

    branch_matrix = compute_branch_aspect_matrix(df)

    if not branch_matrix.empty:
        fig_branch = px.imshow(
            branch_matrix,
            text_auto=True,
            aspect="auto",
            title="Negative Reviews Heatmap",
        )
        st.plotly_chart(fig_branch, use_container_width=True)
    else:
        st.info("No branch-level negative reviews to display.")
    st.markdown("---")

    # ---------------------------
    # Source Distribution
    # ---------------------------
    st.header("📲 Source-wise Feedback Distribution")

    source_dist = compute_source_distribution(df)

    fig_source = px.pie(
        values=source_dist.values,
        names=source_dist.index,
        title="Sources of Feedback",
        hole=0.4,
    )

    st.plotly_chart(fig_source, use_container_width=True)
    st.markdown("---")

    # ---------------------------
    # Data Table Section
    # ---------------------------
    st.header("📄 Raw Dataset Preview")
    st.dataframe(df)

    # ---------------------------
    # Download Button
    # ---------------------------
    csv_download = df.to_csv(index=False).encode()
    st.download_button(
        label="⬇️ Download Processed CSV",
        data=csv_download,
        file_name="feedback_processed.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.write("Built by Manoj • Customer Feedback Intelligence System")


if __name__ == "__main__":
    main()
