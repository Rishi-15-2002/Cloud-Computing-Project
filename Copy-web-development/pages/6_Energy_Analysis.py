
import streamlit as st
import pandas as pd
import plotly.express as px

from pages.common import load_csv, apply_style

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Energy & Cost Analysis",
    page_icon="⚡",
    layout="wide"
)

apply_style()

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("⚡ Energy & Cost Analysis")

st.markdown("""
This section compares the estimated energy consumption and operating
cost of the **Reactive Autoscaling** and **Predictive Autoscaling**
approaches.

The calculations are based on the assumptions used in the Python
cloud simulation.
""")

st.info(
    "Note: Energy consumption and costs are simulation estimates. "
    "They are not measurements from physical servers or actual cloud invoices."
)

# --------------------------------------------------
# LOAD PHASE 7 DATA
# --------------------------------------------------

df = load_csv("phase7_energy_cost_comparison.csv")

# The policy names are stored in the first CSV column.
if "Unnamed: 0" in df.columns:
    df = df.rename(columns={"Unnamed: 0": "Policy"})

df["Policy"] = df["Policy"].astype(str)

# --------------------------------------------------
# ENERGY AND COST COMPARISON TABLE
# --------------------------------------------------

st.header("1. Energy and Cost Comparison")

display_df = df.copy()

# Format values for easier reading
currency_columns = [
    "Electricity Cost (₹)",
    "VM Operating Cost (₹)",
    "Total Estimated Cost (₹)"
]

for column in currency_columns:
    display_df[column] = display_df[column].map(
        lambda value: f"₹{value:,.2f}"
    )

display_df["Total Energy (kWh)"] = display_df[
    "Total Energy (kWh)"
].map(lambda value: f"{value:,.2f}")

display_df["Average Active VMs"] = display_df[
    "Average Active VMs"
].map(lambda value: f"{value:,.2f}")

display_df["Average Power (W)"] = display_df[
    "Average Power (W)"
].map(lambda value: f"{value:,.2f}")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# ENERGY CONSUMPTION CHART
# --------------------------------------------------

st.header("2. Energy Consumption Comparison")

energy_chart = px.bar(
    df,
    x="Policy",
    y="Total Energy (kWh)",
    color="Policy",
    text_auto=".2f",
    title="Total Estimated Energy Consumption",
    labels={
        "Policy": "Autoscaling Policy",
        "Total Energy (kWh)": "Energy Consumption (kWh)"
    },
    template="plotly_white"
)

energy_chart.update_layout(
    title_x=0.5,
    hovermode="x unified"
)

st.plotly_chart(
    energy_chart,
    use_container_width=True
)

# --------------------------------------------------
# ELECTRICITY COST COMPARISON
# --------------------------------------------------

st.header("3. Electricity Cost Comparison")

electricity_chart = px.bar(
    df,
    x="Policy",
    y="Electricity Cost (₹)",
    color="Policy",
    text_auto=".2f",
    title="Estimated Electricity Cost",
    labels={
        "Policy": "Autoscaling Policy",
        "Electricity Cost (₹)": "Electricity Cost (₹)"
    },
    template="plotly_white"
)

electricity_chart.update_layout(
    title_x=0.5,
    hovermode="x unified"
)

st.plotly_chart(
    electricity_chart,
    use_container_width=True
)

# --------------------------------------------------
# VM OPERATING COST COMPARISON
# --------------------------------------------------

st.header("4. VM Operating Cost Comparison")

vm_chart = px.bar(
    df,
    x="Policy",
    y="VM Operating Cost (₹)",
    color="Policy",
    text_auto=".2f",
    title="Estimated VM Operating Cost",
    labels={
        "Policy": "Autoscaling Policy",
        "VM Operating Cost (₹)": "VM Operating Cost (₹)"
    },
    template="plotly_white"
)

vm_chart.update_layout(
    title_x=0.5,
    hovermode="x unified"
)

st.plotly_chart(
    vm_chart,
    use_container_width=True
)

# --------------------------------------------------
# TOTAL COST COMPARISON
# --------------------------------------------------

st.header("5. Total Operating Cost Comparison")

