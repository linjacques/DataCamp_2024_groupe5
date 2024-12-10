import csv
import chardet
import pandas as pd
import streamlit as st

st.title("Exploration des fichiers CSV")

st.markdown("""
### Instructions :
1. Cliquez sur le bouton **"Parcourir les fichiers"** pour importer un fichier CSV.
2. Une fois le fichier importé, son contenu sera affiché sous forme de tableau.
""")

# Charger le fichier
uploaded_file = st.file_uploader("Téléchargez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Détection de l'encodage
    raw_data = uploaded_file.read()  # Lire tout le contenu pour détecter l'encodage
    result = chardet.detect(raw_data)
    detected_encoding = result["encoding"]

    st.write(f"**Encodage détecté :** {detected_encoding}")

    # Lecture du fichier CSV
    try:
        # Réinitialiser le curseur avant toute nouvelle lecture
        uploaded_file.seek(0)

        # Détection du séparateur
        try:
            sample_data = uploaded_file.read(1024).decode(detected_encoding)  # Lire un échantillon pour la détection
            uploaded_file.seek(0)  # Réinitialiser le curseur après lecture
            dialect = csv.Sniffer().sniff(sample_data)
            separator = dialect.delimiter
        except Exception:
            st.warning("Impossible de détecter automatiquement le séparateur. Utilisation du séparateur par défaut : ','")
            separator = ';'  # Définir un séparateur par défaut

        st.write(f"**Séparateur utilisé :** `{separator}`")

        # Lecture du fichier avec le séparateur détecté ou par défaut
        df = pd.read_csv(uploaded_file, encoding=detected_encoding, quotechar='"', sep=separator)

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
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
