import streamlit as st

tableau_url = "https://public.tableau.com/views/Classeur2_17339303305480/Tableaudebord1?:language=fr-FR&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"

# Intégrer le tableau dans Streamlit via une iframe
st.write("### Tableau Public intégré dans Streamlit")
st.components.v1.html(f"""
    <iframe src="{tableau_url}?:embed=yes&:showVizHome=no" width="100%" height="700px" frameborder="0"></iframe>
""", height=750, width=1800)

st.write("Si l'affichage est difficile à lire ou incomplet, cliquez sur le lien ci-dessus : 'Afficher dans tableau public'")

