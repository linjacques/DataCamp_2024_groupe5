import streamlit as st
import pandas as pd

st.title("Analyse dynamique des données")

    # Vérifier si un fichier a été chargé
if "dataframe" in st.session_state:

    st.markdown("""
    ### Instructions d'utilisation :
    **Appliquer des filtres dynamiques** :
      1. Pour les colonnes numériques, vous pouvez définir une plage de valeurs à l'aide d'un curseur.
      2. Pour les colonnes catégorielles, sélectionnez les valeurs spécifiques que vous souhaitez inclure dans votre analyse.
      3. Les résultats filtrés s'afficheront automatiquement, avec un aperçu des données et le nombre total de lignes correspondant aux critères.
    """)

    df = st.session_state["dataframe"]  # Récupérer le DataFrame
    #st.write(f"**Colonnes détectées :** {', '.join(df.columns)}")

    # Sélection des colonnes pour les filtres
    st.subheader("Filtres dynamiques")
    selected_columns = st.multiselect(
        "Sélectionnez les colonnes pour filtrer les données", 
        df.columns
    )

    # Créer un dictionnaire de filtres dynamiques
    filters = {}
    for col in selected_columns:

        # Colonne catégorielle
        if df[col].dtype == "object":  
            # Gestion des valeurs concaténées (exemple : "Action, Aventure")
            all_values = df[col].dropna().str.split(",").explode().str.strip().unique()
            selected_values = st.multiselect(f"Valeurs pour la colonne '{col}'", all_values)
            if selected_values:
                filters[col] = selected_values
       
        # Colonne numérique
        else:  
            min_val, max_val = st.slider(
                f"Plage pour la colonne '{col}'",
                float(df[col].min()), 
                float(df[col].max()), 
                (float(df[col].min()), float(df[col].max()))
            )
            filters[col] = (min_val, max_val)

     # Filtrer les données en fonction des sélections
    if filters:
        filtered_df = df.copy()
        for col, condition in filters.items():

            # Plage de valeurs (colonnes numériques)
            if isinstance(condition, tuple):  
                filtered_df = filtered_df[(filtered_df[col] >= condition[0]) & (filtered_df[col] <= condition[1])]
           
            # Valeurs spécifiques (colonnes catégorielles)
            else:  
                 # Filtrer les colonnes concaténées
                filtered_df = filtered_df[
                    filtered_df[col]
                    .apply(lambda x: any(value in x.split(", ") for value in condition) if pd.notnull(x) else False)
                ]

        st.subheader("Données filtrées")
        st.write(filtered_df)
        st.write(f"**Nombre de lignes après filtrage :** {len(filtered_df)}")
    else:
        st.info("Aucun filtre appliqué. Affichage des données originales.")
        st.dataframe(df)
else:
    st.warning("Aucun fichier chargé. Veuillez d'abord charger un fichier dans la page **Exploration de fichier csv**.")


