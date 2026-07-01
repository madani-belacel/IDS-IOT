# Méthodologie d’évaluation et de correction d’un projet scientifique complet

Ce document décrit la méthodologie suivie pendant cette session pour analyser, évaluer et corriger un projet scientifique complet destiné à une publication de haut niveau, notamment dans un journal comme Computer Networks.

Il a été conçu pour être réutilisable sur d’autres projets techniques, scientifiques ou de recherche reproductible.

---

## 1. Objectif de la méthodologie

L’objectif est de produire une évaluation critique, professionnelle et constructive d’un projet scientifique en vérifiant :

- la qualité scientifique globale,
- la structure du manuscrit,
- la cohérence entre code, données, figures et texte,
- la reproductibilité,
- la qualité de la bibliographie,
- la capacité du projet à être publié dans une revue de haut niveau.

Cette méthodologie s’applique aussi bien à :

- un manuscrit LaTeX,
- un dépôt de code scientifique,
- une campagne expérimentale,
- un projet de simulation ou de calcul,
- un package de données et de scripts de traitement.

---

## 2. Philosophie générale de l’évaluation

L’évaluation suit trois principes fondamentaux :

1. Vérifier avant de conclure.
   - Toute affirmation sur la qualité, la compilation, les données ou la reproductibilité doit être étayée par une preuve concrète.

2. Séparer le potentiel scientifique des faiblesses techniques.
   - Un projet peut avoir une bonne idée scientifique mais être encore fragile sur le plan expérimental ou méthodologique.

3. Être honnête, constructif et précis.
   - Le but n’est pas de dénigrer le travail, mais d’identifier précisément ce qui empêche une publication de qualité.

---

## 3. Étapes d’analyse complète d’un projet scientifique

### Étape 1 — Comprendre la structure du projet

Avant toute correction, il faut cartographier le dépôt.

Actions typiques :

- lister les dossiers principaux,
- identifier les fichiers de manuscrit, code, données, scripts, figures, tables, documentation,
- repérer les fichiers d’entrée et de sortie principaux.

Exemples typiques :

- Manuscrit : main.tex, main-ieee.tex, sections/, tables/, Figures/, bib/
- Code : src/, code_source_*/, scripts/
- Données : data/, raw/, parsed/, estimated/
- Documentation : README.md, instruction.md, checklist.md, anomalies/

Objectif : obtenir une vue d’ensemble du projet et savoir où chercher les points de fragilité.

---

### Étape 2 — Lire les documents de présentation et de cadrage

On commence toujours par lire :

- README.md
- instruction.md
- checklist.md
- MASTER_TRACKER.md
- rapports internes d’audit si présents

Cela permet de comprendre :

- l’objectif scientifique du projet,
- son statut actuel,
- les hypothèses prises,
- les limites connues,
- les tâches déjà réalisées.

---

### Étape 3 — Analyser le manuscrit scientifique

Le manuscrit est évalué sur plusieurs plans :

- structure logique du papier,
- clarté de la contribution,
- qualité de la rédaction,
- cohérence des arguments,
- niveau de preuve apporté,
- adéquation au journal cible.

Points vérifiés :

- titre et résumé,
- introduction et positionnement,
- revue de littérature,
- modèle de menace, méthodologie, expérience,
- résultats et discussion,
- limites,
- conclusion,
- reproductibilité.

L’objectif est de déterminer si le papier dit clairement :

- quoi est proposé,
- pourquoi c’est important,
- comment cela a été évalué,
- et jusqu’où les conclusions peuvent aller.

---

### Étape 4 — Examiner le code source

Le code est analysé pour vérifier :

- la cohérence du design logiciel,
- la modularité,
- la présence de dépendances externes,
- la qualité des structures de données,
- la logique de calcul,
- la présence d’anomalies ou d’erreurs structurelles,
- la possibilité de reproduire les expériences.

On vérifie notamment :

