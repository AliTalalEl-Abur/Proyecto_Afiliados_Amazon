"""
Cliente para interactuar con WordPress REST API
"""
import httpx
import os
from typing import Dict, Optional, List
import base64
from datetime import datetime


class WordPressClient:
    """Cliente para publicar artículos en WordPress"""
    
    def __init__(self):
        self.site_url = os.getenv("WORDPRESS_URL", "https://ejemplo.com")
        self.username = os.getenv("WORDPRESS_USER", "")
        self.app_password = os.getenv("WORDPRESS_APP_PASSWORD", "")
        
        # Validar credenciales
        if not self.site_url or not self.username or not self.app_password:
            raise ValueError(
                "Credenciales de WordPress no configuradas. "
                "Verifica WORDPRESS_URL, WORDPRESS_USER y WORDPRESS_APP_PASSWORD en .env"
            )
        
        self.api_url = f"{self.site_url}/wp-json/wp/v2"
        self.auth_header = self._get_auth_header()
    
    def _get_auth_header(self) -> str:
        """Genera header de autenticación Basic Auth"""
        credentials = f"{self.username}:{self.app_password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"
    
    async def get_categories(self) -> List[Dict]:
        """Obtiene todas las categorías de WordPress"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/categories",
                    headers={"Authorization": self.auth_header}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"Error al obtener categorías: {str(e)}")
    
    async def create_category(self, name: str, description: str = "") -> Dict:
        """Crea una nueva categoría"""
        try:
            data = {
                "name": name,
                "description": description,
                "slug": name.lower().replace(" ", "-")
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/categories",
                    headers={"Authorization": self.auth_header},
                    json=data
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"Error al crear categoría: {str(e)}")
    
    async def get_or_create_category(self, name: str) -> int:
        """Obtiene categoría por nombre o la crea si no existe"""
        try:
            categories = await self.get_categories()
            
            # Buscar categoría existente
            for cat in categories:
                if cat["name"].lower() == name.lower():
                    return cat["id"]
            
            # Crear categoría si no existe
            new_cat = await self.create_category(name)
            return new_cat["id"]
        except Exception as e:
            raise Exception(f"Error al obtener/crear categoría: {str(e)}")
    
    async def create_post(
        self,
        title: str,
        content: str,
        excerpt: str = "",
        status: str = "draft",
        categories: List[int] = None,
        featured_image_url: Optional[str] = None,
        meta: Optional[Dict] = None
    ) -> Dict:
        """
        Crea un post en WordPress
        
        Args:
            title: Título del post
            content: Contenido HTML del post
            excerpt: Extracto/descripción corta
            status: 'draft' o 'publish'
            categories: Lista de IDs de categorías
            featured_image_url: URL de imagen destacada
            meta: Metadatos adicionales (SEO, etc)
        
        Returns:
            Información del post creado
        """
        try:
            post_data = {
                "title": title,
                "content": content,
                "excerpt": excerpt,
                "status": status,
                "comment_status": "open",
                "ping_status": "open"
            }
            
            # Añadir categorías
            if categories:
                post_data["categories"] = categories
            
            # Añadir metadatos
            if meta:
                post_data["meta"] = meta
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/posts",
                    headers={"Authorization": self.auth_header},
                    json=post_data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"Error al crear post: {str(e)}")
    
    async def update_post(
        self,
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[str] = None,
        meta: Optional[Dict] = None
    ) -> Dict:
        """Actualiza un post existente"""
        try:
            update_data = {}
            
            if title is not None:
                update_data["title"] = title
            if content is not None:
                update_data["content"] = content
            if status is not None:
                update_data["status"] = status
            if meta is not None:
                update_data["meta"] = meta
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/posts/{post_id}",
                    headers={"Authorization": self.auth_header},
                    json=update_data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"Error al actualizar post: {str(e)}")
    
    async def get_post(self, post_id: int) -> Dict:
        """Obtiene información de un post"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/posts/{post_id}",
                    headers={"Authorization": self.auth_header}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"Error al obtener post: {str(e)}")
    
    def format_for_wordpress(
        self,
        title: str,
        content: Dict,
        affiliate_links: List[Dict]
    ) -> str:
        """Formatea artículo generado para WordPress HTML"""
        
        html = f"<h1>{title}</h1>\n\n"
        
        # Introducción
        if content.get("introduction"):
            html += f"<p><strong>{content['introduction']}</strong></p>\n\n"
        
        # Significado del error
        if content.get("error_meaning"):
            html += "<h2>¿Qué significa este error?</h2>\n"
            html += f"<p>{content['error_meaning']}</p>\n\n"
        
        # Diagnóstico
        if content.get("diagnosis"):
            html += "<h2>Diagnóstico</h2>\n"
            html += f"<p>{content['diagnosis']}</p>\n\n"
        
        # Solución paso a paso
        if content.get("solution_steps"):
            html += "<h2>Solución paso a paso</h2>\n<ol>\n"
            for step in content["solution_steps"]:
                html += f"<li>{step}</li>\n"
            html += "</ol>\n\n"
        
        # Fallos comunes
        if content.get("common_failures"):
            html += "<h2>Fallos comunes relacionados</h2>\n<ul>\n"
            for failure in content["common_failures"]:
                html += f"<li>{failure}</li>\n"
            html += "</ul>\n\n"
        
        # Productos recomendados
        if affiliate_links:
            html += "<h2>Productos recomendados</h2>\n"
            html += "<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;'>\n"
            
            for product in affiliate_links:
                html += f"""<div style='padding: 1.5rem; border: 2px solid #e0e0e0; border-radius: 8px;'>
                <h3>{product.get('name', 'Producto')}</h3>
                <p style='color: #666; font-size: 0.9rem;'>{product.get('type', '')}</p>
                <p>{product.get('reason', '')}</p>
                <a href="{product.get('affiliate_link', '#')}" target="_blank" rel="noopener noreferrer" 
                   style='display: inline-block; padding: 0.75rem 1.5rem; background: #f39c12; color: white; 
                   text-decoration: none; border-radius: 6px; font-weight: bold;'>
                   Ver en Amazon →
                </a>
            </div>\n"""
            
            html += "</div>\n"
        
        return html
    
    async def publish_article(
        self,
        title: str,
        article_content: Dict,
        affiliate_links: List[Dict],
        error: str,
        model: str,
        status: str = "draft"
    ) -> Dict:
        """
        Publica un artículo completo en WordPress
        
        Args:
            title: Título del artículo
            article_content: Contenido estructurado del artículo
            affiliate_links: Enlaces de productos con afiliado
            error: Error procesado
            model: Modelo del dispositivo
            status: 'draft' o 'publish'
        
        Returns:
            Información del post publicado
        """
        try:
            # Obtener o crear categoría
            category_id = await self.get_or_create_category("Ayuda técnica")
            
            # Formatear contenido para WordPress
            content_html = self.format_for_wordpress(
                title,
                article_content,
                affiliate_links
            )
            
            # Preparar excerpt
            excerpt = article_content.get("introduction", "")[:160]
            
            # Metadatos SEO
            meta = {
                "error_type": error,
                "device_model": model,
                "_yoast_wpseo_metadesc": excerpt,
            }
            
            # Crear post
            result = await self.create_post(
                title=title,
                content=content_html,
                excerpt=excerpt,
                status=status,
                categories=[category_id],
                meta=meta
            )
            
            return {
                "success": True,
                "post_id": result["id"],
                "url": result.get("link", ""),
                "status": result.get("status", ""),
                "message": f"Artículo {'publicado' if status == 'publish' else 'guardado como borrador'} exitosamente"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
