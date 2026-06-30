J'ai analysé attentivement votre manuscrit "RPL-ClusterIDS" pour le journal Computer Networks. Voici l'identification détaillée de toutes les anomalies, incohérences et problèmes détectés, organisés par catégorie :

---

## 1. ANOMALIES NUMÉRIQUES ET INCOHÉRENCES DE DONNÉES

### 1.1 Tableau 8 (Page 19) - Données manquantes et incohérences
- **B2 et B3** : Le tableau indique `0.0%` pour le taux de détection (DR) de B2/B3, mais la note de bas de page indique `‡FPR data not collected for B2 and B3 baselines in this campaign` — **incohérence** : si les données FPR n'ont pas été collectées, pourquoi afficher `0.0%` plutôt que `N/A` ou un tiret ?
- **B3 dans le scénario "mixed"** : Le graphique Fig. 4 montre B3 avec ~40% de DR, alors que le Tableau 8 indique `0.0%` — **contradiction flagrante** entre le tableau et la figure.

### 1.2 Fig. 4 (Page 19) vs Tableau 8
- Le graphique montre des barres non-nulles pour B3 dans le scénario "mixed" (~40%), alors que le tableau indique 0.0% pour tous les scénarios B1-B3. C'est une **anomalie majeure** : soit le tableau est erroné, soit la légende du graphique est incorrecte.

### 1.3 Fig. 5 (Page 20) - Latence de détection
- La latence pour B1 est affichée comme identique (~25s) pour tous les scénarios, ce qui est statistiquement improbable si B1 est un baseline fonctionnel. Cela suggère que **B1 n'a détecté aucune attaque** (coherent avec DR=0%), mais alors pourquoi afficher une latence ? C'est trompeur — il faudrait indiquer "N/A" ou ne pas afficher B1.

### 1.4 Fig. 6 (Page 22) - FPR par classe de trafic
- Toutes les barres (B1, B2, B3, RPL-ClusterIDS) sont identiques à ~5×10⁻³. C'est **statistiquement suspect** : B1 (centralisé) et RPL-ClusterIDS (distribué hiérarchique) ne peuvent pas avoir exactement le même FPR à la précision affichée. Possible erreur de génération de figure ou de copie de données.

### 1.5 Tableau 10 (Page 23) - Données dupliquées/erronées
- Le tableau est **fragmenté et corrompu** : `DR†FPR†80.6%0.50%` apparaît en double, puis `nced 80.6%0.50%80.6%0.50%` — clairement une erreur de formatage/copie. Les données CPU sont manquantes pour Full et Balanced.

### 1.6 Fig. 11 (Page 27) - Échelle et lisibilité
- Les barres de DR et FPR sont **invisibles** (valeurs ~0.8 et ~0.005) comparées à l'échelle CPU (~5-7%). C'est une **erreur de visualisation** : les séries ne devraient pas être sur le même axe Y, ou il faut utiliser des axes doubles.

---

## 2. ANOMALIES TEXTUELLES ET TYPOGRAPHIQUES

### 2.1 Page 1 (Résumé)
- `80.6%DR` → manque espace : `80.6% DR`
- `0.50%FPR` → manque espace : `0.50% FPR`
- `5–7%CPU` → manque espace : `5–7% CPU`
- `3seeds` → `3 seeds`
- `5attack` → `5 attack`

### 2.2 Page 2 (Abstract)
- `80.6%campaign-level` → `80.6% campaign-level`
- `0.50%false-positive` → `0.50% false-positive`
- `5–7%CPU` → `5–7% CPU`
- `1.1%across` → `1.1% across`
- `Fig.11` → `Fig. 11` (espace manquant, récurrent dans tout le document)

### 2.3 Page 3
- `RPL-ClusterIDS,a` → virgule manquante ou espace : `RPL-ClusterIDS, a`
- `energyand` → `energy and`
- `context-adaptive` → cohérent, mais `context-adaptive` vs `context adaptive` (inconsistance dans le document)

### 2.4 Page 4
- `RPL-ClusterIDS (this work)` dans le tableau : le mot "Table" est tronqué en `able 1` — erreur de rendu LaTeX

### 2.5 Page 5
- `Omathcal((N^{2})` → clairement une **erreur LaTeX** : devrait être $\mathcal{O}(N^2)$

### 2.6 Page 6
- `RPLClusterIDS` → `RPL-ClusterIDS` (tiret manquant, récurrent)

### 2.7 Page 7
- `trust-based` vs `trust based` (inconsistance)
- `RPLspecific` → `RPL-specific`

### 2.8 Page 8
- `security–lifetime` → tiret long (en-dash) utilisé, mais ailleurs tiret court (hyphen) — **inconsistance typographique**

