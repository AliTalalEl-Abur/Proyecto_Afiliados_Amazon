# Test del Backend - Fase 1

## Ejecutar el servidor

```bash
cd backend
python main.py
```

El servidor estará disponible en: http://localhost:8000

## Documentación automática

FastAPI genera documentación interactiva automáticamente:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints disponibles

### 1. Health Check
```bash
GET http://localhost:8000/health
```

### 2. Generar Artículo (Endpoint principal)
```bash
POST http://localhost:8000/generate_article
Content-Type: application/json

{
  "pdf_url": "https://example.com/manual.pdf",
  "error": "Error E03 - Fallo de comunicación",
  "model": "Alexa Echo Dot 4"
}
```

### 3. Subir PDF directamente
```bash
POST http://localhost:8000/upload_pdf
Content-Type: multipart/form-data

file: [seleccionar archivo PDF]
```

## Test con cURL

```bash
# Health check
curl http://localhost:8000/health

# Generar artículo
curl -X POST http://localhost:8000/generate_article \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

## Test con Python

```python
import requests

# Generar artículo
response = requests.post(
    "http://localhost:8000/generate_article",
    json={
        "pdf_url": "https://example.com/manual.pdf",
        "error": "Error E03 - Fallo de comunicación",
        "model": "Amazon Echo Dot 4"
    }
)

print(response.json())
```

## Estructura de respuesta esperada

```json
{
  "success": true,
  "title": "Cómo solucionar el Error E03 en Amazon Echo Dot 4",
  "content": {
    "introduction": "...",
    "error_meaning": "...",
    "diagnosis": "...",
    "solution_steps": ["paso 1", "paso 2", "..."],
    "common_failures": ["fallo 1", "fallo 2"]
  },
  "affiliate_links": [
    {
      "name": "Producto 1",
      "type": "tipo",
      "reason": "por qué es útil",
      "affiliate_link": "https://www.amazon.es/s?k=...&tag=tuafiliado-21",
      "search_term": "producto tipo"
    }
  ],
  "metadata": {
    "model": "Amazon Echo Dot 4",
    "error": "Error E03 - Fallo de comunicación",
    "pdf_chunks": 15,
    "text_length": 12500
  }
}
```

## Notas importantes

1. **PDF de prueba**: Necesitas un PDF real de manual técnico. Puedes usar:
   - Manual de Alexa
   - Manual de router WiFi
   - Manual de dispositivo domótico

2. **OpenAI API Key**: Asegúrate de que tu key esté configurada en `.env`

3. **Costos**: Cada llamada usa GPT-4o + embeddings, estima ~$0.01-0.05 por artículo

4. **Timeout**: La generación puede tardar 10-30 segundos dependiendo del tamaño del PDF
