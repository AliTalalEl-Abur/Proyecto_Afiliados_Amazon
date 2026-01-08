"""
Sistema de enlaces de afiliado de Amazon
"""
from typing import List, Dict
from urllib.parse import quote
import os


class AffiliateLinker:
    """Genera enlaces de afiliado de Amazon para productos"""
    
    def __init__(self):
        # Tag de afiliado (configurar en .env)
        self.affiliate_tag = os.getenv("AMAZON_AFFILIATE_TAG", "tuafiliado-21")
        self.amazon_base_url = "https://www.amazon.es"
    
    def create_affiliate_link(self, product_name: str, search_term: str = None) -> str:
        """
        Crea enlace de afiliado de Amazon
        
        Args:
            product_name: Nombre del producto
            search_term: Término de búsqueda específico (opcional)
        
        Returns:
            URL de afiliado de Amazon
        """
        search = search_term if search_term else product_name
        encoded_search = quote(search)
        
        # Formato: https://www.amazon.es/s?k=PRODUCTO&tag=AFFILIATE_TAG
        affiliate_url = f"{self.amazon_base_url}/s?k={encoded_search}&tag={self.affiliate_tag}"
        
        return affiliate_url
    
    def create_direct_product_link(self, asin: str) -> str:
        """
        Crea enlace directo a producto con ASIN
        
        Args:
            asin: Amazon Standard Identification Number
        
        Returns:
            URL de producto con tag de afiliado
        """
        return f"{self.amazon_base_url}/dp/{asin}?tag={self.affiliate_tag}"
    
    def process_products(self, products: List[Dict]) -> List[Dict]:
        """
        Procesa lista de productos y añade enlaces de afiliado
        
        Args:
            products: Lista de productos con estructura:
                [{"name": "...", "type": "...", "reason": "..."}]
        
        Returns:
            Lista de productos con enlaces de afiliado añadidos
        """
        processed_products = []
        
        for product in products:
            product_name = product.get("name", "")
            product_type = product.get("type", "")
            
            # Crear término de búsqueda optimizado
            search_term = f"{product_name} {product_type}".strip()
            
            processed_product = {
                **product,
                "affiliate_link": self.create_affiliate_link(product_name, search_term),
                "search_term": search_term
            }
            
            processed_products.append(processed_product)
        
        return processed_products
    
    def get_category_recommendations(self, category: str) -> List[Dict]:
        """
        Devuelve productos recomendados por categoría
        
        Args:
            category: Categoría de producto (ej: "herramientas", "cables", "repuestos")
        
        Returns:
            Lista de productos recomendados con enlaces
        """
        # Base de datos simple de productos comunes
        category_products = {
            "herramientas": [
                {"name": "Multímetro digital", "type": "herramienta diagnóstico", "asin": ""},
                {"name": "Destornillador de precisión", "type": "kit herramientas", "asin": ""},
                {"name": "Alicate pelacables", "type": "herramienta", "asin": ""}
            ],
            "cables": [
                {"name": "Cable HDMI 2.1", "type": "cable", "asin": ""},
                {"name": "Cable Ethernet Cat 6", "type": "cable red", "asin": ""},
                {"name": "Cable USB-C", "type": "cable carga", "asin": ""}
            ],
            "domotica": [
                {"name": "Hub Zigbee", "type": "controlador", "asin": ""},
                {"name": "Sensor temperatura", "type": "sensor", "asin": ""},
                {"name": "Enchufe inteligente", "type": "actuador", "asin": ""}
            ]
        }
        
        products = category_products.get(category.lower(), [])
        return self.process_products(products)
