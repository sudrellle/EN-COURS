import streamlit as st

with st.container:
    st.title('Page de connexion')
    
    nom=st.text_input(label='Nom',value='ruth',placeholder='Entrer votre nom')
    nom=st.text_input(label='Mot de passe',value='ruth',placeholder='Entrer votre nom')
    st.write('Nom',nom)
    gauche,droit=st.columns(2,vertical_alignment=True,border=True)
    gauche.button('valider',use_container_width=True,icon=':material/:')
    st.selectbox(options=['Gestionnaire','Administrateur'])
    droit.button('Mot de passe oublié',icon=":material/password:")