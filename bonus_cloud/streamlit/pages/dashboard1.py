import csv
import chardet
import pandas as pd
import streamlit as st

st.title("Exploration des fichiers CSV")

st.markdown("""
### Aperçu du fichier
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
