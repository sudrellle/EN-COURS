import streamlit as st
import pyodbc
st.set_page_config(page_title="Gestionnaire", layout="wide")  # Ajout possible mais facultatif
st.title("Gestionnaire")  # <<< Ce titre doit être celui utilisé dans switch_page

if 'username' in st.session_state and 'role' in st.session_state:
    st.subheader(f"Bienvenue {st.session_state['username']} ({st.session_state['role']})")
else:
    st.error("⚠️ Vous n'êtes pas connecté.")
    st.stop()



def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DB_Inscription;'
        'Trusted_Connection=yes;'
    )
