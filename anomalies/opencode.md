# Revue Complète — RPL-ClusterIDS pour Computer Networks (Elsevier)

**Projet :** RPL-ClusterIDS — A Clustering-Based Energy-Aware Distributed Intrusion Detection System for RPL in IoT Networks  
**Auteur :** Madani Belacel  
**Date de la revue :** 30 juin 2026  
**Cible :** Computer Networks (Elsevier) — ISSN 1389-1286

---

## Table des matières

1. Points forts
2. Anomalies et problèmes critiques
3. Anomalies et problèmes haute priorité
4. Anomalies et problèmes moyenne priorité
5. Anomalies et problèmes basse priorité
6. Suggestions d'amélioration
7. Checklist finale avant soumission

---

## 1. Points forts

### 1.1 Architecture et conception
- **Approche originale et bien motivée** : IDS hiérarchique distribué par clusters énergétiquement conscients pour RPL. La combinaison détection légère membres + vérification CH + adaptation contextuelle (Full/Balanced/Eco) est cohérente et novatrice.
- **Équations formelles** (Eq. 1-4) correctement définies pour l'affinité, le déclenchement de re-clustering, le fitness CH et le LAS.
- **Modèle de menace clair** : 5 familles d'attaques RPL (rank, selective forwarding, wormhole, DAO flooding, mixed) avec signaux synthétiques calibrés.

### 1.2 Qualité du manuscrit (LaTeX)
- **Format Elsevier strict** : `elsarticle [preprint,12pt,number]`, `elsarticle-num` pour les références, booktabs pour les tableaux.
- **Figures vectorielles** (TikZ/PGFPlots) — conformes aux exigences Elsevier (pas de bitmap).
- **Structure complète** : 11 sections bien organisées (Intro → Related → Threat → Arch → Impl → Exp → Results → Discussion → Limits → Concl → Reproducibility).
- **11 figures et 9 tableaux** tous référencés dans le texte avec des `\label{}`/`\ref{}` corrects.
- **Highlights, abstract, keywords** : présents et formatés selon les directives.

### 1.3 Reproductibilité
- **Dépôt public complet** sur GitHub avec firmware, scripts de campagne, données parsées, pipeline d'analyse.
- **Pipeline documenté** : logs Cooja → parse_cooja_ids_metrics.py → aggregate_figures.sh → figures PGFPlots.
- **Scripts de campagne** : `run_ids_campaign.sh` avec modes smoke/pilot/full/batch.
- **Données réelles présentes** dans `data/real/parsed/` (7 CSVs, ~45-97 MB chacun, ~1.8M lignes).
- **Graines reproductibles** : 21 seeds CLUSTERIDS, 3 seeds ablation.

### 1.4 Qualité du code C
- **Pas d'allocation dynamique** — tout statique, approprié pour IoT contraint.
- **Modularité propre** : séparation claire en 7 modules (cluster formation, CH election, member IDS, CH IDS, context policy, attack injectors, campaign logging).
- **Utilisation correcte des API Contiki-NG** (etimer, simple_udp, NETSTACK_ROUTING).
- **Locale C forcée** (`setlocale(LC_ALL, "C")`) pour cohérence décimale — bonne pratique défensive.
- **Variant system** via Makefile et `-imacros` : 8 variantes (B1/B2/B3/MAIN + 4 ablation).

### 1.5 Analyse statistique
- **Tests statistiques présents** : Welch t-test, Mann-Whitney U, bootstrap CI.
- **Tests unitaires** : `test_compute_statistics.py` avec couverture bootstrap, compare_groups, schéma.
- **Ablation study** : 4 composants désactivables (NOCLUS, NOML, NOCTX, NOENR).

---

## 2. Anomalies et problèmes — CRITIQUES

Ces problèmes bloquent la soumission et doivent être résolus impérativement.

### C1. [SÉCURITÉ] Token GitHub personnel exposé dans `push.sh`

**Fichier :** `push.sh:5`  
**Problème :** Token d'accès personnel GitHub en clair :
```
git push https://madani-belacel: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@github.com/...
```
**Impact :** Tout personne ayant accès au dépôt peut pusher sur `main`. Le token doit être **révoqué immédiatement** sur GitHub.  
**Correctif :** Remplacer par `$GITHUB_TOKEN` ou utiliser `gh auth login`. Ne **jamais** committer de tokens.

### C2. [BUG] Wraparound non-signé dans le calcul de fitness CH

