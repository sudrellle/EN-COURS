import streamlit as st
import pyodbc
import pandas as pd
from datetime import datetime

def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DB_Inscription;'
        'Trusted_Connection=yes;'
    )

@st.cache_data(ttl=300)
def get_classes_by_cycle(cycle):
    """Récupère les classes disponibles pour un cycle donné"""
    if not cycle:
        return []
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT libelle FROM repartition_classe
            WHERE nom_cycle = ?
            ORDER BY libelle
        """, (cycle,))
        classes = cursor.fetchall()
        conn.close()
        return [row[0] for row in classes]
    except Exception as e:
        st.error(f"Erreur lors de la récupération des classes: {str(e)}")
        return []

@st.cache_data(ttl=300)
def get_all_cycles():
    """Récupère tous les cycles disponibles"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT nom_cycle FROM repartition_classe
            ORDER BY nom_cycle
        """)
        cycles = cursor.fetchall()
        conn.close()
        return [row[0] for row in cycles]
    except Exception as e:
        st.error(f"Erreur lors de la récupération des cycles: {str(e)}")
        return ['prescolaire', 'primaire', 'collège', 'lycée']

def page_inscription():
    st.subheader("📝 Inscription des élèves")
    
    # Section pour la sélection cycle/classe
    st.write("**Sélection Cycle et Classe**")
    col_cycle, col_classe = st.columns(2)
    
    with col_cycle:
        cycles_disponibles = get_all_cycles()
        cycle_selectionne = st.selectbox(
            '🎓 Choisissez le cycle', 
            options=[''] + cycles_disponibles,
            index=0,
            key="cycle_select"
        )
    
    with col_classe:
        if cycle_selectionne:
            classes_disponibles = get_classes_by_cycle(cycle_selectionne)
            
            if classes_disponibles:
                classe_selectionnee = st.selectbox(
                    f'📚 Classes disponibles pour {cycle_selectionne}',
                    options=[''] + classes_disponibles,
                    index=0,
                    key="classe_select"
                )
                st.info(f"✅ {len(classes_disponibles)} classe(s) trouvée(s) pour le cycle {cycle_selectionne}")
            else:
                st.selectbox(
                    '📚 Choisissez la classe',
                    options=['Aucune classe disponible'],
                    disabled=True,
                    key="classe_select_disabled"
                )
                st.warning(f"⚠️ Aucune classe trouvée pour le cycle {cycle_selectionne}")
        else:
            st.selectbox(
                '📚 Choisissez d\'abord un cycle',
                options=['Sélectionnez d\'abord un cycle'],
                disabled=True,
                key="classe_select_empty"
            )
    
    # Formulaire principal
    with st.form("inscription_form"):
        st.write("**👨‍🎓 Informations de l'élève**")
        
        col1, col2 = st.columns(2)
        nom = col1.text_input('Nom *', placeholder="Entrer le nom de l'élève")
        prenom = col2.text_input('Prénom *', placeholder='Entrer le prénom')
        
        col3, col4 = st.columns(2)
        date_naissance = col3.date_input('📅 Date de naissance *')
        lieu_naissance = col4.text_input('📍 Lieu de naissance', placeholder='Ex: Pointe-Noire, Brazzaville')
        
        cycle_form = cycle_selectionne if cycle_selectionne else None
        classe_form = classe_selectionnee if cycle_selectionne and classe_selectionnee else None
        
        col5, col6 = st.columns(2)
        col5.text_input("🎓 Cycle sélectionné", value=cycle_form or "Non sélectionné", disabled=True)
        col6.text_input("📚 Classe sélectionnée", value=classe_form or "Non sélectionnée", disabled=True)
        
        genre = st.radio("⚧ Genre *", [":blue[👨 Masculin]", ":pink[👩 Féminin]"], horizontal=True)
        
        st.divider()
        st.write('**👨‍👩‍👧‍👦 Informations du tuteur**')
        
        col7, col8 = st.columns(2)
        nom_tuteur = col7.text_input('Nom du tuteur *', placeholder="Entrer le nom du tuteur")
        prenom_tuteur = col8.text_input('Prénom du tuteur *', placeholder='Entrer le prénom du tuteur')
        
        col9, col10 = st.columns(2)
        profession = col9.text_input('💼 Profession', placeholder='Ex: Médecin, Enseignant, Commerçant')
        contact = col10.text_input("📞 Contact *", placeholder='Ex: 066-123-45-67')
        
        statut = st.radio('👨‍👩‍👧‍👦 Statut du tuteur *', 
                         ['👨‍👩‍👧‍👦 Parent', '👨‍👨‍👧‍👦 Responsable familial', '⚖️ Tuteur légal'])
        
        st.divider()
        st.write("**💰 Frais d'inscription**")
        
        # Définition des frais selon le cycle
        frais_inscription = {
            'prescolaire': 50000,
            'primaire': 75000,
            'collège': 100000,
            'lycée': 125000
        }
        
        montant = frais_inscription.get(cycle_selectionne.lower(), 0) if cycle_selectionne else 0
        st.info(f"Montant des frais d'inscription pour {cycle_selectionne}: {montant:,} FCFA")
        
        submitted = st.form_submit_button("✅ Enregistrer l'inscription", use_container_width=True, type="primary")
        
        if submitted:
            erreurs = []
            
            if not nom.strip(): erreurs.append("Le nom de l'élève est requis")
            if not prenom.strip(): erreurs.append("Le prénom de l'élève est requis")
            if not cycle_form: erreurs.append("Veuillez sélectionner un cycle")
            if not classe_form: erreurs.append("Veuillez sélectionner une classe")
            if not nom_tuteur.strip(): erreurs.append("Le nom du tuteur est requis")
            if not prenom_tuteur.strip(): erreurs.append("Le prénom du tuteur est requis")
            if not contact.strip(): erreurs.append("Le contact du tuteur est requis")
            
            if erreurs:
                st.error("⚠️ Erreurs détectées:")
                for erreur in erreurs:
                    st.write(f"• {erreur}")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    
                    # 1. Insertion dans la table tuteur
                    cursor.execute("""
                        INSERT INTO tuteur (nom, prenom, profession, contact)
                        VALUES (?, ?, ?, ?)
                    """, (nom_tuteur.strip().upper(), prenom_tuteur.strip().title(), 
                          profession.strip().title(), contact.strip()))
                    id_tuteur = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
                    
                    # 2. Insertion dans la table eleves
                    genre_value = 'Masculin' if 'Masculin' in genre else 'Féminin'
                    cursor.execute("""
                        INSERT INTO eleves (nom, prenom, date_naissance, lieu_naissance, genre)
                        VALUES (?, ?, ?, ?, ?)
                    """, (nom.strip().upper(), prenom.strip().title(), 
                          date_naissance, lieu_naissance.strip().title(), genre_value))
                    id_eleve = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
                    
                    # 3. Insertion dans la table eleve_tuteur
                    statut_value = statut.split()[1]  # Parent, Responsable, Tuteur
                    cursor.execute("SELECT statut_id FROM statut WHERE nom = ?", (statut_value,))
                    statut_id = cursor.fetchone()[0]
                    
                    cursor.execute("""
                        INSERT INTO eleve_tuteur (id_eleve, id_tuteur, statut_id, actif)
                        VALUES (?, ?, ?, 1)
                    """, (id_eleve, id_tuteur, statut_id))
                    
                    # 4. Insertion dans la table inscription
                    annee_academique = f"{datetime.now().year}-{datetime.now().year + 1}"
                    cursor.execute("""
                        INSERT INTO inscription (id_eleve, cycle, classe, montant, annee_academique, date_inscription)
                        VALUES (?, ?, ?, ?, ?, GETDATE())
                    """, (id_eleve, cycle_form, classe_form, montant, annee_academique))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("✅ Inscription enregistrée avec succès!")
                    st.balloons()
                    
                    # Récapitulatif
                    with st.expander("📋 Récapitulatif de l'inscription", expanded=True):
                        col_recap1, col_recap2 = st.columns(2)
                        
                        with col_recap1:
                            st.write("**👨‍🎓 Élève:**")
                            st.write(f"• Nom: {nom.strip().upper()}")
                            st.write(f"• Prénom: {prenom.strip().title()}")
                            st.write(f"• Date de naissance: {date_naissance}")
                            st.write(f"• Lieu de naissance: {lieu_naissance.strip().title()}")
                            st.write(f"• Genre: {genre_value}")
                        
                        with col_recap2:
                            st.write("**👨‍👩‍👧‍👦 Tuteur:**")
                            st.write(f"• Nom: {nom_tuteur.strip().upper()}")
                            st.write(f"• Prénom: {prenom_tuteur.strip().title()}")
                            st.write(f"• Profession: {profession.strip().title()}")
                            st.write(f"• Contact: {contact.strip()}")
                            st.write(f"• Statut: {statut_value}")
                            st.write("**📚 Scolarité:**")
                            st.write(f"• Cycle: {cycle_form}")
                            st.write(f"• Classe: {classe_form}")
                            st.write(f"• Montant: {montant:,} FCFA")
                            st.write(f"• Année académique: {annee_academique}")
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'enregistrement: {str(e)}")
                    if 'conn' in locals():
                        conn.rollback()
                        conn.close()

def page_liste():
    st.subheader("📋 Liste des élèves")
    
    try:
        conn = get_connection()
        query = """
            SELECT e.id, e.nom, e.prenom, e.date_nais, e.genre, 
                   cla.libelle, c.libelle, a.libelle,
                   t.nom AS nom_tuteur, t.contact
            FROM eleves e
            JOIN inscription i ON e.id = i.id_eleve
            join classe cla on i.id_classe=cla.id
            join cycle c on i.id_cycle=c.id
            join annee_academique a on a.id=i.id_anne
            JOIN eleve_tuteur et ON e.id = et.id_eleve
            JOIN tuteur t ON et.id_tuteur = t.id
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Boutons d'action
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Exporter CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button("Télécharger CSV", csv, "eleves.csv", "text/csv")
            
            with col2:
                if st.button("🔄 Actualiser"):
                    st.rerun()
                    
        else:
            st.info("📝 Aucun élève trouvé dans la base de données")
            
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {str(e)}")

# Configuration de la page
st.set_page_config(
    page_title="Gestionnaire", 
    page_icon="👨‍💼",
    layout="wide"
)

# Vérification de l'authentification
if 'username' not in st.session_state or 'role' not in st.session_state:
    st.error("⚠️ Vous n'êtes pas connecté.")
    st.stop()

# Interface principale
st.title("👨‍💼 Espace Gestionnaire")

# Personnalisation de l'interface
color = st.sidebar.color_picker("🎨 Couleur du thème", "#00f900")
st.markdown(f"""
<style>
    .stSelectbox > div > div > div > div {{
        background-color: {color}20;
    }}
</style>
""", unsafe_allow_html=True)

# Message de bienvenue
st.success(f"👋 Bienvenue {st.session_state['username']} ({st.session_state['role']})")

# Navigation par onglets
tab1, tab2 = st.tabs(["📝 Inscription", "📋 Liste des élèves"])

with tab1:
    page_inscription()

with tab2:
    page_liste()