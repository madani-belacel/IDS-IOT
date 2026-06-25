# RPL-ClusterIDS — Instructions pour assistant AI (complétion du projet)

**Journal cible :** IEEE Internet of Things Journal (IoT Network)  
**Manuscrit :** `IDS_IOT/` — article **distinct** de AER-MQoS (déjà publié)  
**Auteur :** Madani Belacel — ORCID `0009-0003-2928-9565`, `madani.belacel@univ-mosta.dz`  
**Dernière relecture :** 2026-06-08

---

## 0. Mission

Compléter le projet **RPL-ClusterIDS** pour obtenir un article soumettable à l’**IEEE Internet of Things Journal**, avec :

1. **Code source Contiki-NG** fonctionnel (modules IDS + baselines B1–B3).
2. **Campagnes Cooja multi-graines** archivées (logs bruts + CSV agrégés).
3. **Figures 4–11 mesurées** (plus de placeholders TikZ fictifs).
4. **Alignement strict** entre chiffres du manuscrit (`sections/evaluation.tex`, tableaux, abstract) et données CSV.
5. **Références bibliographiques réelles** vérifiées (DOI / pages / titres exacts).
6. **Reproductibilité** documentée (`BUILD_NOTES.txt`, `sim/DATA_PROVENANCE.md`).

> **Ne pas repartir de zéro.** Le manuscrit LaTeX (sections I–VIII), les figures 1–3 illustratives, la biblio de base et la structure IEEE existent déjà. Votre travail principal = **implémentation + simulations + synchronisation chiffres**.

---

## 1. Séparation stricte AER-MQoS ↔ IDS_IOT

| | **AER-MQoS** (publié — ne pas toucher) | **IDS_IOT / RPL-ClusterIDS** (à compléter) |
|---|---|---|
| Sujet | Routage QoS/énergie RPL (AER, MCS, Q-learning) | IDS distribué par **clustering** pour RPL |
| Métriques | PDR, latence, jitter, NRE, contrôle DIO/DAO | Taux détection, FPR, latence détection, overhead alertes, stabilité clusters |
| Protocoles comparés | MRHOF, MQoS, AER, AER-MQoS | B1 central rules, B2 flat distributed, B3 central ML, **Ours** (ClusterIDS) |
| Figures | PDR/latence/énergie routage | Détection/latence IDS/FPR/énergie IDS/clusters |
| Code | `AER-MQoS/code_source_AER_MQoS/` | **À créer** sous `IDS_IOT/code_source_RPL_ClusterIDS/` |
| Données | `AER-MQoS/Section-tex/sim/multi_seed/` | **À créer** sous `IDS_IOT/sim/ids_campaign/` |

**Interdictions :**
- Ne pas copier les CSV PDR/latence d’AER-MQoS dans IDS_IOT.
- Ne pas réutiliser les figures AER-MQoS ni leur pipeline sans adaptation aux métriques IDS.
- Ne pas mentionner AER-MQoS comme contribution de cet article (sauf une phrase de contexte RPL si nécessaire, sans chevauchement de claims).
- Ne pas inventer de chiffres « plausibles » pour remplir les tableaux : **toute valeur numérique publiée doit provenir de logs Cooja parsés**.

**Réutilisation autorisée (méthodologie uniquement) :**
- Structure de scripts (`run_*_campaign.sh`, `parse_cooja_*.py`, `generate_figures_*.py`).
- Format de logs `METRIC,...` (inspiré de `AER-MQoS/code_source_AER_MQoS/simulations/metrics/LOG_FORMAT.md`).
- Gabarit `.csc` Cooja (topologie sky, UDGM, duty cycle 10 %).

---

## 2. État actuel du dépôt (inventaire)

### 2.1 Déjà fait ✓

