# Bonne pratique GIT
# Commandes à utiliser de façon récurrente

`git pull origin <nomDeLaBranche> <main> dans la plupart des cas` : permet de mettre à jour le repo d'une branche spécifique
`git branch <nomDeLaBranche>`: permet de créer une nouvelle branche
`git checkout -b <nomDeLaBranche>` : permet de créer une nouvelle branche et de se déplacer automatiquement sur celle-ci
`git checkout <nomDeLaBranche>` : permet de déplacer d’une branche à une autre, elle prend en argument la branche cible et aussi de supprimer les modifications qui ne sont pas ajoutées.

`git status` : permet d’afficher toutes les modifications non commités sur la branche courante.
`git add .` : permet d’ajouter les changements que nous avons fait dans nos fichiers sur la branche courante.
`git commit -m <nomDuCommit>` : permet de commiter les modifications que nous avons en local sur la branche courante.

`git push --set-upstream origin <nomDeLaBranche>` : permet de pusher sur la branche sur laquelle on bosse
`git push --set-upstream origin <test>` : permet de push ici par exemple sur test

`git merge <nomDeLaBranche>` : rapatrie les commits de la branche ciblée sur ma branche actuelle
Avant de merge toujours être sur la branche main pour rappatrié les commits d'une autre branche
puis faire un `git merge --continue` si besoin ou si conflit 

Si conflit et message d'erreur sur un commit en merge faire `wq` pour sortir du message d'erreur via la console 

`git branch -a` qui montre l'ensemble des branches existantes
main *
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

`git branch -d <nomDeLaBranche>` : permet de supprimer la branche sur le terminal après avoir merge
`git push origin --delete <nomDeBranche>` : permet de supprimer la branche en locale (sur gitHub)

`git log` : voir l’historique de tous les commits de la branche actuelle
`git log --oneline` : idem en version synthétique avec l'identifiant et le nom du commit simplifié

`git remote add correction <adresseDuRepo SSH>`
`git remote -v` : permet de lister les remotes qui sont actuellement liées à un repo local.
`git remote remove <nomduremote>` : permet de supprimer le remote lié au repo local

*Exemple :*

On clone un repo git (`git clone + le repo`)
On fait un npm init pour charger/ initialiser les packages (`npm init`)
On se crée une nouvelle branche via (`git branch <nomDeLaBranche>` puis faire un `git checkout <nomDeLaBranche>` ou sinon faire un `git checkout -b <nomDeLaBranche>` pour directement être sur la nouvelle branche)
En étant sur cette nouvelle branche qu'on appelera 'test' on fera des modifications par exemple: mettre un nouveau dossier JS ou modifier le md etc.
On vérifie bien avec le `git status` si cela a été modifié.
Après avoir fini les modifications on fera un `git add .`
Puis un `git commit -m 'Modifs rapides'`
On le pushera `git push --set-upstream origin <test>`

Après ceci on aura un message du style :

`remote: Create a pull request for 'test' on GitHub by visiting:
remote:      https://github.com/test/pull/new/
remote: 
To github.com:test
[new branch]      test -> test
Branch 'test' set up to track remote branch 'test' from 'origin'.`

On part sur gitHub et on ouvre le pull request on vérifie bien l'état du code modifié.

On repart sur le terminal toujours être au dossier du main puis un git merge test pour récupérer ce que nous avons modifier dans la branche test
A partir de là nous avons récupérer le code de la branche test sans pour le moment commit
Et par la suite on pourra tester les fonctionnalitées et puis commit sur la branche main

A savoir ne pas commit sur la branche main avant de prendre la décision à plusieurs et de pouvoir push correctement.

Idem on recrée un autre fichier ou dossier sur la branche test et qu'on fasse un commit sur la branche du test
On récupérera les infos du merge de la branche par la suite dans le dossier main

**Attention !**
1. 'TOUJOURS Faire les commit en anglais'
2. Faire des petits commit propres et explicites sur les changements apportés avec des mots clés adaptés comme task, features, doc, fonction, refactor, fix etc..
3. Ne pushez pas directement vers la branche main
Quel que soit le modèle de branchement git que vous utilisez, il est toujours judicieux d’activer la protection de branche git pour empêcher les validations directes et vous assurer que votre code de branche principal est déployable à tout moment. Toutes les validations doivent être transmises au main via des pull-requests.
4. Bien organiser les branches les nommers features branch

**Attention dans des cas plus complexes**
**Pour supprimer les commits d'une branche :**
Être sur la branche en question (git checkout <nomDeLaBranche>)

Utiliser `git reset HEAD~3` <- Permet de supprimer les 3 derniers commit selon le chiffre il supprimera le nombre de commit voulu
Si cela ne passe pas faire `git reset --hard HEAD`
HEAD : pour supprimer le dernier commit ;
HEAD^ : pour supprimer l'avant-dernier commit ;
Ensuite faire `git push --force` et le résultat est là !
Attention a bien faire le `git push --force` sinon ça ne sera pas pris en compte.

`git commit --amend`: permet de changer le nom du commit fait par erreur
Après qu'on ai tapé la ligne de git on arrive sur une ligne de commande qu'on devra changer par soit même puis faire controle x pour exit

*Fait par Thomas YU ©*
