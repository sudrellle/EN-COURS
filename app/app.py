import streamlit as st
import numpy as np
import pandas as pd
import time
def page2():
    st.title("Second page")
    st.header('st.slider')
    st.subheader('Slider')
    age=st.slider('Quel age as tu?',0,100,25)
    st.write('j\'ai',age,'ans')
    values = st.slider(
     'Select a range of values',
     0.0, 100.0, (25.0, 75.0))
    st.write('Values:', values)
    st.subheader('Range time slider')

    appointment = st.slider(
        "Schedule your appointment:",
        value=(time(11, 30), time(12, 45)))
    st.write("You're scheduled for:", appointment)

    # Example 4

    st.subheader('Datetime slider')

    start_time = st.slider(
        "When do you start?",
        value=datetime(2020, 1, 1, 9, 30),
        format="MM/DD/YY - hh:mm")
    st.write("Start time:", start_time)


pg = st.navigation([
    st.Page("pages/page1.py", title="Accueil", icon=":material/home:"),
    st.Page(page2, title="Second page", icon=":material/thumb_up:"),
])
pg.run()