| Élément | Fichier / dossier | Statut |
|---------|-------------------|--------|
| Titre & métadonnées auteur | `metadata.tex` | Complet |
| Abstract + 8 sections | `sections/*.tex` | Rédigées (anglais académique) |
| Architecture (cœur clustering) | `sections/architecture.tex` | Équations, LAS, politique contextuelle |
| Threat model | `sections/threat_model.tex` | 5 scénarios d’attaque |
| Implémentation (spec) | `sections/implementation.tex` | 5 modules nommés (`clus_form`, `ch_elect`, …) |
| Évaluation (texte + tableaux) | `sections/evaluation.tex` | **Chiffres provisoires** — à remplacer par mesures |
| Figures 1–3 | `Figures/Fig_1..3_*.tex` | TikZ illustratif — OK pour soumission |
| Figures 4–11 | `Figures/Fig_4..11_*.tex` | **PLACEHOLDER TikZ** — à remplacer |
| Biblio initiale | `bib/references.bib` | ~20 entrées — **à vérifier une par une** |
| Build IEEE | `main-ieee.tex` | Compile → `main-ieee.pdf` |
| Manifest figures | `figures_manifest.csv` | 11 figures cataloguées |
| Checklist | `checklist.md` | À mettre à jour après chaque passe |

### 2.2 Manquant ✗ (travail principal)

| Élément | Emplacement attendu |
|---------|---------------------|
| Code firmware Contiki-NG | `IDS_IOT/code_source_RPL_ClusterIDS/` |
| Scénarios Cooja (.csc) | `code_source_RPL_ClusterIDS/simulations/cooja/` |
| Scripts campagne | `code_source_RPL_ClusterIDS/simulations/scripts/` |
| Logs bruts Cooja | `code_source_RPL_ClusterIDS/simulations/logs/ids_campaign/` |
| CSV agrégés | `IDS_IOT/sim/ids_campaign/*.csv` |
| Script génération figures | `IDS_IOT/scripts/generate_ids_figures.py` |
| Provenance données | `IDS_IOT/sim/DATA_PROVENANCE.md` |
| BUILD_NOTES rempli | `IDS_IOT/BUILD_NOTES.txt` |

---

## 3. Environnement de travail

### 3.1 Phase actuelle (Windows)

- Édition LaTeX, relecture, scripts Python (matplotlib), préparation des specs.
- **Pas de Cooja natif sous Windows** : ne pas prétendre avoir lancé des simulations Cooja depuis Windows.
- Compiler le PDF : TeX Live (`pdflatex`, `bibtex`) — voir `README.md`.

### 3.2 Phase production (Ubuntu — Contiki-NG + Cooja)

L’utilisateur déplacera `IDS_IOT/` vers la section Ubuntu où Contiki-NG et Cooja sont installés (même layout que pour AER-MQoS).

**Prérequis Ubuntu :**
```bash
# Depuis la racine Contiki-NG utilisée par l'utilisateur
git describe --always          # noter le hash
make -C examples/... TARGET=sky # valider toolchain MSP430
# Cooja : Gradle + JDK (Contiki-NG tools/cooja)
```

**Variables d'environnement recommandées :**
```bash
export CONTIKI=/path/to/contiki-ng
export IDS_ROOT=/path/to/projet_madani_v2_ubuntu/IDS_IOT
export IDS_CODE=$IDS_ROOT/code_source_RPL_ClusterIDS
```

Documenter dans `BUILD_NOTES.txt` : hash Contiki-NG, version JDK, `pdflatex --version`, date UTC.

---

## 4. Architecture cible du projet complet

```
IDS_IOT/
├── instruction.md              ← ce fichier
├── checklist.md                ← suivi passe par passe
├── BUILD_NOTES.txt             ← provenance build (à remplir)
├── metadata.tex
├── main-ieee.tex               ← SOUMETTRE main-ieee.pdf
├── sections/                   ← manuscrit (sync chiffres après campagne)
├── Figures/                    ← Fig_1..11 (4–11 = mesurées)
├── bib/references.bib
├── figures_manifest.csv
├── scripts/
│   ├── generate_ids_figures.py ← CSV → PDF/TeX pour Figs 4–11
│   ├── analyze_ids_stats.py    ← moyennes, écarts-type, tests (optionnel)
│   └── sync_evaluation_tex.py  ← (optionnel) injecte moyennes dans evaluation.tex
├── sim/
│   ├── DATA_PROVENANCE.md
│   ├── README.md               ← schéma colonnes CSV
│   └── ids_campaign/
│       ├── detection_rate.csv
│       ├── latency.csv
│       ├── fpr.csv
│       ├── energy.csv
│       ├── alerts.csv
│       ├── stability.csv
│       ├── temporal.csv
│       ├── modes.csv
│       ├── stats/
│       │   └── summary_table.csv
│       └── campaign_manifest.tsv
└── code_source_RPL_ClusterIDS/
    ├── README.md
    ├── Makefile
    ├── project-conf.h
    ├── clusterids-node.c         ← firmware principal
    ├── clus_form.c / .h
    ├── ch_elect.c / .h
    ├── ids_member.c / .h
    ├── ids_ch.c / .h
    ├── ctx_policy.c / .h
    ├── ids_campaign_log.c / .h
    ├── variants/               ← B1, B2, B3, CLUSTERIDS
    └── simulations/
        ├── README_CAMPAIGNS.md
        ├── metrics/LOG_FORMAT.md
        ├── cooja/*.csc
        ├── scripts/
        │   ├── build_variant.sh
        │   ├── generate_campaign_csc.py
        │   ├── parse_cooja_ids_metrics.py
        │   └── run_ids_campaign.sh
        └── logs/ids_campaign/
```

