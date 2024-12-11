import pandas as pd
import re
from wordcloud import STOPWORDS

# Définir la liste de stopwords personnalisée
stopwords_fr = STOPWORDS.union(
{
    'abruti', 'abrutie', 'andouille', 'balourd', 'bâtard', 'bordel', 'bouffon', 
    'con', 'connard', 'connasse', 'conne', 'crétin', 'crétine', 'débile', 'emmerdeur', 
    'emmerdeuse', 'enculé', 'enculée', 'foutre', 'grognasse', 'idiot', 'idiote', 
    'imbécile', 'merde', 'merdique', 'nul', 'nulle', 'ordure', 'pd', 'pédale', 
    'pute', 'putain', 'racaille', 'salope', 'salopard', 'taré', 'tarlouze', 'trouduc', 
    'vulgaire', 'débile', 'bouffonne', 'gros con', 'grosse conne', 'trou du cul', 
    'branleur', 'branleuse', 'chiant', 'chiante', 'déchet', 'enculé de ta race', 
    'ferme ta gueule', 'ferme-la', 'grognasse', 'imbécile heureux', 'sale type', 
    'tête de con', 'va te faire foutre', 'vas chier', 'enfoiré', 'enfoirée', 'ducon', 
    'fils de pute', 'raclure', 'salaud', 'sale', 'baltringue', 'porc', 'clochard', 
    'sombre idiot', 'mal baisé', 'mal baisée', 'gogol', 'mongol', 'imbécile profond', 
    'espèce de merde', 'merdeux', 'couillon', 'taré', 'abruti profond', 'peine-à-jouir', 
    'connard fini', 'sale enfoiré', 'pétasse', 'pd', 'pute' 
}
)

# Charger le fichier CSV
file_path = "../data/Classeur4(Allocine_Reviews).csv"  # Remplacez par le chemin de votre fichier CSV
df = pd.read_csv(file_path, delimiter=";", encoding="latin")

# Vérifier que la colonne de texte existe
col_text = "Commentaire"  # Remplacez par le nom de la colonne contenant les textes
if col_text not in df.columns:
    raise ValueError(f"La colonne '{col_text}' est introuvable dans le fichier CSV.")

# Fonction pour supprimer les stopwords
def remove_stopwords(text):
    if pd.isna(text):  # Vérifier si le texte est NaN
        return text
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords_fr]
    return " ".join(filtered_words)

# Appliquer le nettoyage à la colonne de texte
df[col_text] = df[col_text].apply(remove_stopwords)

# Sauvegarder le fichier nettoyé
output_file_path = "../output/fichier_nettoye.csv"
df.to_csv(output_file_path, index=False, sep=";", encoding="utf-8")

print(f"Fichier nettoyé enregistré sous : {output_file_path}")
