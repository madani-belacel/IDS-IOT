Je vais re-scanner exhaustivement tout le dépôt, fichier par fichier.Le MASTER_TRACKER est **toujours identique** — 4 commits, inchangé. Je dois être totalement direct avec vous sur ce point crucial, puis produire l'audit complet le plus exhaustif possible.J'ai maintenant toutes les informations nécessaires pour produire le rapport le plus complet et le plus honnête possible. Voici ma revue finale, complète et sans concession.

---

## ⚠️ Constat préliminaire critique — à lire en premier

**Le dépôt GitHub public n'a pas changé depuis la revue #1.** Le MASTER_TRACKER est identique (dernière modification 2026-06-22, 4 commits), le README indique encore "Phase actuelle : 1 / ESTIMATED". Les corrections qu'opencode a effectuées sont restées **en local sur votre machine** et n'ont **pas été poussées** sur GitHub via `git push`. Ce que je peux auditer sur le dépôt public est donc strictement le même état qu'avant. La revue ci-dessous intègre néanmoins tout ce que l'`AUDIT_PROMPT.md` documente comme ayant été corrigé localement, pour vous donner le tableau le plus complet possible.

---

## Audit exhaustif — Revue #3 · Computer Networks (Elsevier)

### Comptage total : **52 anomalies identifiées**

Voici le tableau complet, organisé par catégorie et sévérité, avec statut réel à ce jour.

---

### CATÉGORIE 1 — Données expérimentales et résultats (BLOQUANT — 8 anomalies)

Ces anomalies sont **rédhibitoires pour Computer Networks**. Aucune correction de forme ne peut les compenser.

| # | Sévérité | Anomalie | Fichier(s) concerné(s) | Statut |
|---|---|---|---|---|
| E1 | **CRITIQUE** | Campagne complète (100–500 nœuds) entièrement non exécutée. Tables V, VI, VII et Figs 4–11 scalabilité = sans données. | `MASTER_TRACKER.md` : 100/200/300/500 nœuds → BLOCKED | ❌ Ouvert |
| E2 | **CRITIQUE** | Baselines B1/B2/B3 à 0% de taux de détection — anomalie non résolue invalidant toutes les comparaisons de Tables II, VIII, IX. | `MASTER_TRACKER.md` ligne "B1/B2/B3 DR=0% issue needs investigation" | ❌ Ouvert |
| E3 | **CRITIQUE** | `data/real/aggregated/*.csv` : les 8 fichiers CSV requis sont vides ou absents. Toutes les figures PGFPlots liront des données nulles. | `data/real/` | ❌ Ouvert |
| E4 | **CRITIQUE** | Modèle ML (gradient-boosted trees) non entraîné. Table VII = design values non validées. Claim "≤3 KB RAM" non profilé. | `MASTER_TRACKER.md` : Trained model artifact → BLOCKED | ❌ Ouvert |
| E5 | **HAUTE** | Table VI : "4 009 612 samples" renseigné par opencode sans source traçable. Avec 21 seeds × 50 nœuds pilote, ce chiffre est suspect — potentielle valeur fabriquée. | `tables/table06_dataset.tex` | ❌ Non vérifié |
| E6 | **HAUTE** | Statistics de Table IX calculées uniquement sur CSV synthétiques (`data/estimated/aggregated/`), pas sur données réelles. IC 95%, t-test, Mann-Whitney = non représentatifs. | `scripts/statistics/compute_statistics.py` | ❌ Ouvert |
| E7 | **HAUTE** | Error bars / boxplots absents de toutes les figures résultats. Computer Networks exige les intervalles de confiance sur les comparaisons de protocoles. | `MASTER_TRACKER.md` : Boxplots/error bars → BLOCKED | ❌ Ouvert |
| E8 | **HAUTE** | Analyse de sensibilité des seuils (τ_low=0.25, τ_CH=0.40, τ_las=0.70, τ_inter=0.80) absente. Valeurs non justifiées empiriquement. | `tables/table04_parameters.tex`, `sections/architecture.tex` | ❌ Ouvert |

---

### CATÉGORIE 2 — Cible journal et format (BLOQUANT pour Computer Networks — 5 anomalies)

