# Gabarit revue — RPL-ClusterIDS (`IDS_IOT/`)

## Deux versions

| Fichier | Gabarit | Usage |
|---------|---------|--------|
| `main.tex` | `article` 11pt, A4, une colonne | Rédaction auteur |
| `main-ieee.tex` | **IEEEtran** `journal`, deux colonnes | Soumission IEEE |

`IEEEtran.cls` (v1.8b) : `templates/ieee/`. Biblio : `templates/ieee/IEEEtran.bst`.

## Compiler la version IEEE

```bash
cd IDS_IOT
pdflatex main-ieee.tex
bibtex main-ieee
pdflatex main-ieee.tex
pdflatex main-ieee.tex
```

Sortie : **`main-ieee.pdf`** (à soumettre).

## Avant dépôt portail IEEE

- Titre portail = `\PaperTitle` dans `metadata.tex` (mot pour mot)
- Page 1 : `\PaperIEEEJournalAuthor` + `\IEEEaftertitletext` (affiliation / e-mail / ORCID)
- Vérifier 11 figures (voir `figures_manifest.csv`)
- Checklist : `checklist.md`
