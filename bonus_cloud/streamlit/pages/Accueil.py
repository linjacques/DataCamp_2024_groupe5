import streamlit as st
import csv
import chardet
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Exploration des Données Allociné",
    page_icon="🎥",
    layout="wide"
)

# Titre principal stylisé
st.markdown(

    """
        <h1 style="color: #1a73e8; font-family: Arial, sans-serif; font-size: 2.5em; margin: 0;  text-align: center;">
            🎬 Exploration des Données Allociné
        </h1>
    """,
    unsafe_allow_html=True
)

# Introduction
st.markdown(
    """
    <p style="font-size: 1.2em; text-align: center; margin-bottom: 20px;">
        Bienvenue sur notre application Streamlit ! Naviguez entre les différentes sections à l'aide du menu sur la gauche pour découvrir nos analyses et visualisations.
    </p>
    """,
    unsafe_allow_html=True
)

# Objectif du Projet
st.markdown(
    """
    <h2 style="color: #1a73e8;">🌟 Objectif du Projet</h2>
    <p style="font-size: 1.1em; line-height: 1.6;">
        L'objectif de ce projet est de mettre en pratique les concepts de <strong>Streamlit</strong> et de <strong>Data Science</strong>
        en analysant un jeu de données de films. À partir de données scrappées sur <strong>Allociné</strong>, nous allons explorer
        différentes fonctionnalités de Streamlit pour visualiser et analyser ces données.
    </p>
    """,
    unsafe_allow_html=True
)

# Section d'exploration des fichiers CSV
st.markdown(
    """
    <h2 style="color: #1a73e8;">📂 Exploration des Fichiers CSV</h2>
    <h3>Aperçu du fichier : <strong>Allociné_dataset_89bcdf92.csv</strong></h3>
    """,
    unsafe_allow_html=True
)

# Chemin du fichier
file_path = "bonus_cloud/streamlit/output/Allociné_dataset_89bcdf92.csv"

# Lecture et détection de l'encodage
try:
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        detected_encoding = result["encoding"]

    st.markdown(f"**Encodage détecté :** `{detected_encoding}`")

    # Lecture du fichier CSV
    try:
        with open(file_path, "r", encoding=detected_encoding) as f:
            try:
                # Détection du séparateur
                sample_data = f.read(1024)
                f.seek(0)
                dialect = csv.Sniffer().sniff(sample_data)
                separator = dialect.delimiter
            except Exception:
                st.warning("🔍 Séparateur non détecté automatiquement. Utilisation du séparateur par défaut : `;`.")
                separator = ";"

        st.markdown(f"**Séparateur utilisé :** `{separator}`")

        # Chargement des données
        df = pd.read_csv(file_path, encoding=detected_encoding, quotechar='"', sep=separator)

        # Stockage du DataFrame dans la session
        st.session_state["dataframe"] = df

        # Aperçu des données
        st.markdown("<h3 style='color: #1a73e8;'>📊 Détails du Fichier</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Nombre de lignes", len(df))
        col2.metric("Nombre de colonnes", len(df.columns))
        col3.metric("Colonnes uniques", len(df.columns.unique()))

        st.markdown("<h3 style='color: #1a73e8;'>🔎 Aperçu des Colonnes</h3>", unsafe_allow_html=True)
        st.write(", ".join(df.columns))

        st.markdown("<h3 style='color: #1a73e8;'>🧾 Types de Données</h3>", unsafe_allow_html=True)
        st.dataframe(df.dtypes.astype(str), use_container_width=True)

        st.markdown("<h3 style='color: #1a73e8;'>👀 Aperçu des Données</h3>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")

except FileNotFoundError:
    st.error(f"❌ Le fichier spécifié n'a pas été trouvé : {file_path}")
except Exception as e:
    st.error(f"❌ Une erreur inattendue est survenue : {e}")

# Aperçu des pages
st.markdown(
    """
    <h2 style="color: #1a73e8;">🗂️ Aperçu des Pages</h2>
    <ul style="font-size: 1.1em; line-height: 1.6;">
        <li>🏠 <strong>Page principale</strong> : Guide pour naviguer dans l'application et explorer les fonctionnalités.</li>
        <li>🔍 <strong>Exploration Interactive des Données CSV</strong> : Explorez les colonnes, types de données, et visualisez un échantillon.</li>
        <li>📈 <strong>Analyse Visuelle des Notes</strong> : Découvrez les tendances et répartitions des notes des films.</li>
        <li>📊 <strong>Visualisation des Données avec Tableau</strong> : Analyse avancée des données avec des outils dynamiques.</li>
        <li>🤖 <strong>Analyse IA avec Roberta</strong> : Détection automatique des sentiments des spectateurs (positif, neutre, négatif).</li>
        <li>🎥 <strong>Analyse des Films</strong> : Découvrez les notes, genres et commentaires des films pour une vue complète.</li>
    </ul>
    """,
    unsafe_allow_html=True
)

# Footer stylisé
st.markdown(
    """
    <hr style="border: none; border-top: 2px solid #ccc; margin: 20px 0;">
    <h3 style="text-align: center; font-size: 1.1em;">
        🛠️ <strong>Application développée avec Streamlit</strong> | 📅 <strong>2024</strong> | 🎨 <strong>Par Jacques Lin, Thomas Coutarel, Thomas Yu, Noam Boulze, Amir Anciaux</strong>
    </h3>
    """,
    unsafe_allow_html=True
)
