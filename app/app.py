import streamlit as st
import time
import pyodbc

def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DB_Inscription;'
        'Trusted_Connection=yes;'
    )

def verifier_connexion(username, mot_de_passe,role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT u.nom,u.username, r.nom_role FROM utilisateurs u JOIN roles r ON u.id_role = r.id_role WHERE username = ? AND mot_de_passe = ?", (username, mot_de_passe))
    user = cursor.fetchone()
    conn.close()
    return user
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

"""with st.container(border=True):
    st.title("🔐 Page de connexion")

    nom = st.text_input("Nom",placeholder="Entrer votre nom")
    mot_de_passe = st.text_input("Mot de passe", type="password",placeholder="Entrer votre mot de passe")
    role = st.selectbox("Rôle", ["Gestionnaire", "Administrateur"], index=None, placeholder="Choisissez un rôle...")


    if st.button("Valider",use_container_width=True):
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
                st.switch_page("pages/Administrateur.py")"""
with st.container:
    st.title("🔐 Page de connexion")

    username = st.text_input("Nom d'utilisateur", placeholder="Entrer votre nom d'utilisateur")
    mot_de_passe = st.text_input("Mot de passe", type="password", placeholder="Entrer votre mot de passe")
    role = st.selectbox("Rôle", ["Gestionnaire", "Administrateur"], index=None, placeholder="Choisissez un rôle...")

    if st.button("Valider", use_container_width=True):
        if not username.strip():
            st.error("❌ Veuillez saisir votre nom d'utilisateur")
        elif len(mot_de_passe.strip()) < 8:
            st.error("❌ Le mot de passe doit contenir au moins 8 caractères")
        elif not role:
            st.warning("⚠️ Veuillez sélectionner un rôle")
        else:
            with st.spinner("Connexion en cours..."):
                time.sleep(1.5)
            if verifier_connexion(username.strip(), mot_de_passe.strip(), role):
                st.session_state['username'] = username.strip()
                st.session_state['role'] = role

                st.toast("✅ Connexion réussie", icon="🎉")
                time.sleep(1)

                if role == "Gestionnaire":
                    st.switch_page("Gestionnaire")  # sans extension ni dossier (car pages/Gestionnaire.py)
                elif role == "Administrateur":
                    st.switch_page("Administrateur")
            else:
                st.error("❌ Nom d'utilisateur, mot de passe ou rôle incorrect")
