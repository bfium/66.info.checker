"""
Module d'analyse LLM avec support multi-providers
"""
from typing import Dict, Optional
from openai import OpenAI
import anthropic
import requests
from src.config import Config

class LLMAnalyzer:
    """Analyseur LLM avec support pour plusieurs providers"""
    
    def __init__(self, provider: Optional[str] = None):
        """
        Initialise l'analyseur avec un provider spécifique
        
        Args:
            provider: 'openai', 'anthropic', ou 'local'
        """
        self.provider = provider or Config.DEFAULT_LLM_PROVIDER
        
        if self.provider == "openai":
            if not Config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY non configurée")
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        elif self.provider == "anthropic":
            if not Config.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY non configurée")
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        elif self.provider == "local":
            self.client = None  # Utiliser requests pour les appels locaux
        else:
            raise ValueError(f"Provider non supporté: {self.provider}")
    
    def analyze_content(self, transcription: str, video_metadata: Optional[Dict] = None) -> Dict:
        """
        Analyse le contenu transcrit avec un LLM
        
        Args:
            transcription: Texte transcrit de la vidéo
            video_metadata: Métadonnées de la vidéo (optionnel)
            
        Returns:
            Dictionnaire avec l'analyse qualitative et quantitative
        """
        prompt = self._build_analysis_prompt(transcription, video_metadata)
        
        if self.provider == "openai":
            return self._analyze_openai(prompt)
        elif self.provider == "anthropic":
            return self._analyze_anthropic(prompt)
        elif self.provider == "local":
            return self._analyze_local(prompt)
    
    def _build_analysis_prompt(self, transcription: str, video_metadata: Optional[Dict]) -> str:
        """Construit le prompt d'analyse"""
        prompt = f"""Tu es un expert en analyse de contenu et vérification de faits. Analyse le texte suivant d'une vidéo TikTok et fournis une analyse détaillée.

TEXTE À ANALYSER:
{transcription}

Effectue une analyse complète incluant:
1. **Résumé du contenu** : Résume les points principaux abordés
2. **Affirmations clés** : Liste toutes les affirmations factuelles faites dans la vidéo
3. **Ton et style** : Analyse le ton utilisé (neutre, alarmiste, persuasif, etc.)
4. **Sources mentionnées** : Note si des sources sont citées ou mentionnées
5. **Points à vérifier** : Identifie les affirmations qui nécessitent une vérification factuelle
6. **Score de crédibilité initial** : Donne un score de 0 à 100 basé sur la structure et la présentation du contenu

Réponds en français et structure ta réponse de manière claire."""
        
        if video_metadata:
            prompt += f"\n\nMÉTADONNÉES VIDÉO:\n{video_metadata}"
        
        return prompt
    
    def _analyze_openai(self, prompt: str) -> Dict:
        """Analyse avec OpenAI"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse de contenu et vérification de faits."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        analysis_text = response.choices[0].message.content
        
        return {
            'provider': 'openai',
            'analysis': analysis_text,
            'raw_response': response.model_dump()
        }
    
    def _analyze_anthropic(self, prompt: str) -> Dict:
        """Analyse avec Anthropic Claude"""
        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        analysis_text = message.content[0].text
        
        return {
            'provider': 'anthropic',
            'analysis': analysis_text,
            'raw_response': message.model_dump()
        }
    
    def _analyze_local(self, prompt: str) -> Dict:
        """Analyse avec un modèle local (Ollama)"""
        url = f"{Config.LOCAL_LLM_URL}/api/generate"
        
        response = requests.post(
            url,
            json={
                "model": Config.LOCAL_LLM_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Erreur API locale: {response.status_code}")
        
        result = response.json()
        analysis_text = result.get('response', '')
        
        return {
            'provider': 'local',
            'analysis': analysis_text,
            'raw_response': result
        }

