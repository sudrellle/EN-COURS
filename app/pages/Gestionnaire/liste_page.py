import streamlit as st
import pyodbc
import streamlit as st
import pandas as pd
def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DB_Inscription;'
        'Trusted_Connection=yes;'
    )
def affichage_cycle(cycle):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        select libelle from repartition_classe
        WHERE nom_cycle = ? 
    """, (cycle))
    liste_cycle = cursor.fetchall()
    conn.close()
    return liste_cycle
st.set_page_config(page_title="Gestionnaire")  
st.title("Gestionnaire")  



if 'username' in st.session_state and 'role' in st.session_state:
    color=st.color_picker("Pick A Color", "#00f900")
    st.expander(color,expanded=True)
    

    
    st.subheader(f"Bienvenue {st.session_state['username']} ({st.session_state['role']})")
    with st.form("my_form"):
        st.write("Inscription")
        col1,col2=st.columns(2)
        nom=col1.text_input(label='Nom',placeholder="Entrer le nom de l'eleve")
        prenom=col2.text_input(label='Prenom',placeholder='Entrer le prenom')
        col3,col4=st.columns(2)
        date_naissance=col3.date_input(label='Date de naissance')
        lieu_naissance=col4.text_input(label='Lieu de naissance',placeholder='Ex:Brazzaville')
        col5,col6=st.columns(2)
        cycles=col5.selectbox('Choisissez votre cycle',['prescolaire','primaire','collège','lycée'],index=None)
        if cycles:
            affichage_cycle("primaire")

            st.write("affichage",affichage_cycle(cycles))
            
        classe=col6.selectbox('Choisissez la classe',['p1','p2'],index=None)
        genre = st.radio(
        "Genre",
        [":rainbow[Masculin]", ":rainbow[Feminin]"],horizontal=True
        )
        st.divider()
        st.write('information du tuteur')
        
        col7,col8=st.columns(2)
        nom_tuteur=col7.text_input(label='Nom',placeholder="Entrer le nom du tuteur")
        prenom_tuteur=col8.text_input(label='Prenom',placeholder='Entrer du tuteur')
        col9,col10=st.columns(2)
        profession=col9.text_input(label='Profession',placeholder='Medecin')
        contact=col10.number_input(label="Contact",max_value=9,placeholder='0695220532')
        statut=st.radio('Statut du tuteur',['parent','Responsable familiale','tuteur legale'])

        checkbox_val = st.checkbox("Form checkbox")
            
        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            st.toast('Enregistrement valideé')

else:
    st.error("⚠️ Vous n'êtes pas connecté.")
    st.stop()