---

## 5. Spécification firmware (alignée sur le manuscrit)

Lire **obligatoirement** avant d’implémenter :
- `sections/architecture.tex` — équations (1)–(4), règles R1–R4, LAS, modes Full/Balanced/Eco
- `sections/implementation.tex` — 5 modules, empreintes RAM/CPU annoncées
- `sections/threat_model.tex` — attaques et métriques surveillées
- `sections/evaluation.tex` — protocoles B1–B3, scénarios, tailles réseau (50/100/200 nœuds)

### 5.1 Variantes firmware (4 builds)

| Tag | Description | Compile flag |
|-----|-------------|--------------|
| `B1` | IDS rule-based centralisé sur border router | `IDS_VARIANT=B1` |
| `B2` | IDS rules distribuées plates + flooding alertes | `IDS_VARIANT=B2` |
| `B3` | Hybrid ML sur border router, sans clustering | `IDS_VARIANT=B3` |
| `CLUSTERIDS` | RPL-ClusterIDS complet | `IDS_VARIANT=CLUSTERIDS` |

Tous partagent : même stack RPL (`rpl-lite`), même trafic applicatif UDP, mêmes classes C0–C3, même modèle radio.

### 5.2 Attaques à implémenter (5 scénarios)

1. **Rank attack** — nœuds malveillants annoncent rang artificiellement bas  
2. **Selective forwarding** — drop 60 % paquets downstream  
3. **Wormhole** — 2 nœuds collusion tunnel trafic contrôle  
4. **DAO flooding** — DAO ×10 fréquence baseline  
5. **Mixed campaign** — rank + selective drop sur flux C3  

Attaque démarre après **30 min** de stabilisation. Durée totale simulée : **3 h** (10 800 s) — comme §VI.

### 5.3 Logs structurés `METRIC,...`

Créer `simulations/metrics/LOG_FORMAT.md` avec lignes minimales :

```
METRIC,DET,<seed>,<variant>,<scenario>,<tp>,<fp>,<tn>,<fn>,<det_rate>
METRIC,LAT,<seed>,<variant>,<scenario>,<latency_s_mean>
METRIC,FPR,<seed>,<variant>,<scenario>,<class>,<fpr>
METRIC,NRG,<seed>,<variant>,<role>,<mode>,<cpu_pct>,<ram_kb>,<energest_delta_pct>
METRIC,ALERT,<seed>,<variant>,<nodes>,<alerts_per_hour>
METRIC,CLUST,<seed>,<time_min>,<ch_tenure_s>,<recluster_rate>,<mean_nre>
METRIC,TEMP,<seed>,<phase>,<det_rate>          # phase: stab|attack|recovery
METRIC,MODE,<seed>,<mode>,<det_rate>,<fpr>,<cpu_pct>
METRIC,ATTACK,<seed>,<scenario>,<event_id>,<t_start>,<t_end>  # ground truth
```

Activer via `IDS_CONF_CAMPAIGN_METRICS=1` au build Cooja.

---

## 6. Campagne Cooja — protocole expérimental

### 6.1 Paramètres (§VI — ne pas modifier sans mettre à jour le texte)

| Paramètre | Valeur |
|-----------|--------|
| Plateforme | sky mote (MSP430) |
| Topologies | grille + aléatoire |
| Tailles réseau | 50, 100, 200 nœuds |
| Duty cycle radio | 10 % |
| Attaquants | 5–10 % population, profondeurs DODAG variées |
| Graines | **≥ 9** (cible **20** pour robustesse) |
| Timeout sim | `SIM_TIMEOUT_MS=10800000` (3 h) |
| Modes IDS | Full, Balanced, Eco (campagnes séparées ou tag log) |

