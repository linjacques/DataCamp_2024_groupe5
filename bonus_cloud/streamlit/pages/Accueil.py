import streamlit as st

st.title("Accueil")
st.write("Bienvenue sur notre application Streamlit !")
st.write("Vous pouvez naviguer entre les différentes pages grâce à la barre de navigation sur la gauche.")

st.write("### Objectif du projet")
st.write("L'objectif de ce projet est de mettre en pratique les concepts de Streamlit et de Data Science en analysant un jeu de données de films. A partir de données recuprérées sur Allociné à partir du scrapping, nous allons explorer les différentes fonctionnalités de Streamlit pour visualiser et analyser ces données.")

st.write("### Pages disponibles")
st.write("1. **Exploration de fichier csv** : Explorez les données brutes du fichier CSV ainsi que quelques détails sur le fichier.")
st.write("2. **Dashboard Noam** : Visualisez des statistiques sur les films à partir de Streamlit.")
st.write("3. **Filtrer son dataset** : Filtrer les données selon des critères spécifiques.")
st.write("4. **Tableau** : Intégration d'un tableau de bord Tableau Public.")
st.write("5. **Analyse des sentiments par commentaire** : Analysez les sentiments des commentaires des films.")
