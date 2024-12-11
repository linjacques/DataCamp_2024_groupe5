import streamlit as st
import pandas as pd
import plotly.express as px
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

st.title("Analyse des Sentiments")

# Charger le modèle et le tokenizer
@st.cache_resource
def load_model():
    model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# Zone de texte pour écrire un commentaire
user_input = st.text_area("Entrez un texte à analyser :", "")

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
    st.write("### Résultats de l'analyse :")
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
