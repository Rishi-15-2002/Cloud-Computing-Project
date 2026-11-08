
import streamlit as st
import plotly.express as px
from pages.common import load_csv, apply_style
st.set_page_config(page_title="Dataset", page_icon="🗃️", layout="wide")
apply_style()
st.title("Dataset & Feature Engineering")
st.write("Source: Bitbrains GWA-T-12 fastStorage trace. The supplied fleet file contains five-minute aggregated observations.")
df=load_csv("fleet_workload_5min.csv")
features=load_csv("fleet_features_phase3.csv")
c1,c2,c3=st.columns(3)
c1.metric("Fleet intervals",f"{len(df):,}")
c2.metric("Feature columns",f"{len(features.columns):,}")
c3.metric("Trace coverage (mean)",f"{df['trace_vm_coverage_pct'].mean():.2f}%")
st.subheader("Selected fleet workload signals")
choices=["total_cpu_usage_mhz","total_memory_usage_kb","active_vm_count","total_disk_read_kbps","total_disk_write_kbps","total_network_received_kbps","total_network_transmitted_kbps"]
selected=st.selectbox("Choose a signal",choices)
plot=df[["timestamp",selected]].copy()
plot["timestamp"]=__import__("pandas").to_datetime(plot["timestamp"])
fig=px.line(plot,x="timestamp",y=selected,title=selected.replace("_"," ").title(),template="plotly_white")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig,use_container_width=True)
with st.expander("Feature groups used for forecasting"):
    st.markdown("- Lag history: 1, 2, 3, 6, and 12 intervals.\n- Rolling means: 3, 6, and 12 intervals.\n- Trend differences and percentage changes: 1, 3, and 6 intervals.\n- Time context: hour/day-of-week cyclical features, weekend flag, and trace coverage.")
st.dataframe(features.head(10),use_container_width=True)
