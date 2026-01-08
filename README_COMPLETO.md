# 🚀 Proyecto Afiliados Amazon - MVP Completo

## ✨ Descripción General

Sistema completo de generación automática de artículos técnicos con IA, integración con WordPress y monitorización de tráfico mediante Google Search Console.

**Stack Tecnológico:**
- **Backend**: FastAPI + Python 3.12 + LangChain + OpenAI GPT-4o
- **Frontend**: React 18 + Axios
- **Base de datos**: SQLite
- **CMS**: WordPress REST API
- **Búsqueda**: Google Search Console API
- **Vector Store**: FAISS
- **PDF Processing**: PyMuPDF

## 📊 Estado del Proyecto

### ✅ Fases Completadas

#### Fase 1: Backend MVP con RAG
- ✅ Procesamiento de PDFs con PyMuPDF
- ✅ Extracción de chunks optimizada
- ✅ LangChain RAG con FAISS
- ✅ Generación de artículos con GPT-4o
- ✅ Sistema de enlaces de afiliado Amazon
- ✅ Endpoint: `/generate_article`

#### Fase 2: Frontend MVP
- ✅ Interfaz React moderna
- ✅ Formulario de generación
- ✅ Vista previa de artículos
- ✅ Exportación HTML/Markdown
- ✅ Copiar al portapapeles
- ✅ Descarga de JSON

#### Fase 3: Integración WordPress
- ✅ Cliente REST API de WordPress
- ✅ Publicación automática
- ✅ Manejo de categorías
- ✅ Modal de publicación
- ✅ Autenticación con App Passwords
- ✅ Endpoint: `/publish_to_wordpress`

#### Fase 4: Batch & Monitorización
- ✅ Generación de 5-10 artículos
- ✅ Errores comunes predefinidos
- ✅ Publicación en batch
- ✅ Google Search Console Integration
- ✅ Dashboard de métricas
- ✅ Endpoints: `/batch_generate`, `/batch_publish`, `/metrics/*`

## 🎯 Características Principales

### 1. Generación Individual de Artículos
```
URL PDF + Error + Modelo → Artículo Completo
                       ↓
               - Introducción
               - Significado del error
               - Diagnóstico
               - Pasos de solución
               - Productos recomendados
               - Enlaces de afiliado
```

### 2. Generación en Batch
```
[Error 1]
[Error 2] + PDF → [Artículo 1, 2, 3...]
[Error 3]       ↓
              WordPress (automático)
```

**Errores Comunes por Dispositivo:**
- Amazon Alexa / Echo: 10 errores
- Router WiFi: 10 errores  
- Smart TV: 10 errores
- Dispositivos Smart Home: 10 errores

### 3. WordPress Integration
- Publicación automática
- Gestión de categorías
- Borrador/Publicado
- Actualización de posts existentes
- Embedding de productos

### 4. Monitorización de Tráfico
Métricas en tiempo real desde Google Search Console:
- 👁️ **Impresiones**: Veces que aparece en búsquedas
- 🖱️ **Clics**: Visitas desde Google
- 📈 **CTR**: Tasa de clics (%)
- 🎯 **Posición**: Ranking promedio

## 📁 Estructura del Proyecto

```
Proyecto_Afiliados_Amazon/
├── backend/
│   ├── main.py                          # App FastAPI principal
│   ├── agents/
│   │   ├── pdf_processor.py            # Procesamiento de PDFs
│   │   ├── article_generator.py        # Generación con RAG
│   │   ├── affiliate_linker.py         # Enlaces de afiliado
│   │   ├── wordpress_client.py         # Cliente WordPress
│   │   ├── batch_generator.py          # Generación en batch
│   │   └── search_console_client.py    # Google Search Console
│   ├── requirements.txt                # Dependencias Python
│   ├── .env                            # Variables de entorno
│   └── venv/                           # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.js                      # App principal
│   │   ├── App.css                     # Estilos globales
│   │   ├── components/
│   │   │   ├── ArticleGenerator.js     # Formulario individual
│   │   │   ├── ArticleResult.js        # Resultado individual
│   │   │   ├── PublishToWordPress.js   # Modal WordPress
│   │   │   ├── BatchGenerator.js       # Formulario batch
│   │   │   ├── BatchResults.js         # Resultados batch
│   │   │   └── MetricsDashboard.js     # Dashboard métricas
│   │   └── services/
│   │       └── api.js                  # API client
│   ├── package.json
│   └── public/
├── FASE_1.md                           # Documentación Fase 1
├── FASE_2.md                           # Documentación Fase 2
├── FASE_3.md                           # Documentación Fase 3
├── FASE_4.md                           # Documentación Fase 4
├── README.md                           # Este archivo
├── SETUP.md                            # Instalación
└── WORDPRESS_SETUP.md                  # Config WordPress
```

## 🚀 Inicio Rápido

### 1. Clonar repositorio
```bash
git clone https://github.com/AliTalalEl-Abur/Proyecto_Afiliados_Amazon.git
cd Proyecto_Afiliados_Amazon
```

