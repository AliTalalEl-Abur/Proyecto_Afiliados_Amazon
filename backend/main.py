from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from dotenv import load_dotenv
import os
import sys

# Añadir path para importar módulos locales
sys.path.append(os.path.dirname(__file__))

from agents.pdf_processor import PDFProcessor
from agents.article_generator import ArticleGenerator
from agents.affiliate_linker import AffiliateLinker
from agents.wordpress_client import WordPressClient

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="API de Ayuda Técnica",
    description="Sistema de generación automática de artículos con IA",
    version="1.0.0"
)

# Configurar CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar componentes
pdf_processor = PDFProcessor()
article_generator = ArticleGenerator()
affiliate_linker = AffiliateLinker()

# WordPress client (opcional, solo si está configurado)
try:
    wordpress_client = WordPressClient()
    wordpress_enabled = True
except ValueError:
    wordpress_client = None
    wordpress_enabled = False


# Modelos de datos
class GenerateArticleRequest(BaseModel):
    """Request para generar artículo"""
    pdf_url: Optional[str] = Field(None, description="URL del PDF del manual técnico")
    error: str = Field(..., description="Error o problema reportado")
    model: str = Field(..., description="Modelo del producto")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "pdf_url": "https://example.com/manual.pdf",
                "error": "Error E03 - Fallo de comunicación",
                "model": "Alexa Echo Dot 4"
            }]
        }
    }


class ArticleResponse(BaseModel):
    """Response con el artículo generado"""
    success: bool
    title: str
    content: Dict
    affiliate_links: List[Dict]
    metadata: Dict


class PublishToWordPressRequest(BaseModel):
    """Request para publicar artículo en WordPress"""
    post_id: Optional[int] = Field(None, description="ID del post existente para actualizar")
    title: str = Field(..., description="Título del artículo")
    content: Dict = Field(..., description="Contenido estructurado del artículo")
    affiliate_links: List[Dict] = Field(..., description="Enlaces de afiliado")
    error: str = Field(..., description="Error procesado")
    model: str = Field(..., description="Modelo del dispositivo")
    status: str = Field("draft", description="'draft' o 'publish'")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "title": "Cómo solucionar el Error E03",
                "content": {"introduction": "...", "error_meaning": "..."},
                "affiliate_links": [],
                "error": "Error E03",
                "model": "Echo Dot 4",
        "wordpress_configured": wordpress_enabled,
                "status": "draft"
            }]
        }
    }


@app.get("/")
async def root():
    return {
        "message": "API de Ayuda Técnica funcionando",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/generate_article": "POST - Generar artículo técnico"
        }
    }


@app.get("/health")
async def health_check():
    """Verifica el estado de la API y dependencias"""
    checks = {
        "api": "healthy",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
    }
    
    all_healthy = all(v == "healthy" or v == True for v in checks.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks
    }


@app.post("/generate_article", response_model=ArticleResponse)
async def generate_article(request: GenerateArticleRequest):
    """
    Genera un artículo técnico completo basado en un manual PDF y un error reportado.
    
    - **pdf_url**: URL del manual técnico en PDF
    - **error**: Descripción del error o problema
    - **model**: Modelo del producto
    
    Returns un artículo con título, contenido estructurado y enlaces de afiliado.
    """
    try:
        # 1. Validar que hay PDF
        if not request.pdf_url:
            raise HTTPException(
                status_code=400,
                detail="Se requiere pdf_url para generar el artículo"
            )
        
        # 2. Procesar PDF
        pdf_result = await pdf_processor.process_pdf(request.pdf_url)
        
        if not pdf_result["success"]:
            raise HTTPException(
                status_code=400,
                detail="Error al procesar el PDF"
            )
        
        # 3. Generar artículo con LangChain RAG
        article_result = await article_generator.generate_article(
            chunks=pdf_result["chunks"],
            error=request.error,
            model=request.model
        )
        
        if not article_result["success"]:
            raise HTTPException(
                status_code=500,
                detail="Error al generar el artículo"
            )
        
        # 4. Parsear respuesta del LLM
        article_content = article_generator.parse_llm_response(
            article_result["result"]
        )
        
        # 5. Procesar productos y crear enlaces de afiliado
        recommended_products = article_content.get("recommended_products", [])
        affiliate_products = affiliate_linker.process_products(recommended_products)
        
        # 6. Construir respuesta
        response = ArticleResponse(
            success=True,
            title=article_content.get("title", "Artículo Técnico"),
            content={
                "introduction": article_content.get("introduction", ""),
                "error_meaning": article_content.get("error_meaning", ""),
                "diagnosis": article_content.get("diagnosis", ""),
                "solution_steps": article_content.get("solution_steps", []),
                "common_failures": article_content.get("common_failures", []),
            },
            affiliate_links=affiliate_products,
            metadata={
                "model": request.model,
                "error": request.error,
                "pdf_chunks": pdf_result["num_chunks"],
                "text_length": pdf_result["text_length"]
            }
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint para subir PDF directamente (alternativa a URL)
    """
    try:
        # Guardar archivo temporal
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Procesar PDF
        result = await pdf_processor.process_pdf(tmp_path)
        
        # Limpiar archivo temporal
        os.unlink(tmp_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "num_chunks": result["num_chunks"],
            "text_length": result["text_length"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
         


@app.post("/publish_to_wordpress")
async def publish_to_wordpress(request: PublishToWordPressRequest):
    """
    Publica un artículo en WordPress como borrador o publicado
    
    Requiere configuración en .env:
    - WORDPRESS_URL
    - WORDPRESS_USER
    - WORDPRESS_APP_PASSWORD
    """
    try:
        if not wordpress_enabled:
            raise HTTPException(
                status_code=503,
                detail="WordPress no está configurado. Verifica las variables de entorno."
            )
        
        # Publicar en WordPress
        result = await wordpress_client.publish_article(
            title=request.title,
            article_content=request.content,
            affiliate_links=request.affiliate_links,
            error=request.error,
            model=request.model,
            status=request.status
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al publicar en WordPress: {str(e)}"
        )   detail=f"Error al procesar el archivo: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
