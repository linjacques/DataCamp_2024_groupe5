# Projet Data Camp groupe 5 :

- Amir ANCIAUX
- Noam BOULZE
- Thomas COUTAREL
- Jacques LIN
- Thomas YU

## ALLOCINE / IMDb

Bienvenue dans le README de notre projet Data Camp.

Pour commencer, il faut commencer par récupérer les fichiers et installer toutes les dépendances.

On télécharge le dépôt Github :
```bash
git clone https://github.com/linjacques/DataCamp_2024_groupe5
```

Ici on va installer toutes les dépendances requises dans un fichier requirements.txt :
```bash
pip install -r requirements.txt
```

Enfin on va pouvoir lancer le code, en exécutant le fichier Python dans [Visual Studio Code](https://code.visualstudio.com/), [Jupyter Notebook](https://jupyter.org/) ou un autre éditeur de code.

Pour la visualisation il faudra installer [Streamlit](https://streamlit.io/).

Dans le dépot github vous retrouverez le fichier csv brut des données, que l'on récupère après le webscrapping et le fichier csv finale que l'on récupère pour l'analyse de données.

# Comment ça fonctionne ?

## Le scrapping de données : 

La première partie du code est dédiée au webscrapping, en effet pour nôtre problématique il n'existe pas de dataset déjà fait sur lequel on aurais qu'à faire de l'analyse de sentiment et de la visualisation à partir de ses résultats. 
On va devoir récupérer nous-même les données.
On a récupéré les données des sites [AlloCiné](https://www.allocine.fr/), [IMDb](https://www.imdb.com/) plus spécifiquement la liste des avis de films ou de séries.

## L'analyse de sentiment :

Pour l'analyse de sentiment, on utlisera [roBERTa](https://huggingface.co/docs/transformers/model_doc/roberta).

## La visualisation :

La visualisation sera faite pour créer des dashboards interactifs et montrer comment on pourra interpréter nos données.

## Le déploiement sur le cloud : 

Le deploiement se fera sur Streamlit 

## Contribution

Les contributions font de la communauté open source un endroit incroyable pour apprendre, s'inspirer et créer.
Toute contribution que vous apportez est **grandement appréciée**.

Si vous avez une suggestion pour améliorer ce projet, veuillez forker le dépôt et créer une pull request.
Vous pouvez également ouvrir une issue avec le tag "enhancement".
N'oubliez pas de donner une étoile au projet !
Merci encore !

1. Forkez le projet
2. Créez votre branche de fonctionnalité (git checkout -b feature/NouvelleFonctionnalité)
3. Faites vos commits (git commit -m 'Ajout de NouvelleFonctionnalité')
4. Poussez vers la branche (git push origin feature/NouvelleFonctionnalité)
5. Créez une Pull Request

### Contact

> Product Owner : Thomas Y.

> Data Engineer : Thomas C. / Amir A.

> Data Analyst : Jacques L. / Noam B.

> Git Master : Thomas Y.