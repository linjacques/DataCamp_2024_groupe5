import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from wordcloud import STOPWORDS

###########################################
# Scraping des critiques
###########################################

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

# Fonction pour nettoyer les commentaires
def clean_comment(comment):
    if comment:
        # Supprimer les retours à la ligne et les retours chariots
        comment = comment.replace('\n', ' ').replace('\r', ' ')
        # Supprimer le texte lié au spoiler, par exemple "spoiler:" ou des motifs similaires
        comment = comment.replace("spoiler:", "").strip()
        return comment
    return None

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

            # Nettoyer le commentaire avant de l'ajouter
            content = clean_comment(content)

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

###################################
# Nettoyage des données avant fusion
###################################

# On convertit les notes en numérique
allocine_data['Note'] = pd.to_numeric(allocine_data['Note'].str.replace(',', '.'), errors='coerce')

# Nettoyage des colonnes de dates
allocine_data["Date de sortie"] = allocine_data["Date de sortie"].fillna("")
allocine_data["Date de publication"] = allocine_data["Date de publication"].fillna("")

# Fonction pour convertir les dates
def convertir_date(date_str):
    mois_fr = {
        "janvier": "01", "février": "02", "mars": "03", "avril": "04", "mai": "05",
        "juin": "06", "juillet": "07", "août": "08", "septembre": "09", "octobre": "10",
        "novembre": "11", "décembre": "12"
    }
    try:
        jour, mois, annee = date_str.split(" ")
        mois_num = mois_fr[mois]
        return f"{jour}/{mois_num}/{annee}"
    except (ValueError, KeyError, AttributeError):
        return "01/01/2000"

# Appliquer la conversion
allocine_data["Date de sortie"] = allocine_data["Date de sortie"].apply(convertir_date)
allocine_data["Date de publication"] = allocine_data["Date de publication"].apply(convertir_date)

#####################################
# Fusion avec l'autre source de données (le code permettant la génération du CSV que nous récupérons ici est disponible dans > DataCamp_2024_groupe5/scrapy)
#####################################

# Charger les données supplémentaires
additional_data = pd.read_csv('../../../scrapy/reviews_test.csv', sep=',', encoding='utf-8')

# Fusionner les deux DataFrames
allocine_data = pd.concat([allocine_data, additional_data], ignore_index=True)

#####################################
# Nettoyage des données final
#####################################

def arrondir_au_0_5(df, colonne):
    df[colonne] = (df[colonne] / 0.5).round() * 0.5
    return df

# On arrondit les notes à 1 chiffre après la virgule
allocine_data['Note'] = round(allocine_data['Note'], 1)

# Arrondir les notes à 0.5 près
allocine_data = arrondir_au_0_5(allocine_data, 'Note')

# Supprimer les lignes sans commentaire ou sans note
allocine_data.dropna(subset=['Commentaire', 'Note'], inplace=True)
# Supprimer les doublons basés sur l'ID utilisateur et le commentaire
allocine_data.drop_duplicates(subset=['ID Utilisateur', 'Commentaire'], inplace=True)

# Remplacer les valeurs manquantes dans les colonnes 'Titre du film', 'Date de sortie', et 'Genre 1' par des valeurs par défaut
allocine_data['Titre du film'] = allocine_data['Titre du film'].fillna('Titre inconnu')
allocine_data['Date de sortie'] = allocine_data['Date de sortie'].fillna('Date de sortie inconnue')
allocine_data['Genre 1'] = allocine_data['Genre 1'].fillna('Genre inconnu')

# Supprimer les commentaires trop courts (moins de 10 caractères)
allocine_data = allocine_data[allocine_data['Commentaire'].str.len() >= 10]

# Supprimer les notes en dehors de l'intervalle [0, 5]
allocine_data = allocine_data[(allocine_data['Note'] >= 0) & (allocine_data['Note'] <= 5)]

# Définir la liste de stopwords personnalisée (c'est Jacques LIN qui a fait cette liste je balance)
stopwords_fr = STOPWORDS.union({
    # Injures racistes
    'bougnoule', 'négro', 'nègre', 'raton', 'feuj', 'youpin', 'chinetoque', 'bicot', 
    'niakoué', 'portos', 'rital', 'gitan', 'romanichel', 'babtou', 'crouille', 'chleuh', 
    'roumi', 'roumain de merde', 'sale arabe', 'arabe de merde', 'sale noir', 'noir de merde',

    # Injures homophobes
    'pédé', 'pédale', 'tapette', 'gouine', 'tarlouze', 'enculé', 'enculée', 'faggot', 
    'maricón', 'queer', 'homo de merde', 'lesbienne de merde', 'pd',

    # Injures sexistes
    'salope', 'putain', 'pétasse', 'grognasse', 'bâtarde', 'pouffiasse', 
    'cochonne', 'catin', 'sale femme', 'gonzesse', 'pute', 'femmelette', 'sac à foutre',

    # Injures religieuses
    'sale catho', 'catho de merde', 'musulman de merde', 'sale musulman', 
    'sale juif', 'juif de merde', 'bouddhiste de merde', 'hindou de merde',

    # Expressions discriminatoires
    'retardé', 'mongol', 'débile', 'gogol', 'idiot profond', 'espèce de débile', 
    'attardé', 'handicapé mental', 'bête comme ses pieds',

    # Variations possibles
    'fils de chien', 'fille de chien', 'chiennasse', 'sale chien', 'chien de merde', 
    'espèce de chien', 'mange merde', 'trou du cul', 'sale bâtard', 'bâtard fini'
})

# Si un stopword est présent on supprime la ligne entière
# def remove_stopwords(comment):
#     for stopword in stopwords_fr:
#         if stopword in comment.lower():
#             return None
#     return comment

# allocine_data['Commentaire'] = allocine_data['Commentaire'].apply(remove_stopwords)
# allocine_data.dropna(subset=['Commentaire'], inplace=True)

########################################
# Analyse des sentiments
########################################

print('ok', len(allocine_data))

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
allocine_data['Note IA'] = 0.0

# Fonction pour convertir les probabilités de sentiment en une note sur 5
def convert_to_rating(proba_nega, proba_neutre, proba_positif):
    # Pondérer les probabilités pour obtenir une note sur 5
    rating = (proba_positif * 5) + (proba_neutre * 3) + (proba_nega * 1)
    return round(rating, 2)

# Analyser les sentiments pour chaque commentaire et ajouter les probabilités au DataFrame
for index, row in allocine_data.iterrows():
    proba_nega, proba_neutre, proba_positif = analyze_sentiment(row['Commentaire'])
    note_ia = convert_to_rating(proba_nega, proba_neutre, proba_positif)
    
    # On arrondit la note à 0.5 près pour correspondre au nettoyage déjà effectué sur les notes
    allocine_data.at[index, 'Note IA'] = (note_ia / 0.5).round() * 0.5

###################################################
# Sauvegarde des résultats dans un fichier CSV
###################################################

# Sauvegarder le DataFrame mis à jour dans un nouveau fichier CSV
output_file_path = '../output/sentiments_resultat_final.csv'
allocine_data.to_csv(output_file_path, index=False, sep=';')