**Fichier :** `code_source_RPL_ClusterIDS/ch_elect.c:40`  
**Code :**
```c
uint32_t fitness = (uint32_t)nre_x100 * 2u + (uint32_t)(100u - etx_var_x10 * 5u);
```
**Problème :** `etx_var_x10` est un `uint8_t` (0-99, car `tx_counter % 100` dans `clusterids-node.c:113`). Quand `etx_var_x10 > 20`, la soustraction non-signée `100u - 120u` wrappe à `4294967276` (sous `uint32_t`). Le fitness devient astronomique, et **tous les nodes pensent être CH**.  
**Impact :** L'élection CH est corrompue pour la majorité des cas réalistes. L'énergie résiduelle (NRE) devient négligeable devant le terme ETX.  
**Correctif :** Utiliser l'arithmétique signée ou saturer/clamp `etx_var_x10` :
```c
int16_t etx_term = 100 - (int16_t)etx_var_x10 * 5;
if (etx_term < 0) etx_term = 0;
uint32_t fitness = (uint32_t)nre_x100 * 2u + (uint32_t)etx_term;
```

### C3. [BUG] L'attaque ne s'arrête jamais

**Fichier :** `code_source_RPL_ClusterIDS/ids_attack.c:30-32`  
**Code :**
```c
if(sim_s >= IDS_ATTACK_START_S && is_attacker) {
    active = 1;
}
```
**Problème :** Une fois `active = 1`, il n'y a aucun mécanisme pour repasser à 0. La phase "recovery" mentionnée dans `clusterids-node.c:194` (`sim_seconds < IDS_SIM_DURATION_S - 600`) ne voit jamais de vraie récupération car l'attaque reste active jusqu'à la fin.  
**Impact :** Les métriques de phase "recovery" dans les figures temporelles (Fig. 10) et les tableaux sont invalides.  
**Correctif :** Ajouter un compteur de durée d'attaque et une désactivation :
```c
if (active && sim_s > IDS_ATTACK_START_S + IDS_ATTACK_DURATION_S) {
    active = 0;
}
```

### C4. [INTÉGRITÉ] Tous les résultats expérimentaux sont synthétiques

**Fichiers :** `abstract.tex:6`, `results.tex`, `tables/table02_detection.tex` → `table09_statistics.tex`, `Figure/Fig_*.tex`  
**Problème :** Les valeurs de DR (80.6%), FPR (0.50%), CPU (5-7%), overheads, et l'étude d'ablation sont des **placeholders synthétiques** générés par `generate_synthetic_csv.py`. Le projet le reconnaît : `data/estimated/aggregated/summary_runs.csv` contient `status=SYNTHETIC` pour les 720 lignes.  
`reproducibility.tex:38` admet : "CPU, RAM, and energy values in the pilot campaign are pipeline placeholders generated from node-logical properties."  
**Impact :** Soumettre ces résultats à Computer Networks constituerait une **faute scientifique grave**. L'abstract et les highlights présentent des chiffres (80.6% DR, 0.50% FPR) comme des résultats réels alors qu'ils sont fabriqués.  
**Correctif :**
1. Remplacer tous les chiffres synthétiques par les résultats réels de la campagne complète (Phase 2).
2. En attendant, marquer CLAIREMENT chaque valeur comme `ESTIMATED` ou `PRELIMINARY`.
3. Ajouter des bandeaux "Results pending full campaign" sur les figures et tableaux.
4. Ne PAS soumettre tant que la campagne réelle n'est pas terminée.

### C5. [INTÉGRITÉ] B1 baseline 0% DR — extrêmement suspect

**Fichier :** `tables/table02_detection.tex:13-17`  
**Problème :** La baseline B1 (IDS centralisé sur le border router) obtient 0.0% sur TOUS les scénarios (rank, sel_fwd, wormhole, dao_flood, mixed). Un IDS centralisé devrait détecter au moins les attaques évidentes comme le DAO flooding.  
**Impact :** Les reviewers exigeront une explication. Si la baseline B1 est mal implémentée, la comparaison est invalide.  
**Correctif :** Vérifier l'implémentation B1, ou utiliser une baseline reconnue de la littérature.

---

## 3. Anomalies et problèmes — HAUTE PRIORITÉ

### H1. [DUPLICATION] Configuration dupliquée entre `project-conf.h` et `ids_conf.h`

