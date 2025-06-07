import streamlit as st
import time
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

with st.container(border=True):
    st.title("🔐 Page de connexion")

    nom = st.text_input("Nom")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    role = st.selectbox("Rôle", ["Gestionnaire", "Administrateur"], index=None, placeholder="Choisissez un rôle...")

    if st.button("Valider"):
        if not nom.strip():
            st.error("❌ Veuillez saisir votre nom")
        elif len(mot_de_passe.strip()) < 8:
            st.error("❌ Le mot de passe doit contenir au moins 8 caractères")
        elif not role:
            st.warning("⚠️ Veuillez sélectionner un rôle")
        else:
            with st.spinner("Connexion en cours..."):
                time.sleep(1.5)
            st.toast("✅ Connexion réussie", icon="🎉")
            time.sleep(1)
            if role == "Gestionnaire":
                st.switch_page("pages/Gestionnaire.py")
            elif role == "Administrateur":
                st.switch_page("pages/Administrateur.py")
