# Info Checker - Vérificateur de Faits TikTok

## Concept
Démêler le vrai du faux des informations des influenceurs sur TikTok

## Workflow Implémenté

### 1. Téléchargement des vidéos
- Support pour une vidéo spécifique (URL) ou un utilisateur complet
- Utilisation de yt-dlp pour le téléchargement
- Récupération automatique des métadonnées (titre, vues, likes, date)

### 2. Transcription
- Transcription automatique avec Whisper (OpenAI)
- Support du français
- Extraction du texte et des segments temporels

### 3. Analyse LLM
- Analyse qualitative et quantitative avec plusieurs providers :
  - OpenAI (GPT-4)
  - Anthropic (Claude)
  - Modèles locaux (Ollama)
- Extraction des affirmations clés
- Analyse du ton et du style

### 4. Vérification des faits
- Recherche multi-sources :
  - Bases de fact-checking (Snopes, FactCheck.org, etc.)
  - Articles scientifiques (Google Scholar)
  - Sources d'actualité vérifiées (Reuters, AP News, etc.)
  - Recherche web générale
- Calcul d'un score de crédibilité (0-100)
- Détermination d'un verdict (vrai, faux, partiellement vrai, non vérifié)

### 5. Visualisations
- Graphiques de crédibilité par vidéo
- Répartition des verdicts (graphique circulaire)
- Évolution dans le temps (timeline)
- Nuage de mots des sujets principaux
- Tableau de bord interactif (Plotly)

### 6. Stockage
- Sauvegarde en JSON (données brutes)
- Génération de rapports Markdown formatés
- Tableaux de bord HTML interactifs

## Améliorations apportées

✅ Architecture modulaire et extensible
✅ Support multi-providers LLM
✅ Recherche dans plusieurs sources de vérification
✅ Visualisations complètes et interactives
✅ Notebook Jupyter pour workflow interactif
✅ Gestion des erreurs et validation de configuration
✅ Documentation complète (README, QUICKSTART)

## Prochaines améliorations possibles

- [ ] Amélioration de l'extraction d'affirmations avec LLM dédié
- [ ] Cache des résultats de vérification pour éviter les recherches répétées
- [ ] Support de plusieurs langues
- [ ] Interface web au lieu du notebook
- [ ] Analyse de sentiment plus poussée
- [ ] Détection de manipulation d'images/vidéos 