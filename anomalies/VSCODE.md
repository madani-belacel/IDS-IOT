# Revue critique de RPL-ClusterIDS pour Computer Networks

Date de revue : 2026-06-30
Domaine : manuscrits [main.pdf](../main.pdf) et [main-ieee.pdf](../main-ieee.pdf), code source, LaTeX, scripts, figures, tables, données et documentation.

## Verdict synthétique

Le projet est intéressant, techniquement cohérent et potentiellement valorisable, mais il n’est pas encore dans un état suffisamment robuste pour une soumission de niveau Computer Networks sans corrections majeures. La contribution est crédible comme étude de faisabilité et comme paquet de reproductibilité, mais les résultats centraux ne sont pas encore assez solidement validés pour supporter des claims quantitatifs forts sans prudence.

Le manuscrit a une vraie valeur scientifique potentielle, notamment grâce à l’angle original “clustering + détection distribuée + adaptation énergétique” pour RPL. En revanche, plusieurs points doivent être corrigés avant toute soumission sérieuse : cohérence expérimentale, validité statistique, reproductibilité et qualité des références.

---

## 1. Points forts du manuscrit et du projet

### 1.1 Intérêt scientifique réel
- Le sujet est pertinent et bien positionné dans la littérature sur la sécurité RPL pour IoT.
- L’idée de fonder la détection sur un overlay de clusters énergétiquement adaptatifs est originale et sensible, surtout pour des réseaux contraints.
- La distinction entre détection locale, vérification par cluster head et politique contextuelle est conceptuellement solide.

### 1.2 Structure du manuscrit
- La structure est claire : introduction, état de l’art, modèle de menace, architecture, implémentation, plan expérimental, résultats, discussion, limites, conclusion, reproductibilité.
- Le manuscrit est globalement lisible et suit une logique de progression naturelle.
- Les sections de reproductibilité et de packaging artefact sont un vrai point fort pour une revue moderne.

### 1.3 Qualité du projet artefact
- Le dépôt contient un paquet de travail relativement complet : code Contiki-NG, variantes d’ablation, scripts de campagne, scripts de statistiques, figures TikZ/PGFPlots, structure de données et documentation.
- La séparation entre firmware, scripts, données et manuscrit est bonne.
- Les fichiers de provenance et de traçabilité sont un excellent point de départ pour une soumission reproductible.

### 1.4 Solidité technique de la base
- L’implémentation est modulaire et structurée autour de composants distincts : clustering, élection de cluster head, moteur de règles, politique contextuelle.
- Le modèle de menace et les scénarios d’attaque sont plausibles et bien choisis.
- La compilation LaTeX a été vérifiée localement sur [main.tex](../main.tex) et [main-ieee.tex](../main-ieee.tex), ce qui indique que le manuscrit est au moins structurellement stable.

---

## 2. Anomalies et problèmes critiques

### P0 — Problèmes de validation expérimentale et de cohérence des résultats

1. Incohérence majeure entre le texte du manuscrit et les artefacts de données disponibles.
   - Le manuscrit affirme un pilot campaign avec 21 graines pour la variante CLUSTERIDS et 3 graines pour l’ablation.
   - Les artefacts présents dans [data/real/parsed/campaign_manifest.tsv](../data/real/parsed/campaign_manifest.tsv) et [SIMULATION_CAMPAIGN_READY/seeds.txt](../SIMULATION_CAMPAIGN_READY/seeds.txt) ne soutiennent pas cette affirmation de façon transparente.
   - Les fichiers CSV réellement présents dans [data/real/parsed](../data/real/parsed) semblent correspondre à un jeu de données plus limité et/ou à une convention de colonnes différente de celle attendue par le pipeline statistique.

2. Les résultats quantitatives centraux ne sont pas encore reproduits de manière robuste à partir des données fournies.
   - La vérification locale du pipeline de statistiques a produit des valeurs de type NaN / comparaisons non exploitées pour les principaux contrastes, ce qui empêche de confirmer les claims annoncés sur la détection et les faux positifs.
   - Cela est particulièrement problématique pour les valeurs phares telles que le “80.6% detection rate” et le “0.50% FPR” mentionnés dans le manuscrit.

3. Le pipeline statistique n’est pas encore entièrement aligné sur les données réelles.
   - Les scripts [scripts/statistics/compute_statistics.py](../scripts/statistics/compute_statistics.py) et [scripts/python/generate_figures.py](../scripts/python/generate_figures.py) valident l’existence des fichiers, mais ne garantissent pas que les chiffres attribués aux figures et tableaux sont réellement cohérents avec la logique expérimentale décrite dans le texte.
   - En pratique, le travail est à un stade “pipeline prêt” plutôt qu’à un stade “résultats entièrement validés”.

### P0 — Risque de sur-claiming scientifique

4. Le manuscrit est parfois trop affirmatif pour un travail encore préliminaire.
   - Le papier est présenté comme une contribution robuste, mais le texte lui-même admet qu’il s’agit d’un “pilot campaign” et de “preliminary evidence”.
   - C’est honnête, mais l’article doit rester très strict sur le niveau de généralisation : il ne faut pas laisser entendre que les résultats sont définitifs ou transférables à grande échelle sans validation supplémentaire.

### P1 — Qualité des références et bibliographie

5. La bibliographie contient plusieurs éléments qui doivent être vérifiés avant soumission.
   - L’audit interne déjà présent dans [internal/REFERENCES_AUDIT.md](../internal/REFERENCES_AUDIT.md) pointe vers plusieurs entrées douteuses, incomplètes ou potentiellement non pertinentes.
   - Pour Computer Networks, la bibliographie doit être parfaitement soignée : DOI validés, métadonnées correctes, références récentes et directement liées à la contribution.
   - Il faut éviter les références génériques ou trop larges si elles n’apportent pas un apport argumentatif précis.

