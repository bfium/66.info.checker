"""
Module de transcription audio/vidéo avec Whisper
"""
import whisper
from pathlib import Path
from typing import Optional

class AudioTranscriber:
    """Gestionnaire de transcription audio avec Whisper"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialise le modèle Whisper
        
        Args:
            model_size: Taille du modèle ('tiny', 'base', 'small', 'medium', 'large')
        """
        print(f"Chargement du modèle Whisper ({model_size})...")
        self.model = whisper.load_model(model_size)
        print("Modèle chargé avec succès!")
    
    def transcribe_video(self, video_path: Path, language: str = "fr") -> dict:
        """
        Transcrit l'audio d'une vidéo
        
        Args:
            video_path: Chemin vers le fichier vidéo
            language: Code langue ('fr' pour français)
            
        Returns:
            Dictionnaire avec la transcription et les métadonnées
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Fichier vidéo introuvable: {video_path}")
        
        print(f"Transcription de {video_path.name}...")
        result = self.model.transcribe(
            str(video_path),
            language=language,
            task="transcribe"
        )
        
        return {
            'text': result['text'],
            'segments': result.get('segments', []),
            'language': result.get('language', language),
            'duration': result.get('duration', 0)
        }
    
    def transcribe_audio(self, audio_path: Path, language: str = "fr") -> dict:
        """
        Transcrit un fichier audio
        
        Args:
            audio_path: Chemin vers le fichier audio
            language: Code langue ('fr' pour français)
            
        Returns:
            Dictionnaire avec la transcription et les métadonnées
        """
        return self.transcribe_video(audio_path, language)

