# Revue éditoriale — IDS-IOT / RPL-ClusterIDS (pour Computer Networks)

Note méthodologique : j'ai analysé la structure du dépôt GitHub et les fichiers de suivi internes (`MASTER_TRACKER.md`, `REFERENCES_AUDIT.md`, `checklist.md`, README) en plus de l'organisation du manuscrit. Ces fichiers de pilotage interne, normalement non destinés à la publication, révèlent l'état réel du projet et constituent à eux seuls une source d'information cruciale pour cette revue — bien plus fiable que le texte du PDF seul.

## 1. Points forts

- **Architecture scientifique claire** : la séparation clusterisation RPL (`clus_form`, `ch_elect`) / détection d'intrusion contextuelle (`ids_member`, `ids_ch`, `ctx_policy`) / injection d'attaques (`ids_attack`) / journalisation (`ids_campaign_log`) montre une conception logicielle modulaire et bien pensée, assez rare dans ce type de soumission.
- **Effort de reproductibilité réel** : présence d'un dossier `SIMULATION_CAMPAIGN_READY/`, d'un script `run_campaign.sh`, d'un pipeline de statistiques (`compute_statistics.py` avec bootstrap CI, t-test, Mann-Whitney), et d'une matrice de traçabilité (`TRACEABILITY_MATRIX.md`) liant figures/tables aux données sources. C'est exactement le type de rigueur que Computer Networks valorise.
- **Discipline de gestion de projet inhabituelle** : le système de statuts `ESTIMATED` / `READY_FOR_SIMULATION` / `REAL_RESULT` montre une volonté affichée d'éviter la fabrication de résultats — c'est un signe d'intégrité scientifique, pas un défaut en soi.
- **Bibliographie globalement pertinente** : plusieurs références fortes et bien choisies (RFC 6550/7416, Raza et al. 2017 *IEEE IoT J.*, Mayzaud 2016 *IEEE ComST*, Sfar 2018, Hindy 2020), avec un audit interne (`REFERENCES_AUDIT.md`) qui identifie lui-même les entrées à corriger.
- **Double format (Elsevier `elsarticle` + IEEE)** prêt à compiler, ce qui montre une maîtrise correcte de LaTeX académique.

## 2. Anomalies et problèmes critiques (par priorité)

### 🔴 P0 — Bloquants pour toute soumission

1. **Le manuscrit ne repose pas sur une campagne expérimentale complète.** D'après `MASTER_TRACKER.md` : seuls 21 seeds ont été exécutés pour CLUSTERIDS et 3 pour l'ablation, alors que la campagne complète prévue (nœuds = 100/200/300/500) est **entièrement bloquée** (`BLOCKED`). Le modèle ML annoncé dans le pipeline est lui-même marqué `BLOCKED` ("trained model artifact"). C'est une violation directe des standards de Computer Networks, qui exige des résultats statistiquement robustes (multiples seeds, plusieurs échelles de réseau) avant publication.
2. **Bug non résolu et non documenté dans le texte : les trois baselines (B1, B2, B3) affichent un Detection Rate de 0 %.** C'est noté comme "issue needs investigation" dans le tracker. Si ce 0% apparaît dans les Tables II/III/IX du PDF sans explication critique, c'est soit (a) un bug d'instrumentation grave invalidant toute comparaison, soit (b) une présentation trompeuse d'un résultat artificiellement favorable au système proposé. Dans les deux cas, c'est rédhibitoire pour un reviewer Computer Networks — un baseline à 0% de détection est scientifiquement suspect et doit être expliqué/corrigé avant toute soumission.
3. **Mélange entre données réelles et données simulées/synthétiques pas clairement isolé pour le lecteur.** Le tracker indique que les tests statistiques (95% CI, t-test) ont d'abord été validés sur des CSV synthétiques (`data/estimated/aggregated/`) avant d'être (partiellement) rejoués sur des données réelles. Si le manuscrit ne précise pas explicitement, table par table, quelles valeurs proviennent de la campagne pilote réelle (21 seeds) et lesquelles restent des placeholders, c'est un problème d'intégrité scientifique majeur, potentiellement assimilable à une présentation trompeuse de résultats.
4. **Échelle expérimentale insuffisante pour les conclusions affichées.** 21 seeds à 50 nœuds seulement (la configuration "pilote") ne permet pas de soutenir des affirmations générales de scalabilité ou de robustesse pour un environnement IoT à grande échelle — ce qui est pourtant l'argument central de ce type d'article. Computer Networks demandera presque certainement des expériences à 100+ nœuds avant d'envisager l'acceptation.
5. **Statut "DONE" trompeur dans certaines sections du tracker.** Par exemple §X Conclusion est marquée "IN_PROGRESS (no definitive metrics)" alors que d'autres items disent "DONE". Cela suggère que le manuscrit pourrait actuellement contenir des conclusions formulées avant que les données définitives ne soient disponibles — à vérifier ligne par ligne dans le PDF final.

