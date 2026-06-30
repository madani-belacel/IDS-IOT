1. Points forts du manuscrit et du projetLe projet démontre une excellente organisation et un fort souci de reproductibilité, ce qui est rare et très apprécié pour Computer Networks. Le dépôt GitHub est bien structuré avec des dossiers clairs (code_source_RPL_ClusterIDS, SIMULATION_CAMPAIGN_READY, scripts, data/, sections/, tables/, Figures/), des trackers détaillés (MASTER_TRACKER.md, checklists), des guides d'exécution (Ubuntu/Windows/Docker), et un pipeline de parsing/analyse (Python + statistiques avec scipy). 

github.com +1

Contributions scientifiques potentielles : Approche hiérarchique clustering-centric pour IDS dans RPL (membres ultra-légers + CH avec vérification à deux étapes + politique contextuelle à 3 modes : Full/Balanced/Eco). Cela adresse bien les contraintes énergie/topologie/priorité trafic dans les réseaux LLN.
Intégration native Contiki-NG/Cooja avec logging structuré (METRIC,...), variants (B1-B3 + ablations), et campagne reproductible.
Focus sur l'adaptativité contextuelle et l'énergie, qui complète utilement les approches rule-based, federated ou GNN pures. 

raw.githubusercontent.com

Rédaction : La structure est classique et logique (Introduction → Related Work → Threat Model → Architecture → Impl. → Setup → Results → Discussion → Limitations → Reproducibility). Le langage est clair, technique, avec bons liens entre sections. Les macros de statut (\EstimatedCell, etc.) et les dépendances (FIGURE_DEPENDENCIES.md, TABLE_DEPENDENCIES.md) montrent une gestion professionnelle du manuscrit. 

raw.githubusercontent.com

Références : ~34-45 entrées, majoritairement récentes (2023-2026), avec DOIs valides pour la plupart (RFCs, Elsevier/IEEE). Bon mélange surveys, RPL-specific, et travaux récents (FL, TinyML, GNN). Pas de plagiat évident détecté. 

raw.githubusercontent.com

Figures/Tables : TikZ/PGFPlots pour reproductibilité vectorielle ; captions détaillées ; ablations et analyses statistiques (t-tests, CI) bienvenues. 

raw.githubusercontent.com

2. Anomalies et problèmes critiques (classés par priorité)Critiques majeures (P0 - bloquantes pour acceptation) :Résultats majoritairement pilot/estimés : Le manuscrit présente des métriques concrètes (DR 80.6%, FPR 0.50%, overhead 5-7%) issues d'une "pilot campaign" très limitée (3 seeds, 50 nodes). De nombreuses figures/tables restent en mode placeholder ou s'appuient sur data/estimated/. Le tracker indique clairement que la full campaign (jusqu'à 500 nodes) est partielle/blocked, avec des anomalies (B1/B2/B3 à 0% DR). Les claims dans l'abstract/highlights ne sont pas encore solidement étayés par des données réelles à grande échelle. 

github.com +1

Manque de reproductibilité immédiate : Bien que le pipeline existe, data/real/ n'est que partiellement peuplé (pilot seulement). Un reviewer ne peut pas facilement re-exécuter la full campagne sans setup Contiki-NG + temps CPU important. Les scripts Python sont présents mais les CSVs réels limités.
Échelle et généralisation : 50 nodes est trop petit pour des claims sur "large-scale IoT". Scalability mentionnée comme "design-target projections" ou future work.

Problèmes importants (P1) :Originalité : L'idée de clustering pour IDS RPL n'est pas totalement nouvelle (mentions dans related work), mais l'adaptativité énergie/contexte + hiérarchie légère est un bon delta. Il faut mieux positionner vs. travaux 2024-2026 (FL-DSFA, hybrid DL, GNN trust). Le tableau de comparaison est utile mais doit être étendu/nuancé.
Évaluation ML incomplète : Mention de gradient-boosted trees au CH, mais hyperparams/dataset splits (Tables VI-VII) en READY_FOR_SIMULATION. Les résultats semblent surtout rule/threshold-based.
Incohérences mineures : Quelques placeholders résiduels possibles dans PDF ; claims abstraits vs. pilot data ; discussion des limitations (B1/B2/B3 0% DR) doit être plus franche.
Format Elsevier : Le main.tex utilise elsarticle correctement, mais vérifier longueur, highlights, et guidelines précises de Computer Networks (scope networking/comms, pas pure simulation security). 

sciencedirect.com

Problèmes mineurs (P2) :Code C : Bien modulaire, mais besoin d'audit plus profond (sécurité des implémentations d'attaques, gestion mémoire sur motes réels vs. Cooja).
Quelques refs très récentes/futures (2026) — valides pour early access mais vérifier disponibilité.
Figures : Placeholders TikZ ok pour archi, mais résultats doivent être réels et lisibles en deux colonnes.

