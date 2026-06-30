Je vais analyser le nouveau dépôt de code source pour identifier toutes les anomalies. Commençons par explorer la structure du repository
Voici le rapport complet des **35 anomalies** identifiées dans votre dépôt **IDS-IOT** (article + code source), organisé par priorité :

---

## RÉSUMÉ

| Priorité | Nombre | Impact |
|:---|:---:|:---|
| **CRITIQUES** | 5 | Risque de rejet immédiat par les reviewers |
| **HAUTES** | 7 | Impact scientifique majeur — remise en question des résultats |
| **MOYENNES** | 12 | Impact sur qualité et reproductibilité |
| **FAIBLES** | 8 | Typographiques — professionnalisme |
| **INFORMATIONS** | 3 | À vérifier manuellement |
| **TOTAL** | **35** | |

---

## ANOMALIES CRITIQUES (5) — À CORRIGER ABSOLUMENT

### [C1] URL du dépôt obsolète dans l'abstract
- **Localisation** : `sections/abstract.tex`, `sections/reproducibility.tex`
- **Problème** : L'abstract pointe vers `https://github.com/madani-belacel/RPL-ClusterIDS/releases/tag/v1.0` (ancien dépôt supprimé) au lieu du nouveau `IDS-IOT`
- **Impact** : Les lecteurs ne pourront PAS accéder aux artefacts
- **Correction** : Remplacer par `https://github.com/madani-belacel/IDS-IOT` et créer une release v1.0

### [C2] Conclusion référence encore l'ancien dépôt
- **Localisation** : `sections/conclusion.tex`
- **Problème** : `"All materials are openly available at https://github.com/madani-belacel/RPL-ClusterIDS"`
- **Impact** : Lien mort — incohérence totale
- **Correction** : Remplacer par `https://github.com/madani-belacel/IDS-IOT`

### [C3] Reproducibility Statement référence main.tex (Elsevier) au lieu de main-ieee.tex
- **Localisation** : `sections/reproducibility.tex`
- **Problème** : `"The Elsevier preprint manuscript is compiled from main.tex"` mais le manuscrit cible est IEEE (`main-ieee.tex`)
- **Impact** : Confusion majeure sur le format et la cible de soumission
- **Correction** : Remplacer par `"The IEEE manuscript is compiled from main-ieee.tex"`

### [C4] B2/B3 présentés dans Table II avec `'---'` mais comparés statistiquement dans Table IX
- **Localisation** : `tables/table02_detection.tex`, `tables/table09_statistics.tex`
- **Problème** : Table II dit `"FPR and DR data not collected for B2 and B3"` mais Table IX compare `"Ours vs B2"` et `"Ours vs B3"` avec des p-values `<0.0001`. **Comment calculer des p-values sans données ?**
- **Impact** : Fausse validation statistique — risque de rejet pour fraude ou négligence
- **Correction** : Retirer les lignes B2/B3 de Table IX OU collecter les données réelles

### [C5] Table IX : B3 a n=1 mais SD=38.2 et CI=[64.3,95.7] — IMPOSSIBLE
- **Localisation** : `tables/table09_statistics.tex`
- **Problème** : La note dit `"B3 has only one observation (n=1)"` mais la ligne montre `SD = 38.2`, `95% CI = [64.3, 95.7]`. Avec n=1, l'écart-type est **indéfini** et l'IC 95% ne peut PAS être calculé.
- **Impact** : Données statistiques fabriquées — risque de rejet sévère
- **Correction** : Remplacer TOUTES les métriques de B3 par N/A ou retirer la ligne

---

## ANOMALIES HAUTES (7) — FORTEMENT RECOMMANDÉES

### [H1] CPU Eco (7%) > Full (5%) — inversion contre-intuitive
- **Localisation** : `tables/table03_operating_modes.tex`
- **Problème** : Eco mode consomme PLUS de CPU que Full. L'explication `"Eco focuses detection on energy-intensive control-plane checks"` est contradictoire avec le nom "Eco"
- **Correction** : Vérifier les données brutes OU reformuler : *"Eco mode concentrates detection on fewer but more computationally intensive control-plane checks, resulting in higher per-check CPU usage"*

