# Predictive Energy-Aware Auto-Scaling — Streamlit Website

## Run on Windows

1. Install Python 3.10 or newer.
2. Extract this project folder.
3. Open Command Prompt or PowerShell in this folder.
4. Create and activate a virtual environment:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

5. Install packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Start the website:

```powershell
streamlit run app.py
```

Streamlit will open the website in your browser, usually at http://localhost:8501.

## Contents

- `app.py`: Home dashboard
- `pages/`: seven separate project pages
- `data/`: supplied project CSV files
- `assets/`: NIT Warangal emblem extracted from the supplied presentation
- `styles.css`: sandy dust / snow white styling

## Notes

- The autoscaling animation is conceptual and illustrative.
- The graphs and evaluation tables load the supplied CSV results.
- Energy and cost are estimates based on the assumptions described in the project presentation.
- The app does not connect to a live cloud provider.
- Online deployment can be configured later using GitHub and Streamlit Community Cloud.