- si les modules correspondent à la description du manuscrit,
- si les options de compilation sont raisonnables,
- si les scripts d’entrée/sortie sont cohérents,
- s’il existe de vrais flux de traitement de données et non seulement des placeholders.

---

### Étape 5 — Vérifier les données et leur provenance

Les données sont une partie essentielle de l’évaluation scientifique.

On inspecte :

- les données brutes,
- les données traitées,
- les fichiers CSV/TSV,
- les logs de campagne,
- les schémas de données,
- la provenance des chiffres figurant dans les figures et tableaux.

Questions clés :

- les données existent-elles réellement ?
- sont-elles cohérentes ?
- sont-elles structurées de façon exploitable ?
- les figures sont-elles alimentées par des données réelles ou par des placeholders ?

---

### Étape 6 — Vérifier la reproductibilité

Un projet scientifique sérieux doit permettre à un tiers de :

- compiler le manuscrit,
- exécuter les scripts,
- reproduire les figures,
- retrouver les données utilisées,
- comprendre les étapes de traitement.

On vérifie :

- la présence de scripts d’exécution,
- la présence d’instructions de build,
- la clarté de la chaîne de traitement des données,
- la disponibilité des artefacts nécessaires,
- la possibilité de relancer l’analyse de bout en bout.

---

### Étape 7 — Évaluer les figures et tableaux

Les figures et tableaux sont vérifiés pour leur :

- pertinence scientifique,
- lisibilité,
- cohérence avec les données,
- provenance documentaire,
- capacité à supporter les conclusions.

On regarde s’ils :

- portent sur les bons métriques,
- affichent bien les résultats essentiels,
- n’omettent pas les incertitudes et la variabilité,
- sont réellement interprétables.

---

### Étape 8 — Vérifier la qualité bibliographique

On inspecte la bibliographie pour s’assurer que :

- les références sont réelles,
- les métadonnées sont cohérentes,
- les DOI sont valides si disponibles,
- la bibliographie correspond bien au sujet,
- les références sont récentes et pertinentes,
- il n’y a pas de références douteuses, orphelines ou inutiles.

---

### Étape 9 — Produire un jugement critique équilibré

Le dernier pas consiste à synthétiser :

- les points forts,
- les faiblesses majeures,
- les anomalies critiques,
- les actions de correction prioritaires,
- la probabilité de publication après amélioration.

---

## 4. Commandes et techniques utilisées

### 4.1 Lecture de fichiers et navigation

Principales techniques :

- lecture directe de fichiers avec des outils de lecture de contenu,
- recherche de motifs dans les fichiers,
- navigation dans l’arborescence du projet,
- inspection des répertoires clés.

Exemples d’actions :

- lire [README.md](../README.md)
- lire [main.tex](../main.tex)
- lire [sections/experimental_setup.tex](../sections/experimental_setup.tex)
- lire [scripts/statistics/compute_statistics.py](../scripts/statistics/compute_statistics.py)

---

### 4.2 Recherche textuelle et regex

On utilise des recherches ciblées pour retrouver :

- des placeholders,
- des mots-clés de résultats,
- des références douteuses,
- des sections non cohérentes,
- des scripts de génération de figures,
- des chemins de données.

Exemples de motifs typiques :

- `TODO|TBD|placeholder|ESTIMATED`
- `\\cite\{[^}]+\}`
- `\\input\{.*\}`
- `data/real|parsed|aggregated`

---

### 4.3 Vérification de compilation LaTeX

Pour un manuscrit LaTeX, la commande de validation principale est :

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

En général, on relance la compilation plusieurs fois si nécessaire pour :

- résoudre les références,
- générer la bibliographie,
- stabiliser les références croisées.

Dans ce projet, cette vérification a été utilisée sur :

- [main.tex](../main.tex)
- [main-ieee.tex](../main-ieee.tex)

---

### 4.4 Vérification des PDFs générés

La vérification PDF consiste à :

