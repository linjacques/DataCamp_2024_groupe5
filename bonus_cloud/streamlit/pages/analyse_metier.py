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
nltk.download('punkt_tab')

# Charger et nettoyer les données
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, sep=';', encoding='utf-8')
    data['Note'] = pd.to_numeric(data['Note'].str.replace(',', '.'), errors='coerce')
    data['etoiles_ia'] = pd.to_numeric(data['etoiles_ia'], errors='coerce')
    # Convertir les dates en toute lettre en datetime
    data['Date de publication'] = pd.to_datetime(data['Date de publication'], errors='coerce', dayfirst=True)
    return data

# Générer un nuage de mots
def generate_wordcloud(comments):
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
    st.header(f"Informations sur le film : {movie_data['Titre du film']}")
    st.write(f"**Date de sortie :** {movie_data['Date de sortie']}")
    st.write(f"**Genre :** {movie_data['Genre 1']}")

    # Notes globales
    st.subheader("Avis généraux")
    average_note = movie_reviews['Note'].mean()
    average_ia_stars = movie_reviews['etoiles_ia'].mean()
    st.write(f"**Note moyenne des utilisateurs :** {average_note:.2f}/5")
    st.write(f"**Note moyenne IA :** {average_ia_stars:.2f}/5")

    # Comparaison entre Note et étoiles IA
    if average_note > average_ia_stars:
        st.write("💡 **Analyse :** Malgré une note utilisateur plutôt positive, l'analyse des commentaires suggère que le ressenti global est plus réservé.")
    else:
        st.write("💡 **Analyse :** Bien que les notes des utilisateurs soient relativement basses, l'analyse IA des commentaires reflète un ressenti plus positif.")

    # Groupement par URL de la critique
    st.subheader("Performances des sites d'avis")
    grouped_reviews = movie_reviews.groupby('URL de la critique')[['Note', 'etoiles_ia']].mean()
    st.dataframe(grouped_reviews)

    # Identifier le site le plus cohérent
    grouped_reviews['écart'] = abs(grouped_reviews['Note'] - grouped_reviews['etoiles_ia'])
    best_site = grouped_reviews['écart'].idxmin()
    st.write(f"💡 **Site le plus aligné avec l'analyse IA :** {best_site}")

    # Positionnement dans la catégorie principale
    st.subheader("Positionnement dans la catégorie principale")
    category_movies = all_data[all_data['Genre 1'] == movie_data['Genre 1']]
    category_movies = category_movies.groupby('Titre du film')[['Note']].mean().sort_values(by='Note', ascending=False)
    position = category_movies.index.tolist().index(movie_data['Titre du film']) + 1
    total_in_category = len(category_movies)
    st.write(f"Le film est classé **#{position} sur {total_in_category}** dans sa catégorie principale.")

    if position <= total_in_category * 0.3:
        st.write("🎉 Le film est bien classé dans sa catégorie principale.")
    else:
        st.write("📈 Le film a du potentiel pour améliorer sa position.")

    # Nuage de mots des commentaires
    st.subheader("Nuage de mots des commentaires")
    generate_wordcloud(movie_reviews['Commentaire'])

        # Évolution des notes et sentiments dans le temps
    st.subheader("Évolution des notes et sentiments")
    
    # Regrouper les données par mois
    timeline_data = movie_reviews.groupby(movie_reviews['Date de publication'].dt.to_period('M')).mean()
    
    # Vérifier si des données valides existent
    if not timeline_data.empty:
        timeline_data = timeline_data.reset_index()
        timeline_chart = alt.Chart(timeline_data).mark_line().encode(
            x=alt.X('Date de publication:T', title='Date'),
            y=alt.Y('Note', title='Note moyenne'),
            color=alt.value('blue'),
            tooltip=['Date de publication:T', 'Note']
        ).properties(title="Évolution des notes dans le temps")
        st.altair_chart(timeline_chart, use_container_width=True)
    else:
        st.write("⚠️ Aucune donnée disponible pour afficher l'évolution des notes dans le temps.")


    # Recommandations de films similaires
    st.subheader("Films similaires")
    similar_movies = all_data[(all_data['Genre 1'] == movie_data['Genre 1']) & (all_data['Titre du film'] != movie_data['Titre du film'])]
    similar_movies = similar_movies.groupby('Titre du film')[['Note']].mean().sort_values(by='Note', ascending=False).head(5)
    st.write("Ces films similaires permettent de comparer les statistiques et de positionner le film sélectionné parmi eux :")
    for movie, row in similar_movies.iterrows():
        st.write(f"- {movie} (Note moyenne : {row['Note']:.2f}/5)")

# Interface Streamlit
st.title("Analyse des Films")

# Chemin d'accès au fichier CSV
CSV_FILE_PATH = "bonus_cloud/streamlit/output/sentiments_resultat_final.csv"

data = load_data(CSV_FILE_PATH)

# Sélection du film
st.sidebar.header("Sélectionnez un film")
movie_titles = data['Titre du film'].unique()
selected_movie = st.sidebar.selectbox("Choisissez un film :", movie_titles)

# Filtrer les données pour le film sélectionné
movie_data = data[data['Titre du film'] == selected_movie].iloc[0]
movie_reviews = data[data['Titre du film'] == selected_movie]

# Afficher les informations du film
display_movie_info(movie_data, movie_reviews, data)
