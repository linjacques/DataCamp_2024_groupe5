import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Analyse des Sentiments")

# Chemin vers le fichier de sortie
output_file_path = os.path.join("output", "sentiments_resultat.csv")

if os.path.exists(output_file_path):
    # Charger le fichier CSV depuis le répertoire output
    df = pd.read_csv(output_file_path, delimiter=';', encoding='latin1')

    # Vérifiez si les colonnes nécessaires existent dans le DataFrame
    if all(col in df.columns for col in ['Genre 1', 'proba_nega', 'proba_neutre', 'proba_positif']):
        # Ajouter une colonne pour le sentiment dominant
        def sentiment_dominant(row):
            sentiments = {
                'Négatif': row['proba_nega'],
                'Neutre': row['proba_neutre'],
                'Positif': row['proba_positif']
            }
            return max(sentiments, key=sentiments.get)

        df['Sentiment'] = df.apply(sentiment_dominant, axis=1)

        # Grouper les données par genre et sentiment (en prenant uniquement les valeurs dominantes)
        sentiment_counts = df.groupby(['Genre 1', 'Sentiment']).size().reset_index(name='Nombre')

        # Calculer les pourcentages
        sentiment_counts['Pourcentage'] = sentiment_counts.groupby('Genre 1')['Nombre'].transform(lambda x: 100 * x / x.sum())

        st.write("### Répartition des Sentiments par Genre")

        # Assurez-vous que la colonne Genre 1 n'est pas vide
        if df['Genre 1'].dropna().nunique() > 0:
            genre = st.selectbox("Sélectionnez un genre pour voir la répartition des sentiments :", df['Genre 1'].dropna().unique())

            # Filtrer les données pour le genre sélectionné
            filtered_data = sentiment_counts[sentiment_counts['Genre 1'] == genre]

            if not filtered_data.empty:
                # Créer le graphique en camembert
                fig = px.pie(
                    filtered_data,
                    values='Pourcentage',
                    names='Sentiment',
                    title=f"Répartition des Sentiments pour le Genre : {genre}",
                    color='Sentiment',
                    color_discrete_map={'Positif': 'green', 'Neutre': 'blue', 'Négatif': 'red'}
                )
                fig.update_traces(textinfo='percent+label', pull=[0.1 if s == 'Positif' else 0 for s in filtered_data['Sentiment']])

                # Afficher le graphique
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Aucune donnée disponible pour le genre sélectionné : {genre}")
        else:
            st.error("Aucune donnée disponible pour les genres.")
    else:
        st.error("Les colonnes nécessaires pour l'analyse des sentiments ('Genre 1', 'proba_nega', 'proba_neutre', 'proba_positif') sont manquantes dans le fichier.")
else:
    st.error(f"Le fichier {output_file_path} est introuvable. Veuillez exécuter l'analyse des sentiments pour générer ce fichier.")
