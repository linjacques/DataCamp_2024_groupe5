import streamlit as st


Page_acceuil = st.Page(
    page= "pages/Accueil.py",
    title= "Accueil",
    default=True   # indique que c'est la page par défaut = page d'accueil ! 

)

Page_dashboard1 = st.Page(
    page= "pages/dashboard1.py",
    title= "Exploration de fichier csv",
)

Page_Analyse = st.Page(
    page="pages/Analyse1.py",
    title="Filtrer son dataset",

)

Page_PyGWalker = st.Page(
    page= "pages/pygwalker.py",
    title= "Dashboard PygWalker",
)

Page_Analyse1 = st.Page(
    page= "pages/Analyse1.py",
    title= "Filtrer son dataset",
)

# NavBarr

NavBarr = st.navigation(pages=[Page_acceuil, Page_dashboard1, Page_PyGWalker, Page_Analyse1])
NavBarr.run()