"""
Generador de artículos en batch
"""
from typing import List, Dict
import asyncio
from datetime import datetime
import json


class BatchArticleGenerator:
    """Genera múltiples artículos para el mismo dispositivo"""
    
    def __init__(self, pdf_processor, article_generator, affiliate_linker):
        self.pdf_processor = pdf_processor
        self.article_generator = article_generator
        self.affiliate_linker = affiliate_linker
    
    async def generate_multiple_articles(
        self,
        pdf_url: str,
        model: str,
        errors: List[str],
        publish_status: str = "draft"
    ) -> Dict:
        """
        Genera múltiples artículos para diferentes errores del mismo dispositivo
        
        Args:
            pdf_url: URL del manual PDF
            model: Modelo del dispositivo
            errors: Lista de errores a procesar
            publish_status: Estado de publicación (draft/publish)
        
        Returns:
            Resultados de generación de todos los artículos
        """
        results = {
            "total": len(errors),
            "successful": 0,
            "failed": 0,
            "articles": [],
            "errors_log": [],
            "started_at": datetime.now().isoformat(),
        }
        
        try:
            # Procesar PDF una sola vez
            print(f"📄 Procesando PDF: {pdf_url}")
            pdf_result = await self.pdf_processor.process_pdf(pdf_url)
            
            if not pdf_result["success"]:
                results["errors_log"].append({
                    "error": "PDF processing failed",
                    "detail": "No se pudo procesar el PDF"
                })
                return results
            
            chunks = pdf_result["chunks"]
            print(f"✅ PDF procesado: {len(chunks)} chunks")
            
            # Generar artículos para cada error
            for i, error in enumerate(errors, 1):
                print(f"🤖 Generando artículo {i}/{len(errors)}: {error}")
                
                try:
                    # Generar artículo
                    article_result = await self.article_generator.generate_article(
                        chunks=chunks,
                        error=error,
                        model=model
                    )
                    
                    if not article_result["success"]:
                        results["failed"] += 1
                        results["errors_log"].append({
                            "error": error,
                            "detail": "Failed to generate article"
                        })
                        continue
                    
                    # Parsear respuesta
                    article_content = self.article_generator.parse_llm_response(
                        article_result["result"]
                    )
                    
                    # Procesar productos
                    recommended_products = article_content.get("recommended_products", [])
                    affiliate_products = self.affiliate_linker.process_products(recommended_products)
                    
                    # Guardar artículo generado
                    article = {
                        "error": error,
                        "title": article_content.get("title", f"Error: {error}"),
                        "content": {
                            "introduction": article_content.get("introduction", ""),
                            "error_meaning": article_content.get("error_meaning", ""),
                            "diagnosis": article_content.get("diagnosis", ""),
                            "solution_steps": article_content.get("solution_steps", []),
                            "common_failures": article_content.get("common_failures", []),
                        },
                        "affiliate_links": affiliate_products,
                        "metadata": {
                            "model": model,
                            "error": error,
                            "pdf_chunks": len(chunks),
                            "generated_at": datetime.now().isoformat()
                        },
                        "status": publish_status
                    }
                    
                    results["articles"].append(article)
                    results["successful"] += 1
                    print(f"✅ Artículo {i}/{len(errors)} generado exitosamente")
                    
                    # Pequeña pausa para no saturar la API
                    if i < len(errors):
                        await asyncio.sleep(2)
                    
                except Exception as e:
                    results["failed"] += 1
                    results["errors_log"].append({
                        "error": error,
                        "detail": str(e)
                    })
                    print(f"❌ Error generando artículo para {error}: {str(e)}")
            
            results["completed_at"] = datetime.now().isoformat()
            print(f"\n🎉 Proceso completado: {results['successful']}/{results['total']} exitosos")
            
        except Exception as e:
            results["errors_log"].append({
                "error": "Batch process failed",
                "detail": str(e)
            })
        
        return results
    
    def get_common_errors(self, device_type: str) -> List[str]:
        """
        Devuelve una lista de errores comunes por tipo de dispositivo
        
        Args:
            device_type: Tipo de dispositivo (alexa, router, smart_tv, etc.)
        
        Returns:
            Lista de errores comunes
        """
        common_errors = {
            "alexa": [
                "Error E01 - No responde a comandos de voz",
                "Error E02 - Problemas de conexión WiFi",
                "Error E03 - Fallo de comunicación con otros dispositivos",
                "Error E04 - No reproduce música",
                "Error E05 - Luz roja parpadeante",
                "Error E06 - No se enciende",
                "Error E07 - Audio distorsionado",
                "Error E08 - No reconoce el idioma",
                "Error E09 - Problemas con Bluetooth",
                "Error E10 - No actualiza firmware"
            ],
            "router": [
                "Error R01 - Sin conexión a Internet",
                "Error R02 - WiFi intermitente",
                "Error R03 - Velocidad lenta",
                "Error R04 - No asigna IP (DHCP)",
                "Error R05 - LED rojo/naranja",
                "Error R06 - No accede al panel admin",
                "Error R07 - Dispositivos no conectan",
                "Error R08 - Reinicio constante",
                "Error R09 - Puerto Ethernet no funciona",
                "Error R10 - Contraseña WiFi no acepta"
            ],
            "smart_tv": [
                "Error T01 - No enciende",
                "Error T02 - Sin señal HDMI",
                "Error T03 - No conecta a WiFi",
                "Error T04 - Apps no cargan",
                "Error T05 - Audio sin sincronizar",
                "Error T06 - Pantalla negra con sonido",
                "Error T07 - Control remoto no responde",
                "Error T08 - Rayas o líneas en pantalla",
                "Error T09 - No detecta USB",
                "Error T10 - Actualización fallida"
            ],
            "smart_home": [
                "Error S01 - Dispositivo no empareja",
                "Error S02 - Desconexión frecuente",
                "Error S03 - No responde a automatizaciones",
                "Error S04 - Sensor no reporta datos",
                "Error S05 - Batería se agota rápido",
                "Error S06 - LED no funciona",
                "Error S07 - Incompatibilidad con hub",
                "Error S08 - No aparece en app",
                "Error S09 - Retraso en ejecución",
                "Error S10 - Firmware corrupto"
            ]
        }
        
        return common_errors.get(device_type.lower(), [])
    
    async def batch_publish_to_wordpress(
        self,
        articles: List[Dict],
        wordpress_client
    ) -> Dict:
        """
        Publica múltiples artículos en WordPress
        
        Args:
            articles: Lista de artículos generados
            wordpress_client: Cliente de WordPress
        
        Returns:
            Resultados de publicación
        """
        results = {
            "total": len(articles),
            "successful": 0,
            "failed": 0,
            "published": [],
            "errors": []
        }
        
        for i, article in enumerate(articles, 1):
            try:
                print(f"📝 Publicando artículo {i}/{len(articles)}: {article['title']}")
                
                result = await wordpress_client.publish_article(
                    title=article["title"],
                    article_content=article["content"],
                    affiliate_links=article["affiliate_links"],
                    error=article["metadata"]["error"],
                    model=article["metadata"]["model"],
                    status=article.get("status", "draft")
                )
                
                if result["success"]:
                    results["successful"] += 1
                    results["published"].append({
                        "title": article["title"],
                        "url": result.get("url", ""),
                        "post_id": result.get("post_id", 0)
                    })
                    print(f"✅ Publicado: {article['title']}")
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "title": article["title"],
                        "error": result.get("error", "Unknown error")
                    })
                
                # Pausa entre publicaciones
                if i < len(articles):
                    await asyncio.sleep(1)
                    
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "title": article["title"],
                    "error": str(e)
                })
                print(f"❌ Error publicando {article['title']}: {str(e)}")
        
        return results