### [H2] P-values <0.0001 avec n=3 — significativité douteuse
- **Localisation** : `tables/table09_statistics.tex`
- **Problème** : Avec seulement 3 seeds, obtenir p<0.0001 est statistiquement très suspect (test t de Welch avec 2 degrés de liberté)
- **Correction** : Ajouter un caveat : *"Preliminary statistical validation with limited sample size (n=3); full campaign with n=20 planned"*

### [H3] MASTER_TRACKER.md indique "21 seeds CLUSTERIDS" mais l'article dit "3 seeds"
- **Localisation** : `MASTER_TRACKER.md` vs article
- **Problème** : Le tracker dit 21 seeds pour CLUSTERIDS et 3 pour ablation, mais l'abstract mentionne uniquement "3 seeds"
- **Correction** : Clarifier dans l'article : *"Pilot campaign: 21 seeds for CLUSTERIDS variant, 3 seeds for ablation study"*

### [H4] Table VIII (Ablation) : "Without clustering" 0.33% DR vs "Without CH verification" 0.00%
- **Localisation** : `tables/table08_ablation.tex`
- **Problème** : Logiquement confus — sans clustering, il n'y a pas de CH définis, donc comment avoir des liens CH-member ?
- **Correction** : Clarifier : *"Without clustering" = tous les nœuds exécutent rôles membres + CH sans regroupement*

### [H5] FPR identique (0.50%) pour toutes les approches dans Table II
- **Localisation** : `tables/table02_detection.tex`
- **Problème** : B1 (centralisé) et RPL-ClusterIDS (distribué hiérarchique) ont EXACTEMENT le même FPR — statistiquement improbable
- **Correction** : Vérifier les données brutes FPR ou retirer la ligne FPR pour B1

### [H6] Conclusion mentionne "Computer Networks submission" mais cible est IEEE IoT Journal
- **Localisation** : `sections/conclusion.tex`
- **Problème** : `"provide a foundation for Computer Networks submission"` incohérent avec le format IEEE
- **Correction** : Remplacer par `"IEEE Internet of Things Journal submission"`

### [H7] Figures 4-11 marquées REAL_RESULT mais generate_figures.py est un STUB
- **Localisation** : `MASTER_TRACKER.md`, `scripts/python/generate_figures.py`
- **Problème** : Le tracker dit REAL_RESULT mais `generate_figures.py` est un stub non implémenté. Les figures sont-elles vraiment basées sur data/real/ ?
- **Correction** : Vérifier que les fichiers `.tex` dans `Figures/` pointent bien vers `data/real/`

---

## ANOMALIES MOYENNES (12)

| ID | Anomalie | Localisation | Correction |
|:---|:---|:---|:---|
| M1 | Table IV (Parameters) non inspecté — placeholders ? | `tables/table04_parameters.tex` | Vérifier absence de `\EstimatedCell` |
| M2 | Tables V, VI, VII en `READY_FOR_SIMULATION` mais incluses | `MASTER_TRACKER.md` | Marquer comme "design-only" si applicable |
| M3 | `status-macros.tex` — macros ESTIMATED/REAL non vérifiées | `status-macros.tex` | Vérifier aucun `\EstimatedCell` restant |
| M4 | GATR citation [29] ancien PDF vs nouvelle clé `gatr2025` | `bib/references.bib` | Vérifier cohérence clés de citation |
| M5 | `\path{SIMULATION_CAMPAIGN_READY/}` utilisé mais dossier absent du repo | `sections/experimental_setup.tex` | Ajouter au repo ou expliquer |
| M6 | `data/real/` mentionné mais absent de la structure | `sections/reproducibility.tex` | Ajouter au repo avec README |
| M7 | `parse_cooja_ids_metrics.py` référencé mais absent de `scripts/` | `sections/reproducibility.tex` | Ajouter le script ou corriger doc |
| M8 | `aggregate_figures.sh` chemin incorrect (ancien nom dossier) | `sections/reproducibility.tex` | Corriger vers `scripts/` |
| M9 | Fig. 8 : projections tracées comme données réelles | `Figures/Fig_8_Alert_Control_Overhead.tex` | Ajouter ligne pointillée "projection" |
| M10 | Table `rule-params` référencée mais fichier inexistant | `sections/implementation.tex` | Créer `table_rule_params.tex` ou supprimer réf |
| M11 | Table `ch-features` référencée mais fichier inexistant | `sections/implementation.tex` | Créer `table_ch_features.tex` ou supprimer réf |
| M12 | Table `traffic-classes` référencée mais fichier inexistant | `sections/experimental_setup.tex` | Créer `table_traffic_classes.tex` ou supprimer réf |