### 2.9 Page 10
- `N R E` → `NRE` (espaces parasites dans la formule mathématique)
- `Stabj` → `Stab_j` (indice manquant)
- `Disti,j` → `Dist_{i,j}` (formatage incorrect)

### 2.10 Page 11
- `T_{\mathrm{m a x}}` → espaces parasites dans le subscript mathématique

### 2.11 Page 12
- `Fig.3` → `Fig. 3` (espace manquant)

### 2.12 Page 13
- `RPL-ClusterIDS` vs `RPLClusterIDS` (récurrent)

### 2.13 Page 14
- `SIMULATION_CAMPAIGN_READY/attacks/` → chemin de fichier en dur dans le texte, inhabituel pour un article

### 2.14 Page 15
- `3perconfiguration` → `3 per configuration`
- `seeds.txt）` → parenthèse fermante chinoise `）` au lieu de parenthèse latine `)` — **anomalie d'encodage**

### 2.15 Page 16
- `O_{\mathrm{a l e r t}}, O{{\ {bar O}}}{{\ \{{t r l}\ \}}}` → **formule LaTeX complètement corrompue**, illisible

### 2.16 Page 17
- `ameter Configuration` → `Parameter Configuration` (début de mot tronqué)

### 2.17 Page 18
- `ble 6` → `Table 6` (début de mot tronqué, récurrent pour les tableaux)
- `firmware scale [0,∼175]` → phrase incompréhensible, probablement `firmware; scale [0,~175]`

### 2.18 Page 19
- `Fig.4and Fig.5` → `Fig. 4 and Fig. 5`
- `Fig.6stratifies` → `Fig. 6 stratifies`

### 2.19 Page 20
- `Fig.9links` → `Fig. 9 links`

### 2.20 Page 21
- `9.9\cdot10^{-3}` → texte parasite au-dessus de la figure, probablement une valeur de données mal placée

### 2.21 Page 22
- `Table 10` : texte corrompu `DR†FPR†80.6%0.50%` (déjà mentionné)

### 2.22 Page 23
- `O_{\mathrm{a l e r t}}, O{{\ {bar O}}}{{\ \{{t r l}\ \}}}` → répétition de la formule corrompue

### 2.23 Page 24
- `Fig.8is` → `Fig. 8 is`
- `50–500nodes` → `50–500 nodes`

### 2.24 Page 25
- `Fig.10stratifies` → `Fig. 10 stratifies`
- `Fig.11quantify` → `Fig. 11 quantify`

### 2.25 Page 26
- `50-node grid only` → titre de section sans majuscule initiale (inconsistant avec les autres sections)

### 2.26 Page 27
- `T_{\mathrm{m a x}}` → espaces parasites
- `C0,\ldots,C3` → formatage mathématique en plein texte

### 2.27 Page 28
- `twostage` → `two-stage` (tiret manquant)

### 2.28 Page 29
- `code_source_RPL_ClusterIDS/` → chemin de fichier en dur
- `figure generation` → `figure-generation` (inconsistance)

### 2.29 Page 30
- `data/real/(schemas` → `data/real/ (schemas` (espace manquant)
- `figure generation` → `figure-generation`
- `per-figure` → phrase incomplète

---

## 3. ANOMALIES DE CONTENU SCIENTIFIQUE ET MÉTHODOLOGIQUES

### 3.1 Baselines B2 et B3 (Page 14, 19)
- Le texte indique que B2 et B3 sont "planned for a future full campaign" (page 14), mais le Tableau 8 et les figures les incluent avec des valeurs `0.0%` ou des barres graphiques — **contradiction méthodologique majeure**. On ne peut pas comparer avec des baselines non implémentées.

### 3.2 Scénario "Mixed" - DR de 80.6% vs 95.1%
- Le texte (page 2) indique `80.6% campaign-level detection rate† (95.1% on individual attack scenarios)`. Le Tableau 8 montre 95.1% pour les attaques individuelles et 80.6% pour mixed. C'est cohérent, mais la note `†` n'est pas définie immédiatement — elle l'est page 19.

### 3.3 Ablation Study (Tableau 9, Page 20)
- `Without CH two-stage verification` donne `0.00%` DR — le texte explique que c'est parce que les LAS membres restent sous τ_las=0.60. Mais alors comment expliquer que `Without clustering` (qui n'a pas de CH) ait `0.33%` DR ? C'est **logiquement incohérent** : sans clustering, il n'y a pas de CH, donc le mécanisme devrait être similaire à "Without CH verification". La différence n'est pas expliquée.

### 3.4 CPU Overhead (Tableau 10, Page 23)
- Eco mode a `7%` CPU, Balanced `6%`, Full `5%` — **inversion contre-intuitive** : Eco (mode économique) consomme PLUS de CPU que Full. Le texte ne l'explique pas. C'est soit une erreur de données, soit une explication manquante.