3. Suggestions d’amélioration concrètesExécuter la Phase 2 complète : Sur Ubuntu, lancer la full campaign (SIMULATION_CAMPAIGN_READY), populer data/real/, re-générer tables/figures/stats. Remplacer tous les estimated par REAL_RESULT. Viser au moins 100-200 nodes + plus de seeds (≥10-20) pour stats robustes.
Renforcer l'évaluation : Ajouter comparaison vs. baselines plus fortes (e.g., Raza 2017 implémentée, ou un TinyML baseline). Inclure energy consumption réelle (Energest + profiling), overhead réseau détaillé, et sensibilité aux params. Ajouter ROC/AUC si ML utilisé.
Améliorer Related Work & Positioning : Étendre Table I avec colonnes quantitatives (DR/FPR/overhead sur benchmarks communs comme ROUT-4 ou Dib2024). Souligner clairement les gaps comblés (energy/context-aware clustering comme primary principle).
Discussion & Limitations : Section dédiée plus profonde sur trade-offs modes, impact sur RPL stability, falsifiabilité, généralisation à motes réels (Sky/Z1 vs. Cooja), et comparaison coût/bénéfice vs. approches centralisées.
Reproducibility : Fournir un Docker complet one-click + Zenodo DOI pour dataset complet + scripts avec seed fixing. Ajouter unit tests et validation des parsers.
Rédaction : Clarifier abstract (baser claims sur données finales). Ajouter équations pour LAS, fitness CH, politique contextuelle. Vérifier uniformité (anglais académique fluide déjà bon). Considérer plus de visualisations (e.g., heatmaps temporelles).
Scope journal : Computer Networks valorise contributions networking/architecturales pratiques. Mettre l'accent sur l'intégration RPL, overhead control-plane, et scalabilité distribuée plutôt que pure ML. 

sciencedirect.com

4. Checklist finale : ce qui doit absolument être corrigé avant soumissionFull campaign exécutée + toutes tables/figures mises à jour avec REAL data (supprimer estimated).
Abstract/highlights reflètent exactement les résultats finaux (pas pilot).
≥10 seeds + analyses statistiques robustes (CI, tests multiples, power analysis si possible).
Comparaisons baselines étendues + ablation complète documentée.
Dataset complet + pipeline one-command reproductible partagé (Zenodo/GitHub release).
Vérification DOI/refs + format elsarticle strict (pas de warnings LaTeX).
Section Limitations honnête + future work clair (motes réels, ML full, plus grande échelle).
Relecture native speaker + check plagiat (iThenticate-like).
PDF compilé propre (main.pdf pour Elsevier).

5. Verdict globalLe projet a un potentiel solide pour Computer Networks après corrections majeures : bonne idée architecturale, exécution reproductible, et pertinence pour IoT/RPL security (dans le scope du journal). Actuellement : Major Revision (ou Reject & Resubmit) en l'état, principalement à cause des résultats pilot/estimés qui ne supportent pas encore les claims. Avec la Phase 2 complétée, stats solides, et positionnement affûté, il deviendrait publiable après 1-2 rounds de révision (niveau acceptable pour CN, qui attend des contributions pratiques/novatrices avec éval rigoureuse). C'est un excellent squelette reproductible — finalisez les données réelles et cela passera bien. Le dépôt montre déjà un niveau de maturité et d'honnêteté scientifique appréciable. Bon travail global, continuez !


