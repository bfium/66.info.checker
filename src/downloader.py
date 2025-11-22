"""
Module de téléchargement de vidéos TikTok
"""
import os
import yt_dlp
from pathlib import Path
from typing import List, Optional
from src.config import Config

class TikTokDownloader:
    """Gestionnaire de téléchargement de vidéos TikTok"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Config.VIDEOS_DIR
        self.output_dir.mkdir(exist_ok=True)
    
    def download_video(self, url: str, output_filename: Optional[str] = None) -> Path:
        """
        Télécharge une vidéo TikTok spécifique
        
        Args:
            url: URL de la vidéo TikTok
            output_filename: Nom du fichier de sortie (optionnel)
            
        Returns:
            Chemin du fichier vidéo téléchargé
        """
        if output_filename:
            output_path = self.output_dir / output_filename
        else:
            output_path = self.output_dir / "%(title)s.%(ext)s"
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': str(output_path),
            'quiet': False,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return Path(filename)
    
    def download_user_videos(self, username: str, max_videos: int = 5) -> List[Path]:
        """
        Télécharge les vidéos récentes d'un utilisateur TikTok
        
        Args:
            username: Nom d'utilisateur TikTok (sans @)
            max_videos: Nombre maximum de vidéos à télécharger
            
        Returns:
            Liste des chemins des vidéos téléchargées
        """
        user_url = f"https://www.tiktok.com/@{username}"
        user_dir = self.output_dir / username
        user_dir.mkdir(exist_ok=True)
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': str(user_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'playlistend': max_videos,
        }
        
        downloaded_files = []
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(user_url, download=True)
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            filename = ydl.prepare_filename(entry)
                            downloaded_files.append(Path(filename))
            except Exception as e:
                print(f"Erreur lors du téléchargement: {e}")
        
        return downloaded_files
    
    def get_video_info(self, url: str) -> dict:
        """
        Récupère les métadonnées d'une vidéo sans la télécharger
        
        Args:
            url: URL de la vidéo TikTok
            
        Returns:
            Dictionnaire avec les métadonnées
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', ''),
                'description': info.get('description', ''),
                'uploader': info.get('uploader', ''),
                'upload_date': info.get('upload_date', ''),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'like_count': info.get('like_count', 0),
            }

