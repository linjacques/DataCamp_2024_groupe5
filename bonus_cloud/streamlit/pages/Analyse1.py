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

    df = st.session_state["dataframe"]  

    # Barre des filtres
    st.subheader("Filtres dynamiques")
    selected_columns = st.multiselect(
        "Sélectionnez les colonnes pour filtrer les données", 
        df.columns
    )

    # dictionnaire de filtres dynamiques
    filtre = {}
    for col in selected_columns:

        # Colonne catégorielle
        if df[col].dtype == "object":  
            # Gestion des valeurs concaténées (exemple : "Action, Aventure")
            all_values = df[col].dropna().str.split(",").explode().str.strip().unique()
            selected_values = st.multiselect(f"Valeurs pour la colonne '{col}'", all_values)
            if selected_values:
                filtre[col] = selected_values
       
        # Colonne numérique
        else:  
            min_val, max_val = st.slider(
                f"Plage pour la colonne '{col}'",
                float(df[col].min()), 
                float(df[col].max()), 
                (float(df[col].min()), float(df[col].max()))
            )
            filtre[col] = (min_val, max_val)

     # Filtrer les données en fonction des sélections
    if filtre:
        df_filtre = df.copy()
        for col, condition in filtre.items():

            # Plage de valeurs (colonnes numériques)
            if isinstance(condition, tuple):  
                df_filtre = df_filtre[(df_filtre[col] >= condition[0]) & (df_filtre[col] <= condition[1])]
           
            # Valeurs spécifiques (colonnes catégorielles)
            else:  
                 # Filtrer les colonnes concaténées
                df_filtre = df_filtre[
                    df_filtre[col]
                    .apply(lambda x: any(value in x.split(", ") for value in condition) if pd.notnull(x) else False)
                ]

        st.subheader("Données filtrées")
        st.write(df_filtre)
        st.write(f"**Nombre de lignes après filtrage :** {len(df_filtre)}")
    else:
        st.info("Aucun filtre appliqué. Affichage des données originales.")
        st.dataframe(df)
else:
    st.warning("Aucun fichier chargé. Veuillez d'abord charger un fichier dans la page **Exploration de fichier csv**.")


