import streamlit as st
import numpy as np
import pandas as pd
import time
import datetime
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
    
pg = st.navigation([
    st.Page("pages/page1.py", title="Accueil", icon=":material/home:"),
    st.Page(page2, title="Second page", icon=":material/thumb_up:"),
])
pg.run()