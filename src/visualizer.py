"""
Module de visualisation des résultats d'analyse
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import pandas as pd
from typing import Dict, List
import re

# Configuration matplotlib pour le français
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

class ResultVisualizer:
    """Gestionnaire de visualisations des résultats"""
    
    def __init__(self):
        self.colors = {
            'vrai': '#2ecc71',
            'faux': '#e74c3c',
            'partiellement_vrai': '#f39c12',
            'probablement_vrai': '#3498db',
            'non_verifie': '#95a5a6'
        }
    
    def create_credibility_chart(self, results: List[Dict], save_path: str = None):
        """
        Crée un graphique en barres des scores de crédibilité
        
        Args:
            results: Liste des résultats d'analyse
            save_path: Chemin pour sauvegarder le graphique
        """
        titles = [r.get('title', f"Vidéo {i+1}") for i, r in enumerate(results)]
        scores = [r.get('credibility_score', 0) for r in results]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(titles, scores, color='steelblue')
        
        # Ajouter les valeurs sur les barres
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 1, i, f'{score}%', va='center', fontweight='bold')
        
        ax.set_xlabel('Score de Crédibilité (%)', fontsize=12)
        ax.set_title('Scores de Crédibilité par Vidéo', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_verdict_pie(self, results: List[Dict], save_path: str = None):
        """
        Crée un graphique circulaire des verdicts
        
        Args:
            results: Liste des résultats d'analyse
            save_path: Chemin pour sauvegarder le graphique
        """
        verdicts = {}
        for result in results:
            verdict = result.get('verdict', 'non_verifie')
            verdicts[verdict] = verdicts.get(verdict, 0) + 1
        
        labels = list(verdicts.keys())
        sizes = list(verdicts.values())
        colors_list = [self.colors.get(v, '#95a5a6') for v in labels]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_list, startangle=90)
        ax.set_title('Répartition des Verdicts', fontsize=14, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_timeline_chart(self, results: List[Dict], save_path: str = None):
        """
        Crée un graphique d'évolution dans le temps
        
        Args:
            results: Liste des résultats d'analyse avec dates
            save_path: Chemin pour sauvegarder le graphique
        """
        dates = []
        scores = []
        
        for result in results:
            date = result.get('upload_date', '')
            if date:
                dates.append(date)
                scores.append(result.get('credibility_score', 0))
        
        if not dates:
            return None
        
        df = pd.DataFrame({'date': dates, 'score': scores})
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
        df = df.sort_values('date')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['date'], df['score'], marker='o', linewidth=2, markersize=8)
        ax.fill_between(df['date'], df['score'], alpha=0.3)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Score de Crédibilité (%)', fontsize=12)
        ax.set_title('Évolution de la Crédibilité dans le Temps', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_wordcloud(self, transcriptions: List[str], save_path: str = None):
        """
        Crée un nuage de mots à partir des transcriptions
        
        Args:
            transcriptions: Liste des textes transcrits
            save_path: Chemin pour sauvegarder le graphique
        """
        # Combiner tous les textes
        text = ' '.join(transcriptions)
        
        # Nettoyer le texte (supprimer les mots vides français)
        stopwords_fr = {'le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'un', 'une', 
                       'ce', 'cette', 'ces', 'il', 'elle', 'ils', 'elles', 'je', 'tu',
                       'nous', 'vous', 'on', 'ça', 'c\'est', 'est', 'sont', 'être',
                       'avoir', 'faire', 'dire', 'voir', 'aller', 'venir', 'pour',
                       'dans', 'sur', 'avec', 'sans', 'par', 'pour', 'mais', 'donc'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = [w for w in words if w not in stopwords_fr and len(w) > 3]
        text_clean = ' '.join(filtered_words)
        
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            max_words=100,
            colormap='viridis'
        ).generate(text_clean)
        
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Nuage de Mots - Sujets Principaux', fontsize=16, fontweight='bold', pad=20)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_interactive_dashboard(self, results: List[Dict], save_path: str = None):
        """
        Crée un tableau de bord interactif avec Plotly
        
        Args:
            results: Liste des résultats d'analyse
            save_path: Chemin pour sauvegarder le HTML
        """
        df = pd.DataFrame(results)
        
        # Graphique 1: Scores de crédibilité
        fig1 = px.bar(
            df,
            x='title',
            y='credibility_score',
            title='Scores de Crédibilité',
            labels={'credibility_score': 'Score (%)', 'title': 'Vidéo'}
        )
        
        # Graphique 2: Répartition des verdicts
        verdict_counts = df['verdict'].value_counts()
        fig2 = px.pie(
            values=verdict_counts.values,
            names=verdict_counts.index,
            title='Répartition des Verdicts'
        )
        
        # Combiner les graphiques
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Scores de Crédibilité', 'Répartition des Verdicts'),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )
        
        fig.add_trace(fig1.data[0], row=1, col=1)
        fig.add_trace(fig2.data[0], row=1, col=2)
        
        fig.update_layout(
            height=600,
            title_text="Tableau de Bord d'Analyse",
            showlegend=True
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig

