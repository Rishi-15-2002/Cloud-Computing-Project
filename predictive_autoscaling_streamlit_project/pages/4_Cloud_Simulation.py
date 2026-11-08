
import streamlit as st
import pandas as pd
import plotly.express as px
import math

from pages.common import load_csv, apply_style

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cloud Simulation",
    page_icon="☁️",
    layout="wide"
)

apply_style()

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("☁️ Cloud Resource Simulation")

st.markdown("""
This page explains how the Python-based cloud simulation models
virtual machine allocation and resource utilization.

The simulation uses aggregated workload traces to estimate how many
virtual machines are required to handle CPU and memory demand at
each 5-minute interval.
""")

st.info(
    "This is a Python-based cloud simulation. It does not provision "
    "or control actual virtual machines on AWS, Azure, or Google Cloud."
)

# --------------------------------------------------
# SIMULATION CONFIGURATION
# --------------------------------------------------

st.header("1. Simulation Configuration")

config = {
    "Parameter": [
        "Simulation interval",
        "CPU utilization target",
        "Memory utilization target",
        "Minimum number of VMs",
        "Maximum number of VMs",
        "Scaling approach"
    ],
    "Configured value": [
        "5 minutes",
        "70%",
        "70%",
        "1 VM",
        "100 VMs",
        "CPU and memory demand"
    ]
}

st.table(pd.DataFrame(config))

# --------------------------------------------------
# LOAD WORKLOAD DATA
# --------------------------------------------------

st.header("2. Historical Fleet Workload")

try:
    workload = load_csv("fleet_workload_5min.csv")

    st.markdown(
        "The aggregated fleet workload is used as the input "
        "to the cloud resource simulation."
    )

    st.caption(
        f"Total workload intervals: {len(workload):,}"
    )

    st.dataframe(
        workload.head(10),
        use_container_width=True,
        hide_index=True
    )

except Exception as error:
    st.error(f"Unable to load workload data: {error}")
    workload = pd.DataFrame()

# --------------------------------------------------
# RESOURCE ALLOCATION FORMULAS
# --------------------------------------------------

st.header("3. Resource Allocation Calculations")

st.subheader("CPU Utilization")

st.markdown("""
CPU utilization represents the percentage of allocated CPU capacity
required by the workload.
""")

st.latex(
    r"\text{CPU Utilization (\%)} = "
    r"\frac{\text{CPU Demand}}{\text{Total Allocated CPU Capacity}}"
    r"\times 100"
)

st.subheader("Memory Utilization")

st.markdown("""
Memory utilization represents the percentage of allocated memory
capacity required by the workload.
""")

st.latex(
    r"\text{Memory Utilization (\%)} = "
    r"\frac{\text{Memory Demand}}{\text{Total Allocated Memory Capacity}}"
    r"\times 100"
)

st.subheader("CPU-Based VM Requirement")

st.markdown("""
The number of VMs required based on CPU demand is calculated
using CPU capacity per VM and the target utilization.
""")

st.latex(
    r"N_{\text{CPU}} = "
    r"\left\lceil "
    r"\frac{D_{\text{CPU}}}"
    r"{C_{\text{CPU}} \times U_{\text{target}}}"
    r"\right\rceil"
)

st.subheader("Memory-Based VM Requirement")

st.markdown("""
The number of VMs required based on memory demand is calculated
using memory capacity per VM and the target utilization.
""")

st.latex(
    r"N_{\text{Memory}} = "
    r"\left\lceil "
    r"\frac{D_{\text{Memory}}}"
    r"{C_{\text{Memory}} \times U_{\text{target}}}"
    r"\right\rceil"
)

st.subheader("Final VM Requirement")

st.markdown("""
The final requirement is the larger of the CPU-based and
memory-based VM requirements, subject to the configured
minimum and maximum VM limits.
""")

st.latex(
    r"N_{\text{required}} = "
    r"\min\left("
    r"N_{\max}, "
    r"\max\left("
    r"N_{\min}, N_{\text{CPU}}, N_{\text{Memory}}"
    r"\right)\right)"
)

# --------------------------------------------------
# FORMULA SYMBOL EXPLANATION
# --------------------------------------------------

with st.expander("Understand the mathematical symbols"):

    symbols = {
        "Symbol": [
            "D_CPU",
            "D_Memory",
            "C_CPU",
            "C_Memory",
            "U_target",
            "N_min",
            "N_max"
        ],
        "Meaning": [
            "Total CPU workload demand",
            "Total memory workload demand",
            "CPU capacity of one VM",
            "Memory capacity of one VM",
            "Target utilization expressed as a fraction",
            "Minimum permitted VM count",
            "Maximum permitted VM count"
        ]
    }

    st.table(pd.DataFrame(symbols))

