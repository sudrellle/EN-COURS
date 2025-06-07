import streamlit as st
import time

st.title('🔐 Page de connexion')
with st.container(border=True):
    st.markdown("""
        <div style="
            background-color: #f0f8ff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        ">
            <h2 style="text-align:center;">Page de Connexion</h2>
        </div>
    """,
    unsafe_allow_html=True)
    
    
    
    nom=st.text_input(label='Nom',placeholder='Entrer votre nom')
    Mot_de_passe=st.text_input(label='Mot de passe',placeholder='Entrer votre Mot de passe',type='password')
    option=st.selectbox("Role",
    ["Gestionnaire","Administrateur"],
    index=None,
    placeholder="Choisissez votre role...",
)

    gauche,droit=st.columns(2)
    validation=gauche.button('valider',use_container_width=True,icon=':material/login:')
    
    oubli=droit.button('Mot de passe oublié',use_container_width=True,icon=":material/password:")

    if validation:
    # Vérification du nom
        if not nom.strip():
            st.error('❌ Veuillez saisir votre nom')
        
        # Vérification du mot de passe
        elif len(Mot_de_passe.strip()) < 8:
            st.error("❌ Le mot de passe doit contenir au moins 8 caractères.")
        
        # Vérification du rôle
        elif not option:
            st.warning("⚠️ Veuillez sélectionner un rôle.")

        else:
            with st.spinner("🔄 Connexion en cours..."):
                time.sleep(1.5)

            st.toast("✅ Connexion réussie", icon="🎉")

            time.sleep(1)

            if option == "Gestionnaire":
                st.switch_page("./pages/Gestionnaire.py")
            elif option == "Administrateur":
                st.switch_page("Administrateur")