### 🟠 P1 — Majeurs, à corriger avant soumission

6. **Bibliographie non vérifiée : ~5 références signalées "uncertain metadata" par votre propre audit**, dont `raza2018cluster` dont les pages (12345–12358) ont manifestement l'air d'un placeholder generated automatiquement plutôt que de vraies pages d'article — un reviewer Elsevier détectera ceci immédiatement et le percevra comme un signal d'alarme sur la rigueur générale du travail.
7. **~19 références orphelines (non citées) dans le `.bib`**, soit près de 40% du fichier bibliographique. Cela suggère soit un nettoyage incomplet, soit une bibliographie gonflée artificiellement (« reference padding »), une pratique que les éditeurs scrutent désormais activement.
8. **Incohérence de journal cible.** Le README affiche "IEEE Internet of Things Journal" comme cible principale, alors que la demande porte sur Computer Networks. Il faut vérifier que la version `main.tex` (Elsevier) n'est pas simplement une reconversion de forme du manuscrit IEEE sans adaptation de fond (scope, longueur des sections related-work, style argumentatif) — les deux journaux ont des attentes différentes en termes de profondeur de discussion et de positionnement vis-à-vis de l'état de l'art.
9. **DOI manquants pour la quasi-totalité des références.** Seules 2 entrées sur ~34 citées ont un DOI confirmé dans l'audit interne. C'est très en-dessous des standards attendus par Elsevier en 2026.
10. **Métadonnées clé erronées non corrigées** : `anton2014rpl` a une année de clé (2014) incohérente avec le champ année réel (2024) — ce genre d'erreur, si elle persiste dans le PDF final, sera immédiatement relevée en review.

### 🟡 P2 — Mineurs mais à nettoyer

11. Présence de très nombreux fichiers de gestion de projet (`MASTER_TRACKER.md`, `PHASE2_COMMAND_SUMMARY.md`, `PROJECT_HEALTH_REPORT.md`, `UBUNTU_EXECUTION_PLAN.md`, `WINDOWS_SETUP_GUIDE.md`, `AUDIT_PROMPT.md`, `BUILD_NOTES.txt`...) à la racine du dépôt public. Ce n'est pas un problème de qualité scientifique, mais cela nuit énormément à la présentation professionnelle du dépôt pour la reproductibilité — un reviewer ou un lecteur qui clone le repo verra immédiatement que le projet est en chantier actif, avec des incertitudes ouvertes documentées noir sur blanc ("0% DR issue needs investigation", "trained model artifact BLOCKED"). Ces fichiers ne doivent pas forcément être supprimés, mais clairement déplacés hors du dépôt public de soumission (ou dans un sous-dossier `dev-notes/` exclu du package de reproductibilité officiel), car leur présence expose publiquement les limites non résolues du travail avant même la lecture du papier.
12. Fichier `test-elsarticle.pdf` à la racine — fichier de test, à retirer du dépôt final destiné aux reviewers.
13. Le `requirements.txt`, `docker-compose.yml`, `Dockerfile` sont de bons signes de reproductibilité — mais il faut vérifier qu'ils sont réellement testés (build propre depuis zéro) et pas seulement présents.

## 3. Suggestions concrètes pour atteindre le niveau Computer Networks

