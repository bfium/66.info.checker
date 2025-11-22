# Guide de Démarrage Rapide

## Installation

1. **Installer les dépendances Python** :
```bash
pip install -r requirements.txt
```

2. **Installer FFmpeg** (requis pour le traitement vidéo) :
```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg

# Windows
# Télécharger depuis https://ffmpeg.org/download.html
```

3. **Configurer les variables d'environnement** :
```bash
# Copier le fichier d'exemple
cp env.example .env

# Éditer .env et ajouter votre clé API OpenAI
# OPENAI_API_KEY=sk-votre-cle-ici
```

## Utilisation

1. **Ouvrir le notebook Jupyter** :
```bash
jupyter notebook main.ipynb
```

2. **Dans le notebook, configurer les paramètres** (Cellule 2) :
   - Choisir le mode : `"video"` pour une vidéo spécifique ou `"user"` pour un utilisateur
   - Fournir l'URL de la vidéo ou le nom d'utilisateur
   - Ajuster le nombre de vidéos à analyser si nécessaire

3. **Exécuter les cellules dans l'ordre** :
   - Cellule 1 : Configuration et import
   - Cellule 2 : Paramètres d'analyse
   - Cellule 3 : Téléchargement des vidéos
   - Cellule 4 : Transcription
   - Cellule 5 : Analyse LLM
   - Cellule 6 : Extraction des affirmations
   - Cellule 7 : Vérification des faits
   - Cellule 8 : Compilation des résultats
   - Cellule 9 : Visualisations
   - Cellule 10 : Sauvegarde
   - Cellule 11 : Tableau de bord interactif

## Exemple d'utilisation

### Analyser une vidéo spécifique :
```python
analysis_mode = "video"
video_url = "https://www.tiktok.com/@username/video/1234567890"
```

### Analyser un utilisateur complet :
```python
analysis_mode = "user"
username = "username"  # Sans le @
max_videos = 5
```

## Résultats

Les résultats sont sauvegardés dans le dossier `results/` :
- **Fichiers JSON** : Données brutes de l'analyse
- **Fichiers Markdown** : Rapports formatés
- **Fichiers HTML** : Tableaux de bord interactifs
- **Graphiques** : Visualisations matplotlib

## Notes importantes

- La première utilisation peut prendre du temps car Whisper télécharge le modèle
- Les appels API OpenAI peuvent avoir un coût selon votre plan
- Le téléchargement de vidéos TikTok peut être limité par les politiques de TikTok
- Les recherches web peuvent prendre plusieurs minutes selon le nombre d'affirmations

## Dépannage

**Erreur "OPENAI_API_KEY non configurée"** :
- Vérifiez que le fichier `.env` existe et contient votre clé API

**Erreur lors du téléchargement de vidéos** :
- TikTok peut bloquer certains téléchargements
- Essayez avec une URL différente ou vérifiez votre connexion

**Erreur de transcription** :
- Vérifiez que FFmpeg est installé : `ffmpeg -version`
- Assurez-vous que le fichier vidéo est valide

