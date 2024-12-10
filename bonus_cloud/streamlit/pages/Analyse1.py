import streamlit as st

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
        if df[col].dtype == "object":  # Colonne catégorielle
            options = st.multiselect(f"Valeurs pour la colonne '{col}'", df[col].unique())
            if options:
                filters[col] = options
        else:  # Colonne numérique
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
                filtered_df = filtered_df[filtered_df[col].isin(condition)]

        st.subheader("Données filtrées")
        st.write(filtered_df)
        st.write(f"**Nombre de lignes après filtrage :** {len(filtered_df)}")
    else:
        st.info("Aucun filtre appliqué. Affichage des données originales.")
        st.dataframe(df)
else:
    st.warning("Aucun fichier chargé. Veuillez d'abord charger un fichier dans la page **Exploration de fichier csv**.")


