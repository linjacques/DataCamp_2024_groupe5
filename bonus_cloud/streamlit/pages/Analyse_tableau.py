import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Intégration Tableau Public",
    page_icon="📊",
    layout="wide"
)

# URL du tableau
tableau_url = "https://public.tableau.com/views/Classeur2_17339303305480/Tableaudebord1?:language=fr-FR&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"

# Titre principal stylisé
st.markdown(
    """
        <h1 style="color: #1a73e8; font-family: Arial, sans-serif; font-size: 2.5em; margin: 0; text-align: center; ">
            📊 Tableau Public intégré dans Streamlit
        </h1>
    """,
    unsafe_allow_html=True
)

# Message explicatif
st.markdown(
    """
    <p style="font-size: 1.2em; text-align: center;">
        Ce tableau de bord interactif est intégré directement dans cette page. Vous pouvez explorer les données en temps réel.
    </p>
    """,
    unsafe_allow_html=True
)

# Intégration du tableau via iframe avec la taille originale
st.components.v1.html(f"""
    <iframe src="{tableau_url}?:embed=yes&:showVizHome=no" width="1800" height="700" frameborder="0" style="border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);"></iframe>
""", height=750, width=1800)

# Lien externe pour ouvrir dans Tableau Public
st.markdown(
    f"""
    <p style="font-size: 1.1em; text-align: center; margin-top: 20px;">
        Si l'affichage est difficile à lire ou incomplet, <a href="{tableau_url}" target="_blank" style="color: #1a73e8; text-decoration: none;"><strong>cliquez ici</strong></a> pour ouvrir le tableau dans une nouvelle fenêtre.
    </p>
    """,
    unsafe_allow_html=True
)