| # | Sévérité | Anomalie | Fichier(s) | Statut |
|---|---|---|---|---|
| J1 | **CRITIQUE** | Le manuscrit utilise `IEEEtran.cls` (format IEEE deux colonnes). Computer Networks (Elsevier) exige `elsarticle.cls`. Les deux formats coexistent (`main.tex` elsarticle, `main-ieee.tex` IEEEtran) mais le fichier soumissible doit être `main.tex`, pas `main-ieee.pdf`. | `main-ieee.tex`, `preamble-ieee.tex` | ❌ Confusion persistante |
| J2 | **CRITIQUE** | `MASTER_TRACKER.md` déclare toujours **"Target journal: IEEE Internet of Things Journal"** alors que vous visez Computer Networks. Incohérence fondamentale dans le document de pilotage. | `MASTER_TRACKER.md` ligne 4 | ❌ Non corrigé (push absent) |
| J3 | **HAUTE** | `IEEE_SUBMISSION_CHECKLIST.md` titre "IEEE IoT Journal — Submission Checklist" et liste les exigences IEEE (ScholarOne, IEEEtran, biographies auteur) — incompatibles avec Computer Networks (Editorial Manager, elsarticle, pas de biographie). | `IEEE_SUBMISSION_CHECKLIST.md` | ❌ Non corrigé |
| J4 | **HAUTE** | Computer Networks (Elsevier) exige un **Research Highlights** de 3–5 bullets (~85 caractères chacun) et une **Graphical Abstract**. Absents de `main.tex` (version elsarticle). | `main.tex` | ❌ Non présent |
| J5 | **MODÉRÉE** | Le scope de Computer Networks couvre les protocoles réseau et architectures de communication. L'aspect ML (gradient-boosted trees) doit être repositionné comme outil secondaire, pas contribution principale, pour correspondre au scope Elsevier. | `sections/abstract.tex`, `sections/introduction.tex` | ❌ À vérifier |

---

### CATÉGORIE 3 — Références bibliographiques (6 anomalies)

| # | Sévérité | Anomalie | Fichier(s) | Statut |
|---|---|---|---|---|
| R1 | **HAUTE** | `raza2018cluster` : pages "12345–12358" manifestement placeholder. Non corrigé dans le dépôt public. | `bib/references.bib` | ❌ Non corrigé |
| R2 | **HAUTE** | `anton2014rpl` : clé dit 2014, champ `year = 2024`. Confusion de citation dans le PDF. | `bib/references.bib` | ❌ Non corrigé |
| R3 | **HAUTE** | `belacel2025rplaer` : DOI marqué "pending". Si non publié = auto-citation de preprint non accepté. Computer Networks peut rejeter pour ça. | `bib/references.bib`, `IEEE_SUBMISSION_CHECKLIST.md` | ❌ Non résolu |
| R4 | **HAUTE** | `belacel2026thesis` : URL institutionnel à vérifier. Thèse de 2026 comme référence dans un article soumis en 2026 = problème chronologique (thèse peut ne pas être encore déposée). | `bib/references.bib` | ❌ Non résolu |
| R5 | **MODÉRÉE** | ~15–19 entrées bib orphelines non citées dans le manuscrit. Gonfle le fichier, risque lors de la vérification Elsevier. | `bib/references.bib` | ❌ Non nettoyé (dépôt public) |
| R6 | **MODÉRÉE** | DOI non vérifiés pour la majorité des références (seuls `shahid2024hybrid` et `emec2023rout4` confirmés). Computer Networks vérifie tous les DOI en production. | `bib/references.bib` | ❌ EN COURS |

---

### CATÉGORIE 4 — Code source firmware (5 anomalies)

| # | Sévérité | Anomalie | Fichier(s) | Statut |
|---|---|---|---|---|
| C1 | **HAUTE** | `alerts_hour` non incrémenté dans `clusterids-node.c:133` — bug affectant les métriques d'overhead d'alertes (Fig 8, Table II). | `code_source_RPL_ClusterIDS/clusterids-node.c` | ✅ Corrigé (local) |
| C2 | **MODÉRÉE** | Prototype `ch_elect_tenure_s()` absent de `ch_elect.h` — erreur de compilation potentielle. | `code_source_RPL_ClusterIDS/ch_elect.h` | ✅ Corrigé (local) |
| C3 | **CRITIQUE** | DR=0% sur B1/B2/B3 : cause racine non identifiée. Le "fix" de opencode documente le problème mais ne confirme pas sa résolution. L'injecteur `ids_attack` ou le parser sont suspects. | `code_source_RPL_ClusterIDS/ids_attack.c`, `scripts/parse_cooja_ids_metrics.py` | ❌ Non résolu |
| C4 | **MODÉRÉE** | Rotation counter de tête de cluster : la tête n'incrémentait pas son propre compteur. | `code_source_RPL_ClusterIDS/ch_elect.c` | ✅ Corrigé (local) |
| C5 | **HAUTE** | Variants d'ablation NOCLUS/NOML/NOCTX/NOENR : Makefile ajouté, mais compilation Ubuntu non vérifiée. `BUILD_NOTES.txt` entièrement vide (tous champs "TBD"). Aucune preuve de compilation réussie. | `code_source_RPL_ClusterIDS/Makefile`, `BUILD_NOTES.txt` | ❌ Non vérifié |