1. **Compléter la campagne expérimentale avant toute soumission.** Au minimum : exécuter les configurations à 100 et 200 nœuds (les 300/500 peuvent être discutées comme "future work" si les ressources manquent), avec un nombre de seeds homogène entre CLUSTERIDS et les baselines B1/B2/B3 (actuellement asymétrique : 21 vs 3).
2. **Résoudre et documenter explicitement le bug DR=0% des baselines.** Soit c'est un artefact d'instrumentation à corriger, soit c'est un résultat réel qu'il faut justifier théoriquement dans le texte (pourquoi ces baselines échouent totalement dans ce scénario précis) — un 0% net sans explication est scientifiquement incrédible et sera flaggé en review.
3. **Ajouter un tableau de provenance des données en annexe** (Real / Estimated / Pilot) directement visible dans le manuscrit, pas seulement dans les fichiers internes — transparence totale sur ce qui est mesuré vs. modélisé.
4. **Nettoyer la bibliographie** selon votre propre audit : retirer les ~19 orphelines, corriger ou retirer `raza2018cluster`, vérifier les 5 entrées signalées, ajouter systématiquement les DOI (vérifiables via Crossref/doi.org).
5. **Renforcer le Related Work** avec 2-3 références 2024-2026 supplémentaires sur les IDS hiérarchiques/énergie-conscients pour IoT — le domaine évolue vite, et un comité Computer Networks attendra une couverture de l'état de l'art jusqu'à l'année de soumission.
6. **Clarifier la cible éditoriale.** Adapter réellement le contenu (pas juste le template LaTeX) entre la version Elsevier et IEEE : profondeur du related work, longueur, conventions de notation.
7. **Restructurer le dépôt pour la soumission publique** : séparer clairement `code/`, `data/`, `paper/`, et reléguer tous les fichiers de pilotage interne hors du package de reproductibilité visible aux reviewers.
8. **Faire relire l'anglais/français et la cohérence terminologique** (non vérifié ici en détail faute d'accès direct au texte intégral du PDF — à faire faire par un relecteur natif avant soumission).

## 4. Checklist finale avant soumission

- [ ] Campagne de simulation complète exécutée (≥100-200 nœuds, seeds symétriques entre toutes les variantes)
- [ ] Bug DR=0% des baselines résolu ou justifié explicitement dans le texte
- [ ] Toutes les valeurs `ESTIMATED`/placeholder éliminées des tables et figures finales (Tables V, VI, VII actuellement encore `READY_FOR_SIMULATION`, pas `REAL_RESULT`)
- [ ] Modèle ML effectivement entraîné et ses hyperparamètres réels rapportés (actuellement `BLOCKED`)
- [ ] Bibliographie nettoyée : orphelines retirées, métadonnées vérifiées, DOI ajoutés
- [ ] Cohérence entre version Elsevier et IEEE vérifiée (pas un simple reformatage)
- [ ] Dépôt public réorganisé (fichiers de pilotage interne déplacés hors du package soumis)
- [ ] Relecture linguistique complète
- [ ] Vérification anti-plagiat formelle (iThenticate/Turnitin) — non réalisable depuis cette analyse, à faire en interne

## 5. Verdict global

**Non publiable en l'état.** Ce n'est pas un problème de forme ou de rédaction (la structure et l'ambition scientifique sont solides), mais un problème de **fond expérimental** : les propres fichiers de suivi du projet indiquent que la campagne de simulation est partielle, que le modèle ML n'est pas entraîné, qu'un bug critique invalidant potentiellement les comparaisons avec les baselines n'est pas résolu, et que plusieurs tables contiennent encore des données provisoires.

À ce stade, le projet ressemble davantage à un **travail en cours (Phase 2 sur 2)** prématurément packagé en manuscrit qu'à un article prêt pour relecture par les pairs. C'est un point positif inhabituel : la traçabilité interne du projet est si rigoureuse qu'elle s'auto-dénonce — ce qui suggère une équipe honnête et consciencieuse, mais qui a soumis (ou s'apprête à soumettre) trop tôt.

**Recommandation** : Major Revision avant resoumission, voire retrait temporaire de la soumission tant que la campagne complète n'est pas terminée. Une fois la campagne expérimentale achevée, le bug des baselines résolu, et la bibliographie nettoyée selon votre propre audit, ce travail a un potentiel réel d'acceptation dans Computer Networks — l'architecture technique (clustering + IDS contextuel pour RPL) est une contribution pertinente et le scope correspond bien au journal.
