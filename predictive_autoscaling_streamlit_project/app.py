
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Predictive Energy-Aware Auto-Scaling", page_icon="☁️", layout="wide", initial_sidebar_state="expanded")
ROOT = Path(__file__).parent
st.markdown((ROOT / "styles.css").read_text(encoding="utf-8"), unsafe_allow_html=True)

with st.sidebar:
    logo = ROOT / "assets" / "nitw_emblem.png"
    if logo.exists():
        st.image(str(logo), width=115)
    st.markdown("### NIT Warangal")
    st.caption("M.Tech • Computer Science and Engineering")
    st.divider()
    st.markdown("**PROJECT NAVIGATION**")
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_Project_Introduction.py", label="Project Introduction", icon="🎓")
    st.page_link("pages/2_Dataset.py", label="Dataset", icon="🗃️")
    st.page_link("pages/3_ML_Forecasting.py", label="ML Forecasting", icon="🧠")
    st.page_link("pages/4_Cloud_Simulation.py", label="Cloud Simulation", icon="☁️")
    st.page_link("pages/5_Autoscaling_Animation.py", label="Autoscaling Animation", icon="⚙️")
    st.page_link("pages/6_Energy_Analysis.py", label="Energy Analysis", icon="⚡")
    st.page_link("pages/7_Results_Evaluation.py", label="Results & Evaluation", icon="📊")
    st.divider()
    st.caption("Bitbrains GWA-T-12 fastStorage • Python simulation")

st.markdown("""
<div class="hero">
  <div class="eyebrow">M.Tech • Cloud Computing + Machine Learning</div>
  <h1>Predictive Energy-Aware<br>Auto-Scaling</h1>
  <p>Cost-Efficient Cloud Resource Management</p>
  <p>Forecasting fleet workload to inform virtual-machine allocation, compare reactive and predictive autoscaling, and evaluate utilization, energy, and estimated operating cost.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.markdown("### Explore the project")
st.caption("Choose a section to explore the dataset, forecasting pipeline, cloud simulation, and experimental findings.")

cards = [
    ("🎓","Project Introduction","Project motivation, team, mentor, and objectives.","pages/1_Project_Introduction.py"),
    ("🗃️","Dataset","Bitbrains trace, workload signals, and engineered features.","pages/2_Dataset.py"),
    ("🧠","ML Forecasting","Prediction targets, candidate regressors, and test metrics.","pages/3_ML_Forecasting.py"),
    ("☁️","Cloud Simulation","VM capacity assumptions and allocation logic.","pages/4_Cloud_Simulation.py"),
    ("⚙️","Auto-Scaling","Interactive reactive-versus-predictive animation.","pages/5_Autoscaling_Animation.py"),
    ("⚡","Energy Analysis","Power model, energy estimates, and cost assumptions.","pages/6_Energy_Analysis.py"),
    ("📊","Results & Evaluation","Interactive charts and detailed evaluation metrics.","pages/7_Results_Evaluation.py"),
]
for row in range(0, len(cards), 2):
    cols = st.columns(2)
    for col, item in zip(cols, cards[row:row+2]):
        emoji, title, desc, target = item
        with col:
            st.markdown(f'<div class="section-card"><div class="emoji">{emoji}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            st.page_link(target, label=f"Open {title} →")
st.markdown("")
st.markdown('<div class="info-note">This website presents a Python-based simulation using the Bitbrains GWA-T-12 fastStorage trace. Energy and cost are estimates based on stated assumptions, not measurements from a live cloud provider.</div>', unsafe_allow_html=True)