### 6.2 Pipeline campagne (modèle AER-MQoS)

```bash
# 1. Smoke test (90 s, 3 graines) — valider toolchain
NUM_SEEDS=3 SIM_TIMEOUT_MS=90000 ./simulations/scripts/run_ids_campaign.sh smoke

# 2. Pilote (1800 s, 5 graines) — valider parseur
NUM_SEEDS=5 SIM_TIMEOUT_MS=1800000 ./simulations/scripts/run_ids_campaign.sh pilot

# 3. Campagne publication (3 h, ≥9 graines)
NUM_SEEDS=9 SIM_TIMEOUT_MS=10800000 ./simulations/scripts/run_ids_campaign.sh full
```

Pour chaque run : sauvegarder `log_<VARIANT>_<TOPO>_<N>nodes_<SCENARIO>_seed<SEED>.log`.

### 6.3 Parsing → CSV

```bash
python3 simulations/scripts/parse_cooja_ids_metrics.py \
  --logs simulations/logs/ids_campaign/ \
  --out $IDS_ROOT/sim/ids_campaign/
```

Le parseur doit produire les 8 CSV référencés dans `figures_manifest.csv`.  
Générer aussi `stats/summary_table.csv` (moyenne ± écart-type par variant/scenario).

---

## 7. Schéma des CSV (obligatoire)

Voir `sim/README.md` (à créer). Colonnes minimales :

**detection_rate.csv**
```
variant,seed,scenario,nodes,topology,mode,det_rate,tp,fp,tn,fn
```

**latency.csv**
```
variant,seed,scenario,latency_s_mean,latency_s_std
```

**fpr.csv**
```
variant,seed,scenario,traffic_class,fpr
```

**energy.csv**
```
variant,seed,role,mode,cpu_overhead_pct,ram_kb,energest_delta_pct,nodes
```

**alerts.csv**
```
variant,seed,nodes,alerts_per_hour,control_pkts_per_hour
```

**stability.csv**
```
seed,time_min,ch_tenure_s_mean,recluster_events,mean_nre
```

**temporal.csv**
```
seed,phase,det_rate   # phase ∈ {stabilization,attack,recovery}
```

**modes.csv**
```
seed,mode,det_rate,fpr,cpu_overhead_pct
```

---

## 8. Figures — génération et remplacement

### 8.1 Règle d’or

**Aucune figure 4–11 ne doit contenir de barres/ courbes inventées.**  
Supprimer `\CaptionFigVisualDisclaimer` des légendes une fois les données mesurées sont intégrées (`Figures/CAPTIONS_EN.tex`).

### 8.2 Workflow

```bash
cd IDS_IOT
python3 scripts/generate_ids_figures.py --csv sim/ids_campaign/ --out Figures/
pdflatex -interaction=nonstopmode main-ieee.tex
bibtex main-ieee
pdflatex -interaction=nonstopmode main-ieee.tex
pdflatex -interaction=nonstopmode main-ieee.tex
```

Mettre à jour `figures_manifest.csv` : statut `PLACEHOLDER` → `MEASURED`.

### 8.3 Format figure

- Préférer **PDF vectoriel** inclus via `\includegraphics` OU mettre à jour les `.tex` TikZ/pgfplots avec données `\pgfplotstableread` depuis CSV.
- Conserver les noms de fichiers existants (`Fig_4_Detection_Rate_Comparison.tex`, etc.) pour ne pas casser `evaluation.tex`.

---

## 9. Synchronisation manuscrit ↔ données

### 9.1 Fichiers à mettre à jour après campagne

| Fichier | Contenu à synchroniser |
|---------|------------------------|
| `sections/evaluation.tex` | Tableaux I–II, paragraphes avec %, latences, overhead |
| `sections/abstract.tex` | « above 93 % », « under 6 % CPU », « 2.8 KB RAM » |
| `sections/implementation.tex` | Empreintes RAM/CPU/Flash (moyennes mesurées) |
| `sections/conclusion.tex` | Reformuler si chiffres changent |
| `Figures/CAPTIONS_EN.tex` | Retirer disclaimer Figs 4–11 |

### 9.2 Règle de cohérence (reviewer-proof)