**Fichiers :** `code_source_RPL_ClusterIDS/project-conf.h` et `code_source_RPL_ClusterIDS/ids_conf.h`  
**Problème :** Les deux fichiers définissent les mêmes macros (`IDS_CONF_CAMPAIGN_METRICS`, `IDS_CAMPAIGN_SEED`, `IDS_CAMPAIGN_SCENARIO`, `IDS_ATTACK_START_S`, `IDS_SIM_DURATION_S`, `IDS_UDP_PORT`). Si l'un est modifié sans l'autre, le comportement du build devient indéterministe.  
**Impact :** Bug silencieux. Par exemple, `project-conf.h` a des guards `#ifndef` pour toutes les macros, `ids_conf.h` aussi, mais l'ordre d'inclusion détermine quelle valeur l'emporte.  
**Correctif :** Supprimer les définitions redondantes d'un fichier, ou faire inclure l'un par l'autre.

### H2. [PIPELINE] `compute_statistics.py` incompatible avec les données réelles

**Fichier :** `scripts/statistics/compute_statistics.py:72`  
**Problème :** `load_runs()` cherche `summary_runs.csv`, mais le pipeline de parsing (`parse_cooja_ids_metrics.py`) produit des fichiers individuels (`detection_rate.csv`, `latency.csv`, etc.), pas de `summary_runs.csv`. Seul `generate_synthetic_csv.py` produit ce fichier.  
**Impact :** Le pipeline statistique ne fonctionne qu'avec les données synthétiques. Impossible de produire Table IX à partir des vrais logs.  
**Correctif :** Aligner les noms de colonnes entre parseur et script stats, ou ajouter une étape de fusion des CSVs.

### H3. [BIBLIOGRAPHIE] 19 entrées orphelines non citées

**Fichier :** `bib/references.bib`  
**Problème :** Entrées non citées dans le manuscrit : `baronti2007`, `faheem2013`, `sfar2018`, `beno2018qosrpl`, `dib2024`, `osterlind2006cooja`, `granjal2015rplsec`, `yan2014iotsec`, `shahid2024hybrid`, `emec2023rout4`, `raza2020rplids`, `sicari2015security`, `belacel2025rplaer`, `belacel2025rplmqos`, `fldsfa2024`, `fedrpl2024`, `sharma2025tinyml`, `gatr2025`, `trustawaregnn2025`, `spatiotemporal2026`, `anomalefd2026`, `xaiids2026`, `causalfl2026`.  
**Impact :** Les directives Elsevier exigent que chaque référence soit citée dans le texte.  
**Correctif :** Supprimer les non-citées ou les intégrer dans le texte. Maximum 45 références recommandé par Elsevier.

### H4. [LATEX] Symbole `\dag{}` dans l'abstract sans définition de footnote

**Fichier :** `sections/abstract.tex:6`  
**Problème :** `80.6\% campaign-level detection rate\dag{}` — le `\dag{}` est un symbole orphelin. Aucune `\footnote` ou `\dagtext` n'est définie.  
**Impact :** Un `†` nu apparaît dans le PDF sans explication.  
**Correctif :** Remplacer par `\footnote{...}` ou définir `\newcommand{\dagtext}{...}`.

### H5. [MANUSCRIT] Tous les modes (Full/Balanced/Eco) ont le même DR (80.6%) et FPR (0.50%)

**Fichier :** `tables/table03_operating_modes.tex:13-15`  
**Problème :** Les trois modes opératoires montrent des performances identiques en DR et FPR. La seule différence est CPU (5/6/7%, qualifié "design-target estimates").  
**Impact :** Cela contredit la proposition centrale que les modes offrent un compromis sécurité/énergie. Un reviewer demandera pourquoi utiliser autre chose que Eco.  
**Correctif :** L'explication (ligne 21-22) dit que "severe attacks dominate" — ajouter des métriques par-intervalle ou par type d'attaque qui montrent la différence.

### H6. [SÉCURITÉ] Token obsolète dans un commentaire

**Fichier :** `internal/push-project.sh:14`  
**Problème :** `# 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` — token GitHub dans un commentaire.  
**Correctif :** Supprimer la ligne. Même révoqué, il ne doit pas apparaître.

---

## 4. Anomalies et problèmes — MOYENNE PRIORITÉ

### M1. Terme ETX domine complètement NRE dans le calcul de fitness