### 3.5 Fig. 7 (Page 23) - Énergie
- RPL-ClusterIDS montre ~42% overhead pour membres et ~78% pour CH, alors que le texte (page 5) cite "5–7% CPU overhead". L'échelle Energest (%) n'est pas la même que CPU (%) — mais cela n'est pas clairement expliqué, créant une confusion potentielle.

### 3.6 Nombre de graines (seeds)
- Le texte répète "3 seeds" comme une limitation, mais ne justifie pas pourquoi ce nombre est suffisant pour des prétentions statistiques. Le Tableau 11 montre des p-values <0.0001 avec n=3 — ces p-values sont **statistiquement douteuses** avec si peu de degrés de liberté.

### 3.7 Fig. 8 (Page 24) - Scalabilité
- Le titre indique "values beyond 50 nodes are design-target projections" — mais ces projections sont tracées comme des points de données réels (diamants bleus). C'est **trompeur** : il faudrait une ligne pointillée ou une distinction visuelle claire.

### 3.8 Références [25] et [31]
- `[25]` : `Babylonian Journal of Artificial Intelligence 2026(2026)7–19,,Early access` — double virgule
- `[31]` : `19(2026)33,,Early access` — double virgule
- `\ {mathrm V y}` à la fin de [31] — **texte parasite LaTeX**

---

## 4. ANOMALIES DE STRUCTURE ET DE FORMAT

### 4.1 Numérotation des figures
- Fig. 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 — séquence correcte, mais certaines figures sont référencées avant leur apparition (Fig. 3 page 12, mais figure page 13).

### 4.2 Numérotation des tableaux
- Tableaux 1-11 présents, mais Tableaux 3-7 sont "Parameter Configuration" fragmentés — confusion entre Tableau 3 (paramètres), Tableau 4 (classes), Tableau 5 (règles membres), Tableau 6 (features CH), Tableau 7 (paramètres moteur). C'est dense et pourrait être fusionné.

### 4.3 Page 20 - Numéro de page "0"
- La page contient `0` comme numéro de page — **erreur de pagination** dans le PDF généré.

### 4.4 Figures manquantes référencées
- Le texte mentionne "see Fig. 11" pour le per-interval DR, mais Fig. 11 montre CPU/DR/FPR par mode — la valeur "1.1%" n'est pas visiblement annotée sur la figure.

---

## 5. ANOMALIES DE REPRODUCTIBILITÉ

### 5.1 URL du dépôt
- `https://github.com/madani-belacel/RPL-ClusterIDS` — URL correcte mais non vérifiée dans le document (pas de lien hypertexte actif dans le PDF).

### 5.2 Chemin de fichiers absolus
- `SIMULATION_CAMPAIGN_READY/`, `data/estimated/`, `code_source_RPL_ClusterIDS/` — ces chemins sont présentés comme des références internes, mais un lecteur externe ne peut pas les résoudre sans le dépôt.

### 5.3 "A persistent DOI will be requested upon acceptance"
- Mentionné deux fois (pages 29 et 30) — répétition inutile.

---

## RÉSUMÉ DES ANOMALIES CRITIQUES (À CORRIGER ABSOLUMENT AVANT PUBLICATION)

| Priorité | Anomalie | Localisation |
|:---|:---|:---|
| **CRITIQUE** | Incohérence B3 : 0% dans tableau vs ~40% dans Fig. 4 | Tableau 8, Fig. 4 |
| **CRITIQUE** | Tableau 10 corrompu (données dupliquées) | Page 23 |
| **CRITIQUE** | Formule LaTeX corrompue O_alert | Pages 16, 23 |
| **CRITIQUE** | Baselines B2/B3 "planned" mais présentées comme données | Page 14, Tableau 8 |
| **HAUTE** | CPU Eco (7%) > Full (5%) — inversion non expliquée | Tableau 10 |
| **HAUTE** | Ablation "Without clustering" 0.33% vs "Without CH" 0.00% — incohérence | Tableau 9 |
| **HAUTE** | FPR identique pour toutes les approches dans Fig. 6 | Fig. 6 |
| **MOYENNE** | Nombreuses erreurs d'espacement (Fig.11, 3seeds, etc.) | Tout le document |
| **MOYENNE** | Parenthèse chinoise `）` dans seeds.txt | Page 15 |
| **MOYENNE** | Double virgules dans références [25], [31] | Page 31-32 |
| **FAIBLE** | Numéro de page "0" | Page 20 |

---

Recommande fortement une relecture complète par un éditeur natif anglophone et une vérification rigoureuse des données source (CSV/logs) pour les Figures 4, 6 et le Tableau 10 avant soumission.
