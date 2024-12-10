import chardet
import pandas as pd
import streamlit as st

# Titre de l'application
st.title("Exploration des fichiers CSV")

st.markdown("""
### Instructions :
1. Cliquez sur le bouton **"Parcourir les fichiers"** pour importer un fichier CSV.
2. Une fois le fichier importé, son contenu sera affiché sous forme de tableau.
""")

# Étape 1 : Charger le fichier
uploaded_file = st.file_uploader("Téléchargez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Étape 2 : Détection de l'encodage
    # Lire un échantillon pour détecter l'encodage (depuis le fichier téléchargé, qui est en mémoire)
    raw_data = uploaded_file.read() 
    result = chardet.detect(raw_data)
    detected_encoding = result["encoding"]

    st.write(f"**Encodage détecté :** {detected_encoding}")

    # Étape 3 : Lecture du fichier CSV
    try:
        # Réinitialiser le curseur du fichier avant la lecture avec Pandas
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding=detected_encoding, quotechar='"', sep=";")

        # Détails du fichier
        st.subheader("Détails importants")
        st.write(f"- **Nombre de lignes** : {len(df)}")
        st.write(f"- **Nombre de colonnes** : {len(df.columns)}")
        st.write("- **Colonnes** :", ", ".join(df.columns))
        
        st.subheader("Types de données")
        st.write(df.dtypes)
        
        # Aperçu des données
        st.subheader("Aperçu des données")
        st.dataframe(df.head())
 
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