cost_chart = px.bar(
    df,
    x="Policy",
    y="Total Estimated Cost (₹)",
    color="Policy",
    text_auto=".2f",
    title="Total Estimated Operating Cost",
    labels={
        "Policy": "Autoscaling Policy",
        "Total Estimated Cost (₹)": "Total Cost (₹)"
    },
    template="plotly_white"
)

cost_chart.update_layout(
    title_x=0.5,
    hovermode="x unified"
)

st.plotly_chart(
    cost_chart,
    use_container_width=True
)

# --------------------------------------------------
# MATHEMATICAL FORMULAS
# --------------------------------------------------

st.header("6. Mathematical Formulas")

st.subheader("Energy Consumption")

st.markdown(
    "Energy consumption is calculated using power consumption "
    "and the duration of operation."
)

st.latex(
    r"\text{Energy (kWh)} = "
    r"\frac{\text{Power (W)} \times \text{Time (h)}}{1000}"
)

st.subheader("Total Operating Cost")

st.markdown(
    "The total estimated operating cost is the sum of electricity "
    "cost and VM operating cost."
)

st.latex(
    r"\text{Total Cost} = "
    r"\text{Electricity Cost} + \text{VM Operating Cost}"
)

# --------------------------------------------------
# SIMULATION ASSUMPTIONS
# --------------------------------------------------

st.header("7. Simulation Assumptions")

assumptions = {
    "Parameter": [
        "Idle Power per VM",
        "Maximum Power per VM",
        "Power Model",
        "Power Usage Effectiveness (PUE)",
        "Electricity Tariff",
        "VM Operating Rate",
        "Simulation Interval"
    ],
    "Value": [
        "100 W",
        "200 W",
        "Linear CPU-to-power relationship",
        "1.5",
        "₹8 per kWh",
        "₹5 per VM-hour",
        "5 minutes"
    ]
}

assumptions_df = pd.DataFrame(assumptions)

st.table(assumptions_df)

# --------------------------------------------------
# AUTOMATIC RESULT INTERPRETATION
# --------------------------------------------------

st.header("8. Result Interpretation")

reactive = df[df["Policy"].str.lower() == "reactive"]
predictive = df[df["Policy"].str.lower() == "predictive"]

if not reactive.empty and not predictive.empty:

    reactive_energy = reactive["Total Energy (kWh)"].iloc[0]
    predictive_energy = predictive["Total Energy (kWh)"].iloc[0]

    reactive_cost = reactive["Total Estimated Cost (₹)"].iloc[0]
    predictive_cost = predictive["Total Estimated Cost (₹)"].iloc[0]

    energy_difference = (
        (predictive_energy - reactive_energy)
        / reactive_energy
    ) * 100

    cost_difference = (
        (predictive_cost - reactive_cost)
        / reactive_cost
    ) * 100

    st.markdown("### Energy consumption findings")

    if energy_difference > 0:
        st.write(
            f"Predictive autoscaling consumed approximately "
            f"{energy_difference:.2f}% more energy than reactive autoscaling."
        )
    elif energy_difference < 0:
        st.write(
            f"Predictive autoscaling consumed approximately "
            f"{abs(energy_difference):.2f}% less energy than reactive autoscaling."
        )
    else:
        st.write("Both policies consumed approximately the same energy.")

    st.markdown("### Operating cost findings")

    if cost_difference > 0:
        st.write(
            f"Predictive autoscaling had approximately "
            f"{cost_difference:.2f}% higher estimated operating cost."
        )
    elif cost_difference < 0:
        st.write(
            f"Predictive autoscaling had approximately "
            f"{abs(cost_difference):.2f}% lower estimated operating cost."
        )
    else:
        st.write("Both policies had approximately the same estimated cost.")

# --------------------------------------------------
# FINAL NOTE
# --------------------------------------------------

st.divider()

st.subheader("Conclusion")

st.markdown("""
The energy and cost analysis provides a quantitative comparison of
reactive and predictive autoscaling.

The results should be interpreted alongside the resource utilization,
overload, and scaling-event results. Predictive autoscaling should not
automatically be considered more energy-efficient or less expensive:
its actual performance depends on workload forecasts, VM allocation,
and the simulation assumptions.
""")

st.warning(
    "Limitation: The power model, electricity tariff, VM operating rate, "
    "and PUE are assumed simulation parameters. Real-world cloud energy "
    "consumption and pricing may differ."
)