- s’assurer que le PDF est bien généré,
- contrôler qu’il existe bien dans le dépôt,
- vérifier s’il correspond au manuscrit actuel,
- vérifier que les pages et la structure sont cohérentes.

---

### 4.5 Vérification du pipeline de données

Pour les projets de recherche reproductible, on exécute les scripts de traitement :

```bash
python3 scripts/statistics/compute_statistics.py --input data/real/parsed --output data/real/statistics
```

et éventuellement :

```bash
python3 scripts/python/generate_figures.py --csv data/real/parsed/agg --out Figures/
```

Objectif : vérifier que les données réelles peuvent produire des sorties exploitables.

---

### 4.6 Exécution des tests

Quand un projet contient des tests, on les exécute avec :

```bash
python3 -m unittest discover -s scripts/statistics -p 'test_*.py'
```

Cela permet de vérifier que les scripts de traitement et de validation ne se sont pas dégradés.

---

### 4.7 Vérification de la structure des données

On inspecte les fichiers CSV/TSV pour vérifier leur forme réelle, par exemple :

- présence de colonnes attendues,
- nombre de lignes,
- valeurs cohérentes,
- existence de modes de campagne ou scénarios attendus.

---

## 5. Démarches de correction des anomalies

### 5.1 Identifier la source du problème

Avant de corriger quoi que ce soit, il faut comprendre la cause réelle.

Exemples de causes fréquentes :

- un script n’attend pas le bon format de données,
- une colonne de CSV a un nom différent de celui attendu,
- le manuscrit affirme des résultats sans données correspondantes,
- une section de texte est trop vague ou non soutenue par des preuves,
- une référence bibliographique est douteuse ou mal structurée.

---

### 5.2 Corriger le problème à la source

La correction doit viser la cause et non seulement la conséquence.

Exemples :

- si le script ne lit pas correctement les données, corriger le parser,
- si la documentation dit une chose différente de l’état réel, l’aligner,
- si le manuscrit surestime les résultats, rephrasing et cadrage plus prudent,
- si les figures ne sont pas traçables, ajouter une provenance explicite.

---

### 5.3 Rendre les corrections vérifiables

Chaque correction est ensuite vérifiée par une preuve concrète :

- exécution du script,
- exécution des tests,
- compilation LaTeX,
- inspection des sorties générées,
- comparaison entre texte et artefacts.

---

### 5.4 Corriger la documentation pour éviter les régressions

Lorsqu’on corrige un problème, il faut souvent mettre à jour :

- README.md,
- instruction.md,
- checklist.md,
- rapports d’anomalies,
- documentation de données,
- commentaires dans les scripts.

Cela évite que le projet reste incohérent malgré les correctifs techniques.

---

## 6. Types d’anomalies typiquement recherchés

### 6.1 Anomalies structurelles

- fichiers manquants,
- incohérence entre dossiers et contenu,
- absence de documentation essentielle,
- structure de projet mal organisée.

### 6.2 Anomalies de manuscrit

- texte trop affirmatif pour les preuves disponibles,
- manque de cadrage scientifique,
- incohérences entre résultats et discussion,
- figures ou tableaux mal justifiés.

### 6.3 Anomalies de code

- scripts ne lisant pas correctement les données,
- mauvais schémas de colonnes,
- logique non robuste,
- dépendances mal documentées.

### 6.4 Anomalies de données

- absence de données réelles,
- données mal interprétées,
- fichiers de sortie vides ou incomplets,
- provenance non traçable.

### 6.5 Anomalies de reproductibilité

- scripts non exécutables ou non documentés,
- étapes de traitement mal décrites,
- manque de traçabilité entre résultats et sources.

### 6.6 Anomalies de bibliographie

- références douteuses,
- DOI manquants ou invalides,
- références non pertinentes,
- références orphelines ou peu utiles.

---

## 7. Bonnes pratiques pour rendre un projet publiable dans un journal de haut niveau

