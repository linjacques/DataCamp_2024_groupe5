import streamlit as st


Page_accueil = st.Page(
    page= "pages/Accueil.py",
    title= "Accueil",
    default=True 

)
Page_dashboard1 = st.Page(
    page= "pages/dashboard1.py",
    title= "Exploration de fichier csv",
)
Page_Analyse = st.Page(
    page="pages/Analyse1.py",
    title="Filtrer son dataset",

)

Page_dashboard = st.Page(
    page= "pages/dashboard.py",
    title= "Dashboard",
)

Page_Analyse1 = st.Page(
    page= "pages/Analyse1.py",
    title= "Filtrer son dataset",
)

Page_Tableau = st.Page(
    page= "pages/tableautest.py",
    title= "Tableau",
)

Page_Sentiment = st.Page(
    page= "pages/sentiment.py",
    title="Analyse des sentiments par commentaire"
)

# NavBarr

NavBarr = st.navigation(pages=[Page_accueil, Page_dashboard1, Page_dashboard, Page_Analyse1, Page_Tableau, Page_Sentiment])
NavBarr.run()