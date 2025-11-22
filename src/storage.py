"""
Module de stockage des résultats en JSON et Markdown
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from src.config import Config

class ResultStorage:
    """Gestionnaire de stockage des résultats"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Config.OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)
    
    def save_results(self, results: Dict, filename_prefix: str = None) -> Dict[str, Path]:
        """
        Sauvegarde les résultats en JSON et Markdown
        
        Args:
            results: Dictionnaire avec les résultats d'analyse
            filename_prefix: Préfixe pour les noms de fichiers
            
        Returns:
            Dictionnaire avec les chemins des fichiers sauvegardés
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = filename_prefix or "analysis"
        base_filename = f"{prefix}_{timestamp}"
        
        # Sauvegarder en JSON
        json_path = self.output_dir / f"{base_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder en Markdown
        md_path = self.output_dir / f"{base_filename}.md"
        markdown_content = self._generate_markdown(results)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return {
            'json': json_path,
            'markdown': md_path
        }
    
    def _generate_markdown(self, results: Dict) -> str:
        """Génère le contenu Markdown à partir des résultats"""
        md = f"# Rapport d'Analyse - {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        # Informations générales
        if 'metadata' in results:
            md += "## Informations Générales\n\n"
            metadata = results['metadata']
            md += f"- **Influenceur/URL**: {metadata.get('source', 'N/A')}\n"
            md += f"- **Nombre de vidéos analysées**: {metadata.get('video_count', 0)}\n"
            md += f"- **Date d'analyse**: {metadata.get('analysis_date', 'N/A')}\n\n"
        
        # Résultats par vidéo
        if 'videos' in results:
            md += "## Résultats par Vidéo\n\n"
            
            for i, video in enumerate(results['videos'], 1):
                md += f"### Vidéo {i}: {video.get('title', 'Sans titre')}\n\n"
                
                # Métadonnées
                if 'metadata' in video:
                    meta = video['metadata']
                    md += f"**Métadonnées:**\n"
                    md += f"- Auteur: {meta.get('uploader', 'N/A')}\n"
                    md += f"- Date: {meta.get('upload_date', 'N/A')}\n"
                    md += f"- Vues: {meta.get('view_count', 0):,}\n"
                    md += f"- Likes: {meta.get('like_count', 0):,}\n\n"
                
                # Transcription
                if 'transcription' in video:
                    md += f"**Transcription:**\n\n{video['transcription'].get('text', 'N/A')}\n\n"
                
                # Analyse LLM
                if 'llm_analysis' in video:
                    md += f"**Analyse LLM:**\n\n{video['llm_analysis'].get('analysis', 'N/A')}\n\n"
                
                # Vérification des faits
                if 'fact_checking' in video:
                    fact_check = video['fact_checking']
                    md += f"**Vérification des Faits:**\n\n"
                    md += f"- Score de crédibilité: {fact_check.get('credibility_score', 0)}%\n"
                    md += f"- Verdict: {fact_check.get('verdict', 'non_verifie')}\n\n"
                    
                    # Sources
                    if 'sources' in fact_check:
                        md += "**Sources trouvées:**\n\n"
                        for source in fact_check['sources'][:10]:  # Limiter à 10
                            md += f"- [{source.get('title', 'Sans titre')}]({source.get('url', '#')})\n"
                            md += f"  - {source.get('snippet', '')[:100]}...\n\n"
                
                md += "---\n\n"
        
        # Statistiques globales
        if 'statistics' in results:
            md += "## Statistiques Globales\n\n"
            stats = results['statistics']
            md += f"- Score moyen de crédibilité: {stats.get('average_credibility', 0):.1f}%\n"
            md += f"- Nombre de vidéos vérifiées: {stats.get('verified_count', 0)}\n"
            md += f"- Nombre de vidéos non vérifiées: {stats.get('unverified_count', 0)}\n\n"
        
        return md
    
    def load_results(self, json_path: Path) -> Dict:
        """
        Charge les résultats depuis un fichier JSON
        
        Args:
            json_path: Chemin vers le fichier JSON
            
        Returns:
            Dictionnaire avec les résultats
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

