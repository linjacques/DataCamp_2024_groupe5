import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Analyse avec StreamLit")

if "dataframe" in st.session_state:
    df = st.session_state["dataframe"]

    # Ajouter des filtres
    st.sidebar.title("Filtres")
    df_filtre = df.copy()

    # Filtrer par genre
    if 'Genre 1' in df.columns:
        genres = st.sidebar.multiselect("Filtrer par Genre", options=df_filtre['Genre 1'].dropna().unique())
        if genres:
            df_filtre = df_filtre[df_filtre['Genre 1'].isin(genres)]

    # Filtrer par date
    if 'Date' in df.columns:
        df_filtre['Date'] = pd.to_datetime(df_filtre['Date'], errors='coerce')
        min_date, max_date = st.sidebar.slider("Filtrer par Date", 
                                               value=(df_filtre['Date'].min(), df_filtre['Date'].max()), 
                                               format="YYYY-MM-DD")
        df_filtre = df_filtre[(df_filtre['Date'] >= min_date) & (df_filtre['Date'] <= max_date)]

    # Vérification des données avant calcul de la Moyenne
    if 'Genre 1' in df_filtre.columns and 'Note' in df_filtre.columns:
        df_filtre['Note'] = pd.to_numeric(df_filtre['Note'], errors='coerce', downcast='float')  # Convertir les notes en numérique

 
        # Calculer la Moyenne des notes par genre
        medianne_des_notes_par_genre = df_filtre.groupby('Genre 1')['Note'].mean().sort_values(ascending=False)

        st.write("### Moyenne des Notes par Genre")
        fig_median_genre = px.bar(
            medianne_des_notes_par_genre, 
            x=medianne_des_notes_par_genre.index, 
            y=medianne_des_notes_par_genre.values, 
            labels={'x': 'Genre', 'y': 'Moyenne des Notes'},
            title="Genres de Films avec les Meilleures Notes",
            text_auto='.2f'  # Affiche les virgules avec deux décimales
        )
        fig_median_genre.update_layout(
            xaxis_tickangle=-45,
            xaxis_title="Genre",
            yaxis_title="Moyenne des Notes",
            coloraxis_showscale=True,
            title_font_size=18
        )
        st.plotly_chart(fig_median_genre)

    # Télécharger le fichier mis à jour
    csv = df_filtre.to_csv(index=False)
    st.download_button(
        label="Télécharger le CSV",
        data=csv,
        file_name="data_export.csv",
        mime="text/csv"
    )
else:
    st.warning("Aucun fichier chargé. Veuillez d'abord charger un fichier dans la page **Exploration de fichier csv**.")
