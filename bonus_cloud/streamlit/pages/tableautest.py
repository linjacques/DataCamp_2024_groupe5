import streamlit as st

tableau_url = "https://public.tableau.com/views/Testtableauallocin/Feuille1?:language=fr-FR&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"

# Intégrer le tableau dans Streamlit via une iframe
st.write("### Tableau Public intégré dans Streamlit")
st.components.v1.html(f"""
    <iframe src="{tableau_url}?:embed=yes&:showVizHome=no" width="100%" height="650px" frameborder="0"></iframe>
""", height=1000)

