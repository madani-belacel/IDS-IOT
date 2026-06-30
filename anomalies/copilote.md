Gathered additional information

Get data from /repos/madani-belacel/IDS-IOT/contents

Using results of get file and 6 other tool calls

View directory code_source_RPL_ClusterIDS
Résumé rapide (en une phrase) RPL-ClusterIDS est une implémentation Contiki‑NG d’un IDS hiérarchique pour RPL axé sur le clustering économe en énergie, accompagnée d’un paquet reproductible (firmware, scripts de campagne Cooja, parseurs, figures LaTeX) et d’un pilotage expérimental sur 50 nœuds annoncé dans le manuscrit destiné à Computer Networks.

Preuve lue (ce que j’ai inspecté)

README.md, SIMULATION_CAMPAIGN_READY/README.md, Figures/README.md, figures_manifest.csv
main.tex + preambles et sections (abstract, introduction, results, etc.)
tables/table02_detection.tex et plusieurs inclusions de tables/figures dans sections/results.tex
dossier code_source_RPL_ClusterIDS (Makefile, nombreux .c/.h : clusterids-node.c, ids_member.c, ids_ch.c, ch_elect.c, ctx_policy.c, ids_campaign_log.c, etc.)
structure de données (data/, data/real/parsed mentionné), scripts (scripts/python/generate_figures.py, scripts/statistics/compute_statistics.py)
pistes de campagne : SIMULATION_CAMPAIGN_READY (run_campaign.sh, campaign_matrix.tsv, seeds.txt)
Points forts

Cohérence conceptuelle et contribution claire : clustering dynamique prenant en compte énergie résiduelle, stabilité topologique et priorité de trafic — contribution bien cadrée par rapport aux limites identifiées de travaux antérieurs (sec. introduction).
Artéfacts de reproduction fournis : code Contiki‑NG, scripts de campagne, parseurs, figures LaTeX et manifeste des figures ; la structure du dépôt est pensée pour reproduire l’étude.
Manuscrit structuré selon une soumission Elsevier (elsarticle), avec highlights, abstract, sections complètes et bibliographie incluse.
Implémentation concrète dans Contiki‑NG (fichiers source détaillés) — pas seulement simulation conceptuelle.
Déclaration de design expérimental (SIMULATION_CAMPAIGN_READY) : matrice factorielle, seeds, définitions de métriques et scripts d’exécution.
Anomalies, problèmes et éléments à corriger (ordre d’importance)

Statistique et puissance expérimentale insuffisantes / résultats possiblement trompeurs
Table de détection (tables/table02_detection.tex) : CLUSTERIDS évalué avec 21 seeds, B1 avec 3 seeds — comparaison asymétrique invalide pour tests statistiques. L’affirmation “p < 0.05 (Welch’s t‑test; preliminary with n=21 and n=3)” (sections/results.tex) est trompeuse : n=3 rend le test non fiable et la normalité/non‑homogénéité non vérifiée.
Pas d’IC (intervalle de confiance) ni d’estimation d’effet (Cohen’s d, taille d’effet) ; seules valeurs ponctuelles affichées.
Taille et portée des expériences
Pilotage limité à 50 nœuds ; figures et discussion font référence à projections jusqu’à 500 nœuds mais les données empiriques manquent.
Figures incomplètes / placeholders
Figures/README.md signale de nombreux panels comme "PLACEHOLDER" (Fig_4…Fig_11). Le manuscrit intègre ces fichiers ; il faut remplacer les placeholders par données réelles (vecteur si possible) avant soumission.
Définitions et métriques
Définition d’une « campaign‑level detection rate » ambiguë : le pied de table dit “at least one confirmed alert per attack period” — cela doit être formalisé (est‑ce la métrique principale ?).
Déclarations sur FPR identiques pour B1 et RPL‑ClusterIDS expliquées par un partage de seuils (table02 note) : nécessitent justification et explication technique (pourquoi le seuil de première étape est commun et quel est l’impact sur comparaison).
Reproductibilité pratique
Les scripts et instructions existent mais :
préciser versions exactes (Contiki‑NG version, Cooja/Sim version, OS, Python packages versions).
verrouiller requirements (requirements.txt existe mais vérifier qu’il contient versions fixes).
fournir un script d’installation/contenerisation (Dockerfile ou instructions reproducible) et tests de smoke.
Absence d’un DOI/archivage (Zenodo) ou d’un fichier CITATION.cff / LICENSE (je n’ai pas vu LICENSE en top‑level).
Qualité du manuscrit / LaTeX
Captions référencées via Figures/CAPTIONS_EN.tex — vérifier qu’elles sont complètes et informatives.
S’assurer que les tableaux contiennent n (taille d’échantillon), écarts‑types, et tests statistiques détaillés.
Mesures d’énergie
Energest est mentionné mais méthodologie (conversion unités → consommation réelle, hypothèses sur batterie) pas détaillée ; fournir méthode de conversion et incertitudes.
Baselines et comparaisons
B1/B2/B3 mentionnées mais B2/B3 non évaluées dans pilot; pour la revue, il est préférable d’avoir comparaisons complètes ou de justifier l’absence.
Aspects de code
Documenter paramètres clefs (tau_low, tau_CH, tau_inter, w_e, w_d, lambda_1…4) : localiser dans ids_conf.h/project-conf.h et exposer valeurs par défaut et motivation.
Ajouter instructions de compilation détaillées (README dans code_source déjà présent mais s’assurer qu’il est complet).
Métadonnées de soumission
Déclarations obligatoires pour Elsevier : conflict of interest, funding, data availability — vérifier inclusion (metadata.tex présent, mais valider contenu).
Suggestions concrètes pour atteindre le niveau d’un article accepté par Computer Networks Expérimentation et statistique