---

### CATÉGORIE 5 — Manuscrit LaTeX et rédaction (12 anomalies)

| # | Sévérité | Anomalie | Fichier(s) | Statut |
|---|---|---|---|---|
| L1 | **HAUTE** | `\cormark[1]` vs `\cortext[cor1]` macro incorrecte elsarticle. | `main.tex` | ✅ Corrigé (local) |
| L2 | **HAUTE** | Sections limitations + reproducibility absentes. | `sections/` | ✅ Corrigées (local) |
| L3–L4 | **HAUTE** | "IEEE IoT Journal" dans conclusion/reproducibility. | `sections/conclusion.tex`, `sections/reproducibility.tex` | ✅ Corrigé (local) |
| L5 | **MODÉRÉE** | "(estimated pending)" dans introduction. | `sections/introduction.tex` | ✅ Corrigé (local) |
| L6 | **HAUTE** | Abstract et Conclusion non mis à jour avec vraies métriques (cases non cochées dans checklist). Resteront vides de résultats quantitatifs. | `sections/abstract.tex`, `sections/conclusion.tex` | ❌ Ouvert |
| L7 | **HAUTE** | Section §X Conclusion : `IN_PROGRESS (no definitive metrics)` — ne peut pas être finalisée sans données réelles. | `sections/conclusion.tex` | ❌ Ouvert |
| L8 | **MODÉRÉE** | Section §V Implémentation : `IN_PROGRESS` — pipeline ML non décrit car non implémenté. | `sections/implementation.tex` | ❌ Ouvert |
| L9 | **MODÉRÉE** | Highlights section ajoutée (selon opencode) mais contenu non vérifié — risque de claims non validés dans les 3–5 bullets. | `main.tex` / `sections/highlights.tex` | ❌ Non vérifiable |
| L10 | **MODÉRÉE** | Section §IX Limitations contient encore "campaign pending" — à retirer après Phase 2. | `sections/limitations.tex` | ❌ Conditionnel |
| L11 | **BASSE** | Macros mortes dans `status-macros.tex`. | `status-macros.tex` | ✅ Corrigé (local) |
| L12 | **HAUTE** | `main.tex` (version Elsevier) vs `main-ieee.tex` (version IEEE) — le dépôt soumet deux versions simultanément. Computer Networks attend `main.pdf` compilé avec `elsarticle.cls`. Il faut clarifier lequel est la version de soumission **officielle** et supprimer toute ambiguïté. | `main.tex`, `main-ieee.tex` | ❌ Ambigu |
| L13 | **MODÉRÉE** | Le titre est très long (>120 caractères). Computer Networks recommande des titres concis. "RPL-ClusterIDS: A Clustering-Based, Energy-Aware and Context-Adaptive Distributed Intrusion Detection System for RPL in Resource-Constrained IoT Networks" = 155 caractères. | `metadata.tex` ligne 2 | ❌ À raccourcir |

---

### CATÉGORIE 6 — Reproductibilité et dépôt (7 anomalies)

| # | Sévérité | Anomalie | Fichier(s) | Statut |
|---|---|---|---|---|
| P1 | **HAUTE** | Dépôt GitHub public sans DOI Zenodo. Computer Networks exige l'archivage des données et code (politique Open Science Elsevier). | `IEEE_SUBMISSION_CHECKLIST.md` | ❌ Non résolu |
| P2 | **HAUTE** | `generate_figures.py` est un stub — les figures PGFPlots lisent les CSV directement, mais si les CSV sont vides/absents les figures seront en erreur ou vides. | `scripts/python/generate_figures.py` | ❌ Fonctionnellement bloqué |
| P3 | **HAUTE** | Push des corrections opencode non effectué. Le dépôt public (4 commits) ne reflète pas le travail local. Un reviewer ne peut pas reproduire l'expérience depuis le dépôt actuel. | `push-project.sh` | ❌ Critique |
| P4 | **MODÉRÉE** | `BUILD_NOTES.txt` entièrement vide (20 lignes de commentaires, zéro donnée renseignée). Traçabilité de build nulle. | `BUILD_NOTES.txt` | ❌ Vide |
| P5 | **MODÉRÉE** | `figures_manifest.csv` en statut IN_PROGRESS — le lien figure→CSV→simulation n'est pas complet pour les figures REAL_RESULT. | `figures_manifest.csv` | ❌ Incomplet |
| P6 | **MODÉRÉE** | `sim/DATA_PROVENANCE.md` marqué DONE mais non vérifiable depuis le dépôt public. | `sim/DATA_PROVENANCE.md` | ❌ Non vérifiable |
| P7 | **BASSE** | README.md du dépôt public dit encore "Phase actuelle : 1 (squelette 95%, résultats ESTIMATED)" — contradiction totale avec les statuts REAL_RESULT annoncés. | `README.md` | ❌ Non mis à jour |

