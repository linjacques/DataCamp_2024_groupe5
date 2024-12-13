# Datacamp Groupe 5 :

- Amir ANCIAUX
- Noam BOULZE
- Thomas COUTAREL
- Jacques LIN
- Thomas YU

## Datacamp

Bienvenue dans le README de notre projet Datacamp. 
Ce document vous guide pas à pas pour installer, utiliser et comprendre les différentes étapes de notre projet.

---

## Installation

### 1. Cloner le dépôt GitHub

Pour récupérer le projet, utilisez la commande suivante dans votre terminal, via l'éditeur de code de votre choix :

```bash
git clone https://github.com/linjacques/DataCamp_2024_groupe5
```

### 2. Installer les dépendances

Une fois le dépôt cloné, installez les dépendances nécessaires en exécutant la commande suivante :

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application en local

Rendez-vous dans le dossier `streamlit` situé dans `bonus_cloud` et lancez l'application avec la commande suivante :

```bash
streamlit run .\app.py
```

Cela ouvrira une version locale de l'application dans votre navigateur.

### 4. Accéder à la version cloud

Pour accéder à la version cloud de l'application, utilisez ce lien :
[Streamlit Cloud App](https://linjacques-datacamp-2024-groupe5-bonus-cloudstreamlitapp-og7ob2.streamlit.app/).

Nous recommandons d'utiliser cette version cloud pour tester et manipuler toutes les fonctionnalités sans configuration supplémentaire.

---

## Fonctionnement du projet

### 1. Scrapping de données

Notre projet commence par une étape de **web scraping** car il n'existait pas de dataset adapté à notre problématique. Nous avons récupéré les données à partir de sites d'avis de films tels que :

- [AlloCiné](https://www.allocine.fr/)
- [Rottentomatoes](https://rottentomatoes.com/)

Pour ce faire, nous avons utilisé plusieurs librairies Python :

- **BeautifulSoup** : pour extraire les éléments HTML nécessaires.
- **Scrapy** : pour parcourir et collecter les données de manière performante.
- **Selenium** : pour manipuler les pages dynamiques nécessitant du JavaScript.

L'utilisation combinée de ces librairies a permis de répondre aux exigences du **BONUS** technique.

### 2. Nettoyage des données

Les données brutes issues du scraping ont été nettoyées et standardisées pour être exploitables. Voici les principales étapes :

- **Formatage des dates** : les dates (de sortie et de commentaires) ont été converties au format standard `DD/MM/YYYY`.
- **Standardisation des notes** :
  - Remplacement des valeurs non adaptées par `NULL`.
  Les valeurs `NULL` sont quand à eux aussi remplacer par la moyenne des notes collectées pour le film en question.
  - Conversion des formats, par exemple `3,5` en `3.5`.
- **Uniformisation des URLs** :
  - Une boucle a été créée pour nettoyer et standardiser les URLs.
  - Conversion des noms en minuscules avec des underscores pour Rotten Tomatoes.
- **Gestion des utilisateurs** :
  - Si un nom était absent, l'utilisateur était désigné comme "Visiteur".
  - Sinon, le nom ou un ID utilisateur a été enregistré.
- **Filtrage des mots** : Suppression des mots vides (*stopwords*) et des termes vulgaires en français et anglais.

### 3. Analyse de sentiment

Pour analyser les sentiments exprimés dans les commentaires, nous avons utilisé le modèle pré-entraîné **roBERTa** via la librairie [Transformers](https://huggingface.co/docs/transformers).

- **Modèle final** :
  - Après avoir testé plusieurs modèles (notamment avec des datasets spécifiques d'AlloCiné), nous avons retenu `lyxuand/distilbert`, qui s'est révélé le plus performant.
- **Pipeline** :
  - Extraction des sentiments (positif, négatif, neutre) directement utilisable dans l'interface graphique.

### 4. Visualisation des données

Pour présenter les résultats de manière intuitive, nous avons développé des visualisations interactives via **Streamlit** et **Tableau** :

- **Dashboards dynamiques** : pour explorer et analyser les données.
- **Nuage de mots** : réalisé avec la librairie **WordCloud** pour mettre en avant les termes les plus fréquents.
- **Graphiques simples et clairs** : tels que des histogrammes et des diagrammes circulaires pour une compréhension rapide.

### 5. Déploiement sur le cloud

Le déploiement a été effectué sur **Streamlit Cloud**, qui offre une intégration fluide avec notre repository GitHub. L'interface utilisateur est conviviale, permettant de tester toutes les fonctionnalités sans avoir à exécuter de code localement.

Lien de l'application déployée : [Streamlit Cloud App](https://linjacques-datacamp-2024-groupe5-bonus-cloudstreamlitapp-og7ob2.streamlit.app/).

---

## Contribution

Les contributions font de la communauté open source un endroit incroyable pour apprendre, s'inspirer et créer.
Toute contribution que vous apportez est **grandement appréciée**.

Si vous avez une suggestion pour améliorer ce projet, veuillez forker le dépôt et créer une pull request.
N'oubliez pas de donner une étoile au projet !
Merci encore !

1. Forkez le projet
2. Créez votre branche de fonctionnalité (git checkout -b feature/NouvelleFonctionnalité)
3. Faites vos commits (git commit -m 'Ajout de NouvelleFonctionnalité')
4. Poussez vers la branche (git push origin feature/NouvelleFonctionnalité)
5. Créez une Pull Request

## Contact

> Product Owner : Thomas Y.

> Data Engineer : Thomas C. / Amir A.

> Data Analyst : Jacques L. / Noam B.

> Git Master : Thomas Y.