Équilibrer les tailles d’échantillon des variantes : exécuter B1/B2/B3 avec le même nombre de seeds que CLUSTERIDS (idéal ≥ 20 par condition) ; pour comparaisons importantes viser n≥20–30 selon variance.
Remplacer Welch t‑test préliminaire par une démarche robuste :
rapporter distributions par seed (boxplots/violin plots) pour DR et FPR ;
fournir IC 95% (bootstrap si distribution inconnue) pour DR/FPR ;
utiliser tests non‑paramétriques (Mann‑Whitney) si conditions de normalité non respectées ;
corriger comparaisons multiples (Bonferroni / Holm) quand vous testez plusieurs scénarios.
Rapporter taille d’effet (Cohen’s d ou autre) et puissance calculée pour les comparaisons clés.
Fournir matrice de confusion agrégée, courbes ROC/PR si applicable, et métriques par scénario (rank, sel_fwd, wormhole, dao_flood, mixed) avec erreur standard.
Étendre la campagne à échelles supérieures (100–500) ou fournir simulation analytique/estimation validée pour justifier les projections.
Manuscrit & Figures

Remplacer tous les placeholders de Figures par versions finales (préférence : PDF/vectoriel pour TikZ/PGFPlots ; PNG haute résolution si image raster nécessaire).
Rendre chaque légende auto‑suffisante (n, mode opératoire, condition expérimentale).
Indiquer clairement le nombre d’exécutions (seeds) dans le caption des figures et en légende de tables.
Améliorer la section « Statistical Validation » : exposition claire de tests, hypothèses, seuil alpha, corrections et interprétation pratique des résultats.
Détailler limitations (section limitations déjà présente : étoffer sur généralisation hors topologie grid, timings différents, charge réelle du trafic IoT).
Reproductibilité

Fournir un container (Docker) ou script d’environnement (Makefile top‑level / instructions pas à pas) qui installe :
Contiki‑NG commit hash ou version (ex.: vX.Y), Cooja/Sky/emu versions,
Python versions et packages avec versions (requirements.txt pin),
tout outil auxiliaire (awk, sed, Java version si Cooja dépend de Java).
Archiver les données finales (parsed/aggregated, scripts de parsing) et demander un DOI (Zenodo) ; placer le lien DOI dans le manuscrit et le README.
Inclure un small smoke test (ex.: run_campaign.sh --pilot reproduit exactement figures X–Y) et un rapport de checksum/MD5 des sorties.
Ajouter un fichier LICENSE (MIT/Apache2) et CITATION.cff.
Code & documentation

Documenter et commenter les paramètres exposés dans ids_conf.h et project-conf.h ; ajouter un tableau paramètre → valeur par défaut → justification dans documentation.
Exécuter une compilation propre et corriger warnings du compilateur (-Wall -Wextra) ; documenter options de cross‑compilation si besoin.
Ajouter tests unitaires ou scripts de validation pour les parseurs (parse_cooja_ids_metrics.py).
Publier exemples de logs bruts et des scripts exacts pour générer les fichiers agrégés (pour que le relecteur/reader reproduise les chiffres).
Méthodologie/mesures d’énergie