### 2. Configurar Backend
```bash
cd backend
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Crear archivo .env con:
OPENAI_API_KEY=sk-proj-...
WORDPRESS_URL=https://tudominio.com
WORDPRESS_USER=usuario
WORDPRESS_APP_PASSWORD=contraseña
AMAZON_AFFILIATE_TAG=tutorial-21
CORS_ORIGINS=http://localhost:3000
```

### 3. Configurar Frontend
```bash
cd frontend
npm install
```

### 4. Ejecutar
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start

# Terminal 3 - Ver documentación
# Abre http://localhost:8000/docs
```

## 📡 API Endpoints

### Generación de Artículos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/generate_article` | Generar un artículo |
| POST | `/batch_generate` | Generar múltiples artículos |
| POST | `/upload_pdf` | Subir PDF directamente |

### WordPress
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/publish_to_wordpress` | Publicar artículo |
| POST | `/batch_publish` | Publicar múltiples |

### Métricas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/metrics/site` | Métricas del sitio |
| GET | `/metrics/page` | Métricas de página |
| GET | `/device_types` | Tipos de dispositivos |

### Otros
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/docs` | Documentación Swagger |

## 🎓 Flujos de Usuario

### Flujo 1: Generar Artículo Individual
1. Ingresa URL del PDF
2. Describe el error
3. Especifica el modelo
4. Haz clic en "Generar"
5. Revisa el artículo
6. Copia, descarga o publica en WordPress

### Flujo 2: Generación en Batch
1. Selecciona tipo de dispositivo
2. Elige usar errores comunes
3. Ingresa URL del PDF
4. Haz clic en "Generar Artículos"
5. Revisa los resultados
6. Publica todos en WordPress
7. Descarga JSON si deseas

### Flujo 3: Monitorizar Tráfico
1. Ve a la pestaña "Métricas"
2. Selecciona período (7, 30, 90 días)
3. Ve impresiones, clics, CTR, posición
4. Busca página específica si quieres
5. Analiza el rendimiento

## ⚙️ Configuración Avanzada

### Google Search Console
Requiere OAuth2. Ver `FASE_4.md` para configuración.

### Amazon Affiliate Program
1. Registra tu programa de afiliados Amazon
2. Obtén tu tag de afiliado
3. Configura en `.env`:
   ```env
   AMAZON_AFFILIATE_TAG=tu_tag-21
   ```

### WordPress REST API
1. Instala plugin "Application Passwords"
2. Genera contraseña de app
3. Configura en `.env`:
   ```env
   WORDPRESS_URL=https://tudominio.com
   WORDPRESS_USER=usuario
   WORDPRESS_APP_PASSWORD=contraseña
   ```

## 📊 Ejemplos de Uso

### Ejemplo 1: Generar Artículo Individual
```bash
curl -X POST "http://localhost:8000/generate_article" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_url": "https://ejemplo.com/echo-dot.pdf",
    "error": "Echo Dot no responde a comandos de voz",
    "model": "Echo Dot 4"
  }'
```

### Ejemplo 2: Generación en Batch
```bash
curl -X POST "http://localhost:8000/batch_generate" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_url": "https://ejemplo.com/echo-dot.pdf",
    "model": "Echo Dot 4",
    "device_type": "alexa",
    "use_common_errors": true,
    "errors": []
  }'
```

### Ejemplo 3: Obtener Métricas
```bash
# Sitio completo (últimos 30 días)
curl "http://localhost:8000/metrics/site?days=30"

# Página específica
curl "http://localhost:8000/metrics/page?url=https://tudominio.com/articulo&days=30"
```

## 🔐 Seguridad

- ✅ Variables de entorno para credenciales
- ✅ CORS configurado
- ✅ App Passwords para WordPress
- ✅ OAuth2 ready para Google
- ✅ .env en .gitignore

## 🐛 Troubleshooting

### Error: "API desconectada"
```bash
# Verifica que el backend está corriendo
curl http://localhost:8000/health
```

### Error: "No puedo procesar PDF"
```bash
# Verifica que la URL es accesible
curl -I https://tu-url-del-pdf.pdf

# Verifica que OpenAI API Key es válido
echo $OPENAI_API_KEY
```

### Error: "WordPress no publica"
```bash
# Verifica credenciales
curl -u "usuario:contraseña" https://tudominio.com/wp-json/wp/v2/posts
```

## 📈 Roadmap Futuro

- [ ] Base de datos persistente completa
- [ ] Autenticación de usuarios
- [ ] Panel de admin
- [ ] Programación de publicaciones
- [ ] Integración con más CMS
- [ ] Análisis avanzado de rendimiento
- [ ] Generación de imágenes con IA
- [ ] Múltiples idiomas
- [ ] Mobile app

## 📝 Licencia

Este proyecto es de código abierto. Úsalo libremente.

## 👨‍💻 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

- 📖 Lee la documentación en el directorio raíz
- 🐛 Reporta bugs en GitHub Issues
- 💬 Discuss ideas en Discussions

## 🎉 Agradecimientos

Construido con:
- FastAPI
- React
- LangChain
- OpenAI
- WordPress
- Google Cloud

---

**Última actualización**: Fase 4 Completa ✨

¡Gracias por usar nuestro sistema! 🚀
