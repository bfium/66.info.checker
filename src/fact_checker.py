"""
Module de vérification des faits avec recherche multi-sources
"""
from typing import List, Dict
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import re

class FactChecker:
    """Vérificateur de faits avec recherche dans plusieurs sources"""
    
    def __init__(self):
        self.fact_checking_sites = [
            'snopes.com',
            'factcheck.org',
            'politifact.com',
            'lemonde.fr/verification',
            'lesdecodeurs.lemonde.fr',
            'factuel.afp.com'
        ]
    
    def verify_claims(self, claims: List[str], language: str = "fr") -> Dict:
        """
        Vérifie une liste d'affirmations
        
        Args:
            claims: Liste des affirmations à vérifier
            language: Langue de recherche ('fr' pour français)
            
        Returns:
            Dictionnaire avec les résultats de vérification pour chaque affirmation
        """
        results = {}
        
        for claim in claims:
            print(f"Vérification de: {claim[:50]}...")
            verification = self._verify_single_claim(claim, language)
            results[claim] = verification
        
        return results
    
    def _verify_single_claim(self, claim: str, language: str) -> Dict:
        """Vérifie une seule affirmation"""
        results = {
            'claim': claim,
            'sources': [],
            'fact_checking_results': [],
            'scientific_results': [],
            'news_results': [],
            'credibility_score': 0,
            'verdict': 'non_verifie'
        }
        
        # Recherche dans les bases de fact-checking
        fact_check_results = self._search_fact_checking(claim, language)
        results['fact_checking_results'] = fact_check_results
        
        # Recherche scientifique
        scientific_results = self._search_scientific(claim, language)
        results['scientific_results'] = scientific_results
        
        # Recherche dans les sources d'actualité
        news_results = self._search_news(claim, language)
        results['news_results'] = news_results
        
        # Recherche web générale
        web_results = self._search_web(claim, language)
        results['sources'] = web_results
        
        # Calcul du score de crédibilité
        results['credibility_score'] = self._calculate_credibility_score(results)
        
        # Détermination du verdict
        results['verdict'] = self._determine_verdict(results)
        
        return results
    
    def _search_fact_checking(self, query: str, language: str) -> List[Dict]:
        """Recherche dans les sites de fact-checking"""
        results = []
        
        for site in self.fact_checking_sites:
            search_query = f"{query} site:{site}"
            try:
                # Utiliser DuckDuckGo pour éviter les limites de Google
                with DDGS() as ddgs:
                    for result in ddgs.text(search_query, max_results=3):
                        results.append({
                            'title': result.get('title', ''),
                            'url': result.get('href', ''),
                            'snippet': result.get('body', ''),
                            'source': site
                        })
            except Exception as e:
                print(f"Erreur recherche fact-checking sur {site}: {e}")
        
        return results[:10]  # Limiter à 10 résultats
    
    def _search_scientific(self, query: str, language: str) -> List[Dict]:
        """Recherche dans les bases de données scientifiques"""
        results = []
        
        # Recherche Google Scholar
        scholar_query = f"{query} site:scholar.google.com"
        try:
            with DDGS() as ddgs:
                for result in ddgs.text(scholar_query, max_results=5):
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'source': 'Google Scholar'
                    })
        except Exception as e:
            print(f"Erreur recherche scientifique: {e}")
        
        return results
    
    def _search_news(self, query: str, language: str) -> List[Dict]:
        """Recherche dans les sources d'actualité vérifiées"""
        trusted_news_sources = [
            'reuters.com',
            'apnews.com',
            'lemonde.fr',
            'franceinfo.fr',
            'france24.com'
        ]
        
        results = []
        
        for source in trusted_news_sources:
            search_query = f"{query} site:{source}"
            try:
                with DDGS() as ddgs:
                    for result in ddgs.text(search_query, max_results=3):
                        results.append({
                            'title': result.get('title', ''),
                            'url': result.get('href', ''),
                            'snippet': result.get('body', ''),
                            'source': source
                        })
            except Exception as e:
                print(f"Erreur recherche actualités sur {source}: {e}")
        
        return results[:15]
    
    def _search_web(self, query: str, language: str) -> List[Dict]:
        """Recherche web générale"""
        results = []
        
        try:
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=10):
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'source': 'Web'
                    })
        except Exception as e:
            print(f"Erreur recherche web: {e}")
        
        return results
    
    def _calculate_credibility_score(self, results: Dict) -> int:
        """Calcule un score de crédibilité de 0 à 100"""
        score = 50  # Score de base
        
        # Bonus pour résultats de fact-checking
        if results['fact_checking_results']:
            score += min(len(results['fact_checking_results']) * 5, 20)
        
        # Bonus pour résultats scientifiques
        if results['scientific_results']:
            score += min(len(results['scientific_results']) * 3, 15)
        
        # Bonus pour sources d'actualité vérifiées
        if results['news_results']:
            score += min(len(results['news_results']) * 2, 15)
        
        return min(score, 100)
    
    def _determine_verdict(self, results: Dict) -> str:
        """Détermine le verdict (vrai, faux, non_verifie, partiellement_vrai)"""
        fact_checking = results['fact_checking_results']
        scientific = results['scientific_results']
        news = results['news_results']
        
        # Si des résultats de fact-checking existent, les prioriser
        if fact_checking:
            # Analyser les snippets pour détecter des mots-clés
            snippets = ' '.join([r.get('snippet', '').lower() for r in fact_checking])
            if any(word in snippets for word in ['false', 'faux', 'misleading', 'trompeur']):
                return 'faux'
            elif any(word in snippets for word in ['true', 'vrai', 'correct', 'correct']):
                return 'vrai'
            elif any(word in snippets for word in ['partially', 'partiellement', 'mixture']):
                return 'partiellement_vrai'
        
        # Si beaucoup de sources scientifiques et d'actualité
        if len(scientific) >= 3 and len(news) >= 3:
            return 'probablement_vrai'
        
        # Si peu ou pas de sources
        if len(results['sources']) < 3:
            return 'non_verifie'
        
        return 'non_verifie'

