
import streamlit as st
import time
from pages.common import apply_style
st.set_page_config(page_title="Autoscaling Animation", page_icon="⚙️", layout="wide")
apply_style()
st.title("Reactive vs Predictive Autoscaling")
st.write("Illustrative animation of the control-flow difference. It is a conceptual demonstration, not a replay of individual CSV rows.")
mode=st.radio("Choose model",["Traditional reactive","Predictive"],horizontal=True)
if "anim_step" not in st.session_state: st.session_state.anim_step=0
labels=["Normal client traffic","Client requests rise sharply","Capacity pressure / forecast signal","VM fleet scales out","Workload is served by expanded fleet"]
if st.button("Reset animation"): st.session_state.anim_step=0
c1,c2,c3=st.columns(3)
with c1:
    if st.button("Previous stage",disabled=st.session_state.anim_step==0): st.session_state.anim_step-=1
with c2:
    if st.button("Next stage",disabled=st.session_state.anim_step==4): st.session_state.anim_step+=1
with c3:
    autoplay=st.toggle("Auto-play",value=False)
if autoplay:
    st.session_state.anim_step=(st.session_state.anim_step+1)%5
step=st.session_state.anim_step
st.progress((step+1)/5)
st.subheader(labels[step])
client_count=[3,10,10,10,10][step]
vm_count=([3,3,3,7,7] if mode=="Traditional reactive" else [3,3,7,7,7])[step]
if mode=="Traditional reactive":
    detail=["Clients send a steady stream of requests.","A sudden surge arrives before the autoscaler reacts.","The monitoring threshold detects high utilization; requests queue or experience pressure.","The reactive controller provisions additional VMs after observing the spike.","The expanded fleet handles the increased request volume."]
else:
    detail=["The system observes the recent workload history.","The model identifies an upcoming increase in demand.","The autoscaler acts on the forecast and provisions capacity ahead of the spike.","Additional VMs are ready when the client surge arrives.","The expanded fleet serves the surge with less reactive delay."]
st.info(detail[step])
st.markdown("#### Client requests")
cols=st.columns(10)
for i,col in enumerate(cols):
    with col: st.markdown("👤" if i<client_count else "　")
st.markdown("#### Active virtual machines (illustrative)")
cols=st.columns(7)
for i,col in enumerate(cols):
    with col:
        st.markdown("☁️" if i<vm_count else "▫️")
st.caption(f"Illustrative stage {step+1} of 5 • {client_count} client icons • {vm_count} VM icons")
if autoplay:
    time.sleep(1.0)
    st.rerun()
