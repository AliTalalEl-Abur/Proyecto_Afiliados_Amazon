"""
Cliente para Google Search Console API
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os


class SearchConsoleClient:
    """Cliente para obtener métricas de Google Search Console"""
    
    def __init__(self):
        # Credenciales de servicio (JSON)
        self.credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "")
        self.site_url = os.getenv("SITE_URL", "")
        
        # Inicializar cliente si hay credenciales
        self.client = None
        if self.credentials_file and self.site_url:
            try:
                from google.oauth2 import service_account
                from googleapiclient.discovery import build
                
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_file,
                    scopes=['https://www.googleapis.com/auth/webmasters.readonly']
                )
                
                self.client = build('searchconsole', 'v1', credentials=credentials)
            except Exception as e:
                print(f"Warning: No se pudo inicializar Search Console: {str(e)}")
                self.client = None
    
    async def get_site_metrics(
        self,
        days_back: int = 30,
        dimensions: List[str] = None
    ) -> Dict:
        """
        Obtiene métricas del sitio desde Search Console
        
        Args:
            days_back: Número de días hacia atrás
            dimensions: Dimensiones a analizar (query, page, country, device)
        
        Returns:
            Métricas del sitio
        """
        if not self.client:
            return {
                "success": False,
                "error": "Google Search Console no configurado"
            }
        
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days_back)
            
            request_body = {
                'startDate': start_date.isoformat(),
                'endDate': end_date.isoformat(),
                'dimensions': dimensions or ['query'],
                'rowLimit': 100
            }
            
            response = self.client.searchanalytics().query(
                siteUrl=self.site_url,
                body=request_body
            ).execute()
            
            return {
                "success": True,
                "data": response.get('rows', []),
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_page_performance(
        self,
        page_url: str,
        days_back: int = 30
    ) -> Dict:
        """
        Obtiene métricas de una página específica
        
        Args:
            page_url: URL de la página
            days_back: Número de días hacia atrás
        
        Returns:
            Métricas de la página
        """
        if not self.client:
            return self._mock_data(page_url)
        
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days_back)
            
            request_body = {
                'startDate': start_date.isoformat(),
                'endDate': end_date.isoformat(),
                'dimensions': ['query'],
                'dimensionFilterGroups': [{
                    'filters': [{
                        'dimension': 'page',
                        'expression': page_url
                    }]
                }],
                'rowLimit': 50
            }
            
            response = self.client.searchanalylytics().query(
                siteUrl=self.site_url,
                body=request_body
            ).execute()
            
            # Calcular métricas agregadas
            rows = response.get('rows', [])
            total_clicks = sum(row.get('clicks', 0) for row in rows)
            total_impressions = sum(row.get('impressions', 0) for row in rows)
            avg_position = sum(row.get('position', 0) for row in rows) / len(rows) if rows else 0
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            
            return {
                "success": True,
                "url": page_url,
                "metrics": {
                    "clicks": total_clicks,
                    "impressions": total_impressions,
                    "ctr": round(ctr, 2),
                    "position": round(avg_position, 1)
                },
                "queries": rows[:10],  # Top 10 queries
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _mock_data(self, page_url: str) -> Dict:
        """Datos de ejemplo para desarrollo sin API configurada"""
        return {
            "success": True,
            "url": page_url,
            "is_mock": True,
            "metrics": {
                "clicks": 0,
                "impressions": 0,
                "ctr": 0.0,
                "position": 0.0
            },
            "queries": [],
            "period": {
                "start": (datetime.now() - timedelta(days=30)).date().isoformat(),
                "end": datetime.now().date().isoformat()
            },
            "message": "Datos de ejemplo. Configura GOOGLE_CREDENTIALS_FILE para datos reales."
        }
    
    async def get_top_queries(self, limit: int = 20) -> Dict:
        """Obtiene las queries más populares"""
        if not self.client:
            return {
                "success": False,
                "error": "Google Search Console no configurado"
            }
        
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)
            
            request_body = {
                'startDate': start_date.isoformat(),
                'endDate': end_date.isoformat(),
                'dimensions': ['query'],
                'rowLimit': limit
            }
            
            response = self.client.searchanalytics().query(
                siteUrl=self.site_url,
                body=request_body
            ).execute()
            
            return {
                "success": True,
                "queries": response.get('rows', [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_articles_performance(self, article_urls: List[str]) -> Dict:
        """
        Obtiene métricas de múltiples artículos
        
        Args:
            article_urls: Lista de URLs de artículos
        
        Returns:
            Métricas consolidadas de todos los artículos
        """
        results = {
            "total_articles": len(article_urls),
            "articles": [],
            "summary": {
                "total_clicks": 0,
                "total_impressions": 0,
                "avg_ctr": 0.0,
                "avg_position": 0.0
            }
        }
        
        for url in article_urls:
            metrics = await self.get_page_performance(url)
            
            if metrics["success"]:
                results["articles"].append({
                    "url": url,
                    "metrics": metrics.get("metrics", {}),
                    "is_mock": metrics.get("is_mock", False)
                })
                
                # Acumular para summary
                m = metrics.get("metrics", {})
                results["summary"]["total_clicks"] += m.get("clicks", 0)
                results["summary"]["total_impressions"] += m.get("impressions", 0)
        
        # Calcular promedios
        if results["articles"]:
            results["summary"]["avg_ctr"] = round(
                sum(a["metrics"].get("ctr", 0) for a in results["articles"]) / len(results["articles"]),
                2
            )
            results["summary"]["avg_position"] = round(
                sum(a["metrics"].get("position", 0) for a in results["articles"]) / len(results["articles"]),
                1
            )
        
        return results
