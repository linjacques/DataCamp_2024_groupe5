import streamlit as st


Page_acceuil = st.Page(
    page= "pages/accueil.py",
    title= "accueil",
    default=True   # indique que c'est la page par défaut = page d'accueil ! 

)

Page_dashboard1 = st.Page(
    page= "pages/dashboard1.py",
    title= "Exploration des fichiers csv",
)

Page_PyGWalker = st.Page(
    page= "pages/pygwalker.py",
    title= "Dashboard PygWalker",
)

# NavBarr

NavBarr = st.navigation(pages=[Page_acceuil, Page_dashboard1, Page_PyGWalker])
NavBarr.run()