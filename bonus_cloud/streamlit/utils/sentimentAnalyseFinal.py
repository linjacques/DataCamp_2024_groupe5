import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Fonction pour récupérer le titre d'un film
def get_film_title(film_url):
    try:
        response = requests.get(film_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Prioriser la balise contenant le titre du film
        title_div =soup.find('span', class_='dark-grey')
        if title_div:
            return title_div.text.strip()
        # Si la balise précédente n'est pas présente, essayer une alternative
        title_span =  soup.find('div', class_='titlebar-title titlebar-title-xl')
        return title_span.text.strip() if title_span else None
    except Exception as e:
        print(f"Erreur lors de la récupération du titre pour {film_url} : {e}")
        return None

# Fonction pour récupérer la date de sortie d'un film
def get_film_release_date(film_url):
    try:
        response = requests.get(film_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        date_div = soup.find('div', class_='meta-body-item meta-body-info')
        if date_div:
            date = date_div.find_all('span')[0].text.strip()
            return date
        else:
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération de la date de sortie pour {film_url} : {e}")
        return None

# Fonction pour récupérer le premier genre d'un film
def get_genre1(film_url):
    try:
        response = requests.get(film_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        date_div = soup.find('div', class_='meta-body-item meta-body-info')
        if date_div:
            genre1 = date_div.find_all('span')[4].text.strip()
            return genre1
        else:
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération du genre1 pour {film_url} : {e}")
        return None
# Fonction pour récupérer le second genre d'un film

# Dictionnaire des genres associés aux films
film_ids = ['61282', '115362', '130440','232669','218265','198488','193113','256880','196604','193108','53751','182745',
            '182745','10568','10126','5818','223940','203691','10862','135523','206775','130368',
            '448','5247','29289','8488','12789','35973','18598','258374','208692','57410','145646','309','29276','41245','46865',
            '53756','58608','116305','126693','134925','111112','188550','19395','21189','5969','19776',
            '114782','44449','229831','45264','24944','190918','28968']#52
ids_utilisateur = []
notes = []
commentaire = []
dates_publication = []
urls = []
num_films = []
titres = []
release_dates = []
genres1 = []
film_titles = {}
film_release_dates = {}
film_genres1 = {}

for film_id in film_ids:
    critiques_url = f"https://www.allocine.fr/film/fichefilm-{film_id}/critiques/spectateurs/"
    film_url = f"https://www.allocine.fr/film/fichefilm_gen_cfilm={film_id}.html"
    if film_id not in film_titles:
        print(f"Récupération du titre pour le film ID : {film_id}")
        film_title = get_film_title(film_url)
        film_titles[film_id] = film_title if film_title else "Titre inconnu"
    if film_id not in film_release_dates:
        print(f"Récupération de la date de sortie pour le film ID : {film_id}")
        film_release_date = get_film_release_date(film_url)
        film_release_dates[film_id] = film_release_date if film_release_date else "Date de sortie inconnue"
    if film_id not in film_genres1:
        print(f"Récupération du premier genre pour le film ID : {film_id}")
        film_genre1 = get_genre1(film_url)
        film_genres1[film_id] = film_genre1 if film_genre1 else "Genre 1 inconnu"
    for page in range(1, 2):
        url = critiques_url + f'?page={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', class_='review-card')
        for review in reviews:
            rating = review.find('span', class_='stareval-note')
            rating = rating.text.strip() if rating else None
            content = review.find('div', class_='content-txt review-card-content')
            content = content.text.strip() if content else None
            date = review.find('span', class_='review-card-meta-date')
            date = date.text.strip().replace("Publiée le", "").strip() if date else None
            user_info = review.find('div', class_='review-card-user-infos')
            if user_info:
                username_tag = user_info.find('a', class_='xXx')
                if username_tag:
                    user_href = username_tag['href']
                    user_id = user_href.split('/')[-2]
                else:
                    visitor_tag = user_info.find('span')
                    user_id = "Visiteur" if visitor_tag and visitor_tag.text.strip() == "Un visiteur" else "id" + str(len(ids_utilisateur) + 1)
            else:
                user_id = "Inconnu"
            critique_url = url.split('.fr')[0] if '.fr' in url else url.split('.com')[0]
            # Ajout des données dans les listes
            ids_utilisateur.append(user_id)
            notes.append(rating)
            commentaire.append(content)
            dates_publication.append(date)
            urls.append(critique_url)
            num_films.append(film_id)
            titres.append(film_titles[film_id]) # Ajouter le titre récupéré
            release_dates.append(film_release_dates[film_id])  # Ajouter la date de sortie récupérée
            genres1.append(film_genres1[film_id])  # Ajouter le premier genre récupéré
        time.sleep(2)

# Création du DataFrame avec toutes les colonnes
allocine_data = pd.DataFrame({
    'ID Utilisateur': ids_utilisateur,
    'Note': notes,
    'Commentaire': commentaire,
    'Date de publication': dates_publication,
    'URL de la critique': urls,
    'id du film' : num_films,
    'Titre du film': titres,  # Ajout de la colonne titre
    'Date de sortie': release_dates,  # Ajout de la colonne date de sortie
    'Genre 1': genres1,  # Ajout du premier genre
})

# Analyse des sentiments pour chaque commentaire
model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Fonction pour analyser le sentiment
def analyze_sentiment(comment):
    inputs = tokenizer(comment, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=1)
    sentiment_scores = scores.detach().numpy()[0]
    
    return sentiment_scores

# Ajouter les nouvelles colonnes pour les probabilités de sentiment
allocine_data['etoiles_ia'] = 0.0

# Fonction pour convertir les probabilités de sentiment en une note sur 5
def convert_to_rating(proba_nega, proba_neutre, proba_positif):
    # Pondérer les probabilités pour obtenir une note sur 5
    rating = (proba_positif * 5) + (proba_neutre * 3) + (proba_nega * 1)
    return round(rating, 2)

# Analyser les sentiments pour chaque commentaire et ajouter les probabilités au DataFrame
for index, row in allocine_data.iterrows():
    proba_nega, proba_neutre, proba_positif = analyze_sentiment(row['Commentaire'])
    etoiles_ia = convert_to_rating(proba_nega, proba_neutre, proba_positif)
    allocine_data.at[index, 'etoiles_ia'] = etoiles_ia

# Sauvegarder le DataFrame mis à jour dans un nouveau fichier CSV
output_file_path = '../output/sentiments_resultat_final.csv'
allocine_data.to_csv(output_file_path, index=False, sep=';')