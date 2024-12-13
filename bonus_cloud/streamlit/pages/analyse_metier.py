import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import altair as alt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Télécharger les ressources nécessaires de NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Configuration de la page
st.set_page_config(
    page_title="Analyse des Films",
    page_icon="🎥",
    layout="wide"
)

# Titre principal stylisé
st.markdown(
    """
    <div style="
        background-color: #cce7f5; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center; 
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #1a73e8; font-family: Arial, sans-serif; font-size: 2.5em; margin: 0;">
            🎥 Analyse des Films
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Charger et nettoyer les données
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, sep=';', encoding='utf-8')
    data['Note'] = pd.to_numeric(data['Note'].str.replace(',', '.'), errors='coerce')
    data['etoiles_ia'] = pd.to_numeric(data['etoiles_ia'], errors='coerce')
    data['Date de publication'] = pd.to_datetime(data['Date de publication'], errors='coerce', dayfirst=True)
    return data

# Générer un nuage de mots
def generate_wordcloud(comments):
    st.markdown("<h2 style='color: #1a73e8;'>☁️ Nuage de Mots des Commentaires</h2>", unsafe_allow_html=True)
    text = " ".join(comments.dropna())
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english') + stopwords.words('french'))
    filtered_words = [word for word in tokens if word not in stop_words]
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(filtered_words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Afficher les informations détaillées d'un film
def display_movie_info(movie_data, movie_reviews, all_data):
    st.markdown(f"<h2 style='color: #1a73e8;'>📽️ Informations sur le Film : {movie_data['Titre du film']}</h2>", unsafe_allow_html=True)
    st.write(f"**Date de sortie :** {movie_data['Date de sortie']}")
    st.write(f"**Genre :** {movie_data['Genre 1']}")

    # Notes globales
    st.markdown("<h3 style='color: #1a73e8;'>⭐ Avis Généraux</h3>", unsafe_allow_html=True)
    average_note = movie_reviews['Note'].mean()
    average_ia_stars = movie_reviews['etoiles_ia'].mean()
    st.write(f"**Note moyenne des utilisateurs :** {average_note:.2f}/5")
    st.write(f"**Note moyenne IA :** {average_ia_stars:.2f}/5")

    # Comparaison entre Note et étoiles IA
    if average_note > average_ia_stars:
        st.info("💡 **Analyse :** Malgré une note utilisateur plutôt positive, l'analyse des commentaires suggère que le ressenti global est plus réservé.")
    else:
        st.success("💡 **Analyse :** Bien que les notes des utilisateurs soient relativement basses, l'analyse IA des commentaires reflète un ressenti plus positif.")

    # Performances des sites d'avis
    st.markdown("<h3 style='color: #1a73e8;'>🌐 Performances des Sites d'Avis</h3>", unsafe_allow_html=True)
    grouped_reviews = movie_reviews.groupby('URL de la critique')[['Note', 'etoiles_ia']].mean()
    st.dataframe(grouped_reviews)

    # Identifier le site le plus cohérent
    grouped_reviews['Écart'] = abs(grouped_reviews['Note'] - grouped_reviews['etoiles_ia'])
    best_site = grouped_reviews['Écart'].idxmin()
    st.write(f"💡 **Site le plus aligné avec l'analyse IA :** {best_site}")

    # Nuage de mots des commentaires
    generate_wordcloud(movie_reviews['Commentaire'])

    # Recommandations de films similaires
    st.markdown("<h3 style='color: #1a73e8;'>🎬 Films Similaires</h3>", unsafe_allow_html=True)
    similar_movies = all_data[(all_data['Genre 1'] == movie_data['Genre 1']) & (all_data['Titre du film'] != movie_data['Titre du film'])]
    similar_movies = similar_movies.groupby('Titre du film')[['Note']].mean().sort_values(by='Note', ascending=False).head(5)
    st.write("Ces films similaires permettent de comparer les statistiques et de positionner le film sélectionné parmi eux :")
    for movie, row in similar_movies.iterrows():
        st.write(f"- {movie} (Note moyenne : {row['Note']:.2f}/5)")

# Interface Streamlit
st.sidebar.header("🎬 Sélectionnez un Film")
CSV_FILE_PATH = "bonus_cloud/streamlit/output/sentiments_resultat_final.csv"
data = load_data(CSV_FILE_PATH)

# Sélection du film
movie_titles = data['Titre du film'].unique()
selected_movie = st.sidebar.selectbox("Choisissez un film :", movie_titles)

# Filtrer les données pour le film sélectionné
movie_data = data[data['Titre du film'] == selected_movie].iloc[0]
movie_reviews = data[data['Titre du film'] == selected_movie]

# Afficher les informations du film
display_movie_info(movie_data, movie_reviews, data)
