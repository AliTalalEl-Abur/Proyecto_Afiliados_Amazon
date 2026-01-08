# Fase 4: Generación en Batch y Monitorización de Tráfico

## 📋 Descripción General

La Fase 4 implementa dos funcionalidades clave:
1. **Generación en Batch**: Crear 5-10 artículos automáticamente para el mismo dispositivo
2. **Monitorización de Tráfico**: Integración con Google Search Console para ver impresiones, clics, CTR y posicionamiento

## 🎯 Funcionalidades Implementadas

### 1. Generación en Batch

#### Backend: `batch_generator.py`
```python
# Generador de múltiples artículos
class BatchArticleGenerator:
    - generate_multiple_articles() # Genera artículos para lista de errores
    - batch_publish_to_wordpress() # Publica todos en WordPress
    - get_common_errors() # Obtiene errores comunes por tipo de dispositivo
```

#### API Endpoints

**POST /batch_generate**
```json
{
  "pdf_url": "https://ejemplo.com/manual.pdf",
  "model": "Echo Dot 4",
  "errors": ["Error E01", "Error E02", "Error E03"],
  "device_type": "alexa",
  "use_common_errors": false
}
```

Respuesta:
```json
{
  "total": 3,
  "successful": 3,
  "failed": 0,
  "articles": [
    {
      "title": "Cómo solucionar Error E01...",
      "content": {...},
      "affiliate_links": [...],
      "metadata": {...}
    }
  ],
  "errors_log": []
}
```

**POST /batch_publish**
Publica múltiples artículos en WordPress de una sola vez.

**GET /device_types**
Obtiene tipos de dispositivos soportados y sus errores comunes.

### 2. Monitorización de Tráfico

#### Backend: `search_console_client.py`
```python
class SearchConsoleClient:
    - get_site_metrics() # Métricas generales del sitio
    - get_page_performance() # Métricas de página específica
```

#### API Endpoints

**GET /metrics/site?days=30**
```json
{
  "impressions": 1500,
  "clicks": 45,
  "ctr": 0.03,
  "position": 8.5
}
```

**GET /metrics/page?url=...&days=30**
```json
{
  "url": "https://...",
  "impressions": 120,
  "clicks": 8,
  "ctr": 0.067,
  "position": 4.2
}
```

## 🖼️ Componentes Frontend

### BatchGenerator.js
- Formulario para ingresar URL del PDF, modelo del dispositivo
- Selector de tipo de dispositivo (usa errores comunes)
- Campo para errores personalizados (máx 10)
- Barra de progreso durante generación
- Validación de formulario

### BatchResults.js
- Resumen de artículos generados (exitosos/fallidos)
- Lista de todos los artículos con vista previa
- Botones para:
  - Publicar todos en WordPress
  - Descargar JSON
  - Nueva generación

### MetricsDashboard.js
- Métricas del sitio (impresiones, clics, CTR, posición)
- Búsqueda de página específica
- Selector de período (7, 30, 90 días)
- Visualización con cards coloridas
- Información contextual

## 🔧 Configuración Requerida

### Google Search Console

Para usar las métricas de Search Console, necesitas:

1. **Crear un proyecto en Google Cloud Console**
   - Ve a https://console.cloud.google.com
   - Crea un nuevo proyecto
   - Habilita la API de Google Search Console

2. **Crear credenciales OAuth2**
   - Tipo: Aplicación de escritorio (Desktop)
   - Descargar JSON de credenciales
   - Guardar en `backend/.env` como `GSC_CREDENTIALS_JSON`

3. **Autorizar el sitio**
   ```bash
   # Se abrirá una ventana del navegador para autorizar
   python backend/agents/search_console_client.py
   ```

4. **Configurar en .env**
   ```env
   GSC_SITE_URL=https://tudominio.com
   GSC_CREDENTIALS_JSON={"type": "service_account", ...}
   ```

### WordPress (para publicación en batch)

Asegúrate que tienes configurado:
```env
WORDPRESS_URL=https://tudominio.com
WORDPRESS_USER=tu_usuario
WORDPRESS_APP_PASSWORD=tu_contraseña_app
```

## 📊 Errores Comunes por Dispositivo

### Amazon Alexa / Echo
- Error E01 - No responde a comandos de voz
- Error E02 - Problemas de conexión WiFi
- Error E03 - Fallo de comunicación con otros dispositivos
- Error E04 - No reproduce música
- ... (10 total)

