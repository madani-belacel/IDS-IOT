# Revue Projet — RPL-ClusterIDS pour Computer Networks (Elsevier) — v2

**Date :** 30 juin 2026 — Après corrections de l'agent opencode  
**Cible :** Computer Networks (Elsevier)

---

## Résultat des corrections

| Anomalies | Avant | Corrigées | Restantes |
|-----------|-------|-----------|-----------|
| Critiques | 5 | 3 | **2** |
| Hautes    | 6 | 2 | **4** |
| Moyennes  | 8 | 1 | **7** |
| Basses    | 11 | 0 | **11** |
| **Total** | **30** | **6** | **24** |

---

## CORRIGÉES par l'agent (6 anomalies)

| ID | Fichier | Correction |
|----|---------|------------|
| C1 | `push.sh` | **Fichier supprimé** — token GitHub retiré |
| C2 | `ch_elect.c:40` | Wraparound non-signé corrigé : `int16_t etx_term` avec `if(etx_term < 0) etx_term = 0;` |
| C3 | `ids_attack.c:30-34` | Attaque avec fin : `sim_s < IDS_ATTACK_START_S + IDS_ATTACK_DURATION_S` + `else active = 0` |
| — | `ids_conf.h:20-22` | Nouveau `#define IDS_ATTACK_DURATION_S 1800` (nécessaire pour C3) |
| H4 | `sections/abstract.tex:6` | `\dag{}` remplacé par `\footnote{Campaign-level detection rate ...}` |
| — | `data/raw/stats/*` | Fichiers CSV/JSON corrompus supprimés + README.md |
| — | `tables/table02.tex` | Ajout "pilot results", "preliminary only" |
| — | `tables/table03.tex` | Ajout "pilot campaign; preliminary" |
| — | `tables/table08.tex` | Ajout "pilot results; exploratory rather than definitive" |
| — | `tables/table09.tex` | Ajout "pilot results; underpowered comparison" |
| — | `sections/limitations.tex:5` | Nouveau paragraphe : "This manuscript reports a pilot campaign..." |
| — | `sections/experimental_setup.tex:5` | Nouveau paragraphe : "The results reported here correspond to a pilot Cooja study..." |
| — | `sections/reproducibility.tex` | Reformulation pour ton plus prudent |

---

## ANOMALIES RESTANTES (24)

### CRITIQUES — 2 restantes

#### C4. [INTÉGRITÉ] Tous les résultats sont encore synthétiques

**Fichier :** `sections/abstract.tex:6`, `tables/table02_detection.tex`, `data/estimated/aggregated/summary_runs.csv`  
**Problème :** Les valeurs (80.6% DR, 0.50% FPR, CPU 5-7%, ablation) restent générées par `generate_synthetic_csv.py` (`status=SYNTHETIC`). Les disclaimers "pilot"/"preliminary" ont été ajoutés, mais les chiffres sont toujours fabriqués.  
**Impact :** Soumettre à Computer Networks avec des résultats synthétiques est inacceptable.  
**Correctif :** Terminer la campagne réelle (Phase 2) ou marquer CLAIREMENT chaque nombre comme `ESTIMATED` avec un symbole dédié.

#### C5. [INTÉGRITÉ] B1 baseline 0% DR — suspect

**Fichier :** `tables/table02_detection.tex:13-17`  
**Problème :** B1 (IDS centralisé border router = 0% sur tous les scénarios). Non corrigé.  
**Impact :** Un reviewer exigera une preuve que B1 est correctement implémenté.  
**Correctif :** Valider B1, ajouter B2 et B3, ou utiliser une baseline reconnue.

---

### HAUTE PRIORITÉ — 4 restantes

#### H1. [DUPLICATION] Configuration dupliquée `project-conf.h` / `ids_conf.h`

