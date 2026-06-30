Voici maintenant la revue détaillée en texte, section par section, telle qu'un reviewer de Computer Networks la rédigerait.

Revue complète — RPL-ClusterIDS
Reviewer simulé : Computer Networks (Elsevier) · Juin 2026

1. Points forts du manuscrit et du projet
Architecture et firmware. La conception modulaire de l'IDS en Contiki-NG est le vrai point fort du projet. La séparation entre clus_form, ch_elect, ids_member, ids_ch, et ctx_policy est propre et justifie l'appellation "hierarchical distributed". Le schéma de politique contextuelle (weights wew_e
we​–wdw_d
wd​, classes C0–C3, trois modes Full/Balanced/Eco) est original et différencie le travail de simples reproductions de LEACH-IDS.
Processus de qualité interne. Rares sont les projets de soumission comportant une TRACEABILITY_MATRIX, une FIGURE_DEPENDENCIES, une TABLE_DEPENDENCIES et un REFERENCES_AUDIT aussi complets. C'est une pratique de rigueur scientifique exemplaire qui faciliterait le travail d'un reviewer s'il y avait des données réelles derrière.
Honnêteté intellectuelle. Le PROJECT_HEALTH_REPORT qui s'auto-note 4.9/10 est inhabituellement honnête. L'auteur sait exactement où en est le projet — ce qui est une qualité, à condition de ne pas soumettre avant d'avoir comblé les lacunes identifiées.
Protocole statistique. Le design statistique prévu (IC 95%, t-test de Student, Mann-Whitney U, 20 seeds par configuration, 8 comparaisons) est exactement ce qu'attend Computer Networks pour une évaluation de protocole réseau. Une fois exécuté sur de vraies données, ce sera convaincant.

2. Anomalies et problèmes critiques
Problème P0 fondamental — aucune donnée complète et fiable.
Le tracker indique que la campagne pilote a été exécutée (21 seeds CLUSTERIDS, 3 seeds ablation, 50 nœuds seulement), mais les baselines B1/B2/B3 présentent un taux de détection de 0%, signalé comme "issue needs investigation" et non résolu. C'est un signal d'alarme majeur : si les baselines ne détectent rien, soit l'injecteur d'attaques (ids_attack) n'injecte pas effectivement les attaques dans la simulation Cooja, soit le parser de logs (parse_cooja_ids_metrics.py) ne récupère pas les lignes METRIC des baselines, soit le code des baselines est bogué. Dans les trois cas, toutes les Tables II, III, VIII, IX publiées comme "REAL_RESULT" sont construites sur une comparaison avec des baselines à 0% — ce qui rend n'importe quel avantage de CLUSTERIDS trivialement vrai et scientifiquement sans valeur.
Incohérence critique — double cible journal.
Le MASTER_TRACKER déclare "Target journal: IEEE Internet of Things Journal", la checklist mentionne "Computer Networks Audit", et les deux PDF (main.pdf en elsarticle, main-ieee.pdf en IEEEtran) coexistent. Ce n'est pas une question de forme : le scope de Computer Networks (Elsevier) est centré sur les protocoles réseau et les architectures de communication, tandis que l'IEEE IoT Journal accepte davantage de contributions systèmes IoT avec composante ML. Les contributions du manuscrit — IDS + RPL + clustering + ML — correspondent mieux à l'IEEE IoT Journal ou à des conférences comme IEEE INFOCOM. Si la cible est Computer Networks, le positionnement dans le contexte RPL/6LoWPAN doit être nettement renforcé dans la Related Work.
ML non entraîné, Tables VI et VII vides de substance.
Le §V et le §VII décrivent un pipeline ML (gradient-boosted trees à ≤8 arbres, profondeur 3, LR 0.1, split 70/15/15, 12 features) mais le modèle n'est pas entraîné, le dataset Cooja n'est pas collecté, et les métriques de test (accuracy, F1, RAM footprint) n'existent pas. La Table VII "ML hyperparameters" affiche des valeurs de design qui ne peuvent pas être présentées comme résultats d'entraînement. Aucun reviewer ML d'IEEE IoT Journal n'acceptera cela sans ablation expérimentale du modèle.
Références — problèmes concrets.
L'entrée raza2018cluster avec des pages "12345–12358" est manifestement un placeholder. La clé anton2014rpl avec year=2024 créera une confusion de citation. Trois entrées sont marquées "Verify before submission" et ne l'ont pas été. Plus grave, ~19 entrées de la bibliographie ne sont pas citées dans le manuscrit — un fichier bib avec 50% d'orphelins est le signe d'une accumulation automatique non contrôlée. Computer Networks limite souvent à 50 références et les vérifie à la production.
Seuils non justifiés.
Les valeurs τlow=0.25\tau_{low}=0.25
τlow​=0.25, τCH=0.40\tau_{CH}=0.40
τCH​=0.40, τlas=0.70\tau_{las}=0.70
τlas​=0.70, τinter=0.80\tau_{inter}=0.80
τinter​=0.80 sont présentées comme des paramètres de conception sans analyse de sensibilité. La question "pourquoi 0.40 et pas 0.35 ou 0.50 pour τCH\tau_{CH}
τCH​?" est systématiquement posée par les reviewers de protocoles. Le sweeping ±20%\pm20\%
±20% est prévu mais non exécuté.

