import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Analyse dynamique des données",
    page_icon="📊",
    layout="wide"
)

# Titre principal stylisé
st.markdown(
    """
        <h1 style="color: #1a73e8; font-family: Arial, sans-serif; font-size: 2.5em;">
            📊 Analyse dynamique des données
        </h1>
    """,
    unsafe_allow_html=True
)

# Vérification si un fichier a été chargé
if "dataframe" in st.session_state:

    # Instructions d'utilisation stylisées
    st.markdown(
        """
            <h3 style="color: #4caf50; font-family: Arial, sans-serif;">
                ✅ Instructions d'utilisation :
            </h3>
            <ul style="font-size: 1.1em; line-height: 1.6;">
                <li><b>Appliquer des filtres dynamiques</b> :</li>
                <li>Pour les colonnes numériques, définissez une plage de valeurs à l'aide d'un curseur.</li>
                <li>Pour les colonnes catégorielles, sélectionnez les valeurs spécifiques à inclure.</li>
                <li>Les résultats filtrés s'afficheront automatiquement avec le nombre total de lignes correspondantes.</li>
            </ul>
        """,
        unsafe_allow_html=True
    )

    df = st.session_state["dataframe"]  # Chargement du DataFrame

    # Barre des filtres
    st.markdown(
        """
        <h2 style="color: #1a73e8; font-family: Arial, sans-serif;">
            🎯 Filtres dynamiques
        </h2>
        """,
        unsafe_allow_html=True
    )
    selected_columns = st.multiselect(
        "Sélectionnez les colonnes pour filtrer les données", 
        df.columns
    )

    # Dictionnaire de filtres dynamiques
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

        # Affichage des données filtrées
        st.markdown(
            """
            <h2 style="color: #1a73e8; font-family: Arial, sans-serif;">
                📋 Données filtrées
            </h2>
            """,
            unsafe_allow_html=True
        )
        st.write(df_filtre)
        st.write(
            f"<p style='font-size: 1.1em; color: #4caf50;'><b>Nombre de lignes après filtrage :</b> {len(df_filtre)}</p>",
            unsafe_allow_html=True
        )
    else:
        st.info("Aucun filtre appliqué. Affichage des données originales.")
        st.dataframe(df)

else:
    st.warning(
        """
        ⚠️ Aucun fichier chargé. Veuillez d'abord charger un fichier dans la page 
        **Exploration de fichier CSV**.
        """
    )
