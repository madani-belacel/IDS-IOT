# Checklist des anomalies locales

## État général
- [x] Anomalies critiques de sécurité et de logique de code corrigées localement
- [x] Anomalies de checklist / placeholders nettoyées
- [x] Script de statistiques adapté aux CSV réels du pipeline
- [x] Bibliographie nettoyée sur la seule entrée réellement orpheline
- [x] Cohérence du manuscrit renforcée sur notation et formulations
- [ ] Campagne expérimentale complète et équilibrée encore à exécuter si une validation finale est requise
- [ ] Vérification finale des points d’audit restants si une revue plus stricte est demandée

## Correctifs appliqués
- [x] Suppression du token GitHub exposé dans [internal/push-project.sh](../internal/push-project.sh)
- [x] Déduplication des définitions de configuration dans [code_source_RPL_ClusterIDS/project-conf.h](../code_source_RPL_ClusterIDS/project-conf.h) et [code_source_RPL_ClusterIDS/ids_conf.h](../code_source_RPL_ClusterIDS/ids_conf.h)
- [x] Alignement du script de statistiques avec les CSV réels présents dans [data/real/parsed](../data/real/parsed)
- [x] Remplacement du contenu placeholder dans [instruction.md](../instruction.md)
- [x] Création d’une checklist d’anomalies opérationnelle dans ce fichier

## À poursuivre si besoin
- [ ] Validation complète du B1 vs. autres baselines sur campagne réelle
- [ ] Nettoyage bibliographique plus fin (orphelines / références non citées)
- [ ] Exécution d’une campagne plus large avec seeds équilibrés si la soumission finale l’exige
- [ ] Revue finale des anomalies restantes listées dans les rapports internes
- [ ] Vérifier la cohérence entre les résultats annoncés dans le manuscrit et les données réellement produites par le pipeline
- [ ] Clarifier et documenter le nombre exact de graines et le protocole statistique utilisé
- [ ] Séparer clairement les résultats “pilot / préliminaires” des claims plus forts de performance
- [ ] Vérifier les DOI et métadonnées des références utilisées dans la version finale
- [ ] Rendre la traçabilité de chaque figure/tableau vers ses CSV et scripts explicite et reproductible

## Revue Computer Networks (2026-06-30)
- [x] Revue scientifique complète réalisée sur le manuscrit principal et la version IEEE
- [x] Points forts identifiés : originalité du concept, structure claire, paquet de reproductibilité solide
- [x] Problèmes critiques identifiés : validation expérimentale, alignement des résultats et pipeline, qualité bibliographique, niveau de prudence scientifique
- [x] Rapport de revue enregistré dans [anomalies/VSCODE.md](VSCODE.md)
- [ ] Corriger les points critiques ci-dessus avant toute soumission à Computer Networks