Décrire exactement comment Energest a été instrumenté, quelles composantes d’énergie sont mesurées, et comment cela se traduit en % d’autonomie ; présenter incertitudes de mesure.
Fournir profils CPU/mémoire pour CH vs member dans des tableaux.
Rédaction / formalisme

Clarifier définition de la métrique principale (campaign‑level DR) et donner métriques secondaires (per‑attack DR, time‑to‑detect médian, FPR par intervalle).
Ajouter discussion de sécurité (attaques non couverts, robustesse aux attaques adaptatives).
Ajouter une courte « Reproducibility statement » (manuscript) avec lien DOI et instructions simplifiées.
Checklist finale avant soumission (items à cocher) Manuscrit

 Manuscrit formaté selon les instructions d’Elsevier (elsarticle) : marges, lenght, highlights, keywords.
 Abstract concis (150–250 mots selon la consigne), highlights précis.
 Toutes les figures finales insérées (aucun placeholder) ; légendes complètes avec n, conditions et métriques.
 Toutes les tables contiennent n, moyenne ± écart‑type/IC, et test statistique indiqué.
 Section statistique révisée : tests appropriés, ICs, tailles d’effet, corrections multiples.
 Limitations et future work clairement énoncés.
 Déclarations obligatoires : Funding, Conflict of Interest, Data Availability, Author Contributions (si demandé).
 Orthographe/anglais relu (preferable review by a native or professional proofreader).
Expérimentations et données

 Exécuter campagne complète ou étendre pilot pour équilibrer baselines (B1/B2/B3) avec enough seeds (≥ 20 each).
 Produire et sauvegarder toutes les sorties agrégées utilisées pour figures/tables.
 Générer et ajouter courbes distributionnelles (boxplots/violin/ROC/PR).
 Archiver dataset et code (Zenodo) → obtenir DOI.
Reproductibilité et artefacts

 README top‑level mis à jour avec commandes minimales reproductibles.
 requirements.txt avec versions figées ; ajouter environment file / Dockerfile.
 Scripts d’exécution clairement documentés (SIMULATION_CAMPAIGN_READY/run_campaign.sh usage complet).
 Fournir smoke test (pilot) qui reproduit quelques résultats clés.
 LICENSE ajoutée et CITATION.cff.
Code et construction

 Makefile/README du code_source complet et testé sur la version indiquée de Contiki‑NG.
 Compiler sans warnings et documenter flags.
 Paramètres principaux exposés et documentés dans un tableau.
 Tests des parseurs et scripts d’analyse (unit/block tests ou exemples).
Présentation & fichiers LaTeX

 Figures vectorielles (TikZ/PGFPlots) ou PNG 300dpi si nécessaire ; vérifier taille caméra/embedding.
 Bibliographie complète et formatée ; vérifier doublons et entrées incomplètes.
 Fichiers annexes (CAPTIONS_EN.tex, status-macros.tex) inclus dans l’archive soumise.
Points à expliciter dans la lettre de soumission

Clarté que l’artefact complet (code + data + scripts) est disponible et où (inclure DOI).
Limites connues (échelle pilotée à 50 nœuds; plan de campagne complet en cours).
Pourquoi la méthode est pertinente pour la communauté (gain énergie vs détection, scalabilité attendue).
Conclusion Le projet est à un stade solide : idée claire, implémentation opérationnelle et artefacts de reproduction présents. Pour atteindre le niveau attendu par Computer Networks, il reste principalement à renforcer la rigueur expérimentale et statistique (équilibrer tailles d’échantillon, ajouter IC/tailles d’effet, compléter figures), finaliser la reproductibilité pratique (versions figées, DOI, container), et remplacer les figures/textes placeholders. Si vous voulez, je peux fournir (1) une checklist prête à coller dans votre MASTER_TRACKER.md/IEEE_SUBMISSION_CHECKLIST.md, (2) un exemple de paragraphe statistique à insérer dans la section Validation, ou (3) une liste précise de commandes Docker / environment.yml pour verrouiller l’environnement expérimental.

vous pouvez corriger ces erreurs en ligne?
Je suis en attente de votre confirmation via la boîte de dialogue (accepter ou refuser) pour pouvoir lancer et finaliser les corrections en ligne.

Make these code changes?
sections/results.tex

TeX
% Updated Results section: make statistical claims cautious and document planned analysis.
\section{Results}
\label{sec:results}

