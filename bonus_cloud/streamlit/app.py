import streamlit as st


Page_accueil = st.Page(
    page= "pages/Accueil.py",
    title= "Accueil",
    default=True   # indique que c'est la page par défaut = page d'accueil ! 

)

Page_dashboard1 = st.Page(
    page= "pages/dashboard1.py",
    title= "Exploration de fichier csv",
)

Page_dashboard2 = st.Page(
    page= "pages/dashboard2.py",
    title= "Analyse avec Streamlit",
)

Page_Analyse = st.Page(
    page="pages/Analyse1.py",
    title="Filtrer son dataset",

)


Page_dashboardNoam = st.Page(
    page= "pages/dashboardNoam.py",
    title= "Dashboard Noam",
)

Page_Analyse1 = st.Page(
    page= "pages/Analyse1.py",
    title= "Filtrer son dataset",
)

Page_Tableau = st.Page(
    page= "pages/tableautest.py",
    title= "Tableau",
)

# NavBarr

NavBarr = st.navigation(pages=[Page_accueil, Page_dashboard1, Page_PyGWalker, Page_Analyse1, Page_Tableau])
NavBarr.run()