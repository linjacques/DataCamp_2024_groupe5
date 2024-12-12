import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Tableau de bords")

if "dataframe" in st.session_state:
    
    df = st.session_state["dataframe"]  

    # Distribution des notes
    def display_note_distribution(df):
        if 'Note' in df.columns:
                note_counts = df['Note'].value_counts().sort_index() 
                st.write("### Distribution des notes (Allociné)")
                st.bar_chart(note_counts)
        else:
                st.error("La colonne 'Note' est absente du fichier CSV. Veuillez vérifier vos données.")

    # Moyenne des notes par année
    def display_mean_note_by_year(df):
        if 'Date de publication' in df.columns and 'Note' in df.columns:
                df['Note'] = pd.to_numeric(df['Note'], errors='coerce') 
                df['Annee'] = pd.to_datetime(df['Date de publication'], format='%d/%m/%Y', errors='coerce').dt.year
                df = df.dropna(subset=['Annee', 'Note'])

                df['Annee'] = df['Annee'].astype('str')  

                moyenne_par_annee = df.groupby('Annee')['Note'].mean().dropna()

                st.write("### Tableau des moyennes par année")
                st.line_chart(moyenne_par_annee)
        else:
                st.error("Les colonnes 'Date de publication' ou 'Note' sont absentes du fichier CSV. Veuillez vérifier vos données.")

    # Moyenne des notes par année et par genre
    def display_mean_note_by_year_by_genre(df):
        if 'Date de publication' in df.columns and 'Note' in df.columns and 'Genre 1' in df.columns:
                df['Note'] = pd.to_numeric(df['Note'], errors='coerce') 
                df['Annee'] = pd.to_datetime(df['Date de publication'], format='%d/%m/%Y', errors='coerce').dt.year
                df = df.dropna(subset=['Annee', 'Note', 'Genre 1'])
                
                # Liste des genres uniques
                genres = df['Genre 1'].unique()
                selected_genres = st.multiselect("Sélectionner un genre", options=genres, default='Action')
                
                df['Annee'] = df['Annee'].astype('str')
    
                if selected_genres:
                        filtered_df = df[df['Genre 1'].isin(selected_genres)]

                        moyenne_par_annee_genre = filtered_df.groupby(['Annee', 'Genre 1'])['Note'].mean().reset_index()

                        chart = alt.Chart(moyenne_par_annee_genre).mark_line(point=True).encode(
                        x='Annee:N',
                        y='Note:Q',
                        color='Genre 1:N',
                        tooltip=[
                                alt.Tooltip('Annee', title='Année'),
                                alt.Tooltip('Genre 1', title='Genre'),
                                alt.Tooltip('Note', title='Note Moyenne', format='.2f')
                        ]
                        ).properties(
                        title='Moyenne des notes par année et par genre'
                        ).interactive()

                        st.altair_chart(chart, use_container_width=True)
                else:
                        st.error("Veuillez sélectionner au moins un genre à afficher.")

    def generate_wordcloud(df):
        film_titles = df['Titre du film'].unique()
        selected_film_title = st.selectbox("Sélectionner un titre de film", options=film_titles)

        filtered_comments = df[df['Titre du film'] == selected_film_title]['Commentaire'].str.cat(sep=' ')

        stopwords_fr = STOPWORDS.union({'le', 'la', 'les', 'un', 'une', 'de', 'et', 'à', 'dans', 'ce', 'ces', 'pour', 'est', 'en', 'sur', 'qui', 'ce','se','que', 'mais', 'sont', 'avec','cest',"c'est",'plus', 'aux', 'ou', 'il', 'du', 'au', 'ne', 'pas', 'des', 'dun', 'une', 'par', 'comme', 'ont', 'leur', 'leurs', 'ils', 'elles', 'tout', 'tous', 'toutes', 'faire', 'fait', 'faite', 'faits', 'film','son', 'je', 'ça', 'ses', 'cette', 'très', 'vous', 'nous', 'meme', 'même', 'aussi'})
        
        wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords_fr).generate(filtered_comments)
        st.write("### Nuage de mots pour le film sélectionné")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    def display_csv(df):
        csv = df.to_csv(index=False) 
        st.download_button(
                label="Télécharger le CSV",
                data=csv,
                file_name="data_export.csv",
                mime="text/csv"
            )
        
    display_note_distribution(df)
    display_mean_note_by_year(df)
    display_mean_note_by_year_by_genre(df)
    generate_wordcloud(df)
    display_csv(df)

else:
    st.warning("Aucun fichier chargé. Veuillez d'abord charger un fichier dans la page **Exploration de fichier csv**.")