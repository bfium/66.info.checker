# Info Checker - Vérificateur de Faits pour TikTok

Application Python pour analyser et vérifier la crédibilité des informations partagées par les influenceurs TikTok.

## Fonctionnalités

- 📥 **Téléchargement automatique** : Télécharge les vidéos TikTok d'un influenceur ou une vidéo spécifique
- 🎤 **Transcription** : Transcription automatique de l'audio avec Whisper
- 🤖 **Analyse LLM** : Analyse qualitative et quantitative avec plusieurs providers (OpenAI, Anthropic, local)
- 🔍 **Vérification des faits** : Recherche dans plusieurs sources (web, bases fact-checking, articles scientifiques, sources d'actualité)
- 📊 **Visualisations** : Graphiques, statistiques et diagrammes interactifs
- 💾 **Stockage** : Sauvegarde des résultats en JSON et Markdown

## Installation

1. Cloner le projet
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env et ajouter vos clés API
```

4. Installer FFmpeg (requis pour le traitement vidéo) :
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg

# Windows
# Télécharger depuis https://ffmpeg.org/download.html
```

## Utilisation

Ouvrir le notebook Jupyter principal :
```bash
jupyter notebook main.ipynb
```

## Structure du projet

```
.
├── src/
│   ├── downloader.py      # Téléchargement vidéos TikTok
│   ├── transcriber.py      # Transcription audio
│   ├── analyzer.py         # Analyse LLM
│   ├── fact_checker.py     # Vérification des faits
│   ├── visualizer.py       # Visualisations
│   └── storage.py          # Stockage JSON/Markdown
├── main.ipynb              # Notebook principal
├── requirements.txt
└── README.md
```

## Configuration

Modifier `.env` pour configurer :
- Clés API (OpenAI, Anthropic)
- Provider LLM par défaut
- Répertoires de sortie

## Licence

Usage personnel

