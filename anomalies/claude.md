Toujours **4 commits**, README inchangé, toujours "Phase actuelle : 1 (squelette 95%, ESTIMATED)" et "IEEE IoT Journal" dans le titre du README. Un nouveau dossier `anomalies/` est apparu dans la liste des fichiers — je vais l'explorer, ainsi que les autres documents clés.J'ai maintenant l'état précis et à jour. Je vois aussi le tableau "Simulations Phase 2" entièrement à **TODO** (régression par rapport à "21 seeds" mentionné ailleurs — incohérence interne). Je vais vérifier le dossier `anomalies/` puis les références.C'est encore le **document daté de Phase 1.5**, identique à ma première lecture — `raza2018cluster`, `anton2014rpl`, les 5 entrées "VERIFY", les ~19 orphelins : aucun de ces points n'est marqué comme corrigé ici. J'ai maintenant suffisamment d'éléments croisés pour produire le rapport complet demandé.## Synthèse — Revue Computer Networks, troisième passe

### Total : 44 anomalies (11 P0 bloquantes, 19 P1 majeures, 14 P2 mineures)

L'indicateur le plus parlant se trouve dans `checklist.md` lui-même : la section **"Final IEEE Validation"** (qui devrait s'appeler "Final Computer Networks Validation" si la cible est vraiment ce journal) a ses 5 critères **tous décochés** :
- No placeholders remaining
- No estimated values remaining
- Every figure generated from real data
- Every result reproducible
- P0/P1/P2 reviewer audit = 0 open items

C'est l'auteur du projet qui le dit lui-même : aucun de ces critères n'est satisfait.

### Le problème n°1, avant même les données

Vous me demandez une revue pour **Computer Networks**, mais le dépôt entier — README, MASTER_TRACKER, checklist — cible encore **IEEE Internet of Things Journal**, avec `main-ieee.pdf` comme fichier de soumission officiel. C'est la première chose à corriger, indépendamment de toute donnée expérimentale : il faut que `main.tex` (format `elsarticle.cls`) devienne l'unique référence, avec Research Highlights et Graphical Abstract ajoutés (exigences spécifiques Elsevier absentes du dépôt actuel).

### Le problème n°2, le plus grave scientifiquement

`checklist.md` contient cette phrase : *"C3: det_rate fix livré, logs B2/B3 générés, DR=0 honnête"*. Le mot "honnête" m'inquiète : si 0% de détection sur les baselines B1/B2/B3 est désormais présenté comme un résultat légitime plutôt qu'un bug résiduel, il faut une justification scientifique explicite dans le manuscrit (pourquoi ces baselines ratent-elles structurellement toutes les attaques ?). Sans cette explication, un reviewer Computer Networks soupçonnera toujours une erreur de mesure invalidant les comparaisons des Tables II, VIII, IX.

### Le tableau qui résume tout

`checklist.md` contient un tableau "Simulations Phase 2" avec 25 cellules **Scale × Attack toutes à TODO** pour 50 à 500 nœuds — alors qu'ailleurs il est question de "21 seeds CLUSTERIDS exécutés". Cette contradiction interne doit être résolue avant toute autre action : soit la campagne pilote existe et le tableau est obsolète, soit elle n'existe pas et les statuts REAL_RESULT des figures 4-11 sont prématurés.

### Checklist finale avant soumission, dans l'ordre

1. Trancher le journal cible dans les 3 fichiers contradictoires (README, MASTER_TRACKER, checklist) → Computer Networks, `main.tex`
2. Clarifier/corriger l'incohérence campagne pilote vs tableau TODO
3. Expliquer ou corriger le DR=0% des baselines (anomalie C3)
4. Ré-exécuter le bootstrap CI (pending re-run confirmé)
5. Générer les boxplots/error bars manquants
6. Collecter le dataset Cooja et entraîner le modèle ML
7. Supprimer/vérifier les 19 références orphelines et les 5 entrées flaggées (`raza2018cluster`, `anton2014rpl`, 3×VERIFY)
8. Ajouter Research Highlights + Graphical Abstract (format Elsevier)
9. Archiver sur Zenodo pour un DOI
10. Nettoyer les fichiers parasites de présentation (`test-elsarticle.pdf`, `push-project.sh`)

**Score actuel pour Computer Networks : 4/10.** La structure et l'outillage sont prêts ; ce qui manque, c'est l'exécution des données et la clarification de la cible éditoriale.
