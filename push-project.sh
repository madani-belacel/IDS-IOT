#!/bin/bash

cd ~/contiki-ng/examples/IDS_IOT

echo "=== Push Project IDS-IOT ==="

# Vérifier s'il y a des modifications
if git status --porcelain | grep -q .; then
    echo "📝 Modifications détectées :"
    git status --short
    
    git add .
    
    git commit -m "Mise à jour : corrections diverses - $(date '+%Y-%m-%d %H:%M')"
    
    echo "🚀 Push en cours..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Push réussi !"
        echo "Lien : https://github.com/madani-belacel/IDS-IOT"
    else
        echo "❌ Erreur lors du push"
    fi
else
    echo "⚠️ Aucune modification détectée."
fi
