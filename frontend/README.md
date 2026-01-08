# Frontend - Fase 2

## Componentes Implementados

### 1. ArticleGenerator
Formulario para generar artículos con:
- Selector de modo: URL o archivo local
- Input para URL del PDF
- Input para error/problema
- Input para modelo del dispositivo
- Validación de campos
- Estado de carga con spinner

### 2. ArticleResult
Visualización de artículos generados con:
- Título y contenido estructurado
- Secciones: introducción, diagnóstico, solución, fallos comunes
- Productos recomendados con enlaces de afiliado
- Selector de formato (HTML/Markdown)
- Botón de copiar al portapapeles
- Botón de descarga
- Metadata del proceso

### 3. API Service
Conexión con el backend FastAPI:
- Health check
- Generación de artículos
- Subida de PDFs

## Estructura de archivos

```
frontend/src/
├── components/
│   ├── ArticleGenerator.js       # Formulario principal
│   ├── ArticleGenerator.css      # Estilos del formulario
│   ├── ArticleResult.js          # Visualización de resultados
│   └── ArticleResult.css         # Estilos de resultados
├── services/
│   └── api.js                    # Servicio de API
├── App.js                        # Componente principal
├── App.css                       # Estilos globales
└── index.js                      # Punto de entrada
```

## Características

### ✨ Generación de Artículos
- Formulario intuitivo con validación
- Soporte para URL de PDF (archivo local próximamente)
- Feedback visual durante la generación
- Manejo de errores

### 📄 Visualización
- Preview completo del artículo generado
- Formato estructurado y legible
- Tarjetas de productos con enlaces de afiliado
- Metadata del proceso

### 💾 Exportación
- **Copiar al portapapeles**: HTML o Markdown
- **Descargar**: Archivo .html o .md
- **Formatos soportados**:
  - HTML: Listo para pegar en WordPress/editores
  - Markdown: Para blogs que soporten MD

### 🎨 Interfaz
- Diseño moderno y responsive
- Gradientes y animaciones suaves
- Indicador de estado de API
- Experiencia de usuario optimizada

## Ejecutar el Frontend

```bash
cd frontend
npm start
```

La aplicación se abrirá en: http://localhost:3000

## Variables de Entorno

Archivo `.env` en `/frontend`:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Flujo de Uso

1. **Verificar conexión**: El header muestra el estado de la API
2. **Completar formulario**:
   - Proporcionar URL del manual PDF
   - Describir el error/problema
   - Especificar modelo del dispositivo
3. **Generar**: Clic en "Generar Artículo" (10-30 segundos)
4. **Revisar**: El artículo se muestra con formato profesional
5. **Exportar**:
   - Seleccionar formato (HTML/Markdown)
   - Copiar al portapapeles o descargar
   - Pegar en WordPress/blog

## Próximas Mejoras

- [ ] Subida de archivos PDF locales
- [ ] Publicación directa a WordPress vía API
- [ ] Historial de artículos generados
- [ ] Editor en línea para ajustes
- [ ] Templates de estilos personalizables
- [ ] Preview antes de exportar
- [ ] Soporte para múltiples idiomas

## Integración con WordPress

### Opción 1: Copiar y Pegar (Actual)
1. Generar artículo
2. Copiar en formato HTML
3. Pegar en WordPress usando editor de bloques o HTML

### Opción 2: API REST (Próximamente)
```javascript
// Configuración de WordPress
WORDPRESS_URL=https://tublog.com
WORDPRESS_USER=admin
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

El sistema publicará automáticamente usando la API REST de WordPress.

## Troubleshooting

### "API desconectada"
- Verifica que el backend esté ejecutándose: `python backend/main.py`
- Comprueba la URL en `.env`: `REACT_APP_API_URL`

### Error CORS
- El backend debe tener configurado CORS para http://localhost:3000
- Verificar `CORS_ORIGINS` en `backend/.env`

### No se copia al portapapeles
- Usar navegador moderno (Chrome, Firefox, Edge)
- HTTPS requerido en producción (localhost funciona)
