import streamlit as st
import numpy as np
import pandas as pd

def page2():
    st.title("Second page")

pg = st.navigation([
    st.Page("pages/page1.py", title="Accueil", icon=":material/home:"),
    st.Page(page2, title="Second page", icon=":material/thumb_up:"),
])
pg.run()