3. Suggestions d'amélioration concrètes
Priorité absolue — déboguer les baselines avant tout. Insérer des printf ou logs DEBUG dans le code des variantes B1, B2, B3 pour confirmer que les attaques sont bien reçues et traitées. Vérifier que le parser Python extrait bien les lignes METRIC des logs Cooja pour ces variantes, pas seulement pour CLUSTERIDS.
Exécuter la campagne complète. La campagne 50–500 nœuds, 5 attaques, 4 variantes, 20 seeds est la seule voie vers une soumission valide. Le document UBUNTU_EXECUTION_PLAN.md est prêt — il faut exécuter. Les résultats pilote partiels ne suffisent pas.
Reformuler les figures 4–11 avec error bars. Une fois les CSV réels disponibles, toutes les figures bar/line chart doivent afficher les intervalles de confiance à 95%. Des barplots sans error bars pour une comparaison de protocoles seront refusés.
Ajouter la sensibilité aux thresholds. Un heatmap DR/FPR en fonction de τCH\tau_{CH}
τCH​ et τlas\tau_{las}
τlas​ (3×3 ou 5×5 valeurs) transformerait les seuils de "paramètres arbitraires" en "paramètres robustes" — et ne coûte qu'un paramétrage supplémentaire de la campagne.
Nettoyer la bibliographie maintenant. Supprimer les 15 orphelins, corriger les 5 entrées problématiques, valider les DOI manquants sur doi.org — ce travail peut être fait indépendamment de la campagne.
Archiver sur Zenodo. Un DOI Zenodo pour le code firmware, le fichier de campagne, et les données réelles (une fois collectées) est exigé par Computer Networks dans sa politique Open Science.

4. Verdict global
Ce projet est publiable après corrections majeures — probablement dans IEEE Internet of Things Journal plutôt que Computer Networks en raison du scope — mais uniquement après :

la résolution du bug DR=0% sur les baselines,
l'exécution complète de la campagne Cooja,
l'entraînement du modèle ML et la collecte du dataset,
la vérification complète des références.

Le potentiel de la contribution (IDS hiérarchique, contexte-adaptatif, énergie-conscient, pour RPL/IoT, avec Contiki-NG) est réel et le positionnement est pertinent. La maturité du design et du protocole expérimental planifié est au-dessus de la moyenne. Mais entre un plan expérimental et des résultats, il y a une frontière que ne peut pas franchir une soumission sérieuse. La durée estimée pour atteindre le niveau de soumission est de 4 à 8 semaines de travail intensif sur Ubuntu avec Cooja, en supposant que le bug baselines soit résolu rapidement.
Score global actuel : 4.9/10. Score cible après Phase 2 complète : 8/10 — acceptable pour IEEE IoT Journal.