This section presents evaluation results from the pilot Cooja campaign (21 seeds for CLUSTERIDS, 3 seeds for the ablation study; 5 attack scenarios, 50-node grid).
Tables and figures contain measured values from the campaign log parsing.
Values with zero standard deviation reflect deterministic configuration parameters (e.g.,~FPR) and single-run per-seed latency measurements; statistical significance tests were not performed on the full campaign dataset.

\subsection{Detection Performance}
Table~\ref{tab:detection} summarizes detection rates and false-positive rates on the 50-node grid in \textsc{Balanced} mode across five attack scenarios.
Fig.~\ref{fig:detection-rate} and Fig.~\ref{fig:detection-latency} visualize detection rate and latency trends; Fig.~\ref{fig:fpr-scenario} stratifies false positives by scenario and traffic-priority.

\input{tables/table02_detection}

\begin{figure}[!t]
  \centering
  \resizebox{\linewidth}{!}{\input{Figures/Fig_4_Detection_Rate_Comparison.tex}}
  \caption{\CaptionFigFour{} \CaptionFigStatusNote}
  \label{fig:detection-rate}
\end{figure}

\begin{figure}[!t]
  \centering
  \resizebox{\linewidth}{!}{\input{Figures/Fig_5_Detection_Latency_Comparison.tex}}
  \caption{\CaptionFigFive{} \CaptionFigStatusNote}
  \label{fig:detection-latency}
\end{figure}

\begin{figure}[!t]
  \centering
  \resizebox{\linewidth}{!}{\input{Figures/Fig_6_FPR_By_Scenario.tex}}
  \caption{\CaptionFigSix{} \CaptionFigStatusNote}
  \label{fig:fpr-scenario}
\end{figure}

\subsection{Overhead, Energy, and Scalability}
Fig.~\ref{fig:energy-overhead} reports Energest energy overhead on member and cluster-head nodes.
Fig.~\ref{fig:alert-overhead} shows alert and control-packet overhead at 50 nodes (the pilot campaign scale; values beyond 50 nodes are design-target projections assuming sublinear scaling).
Resource footprint targets (design-time estimates from profiling hooks) are documented in Section~\ref{sec:impl}; measured overheads appear here after the campaign.

\begin{figure}[!t]
  \centering
  \resizebox{\linewidth}{!}{\input{Figures/Fig_7_Energy_Overhead_Comparison.tex}}
  \caption{\CaptionFigSeven{} \CaptionFigStatusNote}
  \label{fig:energy-overhead}
\end{figure}

\begin{figure}[!t]
  \centering
  \resizebox{\linewidth}{!}{\input{Figures/Fig_8_Alert_Control_Overhead.tex}}
  \caption{\CaptionFigEight{} \CaptionFigStatusNote}
  \label{fig:alert-overhead}
\end{figure}

\subsection{Ablation Study}
Table~\ref{tab:ablation} compares five system variants on the mixed campaign scenario: full RPL-ClusterIDS, and ablations that disable clustering, CH threshold verification, context adaptation, or other components.
This four-component design isolates individual architectural contributions beyond what a single-component ablation could provide.

\input{tables/table08_ablation}

Fig.~\ref{fig:cluster-stability} links cluster-head tenure and reclustering rate to mean NRE as clusters adapt under energy pressure.

\begin{figure}[!t]
  \centering
  \resizebox{\linewidth}{!}{\input{Figures/Fig_9_Cluster_Stability.tex}}
  \caption{\CaptionFigNine{} \CaptionFigStatusNote}
  \label{fig:cluster-stability}
\end{figure}

\subsection{Temporal Behavior and Operating Modes}
Fig.~\ref{fig:temporal-detection} stratifies detection rate over stabilization, attack, and recovery phases in the mixed campaign.
Table~\ref{tab:modes} and Fig.~\ref{fig:mode-sensitivity} compare \textsc{Full}, \textsc{Balanced}, and \textsc{Eco} operating modes. The campaign-level DR remains stable across modes because several detection opportunities are equivalent across modes for the pilot grid; larger-scale or longer-duration runs are needed to assess differences fully.

\input{tables/table03_operating_modes}

\begin{figure}[!t]
  \centering
  \resizebox{\linewidth}{!}{\input{Figures/Fig_10_Temporal_Detection_Stratification.tex}}
  \caption{\CaptionFigTen{} \CaptionFigStatusNote}
  \label{fig:temporal-detection}
\end{figure}

\begin{figure}[!t]
  \centering
  \resizebox{\linewidth}{!}{\input{Figures/Fig_11_Operating_Mode_Sensitivity.tex}}
  \caption{\CaptionFigEleven{} \CaptionFigStatusNote}
  \label{fig:mode-sensitivity}
