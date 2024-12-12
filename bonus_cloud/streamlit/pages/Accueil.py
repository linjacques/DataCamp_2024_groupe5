import streamlit as st
import csv
import chardet
import pandas as pd

st.title("Accueil")
st.write("Bienvenue sur notre application Streamlit !")
st.write("Vous pouvez naviguer entre les différentes pages grâce à la barre de navigation sur la gauche.")

st.write("### Objectif du projet")
st.write("L'objectif de ce projet est de mettre en pratique les concepts de Streamlit et de Data Science en analysant un jeu de données de films. A partir de données recuprérées sur Allociné à partir du scrapping, nous allons explorer les différentes fonctionnalités de Streamlit pour visualiser et analyser ces données.")
st.title("Exploration des fichiers CSV")

st.markdown("""
### Aperçu du fichier Allociné_dataset_89bcdf92.csv
""")

# Chemin du fichier
file_path = "bonus_cloud/streamlit/output/Allociné_dataset_89bcdf92.csv"

# Lecture et détection de l'encodage
try:
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        detected_encoding = result["encoding"]

    st.write(f"**Encodage détecté :** {detected_encoding}")

    # Lecture du fichier CSV
    try:
        with open(file_path, "r", encoding=detected_encoding) as f:
            # Détection du séparateur
            try:
                sample_data = f.read(1024)  # Lire un échantillon pour la détection
                f.seek(0)  # Réinitialiser le curseur après lecture
                dialect = csv.Sniffer().sniff(sample_data)
                separator = dialect.delimiter
            except Exception:
                st.warning("Impossible de détecter automatiquement le séparateur. Utilisation du séparateur par défaut :  ' ; ' ")
                separator = ';'  # Définir un séparateur par défaut

        st.write(f"**Séparateur utilisé :** `{separator}`")

        # Lecture du fichier avec le séparateur détecté ou par défaut
        df = pd.read_csv(file_path, encoding=detected_encoding, quotechar='"', sep=separator)

        # Stocker le DataFrame dans session_state
        st.session_state["dataframe"] = df

        # Détails du fichier
        st.subheader("Détails importants")
        st.write(f"- **Nombre de lignes** : {len(df)}")
        st.write(f"- **Nombre de colonnes** : {len(df.columns)}")
        st.write("- **Colonnes** :", ", ".join(df.columns))
        
        st.subheader("Types de données")
        st.write(df.dtypes)
        
        # Aperçu des données
        st.subheader("Aperçu des données")
        st.dataframe(df.head(10))

    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")

except FileNotFoundError:
    st.error(f"Le fichier spécifié n'a pas été trouvé : {file_path}")
except Exception as e:
    st.error(f"Une erreur inattendue est survenue : {e}")

st.title("Aperçu des Pages")

st.subheader("Accueil")
st.write("Cette page principale vous guide dans l'exploration et l'analyse des données. Vous y trouverez un aperçu global des fonctionnalités de l'application.")

st.subheader("Exploration Interactive des Données CSV")
st.write("Plongez dans vos fichiers CSV grâce à une interface interactive. Visualisez et analysez les données en détail, tout en explorant les colonnes, les types de données et un échantillon des enregistrements.")

st.subheader("Analyse Visuelle des Notes : Tendances et Répartitions")
st.write("Découvrez des graphiques détaillés pour analyser les notes des films. Identifiez les tendances, comparez les genres, et comprenez la répartition des notes.")

st.subheader("Visualisation des Données avec Tableau")
st.write("Profitez d'une intégration avec le logiciel Tableau pour une exploration avancée des données via des tableaux de bord interactifs et puissants.")

st.subheader("Analyse Automatisée des Sentiments avec Roberta")
st.write("Une intelligence artificielle analyse les commentaires pour déterminer leur tonalité : positive, neutre ou négative. Découvrez rapidement l'humeur générale des spectateurs.")

st.subheader("Analyse des films")
st.write("Accédez à des insights spécifiques sur les films, combinant notes, genres et commentaires pour une vision complète des préférences et des critiques.")