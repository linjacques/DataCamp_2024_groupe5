import pandas as pd
import uuid
from wordcloud import STOPWORDS

# Définir la liste de stopwords personnalisée
stopwords_fr = STOPWORDS.union({
    # Injures générales
    'andouille', 'balourd', 'bâtard', 'bordel', 'bouffon', 
    'con', 'connard', 'connasse', 'conne', 'crétin', 'crétine', 'débile', 'emmerdeur', 
    'emmerdeuse', 'enculé', 'enculée', 'foutre', 'grognasse', 'idiot', 'idiote', 
    'imbécile', 'ordure', 'pd', 'pédale', 
    'pute', 'putain', 'racaille', 'salope', 'salopard', 'taré', 'tarlouze', 'trouduc', 
    'vulgaire', 'débile', 'bouffonne', 'gros con', 'grosse conne', 'trou du cul', 
    'branleur', 'branleuse', 'enculé de ta race', 
    'ferme ta gueule', 'ferme-la', 'grognasse', 'imbécile heureux', 'sale type', 
    'tête de con', 'va te faire foutre', 'vas chier', 'enfoiré', 'enfoirée', 'ducon', 
    'fils de pute', 'raclure', 'salaud', 'sale', 'baltringue', 'porc', 'clochard', 
    'sombre idiot', 'mal baisé', 'mal baisée', 'gogol', 'mongol', 'imbécile profond', 
    'espèce de merde', 'merdeux', 'couillon', 'taré', 'abruti profond', 'peine-à-jouir', 
    'connard fini', 'sale enfoiré', 'pétasse', 'pd', 'pute', 'enflure',

    # Injures racistes
    'bougnoule', 'négro', 'nègre', 'raton', 'feuj', 'youpin', 'chinetoque', 'bicot', 
    'niakoué', 'portos', 'rital', 'gitan', 'romanichel', 'babtou', 'crouille', 'chleuh', 
    'roumi', 'roumain de merde', 'sale arabe', 'arabe de merde', 'sale noir', 'noir de merde',

    # Injures homophobes
    'pédé', 'pédale', 'tapette', 'gouine', 'tarlouze', 'enculé', 'enculée', 'faggot', 
    'maricón', 'queer', 'homo de merde', 'lesbienne de merde',

    # Injures sexistes
    'salope', 'putain', 'pétasse', 'grognasse', 'chienne', 'bâtarde', 'pouffiasse', 
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


file_path = "../../data/Classeur4(Allocine_Reviews).csv"  
df = pd.read_csv(file_path, delimiter=";", encoding="latin")

# Supprimer les lignes contenant des valeurs NaN ou NULL
df_nettoye = df.dropna()

unique_id = uuid.uuid4().hex[:8]  # Prend les 8 premiers caractères d'un UUID

# Vérifier que la colonne de texte existe
col_texte = "Commentaire"  
if col_texte not in df_nettoye.columns:
    raise ValueError(f"La colonne '{col_texte}' est introuvable dans le fichier CSV.")

# Fonction pour supprimer les stopwords
def remove_stopwords(text):
    if pd.isna(text):  
        return text
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords_fr]
    return " ".join(filtered_words)

# Appliquer le nettoyage à la colonne de texte
df_nettoye[col_texte] = df_nettoye[col_texte].apply(remove_stopwords)

output_file_path = f"../../output/Allociné_dataset_{unique_id}.csv"

df_nettoye.to_csv(output_file_path, index=False, sep=";", encoding="utf-8")

print(f"Fichier nettoyé enregistré sous : {output_file_path}")