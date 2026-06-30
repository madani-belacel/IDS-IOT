# Audit Prompt — RPL-ClusterIDS Manuscript (Computer Networks / Elsevier)

Tu es un auditeur LaTeX très rigoureux spécialisé dans les articles de recherche.

## Contexte

- **Projet** : `/home/madani/contiki-ng/examples/IDS_IOT/`
- **Journal** : Computer Networks (Elsevier)
- **Classe** : `elsarticle [preprint,12pt,number]`
- **Style biblio** : `elsarticle-num.bst`
- **Compilation** : `pdflatex main && bibtex main && pdflatex main && pdflatex main`
- **État actuel** : 34 pages, 0 LaTeX errors, 0 undefined control sequences.

## Anomalies déjà corrigées (à ne pas re-signaler)

- L1 : `\cormark[1]` vs `\cortext[cor1]` → fixé
- L2 : sections manquantes (limitations, reproducibility) → ajoutées
- L3-L4 : "IEEE IoT Journal" dans conclusion/reproducibility → "Computer Networks"
- L5 : "(estimated pending)" dans introduction → "(Phase~2 campaign)"
- L8-L10 : macros mortes dans status-macros.tex → nettoyées
- F3 : symlink `data/real/parsed/` créé
- R1-R4 : entrées bib fabriquées → remplacées
- C1 : `alerts_hour` incrémenté (clusterids-node.c:133)
- C2 : prototype `ch_elect_tenure_s()` ajouté dans ch_elect.h
- C4 : rotation counter corrigé (head incrémente aussi)
- O1-O12 : fichiers orphelins nettoyés
- Highlights section ajoutée (elsarticle)
- Tableaux VI (total samples = 4 009 612), VIII (Full + NOML remplis)
- Figures 4-11 : réécrites en PGFPlots lisant les CSV agrégés
- Variants d'ablation NOCLUS/NOML/NOCTX/NOENR : Makefile + code C + compilation OK
- `reproducibility.tex` : nettoyé (plus de main-ieee, ESTIMATED, generate_figures.py)

## Travail demandé

Parcourt TOUS les fichiers `.tex`, `.bib`, `.c`, `.h` du projet et identifie TOUTE anomalie restante. Sois exhaustif : vérifie chaque `\ref{}`/`\label{}`, chaque `\cite{}`, chaque `\input{}`, chaque warning LaTeX, chaque commentaire de code, chaque métadonnée, chaque coin du projet.

Ne te limite PAS à une simple recherche textuelle. Vérifie la cohérence SÉMANTIQUE : les valeurs dans les tableaux correspondent-elles aux données parsées ? Le texte des sections décrit-il correctement ce que les figures montrent ? Les métriques sont-elles plausibles ?

**Rapporte TOUT** avec le chemin exact du fichier, le numéro de ligne, et une description de l'anomalie. Classe par sévérité (critical/high/medium/low/info).
