(# Customer Feedback Intelligence)

Small demo project to run the Customer Feedback Intelligence Streamlit dashboard.

Quick start
-----------

1. Create and activate the project's virtual environment (if not already):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt```

3. Run the Streamlit app (recommended):

```bash
streamlit run dashboard/app.py
```

Or run as a module:

```bash
python -m dashboard.app
```

Notes
-----
- The repository root is added to `sys.path` inside `dashboard/app.py` so `from src...` imports work when running from the `dashboard` folder.
- If you get warnings about `use_container_width`, update calls to `st.plotly_chart(..., width='stretch')`.