Pour **chaque** nombre dans le PDF :
1. Tracer jusqu’au CSV (`sim/ids_campaign/`).
2. Vérifier moyenne sur N graines ≥ 9.
3. Arrondir : taux détection → 2 décimales ; latence → entier secondes ; CPU → 1 décimale %.
4. Si mesure **contredit** le placeholder actuel → **modifier le texte**, jamais l’inverse.

**Exemples de claims actuels à re-valider :**
- Table détection (50-node grid, Balanced) : Ours 0.96 rank, 0.95 sel.fwd, … FPR 0.03  
- Latence détection : 18–34 s  
- Overhead énergie : 4.2 % membres, 7.8 % CH (Balanced) ; 2.1 % membres (Eco)  
- Alertes 200 nœuds : −67 % vs B2, −41 % vs B3  
- Ablation clustering : −4–7 % accuracy, alertes ×2.3  
- Table modes : Full 0.93/0.04/7.1 %, Balanced 0.91/0.03/5.8 %, Eco 0.84/0.02/3.2 %

### 9.3 Abstract — contraintes IEEE IoT Journal

- 150–250 mots (vérifier count actuel).
- Pas de citations dans l’abstract.
- Chiffres = moyennes campagne, pas max d’une graine.
- Index Terms : 8–10 mots (déjà dans `sections/abstract.tex`).

---

## 10. Bibliographie — références réelles

### 10.1 État actuel

`bib/references.bib` contient des entrées **plausibles mais non vérifiées** (ex. `garg2023`, `hamdi2024`, `dib2024`, `raza2018cluster` avec pages suspectes).

### 10.2 Procédure obligatoire

Pour **chaque** `\cite{...}` du manuscrit :
1. Vérifier existence (Google Scholar, IEEE Xplore, DOI).
2. Corriger auteurs, titre, volume, pages, année.
3. Ajouter `doi = {...}` quand disponible.
4. Supprimer toute entrée non retrouvable — remplacer par source réelle équivalente.
5. Viser **35–50 références** pour soumission IoT Journal (actuellement ~20).

### 10.3 Références IDS RPL prioritaires à inclure (vérifier DOI)

- Mayzaud et al. 2016 (IEEE Comm. Surveys) — déjà présent ✓  
- Raza et al. 2017 (IEEE IoT Journal) — déjà présent ✓  
- Sfar et al. 2018 (IEEE IoT Journal) — déjà présent ✓  
- RFC 6550, RFC 7416 — déjà présents ✓  
- Travaux récents 2022–2025 sur IDS RPL hybride / clustering / TinyML (à rechercher et ajouter)

**Ne pas citer AER-MQoS** comme référence principale de cet article.

---

## 11. Critères relecteur — IEEE IoT Journal

Un reviewer IoT Journal vérifiera typiquement :

| Critère | Action |
|---------|--------|
| **Originalité clustering** | §IV doit dominer ; ablation avec/sans clustering obligatoire |
| **Threat model clair** | §III : adversaire interne, capacités, limites IDS |
| **Baseline fairness** | B1–B3 même trafic, même topologie, même charge attaque |
| **Reproductibilité** | Code + scripts + logs archivés ; pas « simulation-only » sans détails |
| **Overhead honnête** | RAM/CPU/Energest mesurés, pas estimés |
| **Statistique** | Multi-graines, écart-type ou intervalle de confiance |
| **Pas de placeholder** | Aucune mention « conceptual placeholder » dans PDF final |
| **English quality** | Phrases naturelles, pas de listes IA ; cohérence terminologique |
| **Figures lisibles** | Deux colonnes IEEE : labels ≥ `\footnotesize`, légendes explicites |

### 11.1 Points faibles actuels (P0 — bloquants soumission)

1. Figs 4–11 = placeholders + disclaimer visible dans PDF.  
2. Aucun code Contiki-NG ni log Cooja.  
3. Chiffres §VI non traçables.  
4. Références partiellement fictives.  
5. `BUILD_NOTES.txt` vide.

### 11.2 Forces actuelles (à préserver)

1. Architecture clustering bien développée (équations, LAS, politique contextuelle).  
2. Structure IEEE complète et compilable.  
3. Positionnement Related Work + tableau comparatif.  
4. Séparation claire vs AER-MQoS.  
5. Plan 11 figures cohérent avec l’évaluation.

---

## 12. Ordre de travail recommandé (passe par passe)

