
import streamlit as st
from pathlib import Path
from pages.common import ROOT, apply_style
st.set_page_config(page_title="Project Introduction", page_icon="🎓", layout="wide")
apply_style()
st.title("Project Introduction")
st.caption("National Institute of Technology Warangal • M.Tech, Computer Science and Engineering")
c1,c2 = st.columns([1,2])
with c1:
    logo = ROOT / "assets" / "nitw_emblem.png"
    if logo.exists(): st.image(str(logo), use_container_width=True)
with c2:
    st.markdown("## Predictive Energy-Aware Auto-Scaling")
    st.markdown("### for Cost-Efficient Cloud Resource Management")
    st.write("A Python-based cloud workload forecasting and autoscaling study using the Bitbrains GWA-T-12 fastStorage trace.")
st.divider()
a,b = st.columns(2)
with a:
    st.subheader("Project team")
    st.markdown("**Hrishikesh Chandra**  \n26CSM1R05")
    st.markdown("**Prakash Kumar**  \n26CSM1R16")
with b:
    st.subheader("Project mentor")
    st.markdown("**Prof. Manoj Kumar Patra**")
    st.markdown("**Programme:** M.Tech – Computer Science and Engineering")
st.divider()
st.subheader("Project objectives")
st.markdown("- Forecast next-interval fleet CPU and memory demand from historical workload features.\n- Compare a reactive baseline with ML-driven predictive autoscaling.\n- Estimate energy consumption and operating cost under explicit simulation assumptions.")
