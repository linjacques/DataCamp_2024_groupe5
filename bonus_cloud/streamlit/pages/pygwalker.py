import streamlit as st
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
import plotly.express as px

st.title("Tableau de bords")

if "dataframe" in st.session_state:
    
    df = st.session_state["dataframe"]  

    if 'Note' in df.columns:
            note_counts = df['Note'].value_counts().sort_index() 
            st.write("### Distribution des notes (Allociné)")
            st.bar_chart(note_counts)
    else:
            st.error("La colonne 'Note' est absente du fichier CSV. Veuillez vérifier vos données.")

    if 'Date de publication' in df.columns and 'Note' in df.columns:
            df['Note'] = pd.to_numeric(df['Note'], errors='coerce')  # Convertir en float, remplacer erreurs par NaN
            df['Annee'] = pd.to_datetime(df['Date de publication'], format='%d/%m/%Y', errors='coerce').dt.year
            df = df.dropna(subset=['Annee', 'Note'])

            df['Annee'] = df['Annee'].astype('str')  # Utilisation du type 'Int64' pour conserver les entiers
            # Calculer la moyenne des notes par année
            moyenne_par_annee = df.groupby('Annee')['Note'].mean().dropna()

            # Afficher les moyennes sous forme de tableau
            st.write("### Tableau des moyennes par année")
            st.line_chart(moyenne_par_annee)

            csv = df.to_csv(index=False) 
            st.download_button(
                label="Télécharger le CSV",
                data=csv,
                file_name="data_export.csv",
                mime="text/csv"
            )
    else:
            st.error("Les colonnes 'Date de publication' ou 'Note' sont absentes du fichier CSV. Veuillez vérifier vos données.")
else:
    st.warning("Aucun fichier chargé. Veuillez d'abord charger un fichier dans la page **Exploration de fichier csv**.")


# pyg_app = StreamlitRenderer(df)
# pyg_app.explorer()