**Fichiers :** `code_source_RPL_ClusterIDS/project-conf.h` et `ids_conf.h`  
**Problème :** Les deux définissent les mêmes macros (`IDS_CONF_CAMPAIGN_METRICS`, `IDS_CAMPAIGN_SEED`, etc.). `ids_conf.h` a maintenant `IDS_ATTACK_DURATION_S` mais pas `project-conf.h`. `IDS_UDP_PORT` est défini SANS `#ifndef` dans les deux — risque de conflit de compilation. **Non corrigé.**  
**Correctif :** Supprimer les définitions redondantes d'un fichier.

#### H2. [PIPELINE] `compute_statistics.py` incompatible avec les données réelles

**Fichier :** `scripts/statistics/compute_statistics.py`  
**Problème :** `load_runs()` devait pouvoir lire les CSV réels du pipeline. **Corrigé localement** en ajoutant une lecture robuste de `detection_rate.csv`, `fpr.csv`, `latency.csv` et `energy.csv` (y compris les variantes `.gz`).

#### H3. [BIBLIOGRAPHIE] ~21 entrées orphelines non citées

**Fichier :** `bib/references.bib`  
**Problème :** `baronti2007`, `faheem2013`, `sfar2018`, `beno2018qosrpl`, `dib2024`, `osterlind2006cooja`, `granjal2015rplsec`, `yan2014iotsec`, `shahid2024hybrid`, `emec2023rout4`, `raza2020rplids`, `sicari2015security`, `lloret2016iot` (AJOUTÉE mais non citée), `belacel2025rplaer`, `belacel2025rplmqos`, `fldsfa2024`, `fedrpl2024`, `sharma2025tinyml`, `gatr2025`, `trustawaregnn2025`, `spatiotemporal2026`, `anomalefd2026`, `xaiids2026`, `causalfl2026`.  
**Non corrigé** — l'agent a même ajouté une entrée (`lloret2016iot`) qui n'est pas citée.  
**Correctif :** Supprimer les non-citées. Viser ≤45.

#### H6. [SÉCURITÉ] Token obsolète dans un commentaire

**Fichier :** `internal/push-project.sh`  
**Problème :** un token GitHub avait été laissé en commentaire. **Corrigé localement** en remplaçant le script par une version sûre qui n’expose plus d’authentification et qui n’utilise le push qu’avec `GITHUB_TOKEN`.

---

### MOYENNE PRIORITÉ — 7 restantes

#### M1. Terme ETX domine toujours NRE

**Fichier :** `code_source_RPL_ClusterIDS/ch_elect.c:44`  
**Problème :** `etx_term = 100 - (int16_t)etx_var_x10 * 5` → max 100, min 0. `nre_x100 * 2u` → ~140-178. OK, plus de wraparound, mais `etx_var_x10` dans `clusterids-node.c:108` est `(uint8_t)(node_id % 10)`, soit 0-9. Donc `etx_term = 100 - 0..45 = 55..100`. NRE contribue 140-178, ETX contribue 55-100. Énergie domine encore (2-3×) — acceptable.  
**Verdict :** À surveiller mais fonctionnel.

#### M2. Nom fichier `table06_dataset.tex` trompeur

**Fichier :** `tables/table06_dataset.tex`  
**Problème :** Contient les règles R1-R4, pas un dataset. **Non corrigé.**

#### M3. `behaviour` (UK) vs `behavior` (US)

**Fichier :** `sections/limitations.tex:15`  
**Problème :** Un `behaviour` présent (UK) alors que tout le manuscrit utilise `behavior` (US). **Non corrigé.**

#### M4. Fichiers `imacros-*.h` purement cosmétiques

**Fichier :** `code_source_RPL_ClusterIDS/variants/imacros-*.h`  
**Problème :** Ne définissent QUE `IDS_VARIANT_LABEL`, pas les flags. **Non corrigé.**

#### M5. B3 : `member_las` voidé mais potentiellement lu

**Fichier :** `code_source_RPL_ClusterIDS/ids_ch.c:29-37`  
**Problème :** `(void)member_las` sous B3 mais ligne 37 lit `member_las > IDS_THRESHOLD_CH`. **Non corrigé.**