**Fichier :** `code_source_RPL_ClusterIDS/ch_elect.c:40`  
**Problème :** Même après correction du wraparound, `etx_var_x10 * 5u` varie de 0 à 495 alors que `nre_x100 * 2u` varie de ~140 à ~178 (NRE 70-89%). Le terme ETX (max 495) domine le terme énergie (max ~178). L'énergie résiduelle est quasiment ignorée.  
**Correctif :** Normaliser les deux termes ou ajuster les poids pour qu'ils aient une plage comparable.

### M2. Nom de fichier `table06_dataset.tex` trompeur

**Fichier :** `tables/table06_dataset.tex`  
**Problème :** Le fichier contient les règles R1-R4 et les features CH, pas un dataset ML. Le nom suggère un schéma de données alors que c'est une table de règles.  
**Correctif :** Renommer en `table06_rules.tex`.

### M3. Incohérence orthographique britannique/américain

**Fichier :** `sections/limitations.tex:14`  
**Problème :** `behaviour` (UK) vs `behavior` (US) ailleurs dans le manuscrit.  
**Impact :** Incohérence stylistique. Les revues Elsevier acceptent les deux mais exigent la cohérence.  
**Correctif :** Uniformiser en `behavior` (US, standard Elsevier).

### M4. Les fichiers d'en-tête de variantes sont purement cosmétiques

**Fichiers :** `code_source_RPL_ClusterIDS/variants/imacros-*.h`  
**Problème :** Les fichiers `imacros-*.h` ne définissent QUE `IDS_VARIANT_LABEL`. Les flags réels (`IDS_VARIANT_B1`, etc.) sont définis dans le Makefile via `-D`. Un développeur lisant `imacros-B1.h` s'attendrait à voir `#define IDS_VARIANT_B1 1`.  
**Correctif :** Ajouter la définition du flag dans chaque `imacros-*.h` ou documenter clairement dans l'en-tête.

### M5. Variante B3 : `member_las` voidé mais potentiellement lu

**Fichier :** `code_source_RPL_ClusterIDS/ids_ch.c:29-37`  
**Problème :** Sous B3, `(void)member_las` supprime le warning mais la valeur sur la pile pourrait être lue ligne 37 (`member_las > IDS_THRESHOLD_CH`). Comportement indéfini uniquement si la valeur est indéterminée, mais confusion.  
**Correctif :** Mettre explicitement `member_las = 0` sous B3.

### M6. Duplication de code ~90% entre `compute_table_stats.py` et `summary_stats.py`

**Fichiers :** `scripts/*/compute_table_stats.py`, `scripts/*/summary_stats.py`  
**Problème :** Deux scripts qui calculent les mêmes statistiques avec un formatage légèrement différent. Maintenance redondante.  
**Correctif :** Fusionner en un seul script avec option `--format latex` / `--format text`.

### M7. checklist.md corrompu

**Fichier :** `checklist.md`  
**Problème :** Contient uniquement `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`.  
**Correctif :** Remplacer par une vraie checklist ou supprimer.

### M8. instruction.md est un placeholder

**Fichier :** `instruction.md`  
**Problème :** Contient `1111111111111111 / 2222222222222222`.  
**Correctif :** Supprimer ou remplir.

---

## 5. Anomalies et problèmes — BASSE PRIORITÉ

### L1. Cibles Makefile redondantes (NOCLUS = MAIN_NOCLUS, etc.)

**Fichier :** `code_source_RPL_ClusterIDS/Makefile:41-80`  
**Problème :** Chaque variante d'ablation a DEUX alias (ex: `NOCLUS` et `MAIN_NOCLUS`) — pourtant les deux font exactement la même chose.  
**Impact :** Maintenabilité réduite.  
**Correctif :** Supprimer les alias redondants.

### L2. Script `build_variant.sh` n'exécute pas — juste `echo`

**Fichier :** `simulations/scripts/build_variant.sh`  
**Problème :** Le script fait `echo` des commandes make au lieu de les exécuter. C'est un document, pas un script.  
**Correctif :** Remplacer `echo` par `eval` ou supprimer le fichier.

### L3. Commentaires en français dans le code C

**Fichiers :** `clusterids-node.c:115`, `ids_conf.h:20-21`, `ids_attack.c:47`  
**Problème :** Commentaires bilingues français/anglais dans une base de code internationale.  
**Correctif :** Traduire en anglais.

### L4. Graphics path non utilisé dans les préambules