### 7.1 Prioriser la crédibilité scientifique

Un manuscrit de haut niveau doit être crédible, pas seulement bien écrit.

Cela implique :

- des résultats réellement soutenus par des données,
- une méthodologie claire,
- une discussion prudente et précise,
- des limites honnêtes.

---

### 7.2 Éviter les sur-claims

Ne pas présenter un résultat comme solide si l’évidence n’est pas encore assez forte.

En pratique :

- utiliser un langage prudent pour les études pilotes,
- éviter les généralités excessives,
- ne pas prétendre à une validité de grande échelle sans la preuve correspondante.

---

### 7.3 Rendre le travail reproductible

Un projet de qualité de revue doit permettre à un lecteur de relancer les étapes de travail.

Cela demande :

- des scripts propres,
- des données bien structurées,
- une documentation précise,
- des instructions de build claires,
- une traçabilité explicite entre données et figures.

---

### 7.4 Soigner la qualité des figures et tableaux

Les figures doivent être :

- lisibles,
- interprétables,
- directement liées aux résultats,
- accompagnées d’une légende claire.

Les tableaux doivent :

- être cohérents,
- montrer les bonnes métriques,
- indiquer les incertitudes quand elles sont pertinentes.

---

### 7.5 Travailler la bibliographie comme un composant scientifique à part entière

Une bonne bibliographie n’est pas seulement une liste de références :

- elle doit refléter l’état de l’art,
- montrer la différence de la contribution,
- être proprement formattée,
- éviter les références faibles ou douteuses.

---

### 7.6 Séparer clairement ce qui est démontré de ce qui est proposé

Un bon manuscrit distingue :

- ce qui a été démontré expérimentalement,
- ce qui est une hypothèse ou une implication,
- ce qui reste à valider.

C’est essentiel pour garder la rigueur scientifique.

---

## 8. Méthodologie pratique appliquée pendant cette session

### 8.1 Analyse initiale

- lecture du dépôt et des documents de cadrage,
- lecture du manuscrit principal et de la version IEEE,
- inspection du code, des scripts et des données,
- identification des anomalies de structure, de cohérence et de validité scientifique.

### 8.2 Vérification technique

- compilation du manuscrit LaTeX,
- vérification de la présence des PDF,
- exécution des scripts de statistiques et de génération de figures,
- exécution des tests associés au pipeline.

### 8.3 Correction ciblée

- correction du pipeline de lecture des données,
- normalisation des champs de données et des modes de campagne,
- mise à jour de la documentation pour refléter l’état réel du projet,
- amélioration du cadrage du manuscrit pour éviter les sur-claims.

### 8.4 Validation finale

- re-exécution des tests,
- re-exécution des scripts,
- re-compilation du manuscrit,
- vérification de la cohérence globale.

---

## 9. Checklist de relecture réutilisable

Avant de considérer un projet prêt pour une revue sérieuse, je vérifie :

- [ ] le projet a une structure claire,
- [ ] le manuscrit est cohérent et bien organisé,
- [ ] les résultats sont soutenus par des données réelles,
- [ ] les scripts fonctionnent,
- [ ] les figures et tableaux sont traçables,
- [ ] la reproductibilité est démontrable,
- [ ] la bibliographie est propre et pertinente,
- [ ] les limites sont honnêtes,
- [ ] les conclusions ne dépassent pas les preuves.

---

## 10. Conclusion

Cette méthodologie permet d’évaluer un projet scientifique de manière rigoureuse, équilibrée et utile à la publication. Elle ne vise pas seulement à “trouver des erreurs”, mais à transformer un projet prometteur en un artefact plus solide, plus crédible et plus proche du standard d’un journal de haut niveau.

L’essentiel est de combiner :

- une lecture critique du manuscrit,
- une vérification technique du code et des données,
- une évaluation de la reproductibilité,
- et une correction ciblée, fondée sur des preuves.