### P1 — Provenance et interprétation des données

6. Les figures et les tableaux sont bien structurés, mais la provenance des valeurs n’est pas encore complétement transparente.
   - Il faut documenter précisément quels logs, quelles graines, quels scénarios et quelles agrégations ont produit chaque figure et chaque tableau.
   - Sans cela, la reproductibilité reste partielle, même si le dépôt est bien organisé.

### P1 — Nature des métriques énergétiques et d’overhead

7. Les métriques d’énergie/CPU/RAM sont encore présentées comme des estimations ou des valeurs intermédiaires dans plusieurs sections.
   - Pour un journal de haut niveau, cela est acceptable si le papier est clairement présenté comme une étude de faisabilité, mais pas si les conclusions sont formulées comme des résultats définitifs.
   - Le meilleur chemin est soit de produire de vraies mesures Energest fiables, soit de limiter strictement la portée de l’analyse à la méthode et à la faisabilité.

### P2 — Faible niveau de polish rédactionnel

8. Le manuscrit pourrait être encore mieux affine pour un journal de haut niveau.
   - Certaines sections sont un peu longues ou répétitives.
   - Le positionnement comparatif vis-à-vis de l’état de l’art pourrait être plus tranchant.
   - La valeur ajoutée de l’approche devrait être formulée plus agressivement, avec un message de contribution plus net et plus compact.

---

## 3. Suggestions concrètes pour atteindre un niveau de soumission de qualité Computer Networks

### 3.1 Recentrer le papier sur une contribution robuste et vérifiable
- Refaire l’angle du papier autour d’un message principal clair : “un système de détection hiérarchique et adaptatif pour RPL, évalué sur une campagne pilote reproductible”.
- Éviter d’écrire comme si le travail était déjà pleinement validé à grande échelle.

### 3.2 Valider expérimentalement les chiffres principaux
- Exécuter une campagne cohérente avec un nombre de graines explicitement défini, documenté et reproduisible.
- Publier les résultats sous forme de tableaux et de figures générés à partir d’un unique pipeline stable.
- Ajouter des intervalles de confiance, écarts types, tests statistiques et tailles d’effets.

### 3.3 Clarifier la relation entre les données réelles et les figures
- Rendre chaque figure traceable vers un fichier CSV précis et une version de script précise.
- Ajouter un script de validation de schéma des données qui vérifie que les colonnes attendues sont bien présentes et cohérentes.

### 3.4 Renforcer la partie “related work”
- Réduire la liste de références trop large et trop dispersée.
- Mettre en évidence ce qui est unique dans RPL-ClusterIDS par rapport aux approches basées sur la confiance, l’apprentissage fédéré, TinyML et les GNN.

### 3.5 Améliorer la qualité des figures et de l’exposé des résultats
- Ajouter des barres d’incertitude là où elles sont pertinentes.
- Éviter les graphiques trop denses ou trop abstraits.
- S’assurer que chaque figure a un message clair et un seul.

### 3.6 Finaliser la bibliographie
- Supprimer ou remplacer les entrées problématiques.
- Vérifier les DOI et les métadonnées de chaque référence utilisée.
- Réduire la bibliographie à un ensemble de références vraiment fortes, présentées de façon compacte.

---

## 4. Checklist finale avant soumission

### À corriger absolument
- [ ] Vérifier la cohérence entre le texte expérimental et les artefacts réellement présents.
- [ ] Clarifier le nombre exact de graines utilisées et expliquer la divergence entre le manuscrit et les fichiers de campagne.
- [ ] Reproduire les métriques principales à partir des données réellement fournies et s’assurer qu’elles sont cohérentes.
- [ ] Corriger ou supprimer les références douteuses.
- [ ] Définir un protocole statistique robuste et l’appliquer aux résultats.
- [ ] Clarifier le statut des métriques d’énergie/CPU/RAM : estimées vs mesurées.
- [ ] Vérifier la provenance complète de chaque figure et tableau.
- [ ] Rendre la section de reproductibilité réellement exécutable sans hypothèse implicite.

### À améliorer fortement
- [ ] Rédaction plus concise et plus percutante.
- [ ] Meilleure distinction entre étude pilote, faisabilité et résultats définitifs.
- [ ] Meilleur positionnement vis-à-vis de l’état de l’art.
- [ ] Figures plus lisibles et plus interprétables.

---

## 5. Verdict global

### Évaluation globale
- Le projet montre un vrai potentiel scientifique et une bonne base technique.
- Il est crédible comme contribution préliminaire et comme paquet de reproductibilité.
- Il n’est pas encore au niveau d’une soumission “ready-to-submit” pour Computer Networks dans sa forme actuelle.

### Niveau de publication probable
- En l’état : pas encore publiable en tant que papier de niveau Computer Networks sans révision majeure.
- Après corrections sérieuses et validation expérimentale renforcée : il pourrait évoluer vers une contribution solide, probablement de niveau “good journal submission” ou “strong applied networking paper”, sous réserve d’une campagne plus robuste et d’un argumentaire plus tranchant.

### Recommandation finale
- Ne pas soumettre tel quel.
- Réviser en profondeur le volet expérimental et statistique, puis resoumettre en tant que version plus solide, plus transparente et plus clairement limitée à une étude pilote ou à une preuve de concept validée.