### Passe 1 — Fondations (Ubuntu)
- [ ] Créer `code_source_RPL_ClusterIDS/` + Makefile + `project-conf.h`
- [ ] Implémenter trafic C0–C3 + logging `METRIC,...`
- [ ] Implémenter variante B1 (baseline minimal)
- [ ] Smoke test Cooja 3 nœuds

### Passe 2 — IDS complet
- [ ] Modules `clus_form`, `ch_elect`, `ids_member`, `ids_ch`, `ctx_policy`
- [ ] Variantes B2, B3, CLUSTERIDS
- [ ] Implémenter 5 injecteurs d’attaque
- [ ] Pilote 1800 s × 5 graines

### Passe 3 — Campagne publication
- [ ] Campagne full 3 h × ≥9 graines × 4 variantes × 5 scénarios × 3 tailles
- [ ] Parser → CSV → `sim/ids_campaign/`
- [ ] `DATA_PROVENANCE.md` + `BUILD_NOTES.txt`

### Passe 4 — Figures & manuscrit
- [ ] `generate_ids_figures.py` → Figs 4–11 MEASURED
- [ ] Sync `evaluation.tex`, `abstract.tex`, `implementation.tex`
- [ ] Retirer disclaimers ; recompiler `main-ieee.pdf`

### Passe 5 — Relecture finale
- [ ] Vérifier toutes références
- [ ] Relire §IV (clustering = contribution centrale)
- [ ] Checklist `checklist.md` → P0=0, P1=0, P2=0
- [ ] Vérification : `pdftotext main-ieee.pdf - | grep -c '\[?'` → 0

---

## 13. Documents sources à lire en premier

| Priorité | Fichier | Pourquoi |
|----------|---------|----------|
| 1 | `Message_cursor1.txt` | Brief initial auteur |
| 2 | `Discussion_Grok.txt` | Genèse idée clustering, abstract brouillon |
| 3 | `sections/architecture.tex` | Spec technique complète |
| 4 | `sections/evaluation.tex` | Protocole expérimental + chiffres cibles |
| 5 | `figures_manifest.csv` | Mapping figure → CSV |
| 6 | `AER-MQoS/.../simulations/README_CAMPAIGNS.md` | **Méthodo only** — pas les données |
| 7 | `AER-MQoS/.../sim/DATA_PROVENANCE.md` | Modèle provenance |
| 8 | `checklist.md` | Suivi avancement |

---

## 14. Anti-patterns (ne jamais faire)

- ❌ Générer des CSV avec `numpy.random` pour « faire joli »  
- ❌ Copier-coller paragraphes ou figures d’AER-MQoS  
- ❌ Laisser « placeholder » ou « TBD » dans le PDF soumis  
- ❌ Citer un article sans vérifier DOI  
- ❌ Annoncer déploiement hardware (hors scope — simulation Cooja uniquement)  
- ❌ Modifier RPL (`rpl-lite`) — IDS en overlay UDP  
- ❌ Soumettre `main.pdf` (brouillon 1 colonne) au lieu de `main-ieee.pdf`  
- ❌ Mélanger métriques routage (PDR) et métriques IDS (detection rate)  

---

## 15. Livrables finaux attendus

1. `main-ieee.pdf` — camera-ready, sans placeholder, sans `[?]` citations  
2. `code_source_RPL_ClusterIDS/` — compilable, README avec instructions build  
3. `sim/ids_campaign/` — CSV + stats + manifest  
4. `simulations/logs/ids_campaign/` — logs bruts (ou archive `.tar.gz` avec checksum)  
5. `BUILD_NOTES.txt` — hash git Contiki-NG, paramètres campagne, date  
6. `checklist.md` — tout coché, P0=P1=P2=0  
7. (Optionnel) Archive Zenodo / supplementary — code + datasets pour reproductibilité  

---

## 16. Contact & métadonnées soumission

- **Titre portail ScholarOne** = `\PaperTitle` dans `metadata.tex` (mot pour mot)  
- **Byline page 1** : Madani Belacel seul ; affiliation + e-mail + ORCID en footnote (`\IEEEaftertitletext`)  
- **Fichier soumis** : `main-ieee.pdf`  
- **Cover letter** (hors scope AI) : insister sur clustering energy-aware + reproductibilité  

---

*Fin instruction.md — mettre à jour la date en tête si le protocole expérimental change.*
