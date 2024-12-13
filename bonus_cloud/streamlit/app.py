import streamlit as st


Page_accueil = st.Page(
    page= "pages/Accueil.py",
    title= "Accueil",
    default=True 
)

Page_Analyse_csv = st.Page(
    page="pages/Analyse_csv.py",
    title="Exploration Interactive des Données CSV",
)

Page_Analyse_notes = st.Page(
    page= "pages/Analyse_notes.py",
    title= "Analyse Visuelle des Notes : Tendances et Répartitions",
)

Page_Tableau = st.Page(
    page= "pages/Analyse_tableau.py",
    title= "Visualisation des Données avec Tableau ",
)

Page_Sentiment = st.Page(
    page= "pages/Analyse_sentiments.py",
    title="Analyse Automatisée des Sentiments avec Roberta"
)

Page_AnalyseMetier = st.Page(
    page= "pages/analyse_metier.py",
    title="Analyse des films"
)

# NavBarr
NavBarr = st.navigation ( pages = [
    Page_accueil, Page_Analyse_csv,Page_Analyse_notes,
    Page_Tableau, Page_Sentiment, Page_AnalyseMetier
] )

NavBarr.run()