\end{figure}

\subsection{Statistical Validation}
The pilot campaign provides descriptive evidence for RPL-ClusterIDS performance on a 50-node grid. Current pilot results report a campaign-level detection rate of 80.6\% for the CLUSTERIDS variant and 0\% for the B1 baseline on the runs performed to date. However, the available runs are imbalanced across variants (21 seeds for CLUSTERIDS versus 3 seeds for the B1 baseline), which prevents reliable inferential conclusions from being drawn at this time.

Accordingly, we avoid strong inferential claims in this manuscript and treat the pilot results as preliminary. For the full campaign we commit to the following statistical analysis plan, and we will update the manuscript when the full balanced dataset is available:
\begin{itemize}
  \item Run each experimental condition (all baselines and variants) with at least 20 independent seeds to obtain stable distributional estimates.
  \item Report mean, standard deviation, and 95\% confidence intervals for key metrics (DR, FPR, time-to-detect, energy overhead). Use bootstrap intervals when distributional assumptions are uncertain.
  \item Present distributional plots (boxplots/violin) and per-seed raw measurements as supplementary material.
  \item Use nonparametric tests (Mann--Whitney U / Kruskal--Wallis) when normality cannot be assumed; report corrected p-values for multiple comparisons and effect sizes (e.g., Cliff's delta or Cohen's d as appropriate).
  \item Where appropriate, provide ROC/PR curves and confusion-matrix aggregates for detector-level behavior.
\end{itemize}

\input{tables/table09_statistics}

\subsection{Sensitivity Analysis}
A sensitivity sweep varying $\tau_{\mathrm{low}}$, $\tau_{\mathrm{CH}}$, $\tau_{\mathrm{inter}}$, $w_e$--$w_d$, and $\lambda_1$--$\lambda_4$ is left for future work, as the pilot campaign focused on demonstrating feasibility and validating the instrumentation and parsing pipeline.

\subsection{Scalability Across Network Sizes}
Fig.~\ref{fig:alert-overhead} is designed to span 50--500 nodes. The pilot campaign covered the 50-node grid; larger-scale evaluation (100--500 nodes) is left for the full campaign and will be reported in an updated manuscript and the reproducibility archive.

tables/table02_detection.tex

TeX
% Table II — Detection performance (pilot campaign results).
% NOTE (pre-submission): pilot data are imbalanced across variants (CLUSTERIDS: 21 seeds; B1: 3 seeds). The comparisons are therefore preliminary; see Section~\ref{sec:results} for the statistical validation plan and planned full-campaign analysis.
\begin{table}[!t]
  \caption{Detection Performance — 50-node Grid, \textsc{Balanced} Mode (21 seeds for CLUSTERIDS, 3 for B1).}
  \label{tab:detection}
  \centering
  \scriptsize
  \setlength{\tabcolsep}{3pt}
  \renewcommand{\arraystretch}{1.1}
  \begin{tabular}{@{}lcc@{}}
    \toprule
    \textbf{Scenario} & \textbf{B1} & \textbf{RPL-ClusterIDS} \\
    \midrule
    rank     & 0.0\% & 95.1\% \\
    sel\_fwd & 0.0\% & 95.1\% \\
    wormhole & 0.0\% & 95.1\% \\
    dao\_flood & 0.0\% & 95.1\% \\
    mixed    & 0.0\% & 80.6\% \\
    \midrule
    FPR      & 0.50\% & 0.50\% \\
    \bottomrule
  \end{tabular}
  \vspace{2pt}
  \raggedright\scriptsize
  \dag{} Campaign-level detection rate: at least one confirmed alert per attack period.
  B2 (flat distributed) and B3 (centralized with CH verification) baselines are planned for the full campaign but not evaluated in this pilot study.
  Both B1 and RPL-ClusterIDS report 0.50\% FPR because the centralized rules share the same first-stage detection thresholds; the distinguishing advantage of RPL-ClusterIDS lies in its hierarchical confirmation and aggregation.
\end{table}

README.md

md
# RPL-ClusterIDS — Reproducible Scientific Project (Computer Networks — Elsevier)

**Target journal:** Computer Networks (Elsevier)  
**Phase:** 2.1 (pilot campaign data available, full campaign pending, transparency fixes applied)  
**Tracker:** [`anomalies/opencode.md`](anomalies/opencode.md)

## Repository Structure

