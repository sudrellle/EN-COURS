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
    st.header('Line chart')

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    
    dataframe,line_chart=st.tabs(['dataframe','line_chart'])
    with dataframe:
        st.write('voici le dataframe',chart_data)
    with line_chart : 
       
      st.line_chart(chart_data)
    
pg = st.navigation([
    st.Page("pages/page1.py", title="Accueil", icon=":material/home:"),
    st.Page(page2, title="Second page", icon=":material/thumb_up:"),
])
pg.run()

  """if validation:
        if len(Mot_de_passe)<8:
            st.markdown("""
            <div style='color: red; font-weight: bold;'>
                #❌ Le mot de passe doit contenir au moins 8 caractères.
            </div>
            """, unsafe_allow_html=True)
          
        else:
            progress_text = "chargement de la page."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            st.empty()"""


                