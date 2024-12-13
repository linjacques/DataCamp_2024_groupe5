import streamlit as st
import pandas as pd
import plotly.express as px
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Configuration de la page
st.set_page_config(
    page_title="Analyse des Sentiments et Avis",
    page_icon="😍",
    layout="wide"
)

# Titre principal stylisé
st.markdown(
    """
        <h1 style="color: #1a73e8; font-family: Arial, sans-serif; font-size: 2.5em; margin: 0; text-align: center; ">
            📊 Analyse des Sentiments et Avis
        </h1>
    """,
    unsafe_allow_html=True
)

# Charger le modèle et le tokenizer
@st.cache_resource
def load_model():
    model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# Zone de texte pour écrire un commentaire
st.markdown("<h2 style='color: #1a73e8;'>📝 Entrez un texte à analyser :</h2>", unsafe_allow_html=True)
user_input = st.text_area("", "")

if user_input:
    # Fonction pour analyser le sentiment
    def analyze_sentiment(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiment_scores = scores.detach().numpy()[0]
        
        proba_positif, proba_neutre, proba_nega = sentiment_scores
        return {
            "Négatif": proba_nega,
            "Neutre": proba_neutre,
            "Positif": proba_positif
        }

    # Analyser le texte de l'utilisateur
    sentiment_scores = analyze_sentiment(user_input)

    # Afficher un tableau des probabilités
    st.markdown("<h3 style='color: #1a73e8;'>🔢 Résultats de l'analyse :</h3>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([sentiment_scores]).T.rename(columns={0: "Probabilité"}))

    # Créer un graphique en camembert
    fig = px.pie(
        names=sentiment_scores.keys(),
        values=sentiment_scores.values(),
        title="Répartition des Sentiments",
        color_discrete_map={'Positif': 'green', 'Neutre': 'blue', 'Négatif': 'red'}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Veuillez entrer un texte ci-dessus pour analyser les sentiments.")

# Analyse des avis par catégorie de film
st.markdown("<h2 style='color: #1a73e8;'>🎥 Avis par catégorie de film</h2>", unsafe_allow_html=True)

# Chemin vers le fichier de sortie
output_file_path = os.path.join("output", "sentiments_resultat_bis.csv")

if os.path.exists(output_file_path):
    df = pd.read_csv(output_file_path, delimiter=';', encoding='latin1')

    if all(col in df.columns for col in ['Genre 1', 'proba_nega', 'proba_neutre', 'proba_positif']):
        # Ajouter une colonne pour le sentiment dominant
        def dominant_sentiment(row):
            sentiments = {
                'negatif': row['proba_nega'],
                'neutre': row['proba_neutre'],
                'positif': row['proba_positif']
            }
            return max(sentiments, key=sentiments.get)

        df['Sentiment'] = df.apply(dominant_sentiment, axis=1)

        # Grouper les données par genre et sentiment
        sentiment_counts = df.groupby(['Genre 1', 'Sentiment']).size().reset_index(name='Counts')
        sentiment_counts['Percentage'] = sentiment_counts.groupby('Genre 1')['Counts'].transform(lambda x: 100 * x / x.sum())

        st.markdown("<h3 style='color: #1a73e8;'>🌄 Répartition des Sentiments par Genre de film</h3>", unsafe_allow_html=True)

        genre = st.selectbox("Sélectionnez un genre pour voir la répartition des sentiments :", df['Genre 1'].dropna().unique())
        filtered_data = sentiment_counts[sentiment_counts['Genre 1'] == genre]

        if not filtered_data.empty:
            fig = px.pie(
                filtered_data,
                values='Percentage',
                names='Sentiment',
                title=f"Répartition des Sentiments pour le Genre : {genre}",
                color='Sentiment',
                color_discrete_map={'positif': 'green', 'neutre': 'blue', 'negatif': 'red'}
            )
            fig.update_traces(textinfo='percent+label', pull=[0.1 if s == 'positif' else 0 for s in filtered_data['Sentiment']])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"Aucune donnée disponible pour le genre sélectionné : {genre}")
    else:
        st.error("Les colonnes nécessaires pour l'analyse des sentiments ('Genre 1', 'proba_nega', 'proba_neutre', 'proba_positif') sont manquantes dans le fichier.")
else:
    st.error(f"Le fichier {output_file_path} est introuvable. Veuillez exécuter l'analyse des sentiments pour générer ce fichier.")
