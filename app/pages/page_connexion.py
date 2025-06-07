import streamlit as st
import time

st.title('🔐 Page de connexion')
with st.container(border=True):
    
    
    
    
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
                st.switch_page("Gestionnaire")
            elif option == "Administrateur":
                st.switch_page("Administrateur")