IDS_IOT/ ├── main.tex # Manuscript (Elsevier elsarticle format) ├── main-ieee.tex # IEEE variant (auxiliary) ├── sections/ # 11 LaTeX sections ├── tables/ # Tables II–IX ├── Figures/ # 11 figures (TikZ/PGFPlots) ├── bib/references.bib # References (~34 entries) ├── status-macros.tex # Status macros ├── MASTER_TRACKER.md # Project tracking ├── SIMULATION_CAMPAIGN_READY/ # Campaign scripts (Ubuntu) ├── data/ │ ├── estimated/ # Reference CSV schemas │ ├── real/raw/ # Raw Cooja logs (pilot) │ └── real/parsed/ # Parsed aggregated CSVs ├── scripts/ │ ├── python/generate_figures.py │ └── statistics/compute_statistics.py ├── code_source_RPL_ClusterIDS/ # Contiki-NG firmware └── anomalies/ # AI audit reports (6 tools)

Code

## Compilation (Elsevier — submission target)

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
Full Campaign (Ubuntu with Contiki-NG + Cooja)
bash
cd SIMULATION_CAMPAIGN_READY
./run_campaign.sh --full
python3 ../scripts/statistics/compute_statistics.py --input ../data/real/parsed
python3 ../scripts/python/generate_figures.py --csv ../data/real/parsed/agg --out ../Figures/
Known issues and TODO (pre-submission)
Statistical imbalance: pilot runs are currently unbalanced across variants (CLUSTERIDS: 21 seeds; B1 baseline: 3 seeds). The paper does not make strong inferential claims on these pilot numbers; we plan to rerun baselines with balanced seeds (>=20) before submission. See sections/results.tex for the planned statistical analysis.
Figures placeholders: several figure files are currently placeholders in Figures/ (marked in Figures/README.md). Replace placeholders with plots generated from the aggregated outputs before final submission.
Pin external versions: add Contiki‑NG commit hash and Cooja version to SIMULATION_CAMPAIGN_READY/README.md and requirements.txt (requirements already exists; please pin package versions).
Archival: archive aggregated datasets and analysis scripts (e.g., Zenodo) and add DOI to README and manuscript.
LICENSE: add an explicit LICENSE file (MIT suggested). This repository now includes a LICENSE file on branch fix/statistics-reproducibility.
Status Legend
Mark	Meaning
REAL_RESULT	Pilot campaign measurement (pipeline-generated; see anomalies/opencode.md)
READY_FOR_SIMULATION	Ready to run on Ubuntu
ESTIMATED	Placeholder (no Cooja data yet)
Note
This repository contains the IDS project only. The AER-MQoS routing project is maintained separately.

Code
LICENSE

LICENSE
MIT License

Copyright (c) 2026 Madani Belacel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

CITATION.cff

cff
cff-version: 1.2.0
message: "If you use this software, please cite it using the metadata below."
title: "RPL-ClusterIDS"
version: "0.1.0"
date-released: 2026-06-30
authors:
  - family-names: "Belacel"
    given-names: "Madani"
    orcid: ""
repository-code: "https://github.com/madani-belacel/IDS-IOT"

docker/Dockerfile

docker/Dockerfile
# Dockerfile for analysis steps (parsing, figure generation, LaTeX compilation)
# Note: running Cooja/Contiki simulations inside Docker is non-trivial due to GUI/Java/Cooja constraints.
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 python3-pip python3-venv \
    texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended \
    texlive-pictures texlive-binaries \
    git curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install Python requirements (use requirements.txt from repo)
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /work

# Usage notes:
# - Mount the repository into /work and run analysis commands (parsing, figure generation, LaTeX build).
# - For Contiki-NG + Cooja simulation runs, perform them on a host with Contiki and Java installed (or create a separate image).

SIMULATION_CAMPAIGN_READY/README.md

md
<!-- SIMULATION_CAMPAIGN_READY README additions -->

> NOTE (reproducibility): Before running the full campaign, please pin your Contiki‑NG source tree to a specific commit or release. Add the commit hash in this README and set the `CONTIKI_NG` environment variable accordingly.

Current quick start commands assume Contiki‑NG is available and configured. For exact reproducibility, record:
- Contiki‑NG commit hash / tag
- Cooja version and Java runtime (e.g., OpenJDK 17)

Example (recommended):

```bash
export CONTIKI_NG=/path/to/contiki-ng@<commit-hash>
# then proceed with the existing quick start
Code
Please confirm you want Copilot to push 7 files to branch fix/statistics-reproducibility in madani-belacel/IDS-IOT.

 ousanesisl-hub accepted the action
