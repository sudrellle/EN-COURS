import streamlit as st
import numpy as np
import pandas as pd

def page2():
    st.title("Second page")
    st.header('st.slider')
    st.subheader('Slider')
    age=st.slider('Quel age as tu?',0,100,25)
    st.write('j\'ai',age,'ans')

pg = st.navigation([
    st.Page("pages/page1.py", title="Accueil", icon=":material/home:"),
    st.Page(page2, title="Second page", icon=":material/thumb_up:"),
])
pg.run()