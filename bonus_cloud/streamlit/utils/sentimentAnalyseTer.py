from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd

if __name__ == '__main__':
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Fonction pour analyser le sentiment
    def analyze_sentiment(comment):
        inputs = tokenizer(comment, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiment_scores = scores.detach().numpy()[0]
        
        # Retourner les probabilités de chaque sentiment
        return sentiment_scores[4], sentiment_scores[3], sentiment_scores[2], sentiment_scores[1], sentiment_scores[0]
    
    # Charger le fichier CSV
    file_path = '../data/Classeur4(Allocine_Reviews).csv'
    df = pd.read_csv(file_path, delimiter=';')

    # Ajouter les nouvelles colonnes pour les probabilités de sentiment
    df['5_etoiles'] = 0.0
    df['4_etoiles'] = 0.0
    df['3_etoiles'] = 0.0
    df['2_etoiles'] = 0.0
    df['1_etoile'] = 0.0

    # Analyser les sentiments pour chaque commentaire et ajouter les probabilités au DataFrame
    for index, row in df.iterrows():
        proba_5_etoiles, proba_4_etoiles, proba_3_etoiles, proba_2_etoiles, proba_1_etoile = analyze_sentiment(row['Commentaire'])
        df.at[index, '5_etoiles'] = proba_5_etoiles
        df.at[index, '4_etoiles'] = proba_4_etoiles
        df.at[index, '3_etoiles'] = proba_3_etoiles
        df.at[index, '2_etoiles'] = proba_2_etoiles
        df.at[index, '1_etoile'] = proba_1_etoile

    # Sauvegarder le DataFrame mis à jour dans un nouveau fichier CSV
    output_file_path = '../output/sentiments_resultat_ter.csv'
    df.to_csv(output_file_path, index=False, sep=';')