### Router WiFi
- Error R01 - Sin conexión a Internet
- Error R02 - WiFi intermitente
- Error R03 - Velocidad lenta
- ... (10 total)

### Smart TV
- Error T01 - No enciende
- Error T02 - Sin señal HDMI
- Error T03 - No conecta a WiFi
- ... (10 total)

### Dispositivos Smart Home
- Error S01 - Dispositivo no empareja
- Error S02 - Desconexión frecuente
- ... (10 total)

## 🚀 Flujo de Uso

### Generación en Batch

1. **Navega a "🚀 Generación en Batch"**
2. **Ingresa los datos**:
   - URL del manual PDF
   - Modelo del dispositivo
   - Selecciona tipo de dispositivo (opcional, para errores comunes)
3. **Selecciona errores**:
   - Opción A: Usar errores comunes del tipo
   - Opción B: Especificar errores personalizados
4. **Haz clic en "Generar Artículos"**
5. **Espera a que se complete** (muestra progreso)
6. **Revisa los resultados**
7. **Publica en WordPress** o descarga como JSON

### Monitorización de Tráfico

1. **Navega a "📊 Métricas"**
2. **Selecciona período** (7, 30, 90 días)
3. **Ve métricas del sitio**:
   - Impresiones totales
   - Clics totales
   - CTR promedio
   - Posición media
4. **Busca página específica**:
   - Ingresa URL completa
   - Obtén métricas de esa página
5. **Analiza el rendimiento**

## 📈 Interpretación de Métricas

### Impresiones
Número de veces que tu contenido aparece en búsquedas. Más impresiones = mejor posicionamiento.

### Clics
Número de usuarios que hacen clic. Refleja si el título es atractivo.

### CTR (Click-Through Rate)
Porcentaje de clics vs impresiones. 
- 1-3% es típico
- >5% es excelente
- <1% indica problemas con el título o descripción

### Posición Media
Puesto promedio en resultados.
- Posición 1-3: Excelente
- Posición 4-10: Bueno
- Posición 10+: Necesita mejora

## 🔄 Integración con Fases Anteriores

### Fase 1: Generación de Artículos
- Reutiliza ArticleGenerator para crear múltiples artículos
- Usa PDFProcessor para procesar el PDF una sola vez
- Aplica AffiliateLinker a cada artículo

### Fase 2: Frontend
- Nuevas pestañas para Batch y Métricas
- Componentes reutilizables para mostrar resultados
- API service actualizado con nuevos endpoints

### Fase 3: WordPress
- BatchGenerator usa WordPressClient
- Publica múltiples artículos automáticamente
- Maneja errores de publicación

## 🛠️ Troubleshooting

### Error: "PDF no se procesa en batch"
```bash
# Verifica que la URL sea accesible
curl "https://ejemplo.com/manual.pdf"
# Asegúrate que no hay timeout
```

### Error: "Google Search Console no responde"
```bash
# Verifica las credenciales OAuth2
python -c "from agents.search_console_client import SearchConsoleClient; print('OK')"

# Revisa que el sitio esté verificado en GSC
# https://search.google.com/search-console
```

### Error: "WordPress no publica artículos en batch"
```bash
# Verifica credenciales
curl -u "usuario:contraseña" https://tudominio.com/wp-json/wp/v2/posts

# Prueba un artículo individual primero
```

## 📚 API Documentation

Accede a la documentación interactiva en:
```
http://localhost:8000/docs
```

## 🎓 Próximos Pasos

### Fase 5: Automatización (Futuro)
- Cron jobs para generación automática
- Alertas cuando CTR baja
- Recomendaciones de mejora basadas en métricas

### Optimizaciones
- Caché de PDFs procesados
- Batch processing más eficiente
- Soporte para múltiples sitios

## 📝 Notas Importantes

1. **Límite de 10 artículos**: Por seguridad y costos de API
2. **PDF se procesa una sola vez**: Optimización de rendimiento
3. **Google Search Console**: Necesita 24-48h para mostrar datos
4. **Métricas de página**: Requiere que Google haya indexado la URL
5. **Estado de artículos**: Se generan como "draft" por defecto

---

¡Fase 4 completada! 🎉

Ahora tu plataforma puede:
✅ Generar 5-10 artículos en lote
✅ Publicar todos automáticamente en WordPress
✅ Monitorizar tráfico y SEO desde Google Search Console
