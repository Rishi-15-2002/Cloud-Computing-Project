
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from pages.common import load_csv, apply_style

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Results & Evaluation",
    page_icon="📊",
    layout="wide"
)

apply_style()

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("📊 Results & Evaluation")

st.markdown("""
This page presents the experimental comparison of traditional
reactive autoscaling and predictive autoscaling.

Both policies are evaluated against the same actual workload
to compare resource utilization, overload events, scaling
behavior, energy consumption, and estimated operating cost.
""")

st.info(
    "All results shown here are from the Python-based simulation. "
    "They are not measurements from a live cloud environment."
)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def normalize_name(name):
    return (
        str(name)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


def find_column(data, possible_names):
    column_map = {
        normalize_name(column): column
        for column in data.columns
    }

    for name in possible_names:
        key = normalize_name(name)

        if key in column_map:
            return column_map[key]

    return None


def numeric_value(value):
    return pd.to_numeric(value, errors="coerce")


def display_comparison(data, title):
    st.subheader(title)
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# LOAD EXPERIMENTAL DATA
# --------------------------------------------------

try:
    autoscaling = load_csv("phase6_autoscaling_comparison.csv")
except Exception as error:
    st.error(f"Could not load Phase 6 comparison data: {error}")
    autoscaling = pd.DataFrame()

try:
    energy_cost = load_csv("phase7_energy_cost_comparison.csv")
except Exception as error:
    st.error(f"Could not load Phase 7 comparison data: {error}")
    energy_cost = pd.DataFrame()

try:
    final_summary = load_csv("phase8_final_experimental_comparison.csv")
except Exception:
    final_summary = pd.DataFrame()

# --------------------------------------------------
# SECTION 1: AUTOSCALING COMPARISON
# --------------------------------------------------

st.header("1. Autoscaling Performance Comparison")

if not autoscaling.empty:

    st.markdown("""
    The following results compare reactive and predictive
    autoscaling under the same workload conditions.
    """)

    display_comparison(
        autoscaling,
        "Phase 6 Experimental Comparison"
    )

    policy_col = find_column(
        autoscaling,
        ["Policy", "Autoscaling Policy"]
    )

    # --------------------------------------------------
    # UTILIZATION COMPARISON
    # --------------------------------------------------

    st.subheader("CPU and Memory Utilization")

    cpu_col = find_column(
        autoscaling,
        ["Average CPU Utilization (%)", "Average CPU Utilization"]
    )

    memory_col = find_column(
        autoscaling,
        ["Average Memory Utilization (%)", "Average Memory Utilization"]
    )

    if policy_col and (cpu_col or memory_col):

        chart_data = autoscaling.melt(
            id_vars=[policy_col],
            value_vars=[
                col for col in [cpu_col, memory_col] if col
            ],
            var_name="Resource",
            value_name="Average Utilization"
        )

        chart = px.bar(
            chart_data,
            x=policy_col,
            y="Average Utilization",
            color="Resource",
            barmode="group",
            text_auto=".2f",
            title="Average CPU and Memory Utilization",
            template="plotly_white"
        )

        chart.update_layout(
            title_x=0.5,
            hovermode="x unified"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

    # --------------------------------------------------
    # OVERLOAD COMPARISON
    # --------------------------------------------------

    st.subheader("Overload Interval Comparison")

    cpu_overload_col = find_column(
        autoscaling,
        ["CPU Overload Intervals", "CPU Overload Count"]
    )

    memory_overload_col = find_column(
        autoscaling,
        ["Memory Overload Intervals", "Memory Overload Count"]
    )

    if policy_col and (cpu_overload_col or memory_overload_col):

        overload_columns = [
            col for col in [
                cpu_overload_col,
                memory_overload_col
            ] if col
        ]

        overload_data = autoscaling.melt(
            id_vars=[policy_col],
            value_vars=overload_columns,
            var_name="Overload Type",
            value_name="Number of Intervals"
        )

        chart = px.bar(
            overload_data,
            x=policy_col,
            y="Number of Intervals",
            color="Overload Type",
            barmode="group",
            text_auto=True,
            title="CPU and Memory Overload Intervals",
            template="plotly_white"
        )

        chart.update_layout(
            title_x=0.5,
            hovermode="x unified"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

    # --------------------------------------------------
    # SCALING EVENTS
    # --------------------------------------------------

    st.subheader("Scaling Events Comparison")

    scale_up_col = find_column(
        autoscaling,
        ["Scale-up Events", "Scale Up Events"]
    )

    scale_down_col = find_column(
        autoscaling,
        ["Scale-down Events", "Scale Down Events"]
    )

    if policy_col and (scale_up_col or scale_down_col):

        scale_columns = [
            col for col in [
                scale_up_col,
                scale_down_col
            ] if col
        ]

        scale_data = autoscaling.melt(
            id_vars=[policy_col],
            value_vars=scale_columns,
            var_name="Scaling Event",
            value_name="Number of Events"
        )

        chart = px.bar(
            scale_data,
            x=policy_col,
            y="Number of Events",
            color="Scaling Event",
            barmode="group",
            text_auto=True,
            title="Scale-up and Scale-down Events",
            template="plotly_white"
        )

        chart.update_layout(
            title_x=0.5,
            hovermode="x unified"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

    # --------------------------------------------------
    # ACTIVE VM COMPARISON
    # --------------------------------------------------

    st.subheader("Average Active Virtual Machines")

    vm_col = find_column(
        autoscaling,
        ["Average Active VMs", "Average VMs"]
    )

    if policy_col and vm_col:

        chart = px.bar(
            autoscaling,
            x=policy_col,
            y=vm_col,
            color=policy_col,
            text_auto=".2f",
            title="Average Active VMs",
            template="plotly_white"
        )

        chart.update_layout(
            title_x=0.5,
            showlegend=False
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

else:
    st.warning("Phase 6 comparison data is unavailable.")

# --------------------------------------------------
# SECTION 2: ENERGY AND COST
# --------------------------------------------------

st.header("2. Energy and Cost Evaluation")

if not energy_cost.empty:

    display_comparison(
        energy_cost,
        "Phase 7 Energy and Cost Comparison"
    )

    energy_policy_col = find_column(
        energy_cost,
        ["Policy", "Autoscaling Policy"]
    )

    energy_col = find_column(
        energy_cost,
        ["Total Energy (kWh)", "Energy (kWh)"]
    )

    electricity_col = find_column(
        energy_cost,
        ["Electricity Cost (₹)", "Electricity Cost"]
    )

    vm_cost_col = find_column(
        energy_cost,
        ["VM Operating Cost (₹)", "VM Operating Cost"]
    )

    total_cost_col = find_column(
        energy_cost,
        ["Total Estimated Cost (₹)", "Total Cost (₹)", "Total Cost"]
    )

    # Energy chart
    if energy_policy_col and energy_col:

        chart = px.bar(
            energy_cost,
            x=energy_policy_col,
            y=energy_col,
            color=energy_policy_col,
            text_auto=".2f",
            title="Total Energy Consumption",
            template="plotly_white"
        )

        chart.update_layout(
            title_x=0.5,
            showlegend=False
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

    # Cost comparison
    cost_columns = [
        col for col in [
            electricity_col,
            vm_cost_col
        ] if col
    ]

    if energy_policy_col and cost_columns:

        cost_data = energy_cost.melt(
            id_vars=[energy_policy_col],
            value_vars=cost_columns,
            var_name="Cost Category",
            value_name="Cost (₹)"
        )

        chart = px.bar(
            cost_data,
            x=energy_policy_col,
            y="Cost (₹)",
            color="Cost Category",
            barmode="group",
            text_auto=".2f",
            title="Electricity and VM Operating Cost",
            template="plotly_white"
        )

        chart.update_layout(
            title_x=0.5,
            hovermode="x unified"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

    # Total cost chart
    if energy_policy_col and total_cost_col:

        chart = px.bar(
            energy_cost,
            x=energy_policy_col,
            y=total_cost_col,
            color=energy_policy_col,
            text_auto=".2f",
            title="Total Estimated Operating Cost",
            template="plotly_white"
        )

        chart.update_layout(
            title_x=0.5,
            showlegend=False
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

else:
    st.warning("Phase 7 energy and cost data is unavailable.")

# --------------------------------------------------
# SECTION 3: MATHEMATICAL FORMULAS
# --------------------------------------------------

st.header("3. Mathematical Evaluation Metrics")

st.markdown("""
The following formulas are used to interpret the experimental
performance of the autoscaling policies.
""")

st.subheader("Percentage Improvement")

st.latex(
    r"\text{Improvement (\%)} = "
    r"\frac{\text{Baseline} - \text{New Value}}"
    r"{\text{Baseline}} \times 100"
)

st.caption(
    "This formula is suitable when a lower value represents better performance, "
    "such as lower energy consumption, cost, or overload count."
)

st.subheader("Percentage Change")

st.latex(
    r"\text{Percentage Change (\%)} = "
    r"\frac{\text{New Value} - \text{Baseline}}"
    r"{\text{Baseline}} \times 100"
)

st.caption(
    "A positive result means the new value increased; a negative result "
    "means it decreased."
)

st.subheader("Average CPU Utilization")

st.latex(
    r"\text{Average CPU Utilization} = "
    r"\frac{1}{n}\sum_{i=1}^{n}"
    r"\text{CPU Utilization}_i"
)

st.subheader("Average Memory Utilization")

st.latex(
    r"\text{Average Memory Utilization} = "
    r"\frac{1}{n}\sum_{i=1}^{n}"
    r"\text{Memory Utilization}_i"
)

st.subheader("Total Energy Consumption")

st.latex(
    r"E_{\text{total}} = "
    r"\sum_{i=1}^{n} P_i \times \Delta t"
)

st.caption(
    "When power is measured in watts and time in hours, divide "
    "the result by 1000 to obtain energy in kWh."
)

st.subheader("Total Estimated Operating Cost")

st.latex(
    r"C_{\text{total}} = "
    r"C_{\text{electricity}} + C_{\text{VM}}"
)

# --------------------------------------------------
# SECTION 4: EXPERIMENTAL FINDINGS
# --------------------------------------------------

st.header("4. Experimental Findings")

st.markdown("""
Based on the project's recorded simulation results:
""")

findings = [
    "Both policies reached the configured maximum of 100 VMs.",
    "Predictive autoscaling recorded lower average CPU utilization.",
    "Predictive autoscaling recorded lower average memory utilization.",
    "Predictive autoscaling recorded slightly fewer CPU and memory overload intervals.",
    "Predictive autoscaling generated fewer scaling events.",
    "Predictive autoscaling consumed slightly more estimated energy.",
    "Predictive autoscaling had a slightly higher estimated total operating cost."
]

for finding in findings:
    st.markdown(f"- {finding}")

# --------------------------------------------------
# SECTION 5: FINAL SUMMARY
# --------------------------------------------------

st.header("5. Overall Evaluation")

st.markdown("""
The experimental results show that predictive autoscaling can
improve some resource-management indicators, including average
resource utilization and overload intervals.

However, in this experiment, predictive autoscaling did not
achieve lower estimated energy consumption or total operating cost.

Both policies reached the maximum VM limit. This constraint may
have affected the overall results and should be considered when
interpreting the comparison.

Therefore, the experiment demonstrates a trade-off between
resource utilization, scaling behavior, energy consumption,
and estimated operating cost.
""")

# --------------------------------------------------
# SECTION 6: LIMITATIONS
# --------------------------------------------------

st.header("6. Experimental Limitations")

st.markdown("""
1. The experiment uses a Python-based simulation rather than
   a live cloud infrastructure.
2. Energy consumption is estimated using an assumed power model.
3. Electricity and VM operating prices are assumed values.
4. The maximum VM allocation is limited to 100 VMs.
5. VM startup delays and migration overhead are not fully modeled.
6. Results depend on the selected workload trace and forecasting accuracy.
""")

st.divider()

st.success(
    "Results and evaluation page completed. "
    "All mathematical formulas use Streamlit's LaTeX renderer."
)