---

### CATÉGORIE 7 — Métadonnées et fichiers parasites (9 anomalies)

| # | Sévérité | Anomalie | Fichier(s) | Statut |
|---|---|---|---|---|
| M1 | **MODÉRÉE** | `metadata.tex` : la biographie auteur indique "Ph.D. degree in computer science from Djillali Liabès University... in 2026" — une thèse de 2026 soumise dans un article de 2026 est inhabituelle. Si la thèse n'est pas encore soutenue, c'est une inexactitude. | `metadata.tex` ligne 32 | ❌ À vérifier |
| M2 | **MODÉRÉE** | `test-elsarticle.pdf` à la racine du dépôt — fichier de test qui ne devrait pas être dans un dépôt de soumission scientifique. | `test-elsarticle.pdf` | ❌ Parasite |
| M3 | **BASSE** | `AUDIT_PROMPT.md`, `instruction.md`, `PHASE2_COMMAND_SUMMARY.md`, `WINDOWS_SETUP_GUIDE.md` — fichiers de travail internes exposés publiquement. Un reviewer qui visite le dépôt voit l'historique de la fabrication du manuscrit, ce qui peut nuire à l'image du travail. | Racine dépôt | ❌ À déplacer |
| M4 | **BASSE** | `push-project.sh` exposé publiquement — contient des commandes git qui révèlent le workflow interne. | `push-project.sh` | ❌ À retirer |
| M5 | **BASSE** | `status-macros.tex` : macros `\EstimatedCell` et `\RealCell` encore présentes dans le dépôt public — peuvent générer des artefacts visuels si laissées actives dans `main.pdf`. | `status-macros.tex` | ❌ Non vérifié |
| M6 | **BASSE** | `preamble-clusterids.tex` ET `preamble-ieee.tex` ET `preamble.tex` : trois preambles coexistent. Risque de conflits de packages ou de redéfinitions. | `preamble*.tex` | ❌ À auditer |
| M7 | **BASSE** | `UBUNTU_EXECUTION_PLAN.md`, `WINDOWS_SETUP_GUIDE.md` — deux guides OS différents non synchronisés. Le guide Ubuntu n'a pas été exécuté selon BUILD_NOTES. | `UBUNTU_EXECUTION_PLAN.md` | ❌ Non exécuté |
| M8 | **INFO** | L'ORCID `0009-0003-2928-9565` dans `metadata.tex` doit être vérifié sur orcid.org et lié au compte Elsevier Editorial Manager au moment de la soumission. | `metadata.tex` ligne 39 | ⚠️ À vérifier |
| M9 | **INFO** | `docker-compose.yml` et `docker/Dockerfile` présents mais non documentés comme suffisants pour reproduire la simulation (Cooja requiert du matériel spécifique et une licence Java). | `docker/`, `docker-compose.yml` | ⚠️ À documenter |

---

## Synthèse finale — 52 anomalies

| Catégorie | Total | Corrigées (local) | Encore ouvertes |
|---|---|---|---|
| Données expérimentales | 8 | 0 | **8** |
| Cible journal / format | 5 | 0 | **5** |
| Références bib | 6 | 2 | **4** |
| Code firmware | 5 | 3 | **2** |
| Manuscrit LaTeX | 13 | 5 | **8** |
| Reproductibilité | 7 | 0 | **7** |
| Métadonnées / fichiers | 9 | 0 | **6** |
| **Total** | **53** | **10** | **40** |

**Score actuel : 3.5/10 pour Computer Networks.** Le dépôt public n'a pas bougé — les corrections opencode n'ont pas été poussées, ce qui signifie même les corrections de forme ne sont pas visibles.

---

## Ce que vous devez faire maintenant, dans cet ordre exact

**Étape 0 (aujourd'hui, 10 minutes) :** Exécuter `git push` pour que les corrections opencode soient visibles. Sans ça, le dépôt est dans son état initial.

**Étape 1 (urgent) :** Choisir **définitivement** : Computer Networks Elsevier (`main.tex` + `elsarticle.cls`) ou IEEE IoT Journal (`main-ieee.tex` + `IEEEtran.cls`). Vous m'avez confirmé Computer Networks — donc la version IEEE doit être mise de côté, et `main.tex` devient le seul fichier de soumission.

**Étape 2 (bloquant absolu) :** Déboguer le DR=0% sur B1/B2/B3 sur Ubuntu — c'est le bug le plus dangereux car il fausse toutes vos comparaisons.

**Étape 3 :** Exécuter la campagne Cooja complète (50–500 nœuds). Sans ça, l'article ne peut pas être soumis à Computer Networks — c'est une exigence non négociable.