**Fichier :** `main.tex:34` — `\graphicspath{{Figures/}}` défini, mais les figures TikZ sont incluses via `\input`, pas `\includegraphics`. La commande est inutile.  
**Correctif :** Sans objet (fonctionnellement inoffensif).

### L5. `status-macros.tex` produit des espaces blancs résiduels

**Fichier :** `status-macros.tex:2-3` et `results.tex:17`  
**Problème :** `\newcommand{\CaptionFigStatusNote}{}` et `\newcommand{\TableStatusNote}{}` sont vides mais utilisées dans `\caption{\CaptionFigFour{} \CaptionFigStatusNote}`. Les macros vides avec `{}` produisent un espace insécable dans le caption.  
**Correctif :** Définir `\newcommand{\CaptionFigStatusNote}{\relax}` et utiliser `\caption{\CaptionFigFour{}\CaptionFigStatusNote}`.

### L6. Fig 11 : données CPU tracées deux fois (double-plot)

**Fichier :** `Figures/Fig_11_Operating_Mode_Sensitivity.tex`  
**Problème :** L'axe de droite et l'axe de gauche tracent tous deux les données CPU. La légende montre "CPU (%)" en double.  
**Correctif :** Nettoyer le code PGFPlots.

### L7. Fichiers de build LaTeX (.aux, .bbl, .pdf, .log) commités

**.gitignore doit être enrichi :** Aucun build artifact LaTeX ne doit être commité.  
**Actuellement ignoré :** `*.aux`, `*.bbl`, `*.log`, `*.pdf` — mais `main.pdf` et `main-ieee.pdf` étaient commités.  
**Correctif :** Nettoyer et ajouter aux règles `.gitignore`.

### L8. Handles de fichiers non fermés en cas d'exception

**Fichier :** `scripts/*/parse_cooja_ids_metrics.py:251-252`  
**Problème :** `with open()` n'est pas utilisé ; `path.open()` suivi de `f.close()` manuel. Si une exception survient entre les deux, le handle fuit.  
**Correctif :** Utiliser `with open(path) as f:`.

### L9. Noms de variantes incohérents entre C et Python

**Problème :** Le C utilise `"MAIN"` (imacros-CLUSTERIDS.h), le Python utilise `"CLUSTERIDS"` (generate_synthetic_csv.py:27). Les données synthétiques ne correspondront pas aux vrais noms de variantes.  
**Correctif :** Aligner sur un seul nom (`"CLUSTERIDS"` recommandé pour le papier).

### L10. `#ifndef` manquant pour `IDS_UDP_PORT`

**Fichier :** `code_source_RPL_ClusterIDS/project-conf.h:28`  
**Problème :** `#define IDS_UDP_PORT 8765` sans guard `#ifndef`. Impossible de surcharger par le build system.  
**Correctif :** Ajouter `#ifndef IDS_UDP_PORT` / `#endif`.

### L11. EWMA avec perte de précision sur `uint8_t`

**Fichier :** `code_source_RPL_ClusterIDS/ids_member.c:53`  
**Problème :** `ewma[i] = (uint8_t)((...) / 8u)` — la division par 8 perd 3 bits de précision à chaque mise à jour.  
**Impact :** Faible, car les signaux sont ~0-85 et le seuil est 60. Acceptable pour 8-bit, mais à noter.

---

## 6. Suggestions d'amélioration pour atteindre le niveau du journal

### 6.1 Avant la soumission

1. **Terminer la campagne complète** (Phase 2) avec 20+ seeds pour toutes les variantes sur tous les scénarios. Les données réelles doivent remplacer les placeholders synthétiques.
2. **Corriger le bug CH election** (C2) qui corrompt l'élection pour les valeurs réalistes d'ETX.
3. **Corriger le bug attack end** (C3) pour que la phase "recovery" soit valide.
4. **Valider la baseline B1** — 0% DR sur tous les scénarios est suspect. Vérifier l'implémentation ou utiliser une baseline reconnue.
5. **Pipeline statistique fonctionnel** : aligner les formats CSV entre parseur et script de stats.
6. **Nettoyage de la biblio** : supprimer les 19 entrées non citées. Viser ≤45 références.

### 6.2 Renforcer le manuscrit

