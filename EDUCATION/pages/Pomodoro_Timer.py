import streamlit as st
import time


st.title("The Pomodoro App (Let's do some focused study work)")

button_clicked = st.button("Start")

t1 = 1500
t2 = 300

if button_clicked:
    with st.empty():
        while t1:
            mins,secs = divmod(t1,60)
            timer = '{:02d}:{:02d}'.format(mins,secs)
            st.header(f"⏳{timer}")
            time.sleep(1)
            t1 -= 1
            st.success("🔔 25 minutes is over ! Time for a break!")
    with st.empty():
        while t2:
            mins2,secs2 = divmod(t2,60)
            timer2 = '{:02d}:{:02d}'.format(mins2,secs2)
            st.header(f"⏳{timer2}")
            time.sleep(1)
            t2 -= 1
            st.error("⏰ 5 minute break is over!")     