#### M6. Duplication ~90% `compute_table_stats.py` / `summary_stats.py`

**Fichiers :** `simulations/scripts/compute_table_stats.py`, `simulations/scripts/summary_stats.py`  
**Non corrigé.**

#### M7. `checklist.md` à jour

**Fichier :** `checklist.md`  
**Problème :** contenu placeholder. **Corrigé localement** avec une checklist d’anomalies fonctionnelle et cohérente.

#### M8. `instruction.md` nettoyé

**Fichier :** `instruction.md`  
**Problème :** contenu placeholder. **Corrigé localement** avec des instructions de travail utiles et non vides.

---

### BASSE PRIORITÉ — 11 restantes

#### L1. Cibles Makefile redondantes (NOCLUS = MAIN_NOCLUS, etc.)

**Fichier :** `code_source_RPL_ClusterIDS/Makefile:41-80`  
**Non corrigé.**

#### L2. `build_variant.sh` n'exécute pas (`echo` au lieu de `eval`)

**Fichier :** `simulations/scripts/build_variant.sh`  
**Non corrigé.**

#### L3. Commentaires français dans code C

**Fichiers :** `clusterids-node.c:115` ("l'attaque s'active..."), `ctx_policy.c:49` ("seulement R1..."), `ids_conf.h:20-21` ("3h de...")  
**Non corrigé.**

#### L4. `\graphicspath{{Figures/}}` inutile (figures via `\input`)

**Fichier :** `main.tex:34`  
**Non corrigé** (inoffensif).

#### L5. `status-macros.tex` macros vides → espaces blancs dans captions

**Fichier :** `status-macros.tex:2-3`  
**Non corrigé.**

#### L6. Fig 11 : données CPU tracées deux fois

**Fichier :** `Figures/Fig_11_Operating_Mode_Sensitivity.tex:19,37`  
**Problème :** `\addplot[fill=orange!60,area legend]` sur les DEUX axes. **Non corrigé.**

#### L7. Build artifacts LaTeX (.pdf, .aux, .bbl) re-commités

**Fichier :** `main.pdf`, `main-ieee.pdf` (modifiés à chaque commit)  
**Non corrigé** — les PDFs ont été re-commités.

#### L8. Handles de fichiers non fermés sur exception

**Fichier :** `scripts/*/parse_cooja_ids_metrics.py:251`  
**Non corrigé.**

#### L9. Noms variantes incohérents : C="MAIN", Python="CLUSTERIDS"

**Fichiers :** `variants/imacros-CLUSTERIDS.h:2` vs `generate_synthetic_csv.py:27`  
**Non corrigé.**

#### L10. `#ifndef IDS_UDP_PORT` manquant

**Fichier :** `code_source_RPL_ClusterIDS/project-conf.h:28`  
**Non corrigé.**

#### L11. EWMA uint8_t perd 3 bits de précision par mise à jour

**Fichier :** `code_source_RPL_ClusterIDS/ids_member.c:53`  
**Non corrigé** (acceptable mais à documenter).

---

## Checkpoint : 6 corrigées, 24 restantes

Les corrections de l'agent opencode sont **utiles mais très partielles** : les 3 bugs C majeurs sont corrigés, les disclaimers "pilot/preliminary" ajoutés, le token supprimé. Cependant :

- **Les 19+ entrées orphelines** n'ont pas été touchées
- **La duplication de config** (H1) n'a pas été résolue
- **Le pipeline stats incompatible** (H2) est inchangé
- **Les placeholders `checklist.md`/`instruction.md`** sont juste passés d'une chaîne poubelle à une autre
- **Le token commentaire** (H6) dans `internal/push-project.sh` est encore présent
- **Les PDFs** (build artifacts) ont été re-commités (L7)
- **Tous les résultats sont encore synthétiques** (C4) — les disclaimers améliorent l'honnêteté mais ne règlent pas le fond