7. **Ajouter une section "Threat Model" plus formelle** avec capabilities de l'adversaire, etc.
8. **Comparaison avec baselines supplémentaires** : B2 et B3 (promis dans Table II mais absent).
9. **Scénarios réalistes** : topologies aléatoires (pas seulement grille 50 nœuds).
10. **Analyse de sensibilité** des hyperparamètres ($\tau_{low}$, $w_e$, etc.) — reportée à "future work", mais une analyse partielle renforcerait le papier.
11. **Validation sur matériel réel** (Tmote Sky, Zolertia) pour crédibilité.
12. **Discussion sur l'énergie plus détaillée** : remplacer "design-target estimates" par des mesures Energest réelles.

### 6.3 Améliorations du code

13. **Ajouter des tests unitaires pour le C** (framework existant Contiki-NG).
14. **`IDS_UDP_PORT` configurable** via `#ifndef`.
15. **Documenter les flags de build** dans chaque `imacros-*.h`.
16. **Fusionner les scripts stats dupliqués**.

### 6.4 Améliorations de la reproductibilité

17. **DOI persistant** via Zenodo (mentionné mais pas fait).
18. **Conteneur Docker** pour environnement Cooja reproductible.
19. **Script de validation** qui vérifie que les figures peuvent être régénérées.

---

## 7. Checklist finale avant soumission

### 7.1 Intégrité scientifique
- [ ] Tous les résultats proviennent de simulations réelles (pas de placeholders synthétiques)
- [ ] Les données brutes sont archivées et documentées
- [ ] Les baselines (B1, B2, B3) sont correctement implémentées et validées
- [ ] Les tests statistiques sont valides (n ≥ 20 par groupe)
- [ ] Aucun résultat présenté comme "REAL_RESULT" n'est en fait "ESTIMATED"

### 7.2 Code et reproductibilité
- [ ] Token GitHub supprimé de `push.sh` et `internal/push-project.sh`
- [ ] Bug wraparound `ch_elect.c:40` corrigé
- [ ] Bug attaque infinie `ids_attack.c:31` corrigé
- [ ] Pipeline statistique fonctionnel avec données réelles
- [ ] `summary_runs.csv` généré par le pipeline de parsing
- [ ] Fichiers placeholders (`checklist.md`, `instruction.md`) supprimés
- [ ] Commentaires français traduits en anglais

### 7.3 Manuscrit (LaTeX)
- [ ] `\dag{}` dans l'abstract remplacé par `\footnote{}`
- [ ] `behaviour` → `behavior` (cohérence US)
- [ ] `table06_dataset.tex` renommé en `table06_rules.tex`
- [ ] Tous les tableaux et figures ont des légendes auto-suffisantes
- [ ] Aucune note de bas de page orpheline
- [ ] `status-macros.tex` nettoyé (macros vides)
- [ ] Fig 11 : double-plot CPU corrigé

### 7.4 Bibliographie
- [ ] 19 entrées non citées supprimées ou intégrées
- [ ] ≤ 45 références
- [ ] Format cohérent (tous les DOI présents)
- [ ] `anton2024rpl` : clé de citation corrigée (`2024` pas `2014`)

### 7.5 Dépôt et mise en page
- [ ] Builds LaTeX artifact (.aux, .bbl, .log, .out) exclus du dépôt
- [ ] `main.pdf` et `main-ieee.pdf` exclus du dépôt
- [ ] `.gitignore` complet
- [ ] README.md à jour

### 7.6 Soumission Elsevier
- [ ] Format : elsarticle, preprint 12pt
- [ ] Highlights (3-5) — actuellement 6, réduire si nécessaire
- [ ] Abstract 150-250 mots ✓
- [ ] 5-8 keywords ✓
- [ ] ORCID et affiliation complète ✓
- [ ] Auteur correspondant marqué ✓
- [ ] Figures vectorielles (TikZ/PGFPlots) ✓
- [ ] Tableaux format booktabs ✓
- [ ] Références numérotées (elsarticle-num) ✓
- [ ] Manuscript en une colonne ✓

---

## Résumé des anomalies

| Sévérité | Nombre |
|----------|--------|
| Critique | 5 |
| Haute    | 6 |
| Moyenne  | 8 |
| Basse    | 11 |
| **Total** | **30** |

**Conclusion :** Le projet est structurellement excellent (architecture, modularité, reproductibilité, format Elsevier). Cependant, **la soumission est prématurée** — les résultats expérimentaux sont synthétiques, l'élection CH est corrompue par un bug arithmétique, l'attaque ne s'arrête jamais, un token GitHub est exposé, et le pipeline statistique ne fonctionne pas avec les données réelles. La priorité #1 est de terminer la campagne réelle (Phase 2) avant toute soumission.