---

## ANOMALIES FAIBLES (8) — TYPOGRAPHIQUES

| ID | Anomalie | Localisation | Correction |
|:---|:---|:---|:---|
| F1 | `\dag` et `\ddag` redéfinis avec significations différentes | Tous les tableaux | Uniformiser les définitions |
| F2 | `\textsc{Balanced/Full/Eco}` casse incohérente | Tout le document | Toujours utiliser `\textsc` |
| F3 | Espaces insécables `~` manquants avant `\cite{}` | `sections/introduction.tex` etc. | Ajouter `~` avant chaque `\cite` |
| F4 | `"behaviour"` (UK) vs `"behavior"` (US) | `sections/limitations.tex` | Uniformiser en US English |
| F5 | `R1--R4` vs `R1---R4` (tiret long vs court) | Tout le document | Uniformiser en `--` (en-dash) |
| F6 | `$C0,\ldots,C3$` vs `C0--C3` | Tout le document | Choisir une notation |
| F7 | `\CaptionFigStatusNote` macro non définie (fichiers non lus) | `sections/results.tex` | Vérifier dans `preamble-ieee.tex` |
| F8 | `\PaperTitleIEEE`, `\PaperAuthorsPDF` macros non inspectées | `main-ieee.tex` | Vérifier `metadata.tex` |

---

## INFORMATIONS À VÉRIFIER (3)

| ID | À vérifier | Fichiers concernés |
|:---|:---|:---|
| I1 | Fichiers non inspectés — anomalies potentielles | `preamble-ieee.tex`, `metadata.tex`, `tables/table04-07.tex`, `bib/references.bib`, tous les `Figures/*.tex`, `code_source_RPL_ClusterIDS/*` |
| I2 | ML pipeline mentionné mais `BLOCKED` / `READY_FOR_SIMULATION` | Clarifier dans le papier que le ML est design-only |
| I3 | `ids_campaign_log` mentionné comme DONE mais non inspecté | Inspecter le code source |

---

## PLAN DE CORRECTION RECOMMANDÉ

### Phase 1 — AVANT SOUMISSION (Critiques + Hautes)
1. **[C1-C2]** Corriger toutes les URLs vers `IDS-IOT`
2. **[C3]** Corriger Elsevier → IEEE
3. **[C4]** Retirer B2/B3 de Table IX ou collecter données
4. **[C5]** Corriger statistiques impossibles B3 (n=1)
5. **[H1]** Vérifier/corriger inversion CPU Eco/Full
6. **[H2]** Ajouter caveat sur p-values n=3
7. **[H3]** Clarifier 3 vs 21 seeds
8. **[H5]** Vérifier données FPR identiques
9. **[H6]** Corriger Computer Networks → IEEE IoT Journal
10. **[H4]** Clarifier ablation "Without clustering"
11. **[H7]** Vérifier figures utilisent bien `data/real/`

### Phase 2 — AVANT SOUMISSION (Moyennes)
12. **[M10-M12]** Créer tableaux manquants ou supprimer références
13. **[M5-M8]** Vérifier chemins fichiers et présence scripts
14. **[M1-M3]** Vérifier tableaux paramètres et macros
15. **[M9]** Distinguer projections dans Fig. 8
16. **[M4]** Vérifier cohérence références bib

### Phase 3 — POLISH FINAL (Faibles)
17. **[F1-F8]** Corrections typographiques et style
18. **[I1]** Inspection complémentaire fichiers non lus

---

**Recommandation** : Transmettez cette liste à l'agent OpenCode en priorisant les 11 anomalies CRITIQUES + HAUTES de la Phase 1. Après correction, republiez le dépôt et je ferai une analyse de suivi sur les anomalies restantes + les fichiers non encore inspectés (`preamble-ieee.tex`, `metadata.tex`, `bib/references.bib`, code source firmware, etc.).
