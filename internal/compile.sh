#!/bin/bash
# ================================================
# Compile.sh - Script de compilation LaTeX IDS_IOT
# ================================================

cd "$(dirname "$0")"

echo "=== Nettoyage des fichiers temporaires LaTeX ==="
find . \( -name "*.aux" -o -name "*.log" -o -name "*.bbl" -o -name "*.blg" \
    -o -name "*.out" -o -name "*.fls" -o -name "*.fdb_latexmk" \
    -o -name "*.synctex.gz" -o -name "*.toc" -o -name "*.lof" -o -name "*.lot" \) -delete 2>/dev/null

echo "Nettoyage terminé."

# ================================================
# Compilation main-ieee.pdf (IEEE format)
# ================================================
echo "=== Compilation main-ieee.pdf (IEEE) ==="

pdflatex -interaction=nonstopmode main-ieee.tex
bibtex main-ieee
pdflatex -interaction=nonstopmode main-ieee.tex
pdflatex -interaction=nonstopmode main-ieee.tex

if [ -f "main-ieee.pdf" ]; then
    echo "✅ main-ieee.pdf généré avec succès !"
    pdfinfo main-ieee.pdf | grep -E "Pages|Title|Producer"
else
    echo "❌ Erreur : main-ieee.pdf n'a pas été généré."
fi

# ================================================
# Compilation main.pdf (Computer Networks / format standard)
# ================================================
echo "=== Compilation main.pdf (format standard) ==="

pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

if [ -f "main.pdf" ]; then
    echo "✅ main.pdf généré avec succès !"
    pdfinfo main.pdf | grep -E "Pages|Title|Producer"
else
    echo "❌ Erreur : main.pdf n'a pas été généré."
fi

echo "============================================"
echo "Compilation terminée."
echo "Fichiers générés :"
ls -lh *.pdf 2>/dev/null || echo "Aucun PDF trouvé."
