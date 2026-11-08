
import streamlit as st
import pandas as pd
import plotly.express as px

from pages.common import load_csv, apply_style

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ML Forecasting",
    page_icon="🤖",
    layout="wide"
)

apply_style()

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🤖 Machine Learning Forecasting")

st.markdown("""
This page presents the machine learning models used to predict
future CPU and memory workload in the cloud environment.

The forecasting process uses historical workload information
to estimate resource demand for the next 5-minute interval.
""")

st.info(
    "The models are evaluated using a chronological train, "
    "validation, and test split to preserve the time-series order."
)

# --------------------------------------------------
# LOAD MODEL RESULTS
# --------------------------------------------------

df = load_csv("phase4_final_test_results.csv")

st.header("1. Model Evaluation Results")

st.markdown("""
The project evaluates three machine learning algorithms:

- **Linear Regression:** A linear model used to learn relationships
  between workload features and future resource usage.
- **Random Forest:** An ensemble of decision trees that captures
  nonlinear patterns.
- **XGBoost:** A gradient-boosting algorithm that builds trees
  sequentially to improve prediction accuracy.
""")

# Display the actual CSV results
st.subheader("Final Test Results")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# IDENTIFY COLUMN NAMES
# --------------------------------------------------

# Normalize column names for flexible matching
def normalize_name(name):
    return (
        str(name)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )

column_map = {
    normalize_name(column): column
    for column in df.columns
}

def find_column(possible_names):
    for name in possible_names:
        key = normalize_name(name)
        if key in column_map:
            return column_map[key]
    return None

target_col = find_column(["Target", "target_name"])
model_col = find_column(["Selected Model", "Model"])
mae_col = find_column(["Test MAE", "MAE"])
rmse_col = find_column(["Test RMSE", "RMSE"])
r2_col = find_column(["Test R2", "Test R²", "R2", "R²"])

# --------------------------------------------------
# METRIC INTERPRETATION
# --------------------------------------------------

st.header("2. Evaluation Metrics")

st.markdown("""
The forecasting models are evaluated using three standard
regression metrics: Mean Absolute Error (MAE), Root Mean
Squared Error (RMSE), and the coefficient of determination (R²).
""")

st.subheader("Mean Absolute Error (MAE)")

st.latex(
    r"\mathrm{MAE} = "
    r"\frac{1}{n}\sum_{i=1}^{n}"
    r"\left|y_i-\hat{y}_i\right|"
)

st.markdown("""
MAE measures the average absolute difference between actual
and predicted values. A lower MAE indicates more accurate predictions.
""")

st.subheader("Root Mean Squared Error (RMSE)")

st.latex(
    r"\mathrm{RMSE} = "
    r"\sqrt{\frac{1}{n}\sum_{i=1}^{n}"
    r"(y_i-\hat{y}_i)^2}"
)

st.markdown("""
RMSE measures prediction error while giving greater weight
to larger errors. A lower RMSE indicates better prediction accuracy.
""")

st.subheader("Coefficient of Determination (R²)")

st.latex(
    r"R^2 = 1 - "
    r"\frac{\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}"
    r"{\sum_{i=1}^{n}(y_i-\bar{y})^2}"
)

st.markdown("""
R² indicates how well the model explains the variation in
the actual workload values.

- R² close to 1: Strong explanatory performance.
- R² close to 0: Performance similar to predicting the mean.
- R² below 0: Worse than predicting the mean on the evaluated data.
""")

st.caption("""
Where n is the number of test observations, yᵢ is the actual value,
ŷᵢ is the predicted value, and ȳ is the mean of actual values.
""")

# --------------------------------------------------
# DISPLAY SELECTED MODEL METRICS
# --------------------------------------------------

st.header("3. Selected Model Performance")

if all([
    target_col,
    model_col,
    mae_col,
    rmse_col,
    r2_col
]):

    results = df.copy()

    for col in [mae_col, rmse_col, r2_col]:
        results[col] = pd.to_numeric(
            results[col],
            errors="coerce"
        )

    for _, row in results.iterrows():

        target_name = str(row[target_col])

        with st.expander(
            f"{target_name} Forecasting Results",
            expanded=True
        ):

            st.write(
                f"**Selected Model:** {row[model_col]}"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Test MAE",
                f"{row[mae_col]:,.2f}"
            )

            col2.metric(
                "Test RMSE",
                f"{row[rmse_col]:,.2f}"
            )

            col3.metric(
                "Test R²",
                f"{row[r2_col]:.4f}"
            )

else:
    st.warning(
        "The CSV column names do not match the expected evaluation "
        "fields. The original results table is shown above. "
        "Please check the CSV headers before displaying individual metrics."
    )

# --------------------------------------------------
# MODEL SELECTION EXPLANATION
# --------------------------------------------------

st.header("4. Model Selection Methodology")

st.markdown("""
The forecasting workflow follows these steps:

1. Historical workload data is prepared and transformed into
   time-series features.
2. The dataset is divided chronologically into training,
   validation, and test sets.
3. Linear Regression, Random Forest, and XGBoost are evaluated.
4. Validation MAE is used to select the best model separately
   for CPU and memory forecasting.
5. The selected model is trained using the combined training
   and validation data.
6. Final performance is evaluated on the held-out test data.
""")

# --------------------------------------------------
# FORECASTING WORKFLOW
# --------------------------------------------------

st.header("5. Forecasting Workflow")

workflow = [
    "Historical workload data",
    "Feature engineering",
    "Training and validation",
    "Model selection",
    "Final test evaluation",
    "Next 5-minute workload prediction"
]

for index, step in enumerate(workflow):
    st.markdown(f"**{index + 1}.** {step}")
    if index != len(workflow) - 1:
        st.markdown("↓")

# --------------------------------------------------
# FINAL NOTE
# --------------------------------------------------

st.divider()

st.subheader("Conclusion")

st.markdown("""
Machine learning forecasting provides an estimate of future CPU
and memory demand. The selected forecasting models supply workload
predictions to the predictive autoscaling simulator, allowing it
to make resource-allocation decisions before the next workload interval.
""")

st.warning("""
The reported evaluation metrics represent performance on the
held-out test dataset. They do not guarantee identical prediction
accuracy on future workloads or in a live cloud environment.
""")
