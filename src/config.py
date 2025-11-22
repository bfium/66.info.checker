"""
Configuration et gestion des variables d'environnement
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration de l'application"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Local LLM
    LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
    LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "llama2")
    
    # Provider par défaut
    DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
    
    # Répertoires
    BASE_DIR = Path(__file__).parent.parent
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "results"))
    VIDEOS_DIR = Path(os.getenv("VIDEOS_DIR", BASE_DIR / "videos"))
    
    # Créer les répertoires s'ils n'existent pas
    OUTPUT_DIR.mkdir(exist_ok=True)
    VIDEOS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Valider la configuration"""
        if cls.DEFAULT_LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY est requis pour utiliser OpenAI")
        if cls.DEFAULT_LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY est requis pour utiliser Anthropic")

