from transformers import AutoTokenizer, RobertaForSequenceClassification
import torch
from sklearn.preprocessing import LabelEncoder
import pandas as pd

if __name__ == '__main__':
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = RobertaForSequenceClassification.from_pretrained(model_name)

    # Fonction pour analyser le sentiment
    def analyze_sentiment(comment):
        inputs = tokenizer(comment, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiment_scores = scores.detach().numpy()[0]
        
        # Retourner les probabilités de chaque sentiment
        return sentiment_scores[0], sentiment_scores[1], sentiment_scores[2]
    
    # Charger le fichier CSV
    file_path = '../data/commentaires.csv'
    df = pd.read_csv(file_path, delimiter=';')

    # Ajouter les nouvelles colonnes pour les probabilités de sentiment
    df['proba_nega'] = 0.0
    df['proba_neutre'] = 0.0
    df['proba_positif'] = 0.0

    # Analyser les sentiments pour chaque commentaire et ajouter les probabilités au DataFrame
    for index, row in df.iterrows():
        proba_nega, proba_neutre, proba_positif = analyze_sentiment(row['Commentaire'])
        df.at[index, 'proba_nega'] = proba_nega
        df.at[index, 'proba_neutre'] = proba_neutre
        df.at[index, 'proba_positif'] = proba_positif

    # Sauvegarder le DataFrame mis à jour dans un nouveau fichier CSV
    output_file_path = '../output/sentiments_resultat.csv'
    df.to_csv(output_file_path, index=False, sep=';')