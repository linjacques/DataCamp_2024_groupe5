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


# NavBarr

NavBarr = st.navigation(pages=[Page_acceuil, Page_dashboard1])
NavBarr.run()