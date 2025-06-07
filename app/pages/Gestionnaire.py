import streamlit as st


if 'username' in st.session_state and 'role' in st.session_state:
    st.title(f"Bienvenue {st.session_state['username']} ({st.session_state['role']})")
else:
    st.error("⚠️ Vous n'êtes pas connecté.")
    st.stop()