import streamlit as st
import pyodbc
import time

# Connexion SQL Server
def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DB_Inscription;'
        'Trusted_Connection=yes;'
    )

# Vérification des identifiants
def verifier_connexion(username, mot_de_passe, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.nom, u.username, r.nom_role
        FROM utilisateurs u
        JOIN roles r ON u.id_role = r.id_role
        WHERE u.username = ? AND u.mot_de_passe = ? AND r.nom_role = ?
    """, (username, mot_de_passe, role))
    user = cursor.fetchone()
    conn.close()
    return user

# Suppression de la sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }

        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 2rem;
            background-color: #f8f9fa;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .stTextInput > div > input, .stSelectbox > div {
            border-radius: 10px;
            padding: 0.6rem;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Titre/logo
st.markdown("<h2 style='text-align: center;'>🔐 Connexion sécurisée</h2>", unsafe_allow_html=True)
# st.image("logo.png", width=100)  # Si tu veux ajouter un logo

with st.container():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    username = st.text_input("👤 Nom d'utilisateur", placeholder="Ex : gesti001")
    mot_de_passe = st.text_input("🔑 Mot de passe", type="password", placeholder="Au moins 8 caractères")
    role = st.selectbox("🎭 Rôle", ["Gestionnaire", "Administrateur"], index=None, placeholder="Choisissez un rôle...")

    col1, col2 = st.columns(2)
    valider = col1.button('✅ Valider', use_container_width=True)
    verification = col2.button('🔍 Vérifier', use_container_width=True)

    if valider:
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
                    st.switch_page("pages/Gestionnaire.py")
                elif role == "Administrateur":
                    st.switch_page("pages/Administrateur.py")
            else:
                st.error("❌ Identifiants ou rôle incorrects")

    elif verification:
        st.switch_page("pages/Gestionnaire.py")

    st.markdown('</div>', unsafe_allow_html=True)