# --------------------------------------------------
# INTERACTIVE VM REQUIREMENT CALCULATOR
# --------------------------------------------------

st.header("4. Interactive VM Requirement Calculator")

st.markdown("""
Change the workload demand and VM capacity to understand
how resource requirements affect the estimated number of VMs.

This calculator is illustrative and does not modify the
original Phase 5 simulation results.
""")

col1, col2 = st.columns(2)

with col1:

    cpu_demand = st.number_input(
        "CPU demand (MHz)",
        min_value=1.0,
        value=10000.0,
        step=1000.0
    )

    cpu_capacity = st.number_input(
        "CPU capacity per VM (MHz)",
        min_value=1.0,
        value=4000.0,
        step=500.0
    )

with col2:

    memory_demand = st.number_input(
        "Memory demand (KB)",
        min_value=1.0,
        value=10000000.0,
        step=1000000.0
    )

    memory_capacity = st.number_input(
        "Memory capacity per VM (KB)",
        min_value=1.0,
        value=4000000.0,
        step=500000.0
    )

target = st.slider(
    "Target utilization (%)",
    min_value=10,
    max_value=100,
    value=70
)

# --------------------------------------------------
# CALCULATE VM REQUIREMENTS
# --------------------------------------------------

target_fraction = target / 100.0

cpu_vms = math.ceil(
    cpu_demand / (cpu_capacity * target_fraction)
)

memory_vms = math.ceil(
    memory_demand / (memory_capacity * target_fraction)
)

minimum_vms = 1
maximum_vms = 100

unlimited_required = max(
    minimum_vms,
    cpu_vms,
    memory_vms
)

required_vms = min(
    maximum_vms,
    unlimited_required
)

# --------------------------------------------------
# DISPLAY CALCULATOR RESULTS
# --------------------------------------------------

st.subheader("Calculated VM Requirements")

result1, result2, result3 = st.columns(3)

result1.metric(
    "CPU-Based VM Requirement",
    f"{cpu_vms:,}"
)

result2.metric(
    "Memory-Based VM Requirement",
    f"{memory_vms:,}"
)

result3.metric(
    "Final VM Requirement",
    f"{required_vms:,}"
)

if unlimited_required > maximum_vms:

    st.warning(
        f"The calculated requirement is {unlimited_required:,} VMs, "
        f"but the configured maximum is {maximum_vms} VMs. "
        "The final allocation is capped at 100 VMs."
    )

else:

    st.success(
        f"The estimated allocation is {required_vms:,} virtual machine(s)."
    )

# --------------------------------------------------
# SIMULATION WORKFLOW
# --------------------------------------------------

st.header("5. Cloud Simulation Workflow")

workflow = [
    "Load aggregated historical workload data",
    "Read CPU and memory demand",
    "Determine available VM capacity",
    "Calculate CPU and memory utilization",
    "Estimate the required number of VMs",
    "Apply minimum and maximum VM limits",
    "Record resource allocation and utilization"
]

for index, step in enumerate(workflow):

    st.markdown(
        f"**Step {index + 1}:** {step}"
    )

    if index < len(workflow) - 1:
        st.markdown("↓")

# --------------------------------------------------
# WORKLOAD VISUALIZATION
# --------------------------------------------------

if not workload.empty:

    st.header("6. Workload Visualization")

    numeric_columns = workload.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        selected_column = st.selectbox(
            "Select a workload variable",
            numeric_columns
        )

        chart = px.line(
            workload,
            y=selected_column,
            title=f"Workload Trend: {selected_column}",
            labels={
                "index": "5-minute interval",
                selected_column: selected_column
            },
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

    else:

        st.warning(
            "No numeric workload columns were found for visualization."
        )

# --------------------------------------------------
# SIMULATION ASSUMPTIONS AND LIMITATIONS
# --------------------------------------------------

st.header("7. Simulation Assumptions and Limitations")

st.markdown("""
- Workload data is aggregated into 5-minute intervals.
- CPU and memory are considered when estimating resource demand.
- Target utilization is set to 70% in the simulation configuration.
- The configured minimum VM count is 1.
- The configured maximum VM count is 100.
- The simulation is implemented in Python rather than a live cloud.
- Real-world VM startup delays, migration overhead, and cloud-provider
  pricing are not fully represented in this basic resource model.
""")

# --------------------------------------------------
# CONCLUSION
# --------------------------------------------------

st.divider()

st.subheader("Conclusion")

st.markdown("""
The cloud simulation provides the resource-allocation environment
used to compare reactive and predictive autoscaling.

It converts historical workload demand into estimated VM requirements
and provides the basis for analyzing resource utilization, overload
events, scaling behavior, energy consumption, and operating cost.
""")

st.warning(
    "The interactive calculator is an illustrative example. "
    "The actual experimental results are generated by the project's "
    "Phase 5 simulation and are evaluated separately."
)
